"""
Swarms API Client

This module provides a production-grade client for interacting with the Swarms API.
It includes both synchronous and asynchronous APIs for maximum flexibility.

Example:
    ```python
    from swarms_client import SwarmsClient

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
import concurrent.futures
import hashlib
import json
import threading
import time
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin

import aiohttp
import requests
from cachetools import TTLCache
from loguru import logger
from pydantic import ValidationError

from swarms_client.config import SwarmsConfig
from swarms_client.models import AgentCompletion, AgentSpec, SwarmSpec
from swarms_client.retry import RetryHandler

# Thread-local storage for sync client session
_thread_local = threading.local()


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
        max_concurrent_requests (int): Maximum number of concurrent requests
        thread_pool_size (int): Maximum number of threads for sync operations
        session (aiohttp.ClientSession): Async HTTP session for making requests
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        max_concurrent_requests: Optional[int] = None,
        retry_on_status: Optional[Set[int]] = None,
        retry_delay: Optional[float] = None,
        max_retry_delay: Optional[int] = None,
        jitter: bool = True,
        enable_cache: bool = True,
        thread_pool_size: Optional[int] = None,
    ):
        """
        Initialize the Swarms API client with optimized settings.

        Args:
            api_key (Optional[str]): API key for authentication. If not provided,
                will look for SWARMS_API_KEY environment variable.
            base_url (Optional[str]): Base URL for the API. Defaults to value from config.
            timeout (Optional[int]): Request timeout in seconds.
            max_retries (Optional[int]): Maximum number of retries for failed requests.
            max_concurrent_requests (Optional[int]): Maximum number of concurrent requests.
            retry_on_status (Optional[Set[int]]): HTTP status codes to retry on.
            retry_delay (Optional[float]): Initial delay between retries in seconds.
            max_retry_delay (Optional[int]): Maximum delay between retries in seconds.
            jitter (bool): Whether to add random jitter to retry delays.
            enable_cache (bool): Whether to enable response caching.
            thread_pool_size (Optional[int]): Maximum number of threads for sync operations.

        Raises:
            AuthenticationError: If no API key is provided or found in environment.
        """
        self.api_key = api_key or SwarmsConfig.get_api_key()

        if not self.api_key:
            raise AuthenticationError(
                "No API key provided. Set SWARMS_API_KEY environment variable or pass api_key parameter."
            )

        self.base_url = (base_url or SwarmsConfig.get_base_url()).rstrip("/")
        self.timeout = timeout or SwarmsConfig.get_timeout()
        self.max_retries = max_retries or SwarmsConfig.get_max_retries()
        self.max_concurrent_requests = (
            max_concurrent_requests or SwarmsConfig.get_max_concurrent_requests()
        )

        # Initialize thread pool for sync operations
        self.thread_pool_size = thread_pool_size or min(
            32, self.max_concurrent_requests * 2
        )
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.thread_pool_size, thread_name_prefix="swarms_client_worker"
        )

        # Initialize async semaphore
        self.semaphore = asyncio.Semaphore(self.max_concurrent_requests)

        # Initialize sessions
        self.async_session = None

        # Initialize response cache
        self.enable_cache = enable_cache
        if enable_cache:
            self.cache = TTLCache(
                maxsize=1000, ttl=SwarmsConfig.get_response_cache_ttl()
            )

        # Initialize retry handler
        self.retry_handler = RetryHandler(
            max_retries=self.max_retries,
            retry_delay=retry_delay or SwarmsConfig.get_retry_delay(),
            max_retry_delay=max_retry_delay or SwarmsConfig.get_max_retry_delay(),
            retry_on_status=retry_on_status,
            jitter=jitter,
        )

        logger.info(f"Initialized SwarmsClient with base URL: {self.base_url}")

    def _get_sync_session(self) -> requests.Session:
        """Get or create thread-local sync session."""
        if not hasattr(_thread_local, "session"):
            session = requests.Session()
            session.headers.update(self._get_headers())
            adapter = requests.adapters.HTTPAdapter(
                pool_connections=self.max_concurrent_requests,
                pool_maxsize=self.max_concurrent_requests,
                max_retries=self.max_retries,
                pool_block=False,
            )
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            _thread_local.session = session
        return _thread_local.session

    async def __aenter__(self):
        """Create optimized aiohttp session when entering async context."""
        tcp_connector = aiohttp.TCPConnector(
            limit=self.max_concurrent_requests,
            ttl_dns_cache=SwarmsConfig.get_dns_cache_ttl(),
            use_dns_cache=True,
            force_close=False,
            enable_cleanup_closed=True,
            tcp_nodelay=SwarmsConfig.get_tcp_nodelay(),
            keepalive_timeout=SwarmsConfig.get_keepalive_timeout(),
        )

        self.async_session = aiohttp.ClientSession(
            headers=self._get_headers(),
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            connector=tcp_connector,
            json_serialize=json.dumps,
            raise_for_status=True,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the async session when exiting context."""
        if self.async_session:
            await self.async_session.close()

    def __enter__(self):
        """Enter sync context."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit sync context and cleanup."""
        self.close()

    def close(self):
        """Close all sessions and cleanup resources."""
        if hasattr(_thread_local, "session"):
            _thread_local.session.close()
            delattr(_thread_local, "session")

        if self.thread_pool:
            self.thread_pool.shutdown(wait=False)

        if self.async_session and not self.async_session.closed:
            asyncio.create_task(self.async_session.close())

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

    def _get_cache_key(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> str:
        """Generate a unique cache key for the request."""
        key_parts = [method, endpoint]
        if params:
            key_parts.append(json.dumps(params, sort_keys=True))
        if data:
            key_parts.append(json.dumps(data, sort_keys=True))
        key_string = "|".join(key_parts)
        return hashlib.sha256(key_string.encode()).hexdigest()

    async def _async_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        skip_cache: bool = False,
    ) -> Dict[str, Any]:
        """Make an optimized async HTTP request."""
        url = urljoin(self.base_url, endpoint)

        # Check cache for GET requests
        if self.enable_cache and method == "GET" and not skip_cache:
            cache_key = self._get_cache_key(method, endpoint, params=params)
            cached_response = self.cache.get(cache_key)
            if cached_response is not None:
                logger.debug(f"Cache hit for {url}")
                return cached_response

        async def _do_request() -> Tuple[Dict[str, Any], float]:
            start_time = time.time()
            async with self.semaphore:
                async with self.async_session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    compress=True,
                ) as response:
                    response_data = await response.json()
                    request_time = time.time() - start_time

                    if response.status == 200:
                        return response_data, request_time
                    elif response.status == 401:
                        raise AuthenticationError("Invalid API key")
                    elif response.status == 429:
                        raise RateLimitError("Rate limit exceeded")
                    else:
                        raise APIError(
                            f"API request failed: {response_data.get('detail', 'Unknown error')}",
                            response.status,
                            response_data,
                        )

        try:
            response_data, request_time = await self.retry_handler.execute_with_retry(
                _do_request
            )

            # Cache successful GET responses
            if self.enable_cache and method == "GET" and not skip_cache:
                cache_key = self._get_cache_key(method, endpoint, params=params)
                self.cache[cache_key] = response_data

            logger.debug(f"Request to {url} completed in {request_time:.2f}s")
            return response_data

        except aiohttp.ClientError as e:
            logger.error(f"Network error: {str(e)}")
            raise SwarmsError(f"Network error: {str(e)}")

    def _sync_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        skip_cache: bool = False,
    ) -> Dict[str, Any]:
        """Make an optimized sync HTTP request."""
        url = urljoin(self.base_url, endpoint)

        # Check cache for GET requests
        if self.enable_cache and method == "GET" and not skip_cache:
            cache_key = self._get_cache_key(method, endpoint, params=params)
            cached_response = self.cache.get(cache_key)
            if cached_response is not None:
                logger.debug(f"Cache hit for {url}")
                return cached_response

        session = self._get_sync_session()
        start_time = time.time()

        try:
            response = session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout,
            )
            request_time = time.time() - start_time

            response_data = response.json()

            if response.status_code == 200:
                # Cache successful GET responses
                if self.enable_cache and method == "GET" and not skip_cache:
                    cache_key = self._get_cache_key(method, endpoint, params=params)
                    self.cache[cache_key] = response_data

                logger.debug(f"Request to {url} completed in {request_time:.2f}s")
                return response_data
            elif response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            else:
                raise APIError(
                    f"API request failed: {response_data.get('detail', 'Unknown error')}",
                    response.status_code,
                    response_data,
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {str(e)}")
            raise SwarmsError(f"Network error: {str(e)}")

    # Async methods
    async def async_get_health(self) -> Dict[str, Any]:
        """
        Check API health status asynchronously.

        Returns:
            Dict[str, Any]: Health status information
        """
        try:
            logger.info("Checking API health")
            response = await self._async_request("GET", "/health")
            logger.info("API health check successful")
            return response
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            raise

    async def async_create_swarm(
        self,
        name: str,
        task: str,
        agents: List[AgentSpec],
        description: Optional[str] = None,
        max_loops: int = 1,
        swarm_type: Optional[str] = None,
        rearrange_flow: Optional[str] = None,
        return_history: bool = True,
        rules: Optional[str] = None,
        tasks: Optional[List[str]] = None,
        messages: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False,
        service_tier: str = "standard",
    ) -> Dict[str, Any]:
        """
        Create and run a swarm with specified configuration asynchronously.

        Args:
            name (str): Name of the swarm
            task (str): Main task for the swarm
            agents (List[AgentSpec]): List of agent specifications
            description (Optional[str]): Swarm description
            max_loops (int): Maximum execution loops
            swarm_type (Optional[str]): Type of swarm architecture
            rearrange_flow (Optional[str]): Flow rearrangement instructions
            return_history (bool): Whether to return execution history
            rules (Optional[str]): Swarm behavior rules
            tasks (Optional[List[str]]): List of tasks
            messages (Optional[List[Dict[str, Any]]]): List of messages
            stream (bool): Whether to stream output
            service_tier (str): Service tier for processing

        Returns:
            Dict[str, Any]: Swarm execution results
        """
        try:
            # Create swarm spec using Pydantic model for validation
            swarm_spec = SwarmSpec(
                name=name,
                description=description,
                agents=agents,
                max_loops=max_loops,
                swarm_type=swarm_type,
                rearrange_flow=rearrange_flow,
                task=task,
                return_history=return_history,
                rules=rules,
                tasks=tasks,
                messages=messages,
                stream=stream,
                service_tier=service_tier,
            )

            logger.info(f"Creating swarm: {name}")
            response = await self._async_request(
                "POST",
                "/v1/swarm/completions",
                data=swarm_spec.model_dump(exclude_none=True),
            )
            logger.info(f"Successfully created swarm: {name}")
            return response

        except Exception as e:
            logger.error(f"Error creating swarm: {str(e)}")
            raise

    async def async_run_swarm(self, swarm_id: str) -> Dict[str, Any]:
        """
        Run a swarm with the specified ID asynchronously.

        Args:
            swarm_id (str): ID of the swarm to run

        Returns:
            Dict[str, Any]: Swarm execution results
        """
        try:
            logger.info(f"Running swarm: {swarm_id}")
            response = await self._async_request("POST", f"/v1/swarm/{swarm_id}/run")
            logger.info(f"Successfully ran swarm: {swarm_id}")
            return response

        except Exception as e:
            logger.error(f"Error running swarm {swarm_id}: {str(e)}")
            raise

    async def async_get_swarm_logs(self, swarm_id: str) -> List[Dict[str, Any]]:
        """
        Get execution logs for a specific swarm asynchronously.

        Args:
            swarm_id (str): ID of the swarm

        Returns:
            List[Dict[str, Any]]: List of log entries
        """
        try:
            logger.info(f"Fetching logs for swarm: {swarm_id}")
            response = await self._async_request("GET", f"/v1/swarm/{swarm_id}/logs")
            logger.info(f"Successfully fetched logs for swarm: {swarm_id}")
            return response.get("logs", [])

        except Exception as e:
            logger.error(f"Error fetching logs for swarm {swarm_id}: {str(e)}")
            raise

    async def async_get_available_models(self) -> List[str]:
        """
        Get list of available models asynchronously.

        Returns:
            List[str]: List of available model names
        """
        try:
            logger.info("Fetching available models")
            response = await self._async_request("GET", "/v1/models/available")
            logger.info("Successfully fetched available models")
            return response.get("models", [])

        except Exception as e:
            logger.error(f"Error fetching available models: {str(e)}")
            raise

    async def async_get_swarm_types(self) -> List[str]:
        """
        Get list of available swarm types asynchronously.

        Returns:
            List[str]: List of available swarm types
        """
        try:
            logger.info("Fetching available swarm types")
            response = await self._async_request("GET", "/v1/swarms/available")
            logger.info("Successfully fetched available swarm types")
            return response.get("swarm_types", [])

        except Exception as e:
            logger.error(f"Error fetching available swarm types: {str(e)}")
            raise

    async def async_run_agent(
        self,
        agent_name: str,
        task: str,
        model_name: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None,
        description: Optional[str] = None,
        auto_generate_prompt: bool = False,
        role: str = "worker",
        max_loops: int = 1,
        tools_dictionary: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Run a single agent asynchronously.

        Args:
            agent_name (str): Name of the agent
            task (str): Task for the agent to complete
            model_name (str): Model to use
            temperature (float): Temperature for generation
            max_tokens (int): Maximum tokens to generate
            system_prompt (Optional[str]): System prompt for the agent
            description (Optional[str]): Description of the agent
            auto_generate_prompt (bool): Whether to auto-generate prompts
            role (str): Role of the agent
            max_loops (int): Maximum number of loops
            tools_dictionary (Optional[List[Dict[str, Any]]]): Tools for the agent

        Returns:
            Dict[str, Any]: Agent execution results
        """
        try:
            # Create agent spec using Pydantic model for validation
            agent_spec = AgentSpec(
                agent_name=agent_name,
                description=description,
                system_prompt=system_prompt,
                model_name=model_name,
                auto_generate_prompt=auto_generate_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                role=role,
                max_loops=max_loops,
                tools_dictionary=tools_dictionary,
            )

            # Create completion request
            completion = AgentCompletion(agent_config=agent_spec, task=task)

            logger.info(f"Running agent: {agent_name}")
            response = await self._async_request(
                "POST",
                "/v1/agent/completions",
                data=completion.model_dump(exclude_none=True),
            )
            logger.info(f"Successfully ran agent: {agent_name}")
            return response

        except Exception as e:
            logger.error(f"Error running agent {agent_name}: {str(e)}")
            raise

    async def async_run_agent_batch(
        self,
        agents: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Run multiple agents in parallel asynchronously.

        Args:
            agents (List[Dict[str, Any]]): List of agent configurations

        Returns:
            List[Dict[str, Any]]: Results from all agents
        """
        try:
            logger.info(f"Running batch of {len(agents)} agents")
            response = await self._async_request(
                "POST", "/v1/agent/batch/completions", data={"agents": agents}
            )
            logger.info(f"Successfully ran batch of {len(agents)} agents")
            return response

        except Exception as e:
            logger.error(f"Error running agent batch: {str(e)}")
            raise

    async def async_run_swarm_batch(
        self,
        swarms: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Run multiple swarms in parallel asynchronously.

        Args:
            swarms (List[Dict[str, Any]]): List of swarm configurations

        Returns:
            List[Dict[str, Any]]: Results from all swarms
        """
        try:
            logger.info(f"Running batch of {len(swarms)} swarms")
            response = await self._async_request(
                "POST", "/v1/swarm/batch/completions", data={"swarms": swarms}
            )
            logger.info(f"Successfully ran batch of {len(swarms)} swarms")
            return response

        except Exception as e:
            logger.error(f"Error running swarm batch: {str(e)}")
            raise

    async def async_get_api_logs(self) -> List[Dict[str, Any]]:
        """
        Get all API request logs for the current API key asynchronously.

        Returns:
            List[Dict[str, Any]]: List of API request logs
        """
        try:
            logger.info("Fetching API logs")
            response = await self._async_request("GET", "/v1/swarm/logs")
            logger.info("Successfully fetched API logs")
            return response.get("logs", [])

        except Exception as e:
            logger.error(f"Error fetching API logs: {str(e)}")
            raise

    # Sync methods
    def get_health(self) -> Dict[str, Any]:
        """
        Check API health status synchronously.

        Returns:
            Dict[str, Any]: Health status information
        """
        try:
            logger.info("Checking API health")
            response = self._sync_request("GET", "/health")
            logger.info("API health check successful")
            return response
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            raise

    def create_swarm(
        self,
        name: str,
        task: str,
        agents: List[AgentSpec],
        description: Optional[str] = None,
        max_loops: int = 1,
        swarm_type: Optional[str] = None,
        rearrange_flow: Optional[str] = None,
        return_history: bool = True,
        rules: Optional[str] = None,
        tasks: Optional[List[str]] = None,
        messages: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False,
        service_tier: str = "standard",
    ) -> Dict[str, Any]:
        """
        Create and run a swarm with specified configuration synchronously.

        Args:
            name (str): Name of the swarm
            task (str): Main task for the swarm
            agents (List[AgentSpec]): List of agent specifications
            description (Optional[str]): Swarm description
            max_loops (int): Maximum execution loops
            swarm_type (Optional[str]): Type of swarm architecture
            rearrange_flow (Optional[str]): Flow rearrangement instructions
            return_history (bool): Whether to return execution history
            rules (Optional[str]): Swarm behavior rules
            tasks (Optional[List[str]]): List of tasks
            messages (Optional[List[Dict[str, Any]]]): List of messages
            stream (bool): Whether to stream output
            service_tier (str): Service tier for processing

        Returns:
            Dict[str, Any]: Swarm execution results
        """
        try:
            # Create swarm spec using Pydantic model for validation
            swarm_spec = SwarmSpec(
                name=name,
                description=description,
                agents=agents,
                max_loops=max_loops,
                swarm_type=swarm_type,
                rearrange_flow=rearrange_flow,
                task=task,
                return_history=return_history,
                rules=rules,
                tasks=tasks,
                messages=messages,
                stream=stream,
                service_tier=service_tier,
            )

            logger.info(f"Creating swarm: {name}")
            response = self._sync_request(
                "POST",
                "/v1/swarm/completions",
                data=swarm_spec.model_dump(exclude_none=True),
            )
            logger.info(f"Successfully created swarm: {name}")
            return response

        except Exception as e:
            logger.error(f"Error creating swarm: {str(e)}")
            raise

    def run_swarm(self, swarm_id: str) -> Dict[str, Any]:
        """
        Run a swarm with the specified ID synchronously.

        Args:
            swarm_id (str): ID of the swarm to run

        Returns:
            Dict[str, Any]: Swarm execution results
        """
        try:
            logger.info(f"Running swarm: {swarm_id}")
            response = self._sync_request("POST", f"/v1/swarm/{swarm_id}/run")
            logger.info(f"Successfully ran swarm: {swarm_id}")
            return response

        except Exception as e:
            logger.error(f"Error running swarm {swarm_id}: {str(e)}")
            raise

    def get_swarm_logs(self, swarm_id: str) -> List[Dict[str, Any]]:
        """
        Get execution logs for a specific swarm synchronously.

        Args:
            swarm_id (str): ID of the swarm

        Returns:
            List[Dict[str, Any]]: List of log entries
        """
        try:
            logger.info(f"Fetching logs for swarm: {swarm_id}")
            response = self._sync_request("GET", f"/v1/swarm/{swarm_id}/logs")
            logger.info(f"Successfully fetched logs for swarm: {swarm_id}")
            return response.get("logs", [])

        except Exception as e:
            logger.error(f"Error fetching logs for swarm {swarm_id}: {str(e)}")
            raise

    def get_available_models(self) -> List[str]:
        """
        Get list of available models synchronously.

        Returns:
            List[str]: List of available model names
        """
        try:
            logger.info("Fetching available models")
            response = self._sync_request("GET", "/v1/models/available")
            logger.info("Successfully fetched available models")
            return response.get("models", [])

        except Exception as e:
            logger.error(f"Error fetching available models: {str(e)}")
            raise

    def run_agent(
        self,
        agent_name: str,
        task: str,
        model_name: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None,
        description: Optional[str] = None,
        auto_generate_prompt: bool = False,
        role: str = "worker",
        max_loops: int = 1,
        tools_dictionary: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Run a single agent synchronously.

        Args:
            agent_name (str): Name of the agent
            task (str): Task for the agent to complete
            model_name (str): Model to use
            temperature (float): Temperature for generation
            max_tokens (int): Maximum tokens to generate
            system_prompt (Optional[str]): System prompt for the agent
            description (Optional[str]): Description of the agent
            auto_generate_prompt (bool): Whether to auto-generate prompts
            role (str): Role of the agent
            max_loops (int): Maximum number of loops
            tools_dictionary (Optional[List[Dict[str, Any]]]): Tools for the agent

        Returns:
            Dict[str, Any]: Agent execution results
        """
        try:
            # Create agent spec using Pydantic model for validation
            agent_spec = AgentSpec(
                agent_name=agent_name,
                description=description,
                system_prompt=system_prompt,
                model_name=model_name,
                auto_generate_prompt=auto_generate_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                role=role,
                max_loops=max_loops,
                tools_dictionary=tools_dictionary,
            )

            # Create completion request
            completion = AgentCompletion(agent_config=agent_spec, task=task)

            logger.info(f"Running agent: {agent_name}")
            response = self._sync_request(
                "POST",
                "/v1/agent/completions",
                data=completion.model_dump(exclude_none=True),
            )
            logger.info(f"Successfully ran agent: {agent_name}")
            return response

        except Exception as e:
            logger.error(f"Error running agent {agent_name}: {str(e)}")
            raise

    def run_agent_batch(
        self,
        agents: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Run multiple agents in parallel synchronously.

        Args:
            agents (List[Dict[str, Any]]): List of agent configurations

        Returns:
            List[Dict[str, Any]]: Results from all agents
        """
        try:
            logger.info(f"Running batch of {len(agents)} agents")
            response = self._sync_request(
                "POST", "/v1/agent/batch/completions", data={"agents": agents}
            )
            logger.info(f"Successfully ran batch of {len(agents)} agents")
            return response

        except Exception as e:
            logger.error(f"Error running agent batch: {str(e)}")
            raise

    def get_swarm_types(self) -> List[str]:
        """
        Get list of available swarm types synchronously.

        Returns:
            List[str]: List of available swarm types
        """
        try:
            logger.info("Fetching available swarm types")
            response = self._sync_request("GET", "/v1/swarms/available")
            logger.info("Successfully fetched available swarm types")
            return response.get("swarm_types", [])

        except Exception as e:
            logger.error(f"Error fetching available swarm types: {str(e)}")
            raise

    def get_api_logs(self) -> List[Dict[str, Any]]:
        """
        Get all API request logs for the current API key synchronously.

        Returns:
            List[Dict[str, Any]]: List of API request logs
        """
        try:
            logger.info("Fetching API logs")
            response = self._sync_request("GET", "/v1/swarm/logs")
            logger.info("Successfully fetched API logs")
            return response.get("logs", [])

        except Exception as e:
            logger.error(f"Error fetching API logs: {str(e)}")
            raise
