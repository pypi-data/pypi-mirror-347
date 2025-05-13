"""
Swarms API Client

This module provides a production-grade client for interacting with the Swarms API.
It includes comprehensive error handling, logging, and type hints for better development experience.

Example:
    ```python
    from swarms_sdk import SwarmsClient

    # Initialize the client
    client = SwarmsClient(api_key="your-api-key")

    # Create a swarm
    swarm = client.create_swarm(
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
    result = client.run_swarm(swarm)
    ```
"""

import asyncio
import os
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import aiohttp
from loguru import logger
from pydantic import ValidationError

# Configure loguru logger
logger.remove()  # Remove default handler
logger.add(
    "swarms_client.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
logger.add(lambda msg: print(msg), level="INFO", format="{message}")


# Custom exceptions
class SwarmsError(Exception):
    """Base exception for all Swarms API errors."""

    pass


class AuthenticationError(SwarmsError):
    """Raised when authentication fails."""

    pass


class RateLimitError(SwarmsError):
    """Raised when rate limit is exceeded."""

    pass


class ValidationError(SwarmsError):
    """Raised when input validation fails."""

    pass


class APIError(SwarmsError):
    """Raised when the API returns an error."""

    def __init__(self, message: str, status_code: int, response: Dict[str, Any]):
        self.status_code = status_code
        self.response = response
        super().__init__(f"{message} (Status: {status_code})")


class SwarmsClient:
    """
    A production-grade client for interacting with the Swarms API.

    This client provides methods for creating and managing swarms, running agents,
    and handling API responses with proper error handling and logging.

    Attributes:
        api_key (str): The API key for authentication
        base_url (str): The base URL for the API
        timeout (int): Request timeout in seconds
        max_retries (int): Maximum number of retries for failed requests
        session (aiohttp.ClientSession): Async HTTP session for making requests
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.swarms.world",
        timeout: int = 60,
        max_retries: int = 3,
        max_concurrent_requests: int = 10,
    ):
        """
        Initialize the Swarms API client.

        Args:
            api_key (Optional[str]): API key for authentication. If not provided,
                will look for SWARMS_API_KEY environment variable.
            base_url (str): Base URL for the API. Defaults to production URL.
            timeout (int): Request timeout in seconds. Defaults to 60.
            max_retries (int): Maximum number of retries for failed requests. Defaults to 3.
            max_concurrent_requests (int): Maximum number of concurrent requests. Defaults to 10.

        Raises:
            AuthenticationError: If no API key is provided or found in environment.
        """
        self.api_key = api_key or os.getenv("SWARMS_API_KEY")
        if not self.api_key:
            raise AuthenticationError(
                "No API key provided. Set SWARMS_API_KEY environment variable or pass api_key parameter."
            )

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = None
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)

        logger.info(f"Initialized SwarmsClient with base URL: {self.base_url}")

    async def __aenter__(self):
        """Create aiohttp session when entering async context."""
        self.session = aiohttp.ClientSession(
            headers={"x-api-key": self.api_key},
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            connector=aiohttp.TCPConnector(
                limit=self.max_concurrent_requests,
                ttl_dns_cache=300,  # Cache DNS results for 5 minutes
                use_dns_cache=True,
            ),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close aiohttp session when exiting async context."""
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        retry_count: int = 0,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API with retry logic and error handling.

        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            data (Optional[Dict[str, Any]]): Request body data
            params (Optional[Dict[str, Any]]): Query parameters
            retry_count (int): Current retry attempt

        Returns:
            Dict[str, Any]: API response data

        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            APIError: For other API errors
            SwarmsError: For other errors
        """
        url = urljoin(self.base_url, endpoint)

        async with self.semaphore:  # Limit concurrent requests
            try:
                async with self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=self._get_headers(),
                ) as response:
                    response_data = await response.json()

                    if response.status == 200:
                        return response_data
                    elif response.status == 401:
                        raise AuthenticationError("Invalid API key")
                    elif response.status == 429:
                        if retry_count < self.max_retries:
                            retry_after = int(response.headers.get("Retry-After", 5))
                            logger.warning(
                                f"Rate limit exceeded. Retrying after {retry_after}s"
                            )
                            await asyncio.sleep(retry_after)
                            return await self._make_request(
                                method, endpoint, data, params, retry_count + 1
                            )
                        raise RateLimitError("Rate limit exceeded")
                    else:
                        raise APIError(
                            f"API request failed: {response_data.get('detail', 'Unknown error')}",
                            response.status,
                            response_data,
                        )

            except aiohttp.ClientError as e:
                logger.error(f"Network error: {str(e)}")
                if retry_count < self.max_retries:
                    logger.warning(f"Retrying request (attempt {retry_count + 1})")
                    await asyncio.sleep(2**retry_count)  # Exponential backoff
                    return await self._make_request(
                        method, endpoint, data, params, retry_count + 1
                    )
                raise SwarmsError(
                    f"Network error after {self.max_retries} retries: {str(e)}"
                )

    async def get_health(self) -> Dict[str, Any]:
        """
        Check API health status.

        Returns:
            Dict[str, Any]: Health status information
        """
        try:
            logger.info("Checking API health")
            response = await self._make_request("GET", "/health")
            logger.info("API health check successful")
            return response
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            raise

    async def create_swarm(
        self,
        name: str,
        task: str,
        agents: List[Dict[str, Any]],
        description: Optional[str] = None,
        max_loops: int = 1,
        swarm_type: Optional[str] = None,
        service_tier: str = "standard",
    ) -> Dict[str, Any]:
        """
        Create a new swarm with specified configuration.

        Args:
            name (str): Name of the swarm
            task (str): Task description for the swarm
            agents (List[Dict[str, Any]]): List of agent configurations
            description (Optional[str]): Optional description of the swarm
            max_loops (int): Maximum number of execution loops
            swarm_type (Optional[str]): Type of swarm architecture
            service_tier (str): Service tier to use ("standard" or "flex")

        Returns:
            Dict[str, Any]: Created swarm configuration
        """
        try:
            swarm_data = {
                "name": name,
                "task": task,
                "agents": agents,
                "description": description,
                "max_loops": max_loops,
                "swarm_type": swarm_type,
                "service_tier": service_tier,
            }

            logger.info(f"Creating swarm: {name}")
            response = await self._make_request(
                "POST", "/v1/swarm/completions", data=swarm_data
            )
            logger.info(f"Successfully created swarm: {name}")
            return response

        except Exception as e:
            logger.error(f"Error creating swarm: {str(e)}")
            raise

    async def run_swarm(self, swarm_id: str) -> Dict[str, Any]:
        """
        Run a swarm with the specified ID.

        Args:
            swarm_id (str): ID of the swarm to run

        Returns:
            Dict[str, Any]: Swarm execution results
        """
        try:
            logger.info(f"Running swarm: {swarm_id}")
            response = await self._make_request("POST", f"/v1/swarm/{swarm_id}/run")
            logger.info(f"Successfully ran swarm: {swarm_id}")
            return response

        except Exception as e:
            logger.error(f"Error running swarm {swarm_id}: {str(e)}")
            raise

    async def get_swarm_logs(self, swarm_id: str) -> List[Dict[str, Any]]:
        """
        Get execution logs for a specific swarm.

        Args:
            swarm_id (str): ID of the swarm

        Returns:
            List[Dict[str, Any]]: List of log entries
        """
        try:
            logger.info(f"Fetching logs for swarm: {swarm_id}")
            response = await self._make_request("GET", f"/v1/swarm/{swarm_id}/logs")
            logger.info(f"Successfully fetched logs for swarm: {swarm_id}")
            return response.get("logs", [])

        except Exception as e:
            logger.error(f"Error fetching logs for swarm {swarm_id}: {str(e)}")
            raise

    async def get_available_models(self) -> List[str]:
        """
        Get list of available models.

        Returns:
            List[str]: List of available model names
        """
        try:
            logger.info("Fetching available models")
            response = await self._make_request("GET", "/v1/models/available")
            logger.info("Successfully fetched available models")
            return response.get("models", [])

        except Exception as e:
            logger.error(f"Error fetching available models: {str(e)}")
            raise

    async def get_swarm_types(self) -> List[str]:
        """
        Get list of available swarm types.

        Returns:
            List[str]: List of available swarm types
        """
        try:
            logger.info("Fetching available swarm types")
            response = await self._make_request("GET", "/v1/swarms/available")
            logger.info("Successfully fetched available swarm types")
            return response.get("swarm_types", [])

        except Exception as e:
            logger.error(f"Error fetching available swarm types: {str(e)}")
            raise

    async def run_agent(
        self,
        agent_name: str,
        task: str,
        model_name: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> Dict[str, Any]:
        """
        Run a single agent with specified configuration.

        Args:
            agent_name (str): Name of the agent
            task (str): Task for the agent to complete
            model_name (str): Model to use
            temperature (float): Temperature for generation
            max_tokens (int): Maximum tokens to generate

        Returns:
            Dict[str, Any]: Agent execution results
        """
        try:
            agent_data = {
                "agent_name": agent_name,
                "task": task,
                "model_name": model_name,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

            logger.info(f"Running agent: {agent_name}")
            response = await self._make_request(
                "POST", "/v1/agent/completions", data=agent_data
            )
            logger.info(f"Successfully ran agent: {agent_name}")
            return response

        except Exception as e:
            logger.error(f"Error running agent {agent_name}: {str(e)}")
            raise

    async def run_agent_batch(
        self,
        agents: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Run multiple agents in parallel.

        Args:
            agents (List[Dict[str, Any]]): List of agent configurations

        Returns:
            List[Dict[str, Any]]: Results from all agents
        """
        try:
            logger.info(f"Running batch of {len(agents)} agents")
            response = await self._make_request(
                "POST", "/v1/agent/batch/completions", data={"agents": agents}
            )
            logger.info(f"Successfully ran batch of {len(agents)} agents")
            return response

        except Exception as e:
            logger.error(f"Error running agent batch: {str(e)}")
            raise

    async def run_swarm_batch(
        self,
        swarms: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Run multiple swarms in parallel.

        Args:
            swarms (List[Dict[str, Any]]): List of swarm configurations

        Returns:
            List[Dict[str, Any]]: Results from all swarms
        """
        try:
            logger.info(f"Running batch of {len(swarms)} swarms")
            response = await self._make_request(
                "POST", "/v1/swarm/batch/completions", data={"swarms": swarms}
            )
            logger.info(f"Successfully ran batch of {len(swarms)} swarms")
            return response

        except Exception as e:
            logger.error(f"Error running swarm batch: {str(e)}")
            raise

    async def get_api_logs(self) -> List[Dict[str, Any]]:
        """
        Get all API request logs for the current API key.

        Returns:
            List[Dict[str, Any]]: List of API request logs
        """
        try:
            logger.info("Fetching API logs")
            response = await self._make_request("GET", "/v1/swarm/logs")
            logger.info("Successfully fetched API logs")
            return response.get("logs", [])

        except Exception as e:
            logger.error(f"Error fetching API logs: {str(e)}")
            raise

    def close(self):
        """Close the client session."""
        if self.session:
            asyncio.create_task(self.session.close())
            logger.info("Closed client session")
