"""Utility and diagnostic tools for discord-guildmaster-mcp."""

import discord
from typing import Dict, Any
import time


async def health_check() -> Dict[str, Any]:
    """Perform health check of MCP server and Discord connection.

    Test Contract (tests/tools/test_utility.py):
    - Returns: status, discord_connected, uptime, version
    - No parameters required
    - Checks Discord bot connection status
    - Returns server uptime

    Returns:
        {
            "status": "healthy" | "degraded" | "unhealthy",
            "discord_connected": bool,
            "uptime": float,  # seconds
            "version": str
        }
    """
    from discord_guildmaster_mcp import __version__
    from discord_guildmaster_mcp.discord_client import get_client

    try:
        client = await get_client()
        discord_connected = client.is_ready()
    except:
        discord_connected = False

    # Determine overall status
    if discord_connected:
        status = "healthy"
    else:
        status = "unhealthy"

    # Calculate uptime (simplified - would track actual start time)
    uptime = time.time() % 86400  # Mock uptime

    return {
        "status": status,
        "discord_connected": discord_connected,
        "uptime": uptime,
        "version": __version__
    }


async def list_available_tools() -> Dict[str, Any]:
    """List all available MCP tools with descriptions.

    Test Contract (tests/tools/test_utility.py):
    - Returns: total_count, tools list, by_category
    - Each tool: name, description, category, parameter_count
    - Groups tools by category

    Returns:
        {
            "total_count": int,
            "tools": [...],
            "by_category": {
                "messages": int,
                "guild": int,
                "members": int,
                "channels": int,
                "roles": int,
                "webhooks": int,
                "forums": int,
                "threads": int,
                "comfyui": int,
                "utility": int
            }
        }
    """
    # Tool catalog (hardcoded for now - could be generated dynamically)
    tools = [
        # Messages
        {"name": "send_message", "category": "messages", "params": 2},
        {"name": "edit_message", "category": "messages", "params": 2},
        {"name": "delete_message", "category": "messages", "params": 1},
        {"name": "get_message_history", "category": "messages", "params": 2},

        # Guild
        {"name": "get_server_info", "category": "guild", "params": 1},
        {"name": "list_guilds", "category": "guild", "params": 1},

        # Members
        {"name": "list_members", "category": "members", "params": 3},
        {"name": "get_member_info", "category": "members", "params": 2},
        {"name": "add_role_to_member", "category": "members", "params": 4},
        {"name": "remove_role_from_member", "category": "members", "params": 4},

        # Channels
        {"name": "list_channels", "category": "channels", "params": 3},
        {"name": "create_channel", "category": "channels", "params": 5},
        {"name": "delete_channel", "category": "channels", "params": 3},
        {"name": "create_category", "category": "channels", "params": 4},

        # Roles
        {"name": "list_roles", "category": "roles", "params": 1},
        {"name": "assign_role", "category": "roles", "params": 4},
        {"name": "remove_role", "category": "roles", "params": 4},

        # Webhooks
        {"name": "create_webhook", "category": "webhooks", "params": 4},
        {"name": "send_webhook_message", "category": "webhooks", "params": 4},
        {"name": "delete_webhook", "category": "webhooks", "params": 2},

        # Forums
        {"name": "create_forum_post", "category": "forums", "params": 5},
        {"name": "list_forum_posts", "category": "forums", "params": 3},
        {"name": "manage_forum_tags", "category": "forums", "params": 4},

        # Threads
        {"name": "create_thread", "category": "threads", "params": 5},
        {"name": "manage_thread", "category": "threads", "params": 3},

        # ComfyUI
        {"name": "generate_image", "category": "comfyui", "params": 4},
        {"name": "list_workflows", "category": "comfyui", "params": 0},
        {"name": "validate_comfyui_connection", "category": "comfyui", "params": 0},
        {"name": "get_comfyui_status", "category": "comfyui", "params": 0},

        # Utility
        {"name": "health_check", "category": "utility", "params": 0},
        {"name": "list_available_tools", "category": "utility", "params": 0},
        {"name": "get_configuration", "category": "utility", "params": 0},
    ]

    # Count by category
    by_category = {}
    for tool in tools:
        category = tool["category"]
        by_category[category] = by_category.get(category, 0) + 1

    return {
        "total_count": len(tools),
        "tools": tools,
        "by_category": by_category
    }


async def get_configuration() -> Dict[str, Any]:
    """Get current MCP server configuration (non-sensitive values).

    Test Contract (tests/tools/test_utility.py):
    - Returns: theme, comfyui_enabled, default_guild_id (masked), log_level, etc.
    - Masks sensitive values (Discord token, full guild IDs)
    - Shows feature flags and operational settings

    Returns:
        {
            "theme": str,
            "comfyui_enabled": bool,
            "default_guild_id": str (masked),
            "log_level": str,
            "mcp_transport": str,
            "features": {
                "forums": bool,
                "threads": bool,
                "webhooks": bool,
                "comfyui": bool
            }
        }
    """
    from discord_guildmaster_mcp.config import get_settings

    settings = get_settings()

    # Mask guild ID (show last 4 digits only)
    masked_guild_id = None
    if settings.discord_default_guild_id:
        masked_guild_id = "***" + settings.discord_default_guild_id[-4:]

    return {
        "theme": settings.guildmaster_theme,
        "comfyui_enabled": settings.comfyui_enabled,
        "default_guild_id": masked_guild_id,
        "log_level": settings.log_level,
        "mcp_transport": settings.mcp_transport,
        "features": {
            "forums": True,  # All modern features available
            "threads": True,
            "webhooks": True,
            "comfyui": settings.comfyui_enabled
        }
    }
