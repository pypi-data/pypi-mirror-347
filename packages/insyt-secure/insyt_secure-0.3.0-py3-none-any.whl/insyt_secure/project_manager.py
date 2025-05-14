"""Project Manager for handling multiple CodeExecutor instances."""

import os
import sys
import asyncio
import logging
import time
import signal
from typing import Dict, List, Optional, Tuple

from insyt_secure.executor.code_executor import CodeExecutor, AuthenticationError, NetworkRestrictionError
from insyt_secure.utils.dns_cache import DNSCache

logger = logging.getLogger(__name__)

class ProjectManager:
    """
    Manages multiple CodeExecutor instances, one for each project.
    
    This class handles the coordination of multiple independent project connections,
    allowing each to have its own credentials and connection state.
    """
    
    def __init__(self):
        """Initialize the project manager."""
        self.executors = {}  # project_id -> CodeExecutor
        self.credentials = {}  # project_id -> credentials
        self.tasks = {}  # project_id -> asyncio task
        self.running = False
        
        # Shared DNS cache across all executors
        self.dns_cache = DNSCache(ttl_seconds=86400)  # 24 hours
        logger.info("Initialized shared DNS cache with 24-hour TTL")
        
        # Project-specific settings
        self.max_workers = {}  # project_id -> max_workers
        self.timeout = {}  # project_id -> execution_timeout
        
        # Shared settings
        self.allowed_hosts = None
        self.always_allowed_domains = ["insyt.co", "localhost"]
        
    async def add_project(self, project_id: str, api_key: str, api_url: str, 
                         max_workers: int = 5, timeout: int = 30) -> bool:
        """
        Add a new project to be managed.
        
        Args:
            project_id: The project ID
            api_key: API key for authenticating with the credentials API
            api_url: The base URL of the credentials API
            max_workers: Maximum number of concurrent code executions
            timeout: Default execution timeout in seconds
            
        Returns:
            bool: True if project was added successfully, False otherwise
        """
        if project_id in self.executors:
            logger.warning(f"Project {project_id} is already being managed")
            return False
            
        logger.info(f"Adding project {project_id} to manager")
        
        # Store project-specific settings
        self.max_workers[project_id] = max_workers
        self.timeout[project_id] = timeout
        
        # Start the project
        if self.running:
            # Create and start a task for this project
            task = asyncio.create_task(
                self._run_project(project_id, api_key, api_url)
            )
            self.tasks[project_id] = task
            
        return True
        
    async def remove_project(self, project_id: str) -> bool:
        """
        Remove a project from management.
        
        Args:
            project_id: The project ID to remove
            
        Returns:
            bool: True if project was removed successfully, False otherwise
        """
        if project_id not in self.executors:
            logger.warning(f"Project {project_id} is not being managed")
            return False
            
        logger.info(f"Removing project {project_id} from manager")
        
        # Cancel the project's task if it exists
        if project_id in self.tasks:
            task = self.tasks[project_id]
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.tasks[project_id]
            
        # Clean up the executor
        if project_id in self.executors:
            executor = self.executors[project_id]
            del self.executors[project_id]
            
        # Clean up other project-specific data
        if project_id in self.credentials:
            del self.credentials[project_id]
        if project_id in self.max_workers:
            del self.max_workers[project_id]
        if project_id in self.timeout:
            del self.timeout[project_id]
            
        return True
    
    def set_shared_network_options(self, allowed_hosts=None, always_allowed_domains=None):
        """Set shared network security options for all projects."""
        if allowed_hosts is not None:
            self.allowed_hosts = allowed_hosts
            
        if always_allowed_domains is not None:
            self.always_allowed_domains = always_allowed_domains
            
        logger.debug(f"Updated shared network options - allowed hosts: {self.allowed_hosts}, allowed domains: {self.always_allowed_domains}")
    
    async def start(self):
        """Start all project executors."""
        if self.running:
            logger.warning("Project manager is already running")
            return
            
        self.running = True
        logger.info("Starting project manager")
        
        # Setup signal handlers for clean shutdown
        self._setup_signal_handlers()
        
        # Start a task for each configured project
        for project_id in list(self.max_workers.keys()):
            # Only start projects that aren't already running
            if project_id not in self.tasks:
                api_key = None  # TODO: Get API key from stored configuration
                api_url = None  # TODO: Get API URL from stored configuration
                
                if api_key and api_url:
                    task = asyncio.create_task(
                        self._run_project(project_id, api_key, api_url)
                    )
                    self.tasks[project_id] = task
        
        # Wait for all tasks to complete (they should run indefinitely)
        running_tasks = list(self.tasks.values())
        if running_tasks:
            done, pending = await asyncio.wait(
                running_tasks, 
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # If any task completes, log it
            for task in done:
                try:
                    result = task.result()
                    logger.info(f"Project task completed with result: {result}")
                except Exception as e:
                    logger.error(f"Project task failed with error: {str(e)}")
    
    async def stop(self):
        """Stop all project executors."""
        if not self.running:
            logger.warning("Project manager is not running")
            return
            
        logger.info("Stopping project manager")
        self.running = False
        
        # Cancel all running tasks
        for project_id, task in list(self.tasks.items()):
            if not task.done():
                logger.info(f"Cancelling task for project {project_id}")
                task.cancel()
                
        # Wait for all tasks to be cancelled
        for project_id, task in list(self.tasks.items()):
            try:
                await task
            except asyncio.CancelledError:
                logger.debug(f"Task for project {project_id} cancelled successfully")
            except Exception as e:
                logger.error(f"Error while cancelling task for project {project_id}: {str(e)}")
                
        # Clear all tasks
        self.tasks.clear()
        
        logger.info("All project executors stopped")
    
    def _setup_signal_handlers(self):
        """Set up signal handlers for graceful shutdown."""
        # Skip in Windows due to asyncio compatibility issues with signals
        if os.name == 'nt':
            return
            
        loop = asyncio.get_running_loop()
        
        # Handle SIGTERM (termination) and SIGINT (keyboard interrupt)
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig,
                lambda: asyncio.create_task(self._handle_signal(sig))
            )
            
    async def _handle_signal(self, sig):
        """Handle shutdown signals."""
        sig_name = signal.Signals(sig).name
        logger.info(f"Received signal {sig_name}, shutting down...")
        
        await self.stop()
        
        # Signal the main loop to exit
        loop = asyncio.get_running_loop()
        loop.stop()
    
    async def _run_project(self, project_id, api_key, api_url):
        """
        Run a single project executor.
        
        This method acquires credentials, starts the executor, and handles
        reconnection and credential refreshing as needed.
        
        Args:
            project_id: The project ID
            api_key: API key for authentication
            api_url: API base URL
        """
        from insyt_secure.main import get_credentials
        
        consecutive_auth_errors = 0
        max_auth_retries = 20
        auth_error_delay = 15
        
        while self.running:
            try:
                # Get credentials for this project
                logger.info(f"Acquiring credentials for project {project_id}")
                credentials = get_credentials(project_id, api_url, api_key)
                logger.info(f"Successfully acquired credentials for project {project_id}")
                
                # Store credentials
                self.credentials[project_id] = credentials
                
                # Reset auth error counter
                if consecutive_auth_errors > 0:
                    logger.info(f"Successfully recovered after {consecutive_auth_errors} authentication errors for project {project_id}")
                    consecutive_auth_errors = 0
                
                # Create or get executor
                if project_id not in self.executors:
                    logger.info(f"Creating new executor for project {project_id}")
                    executor = CodeExecutor(
                        mqtt_broker=credentials['broker'],
                        mqtt_port=int(credentials['port']),
                        mqtt_username=credentials['username'],
                        mqtt_password=credentials['password'],
                        subscribe_topic=credentials['topic'],
                        publish_topic=credentials.get('response_topic', f"response/{credentials['topic']}"),
                        ssl_enabled=credentials.get('ssl_enabled', True),
                        allowed_ips=self.allowed_hosts,
                        always_allowed_domains=self.always_allowed_domains,
                        max_workers=self.max_workers.get(project_id, 5),
                        execution_timeout=self.timeout.get(project_id, 30)
                    )
                    # Use shared DNS cache
                    executor.dns_cache = self.dns_cache
                    self.executors[project_id] = executor
                else:
                    # Update existing executor with new credentials
                    logger.info(f"Updating credentials for existing project {project_id}")
                    executor = self.executors[project_id]
                    executor.mqtt_broker = credentials['broker']
                    executor.mqtt_port = int(credentials['port'])
                    executor.mqtt_username = credentials['username']
                    executor.mqtt_password = credentials['password']
                    executor.subscribe_topic = credentials['topic']
                    executor.publish_topic = credentials.get('response_topic', f"response/{credentials['topic']}")
                    executor.ssl_enabled = credentials.get('ssl_enabled', True)
                
                # Start the executor
                logger.info(f"Starting executor for project {project_id}")
                await executor.start()
                
                # If we reach here, it means start() returned normally,
                # which usually indicates credentials have expired
                logger.warning(f"Executor for project {project_id} disconnected. Getting new credentials...")
                
                # Increment auth error counter
                consecutive_auth_errors += 1
                
                # Check for too many auth errors
                if consecutive_auth_errors >= max_auth_retries:
                    logger.critical(f"Too many consecutive auth errors ({consecutive_auth_errors}) for project {project_id}")
                    logger.critical(f"Removing project {project_id} from management")
                    await self.remove_project(project_id)
                    return
                
                # Wait before retry
                logger.info(f"Waiting {auth_error_delay} seconds before requesting new credentials for project {project_id}")
                await asyncio.sleep(auth_error_delay)
                
            except NetworkRestrictionError as e:
                logger.critical(f"Network restriction error for project {project_id}: {str(e)}")
                logger.critical(f"Removing project {project_id} due to security concerns")
                await self.remove_project(project_id)
                return
                
            except Exception as e:
                logger.error(f"Unexpected error for project {project_id}: {str(e)}")
                logger.info(f"Retrying in 10 seconds for project {project_id}...")
                await asyncio.sleep(10)
                
                # If we have too many errors, consider removing the project
                consecutive_auth_errors += 1
                if consecutive_auth_errors >= max_auth_retries:
                    logger.critical(f"Too many errors ({consecutive_auth_errors}) for project {project_id}, removing from management")
                    await self.remove_project(project_id)
                    return 