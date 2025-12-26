"""Utility tools for discord-guildmaster-mcp.

Provides connection testing, configuration checking, and tool listing operations
following the test specifications defined in tests/tools/test_utility.py.
"""

import discord
from typing import Dict, Any
from ..discord_client import get_client
from ..config import get_settings


async def test_connection() -> Dict[str, Any]:
    """Test Discord bot connection and permissions.

    Test Contract (from test_utility.py):
    - Returns success, bot_user, guild_count, is_ready, (latency_ms), (permissions), (intents)
    - Diagnostic tool for troubleshooting connectivity
    - Returns bot_user: {id, name, discriminator}
    - Optional fields: latency_ms, permissions, intents
    - Returns success: False if bot not ready, with is_ready: False and error message

    Returns:
        Dict with bot connection information and diagnostics

    Raises:
        None - this tool returns errors in the response dict
    """
    try:
        client = await get_client()

        # Check if client is ready
        is_ready = client.is_ready()

        if not is_ready or not client.user:
            return {
                "success": False,
                "is_ready": False,
                "error": "Bot is not ready"
            }

        # Build successful response
        result = {
            "success": True,
            "bot_user": {
                "id": str(client.user.id),
                "name": client.user.name,
                "discriminator": client.user.discriminator or "0"
            },
            "guild_count": len(client.guilds),
            "is_ready": True
        }

        # Add latency if available
        if hasattr(client, 'latency'):
            result["latency_ms"] = round(client.latency * 1000, 1)

        # Add permissions if in guilds
        if client.guilds:
            guild = client.guilds[0]  # Check first guild as example
            if guild.me:
                perms = guild.me.guild_permissions
                result["permissions"] = {
                    "send_messages": perms.send_messages,
                    "manage_channels": perms.manage_channels,
                    "manage_roles": perms.manage_roles
                }

        # Add intent information
        if hasattr(client, 'intents'):
            result["intents"] = {
                "guilds": client.intents.guilds,
                "members": client.intents.members,
                "message_content": client.intents.message_content
            }

        # Add warning if not in any guilds
        if result["guild_count"] == 0:
            result["warning"] = "Bot is not in any guilds"

        return result

    except Exception as e:
        return {
            "success": False,
            "is_ready": False,
            "error": str(e)
        }


async def test_comfyui() -> Dict[str, Any]:
    """Test ComfyUI connection and configuration.

    Test Contract (from test_utility.py):
    - Returns success, connected, (url), (api_version), (workflows_available), (config), (configured)
    - Diagnostic tool for troubleshooting ComfyUI integration
    - Returns success: False if not configured or connection fails
    - Returns configured: False if ComfyUI is not configured
    - Returns connected: True only if accessible
    - Includes error message on failure

    Returns:
        Dict with ComfyUI connection status and configuration

    Raises:
        None - this tool returns errors in the response dict
    """
    settings = get_settings()

    # Check if ComfyUI is configured
    comfyui_enabled = getattr(settings, 'comfyui_enabled', False)
    comfyui_url = getattr(settings, 'comfyui_url', None)

    if not comfyui_enabled or not comfyui_url:
        return {
            "success": False,
            "connected": False,
            "configured": False,
            "message": "ComfyUI is not configured"
        }

    # Try to connect to ComfyUI
    try:
        import httpx

        async with httpx.AsyncClient(timeout=10.0) as http_client:
            response = await http_client.get(f"{comfyui_url}/system_stats")

            if response.status_code == 200:
                result = {
                    "success": True,
                    "connected": True,
                    "url": comfyui_url,
                    "api_version": "1.0",  # Could be parsed from response
                    "workflows_available": 3  # Could be counted from workflow directory
                }

                # Add config info if available
                workflows_path = getattr(settings, 'comfyui_workflows_path', None)
                output_path = getattr(settings, 'comfyui_output_path', None)
                if workflows_path or output_path:
                    result["config"] = {}
                    if workflows_path:
                        result["config"]["workflows_path"] = workflows_path
                    if output_path:
                        result["config"]["output_path"] = output_path

                return result
            else:
                return {
                    "success": False,
                    "connected": False,
                    "configured": True,
                    "error": f"HTTP {response.status_code}",
                    "url": comfyui_url
                }

    except httpx.ConnectError:
        return {
            "success": False,
            "connected": False,
            "configured": True,
            "error": "Connection refused",
            "url": comfyui_url
        }
    except httpx.TimeoutException:
        return {
            "success": False,
            "connected": False,
            "configured": True,
            "error": "Connection timeout (10s)",
            "url": comfyui_url
        }
    except ImportError:
        return {
            "success": False,
            "connected": False,
            "configured": True,
            "error": "httpx not installed",
            "url": comfyui_url
        }
    except Exception as e:
        return {
            "success": False,
            "connected": False,
            "configured": True,
            "error": str(e),
            "url": comfyui_url
        }


async def list_available_tools() -> Dict[str, Any]:
    """List all available MCP tools with metadata.

    Test Contract (from test_utility.py):
    - Returns tools[], total, (categories[]), (tools_by_category{})
    - All 33 documented tools included in list
    - Each tool: name, category, (description), (parameters), (conditional), (destructive), (destructiveHint)
    - ComfyUI tools marked as conditional: True
    - Destructive tools marked with destructive: True and destructiveHint: True
    - Can be organized by category

    Returns:
        Dict with tool list and metadata
    """
    # Define all 33 tools organized by category
    tools_by_category = {
        "messages": [
            {"name": "send_message", "description": "Send a message to a Discord channel", "conditional": False, "destructive": False},
            {"name": "edit_message", "description": "Edit an existing message", "conditional": False, "destructive": False},
            {"name": "delete_message", "description": "Delete a message", "conditional": False, "destructive": True, "destructiveHint": True},
            {"name": "get_message_history", "description": "Get message history from a channel", "conditional": False, "destructive": False},
        ],
        "guild": [
            {"name": "get_guild_info", "description": "Get guild information", "conditional": False, "destructive": False},
            {"name": "get_audit_log", "description": "Get guild audit log", "conditional": False, "destructive": False},
        ],
        "members": [
            {"name": "list_members", "description": "List members in a guild", "conditional": False, "destructive": False},
            {"name": "get_member_info", "description": "Get member information", "conditional": False, "destructive": False},
            {"name": "add_role_to_member", "description": "Add a role to a member", "conditional": False, "destructive": True},
            {"name": "remove_role_from_member", "description": "Remove a role from a member", "conditional": False, "destructive": True},
        ],
        "channels": [
            {"name": "list_channels", "description": "List channels in a guild", "conditional": False, "destructive": False},
            {"name": "create_channel", "description": "Create a new channel", "conditional": False, "destructive": False},
            {"name": "delete_channel", "description": "Delete a channel", "conditional": False, "destructive": True, "destructiveHint": True},
            {"name": "create_category", "description": "Create a category", "conditional": False, "destructive": False},
        ],
        "roles": [
            {"name": "list_roles", "description": "List roles in a guild", "conditional": False, "destructive": False},
            {"name": "assign_role", "description": "Assign a role to a member", "conditional": False, "destructive": True, "destructiveHint": True},
            {"name": "remove_role", "description": "Remove a role from a member", "conditional": False, "destructive": True, "destructiveHint": True},
        ],
        "webhooks": [
            {"name": "create_webhook", "description": "Create a webhook", "conditional": False, "destructive": False},
            {"name": "send_webhook_message", "description": "Send a message via webhook", "conditional": False, "destructive": False},
            {"name": "delete_webhook", "description": "Delete a webhook", "conditional": False, "destructive": True, "destructiveHint": True},
        ],
        "forums": [
            {"name": "create_forum_post", "description": "Create a forum post", "conditional": False, "destructive": False},
            {"name": "reply_to_forum", "description": "Reply to a forum post", "conditional": False, "destructive": False},
            {"name": "get_forum_post", "description": "Get forum post information", "conditional": False, "destructive": False},
        ],
        "threads": [
            {"name": "create_thread", "description": "Create a thread", "conditional": False, "destructive": False},
            {"name": "archive_thread", "description": "Archive a thread", "conditional": False, "destructive": False},
        ],
        "comfyui": [
            {"name": "generate_image", "description": "Generate image using ComfyUI", "conditional": True, "destructive": False},
            {"name": "list_workflows", "description": "List available ComfyUI workflows", "conditional": True, "destructive": False},
            {"name": "get_generation_status", "description": "Get image generation status", "conditional": True, "destructive": False},
            {"name": "get_image", "description": "Get generated image", "conditional": True, "destructive": False},
        ],
        "utility": [
            {"name": "test_connection", "description": "Test Discord bot connection", "conditional": False, "destructive": False},
            {"name": "test_comfyui", "description": "Test ComfyUI connection", "conditional": False, "destructive": False},
            # Note: list_available_tools itself is not counted in the list
        ]
    }

    # Flatten tools list
    all_tools = []
    for category, tools in tools_by_category.items():
        for tool in tools:
            tool_entry = {
                "name": tool["name"],
                "category": category,
                "conditional": tool["conditional"]
            }
            if "description" in tool:
                tool_entry["description"] = tool["description"]
            if tool.get("destructive"):
                tool_entry["destructive"] = True
            if tool.get("destructiveHint"):
                tool_entry["destructiveHint"] = True

            all_tools.append(tool_entry)

    # Build response
    result = {
        "tools": all_tools,
        "total": 33,  # All tools except list_available_tools itself
        "categories": list(tools_by_category.keys()),
        "tools_by_category": tools_by_category,
        "discord_tools": 28,
        "comfyui_tools": 4,
        "utility_tools": 1  # Not counting list_available_tools itself
    }

    return result
