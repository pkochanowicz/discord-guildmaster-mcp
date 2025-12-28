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
    avatar_url: Optional[str] = None,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """Create a webhook for a channel to send messages.

    Test Contract (from test_webhooks.py):
    - Returns webhook_id, name, token, url, channel_id, avatar_url
    - Requires channel_id and name
    - Name must be 1-80 characters
    - Can only be created on text channels (not voice)
    - Optional avatar_url for webhook avatar (downloads and validates HTTP/HTTPS URL)
    - Optional reason for audit log
    - Raises ValueError if channel_id invalid, name missing/too long, or channel not text
    - Raises PermissionError if bot lacks Manage Webhooks permission

    Args:
        channel_id: Discord channel ID (required)
        name: Webhook name (required, 1-80 chars)
        avatar_url: Optional avatar URL for webhook
        reason: Optional reason for audit log

    Returns:
        Dict with webhook details including ID, token, and URL

    Raises:
        ValueError: If channel_id invalid, name missing/too long, or channel not text
        PermissionError: If bot lacks Manage Webhooks permission
    """
    # Validate name length
    if not name or not (1 <= len(name) <= 80):
        raise ValueError(f"Webhook name must be 1-80 characters, got {len(name) if name else 0}")

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

    # Validate channel type (only text/news channels support webhooks)
    if not isinstance(channel, (discord.TextChannel, discord.NewsChannel)):
        raise ValueError(
            f"Channel {channel_id} type {channel.type} does not support webhooks. "
            "Only text and news channels support webhooks."
        )

    # Handle avatar if provided
    avatar_bytes = None
    if avatar_url:
        # Validate URL format
        if not avatar_url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid avatar URL format: {avatar_url}")

        # Download avatar
        import httpx
        try:
            async with httpx.AsyncClient(timeout=30.0) as http_client:
                response = await http_client.get(avatar_url)
                response.raise_for_status()
                avatar_bytes = response.content
        except httpx.HTTPError as e:
            raise ValueError(f"Failed to download avatar from {avatar_url}: {e}")

    # Create webhook
    try:
        webhook = await channel.create_webhook(
            name=name,
            avatar=avatar_bytes,
            reason=reason
        )
    except discord.Forbidden:
        raise PermissionError("Bot lacks Manage Webhooks permission")
    except discord.HTTPException as e:
        raise ValueError(f"Failed to create webhook: {e}")

    return {
        "webhook_id": str(webhook.id),
        "name": webhook.name,
        "channel_id": str(webhook.channel_id),
        "token": webhook.token,
        "url": webhook.url,
        "avatar_url": str(webhook.avatar.url) if webhook.avatar else None
    }


async def send_webhook_message(
    webhook_url: str,
    content: str,
    username: Optional[str] = None,
    avatar_url: Optional[str] = None
) -> Dict[str, Any]:
    """Send a message via webhook.

    Test Contract (from test_webhooks.py):
    - Returns success: True, message_id
    - Validates webhook URL format (must be Discord webhook URL)
    - Validates content length (1-2000 characters)
    - Optional username override (appears as webhook sender)
    - Optional avatar_url override

    Args:
        webhook_url: Full Discord webhook URL (from create_webhook)
        content: Message content, 1-2000 characters (required)
        username: Optional username override for this message
        avatar_url: Optional avatar override for this message

    Returns:
        {
            "success": True,
            "message_id": str
        }

    Raises:
        ValueError: If webhook_url/content invalid or missing
    """
    # Validate content
    if not content or not (1 <= len(content) <= 2000):
        raise ValueError(f"Content must be 1-2000 characters, got {len(content) if content else 0}")

    # Validate webhook URL
    if not webhook_url.startswith('https://discord.com/api/webhooks/'):
        raise ValueError(
            f"Invalid webhook URL format. "
            f"Expected 'https://discord.com/api/webhooks/...', got: {webhook_url}"
        )

    # Send via webhook
    from discord import Webhook
    import aiohttp

    try:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(webhook_url, session=session)

            # Send message (wait=True returns the message)
            message = await webhook.send(
                content=content,
                username=username,
                avatar_url=avatar_url,
                wait=True
            )

            return {
                "success": True,
                "message_id": str(message.id)
            }
    except discord.NotFound:
        raise ValueError("Webhook not found or has been deleted")
    except discord.HTTPException as e:
        raise ValueError(f"Failed to send webhook message: {e}")


async def delete_webhook(
    webhook_id: str,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """Delete a webhook.

    Test Contract (from test_webhooks.py):
    - Returns success: True, webhook_id, deleted_at
    - Validates webhook_id format
    - Validates webhook exists
    - Optional reason for audit log

    Args:
        webhook_id: Discord webhook ID (required)
        reason: Optional reason for audit log

    Returns:
        {
            "success": True,
            "webhook_id": str,
            "deleted_at": str (ISO8601)
        }

    Raises:
        ValueError: If webhook_id invalid or webhook not found
        PermissionError: If bot lacks permission to delete webhook
    """
    from datetime import datetime

    # Validate webhook_id format
    if not webhook_id or not webhook_id.isdigit() or len(webhook_id) < 17:
        raise ValueError(f"Invalid webhook_id format: {webhook_id}")

    # Fetch and delete webhook
    client = await get_client()

    try:
        webhook = await client.fetch_webhook(int(webhook_id))
        await webhook.delete(reason=reason)
    except discord.NotFound:
        raise ValueError(f"Webhook {webhook_id} not found")
    except discord.Forbidden:
        raise PermissionError("Bot lacks permission to delete this webhook")
    except discord.HTTPException as e:
        raise ValueError(f"Failed to delete webhook: {e}")

    return {
        "success": True,
        "webhook_id": webhook_id,
        "deleted_at": datetime.utcnow().isoformat()
    }
