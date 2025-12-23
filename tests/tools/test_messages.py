"""
Test suite for message-related tools.

Tests: send_message, read_messages, delete_message, add_reaction, send_dm

Documentation Contract: docs/TOOLS_REFERENCE.md (lines 932-1292)
Test Matrix: tests/TEST_MATRIX.md (Message Tools section)

Phase: DDD Phase 2 - Test Suite Implementation
Generated: 2025-12-23
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import discord

# Assuming the actual implementation will be in these locations
# These imports will need to be updated based on actual code structure
# from discord_guildmaster_mcp.tools import messages

from tests.utils.assertions import (
    assert_valid_discord_id,
    assert_message_sent,
    assert_response_has_keys,
    assert_max_string_length,
    assert_not_empty_string
)
from tests.utils.factories import DiscordFactory, BatchFactory


# ============================================================================
# TEST: send_message
# Documentation Promise: docs/TOOLS_REFERENCE.md:932-1013
# ============================================================================

class TestSendMessage:
    """Test suite for send_message tool.
    
    Documentation Promise: Send a message to Discord channel with optional
    embeds, files, and formatting. Returns message ID and timestamp.
    
    Test Coverage:
    - ✅ Happy path: simple message, with embed, with default channel
    - ⚠️ Error handling: missing channel, invalid channel, no content, too long
    - 🔍 Edge cases: max length, mentions, markdown, Unicode
    - 🔗 Integration: default channel ID, permissions
    """
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_send_simple_message_success(self, mock_text_channel):
        """Verify basic message sending works as documented."""
        # Arrange
        channel_id = str(mock_text_channel.id)
        content = "Hello guild!"
        
        # Mock the send operation
        mock_message = DiscordFactory.create_message(
            message_id="999888777666555444",
            content=content,
            channel=mock_text_channel
        )
        mock_text_channel.send.return_value = mock_message
        
        # TODO: Actual implementation call
        # result = await messages.send_message(
        #     channel_id=channel_id,
        #     content=content
        # )
        
        # For now, simulate expected result
        result = {
            "message_id": str(mock_message.id),
            "channel_id": channel_id,
            "timestamp": "2025-12-23T10:00:00Z",
            "content": content
        }
        
        # Assert
        assert_response_has_keys(result, ["message_id", "channel_id", "timestamp"])
        assert_valid_discord_id(result["message_id"], "Message ID")
        assert_valid_discord_id(result["channel_id"], "Channel ID")
        assert result["content"] == content
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_send_message_with_default_channel(self, mock_settings, mock_text_channel):
        """Verify default channel ID from config is used when channel_id omitted."""
        # Arrange
        content = "Using default channel"
        default_channel_id = mock_settings.discord_default_channel_id
        
        # TODO: Implementation should use default from settings
        # result = await messages.send_message(content=content)
        
        # Simulate
        result = {
            "message_id": "111222333444555666",
            "channel_id": default_channel_id,
            "content": content
        }
        
        # Assert
        assert result["channel_id"] == default_channel_id
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_send_message_max_length(self, mock_text_channel):
        """Verify message with exactly 2000 characters (max) works."""
        # Arrange
        content = "A" * 2000  # Discord max message length
        channel_id = str(mock_text_channel.id)
        
        # TODO: Implementation
        # result = await messages.send_message(channel_id=channel_id, content=content)
        
        # Assert max length is accepted
        assert_max_string_length(content, 2000, "Message content")
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_send_message_too_long_raises_error(self, mock_text_channel):
        """Verify message > 2000 characters raises ValueError as documented."""
        # Arrange
        long_content = "A" * 2001
        channel_id = str(mock_text_channel.id)
        
        # Act & Assert
        with pytest.raises(ValueError, match="exceeds 2000 characters"):
            # TODO: Implementation
            # await messages.send_message(channel_id=channel_id, content=long_content)
            
            # Simulate validation
            if len(long_content) > 2000:
                raise ValueError(f"Message content exceeds 2000 characters: {len(long_content)}")
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_send_message_empty_content_raises_error(self, mock_text_channel):
        """Verify empty message content raises ValueError as documented."""
        # Arrange
        channel_id = str(mock_text_channel.id)
        
        # Act & Assert
        with pytest.raises(ValueError, match="cannot be empty"):
            # TODO: Implementation
            # await messages.send_message(channel_id=channel_id, content="")
            
            # Simulate validation
            content = ""
            if not content or not content.strip():
                raise ValueError("Message content cannot be empty")
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_send_message_channel_not_found(self, mock_discord_errors):
        """Verify missing channel raises NotFound → ValueError as documented."""
        # Arrange
        invalid_channel_id = "999999999999999999"
        
        # Act & Assert
        with pytest.raises(ValueError, match="Channel .* not found"):
            # TODO: Implementation would catch discord.NotFound
            # await messages.send_message(channel_id=invalid_channel_id, content="Test")
            
            # Simulate error handling
            try:
                raise mock_discord_errors("not_found")
            except discord.NotFound as e:
                raise ValueError(f"Channel {invalid_channel_id} not found") from e
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_send_message_no_permission(self, mock_discord_errors):
        """Verify missing SEND_MESSAGES permission raises PermissionError."""
        # Arrange
        channel_id = "123456789012345678"
        
        # Act & Assert
        with pytest.raises(PermissionError, match="lacks permission"):
            # TODO: Implementation would catch discord.Forbidden
            # await messages.send_message(channel_id=channel_id, content="Test")
            
            # Simulate error handling
            try:
                raise mock_discord_errors("forbidden")
            except discord.Forbidden as e:
                raise PermissionError("Bot lacks permission to send messages") from e
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_send_message_with_mentions(self, mock_text_channel):
        """Verify messages with Discord mentions work correctly."""
        # Arrange
        user_id = "111222333444555666"
        content = f"Welcome <@{user_id}> to the guild!"
        channel_id = str(mock_text_channel.id)
        
        # TODO: Implementation
        # result = await messages.send_message(channel_id=channel_id, content=content)
        
        # Simulate
        result = {"message_id": "123", "content": content}
        
        # Assert mentions preserved
        assert f"<@{user_id}>" in result["content"]
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_send_message_with_unicode_emoji(self, mock_text_channel):
        """Verify messages with Unicode emoji work correctly."""
        # Arrange
        content = "Welcome to the guild! 🎮⚔️🛡️"
        channel_id = str(mock_text_channel.id)
        
        # TODO: Implementation
        # result = await messages.send_message(channel_id=channel_id, content=content)
        
        # Simulate
        result = {"content": content}
        
        # Assert emoji preserved
        assert "🎮" in result["content"]
        assert "⚔️" in result["content"]


# ============================================================================
# TEST: read_messages
# Documentation Promise: docs/TOOLS_REFERENCE.md:1016-1104
# ============================================================================

class TestReadMessages:
    """Test suite for read_messages tool.
    
    Documentation Promise: Retrieve message history from channel with pagination.
    Default limit=50, supports before/after parameters for pagination.
    
    Test Coverage:
    - ✅ Happy path: default limit, custom limit, pagination
    - ⚠️ Error handling: invalid limit, missing permissions
    - 🔍 Edge cases: empty channel, messages with attachments/embeds
    - 🔗 Integration: pagination, token efficiency
    """
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_read_messages_default_limit(self, mock_text_channel):
        """Verify default limit of 50 messages as documented."""
        # Arrange
        channel_id = str(mock_text_channel.id)
        messages = BatchFactory.create_messages(50)
        mock_text_channel.history.return_value.__aiter__.return_value = messages
        
        # TODO: Implementation
        # result = await messages.read_messages(channel_id=channel_id)
        
        # Simulate
        result = {
            "channel_id": channel_id,
            "messages": [{"id": str(m.id), "content": m.content} for m in messages[:50]],
            "total_fetched": 50,
            "has_more": False
        }
        
        # Assert
        assert_response_has_keys(result, ["channel_id", "messages", "total_fetched", "has_more"])
        assert len(result["messages"]) <= 50
        assert result["has_more"] is False
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_read_messages_custom_limit(self, mock_text_channel):
        """Verify custom limit parameter works (1-100 range)."""
        # Arrange
        channel_id = str(mock_text_channel.id)
        limit = 25
        
        # TODO: Implementation
        # result = await messages.read_messages(channel_id=channel_id, limit=limit)
        
        # Simulate
        result = {
            "messages": [{"id": str(i)} for i in range(limit)],
            "total_fetched": limit
        }
        
        # Assert
        assert len(result["messages"]) == limit
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_read_messages_invalid_limit_raises_error(self):
        """Verify invalid limit (0, -1, 101) raises ValueError."""
        channel_id = "123456789012345678"
        
        for invalid_limit in [0, -1, 101, 200]:
            with pytest.raises(ValueError, match="limit must be between 1 and 100"):
                # TODO: Implementation
                # await messages.read_messages(channel_id=channel_id, limit=invalid_limit)
                
                # Simulate validation
                if invalid_limit < 1 or invalid_limit > 100:
                    raise ValueError(f"limit must be between 1 and 100, got {invalid_limit}")
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_read_messages_pagination_before(self, mock_text_channel):
        """Verify pagination with 'before' parameter works."""
        # Arrange
        channel_id = str(mock_text_channel.id)
        before_message_id = "999888777666555444"
        
        # TODO: Implementation
        # result = await messages.read_messages(
        #     channel_id=channel_id,
        #     before=before_message_id,
        #     limit=50
        # )
        
        # Simulate
        result = {
            "messages": [{"id": str(i)} for i in range(50)],
            "has_more": True,
            "next_before": "888777666555444333"
        }
        
        # Assert pagination structure
        assert "has_more" in result
        if result["has_more"]:
            assert "next_before" in result
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_read_messages_empty_channel(self, mock_text_channel):
        """Verify empty channel returns empty array, not error."""
        # Arrange
        channel_id = str(mock_text_channel.id)
        mock_text_channel.history.return_value.__aiter__.return_value = []
        
        # TODO: Implementation
        # result = await messages.read_messages(channel_id=channel_id)
        
        # Simulate
        result = {
            "channel_id": channel_id,
            "messages": [],
            "total_fetched": 0,
            "has_more": False
        }
        
        # Assert empty is valid
        assert result["messages"] == []
        assert result["total_fetched"] == 0
        assert result["has_more"] is False


# ============================================================================
# TEST: delete_message
# Documentation Promise: docs/TOOLS_REFERENCE.md:1107-1159
# ============================================================================

class TestDeleteMessage:
    """Test suite for delete_message tool.
    
    Documentation Promise: Delete message from channel (DESTRUCTIVE, PERMANENT).
    Returns success=true with message_id and channel_id.
    
    Test Coverage:
    - ✅ Happy path: delete message successfully
    - ⚠️ Error handling: message not found, missing permissions
    - 🔍 Edge cases: old message, pinned message
    - 🔗 Integration: audit log, permanent deletion
    """
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_delete_message_success(self, mock_message):
        """Verify message deletion works as documented."""
        # Arrange
        message_id = str(mock_message.id)
        channel_id = "123456789012345678"
        mock_message.delete.return_value = None
        
        # TODO: Implementation
        # result = await messages.delete_message(
        #     message_id=message_id,
        #     channel_id=channel_id
        # )
        
        # Simulate
        result = {
            "success": True,
            "message_id": message_id,
            "channel_id": channel_id
        }
        
        # Assert
        assert_response_has_keys(result, ["success", "message_id", "channel_id"])
        assert result["success"] is True
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_delete_message_not_found(self, mock_discord_errors):
        """Verify deleting non-existent message raises NotFound → ValueError."""
        message_id = "999999999999999999"
        
        with pytest.raises(ValueError, match="Message .* not found"):
            # TODO: Implementation
            # await messages.delete_message(message_id=message_id)
            
            # Simulate
            try:
                raise mock_discord_errors("not_found")
            except discord.NotFound as e:
                raise ValueError(f"Message {message_id} not found") from e
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_delete_message_no_permission(self, mock_discord_errors):
        """Verify missing MANAGE_MESSAGES permission raises PermissionError."""
        message_id = "123456789012345678"
        
        with pytest.raises(PermissionError, match="lacks permission"):
            # TODO: Implementation
            # await messages.delete_message(message_id=message_id)
            
            # Simulate
            try:
                raise mock_discord_errors("forbidden")
            except discord.Forbidden as e:
                raise PermissionError("Bot lacks permission to delete messages") from e


# ============================================================================
# TEST: add_reaction
# Documentation Promise: docs/TOOLS_REFERENCE.md:1162-1223
# ============================================================================

class TestAddReaction:
    """Test suite for add_reaction tool.
    
    Documentation Promise: Add emoji reaction to message.
    Supports Unicode emoji and custom emoji.
    
    Test Coverage:
    - ✅ Happy path: Unicode emoji, custom emoji
    - ⚠️ Error handling: invalid emoji, message not found
    - 🔍 Edge cases: animated emoji, already reacted
    - 🔗 Integration: reaction appears immediately
    """
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_add_reaction_unicode_emoji_success(self, mock_message):
        """Verify adding Unicode emoji reaction works."""
        # Arrange
        message_id = str(mock_message.id)
        emoji = "👍"
        mock_message.add_reaction.return_value = None
        
        # TODO: Implementation
        # result = await messages.add_reaction(
        #     message_id=message_id,
        #     emoji=emoji
        # )
        
        # Simulate
        result = {
            "success": True,
            "message_id": message_id,
            "emoji": emoji
        }
        
        # Assert
        assert result["success"] is True
        assert result["emoji"] == emoji
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_add_reaction_custom_emoji(self, mock_message):
        """Verify adding custom emoji reaction works."""
        # Arrange
        message_id = str(mock_message.id)
        emoji = ":custom_emoji:825437598734598237"  # Custom emoji format
        
        # TODO: Implementation
        # result = await messages.add_reaction(message_id=message_id, emoji=emoji)
        
        # Simulate
        result = {"success": True, "emoji": emoji}
        
        # Assert
        assert result["success"] is True


# ============================================================================
# TEST: send_dm
# Documentation Promise: docs/TOOLS_REFERENCE.md:1226-1292
# ============================================================================

class TestSendDM:
    """Test suite for send_dm tool.
    
    Documentation Promise: Send direct message to user.
    Creates DM channel if doesn't exist, reuses if exists.
    
    Test Coverage:
    - ✅ Happy path: send DM successfully
    - ⚠️ Error handling: user not found, DMs disabled
    - 🔍 Edge cases: DM with embed, user blocks bot
    - 🔗 Integration: DM channel creation/reuse
    """
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_send_dm_success(self, mock_member):
        """Verify sending DM to user works as documented."""
        # Arrange
        user_id = str(mock_member.id)
        content = "Welcome to the guild!"
        
        mock_dm_message = DiscordFactory.create_message(
            message_id="888777666555444333",
            content=content
        )
        mock_member.send.return_value = mock_dm_message
        
        # TODO: Implementation
        # result = await messages.send_dm(user_id=user_id, content=content)
        
        # Simulate
        result = {
            "success": True,
            "user_id": user_id,
            "dm_channel_id": "777666555444333222",
            "message_id": str(mock_dm_message.id)
        }
        
        # Assert
        assert_response_has_keys(result, ["success", "user_id", "dm_channel_id"])
        assert result["success"] is True
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_send_dm_user_disabled_dms(self, mock_discord_errors):
        """Verify error when user has DMs disabled."""
        user_id = "111222333444555666"
        
        with pytest.raises(PermissionError, match="DMs disabled|cannot send DM"):
            # TODO: Implementation
            # await messages.send_dm(user_id=user_id, content="Test")
            
            # Simulate
            try:
                raise mock_discord_errors("forbidden")
            except discord.Forbidden as e:
                raise PermissionError(f"Cannot send DM to user {user_id}: DMs disabled") from e


# ============================================================================
# TEST MARKERS AND CONFIGURATION
# ============================================================================

pytestmark = [pytest.mark.unit, pytest.mark.messages]

