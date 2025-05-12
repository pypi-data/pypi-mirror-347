"""
GA4GH Task Execution Service (TES) MCP Server

This MCP server connects to a GA4GH Task Execution Service endpoint and provides
tools for creating, monitoring, and managing computational tasks through the TES API.
"""

import os
import json
import httpx
from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime

from mcp.server.fastmcp import FastMCP


class TesState(str, Enum):
    """TES task states as defined in the GA4GH specification."""

    UNKNOWN = "UNKNOWN"
    QUEUED = "QUEUED"
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETE = "COMPLETE"
    EXECUTOR_ERROR = "EXECUTOR_ERROR"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    CANCELED = "CANCELED"


@dataclass
class TesExecutor:
    """TES Executor definition."""

    image: str
    command: List[str]
    workdir: Optional[str] = None
    env: Optional[Dict[str, str]] = None


@dataclass
class TesResources:
    """TES Resources definition."""

    cpu_cores: Optional[int] = None
    ram_gb: Optional[float] = None
    disk_gb: Optional[float] = None
    preemptible: Optional[bool] = None


@dataclass
class TesInput:
    """TES Input definition."""

    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None
    type: Optional[str] = None
    content: Optional[str] = None


@dataclass
class TesOutput:
    """TES Output definition."""

    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None
    type: Optional[str] = None


@dataclass
class TesTaskLog:
    """TES Task Log definition."""

    start_time: Optional[str] = None
    end_time: Optional[str] = None
    logs: Optional[List[Dict[str, Any]]] = None
    outputs: Optional[List[TesOutput]] = None
    system_logs: Optional[List[str]] = None


@dataclass
class TesTask:
    """TES Task definition."""

    id: Optional[str] = None
    state: Optional[TesState] = None
    name: Optional[str] = None
    description: Optional[str] = None
    executors: Optional[List[TesExecutor]] = None
    inputs: Optional[List[TesInput]] = None
    outputs: Optional[List[TesOutput]] = None
    resources: Optional[TesResources] = None
    tags: Optional[Dict[str, str]] = None
    logs: Optional[List[TesTaskLog]] = None


class TesClient:
    """Client for the GA4GH Task Execution Service API."""

    def __init__(self):
        """Initialize the TES client using environment variables."""
        self.base_url = os.environ.get("TES_URL", "http://localhost:8000").rstrip("/")
        self.headers = {}
        if token := os.environ.get("TES_TOKEN"):
            self.headers["Authorization"] = f"Bearer {token}"

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a request to the TES API."""
        url = f"{self.base_url}/{endpoint}"
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, headers=self.headers, params=params)
            elif method == "POST":
                response = await client.post(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = await client.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

    async def create_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task in the TES service."""
        return await self._make_request("POST", "v1/tasks", data=task)

    async def get_task(self, task_id: str, view: str = "BASIC") -> Dict[str, Any]:
        """Get details about a specific task."""
        return await self._make_request(
            "GET", f"v1/tasks/{task_id}", params={"view": view}
        )

    async def list_tasks(
        self, view: str = "MINIMAL", page_size: int = 10, page_token: str | None = None
    ) -> Dict[str, Any]:
        """List tasks from the TES service."""
        params = {"view": view, "page_size": page_size}
        if page_token:
            params["page_token"] = page_token
        return await self._make_request("GET", "v1/tasks", params=params)

    async def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """Cancel a running task."""
        return await self._make_request("POST", f"v1/tasks/{task_id}:cancel")

    async def get_service_info(self) -> Dict[str, Any]:
        """Get information about the TES service."""
        return await self._make_request("GET", "v1/service-info")


# Initialize the MCP server
mcp = FastMCP("GA4GH TES Server")


@mcp.tool()
async def get_service_info() -> str:
    """Get information about the TES service."""
    client = TesClient()
    service_info = await client.get_service_info()
    return json.dumps(service_info, indent=2)


@mcp.tool()
async def list_all_tasks() -> str:
    """List all tasks in the TES service."""
    client = TesClient()
    tasks = await client.list_tasks(view="BASIC")

    if not tasks.get("tasks"):
        return "No tasks found."

    task_list = []
    for task in tasks.get("tasks", []):
        task_list.append(
            {
                "id": task.get("id"),
                "name": task.get("name"),
                "state": task.get("state"),
                "description": task.get("description"),
            }
        )

    return json.dumps(task_list, indent=2)


@mcp.tool()
async def get_task_details(task_id: str) -> str:
    """Get detailed information about a specific task."""
    client = TesClient()
    task = await client.get_task(task_id, view="FULL")
    return json.dumps(task, indent=2)


@mcp.tool()
async def get_task_state(task_id: str) -> str:
    """Get the current state of a specific task."""
    client = TesClient()
    task = await client.get_task(task_id)
    state = task.get("state", "UNKNOWN")
    return f"Task {task_id} is in state: {state}"


@mcp.tool()
async def get_task_logs(task_id: str) -> str:
    """Get the logs of a specific task."""
    client = TesClient()
    task = await client.get_task(task_id, view="FULL")

    logs_output = []

    for i, log in enumerate(task.get("logs", [])):
        executor_logs = log.get("logs", [])
        system_logs = log.get("system_logs", [])

        logs_output.append(f"--- Execution Log {i+1} ---")
        logs_output.append(f"Start time: {log.get('start_time', 'N/A')}")
        logs_output.append(f"End time: {log.get('end_time', 'N/A')}")

        logs_output.append("\nExecutor Logs:")
        for j, exec_log in enumerate(executor_logs):
            logs_output.append(f"\n  Executor {j+1}:")
            logs_output.append(f"  - stdout: {exec_log.get('stdout', 'N/A')}")
            logs_output.append(f"  - stderr: {exec_log.get('stderr', 'N/A')}")
            logs_output.append(f"  - exit code: {exec_log.get('exit_code', 'N/A')}")

        if system_logs:
            logs_output.append("\nSystem Logs:")
            for sys_log in system_logs:
                logs_output.append(f"  - {sys_log}")

    if not logs_output:
        return f"No logs available for task {task_id}"

    return "\n".join(logs_output)


@mcp.tool()
async def create_task(
    name: str,
    image: str,
    command: str,
    description: Optional[str] = None,
    cpu_cores: Optional[int] = None,
    ram_gb: Optional[int] = None,
    disk_gb: Optional[int] = None,
    inputs: Optional[str] = None,
    outputs: Optional[str] = None,
    env_vars: Optional[str] = None,
) -> str:
    """
    Create a new task in the GA4GH TES service.

    Args:
        name: Name of the task
        image: Docker image to use (e.g., "ubuntu:latest")
        command: Command to run (as a string, will be split on spaces)
        description: Optional description of the task
        cpu_cores: Number of CPU cores to request
        ram_gb: Amount of RAM in GB
        disk_gb: Amount of disk space in GB
        inputs: JSON string of inputs [{name, url, path}, ...]
        outputs: JSON string of outputs [{name, url, path}, ...]
        env_vars: JSON string of environment variables {key: value, ...}

    Returns:
        Task ID and confirmation message
    """
    client = TesClient()

    # Parse command string into list
    command_list = command.split()

    # Initialize task structure
    task: dict[str, Any] = {
        "name": name,
        "executors": [{"image": image, "command": command_list}],
    }

    if description:
        task["description"] = description

    # Add resources if specified
    resources: dict[str, int] = {}
    if cpu_cores is not None:
        resources["cpu_cores"] = cpu_cores
    if ram_gb is not None:
        resources["ram_gb"] = ram_gb
    if disk_gb is not None:
        resources["disk_gb"] = disk_gb

    if resources:
        task["resources"] = resources

    # Parse environment variables
    if env_vars:
        try:
            env_dict = json.loads(env_vars)
            task["executors"][0]["env"] = env_dict
        except json.JSONDecodeError as e:
            return f"Error parsing environment variables: {e}"

    # Parse inputs
    if inputs:
        try:
            input_list = json.loads(inputs)
            task["inputs"] = input_list
        except json.JSONDecodeError as e:
            return f"Error parsing inputs: {e}"

    # Parse outputs
    if outputs:
        try:
            output_list = json.loads(outputs)
            task["outputs"] = output_list
        except json.JSONDecodeError as e:
            return f"Error parsing outputs: {e}"

    # Create the task
    try:
        response = await client.create_task(task)
        task_id = response.get("id")
        return f"Task created successfully with ID: {task_id}"
    except Exception as e:
        return f"Failed to create task: {e}"


@mcp.tool()
async def cancel_task(task_id: str) -> str:
    """
    Cancel a running task.

    Args:
        task_id: ID of the task to cancel

    Returns:
        Confirmation message
    """
    client = TesClient()

    try:
        await client.cancel_task(task_id)
        return f"Task {task_id} has been canceled"
    except Exception as e:
        return f"Failed to cancel task: {e}"


@mcp.tool()
async def quick_task(command: str, image: str = "ubuntu:latest") -> str:
    """
    Quickly create a simple task with minimal parameters.

    Args:
        command: Command to run
        image: Docker image to use (defaults to ubuntu:latest)

    Returns:
        Task ID and confirmation message
    """
    client = TesClient()

    # Create a simple task with timestamp as name
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    name = f"quick-task-{timestamp}"

    task: dict[str, Any] = {
        "name": name,
        "description": f"Quick task created at {timestamp}",
        "executors": [{"image": image, "command": command.split()}],
    }

    try:
        response = await client.create_task(task)
        task_id = response.get("id")
        return f"Quick task created with ID: {task_id}"
    except Exception as e:
        return f"Failed to create quick task: {e}"


@mcp.prompt()
def create_simple_task() -> str:
    """Create a simple task in the GA4GH TES service."""
    return """
    I'll help you create a task in the GA4GH Task Execution Service.
    
    Let's walk through the process step by step:
    
    1. What Docker image would you like to use? (e.g., ubuntu:latest, python:3.9)
    2. What command would you like to run?
    3. Do you want to specify any resource requirements (CPU, RAM, disk)?
    4. Do you need any inputs or outputs for your task?
    
    Once you provide these details, I can help you build and submit the task.
    """


if __name__ == "__main__":
    mcp.run()
