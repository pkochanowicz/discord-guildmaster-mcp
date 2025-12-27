"""Member management tools for discord-guildmaster-mcp.

Provides member listing, searching, and information retrieval operations
following the test specifications defined in tests/tools/test_members.py.
"""

import discord
from typing import Dict, Any, Optional, List
from ..discord_client import get_client
from ..config import get_settings


async def list_members(
    guild_id: Optional[str] = None,
    limit: int = 50,
    role_id: Optional[str] = None
) -> Dict[str, Any]:
    """List members in a guild with optional role filtering.

    Test Contract (from test_members.py):
    - Returns: guild_id, members list, total_fetched, has_more
    - Each member: id, username, display_name, roles, joined_at
    - Default limit 50, max 1000
    - Optional role_id for filtering
    - Excludes bots automatically
    - Requires Members Intent
    - Raises ValueError if invalid limit, guild not found
    - Raises PermissionError if bot lacks permissions or Members Intent

    Args:
        guild_id: Discord guild ID (optional if default set)
        limit: Number of members to fetch (1-1000)
        role_id: Optional role ID to filter members

    Returns:
        Dict with member list

    Raises:
        ValueError: If invalid limit or guild not found
        PermissionError: If bot lacks permissions or Members Intent
    """
    # Resolve guild_id
    if not guild_id:
        settings = get_settings()
        guild_id = settings.discord_default_guild_id
        if not guild_id:
            raise ValueError("guild_id is required (no default configured)")

    # Validate limit
    if not 1 <= limit <= 1000:
        raise ValueError(f"Limit must be 1-1000 (got {limit})")

    # Validate guild_id format
    if not str(guild_id).isdigit() or len(str(guild_id)) < 17:
        raise ValueError(f"Invalid guild_id format: {guild_id}")

    # Fetch guild
    client = await get_client()

    # Check Members Intent
    if not client.intents.members:
        raise PermissionError("Members Intent not enabled (required for list_members)")

    try:
        guild = await client.fetch_guild(int(guild_id))
    except discord.NotFound:
        raise ValueError(f"Guild {guild_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access guild")

    # Fetch members
    try:
        # Note: fetch_members requires guild to be available (cached)
        # For better compatibility, we'll use guild.chunk() or guild.fetch_members()
        members_list = []

        if role_id:
            # Filter by role
            async for member in guild.fetch_members(limit=limit):
                if member.bot:
                    continue
                if any(str(role.id) == role_id for role in member.roles):
                    members_list.append({
                        "id": str(member.id),
                        "username": member.name,
                        "display_name": member.display_name,
                        "roles": [str(r.id) for r in member.roles if r.id != guild.id],  # Exclude @everyone
                        "joined_at": member.joined_at.isoformat() if member.joined_at else None
                    })
                if len(members_list) >= limit:
                    break
        else:
            # No role filter
            async for member in guild.fetch_members(limit=limit):
                if member.bot:
                    continue
                members_list.append({
                    "id": str(member.id),
                    "username": member.name,
                    "display_name": member.display_name,
                    "roles": [str(r.id) for r in member.roles if r.id != guild.id],  # Exclude @everyone
                    "joined_at": member.joined_at.isoformat() if member.joined_at else None
                })

    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to list guild members")

    return {
        "guild_id": str(guild.id),
        "members": members_list,
        "total_fetched": len(members_list),
        "has_more": len(members_list) == limit
    }


async def get_member_info(
    guild_id: Optional[str] = None,
    user_id: str = None
) -> Dict[str, Any]:
    """Get detailed information about a guild member.

    Test Contract (from test_members.py):
    - Returns: member_id, username, display_name, roles, joined_at, avatar_url, premium_since
    - Requires guild_id and user_id
    - Raises ValueError if member not found in guild
    - Raises PermissionError if bot lacks permissions

    Args:
        guild_id: Discord guild ID (optional if default set)
        user_id: Discord user ID (required)

    Returns:
        Dict with member details

    Raises:
        ValueError: If member not found
        PermissionError: If bot lacks permissions
    """
    # Resolve guild_id
    if not guild_id:
        settings = get_settings()
        guild_id = settings.discord_default_guild_id
        if not guild_id:
            raise ValueError("guild_id is required (no default configured)")

    # Validate required parameter
    if not user_id:
        raise ValueError("user_id is required")

    # Validate ID formats
    if not str(guild_id).isdigit() or len(str(guild_id)) < 17:
        raise ValueError(f"Invalid guild_id format: {guild_id}")
    if not str(user_id).isdigit() or len(str(user_id)) < 17:
        raise ValueError(f"Invalid user_id format: {user_id}")

    # Fetch guild and member
    client = await get_client()

    try:
        guild = await client.fetch_guild(int(guild_id))
    except discord.NotFound:
        raise ValueError(f"Guild {guild_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access guild")

    try:
        member = await guild.fetch_member(int(user_id))
    except discord.NotFound:
        raise ValueError(f"Member {user_id} not found in guild")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access member")

    # Build response
    return {
        "member_id": str(member.id),
        "username": member.name,
        "display_name": member.display_name,
        "roles": [
            {
                "id": str(role.id),
                "name": role.name
            }
            for role in member.roles
            if role.id != guild.id  # Exclude @everyone
        ],
        "joined_at": member.joined_at.isoformat() if member.joined_at else None,
        "avatar_url": str(member.avatar.url) if member.avatar else None,
        "premium_since": member.premium_since.isoformat() if member.premium_since else None
    }


async def search_members(
    guild_id: Optional[str] = None,
    query: str = None,
    limit: int = 25
) -> Dict[str, Any]:
    """Search for members by username or nickname.

    Test Contract (from test_members.py):
    - Returns: guild_id, members list, total_found, query
    - Each member: id, username, display_name, match_score
    - Max limit 100
    - Case-insensitive partial matching
    - Raises ValueError if query empty, limit invalid, guild not found
    - Requires Members Intent

    Args:
        guild_id: Discord guild ID (optional if default set)
        query: Search query string (required)
        limit: Maximum results to return (1-100)

    Returns:
        Dict with search results

    Raises:
        ValueError: If query empty, invalid limit, or guild not found
        PermissionError: If bot lacks Members Intent
    """
    # Resolve guild_id
    if not guild_id:
        settings = get_settings()
        guild_id = settings.discord_default_guild_id
        if not guild_id:
            raise ValueError("guild_id is required (no default configured)")

    # Validate required parameter
    if not query:
        raise ValueError("query is required")

    # Validate limit
    if not 1 <= limit <= 100:
        raise ValueError(f"Limit must be 1-100 (got {limit})")

    # Validate guild_id format
    if not str(guild_id).isdigit() or len(str(guild_id)) < 17:
        raise ValueError(f"Invalid guild_id format: {guild_id}")

    # Fetch guild
    client = await get_client()

    # Check Members Intent
    if not client.intents.members:
        raise PermissionError("Members Intent not enabled (required for search_members)")

    try:
        guild = await client.fetch_guild(int(guild_id))
    except discord.NotFound:
        raise ValueError(f"Guild {guild_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access guild")

    # Search members
    query_lower = query.lower()
    matches = []

    try:
        async for member in guild.fetch_members(limit=1000):  # Fetch up to 1000 to search
            if member.bot:
                continue

            # Check username and display name
            username_match = query_lower in member.name.lower()
            display_match = query_lower in member.display_name.lower()

            if username_match or display_match:
                # Simple match score: 2 if both match, 1 if one matches
                match_score = (2 if username_match and display_match else 1)

                matches.append({
                    "id": str(member.id),
                    "username": member.name,
                    "display_name": member.display_name,
                    "match_score": match_score
                })

                if len(matches) >= limit:
                    break

    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to search guild members")

    # Sort by match score (highest first)
    matches.sort(key=lambda m: m["match_score"], reverse=True)

    return {
        "guild_id": str(guild.id),
        "members": matches,
        "total_found": len(matches),
        "query": query
    }


async def get_user_id_by_name(
    guild_id: Optional[str] = None,
    username: str = None
) -> Dict[str, Any]:
    """Get user ID by exact username match.

    Test Contract (from test_members.py):
    - Returns: user_id, username, display_name, guild_id
    - Requires exact username match (case-insensitive)
    - Raises ValueError if username not provided, not found, guild not found
    - Requires Members Intent

    Args:
        guild_id: Discord guild ID (optional if default set)
        username: Exact username to find (required)

    Returns:
        Dict with user information

    Raises:
        ValueError: If username not provided, not found, or guild not found
        PermissionError: If bot lacks Members Intent
    """
    # Resolve guild_id
    if not guild_id:
        settings = get_settings()
        guild_id = settings.discord_default_guild_id
        if not guild_id:
            raise ValueError("guild_id is required (no default configured)")

    # Validate required parameter
    if not username:
        raise ValueError("username is required")

    # Validate guild_id format
    if not str(guild_id).isdigit() or len(str(guild_id)) < 17:
        raise ValueError(f"Invalid guild_id format: {guild_id}")

    # Fetch guild
    client = await get_client()

    # Check Members Intent
    if not client.intents.members:
        raise PermissionError("Members Intent not enabled (required for get_user_id_by_name)")

    try:
        guild = await client.fetch_guild(int(guild_id))
    except discord.NotFound:
        raise ValueError(f"Guild {guild_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access guild")

    # Search for exact username match
    username_lower = username.lower()

    try:
        async for member in guild.fetch_members(limit=1000):
            if member.name.lower() == username_lower:
                return {
                    "user_id": str(member.id),
                    "username": member.name,
                    "display_name": member.display_name,
                    "guild_id": str(guild.id)
                }

    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to search guild members")

    # Not found
    raise ValueError(f"User '{username}' not found in guild")
