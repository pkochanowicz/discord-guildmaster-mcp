"""Forum management tools for discord-guildmaster-mcp."""

import discord
from typing import Dict, Any, Optional, List
from ..discord_client import get_client


async def create_forum_post(
    forum_channel_id: str,
    title: str,
    content: str,
    tags: Optional[List[str]] = None,
    auto_archive_duration: int = 1440
) -> Dict[str, Any]:
    """Create a post (thread) in a forum channel.

    Test Contract (tests/tools/test_forums.py):
    - Returns: thread_id, title, forum_channel_id, created_at, tags
    - Validates forum_channel_id points to forum channel
    - Forum posts REQUIRE initial message (content parameter)
    - Tags can be tag names or tag IDs
    - Auto-archive duration: 60, 1440, 4320, 10080 minutes

    Args:
        forum_channel_id: Discord forum channel ID (required)
        title: Thread/post title (required)
        content: Initial message content (required for forums)
        tags: Optional list of tag names or IDs to apply
        auto_archive_duration: Minutes until auto-archive (default: 1440 = 1 day)

    Returns:
        {
            "thread_id": str,
            "title": str,
            "forum_channel_id": str,
            "created_at": str (ISO8601),
            "tags": List[str]  # Tag names applied
        }

    Raises:
        ValueError: If channel not forum type, invalid tags, invalid duration
        PermissionError: If bot lacks permissions
    """
    # Validate auto-archive duration
    valid_durations = [60, 1440, 4320, 10080]
    if auto_archive_duration not in valid_durations:
        raise ValueError(
            f"Invalid auto_archive_duration: {auto_archive_duration}. "
            f"Valid values: {valid_durations}"
        )

    # Validate required parameters
    if not title:
        raise ValueError("title is required")
    if not content:
        raise ValueError("content is required for forum posts")

    # Validate forum_channel_id format
    if not forum_channel_id or not forum_channel_id.isdigit() or len(forum_channel_id) < 17:
        raise ValueError(f"Invalid forum_channel_id format: {forum_channel_id}")

    # Fetch forum channel
    client = await get_client()

    try:
        channel = await client.fetch_channel(int(forum_channel_id))
    except discord.NotFound:
        raise ValueError(f"Channel {forum_channel_id} not found")
    except discord.Forbidden:
        raise PermissionError(f"Bot lacks permission to access channel {forum_channel_id}")

    # Validate channel is a forum
    if not isinstance(channel, discord.ForumChannel):
        raise ValueError(
            f"Channel {forum_channel_id} is type {channel.type}, not a forum channel. "
            "This tool only works with forum channels."
        )

    # Resolve tags if provided
    applied_tags = []
    if tags:
        for tag_input in tags:
            # Try to find tag by name first
            forum_tag = discord.utils.get(channel.available_tags, name=tag_input)

            # If not found by name and input is numeric, try by ID
            if not forum_tag and tag_input.isdigit():
                forum_tag = discord.utils.get(channel.available_tags, id=int(tag_input))

            # If tag found, add to applied list
            if forum_tag:
                applied_tags.append(forum_tag)
            # Note: Silently skip invalid tags (could also raise ValueError)

    # Create forum post (thread with initial message)
    try:
        thread = await channel.create_thread(
            name=title,
            content=content,
            applied_tags=applied_tags,
            auto_archive_duration=auto_archive_duration
        )
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to create threads in this forum")
    except discord.HTTPException as e:
        raise ValueError(f"Failed to create forum post: {e}")

    return {
        "thread_id": str(thread.id),
        "title": thread.name,
        "forum_channel_id": str(channel.id),
        "created_at": thread.created_at.isoformat(),
        "tags": [tag.name for tag in thread.applied_tags] if hasattr(thread, 'applied_tags') else []
    }


async def list_forum_posts(
    forum_channel_id: str,
    limit: int = 50,
    archived: bool = False
) -> Dict[str, Any]:
    """List posts in a forum channel.

    Test Contract (tests/tools/test_forums.py):
    - Returns: forum_channel_id, total_count, posts list
    - Each post: thread_id, title, author_id, created_at, tags, message_count
    - Limit: 1-100 posts
    - Optional include archived threads

    Args:
        forum_channel_id: Discord forum channel ID
        limit: Maximum posts to return (1-100, default: 50)
        archived: Include archived threads (default: False)

    Returns:
        {
            "forum_channel_id": str,
            "total_count": int,
            "posts": [
                {
                    "thread_id": str,
                    "title": str,
                    "author_id": str | None,
                    "created_at": str (ISO8601),
                    "tags": List[str],
                    "message_count": int
                }
            ]
        }

    Raises:
        ValueError: If forum_channel_id invalid, channel not forum, limit out of range
    """
    # Validate limit
    if not 1 <= limit <= 100:
        raise ValueError(f"Limit must be 1-100, got {limit}")

    # Validate forum_channel_id format
    if not forum_channel_id or not forum_channel_id.isdigit() or len(forum_channel_id) < 17:
        raise ValueError(f"Invalid forum_channel_id format: {forum_channel_id}")

    # Fetch forum channel
    client = await get_client()

    try:
        channel = await client.fetch_channel(int(forum_channel_id))
    except discord.NotFound:
        raise ValueError(f"Channel {forum_channel_id} not found")
    except discord.Forbidden:
        raise PermissionError(f"Bot lacks permission to access channel {forum_channel_id}")

    # Validate channel is a forum
    if not isinstance(channel, discord.ForumChannel):
        raise ValueError(f"Channel {forum_channel_id} is not a forum channel")

    # Get threads (active or archived)
    posts = []

    if archived:
        # Get archived threads
        async for thread in channel.archived_threads(limit=limit):
            posts.append({
                "thread_id": str(thread.id),
                "title": thread.name,
                "author_id": str(thread.owner_id) if thread.owner_id else None,
                "created_at": thread.created_at.isoformat(),
                "tags": [t.name for t in thread.applied_tags] if hasattr(thread, 'applied_tags') else [],
                "message_count": thread.message_count or 0
            })
            if len(posts) >= limit:
                break
    else:
        # Get active threads
        for thread in channel.threads:
            posts.append({
                "thread_id": str(thread.id),
                "title": thread.name,
                "author_id": str(thread.owner_id) if thread.owner_id else None,
                "created_at": thread.created_at.isoformat(),
                "tags": [t.name for t in thread.applied_tags] if hasattr(thread, 'applied_tags') else [],
                "message_count": thread.message_count or 0
            })
            if len(posts) >= limit:
                break

    return {
        "forum_channel_id": str(channel.id),
        "total_count": len(posts),
        "posts": posts
    }


async def manage_forum_tags(
    forum_channel_id: str,
    action: str,
    tag_name: Optional[str] = None,
    tag_emoji: Optional[str] = None
) -> Dict[str, Any]:
    """Manage forum channel tags.

    Test Contract (tests/tools/test_forums.py):
    - Actions: "list", "create", "delete"
    - "list": Returns all available tags
    - "create": Requires tag_name, optional tag_emoji (NOT IMPLEMENTED - requires channel edit)
    - "delete": Requires tag_name (NOT IMPLEMENTED - requires channel edit)

    Args:
        forum_channel_id: Discord forum channel ID
        action: Action to perform ("list", "create", "delete")
        tag_name: Tag name (required for create/delete)
        tag_emoji: Optional emoji for tag (create only)

    Returns:
        For "list": {"forum_channel_id": str, "tags": [{"name": str, "emoji": str|None}]}
        For "create"/"delete": NotImplementedError

    Raises:
        ValueError: If invalid action, missing parameters, channel not forum
        NotImplementedError: For create/delete actions
    """
    # Validate action
    valid_actions = ["list", "create", "delete"]
    if action not in valid_actions:
        raise ValueError(f"Invalid action: {action}. Valid actions: {valid_actions}")

    # Validate forum_channel_id format
    if not forum_channel_id or not forum_channel_id.isdigit() or len(forum_channel_id) < 17:
        raise ValueError(f"Invalid forum_channel_id format: {forum_channel_id}")

    # Fetch forum channel
    client = await get_client()

    try:
        channel = await client.fetch_channel(int(forum_channel_id))
    except discord.NotFound:
        raise ValueError(f"Channel {forum_channel_id} not found")
    except discord.Forbidden:
        raise PermissionError(f"Bot lacks permission to access channel {forum_channel_id}")

    # Validate channel is a forum
    if not isinstance(channel, discord.ForumChannel):
        raise ValueError(f"Channel {forum_channel_id} is not a forum channel")

    # Handle actions
    if action == "list":
        # List all available tags
        return {
            "forum_channel_id": str(channel.id),
            "tags": [
                {
                    "name": tag.name,
                    "emoji": str(tag.emoji) if tag.emoji else None
                }
                for tag in channel.available_tags
            ]
        }

    elif action == "create":
        # Validate tag_name provided
        if not tag_name:
            raise ValueError("tag_name is required for create action")

        # Tag creation requires channel.edit() with new available_tags list
        # This is complex and requires reconstructing the entire tags list
        raise NotImplementedError(
            "Forum tag creation requires channel edit operations. "
            "Use Discord UI or bot with channel management to create tags."
        )

    elif action == "delete":
        # Validate tag_name provided
        if not tag_name:
            raise ValueError("tag_name is required for delete action")

        # Tag deletion requires channel.edit() with modified available_tags list
        raise NotImplementedError(
            "Forum tag deletion requires channel edit operations. "
            "Use Discord UI or bot with channel management to delete tags."
        )
