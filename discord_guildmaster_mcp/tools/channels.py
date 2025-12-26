"""Channel management tools for discord-guildmaster-mcp.

Provides channel creation, listing, and deletion operations following the test
specifications defined in tests/tools/test_channels.py.
"""

import discord
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from ..discord_client import get_client
from ..config import get_settings


# Channel type mapping: discord.ChannelType enum <-> string names
CHANNEL_TYPE_TO_ENUM = {
    "text": discord.ChannelType.text,
    "voice": discord.ChannelType.voice,
    "category": discord.ChannelType.category,
    "forum": discord.ChannelType.forum,
    "announcement": discord.ChannelType.news,
    "stage": discord.ChannelType.stage_voice,
}

ENUM_TO_CHANNEL_TYPE = {v: k for k, v in CHANNEL_TYPE_TO_ENUM.items()}


async def list_channels(guild_id: Optional[str] = None) -> Dict[str, Any]:
    """List all channels in a guild organized by type.

    Test Contract (from test_channels.py):
    - Returns guild_id, text_channels[], voice_channels[], categories[],
      forum_channels[], total_channels
    - Each channel: id, name, type, position, topic (if text)
    - Uses default guild_id from settings if not provided
    - Validates guild_id format
    - Raises ValueError if guild_id invalid or guild not found
    - Raises PermissionError if bot lacks permissions

    Args:
        guild_id: Discord guild ID (uses default if None)

    Returns:
        Dict with categorized channel lists

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

    # Fetch guild and channels
    client = await get_client()

    try:
        guild = await client.fetch_guild(int(target_guild_id))
    except discord.NotFound:
        raise ValueError(f"Guild {target_guild_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access guild")

    # Categorize channels by type
    text_channels = []
    voice_channels = []
    categories = []
    forum_channels = []

    for channel in guild.channels:
        channel_data = {
            "id": str(channel.id),
            "name": channel.name,
            "type": ENUM_TO_CHANNEL_TYPE.get(channel.type, "unknown"),
            "position": channel.position
        }

        # Add type-specific fields
        if hasattr(channel, 'topic') and channel.topic:
            channel_data["topic"] = channel.topic

        # Categorize
        if channel.type == discord.ChannelType.text:
            text_channels.append(channel_data)
        elif channel.type == discord.ChannelType.voice:
            voice_channels.append(channel_data)
        elif channel.type == discord.ChannelType.category:
            categories.append(channel_data)
        elif channel.type == discord.ChannelType.forum:
            forum_channels.append(channel_data)

    result = {
        "guild_id": target_guild_id,
        "text_channels": text_channels,
        "voice_channels": voice_channels,
        "categories": categories,
        "total_channels": len(guild.channels)
    }

    # Include forum_channels only if any exist
    if forum_channels:
        result["forum_channels"] = forum_channels

    return result


async def create_channel(
    guild_id: Optional[str] = None,
    name: str = None,
    channel_type: str = "text",
    parent_id: Optional[str] = None,
    **settings
) -> Dict[str, Any]:
    """Create a new channel with optional parent category.

    Test Contract (from test_channels.py):
    - Returns channel_id, name, type, guild_id, (user_limit for voice)
    - Requires name parameter
    - channel_type: "text", "voice", "announcement"
    - Optional parent_id to place channel in category
    - Type-specific settings: user_limit (voice), topic (text)
    - Validates all parameters
    - Raises ValueError if params invalid or category not found
    - Raises PermissionError if bot lacks Manage Channels permission

    Args:
        guild_id: Discord guild ID (uses default if None)
        name: Channel name (required)
        channel_type: "text", "voice", or "announcement" (default: "text")
        parent_id: Optional parent category ID
        **settings: Type-specific settings (user_limit, topic, etc.)

    Returns:
        Dict with created channel details

    Raises:
        ValueError: If name missing, type invalid, or category not found
        PermissionError: If bot lacks Manage Channels permission
    """
    # Validate required parameters
    if not name:
        raise ValueError("Channel name is required")

    # Validate channel type
    if channel_type not in ["text", "voice", "announcement"]:
        raise ValueError(
            f"Invalid channel_type: {channel_type}. "
            f"Must be one of: text, voice, announcement"
        )

    # Validate and resolve guild_id
    config = get_settings()
    target_guild_id = guild_id or config.discord_default_guild_id

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

    # Handle parent category
    parent_category = None
    if parent_id:
        if not str(parent_id).isdigit() or len(str(parent_id)) < 17:
            raise ValueError(f"Invalid parent_id format: {parent_id}")

        parent_category = guild.get_channel(int(parent_id))
        if not parent_category or parent_category.type != discord.ChannelType.category:
            raise ValueError(f"Category {parent_id} not found or not a category")

    # Create channel based on type
    try:
        if channel_type == "text":
            channel = await guild.create_text_channel(
                name=name,
                category=parent_category,
                topic=settings.get("topic"),
                slowmode_delay=settings.get("slowmode", 0),
                nsfw=settings.get("nsfw", False)
            )
            result_type = "text"

        elif channel_type == "voice":
            user_limit = settings.get("user_limit", 0)
            channel = await guild.create_voice_channel(
                name=name,
                category=parent_category,
                user_limit=user_limit,
                bitrate=settings.get("bitrate", 64000)
            )
            result_type = "voice"

        elif channel_type == "announcement":
            # Announcement channel is a text channel with news type
            channel = await guild.create_text_channel(
                name=name,
                category=parent_category,
                news=True
            )
            result_type = "announcement"

    except discord.Forbidden:
        raise PermissionError("Bot lacks Manage Channels permission")

    # Build response
    result = {
        "channel_id": str(channel.id),
        "name": channel.name,
        "type": result_type,
        "guild_id": target_guild_id
    }

    # Include type-specific fields
    if channel_type == "voice" and hasattr(channel, 'user_limit'):
        result["user_limit"] = channel.user_limit

    return result


async def delete_channel(channel_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
    """Delete a channel with safety checks.

    Test Contract (from test_channels.py):
    - Returns success: True, channel_id, message
    - Requires channel_id
    - Optional reason for audit log
    - Validates channel exists
    - Cannot delete category with children (safety check)
    - Raises ValueError if channel_id invalid, channel not found, or category has children
    - Raises PermissionError if bot lacks Manage Channels permission

    Args:
        channel_id: Discord channel ID (required)
        reason: Optional deletion reason for audit log

    Returns:
        Dict with success status and deletion confirmation

    Raises:
        ValueError: If channel_id invalid, not found, or category has children
        PermissionError: If bot lacks Manage Channels permission
    """
    # Validate channel_id
    if not channel_id:
        raise ValueError("channel_id is required")

    if not str(channel_id).isdigit() or len(str(channel_id)) < 17:
        raise ValueError(f"Invalid channel_id format: {channel_id}")

    # Fetch channel
    client = await get_client()

    try:
        channel = await client.fetch_channel(int(channel_id))
    except discord.NotFound:
        raise ValueError(f"Channel {channel_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access channel")

    # Safety check: prevent deleting category with children
    if channel.type == discord.ChannelType.category:
        # Check if category has child channels
        if hasattr(channel, 'channels') and channel.channels:
            raise ValueError(
                f"Cannot delete category with child channels. "
                f"Move or delete {len(channel.channels)} child channels first."
            )

    # Delete channel
    try:
        await channel.delete(reason=reason)
    except discord.Forbidden:
        raise PermissionError("Bot lacks Manage Channels permission")

    return {
        "success": True,
        "channel_id": str(channel_id),
        "message": f"Channel {channel_id} deleted successfully"
    }


async def create_category(
    guild_id: Optional[str] = None,
    name: str = None,
    position: Optional[int] = None
) -> Dict[str, Any]:
    """Create a category channel for organizing other channels.

    Test Contract (from test_channels.py):
    - Returns category_id, name, type, guild_id, (position if specified)
    - Requires name
    - Optional position for ordering
    - Validates parameters
    - Raises ValueError if name missing or guild not found
    - Raises PermissionError if bot lacks Manage Channels permission

    Args:
        guild_id: Discord guild ID (uses default if None)
        name: Category name (required)
        position: Optional position in channel list

    Returns:
        Dict with created category details

    Raises:
        ValueError: If name missing or guild not found
        PermissionError: If bot lacks Manage Channels permission
    """
    # Validate required parameters
    if not name:
        raise ValueError("Category name is required")

    # Validate and resolve guild_id
    config = get_settings()
    target_guild_id = guild_id or config.discord_default_guild_id

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

    # Create category
    try:
        kwargs = {"name": name}
        if position is not None:
            kwargs["position"] = position

        category = await guild.create_category(**kwargs)

    except discord.Forbidden:
        raise PermissionError("Bot lacks Manage Channels permission")

    # Build response
    result = {
        "category_id": str(category.id),
        "name": category.name,
        "type": "category",
        "guild_id": target_guild_id
    }

    # Include position if specified
    if position is not None:
        result["position"] = category.position

    return result
