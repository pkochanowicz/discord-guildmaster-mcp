"""Thread management tools for discord-guildmaster-mcp.

Provides thread creation and archiving operations following the test
specifications defined in tests/tools/test_threads.py.
"""

import discord
from typing import Dict, Any, Optional
from ..discord_client import get_client


async def create_thread(
    channel_id: str,
    name: str,
    message_id: Optional[str] = None,
    auto_archive_duration: Optional[int] = None
) -> Dict[str, Any]:
    """Create a thread from a message or in a channel.

    Test Contract (from test_threads.py):
    - Returns thread_id, name, channel_id, message_id (if from message), auto_archive_duration (if specified)
    - Requires channel_id and name
    - Name max 100 characters
    - Optional message_id to create thread from specific message
    - Optional auto_archive_duration (must be 60, 1440, 4320, or 10080 minutes)
    - Raises ValueError if channel_id/name invalid, message not found, or invalid auto_archive_duration
    - Raises PermissionError if bot lacks permissions

    Args:
        channel_id: Discord channel ID (required)
        name: Thread name (required, max 100 chars)
        message_id: Optional message ID to create thread from
        auto_archive_duration: Optional auto-archive duration in minutes (60, 1440, 4320, 10080)

    Returns:
        Dict with thread details

    Raises:
        ValueError: If channel_id/name invalid, message not found, or invalid auto_archive_duration
        PermissionError: If bot lacks permissions to create thread
    """
    # Validate required parameters
    if not name:
        raise ValueError("Thread name is required")

    if len(name) > 100:
        raise ValueError("Thread name cannot exceed 100 characters")

    # Validate channel_id format
    if not channel_id or not str(channel_id).isdigit() or len(str(channel_id)) < 17:
        raise ValueError(f"Invalid channel_id format: {channel_id}")

    # Validate message_id format if provided
    if message_id and (not str(message_id).isdigit() or len(str(message_id)) < 17):
        raise ValueError(f"Invalid message_id format: {message_id}")

    # Validate auto_archive_duration if provided
    if auto_archive_duration is not None:
        valid_durations = [60, 1440, 4320, 10080]
        if auto_archive_duration not in valid_durations:
            raise ValueError(f"Invalid auto_archive_duration: {auto_archive_duration}")

    # Fetch channel
    client = await get_client()

    try:
        channel = await client.fetch_channel(int(channel_id))
    except discord.NotFound:
        raise ValueError(f"Channel {channel_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access channel")

    # Create thread
    try:
        if message_id:
            # Create thread from specific message
            message = await channel.fetch_message(int(message_id))
            kwargs = {"name": name}
            if auto_archive_duration:
                kwargs["auto_archive_duration"] = auto_archive_duration

            thread = await message.create_thread(**kwargs)

            result = {
                "thread_id": str(thread.id),
                "name": thread.name,
                "channel_id": channel_id,
                "message_id": message_id
            }
        else:
            # Create standalone thread in channel
            kwargs = {"name": name}
            if auto_archive_duration:
                kwargs["auto_archive_duration"] = auto_archive_duration

            thread = await channel.create_thread(**kwargs)

            result = {
                "thread_id": str(thread.id),
                "name": thread.name,
                "channel_id": channel_id
            }

        # Include auto_archive_duration if specified
        if auto_archive_duration:
            result["auto_archive_duration"] = auto_archive_duration

    except discord.NotFound as e:
        if message_id:
            raise ValueError(f"Message {message_id} not found")
        else:
            raise ValueError(str(e))
    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to create thread")

    return result


async def archive_thread(thread_id: str) -> Dict[str, Any]:
    """Archive a thread (stop new messages).

    Test Contract (from test_threads.py):
    - Returns success: True, thread_id, message
    - Requires thread_id
    - Idempotent: no error if already archived
    - Locked threads can still be archived
    - Raises ValueError if thread_id invalid or thread not found
    - Raises PermissionError if bot lacks permissions

    Args:
        thread_id: Discord thread ID (required)

    Returns:
        Dict with success status and confirmation

    Raises:
        ValueError: If thread_id invalid or thread not found
        PermissionError: If bot lacks permissions to archive thread
    """
    # Validate thread_id format
    if not thread_id or not str(thread_id).isdigit() or len(str(thread_id)) < 17:
        raise ValueError(f"Invalid thread_id format: {thread_id}")

    # Fetch thread
    client = await get_client()

    try:
        thread = await client.fetch_channel(int(thread_id))
    except discord.NotFound:
        raise ValueError(f"Thread {thread_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access thread")

    # Check if already archived (idempotent behavior)
    if getattr(thread, 'archived', False):
        return {
            "success": True,
            "thread_id": thread_id,
            "message": f"Thread {thread_id} already archived"
        }

    # Archive thread
    try:
        await thread.edit(archived=True)
    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to archive thread")

    return {
        "success": True,
        "thread_id": thread_id,
        "message": f"Thread {thread_id} archived successfully"
    }
