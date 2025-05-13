"""
Basic example of using BCOData to fetch data from Business Central OData API.
"""

import asyncio
from bcodata import Client


async def main():
    # Initialize the client with your Business Central OData API URL and credentials
    async with Client(
        base_url="https://api.businesscentral.dynamics.com/v2.0/tenant_id/api/v2.0",
        credentials=("username", "password"),
    ) as client:
        # Fetch data from an endpoint
        data = await client.get_data("companies")
        print(f"Retrieved {len(data)} companies")

        # Print some details about each company
        for company in data:
            print(f"\nCompany: {company.get('name', 'N/A')}")
            print(f"ID: {company.get('id', 'N/A')}")
            print(f"System Version: {company.get('systemVersion', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(main())
