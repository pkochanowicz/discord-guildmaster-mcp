"""Thread management tools for discord-guildmaster-mcp."""

import discord
from typing import Dict, Any, Optional
from ..discord_client import get_client


async def create_thread(
    channel_id: str,
    name: str,
    message_id: Optional[str] = None,
    thread_type: str = "public",
    auto_archive_duration: int = 1440
) -> Dict[str, Any]:
    """Create a thread in a channel.

    Test Contract (tests/tools/test_threads.py):
    - Returns: thread_id, name, parent_channel_id, created_at, type
    - Can create from message (message_id) or standalone
    - Thread types: "public", "private", "news"
    - Auto-archive duration: 60, 1440, 4320, 10080 minutes
    - Validates channel supports threads

    Args:
        channel_id: Parent channel ID (required)
        name: Thread name (required)
        message_id: Optional message ID to create thread from
        thread_type: Thread type - "public", "private", or "news" (default: "public")
        auto_archive_duration: Minutes until auto-archive (default: 1440 = 1 day)

    Returns:
        {
            "thread_id": str,
            "name": str,
            "parent_channel_id": str,
            "created_at": str (ISO8601),
            "type": str
        }

    Raises:
        ValueError: If channel doesn't support threads, invalid type/duration
        PermissionError: If bot lacks permissions
    """
    # Thread type mapping
    THREAD_TYPE_MAP = {
        "public": discord.ChannelType.public_thread,
        "private": discord.ChannelType.private_thread,
        "news": discord.ChannelType.news_thread
    }

    # Validate thread type
    if thread_type not in THREAD_TYPE_MAP:
        raise ValueError(
            f"Invalid thread_type: {thread_type}. "
            f"Valid types: {list(THREAD_TYPE_MAP.keys())}"
        )

    # Validate auto-archive duration
    valid_durations = [60, 1440, 4320, 10080]
    if auto_archive_duration not in valid_durations:
        raise ValueError(
            f"Invalid auto_archive_duration: {auto_archive_duration}. "
            f"Valid values: {valid_durations}"
        )

    # Validate required parameters
    if not name:
        raise ValueError("name is required")

    # Validate channel_id format
    if not channel_id or not channel_id.isdigit() or len(channel_id) < 17:
        raise ValueError(f"Invalid channel_id format: {channel_id}")

    # Fetch channel
    client = await get_client()

    try:
        channel = await client.fetch_channel(int(channel_id))
    except discord.NotFound:
        raise ValueError(f"Channel {channel_id} not found")
    except discord.Forbidden:
        raise PermissionError(f"Bot lacks permission to access channel {channel_id}")

    # Create thread (from message or standalone)
    try:
        if message_id:
            # Create thread from specific message
            if not message_id.isdigit() or len(message_id) < 17:
                raise ValueError(f"Invalid message_id format: {message_id}")

            message = await channel.fetch_message(int(message_id))
            thread = await message.create_thread(
                name=name,
                auto_archive_duration=auto_archive_duration
            )
        else:
            # Create standalone thread
            thread = await channel.create_thread(
                name=name,
                type=THREAD_TYPE_MAP[thread_type],
                auto_archive_duration=auto_archive_duration
            )
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to create threads in this channel")
    except discord.HTTPException as e:
        raise ValueError(f"Failed to create thread: {e}")

    return {
        "thread_id": str(thread.id),
        "name": thread.name,
        "parent_channel_id": str(channel.id),
        "created_at": thread.created_at.isoformat(),
        "type": thread_type
    }


async def manage_thread(
    thread_id: str,
    action: str,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """Manage thread lifecycle.

    Test Contract (tests/tools/test_threads.py):
    - Actions: "archive", "unarchive", "lock", "unlock", "delete"
    - Returns: success: True, thread_id, action
    - Optional reason for audit log
    - Validates thread exists

    Args:
        thread_id: Discord thread ID (required)
        action: Action to perform (required)
        reason: Optional reason for audit log

    Returns:
        {
            "success": True,
            "thread_id": str,
            "action": str
        }

    Raises:
        ValueError: If invalid action, thread_id invalid, thread not found
        PermissionError: If bot lacks permissions
    """
    # Validate action
    valid_actions = ["archive", "unarchive", "lock", "unlock", "delete"]
    if action not in valid_actions:
        raise ValueError(
            f"Invalid action: {action}. "
            f"Valid actions: {valid_actions}"
        )

    # Validate thread_id format
    if not thread_id or not thread_id.isdigit() or len(thread_id) < 17:
        raise ValueError(f"Invalid thread_id format: {thread_id}")

    # Fetch thread
    client = await get_client()

    try:
        thread = await client.fetch_channel(int(thread_id))
    except discord.NotFound:
        raise ValueError(f"Thread {thread_id} not found")
    except discord.Forbidden:
        raise PermissionError(f"Bot lacks permission to access thread {thread_id}")

    # Validate it's actually a thread
    if not isinstance(thread, discord.Thread):
        raise ValueError(
            f"Channel {thread_id} is type {thread.type}, not a thread. "
            "This tool only works with threads."
        )

    # Perform action
    try:
        if action == "archive":
            await thread.edit(archived=True, reason=reason)
        elif action == "unarchive":
            await thread.edit(archived=False, reason=reason)
        elif action == "lock":
            await thread.edit(locked=True, reason=reason)
        elif action == "unlock":
            await thread.edit(locked=False, reason=reason)
        elif action == "delete":
            await thread.delete()
    except discord.Forbidden:
        raise PermissionError(f"Bot lacks permission to {action} thread")
    except discord.HTTPException as e:
        raise ValueError(f"Failed to {action} thread: {e}")

    return {
        "success": True,
        "thread_id": thread_id,
        "action": action
    }
