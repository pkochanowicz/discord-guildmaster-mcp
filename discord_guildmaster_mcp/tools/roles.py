"""Role management tools for discord-guildmaster-mcp.

Provides role listing, assignment, and removal operations following the test
specifications defined in tests/tools/test_roles.py.
"""

import discord
from typing import Dict, Any, Optional
from ..discord_client import get_client
from ..config import get_settings


async def list_roles(guild_id: Optional[str] = None) -> Dict[str, Any]:
    """List all roles in a guild ordered by position (hierarchy).

    Test Contract (from test_roles.py):
    - Returns guild_id, roles[], total_roles
    - Each role: id, name, position, color, permissions, managed, mentionable
    - Roles ordered by position (lowest first)
    - Includes @everyone role at position 0
    - Uses default guild_id from settings if not provided
    - Validates guild_id format
    - Raises ValueError if guild_id invalid or guild not found
    - Raises PermissionError if bot lacks permissions

    Args:
        guild_id: Discord guild ID (uses default if None)

    Returns:
        Dict with role list and metadata

    Raises:
        ValueError: If guild_id invalid or guild not found
        PermissionError: If bot lacks permissions
    """
    # Validate and resolve guild_id
    settings = get_settings()
    target_guild_id = guild_id or settings.discord_default_guild_id

    if not target_guild_id:
        raise ValueError("guild_id required (no default configured)")

    if not str(target_guild_id).isdigit() or len(str(target_guild_id)) < 17:
        raise ValueError(f"Invalid guild_id format: {target_guild_id}")

    # Fetch guild
    client = await get_client()

    try:
        guild = await client.fetch_guild(int(target_guild_id))
    except discord.NotFound:
        raise ValueError(f"Guild {target_guild_id} not found")
    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to list roles")

    # Build role list sorted by position
    roles = []
    for role in sorted(guild.roles, key=lambda r: r.position):
        role_data = {
            "id": str(role.id),
            "name": role.name,
            "position": role.position,
            "color": role.color.value,
            "permissions": role.permissions.value,
            "managed": role.managed,
            "mentionable": role.mentionable
        }
        roles.append(role_data)

    return {
        "guild_id": target_guild_id,
        "roles": roles,
        "total_roles": len(roles)
    }


async def assign_role(
    user_id: str,
    role_id: str,
    guild_id: Optional[str] = None
) -> Dict[str, Any]:
    """Assign a role to a guild member (DESTRUCTIVE).

    Test Contract (from test_roles.py):
    - Returns success: True, user_id, role_id, message
    - Requires user_id and role_id
    - Optional guild_id (uses default if not provided)
    - Checks role hierarchy (bot cannot assign roles higher than its own)
    - Idempotent: no error if role already assigned
    - Validates all IDs
    - Raises ValueError if IDs invalid, member/role not found
    - Raises PermissionError if bot lacks Manage Roles or hierarchy violation

    Args:
        user_id: Discord user ID (required)
        role_id: Discord role ID (required)
        guild_id: Discord guild ID (uses default if None)

    Returns:
        Dict with success status and confirmation message

    Raises:
        ValueError: If IDs invalid or member/role not found
        PermissionError: If bot lacks permissions or hierarchy violation
    """
    # Validate required parameters
    if not user_id:
        raise ValueError("user_id is required")
    if not role_id:
        raise ValueError("role_id is required")

    # Validate ID formats
    if not str(user_id).isdigit() or len(str(user_id)) < 17:
        raise ValueError(f"Invalid user_id format: {user_id}")
    if not str(role_id).isdigit() or len(str(role_id)) < 17:
        raise ValueError(f"Invalid role_id format: {role_id}")

    # Validate and resolve guild_id
    settings = get_settings()
    target_guild_id = guild_id or settings.discord_default_guild_id

    if not target_guild_id:
        raise ValueError("guild_id required (no default configured)")

    if not str(target_guild_id).isdigit() or len(str(target_guild_id)) < 17:
        raise ValueError(f"Invalid guild_id format: {target_guild_id}")

    # Fetch guild
    client = await get_client()

    try:
        guild = await client.fetch_guild(int(target_guild_id))
    except discord.NotFound:
        raise ValueError(f"Guild {target_guild_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access guild")

    # Fetch member
    try:
        member = await guild.fetch_member(int(user_id))
    except discord.NotFound:
        raise ValueError(f"Member {user_id} not found in guild")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access member")

    # Fetch role
    role = guild.get_role(int(role_id))
    if role is None:
        raise ValueError(f"Role {role_id} not found in guild")

    # Check role hierarchy: bot can only assign roles lower than its top role
    bot_member = guild.me
    if bot_member:
        bot_top_role = bot_member.top_role
        if role.position >= bot_top_role.position:
            raise PermissionError(
                f"Cannot assign role higher than bot's highest role "
                f"(role position: {role.position}, bot position: {bot_top_role.position})"
            )

    # Check if member already has the role (idempotent behavior)
    if role in member.roles:
        return {
            "success": True,
            "user_id": user_id,
            "role_id": role_id,
            "message": f"Role {role_id} already assigned to user {user_id}"
        }

    # Assign role
    try:
        await member.add_roles(role)
    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to assign role")

    return {
        "success": True,
        "user_id": user_id,
        "role_id": role_id,
        "message": f"Role {role_id} assigned to user {user_id}"
    }


async def remove_role(
    user_id: str,
    role_id: str,
    guild_id: Optional[str] = None
) -> Dict[str, Any]:
    """Remove a role from a guild member (DESTRUCTIVE).

    Test Contract (from test_roles.py):
    - Returns success: True, user_id, role_id, message
    - Requires user_id and role_id
    - Optional guild_id (uses default if not provided)
    - Checks role hierarchy (bot cannot remove roles higher than its own)
    - Idempotent: no error if role not assigned
    - Cannot remove @everyone role
    - Validates all IDs
    - Raises ValueError if IDs invalid, member/role not found, or @everyone
    - Raises PermissionError if bot lacks Manage Roles or hierarchy violation

    Args:
        user_id: Discord user ID (required)
        role_id: Discord role ID (required)
        guild_id: Discord guild ID (uses default if None)

    Returns:
        Dict with success status and confirmation message

    Raises:
        ValueError: If IDs invalid, member/role not found, or @everyone role
        PermissionError: If bot lacks permissions or hierarchy violation
    """
    # Validate required parameters
    if not user_id:
        raise ValueError("user_id is required")
    if not role_id:
        raise ValueError("role_id is required")

    # Validate ID formats
    if not str(user_id).isdigit() or len(str(user_id)) < 17:
        raise ValueError(f"Invalid user_id format: {user_id}")
    if not str(role_id).isdigit() or len(str(role_id)) < 17:
        raise ValueError(f"Invalid role_id format: {role_id}")

    # Validate and resolve guild_id
    settings = get_settings()
    target_guild_id = guild_id or settings.discord_default_guild_id

    if not target_guild_id:
        raise ValueError("guild_id required (no default configured)")

    if not str(target_guild_id).isdigit() or len(str(target_guild_id)) < 17:
        raise ValueError(f"Invalid guild_id format: {target_guild_id}")

    # Fetch guild
    client = await get_client()

    try:
        guild = await client.fetch_guild(int(target_guild_id))
    except discord.NotFound:
        raise ValueError(f"Guild {target_guild_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access guild")

    # Fetch member
    try:
        member = await guild.fetch_member(int(user_id))
    except discord.NotFound:
        raise ValueError(f"Member {user_id} not found in guild")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access member")

    # Fetch role
    role = guild.get_role(int(role_id))
    if role is None:
        raise ValueError(f"Role {role_id} not found in guild")

    # Prevent removal of @everyone role
    if role.name == "@everyone":
        raise ValueError("Cannot remove @everyone role from member")

    # Check role hierarchy: bot can only remove roles lower than its top role
    bot_member = guild.me
    if bot_member:
        bot_top_role = bot_member.top_role
        if role.position >= bot_top_role.position:
            raise PermissionError(
                f"Cannot remove role higher than bot's highest role "
                f"(role position: {role.position}, bot position: {bot_top_role.position})"
            )

    # Check if member doesn't have the role (idempotent behavior)
    if role not in member.roles:
        return {
            "success": True,
            "user_id": user_id,
            "role_id": role_id,
            "message": f"Role {role_id} not assigned to user {user_id} (no action needed)"
        }

    # Remove role
    try:
        await member.remove_roles(role)
    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to remove role")

    return {
        "success": True,
        "user_id": user_id,
        "role_id": role_id,
        "message": f"Role {role_id} removed from user {user_id}"
    }
