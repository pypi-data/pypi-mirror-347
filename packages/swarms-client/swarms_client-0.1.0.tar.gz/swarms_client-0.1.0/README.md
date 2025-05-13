# Swarms SDK

A production-grade Python client for the Swarms API, providing a simple and intuitive interface for creating and managing AI swarms.

## Features

- 🚀 Async-first design with comprehensive error handling
- 📝 Extensive logging with loguru
- 🔄 Automatic retries with exponential backoff
- 🔒 Secure API key management
- 📊 Detailed telemetry and monitoring
- 🎯 Type hints and validation
- 📚 Comprehensive documentation

## Installation

```bash
pip install swarms-sdk
```

## Quick Start

```python
import asyncio
from swarms_sdk import SwarmsClient

async def main():
    # Initialize the client
    client = SwarmsClient(api_key="your-api-key")

    # Create a swarm
    swarm = await client.create_swarm(
        name="my-swarm",
        task="Analyze this data",
        agents=[
            {
                "agent_name": "analyzer",
                "model_name": "gpt-4",
                "role": "worker"
            }
        ]
    )

    # Run the swarm
    result = await client.run_swarm(swarm["id"])
    print(result)

# Run the async function
asyncio.run(main())
```

## API Reference

### SwarmsClient

The main client class for interacting with the Swarms API.

#### Initialization

```python
client = SwarmsClient(
    api_key="your-api-key",  # Optional: Can also use SWARMS_API_KEY env var
    base_url="https://api.swarms.world",  # Optional: Default API URL
    timeout=60,  # Optional: Request timeout in seconds
    max_retries=3  # Optional: Maximum retry attempts
)
```

#### Methods

##### create_swarm

Create a new swarm with specified configuration.

```python
swarm = await client.create_swarm(
    name="my-swarm",
    task="Analyze this data",
    agents=[
        {
            "agent_name": "analyzer",
            "model_name": "gpt-4",
            "role": "worker"
        }
    ],
    description="Optional description",
    max_loops=1,
    swarm_type="SequentialWorkflow",
    service_tier="standard"
)
```

##### run_swarm

Run a swarm with the specified ID.

```python
result = await client.run_swarm(swarm_id="swarm-123")
```

##### get_swarm_logs

Get execution logs for a specific swarm.

```python
logs = await client.get_swarm_logs(swarm_id="swarm-123")
```

##### get_available_models

Get list of available models.

```python
models = await client.get_available_models()
```

##### get_swarm_types

Get list of available swarm types.

```python
swarm_types = await client.get_swarm_types()
```

### Error Handling

The SDK provides custom exceptions for different error scenarios:

```python
from swarms_sdk import (
    SwarmsError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIError
)

try:
    result = await client.run_swarm(swarm_id)
except AuthenticationError as e:
    print("Authentication failed:", e)
except RateLimitError as e:
    print("Rate limit exceeded:", e)
except APIError as e:
    print(f"API error (status {e.status_code}):", e)
except SwarmsError as e:
    print("Other error:", e)
```

### Logging

The SDK uses loguru for comprehensive logging. Logs are written to both console and file:

```python
import loguru

# Configure custom logging
loguru.logger.add(
    "custom.log",
    rotation="100 MB",
    retention="7 days",
    level="DEBUG"
)
```

## Best Practices

1. **API Key Management**
   - Use environment variables for API keys
   - Never commit API keys to version control
   - Rotate API keys regularly

2. **Error Handling**
   - Always wrap API calls in try-except blocks
   - Handle specific exceptions appropriately
   - Implement retry logic for transient failures

3. **Resource Management**
   - Use async context manager for proper session cleanup
   - Close client sessions when done
   - Monitor memory usage with large swarms

4. **Performance**
   - Use appropriate service tiers
   - Implement caching where appropriate
   - Monitor API rate limits

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 