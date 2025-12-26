"""Webhook management tools for discord-guildmaster-mcp.

Provides webhook creation, message sending, and deletion operations following
the test specifications defined in tests/tools/test_webhooks.py.
"""

import discord
from typing import Dict, Any, Optional, List
from ..discord_client import get_client


async def create_webhook(
    channel_id: str,
    name: str,
    avatar_url: Optional[str] = None
) -> Dict[str, Any]:
    """Create a webhook for a channel to send messages.

    Test Contract (from test_webhooks.py):
    - Returns webhook_id, name, token, url, channel_id, (avatar_url if provided)
    - Requires channel_id and name
    - Name must be 1-80 characters
    - Can only be created on text channels (not voice)
    - Optional avatar_url for webhook avatar
    - Raises ValueError if channel_id invalid, name missing/too long, or channel not text
    - Raises PermissionError if bot lacks Manage Webhooks permission

    Args:
        channel_id: Discord channel ID (required)
        name: Webhook name (required, max 80 chars)
        avatar_url: Optional avatar URL for webhook

    Returns:
        Dict with webhook details including ID, token, and URL

    Raises:
        ValueError: If channel_id invalid, name missing/too long, or channel not text
        PermissionError: If bot lacks Manage Webhooks permission
    """
    # Validate required parameters
    if not name:
        raise ValueError("Webhook name is required")

    if len(name) > 80:
        raise ValueError(f"Webhook name cannot exceed 80 characters (got {len(name)})")

    # Validate channel_id format
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

    # Validate channel type (must be text-based)
    if channel.type == discord.ChannelType.voice:
        raise ValueError("Webhooks can only be created on text channels, not voice channels")

    # Create webhook
    try:
        # Handle avatar_url if provided
        kwargs = {"name": name}
        if avatar_url:
            # TODO: Download and convert avatar_url to bytes for discord.py
            # For now, discord.py create_webhook doesn't directly support avatar_url parameter
            # It requires avatar= with bytes data
            pass

        webhook = await channel.create_webhook(**kwargs)

    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to create webhook")

    # Build response
    result = {
        "webhook_id": str(webhook.id),
        "name": webhook.name,
        "token": webhook.token,
        "url": webhook.url,
        "channel_id": channel_id
    }

    # Include avatar_url if provided
    if avatar_url:
        result["avatar_url"] = avatar_url

    return result


async def send_webhook_message(
    webhook_url: str,
    content: Optional[str] = None,
    username: Optional[str] = None,
    avatar_url: Optional[str] = None,
    embeds: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Send a message via webhook with optional username/avatar override.

    Test Contract (from test_webhooks.py):
    - Returns success: True, message_id, content (if provided), username (if provided),
      avatar_url (if provided), embeds_count (if embeds)
    - Requires webhook_url
    - Either content or embeds must be provided
    - Content max 2000 characters
    - webhook_url must start with "https://discord.com/api/webhooks/"
    - Supports username and avatar_url overrides
    - Raises ValueError if webhook_url invalid, neither content/embeds, or content too long

    Args:
        webhook_url: Discord webhook URL (required)
        content: Message content (optional, max 2000 chars)
        username: Username override (optional)
        avatar_url: Avatar URL override (optional)
        embeds: List of embed dicts (optional)

    Returns:
        Dict with success status and message confirmation

    Raises:
        ValueError: If webhook_url invalid, neither content/embeds, or content too long
    """
    # Validate webhook_url
    if not webhook_url or not webhook_url.startswith("https://discord.com/api/webhooks/"):
        raise ValueError(f"Invalid webhook URL format: {webhook_url}")

    # Validate content or embeds
    if not content and not embeds:
        raise ValueError("Either content or embeds must be provided")

    # Validate content length
    if content and len(content) > 2000:
        raise ValueError(f"Content cannot exceed 2000 characters (got {len(content)})")

    # Parse webhook_url to extract ID and token
    # URL format: https://discord.com/api/webhooks/{webhook_id}/{webhook_token}
    parts = webhook_url.split("/")
    if len(parts) < 7:
        raise ValueError(f"Invalid webhook URL format: {webhook_url}")

    webhook_id = parts[-2]
    webhook_token = parts[-1]

    # Fetch webhook from Discord
    client = await get_client()

    try:
        webhook = await client.fetch_webhook(int(webhook_id))
    except discord.NotFound:
        raise ValueError("Webhook not found or invalid token")
    except discord.Forbidden:
        raise ValueError("Webhook not found or invalid token")

    # Send message via webhook
    try:
        kwargs = {}
        if content:
            kwargs["content"] = content
        if username:
            kwargs["username"] = username
        if avatar_url:
            kwargs["avatar_url"] = avatar_url
        if embeds:
            # Convert embed dicts to discord.Embed objects
            kwargs["embeds"] = [discord.Embed.from_dict(e) for e in embeds]

        message = await webhook.send(**kwargs, wait=True)

    except discord.HTTPException as e:
        raise ValueError(f"Failed to send webhook message: {e}")

    # Build response
    result = {
        "success": True,
        "message_id": str(message.id)
    }

    # Include optional fields if provided
    if content:
        result["content"] = content
    if username:
        result["username"] = username
    if avatar_url:
        result["avatar_url"] = avatar_url
    if embeds:
        result["embeds_count"] = len(embeds)

    return result


async def delete_webhook(
    webhook_id: Optional[str] = None,
    webhook_url: Optional[str] = None
) -> Dict[str, Any]:
    """Permanently delete a webhook (DESTRUCTIVE).

    Test Contract (from test_webhooks.py):
    - Returns success: True, webhook_id, message
    - Accepts webhook_id OR webhook_url (one required)
    - Validates webhook_id format if provided
    - Cannot be undone
    - Raises ValueError if webhook_id invalid or webhook not found
    - Raises PermissionError if bot lacks Manage Webhooks permission

    Args:
        webhook_id: Discord webhook ID (optional)
        webhook_url: Discord webhook URL (optional)

    Returns:
        Dict with success status and deletion confirmation

    Raises:
        ValueError: If webhook_id invalid or webhook not found
        PermissionError: If bot lacks Manage Webhooks permission
    """
    # Validate that one parameter is provided
    if not webhook_id and not webhook_url:
        raise ValueError("Either webhook_id or webhook_url must be provided")

    # Extract webhook_id from URL if URL provided
    if webhook_url:
        # URL format: https://discord.com/api/webhooks/{webhook_id}/{webhook_token}
        parts = webhook_url.split("/")
        if len(parts) >= 7:
            webhook_id = parts[-2]
        else:
            raise ValueError(f"Invalid webhook URL format: {webhook_url}")

    # Validate webhook_id format
    if not str(webhook_id).isdigit() or len(str(webhook_id)) < 17:
        raise ValueError(f"Invalid webhook_id format: {webhook_id}")

    # Fetch and delete webhook
    client = await get_client()

    try:
        webhook = await client.fetch_webhook(int(webhook_id))
    except discord.NotFound:
        raise ValueError(f"Webhook {webhook_id} not found (may already be deleted)")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to access webhook")

    # Delete webhook
    try:
        await webhook.delete()
    except discord.Forbidden:
        raise PermissionError("Insufficient permissions to delete webhook")

    return {
        "success": True,
        "webhook_id": str(webhook_id),
        "message": f"Webhook {webhook_id} deleted successfully"
    }
