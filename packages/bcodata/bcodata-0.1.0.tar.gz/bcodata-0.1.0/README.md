# BCOData

A Python library for interacting with Business Central OData API with built-in rate limiting, retry mechanisms, and concurrent request handling.

## Features

- Asynchronous API client for Business Central OData endpoints
- Automatic rate limiting to prevent API throttling
- Built-in retry mechanism for failed requests
- Concurrent request handling with configurable limits
- Comprehensive error handling with detailed error messages
- Automatic pagination handling for large datasets

## Installation

```bash
pip install bcodata
```

## Usage

### Basic Usage

```python
import asyncio
from bcodata import Client

async def main():
    # Initialize the client with your Business Central OData API URL and credentials
    async with Client(
        base_url="https://api.businesscentral.dynamics.com/v2.0/tenant_id/api/v2.0",
        credentials=("username", "password")
    ) as client:
        # Fetch data from an endpoint
        data = await client.get_data("companies")
        print(f"Retrieved {len(data)} companies")

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Configuration

```python
import asyncio
from bcodata import Client

async def main():
    async with Client(
        base_url="https://api.businesscentral.dynamics.com/v2.0/tenant_id/api/v2.0",
        credentials=("username", "password"),
        max_rate=20,              # Maximum requests per time period
        time_period=1,            # Time period in seconds
        max_concurrency=10,       # Maximum concurrent requests
        max_retries=3,            # Number of retry attempts
        base_retry_delay=1,       # Base delay between retries in seconds
        timeout=90                # Request timeout in seconds
    ) as client:
        data = await client.get_data("companies")
        print(f"Retrieved {len(data)} companies")

if __name__ == "__main__":
    asyncio.run(main())
```

### Concurrent Data Fetching

Here's an example of how to fetch data from multiple endpoints concurrently:

```python
import asyncio
from bcodata import Client

async def fetch_multiple_endpoints(client: Client):
    # Define the endpoints to fetch
    endpoints = [
        "companies",
        "customers",
        "items",
        "salesOrders"
    ]

    # Create tasks for each endpoint
    tasks = [client.get_data(endpoint) for endpoint in endpoints]

    # Execute all tasks concurrently
    results = await asyncio.gather(*tasks)

    # Process results
    for endpoint, data in zip(endpoints, results):
        print(f"Retrieved {len(data)} records from {endpoint}")

async def main():
    async with Client(
        base_url="https://api.businesscentral.dynamics.com/v2.0/tenant_id/api/v2.0",
        credentials=("username", "password")
    ) as client:
        await fetch_multiple_endpoints(client)

if __name__ == "__main__":
    asyncio.run(main())
```

### Error Handling

The library provides specific exceptions for different types of errors:

```python
from bcodata import Client
from bcodata.exceptions import (
    ODataConnectionError,
    ODataHTTPError,
    ODataJSONDecodeError,
    ODataTimeoutError,
    ODataRequestError
)

async def main():
    try:
        async with Client(
            base_url="https://api.businesscentral.dynamics.com/v2.0/tenant_id/api/v2.0",
            credentials=("username", "password")
        ) as client:
            data = await client.get_data("companies")
    except ODataConnectionError as e:
        print(f"Connection error: {e}")
    except ODataTimeoutError as e:
        print(f"Timeout error: {e}")
    except ODataHTTPError as e:
        print(f"HTTP error: {e}")
    except ODataJSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except ODataRequestError as e:
        print(f"Request error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Examples

The repository includes a comprehensive set of examples in the `examples/` directory:

- `basic_usage.py`: Simple example of fetching data from a single endpoint
- `concurrent_fetching.py`: Demonstrates concurrent data fetching from multiple endpoints
- `error_handling.py`: Shows how to handle various error scenarios and implement retry logic

Each example is well-documented and includes comments explaining the code. To run the examples:

```bash
# Clone the repository
git clone https://github.com/yourusername/bcodata.git
cd bcodata

# Install the package
pip install -e .

# Run an example
python examples/basic_usage.py
```

For more details about each example, see the [examples README](examples/README.md).

## Configuration Options

The `Client` class accepts the following configuration parameters:

- `base_url` (str): The base URL of the Business Central OData API
- `credentials` (tuple[str, str] | None): Username and password for authentication
- `max_rate` (int): Maximum number of requests per time period (default: 10)
- `time_period` (int): Time period in seconds for rate limiting (default: 1)
- `max_concurrency` (int): Maximum number of concurrent requests (default: 5)
- `max_retries` (int): Number of retry attempts for failed requests (default: 3)
- `base_retry_delay` (int): Base delay between retries in seconds (default: 1)
- `timeout` (int): Request timeout in seconds (default: 90)

## Best Practices

1. Always use the client as a context manager (`async with`) to ensure proper resource cleanup
2. Configure appropriate rate limits based on your Business Central API tier
3. Use concurrent fetching for multiple endpoints to improve performance
4. Implement proper error handling for production use
5. Monitor the logs for any rate limiting or retry events

## License

This project is licensed under the MIT License - see the LICENSE file for details.
