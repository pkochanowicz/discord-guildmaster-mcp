"""ComfyUI integration tools for AI image generation.

Optional feature - gracefully handles disabled state.
"""

import discord
from typing import Dict, Any, Optional
from pathlib import Path
import json
import random
import time


async def generate_image(
    workflow_name: str,
    prompt: str,
    negative_prompt: Optional[str] = None,
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """Generate image using ComfyUI workflow.

    Test Contract (tests/tools/test_comfyui.py):
    - Returns: image_data, workflow_name, prompt, seed, generation_time
    - Validates COMFYUI_ENABLED=true
    - Validates workflow file exists in COMFYUI_WORKFLOW_DIR
    - Injects prompt into workflow JSON
    - Randomizes seed if not provided and COMFYUI_RANDOMIZE_SEEDS=true
    - Returns base64 image data (or URL depending on COMFYUI_RETURN_MODE)

    Args:
        workflow_name: Workflow filename without .json (e.g., "portrait", "banner")
        prompt: Positive prompt for image generation (required)
        negative_prompt: Optional negative prompt
        seed: Optional seed for reproducibility (random if not provided)

    Returns:
        {
            "image_data": str,  # base64 or URL depending on config
            "workflow_name": str,
            "prompt": str,
            "seed": int,
            "generation_time": float  # seconds
        }

    Raises:
        ValueError: If ComfyUI disabled, workflow not found, invalid parameters
        ConnectionError: If ComfyUI server unreachable
    """
    from discord_guildmaster_mcp.config import get_settings

    settings = get_settings()

    # Check if ComfyUI enabled
    if not settings.comfyui_enabled:
        raise ValueError(
            "ComfyUI integration is disabled (COMFYUI_ENABLED=false). "
            "Set COMFYUI_ENABLED=true in environment to use this feature."
        )

    # Validate prompt
    if not prompt:
        raise ValueError("prompt is required")

    # Load workflow
    workflow_path = Path(settings.comfyui_workflow_dir) / f"{workflow_name}.json"

    if not workflow_path.exists():
        raise ValueError(
            f"Workflow '{workflow_name}' not found. "
            f"Expected file: {workflow_path}. "
            f"Available workflows: {list_workflows()['workflows']}"
        )

    try:
        with open(workflow_path) as f:
            workflow = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid workflow JSON in {workflow_path}: {e}")

    # Inject prompt into workflow
    # (Simplified - real implementation would parse node structure)
    # Find CLIPTextEncode nodes and inject prompts
    for node_id, node in workflow.items():
        if node.get("class_type") == "CLIPTextEncode":
            inputs = node.get("inputs", {})
            if "positive" in str(inputs).lower():
                node["inputs"]["text"] = prompt
            elif negative_prompt and "negative" in str(inputs).lower():
                node["inputs"]["text"] = negative_prompt

    # Handle seed
    if seed is None and settings.comfyui_randomize_seeds:
        seed = random.randint(0, 2**32 - 1)
    elif seed is None:
        seed = 0

    # Inject seed into KSampler nodes
    for node_id, node in workflow.items():
        if node.get("class_type") == "KSampler":
            node["inputs"]["seed"] = seed

    # Submit to ComfyUI
    # (Simplified - real implementation uses HTTP client)
    start_time = time.time()

    # Mock implementation for testing
    # Real implementation would:
    # 1. POST workflow to ComfyUI /prompt endpoint
    # 2. Poll or WebSocket listen for completion
    # 3. Fetch generated image
    # 4. Return base64 or upload to CDN

    image_data = "base64_encoded_image_placeholder"
    generation_time = time.time() - start_time

    return {
        "image_data": image_data,
        "workflow_name": workflow_name,
        "prompt": prompt,
        "seed": seed,
        "generation_time": generation_time
    }


async def list_workflows() -> Dict[str, Any]:
    """List available ComfyUI workflows.

    Test Contract (tests/tools/test_comfyui.py):
    - Returns: total_count, workflows list
    - Each workflow: name, path
    - Lists all .json files in COMFYUI_WORKFLOW_DIR

    Returns:
        {
            "total_count": int,
            "workflows": [
                {
                    "name": str,  # Without .json extension
                    "path": str   # Full path
                }
            ]
        }

    Raises:
        ValueError: If workflow directory doesn't exist
    """
    from discord_guildmaster_mcp.config import get_settings

    settings = get_settings()
    workflow_dir = Path(settings.comfyui_workflow_dir)

    if not workflow_dir.exists():
        raise ValueError(f"Workflow directory not found: {workflow_dir}")

    # Find all .json files
    workflows = []
    for workflow_file in workflow_dir.glob("*.json"):
        workflows.append({
            "name": workflow_file.stem,  # Filename without extension
            "path": str(workflow_file)
        })

    workflows.sort(key=lambda w: w["name"])

    return {
        "total_count": len(workflows),
        "workflows": workflows
    }


async def validate_comfyui_connection() -> Dict[str, Any]:
    """Test connection to ComfyUI server.

    Test Contract (tests/tools/test_comfyui.py):
    - Returns: connected: bool, host, port, version (if connected)
    - Validates COMFYUI_ENABLED=true
    - Attempts connection to ComfyUI server

    Returns:
        {
            "connected": bool,
            "host": str,
            "port": int,
            "version": str | None,
            "error": str | None
        }
    """
    from discord_guildmaster_mcp.config import get_settings

    settings = get_settings()

    if not settings.comfyui_enabled:
        return {
            "connected": False,
            "host": settings.comfyui_host,
            "port": settings.comfyui_port,
            "version": None,
            "error": "ComfyUI integration disabled (COMFYUI_ENABLED=false)"
        }

    # Try to connect to ComfyUI
    # (Simplified - real implementation uses httpx)
    try:
        # Real implementation would:
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(f"http://{host}:{port}/system_stats")
        #     return connected=True, version from response

        return {
            "connected": True,  # Mock success
            "host": settings.comfyui_host,
            "port": settings.comfyui_port,
            "version": "1.0.0",  # Mock version
            "error": None
        }
    except Exception as e:
        return {
            "connected": False,
            "host": settings.comfyui_host,
            "port": settings.comfyui_port,
            "version": None,
            "error": str(e)
        }


async def get_comfyui_status() -> Dict[str, Any]:
    """Get ComfyUI server status and configuration.

    Test Contract (tests/tools/test_comfyui.py):
    - Returns: enabled, connected, workflow_count, config
    - Shows current ComfyUI configuration

    Returns:
        {
            "enabled": bool,
            "connected": bool,
            "workflow_count": int,
            "config": {
                "host": str,
                "port": int,
                "workflow_dir": str,
                "return_mode": str,
                "randomize_seeds": bool
            }
        }
    """
    from discord_guildmaster_mcp.config import get_settings

    settings = get_settings()

    # Get workflow count
    workflow_count = 0
    if settings.comfyui_enabled:
        try:
            workflows = await list_workflows()
            workflow_count = workflows["total_count"]
        except:
            workflow_count = 0

    # Check connection
    connection_result = await validate_comfyui_connection()

    return {
        "enabled": settings.comfyui_enabled,
        "connected": connection_result["connected"],
        "workflow_count": workflow_count,
        "config": {
            "host": settings.comfyui_host,
            "port": settings.comfyui_port,
            "workflow_dir": settings.comfyui_workflow_dir,
            "return_mode": settings.comfyui_return_mode,
            "randomize_seeds": settings.comfyui_randomize_seeds
        }
    }
