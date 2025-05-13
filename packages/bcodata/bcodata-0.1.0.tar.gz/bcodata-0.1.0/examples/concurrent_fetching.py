"""
Example of concurrent data fetching from multiple Business Central OData endpoints.
"""

import asyncio
from typing import Dict, List
from bcodata import Client


async def fetch_multiple_endpoints(client: Client) -> Dict[str, List[dict]]:
    """
    Fetch data from multiple endpoints concurrently.

    Returns:
        Dict[str, List[dict]]: Dictionary mapping endpoint names to their data
    """
    # Define the endpoints to fetch
    endpoints = ["companies", "customers", "items", "salesOrders"]

    # Create tasks for each endpoint
    tasks = [client.get_data(endpoint) for endpoint in endpoints]

    # Execute all tasks concurrently
    results = await asyncio.gather(*tasks)

    # Create a dictionary mapping endpoints to their results
    return dict(zip(endpoints, results))


async def main():
    async with Client(
        base_url="https://api.businesscentral.dynamics.com/v2.0/tenant_id/api/v2.0",
        credentials=("username", "password"),
        max_rate=20,  # Increased rate limit for concurrent requests
        max_concurrency=10,  # Increased concurrency limit
    ) as client:
        # Fetch data from all endpoints concurrently
        results = await fetch_multiple_endpoints(client)

        # Process and display results
        for endpoint, data in results.items():
            print(f"\n=== {endpoint.upper()} ===")
            print(f"Total records: {len(data)}")

            # Display first record as sample
            if data:
                print("\nSample record:")
                for key, value in data[0].items():
                    print(f"{key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
