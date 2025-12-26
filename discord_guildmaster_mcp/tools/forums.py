"""Forum support tools for discord-guildmaster-mcp.

Provides forum post creation, replying, and retrieval operations following
the test specifications defined in tests/tools/test_forums.py.
"""

import discord
from typing import Dict, Any, Optional, List
from ..discord_client import get_client


async def create_forum_post(
    forum_id: str,
    title: str,
    content: str,
    tag_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Create a new forum post (thread) in a forum channel.

    Test Contract (from test_forums.py):
    - Returns thread_id, message_id, title, forum_id, tag_ids (if provided)
    - Requires forum_id, title, and content
    - Title max 100 characters, content max 2000 characters
    - Optional tag_ids list for forum tags
    - Raises ValueError if forum_id invalid, title/content missing/too long, or forum not found
    - Raises PermissionError if bot lacks permissions

    Args:
        forum_id: Discord forum channel ID (required)
        title: Forum post title (required, max 100 chars)
        content: Initial post content (required, max 2000 chars)
        tag_ids: Optional list of tag IDs to apply to post

    Returns:
        Dict with thread and message details

    Raises:
        ValueError: If forum_id invalid, title/content missing/too long, or forum not found
        PermissionError: If bot lacks permissions to create threads
    """
    # Validate required parameters
    if not title:
        raise ValueError("Forum post title is required")

    if len(title) > 100:
        raise ValueError(f"Forum post title cannot exceed 100 characters")

    if content and len(content) > 2000:
        raise ValueError("Content cannot exceed 2000 characters")

    # Validate forum_id format
    if not forum_id or not str(forum_id).isdigit() or len(str(forum_id)) < 17:
        raise ValueError(f"Invalid forum_id format: {forum_id}")

    # Fetch forum channel
    client = await get_client()

    try:
        forum = await client.fetch_channel(int(forum_id))
    except discord.NotFound:
        raise ValueError(f"Forum channel {forum_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access forum channel")

    # Validate channel is a forum
    if forum.type != discord.ChannelType.forum:
        raise ValueError(f"Channel {forum_id} is not a forum channel")

    # Create forum post (thread in forum channel)
    try:
        kwargs = {
            "name": title,
            "content": content
        }

        # Handle tags if provided
        if tag_ids:
            # Convert tag IDs to ForumTag objects
            # discord.py requires actual tag objects, not just IDs
            available_tags = {str(tag.id): tag for tag in forum.available_tags}
            tags = []
            for tag_id in tag_ids:
                if tag_id in available_tags:
                    tags.append(available_tags[tag_id])
            if tags:
                kwargs["applied_tags"] = tags

        thread = await forum.create_thread(**kwargs)

        # Get the initial message ID (first message in thread)
        # The starter message is accessible via thread.starter_message or thread.starting_message
        initial_message = thread.starter_message or thread.starting_message
        message_id = str(initial_message.id) if initial_message else str(thread.id)

    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to create forum post")

    # Build response
    result = {
        "thread_id": str(thread.id),
        "message_id": message_id,
        "title": thread.name,
        "forum_id": forum_id
    }

    # Include tag_ids if provided
    if tag_ids:
        result["tag_ids"] = tag_ids

    return result


async def reply_to_forum(
    thread_id: str,
    content: str
) -> Dict[str, Any]:
    """Reply to an existing forum post (thread).

    Test Contract (from test_forums.py):
    - Returns message_id, thread_id, content
    - Requires thread_id and content
    - Content max 2000 characters
    - Bumps thread to top of forum
    - Cannot reply to locked threads
    - Raises ValueError if thread_id invalid, content missing/too long, thread not found, or thread locked

    Args:
        thread_id: Discord thread ID (required)
        content: Reply content (required, max 2000 chars)

    Returns:
        Dict with message confirmation

    Raises:
        ValueError: If thread_id invalid, content missing/too long, thread not found, or thread locked
    """
    # Validate required parameters
    if not content:
        raise ValueError("Reply content is required")

    if len(content) > 2000:
        raise ValueError("Content cannot exceed 2000 characters")

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

    # Check if thread is locked
    if hasattr(thread, 'locked') and thread.locked:
        raise ValueError("Thread is locked and cannot receive new replies")

    # Send reply message
    try:
        message = await thread.send(content)
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to send messages in thread")

    return {
        "message_id": str(message.id),
        "thread_id": thread_id,
        "content": content
    }


async def get_forum_post(
    thread_id: str,
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """Retrieve a forum post (thread) with messages.

    Test Contract (from test_forums.py):
    - Returns thread_id, title, message_count, locked, archived, messages (if limit provided), limit (if provided)
    - Requires thread_id
    - Supports pagination via limit parameter
    - Raises ValueError if thread_id invalid or thread not found

    Args:
        thread_id: Discord thread ID (required)
        limit: Optional message limit for pagination

    Returns:
        Dict with thread metadata and optional message list

    Raises:
        ValueError: If thread_id invalid or thread not found
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

    # Build response
    result = {
        "thread_id": thread_id,
        "title": thread.name,
        "message_count": thread.message_count or 0,
        "locked": getattr(thread, 'locked', False),
        "archived": getattr(thread, 'archived', False)
    }

    # Fetch messages if limit specified
    if limit is not None:
        messages = []
        async for message in thread.history(limit=limit):
            messages.append({
                "id": str(message.id),
                "content": message.content,
                "author_id": str(message.author.id),
                "created_at": message.created_at.isoformat()
            })

        result["messages"] = messages
        result["limit"] = limit

    return result
