"""
Example of error handling with BCOData.
"""

import asyncio
from bcodata import Client
from bcodata.exceptions import (
    ODataConnectionError,
    ODataHTTPError,
    ODataJSONDecodeError,
    ODataTimeoutError,
    ODataRequestError,
)


async def fetch_with_retry(client: Client, endpoint: str, max_attempts: int = 3) -> list:
    """
    Fetch data from an endpoint with retry logic.

    Args:
        client: BCOData client instance
        endpoint: API endpoint to fetch
        max_attempts: Maximum number of retry attempts

    Returns:
        list: Fetched data

    Raises:
        ODataRequestError: If all retry attempts fail
    """
    for attempt in range(max_attempts):
        try:
            return await client.get_data(endpoint)
        except (ODataConnectionError, ODataTimeoutError) as e:
            if attempt == max_attempts - 1:
                raise ODataRequestError(f"Failed after {max_attempts} attempts: {str(e)}") from e
            print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
            await asyncio.sleep(2**attempt)  # Exponential backoff


async def main():
    try:
        async with Client(
            base_url="https://api.businesscentral.dynamics.com/v2.0/tenant_id/api/v2.0",
            credentials=("username", "password"),
            timeout=30,  # Shorter timeout for demonstration
        ) as client:
            # Example 1: Handle specific error types
            try:
                data = await client.get_data("companies")
                print(f"Successfully retrieved {len(data)} companies")
            except ODataConnectionError as e:
                print(f"Connection error occurred: {e}")
            except ODataTimeoutError as e:
                print(f"Request timed out: {e}")
            except ODataHTTPError as e:
                print(f"HTTP error occurred: {e}")
                if e.status_code == 401:
                    print("Authentication failed. Please check your credentials.")
                elif e.status_code == 403:
                    print("Access forbidden. Please check your permissions.")
            except ODataJSONDecodeError as e:
                print(f"Failed to parse response: {e}")

            # Example 2: Using retry logic
            try:
                data = await fetch_with_retry(client, "customers")
                print(f"Successfully retrieved {len(data)} customers after retries")
            except ODataRequestError as e:
                print(f"All retry attempts failed: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
