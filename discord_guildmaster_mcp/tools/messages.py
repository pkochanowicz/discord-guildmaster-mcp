"""Message management tools for discord-guildmaster-mcp.

Provides message sending, reading, and deletion operations following
the test specifications defined in tests/tools/test_messages.py.
"""

import discord
from typing import Dict, Any, Optional, List
from ..discord_client import get_client
from ..config import get_settings


async def send_message(
    channel_id: Optional[str] = None,
    content: Optional[str] = None,
    embed: Optional[Dict[str, Any]] = None,
    tts: bool = False
) -> Dict[str, Any]:
    """Send a message to a Discord channel.

    Test Contract (from test_messages.py):
    - Returns: message_id, channel_id, timestamp, content
    - Either content or embed must be provided
    - Content max 2000 characters
    - Optional channel_id (uses default if not provided)
    - Optional embed dict
    - Optional TTS (text-to-speech)
    - Raises ValueError if neither content/embed, content too long, or channel not found
    - Raises PermissionError if bot lacks Send Messages permission

    Args:
        channel_id: Discord channel ID (optional if default set)
        content: Message text content (optional, max 2000 chars)
        embed: Embed dict (optional)
        tts: Text-to-speech flag (optional)

    Returns:
        Dict with message details

    Raises:
        ValueError: If neither content/embed, content too long, or channel not found
        PermissionError: If bot lacks Send Messages permission
    """
    # Resolve channel_id
    if not channel_id:
        settings = get_settings()
        channel_id = settings.discord_default_channel_id
        if not channel_id:
            raise ValueError("channel_id is required (no default configured)")

    # Validate content or embed provided
    if not content and not embed:
        raise ValueError("Either content or embed must be provided")

    # Validate content length
    if content and len(content) > 2000:
        raise ValueError(f"Content cannot exceed 2000 characters (got {len(content)})")

    # Validate channel_id format
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

    # Send message
    try:
        kwargs = {}
        if content:
            kwargs["content"] = content
        if embed:
            kwargs["embed"] = discord.Embed.from_dict(embed)
        if tts:
            kwargs["tts"] = tts

        message = await channel.send(**kwargs)

    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to send message")

    # Build response
    return {
        "message_id": str(message.id),
        "channel_id": str(message.channel.id),
        "timestamp": message.created_at.isoformat(),
        "content": message.content
    }


async def read_messages(
    channel_id: Optional[str] = None,
    limit: int = 50,
    before: Optional[str] = None,
    after: Optional[str] = None
) -> Dict[str, Any]:
    """Read message history from a channel.

    Test Contract (from test_messages.py):
    - Returns: channel_id, messages list, total_fetched, has_more
    - Each message: message_id, content, author_id, timestamp, attachments
    - Default limit 50, max 100
    - Optional before/after message IDs for pagination
    - Validates channel exists
    - Raises ValueError if invalid limit, channel not found
    - Raises PermissionError if bot lacks Read Message History permission

    Args:
        channel_id: Discord channel ID (optional if default set)
        limit: Number of messages to fetch (1-100)
        before: Message ID to fetch messages before
        after: Message ID to fetch messages after

    Returns:
        Dict with message list

    Raises:
        ValueError: If invalid limit or channel not found
        PermissionError: If bot lacks Read Message History permission
    """
    # Resolve channel_id
    if not channel_id:
        settings = get_settings()
        channel_id = settings.discord_default_channel_id
        if not channel_id:
            raise ValueError("channel_id is required (no default configured)")

    # Validate limit
    if not 1 <= limit <= 100:
        raise ValueError(f"Limit must be 1-100 (got {limit})")

    # Validate channel_id format
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

    # Build history kwargs
    kwargs = {"limit": limit}
    if before:
        kwargs["before"] = discord.Object(id=int(before))
    if after:
        kwargs["after"] = discord.Object(id=int(after))

    # Fetch messages
    try:
        messages = []
        async for msg in channel.history(**kwargs):
            messages.append({
                "message_id": str(msg.id),
                "content": msg.content,
                "author_id": str(msg.author.id),
                "timestamp": msg.created_at.isoformat(),
                "attachments": [
                    {
                        "url": att.url,
                        "filename": att.filename
                    }
                    for att in msg.attachments
                ]
            })

    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to read message history")

    return {
        "channel_id": str(channel.id),
        "messages": messages,
        "total_fetched": len(messages),
        "has_more": len(messages) == limit
    }


async def delete_message(
    channel_id: str,
    message_id: str,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """Delete a message from a channel.

    Test Contract (from test_messages.py):
    - Returns: success: True, message_id, channel_id
    - Requires channel_id and message_id
    - Optional reason for audit log
    - Validates message exists
    - Raises ValueError if message not found
    - Raises PermissionError if bot lacks Manage Messages permission

    Args:
        channel_id: Discord channel ID (required)
        message_id: Discord message ID (required)
        reason: Optional audit log reason

    Returns:
        Dict with deletion confirmation

    Raises:
        ValueError: If message not found
        PermissionError: If bot lacks Manage Messages permission
    """
    # Validate required parameters
    if not channel_id:
        raise ValueError("channel_id is required")
    if not message_id:
        raise ValueError("message_id is required")

    # Validate ID formats
    if not str(channel_id).isdigit() or len(str(channel_id)) < 17:
        raise ValueError(f"Invalid channel_id format: {channel_id}")
    if not str(message_id).isdigit() or len(str(message_id)) < 17:
        raise ValueError(f"Invalid message_id format: {message_id}")

    # Fetch channel and message
    client = await get_client()

    try:
        channel = await client.fetch_channel(int(channel_id))
    except discord.NotFound:
        raise ValueError(f"Channel {channel_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access channel")

    try:
        message = await channel.fetch_message(int(message_id))
    except discord.NotFound:
        raise ValueError(f"Message {message_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access message")

    # Delete message
    try:
        await message.delete()
    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to delete message")

    return {
        "success": True,
        "message_id": message_id,
        "channel_id": channel_id
    }


async def send_dm(
    user_id: str,
    content: str
) -> Dict[str, Any]:
    """Send a direct message to a user.

    Test Contract (from test_messages.py):
    - Returns: success: True, message_id, user_id
    - Requires user_id and content
    - Content max 2000 characters
    - Creates DM channel if needed
    - Raises ValueError if user not found, content too long
    - May fail if user has DMs disabled

    Args:
        user_id: Discord user ID (required)
        content: Message content (required, max 2000 chars)

    Returns:
        Dict with DM confirmation

    Raises:
        ValueError: If user not found or content too long
    """
    # Validate required parameters
    if not user_id:
        raise ValueError("user_id is required")
    if not content:
        raise ValueError("content is required")

    # Validate content length
    if len(content) > 2000:
        raise ValueError(f"Content cannot exceed 2000 characters (got {len(content)})")

    # Validate user_id format
    if not str(user_id).isdigit() or len(str(user_id)) < 17:
        raise ValueError(f"Invalid user_id format: {user_id}")

    # Fetch user
    client = await get_client()

    try:
        user = await client.fetch_user(int(user_id))
    except discord.NotFound:
        raise ValueError(f"User {user_id} not found")

    # Send DM
    try:
        message = await user.send(content)
    except discord.Forbidden:
        raise ValueError("User has DMs disabled or bot is blocked")

    return {
        "success": True,
        "message_id": str(message.id),
        "user_id": user_id
    }
