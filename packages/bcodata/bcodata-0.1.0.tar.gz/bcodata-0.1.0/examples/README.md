# BCOData Examples

This directory contains example scripts demonstrating various features and use cases of the BCOData library.

## Examples

### 1. Basic Usage (`basic_usage.py`)

A simple example showing how to:

- Initialize the BCOData client
- Fetch data from a single endpoint
- Process and display the results

### 2. Concurrent Fetching (`concurrent_fetching.py`)

Demonstrates how to:

- Fetch data from multiple endpoints concurrently
- Configure the client for concurrent operations
- Process and display results from multiple endpoints
- Handle large datasets efficiently

### 3. Error Handling (`error_handling.py`)

Shows how to:

- Handle different types of errors (connection, timeout, HTTP, etc.)
- Implement custom retry logic
- Use exponential backoff for retries
- Provide meaningful error messages to users

## Running the Examples

1. Make sure you have BCOData installed:

```bash
pip install bcodata
```

2. Update the credentials in each example file with your Business Central API credentials:

```python
base_url="https://api.businesscentral.dynamics.com/v2.0/tenant_id/api/v2.0",
credentials=("username", "password")
```

3. Run any example using Python:

```bash
python examples/basic_usage.py
python examples/concurrent_fetching.py
python examples/error_handling.py
```

## Notes

- These examples are meant to be educational and demonstrate best practices
- Always handle your credentials securely in production environments
- Adjust rate limits and timeouts based on your Business Central API tier
- Consider implementing proper logging in production code
