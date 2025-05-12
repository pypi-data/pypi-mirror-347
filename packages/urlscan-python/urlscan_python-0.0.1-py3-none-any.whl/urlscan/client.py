import contextlib
import datetime
import json
import logging
import os
import time
from dataclasses import dataclass
from io import BytesIO
from typing import Any, BinaryIO, TypedDict

import httpx
from httpx._types import QueryParamTypes, RequestData, TimeoutTypes

from ._version import version
from .error import APIError, RateLimitError, RateLimitRemainingError
from .iterator import SearchIterator
from .types import ActionType, VisibilityType
from .utils import parse_datetime

logger = logging.getLogger("urlscan-python")

BASE_URL = os.environ.get("URLSCAN_BASE_URL", "https://urlscan.io")
USER_AGENT = f"urlscan-py/{version}"


def _compact(d: dict) -> dict:
    """Remove empty values from a dictionary."""
    return {k: v for k, v in d.items() if v is not None}


class RetryTransport(httpx.HTTPTransport):
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        res = super().handle_request(request)
        if res.status_code == 429:
            rate_limit_reset_after: str | None = res.headers.get(
                "X-Rate-Limit-Reset-After"
            )
            if rate_limit_reset_after is None:
                return res

            logger.info(
                f"Rate limit error hit. Wait {rate_limit_reset_after} seconds before retrying..."
            )
            time.sleep(float(rate_limit_reset_after))
            return self.handle_request(request)

        return res


class ClientResponse:
    def __init__(self, res: httpx.Response):
        self._res = res

    @property
    def basename(self) -> str:
        return os.path.basename(self._res.url.path)

    @property
    def content(self) -> bytes:
        return self._res.content

    def json(self) -> Any:
        return self._res.json()

    @property
    def text(self) -> str:
        return self._res.text

    @property
    def headers(self):
        return self._res.headers

    @property
    def status_code(self) -> int:
        return self._res.status_code

    def raise_for_status(self) -> None:
        self._res.raise_for_status()


@dataclass
class RateLimit:
    remaining: int
    reset: datetime.datetime


class RateLimitMemo(TypedDict):
    public: RateLimit | None
    private: RateLimit | None
    unlisted: RateLimit | None
    retrieve: RateLimit | None
    search: RateLimit | None


class Client:
    def __init__(
        self,
        api_key: str,
        base_url: str = BASE_URL,
        user_agent: str = USER_AGENT,
        trust_env: bool = False,
        timeout: TimeoutTypes = 60,
        proxy: str | None = None,
        verify: bool = True,
        retry: bool = False,
    ):
        """
        Args:
            api_key (str): Your urlscan.io API key.
            base_url (str, optional): Base URL. Defaults to BASE_URL.
            user_agent (str, optional): User agent. Defaults to USER_AGENT.
            trust_env (bool, optional): Enable or disable usage of environment variables for configuration. Defaults to False.
            timeout (TimeoutTypes, optional): timeout configuration to use when sending request. Defaults to 60.
            proxy (str | None, optional): Proxy URL where all the traffic should be routed. Defaults to None.
            verify (bool, optional): Either `True` to use an SSL context with the default CA bundle, `False` to disable verification. Defaults to True.
            retry (bool, optional): Whether to use automatic X-Rate-Limit-Reset-After HTTP header based retry. Defaults to False.
        """
        self._api_key = api_key
        self._base_url = base_url
        self._user_agent = user_agent
        self._trust_env = trust_env
        self._timeout = timeout
        self._proxy = proxy
        self._verify = verify
        self._retry = retry

        self._session: httpx.Client | None = None
        self._rate_limit_memo: RateLimitMemo = {
            "public": None,
            "private": None,
            "unlisted": None,
            "retrieve": None,
            "search": None,
        }

        self._scan_uuid_timestamp_memo: dict[str, float] = {}

    def __enter__(self):
        return self

    def __exit__(self, item_type: Any, value: Any, traceback: Any):
        self.close()

    def close(self):
        if self._session:
            self._session.close()
            self._session = None

    def _get_session(self) -> httpx.Client:
        if self._session:
            return self._session

        headers = _compact(
            {
                "User-Agent": self._user_agent,
                "API-Key": self._api_key,
            }
        )
        transport: httpx.HTTPTransport | None = None
        if self._retry:
            transport = RetryTransport()

        self._session = httpx.Client(
            base_url=self._base_url,
            headers=headers,
            timeout=self._timeout,
            proxy=self._proxy,
            verify=self._verify,
            trust_env=self._trust_env,
            transport=transport,
        )
        return self._session

    def _get_action(self, request: httpx.Request) -> ActionType | None:
        path = request.url.path
        if request.method == "GET":
            if path == "/api/v1/search/":
                return "search"

            if path.startswith("/api/v1/result/"):
                return "retrieve"

            return None

        if request.method == "POST":
            if path != "/api/v1/scan/":
                return None

            if request.headers.get("Content-Type") != "application/json":
                return None

            with contextlib.suppress(json.JSONDecodeError):
                data: dict = json.loads(request.content)
                return data.get("visibility")

        return None

    def _send_request(
        self, session: httpx.Client, request: httpx.Request
    ) -> ClientResponse:
        # let it automatic retry if retry is enabled
        if self._retry:
            return ClientResponse(session.send(request))

        action = self._get_action(request)
        if action:
            rate_limit: RateLimit | None = self._rate_limit_memo.get(action)
            if rate_limit:
                utcnow = datetime.datetime.now(datetime.timezone.utc)
                if rate_limit.remaining == 0 and rate_limit.reset > utcnow:
                    raise RateLimitRemainingError(
                        f"{action} is rate limited. Wait until {utcnow}."
                    )

        res = ClientResponse(session.send(request))

        # use action in response headers
        action = res.headers.get("X-Rate-Limit-Action")
        if action:
            remaining = res.headers.get("X-Rate-Limit-Remaining")
            reset = res.headers.get("X-Rate-Limit-Reset")
            if remaining and reset:
                self._rate_limit_memo[action] = RateLimit(
                    remaining=int(remaining),
                    reset=parse_datetime(reset),
                )

        return res

    def get(self, path: str, params: QueryParamTypes | None = None) -> ClientResponse:
        """Send a GET request to a given API endpoint.

        Args:
            path (str): Path to API endpoint.
            params (QueryParamTypes | None, optional): Query parameters. Defaults to None.

        Returns:
            ClientResponse: Response.
        """
        session = self._get_session()
        req = session.build_request("GET", path, params=params)
        return self._send_request(session, req)

    def get_json(self, path: str, params: QueryParamTypes | None = None) -> dict:
        res = self.get(path, params=params)
        return self._response_to_json(res)

    def post(
        self,
        path: str,
        json: Any | None = None,
        data: RequestData | None = None,
    ) -> ClientResponse:
        """Send a POST request to a given API endpoint.

        Args:
            path (str): Path.
            json (Any | None, optional): Dict to send in request body as JSON. Defaults to None.
            data (RequestData | None, optional): Dict to send in request body. Defaults to None.

        Returns:
            ClientResponse: Response.
        """
        session = self._get_session()
        req = session.build_request("POST", path, json=json, data=data)
        return self._send_request(session, req)

    def download(
        self,
        path: str,
        file: BinaryIO,
        params: QueryParamTypes | None = None,
    ) -> None:
        """Download a file from a given API endpoint.

        Args:
            path (str): Path to API endpoint.
            file (BinaryIO): File object to write to.
            params (QueryParamTypes | None, optional): Query parameters. Defaults to None.

        Returns:
            BytesIO: File content.
        """
        res = self.get(path, params=params)
        file.write(res.content)
        return

    def get_content(self, path: str, params: QueryParamTypes | None = None) -> bytes:
        res = self.get(path, params=params)
        return self._response_to_content(res)

    def get_text(self, path: str, params: QueryParamTypes | None = None) -> str:
        res = self.get(path, params=params)
        return self._response_to_str(res)

    def get_result(self, uuid: str) -> dict:
        """Get a result of a scan by UUID.

        Args:
            uuid (str): UUID.

        Returns:
            Dict: Scan result.

        Reference:
            https://urlscan.io/docs/api/#result
        """
        return self.get_json(f"/api/v1/result/{uuid}/")

    def get_screenshot(self, uuid: str) -> BytesIO:
        """Get a screenshot of a scan by UUID.

        Args:
            uuid (str): UUID.

        Returns:
            : Screenshot (img/png) as bytes.

        Reference:
            https://urlscan.io/docs/api/#screenshot
        """
        res = self.get(f"/screenshots/{uuid}.png")
        bio = BytesIO(res.content)
        bio.name = res.basename
        return bio

    def get_dom(self, uuid: str) -> str:
        """Get a DOM of a scan by UUID.

        Args:
            uuid (str): UUID

        Returns:
            str: DOM as a string.

        Reference:
            https://urlscan.io/docs/api/#dom
        """
        return self.get_text(f"/dom/{uuid}/")

    def search(
        self,
        q: str = "",
        size: int = 100,
        limit: int | None = None,
        search_after: str | None = None,
    ) -> SearchIterator:
        """Search.

        Args:
            q (str): Query term. Defaults to "".
            size (int, optional): Number of results returned in a search. Defaults to 100.
            limit (int | None, optional): . Defaults to None.
            search_after (str | None, optional): Maximum number of results that will be returned by the iterator. Defaults to None.

        Returns:
            SearchIterator: Search iterator.

        Reference:
            https://urlscan.io/docs/api/#search
        """
        return SearchIterator(
            self,
            q=q,
            size=size,
            limit=limit,
            search_after=search_after,
        )

    def scan(
        self,
        url: str,
        *,
        visibility: VisibilityType,
        tags: list[str] | None = None,
        customagent: str | None = None,
        referer: str | None = None,
        override_safety: Any = None,
        country: str | None = None,
    ) -> dict:
        """Scan a given URL.

        Args:
            url (str): URL to scan.
            visibility (VisibilityType): Visibility of the scan. Can be "public", "private", or "unlisted".
            tags (list[str] | None, optional): Tags to be attached. Defaults to None.
            customagent (str | None, optional): Custom user agent. Defaults to None.
            referer (str | None, optional): Referer. Defaults to None.
            override_safety (Any, optional): If set to any value, this will disable reclassification of URLs with potential PII in them. Defaults to None.
            country (str | None, optional): Specify which country the scan should be performed from (2-Letter ISO-3166-1 alpha-2 country. Defaults to None.

        Returns:
            dict: Scan response.

        Reference:
            https://urlscan.io/docs/api/#scan
        """
        data = _compact(
            {
                "url": url,
                "tags": tags,
                "visibility": visibility,
                "customagent": customagent,
                "referer": referer,
                "overrideSafety": override_safety,
                "country": country,
            }
        )
        res = self.post("/api/v1/scan/", json=data)
        json_res = self._response_to_json(res)

        json_visibility = json_res.get("visibility")
        if json_visibility is not None and json_visibility != visibility:
            logger.warning(f"Visibility is enforced to {json_visibility}.")

        # memoize the scan UUID & timestamp
        uuid = json_res.get("uuid")
        if isinstance(uuid, str):
            self._scan_uuid_timestamp_memo[uuid] = time.time()

        return json_res

    def bulk_scan(
        self,
        urls: list[str],
        *,
        visibility: VisibilityType,
        tags: list[str] | None = None,
        customagent: str | None = None,
        referer: str | None = None,
        override_safety: Any = None,
        country: str | None = None,
    ) -> list[tuple[str, dict | Exception]]:
        """Scan multiple URLs in bulk.

        Args:
            urls (list[str]): List of URLs to scan.
            visibility (VisibilityType): Visibility of the scan. Can be "public", "private", or "unlisted".
            tags (list[str] | None, optional): Tags to be attached. Defaults to None.
            customagent (str | None, optional): Custom user agent. Defaults to None.
            referer (str | None, optional): Referer. Defaults to None.
            override_safety (Any, optional): If set to any value, this will disable reclassification of URLs with potential PII in them. Defaults to None.
            country (str | None, optional): Specify which country the scan should be performed from (2-Letter ISO-3166-1 alpha-2 country. Defaults to None.

        Returns:
            list[tuple[str, dict | Exception]]: A list of tuples of (url, scan response or error).

        Reference:
            https://urlscan.io/docs/api/#scan
        """

        def inner(url: str) -> dict | Exception:
            try:
                return self.scan(
                    url,
                    visibility=visibility,
                    tags=tags,
                    customagent=customagent,
                    referer=referer,
                    override_safety=override_safety,
                    country=country,
                )
            except Exception as e:
                return e

        return [(url, inner(url)) for url in urls]

    def wait_for_result(
        self,
        uuid: str,
        timeout: float = 60.0,
        interval: float = 1.0,
        initial_wait: float | None = 10.0,
    ) -> None:
        """Wait for a scan result to be available.

        Args:
            uuid (str): UUID of a result.
            timeout (float, optional): Timeout in seconds. Defaults to 60.0.
            interval (float, optional): Interval in seconds. Defaults to 1.0.
            initial_wait (float | None, optional): Initial wait time in seconds. Set None to disable. Defaults to 10.0.
        """
        session = self._get_session()
        req = session.build_request("HEAD", f"/api/v1/result/{uuid}/")

        scanned_at = self._scan_uuid_timestamp_memo.get(uuid)
        if scanned_at and initial_wait:
            elapsed = time.time() - scanned_at
            if elapsed < initial_wait:
                time.sleep(initial_wait - elapsed)

        start_time = time.time()
        while True:
            res = self._send_request(session, req)
            if res.status_code == 200:
                self._scan_uuid_timestamp_memo.pop(uuid, None)
                return

            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout waiting for scan result.")

            time.sleep(interval)

    def scan_and_get_result(
        self,
        url: str,
        visibility: VisibilityType,
        tags: list[str] | None = None,
        customagent: str | None = None,
        referer: str | None = None,
        override_safety: Any = None,
        country: str | None = None,
        timeout: float = 60.0,
        interval: float = 1.0,
        initial_wait: float | None = 10.0,
    ):
        """Scan a given URL, wait for a result and get it.

        Args:
            url (str): URL to scan.
            visibility (VisibilityType): Visibility of the scan. Can be "public", "private", or "unlisted".
            tags (list[str] | None, optional): Tags to be attached. Defaults to None.
            customagent (str | None, optional): Custom user agent. Defaults to None.
            referer (str | None, optional): Referer. Defaults to None.
            override_safety (Any, optional): If set to any value, this will disable reclassification of URLs with potential PII in them. Defaults to None.
            country (str | None, optional): Specify which country the scan should be performed from (2-Letter ISO-3166-1 alpha-2 country. Defaults to None.
            timeout (float, optional): Timeout for waiting a result in seconds. Defaults to 60.0.
            interval (float, optional): Interval in seconds. Defaults to 1.0.
            initial_wait (float | None, optional): Initial wait time in seconds. Set None to disable. Defaults to 10.0.

        Returns:
            dict: Scan result.

        Reference:
            https://urlscan.io/docs/api/#scan
        """
        res = self.scan(
            url,
            visibility=visibility,
            tags=tags,
            customagent=customagent,
            referer=referer,
            override_safety=override_safety,
            country=country,
        )
        uuid: str = res["uuid"]
        self.wait_for_result(
            uuid, timeout=timeout, interval=interval, initial_wait=initial_wait
        )
        return self.get_result(uuid)

    def bulk_scan_and_get_results(
        self,
        urls: list[str],
        visibility: VisibilityType,
        tags: list[str] | None = None,
        customagent: str | None = None,
        referer: str | None = None,
        override_safety: Any = None,
        country: str | None = None,
        timeout: float = 60.0,
        interval: float = 1.0,
        initial_wait: float | None = 10.0,
    ) -> list[tuple[str, dict | Exception]]:
        """Scan URLs, wait for results and get them.

        Args:
            urls (list[str]): URLs to scan.
            visibility (VisibilityType): Visibility of the scan. Can be "public", "private", or "unlisted".
            tags (list[str] | None, optional): Tags to be attached. Defaults to None.
            customagent (str | None, optional): Custom user agent. Defaults to None.
            referer (str | None, optional): Referer. Defaults to None.
            override_safety (Any, optional): If set to any value, this will disable reclassification of URLs with potential PII in them. Defaults to None.
            country (str | None, optional): Specify which country the scan should be performed from (2-Letter ISO-3166-1 alpha-2 country. Defaults to None.
            timeout (float, optional): Timeout for waiting a result in seconds. Defaults to 60.0.
            interval (float, optional): Interval in seconds. Defaults to 1.0.
            initial_wait (float | None, optional): Initial wait time in seconds. Set None to disable. Defaults to 10.0.

        Returns:
            list[tuple[str, dict | Exception]]: A list of tuples of (url, result or error).

        Reference:
            https://urlscan.io/docs/api/#scan
        """

        responses = self.bulk_scan(
            urls,
            visibility=visibility,
            tags=tags,
            customagent=customagent,
            referer=referer,
            override_safety=override_safety,
            country=country,
        )

        def mapping(res_or_error: dict | Exception) -> dict | Exception:
            if isinstance(res_or_error, Exception):
                return res_or_error

            uuid: str = res_or_error["uuid"]
            self.wait_for_result(
                uuid, timeout=timeout, interval=interval, initial_wait=initial_wait
            )
            return self.get_result(uuid)

        return [(url, mapping(res_or_error)) for url, res_or_error in responses]

    def _get_error(self, res: ClientResponse) -> APIError | None:
        try:
            res.raise_for_status()
        except httpx.HTTPStatusError as exc:
            data: dict = exc.response.json()
            message: str = data["message"]
            description: str | None = data.get("description")
            status: int = data["status"]

            # ref. https://urlscan.io/docs/api/#ratelimit
            if status == 429:
                rate_limit_reset_after = float(
                    exc.response.headers.get("X-Rate-Limit-Reset-After", 0)
                )
                return RateLimitError(
                    message,
                    description=description,
                    status=status,
                    rate_limit_reset_after=rate_limit_reset_after,
                )

            return APIError(message, description=description, status=status)

        return None

    def _response_to_json(self, res: ClientResponse) -> dict:
        error = self._get_error(res)
        if error:
            raise error

        return res.json()

    def _response_to_str(self, res: ClientResponse) -> str:
        error = self._get_error(res)
        if error:
            raise error

        return res.text

    def _response_to_content(self, res: ClientResponse) -> bytes:
        error = self._get_error(res)
        if error:
            raise error

        return res.content
