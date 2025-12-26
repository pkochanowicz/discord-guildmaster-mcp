"""Guild information tools for discord-guildmaster-mcp.

Provides guild metadata retrieval and audit log access following the test
specifications defined in tests/tools/test_guild.py.
"""

import discord
from typing import Dict, Any, Optional
from ..discord_client import get_client
from ..config import get_settings


async def get_guild_info(guild_id: Optional[str] = None) -> Dict[str, Any]:
    """Get detailed information about a Discord guild.

    Test Contract (from test_guild.py):
    - Returns id, name, description, member_count, max_members, features,
      owner_id, created_at, icon_url, verification_level
    - Uses default guild ID from settings if guild_id not provided
    - Validates guild_id format (numeric, 17+ chars)
    - Response must be compact (< 500 tokens)
    - Raises ValueError if guild_id invalid or guild not found (discord.NotFound)
    - Raises PermissionError if bot lacks permissions (discord.Forbidden)

    Args:
        guild_id: Discord guild ID (uses default if None)

    Returns:
        Dict with guild information matching test specification

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
        raise ValueError(f"Invalid guild ID format: {target_guild_id}")

    # Fetch guild
    client = await get_client()

    try:
        guild = await client.fetch_guild(int(target_guild_id))
    except discord.NotFound:
        raise ValueError(f"Guild {target_guild_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access guild")

    # Build response
    return {
        "id": str(guild.id),
        "name": guild.name,
        "description": guild.description,
        "member_count": guild.member_count,
        "max_members": guild.max_members,
        "features": list(guild.features),
        "owner_id": str(guild.owner_id),
        "created_at": guild.created_at.isoformat(),
        "icon_url": str(guild.icon.url) if guild.icon else None,
        "verification_level": guild.verification_level.name
    }


async def get_audit_log(
    guild_id: Optional[str] = None,
    limit: int = 50,
    action_type: Optional[str] = None,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """Retrieve guild audit log entries with filtering and pagination.

    Test Contract (from test_guild.py):
    - Returns guild_id, entries[], total_entries, has_more
    - Each entry: id, action_type, user_id, target_id, reason, timestamp
    - Default limit=50, range 1-100
    - Supports filtering by action_type and user_id
    - Uses default guild_id from settings if not provided
    - Validates limit range (1-100)
    - Validates guild_id format
    - Raises ValueError if invalid params or guild not found
    - Raises PermissionError if bot lacks View Audit Log permission

    Args:
        guild_id: Discord guild ID (uses default if None)
        limit: Maximum entries to return (1-100, defaults to 50)
        action_type: Optional action type filter (e.g., "MEMBER_KICK")
        user_id: Optional moderator user ID filter

    Returns:
        Dict with audit log entries and pagination info

    Raises:
        ValueError: If params invalid or guild not found
        PermissionError: If bot lacks View Audit Log permission
    """
    # Validate parameters
    settings = get_settings()
    target_guild_id = guild_id or settings.discord_default_guild_id

    if not target_guild_id:
        raise ValueError("guild_id required (no default configured)")

    if not str(target_guild_id).isdigit() or len(str(target_guild_id)) < 17:
        raise ValueError(f"Invalid guild ID format: {target_guild_id}")

    if limit < 1 or limit > 100:
        raise ValueError(f"limit must be between 1 and 100, got {limit}")

    if user_id and (not str(user_id).isdigit() or len(str(user_id)) < 17):
        raise ValueError(f"Invalid user_id format: {user_id}")

    # Fetch guild
    client = await get_client()

    try:
        guild = await client.fetch_guild(int(target_guild_id))
    except discord.NotFound:
        raise ValueError(f"Guild {target_guild_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access guild")

    # Build audit log filters
    kwargs = {"limit": limit}

    # Map action_type string to discord.AuditLogAction enum if specified
    if action_type:
        try:
            # Convert string like "MEMBER_KICK" to discord.AuditLogAction.kick
            action_enum = getattr(discord.AuditLogAction, action_type.lower().replace("member_", ""))
            kwargs["action"] = action_enum
        except AttributeError:
            raise ValueError(f"Invalid action_type: {action_type}")

    if user_id:
        # Note: discord.py uses 'user' parameter for filtering by moderator
        user_obj = await client.fetch_user(int(user_id))
        kwargs["user"] = user_obj

    # Fetch audit log
    try:
        entries = []
        async for entry in guild.audit_logs(**kwargs):
            entries.append({
                "id": str(entry.id),
                "action_type": entry.action.name.upper().replace("_", "_"),
                "user_id": str(entry.user.id) if entry.user else None,
                "target_id": str(entry.target.id) if hasattr(entry.target, 'id') else None,
                "reason": entry.reason,
                "timestamp": entry.created_at.isoformat()
            })

            if len(entries) >= limit:
                break

    except discord.Forbidden:
        raise PermissionError("Bot lacks View Audit Log permission")

    return {
        "guild_id": target_guild_id,
        "entries": entries,
        "total_entries": len(entries),
        "has_more": len(entries) == limit
    }
