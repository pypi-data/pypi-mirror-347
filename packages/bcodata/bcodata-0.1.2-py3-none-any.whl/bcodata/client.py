import asyncio
import json
import time
import uuid
from types import TracebackType
from typing import Any, Self

import aiolimiter
import httpx
import tenacity
from loguru import logger

from bcodata.exceptions import (
    ODataConnectionError,
    ODataHTTPError,
    ODataJSONDecodeError,
    ODataRequestError,
    ODataTimeoutError,
)


class Client:
    """A client for Business Central OData API."""

    # HTTP status codes that are considered retryable
    RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}  # noqa: RUF012

    # Default configuration values
    DEFAULT_MAX_RATE = 10
    DEFAULT_TIME_PERIOD = 1
    DEFAULT_MAX_CONCURRENCY = 5
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RETRY_DELAY = 1
    DEFAULT_TIMEOUT = 90

    def __init__(
        self,
        base_url: str,
        credentials: tuple[str, str] | None = None,
        max_rate: int = DEFAULT_MAX_RATE,
        time_period: int = DEFAULT_TIME_PERIOD,
        max_concurrency: int = DEFAULT_MAX_CONCURRENCY,
        max_retries: int = DEFAULT_MAX_RETRIES,
        base_retry_delay: int = DEFAULT_RETRY_DELAY,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Initialize the client with the given base URL and credentials.

        Parameters
        ----------
        base_url : str
            The base URL of the Business Central OData API.
        credentials : tuple[str, str] | None
            The credentials for the client.
        max_rate : int
            The maximum number of requests per time period.
        time_period : int
            The time period in seconds.
        max_concurrency : int
            The maximum number of concurrent requests.
        max_retries : int
            The number of times to retry a request.
        base_retry_delay : int
            The base delay in seconds between retries.
        timeout : int
            The timeout for the request.

        Returns
        -------
        None

        """
        self.base_url = base_url.rstrip("/")
        self._username = credentials[0] if credentials else None
        self._password = credentials[1] if credentials else None
        self._session = None
        self.limiter = aiolimiter.AsyncLimiter(max_rate=max_rate, time_period=time_period)
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.max_retries = max_retries
        self.base_retry_delay = base_retry_delay
        self.timeout = timeout

        if max_rate <= 0:
            raise ValueError("max_rate must be greater than 0")
        if time_period <= 0:
            raise ValueError("time_period must be greater than 0")
        if max_concurrency <= 0:
            raise ValueError("max_concurrency must be greater than 0")
        if self.max_retries < 0:
            raise ValueError("max_retries must be greater than or equal to 0")
        if self.base_retry_delay <= 0:
            raise ValueError("base_retry_delay must be greater than 0")
        if self.timeout <= 0:
            raise ValueError("timeout must be greater than 0")

        logger.info(
            f"Initialized OData client with base_url={base_url}, max_rate={max_rate}/{time_period}s, "
            f"concurrency={max_concurrency}, retries={max_retries}, retry_delay={base_retry_delay}s, "
            f"timeout={timeout}s",
        )

    async def __aenter__(self) -> Self:
        """Enter the context manager."""
        logger.debug("Creating HTTP client session")
        self._session = httpx.AsyncClient(auth=(self._username, self._password), timeout=self.timeout)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the context manager."""
        if self._session:
            logger.debug("Closing HTTP client session")
            await self._session.aclose()
        self._session = None

    @staticmethod
    def _is_retryable_exception(exception: BaseException) -> bool:
        """
        Determine if an exception is retryable.

        Parameters
        ----------
        exception : BaseException
            The exception to check.

        Returns
        -------
        bool
            True if the exception is retryable, False otherwise.

        """
        if isinstance(exception, httpx.ConnectError | httpx.ReadTimeout | httpx.PoolTimeout):
            logger.debug(f"Connection/timeout error identified as retryable: {exception!r}")
            return True
        if isinstance(exception, httpx.HTTPStatusError):
            status_code = exception.response.status_code
            is_retryable = status_code in Client.RETRYABLE_STATUS_CODES
            logger.debug(
                f"HTTP error {status_code} identified as "
                f"{'retryable' if is_retryable else 'non-retryable'}: {exception!r}",
            )
            return is_retryable
        logger.debug(f"Non-retryable exception: {exception!r}")
        return False

    async def _request(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        request_id: str | None = None,
    ) -> httpx.Response:
        """
        Make a request to the API.

        Parameters
        ----------
        url : str
            The URL to request.
        params : dict[str, Any] | None
            The parameters to pass to the endpoint.
        request_id : str | None
            A unique identifier for this request for logging purposes.

        Returns
        -------
        httpx.Response
            The response from the endpoint.

        """
        request_id = request_id or str(uuid.uuid4())

        @tenacity.retry(
            stop=tenacity.stop_after_attempt(self.max_retries + 1),
            wait=tenacity.wait_exponential(multiplier=self.base_retry_delay, max=self.timeout / 2),
            retry=tenacity.retry_if_exception(self._is_retryable_exception),
            reraise=True,
        )
        async def _attempt_request() -> httpx.Response:
            async with self.semaphore, self.limiter:
                logger.debug(f"[Request-{request_id}] Making request to {url} with params {params}")
                response = await self._session.get(url, params=params, headers={"X-Request-ID": request_id})
                response.raise_for_status()
                logger.debug(f"[Request-{request_id}] Received response from {url} with status {response.status_code}")
                return response

        if not self._session:
            logger.error("Client not initialized. Use 'async with Client(...):' context manager.")
            raise RuntimeError("Client not initialized. Use 'async with Client(...):' context manager.")

        logger.info(f"[Request-{request_id}] Requesting data from {url}")

        try:
            return await _attempt_request()
        except httpx.ConnectError as e:
            logger.error(f"[Request-{request_id}] Connection error for {url}: {e!s}")
            raise ODataConnectionError(url, params=params, original_exception=e) from e
        except httpx.ReadTimeout as e:
            logger.error(f"[Request-{request_id}] Timeout error for {url}: {self.timeout} seconds")
            raise ODataTimeoutError(url, params=params, timeout_duration=self.timeout) from e
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            error_text = e.response.text
            raise ODataHTTPError(
                url,
                status_code=status_code,
                params=params,
                response_content=error_text,
            ) from e
        except json.JSONDecodeError as e:
            logger.error(f"[Request-{request_id}] JSON decode error for {url}: {e!s}")
            raise ODataJSONDecodeError(url, params=params, original_exception=e) from e
        except httpx.RequestError as e:
            logger.error(f"[Request-{request_id}] Request error for {url}: {e!s}")
            raise ODataRequestError(
                f"An unexpected error occurred for request to {url} with params: {params}. Exception: {e}",
            ) from e
        except Exception as e:
            logger.error(f"[Request-{request_id}] Unexpected error for {url}: {e!s}")
            raise ODataRequestError(
                f"An unexpected error occurred for request to {url} with params: {params}. Exception: {e}",
            ) from e

    async def get_data(self, endpoint: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """
        Get data from the API.

        Parameters
        ----------
        endpoint : str
            The endpoint to request.
        params : dict[str, Any] | None
            The parameters to pass to the endpoint. Can be built using QueryBuilder.

        Returns
        -------
        list[dict[str, Any]]
            The response from the endpoint.

        """
        start_time = time.time()
        request_id = str(uuid.uuid4())  # Generate a unique UUID for this request

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        content = []
        page_count = 0

        logger.info(f"[Request-{request_id}] Starting data fetch from endpoint {endpoint}")

        while url:
            page_count += 1
            page_start_time = time.time()
            logger.debug(f"[Request-{request_id}] Fetching page {page_count} from {url}")

            response = await self._request(url, params, request_id)
            try:
                response_json = response.json()
                logger.debug(f"[Request-{request_id}] Successfully parsed JSON response")
            except json.JSONDecodeError as e:
                logger.error(f"[Request-{request_id}] Failed to decode JSON response from {url}: {e!s}")
                raise ODataJSONDecodeError(url, params=params, original_exception=e) from e

            items = response_json.get("value", [])
            content.extend(items)

            page_duration = time.time() - page_start_time
            logger.debug(
                f"[Request-{request_id}] Added {len(items)} items from page {page_count}, "
                f"total items: {len(content)}, page fetch time: {page_duration:.3f}s",
            )

            url = response_json.get("@odata.nextLink", None)
            if url:
                logger.debug(f"[Request-{request_id}] Next page link found: {url}")
            else:
                logger.debug(f"[Request-{request_id}] No more pages to fetch")
            params = None

        total_duration = time.time() - start_time
        logger.info(
            f"[Request-{request_id}] Retrieved {len(content)} total items from endpoint {endpoint} "
            f"in {total_duration:.3f}s ({page_count} pages, avg {total_duration / (page_count or 1):.3f}s per page)",
        )
        return content
