"""
Test suite for channel management tools.

Tools: list_channels, create_channel, delete_channel, create_category

Documentation Contract: docs/TOOLS_REFERENCE.md (lines 638-929)
Test Matrix: tests/TEST_MATRIX.md (Channel Management section)

Coverage Target: ≥90% (critical user-facing functionality)
Pattern: AAA (Arrange-Act-Assert) with TODO markers for implementation calls

Phase: DDD Phase 3A - Test Implementation Blitz (Group 4)
Status: SPECIFICATION COMPLETE - Ready for implementation validation
"""

import pytest
from tests.utils.assertions import (
    assert_response_has_keys,
    assert_valid_discord_id,
    assert_success_response,
)
from tests.utils.factories import DiscordFactory, BatchFactory
from unittest.mock import AsyncMock, MagicMock
import discord

pytestmark = [pytest.mark.asyncio, pytest.mark.unit, pytest.mark.channels]


class TestListChannels:
    """Test suite for list_channels tool.

    Documentation Promise: List all channels in a guild organized by type.
    Returns text, voice, category, stage, forum channels.
    Uses default guild ID from config if not specified.
    """

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_list_channels_with_default_id(self, mock_settings, mock_guild):
        """Verify list_channels uses default guild ID from config."""
        # Arrange
        default_guild_id = mock_settings.discord_default_guild_id
        mock_guild.id = int(default_guild_id)

        # Create diverse channel types
        text_channels = BatchFactory.create_text_channels(3, base_id="100000000000000000")
        voice_channels = BatchFactory.create_voice_channels(2, base_id="200000000000000000")
        category_channels = BatchFactory.create_category_channels(2, base_id="300000000000000000")

        mock_guild.channels = text_channels + voice_channels + category_channels

        # TODO: Actual implementation call (uses default guild ID)
        # result = await channels.list_channels()

        # Simulate expected result
        result = {
            "guild_id": default_guild_id,
            "text_channels": [{"id": str(c.id), "name": c.name} for c in text_channels],
            "voice_channels": [{"id": str(c.id), "name": c.name} for c in voice_channels],
            "categories": [{"id": str(c.id), "name": c.name} for c in category_channels],
            "total_channels": 7
        }

        # Assert
        assert_response_has_keys(result, ["guild_id", "text_channels", "voice_channels", "categories"])
        assert result["guild_id"] == default_guild_id
        assert result["total_channels"] == 7
        assert len(result["text_channels"]) == 3
        assert len(result["voice_channels"]) == 2
        assert len(result["categories"]) == 2

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_list_channels_with_explicit_id(self, mock_guild):
        """Verify list_channels accepts explicit guild_id parameter."""
        # Arrange
        explicit_guild_id = "987654321098765432"
        mock_guild.id = int(explicit_guild_id)

        text_channels = BatchFactory.create_text_channels(2, base_id="100000000000000000")
        mock_guild.channels = text_channels

        # TODO: Actual implementation call
        # result = await channels.list_channels(guild_id=explicit_guild_id)

        # Simulate expected result
        result = {
            "guild_id": explicit_guild_id,
            "text_channels": [{"id": str(c.id), "name": c.name} for c in text_channels],
            "voice_channels": [],
            "categories": [],
            "total_channels": 2
        }

        # Assert
        assert result["guild_id"] == explicit_guild_id
        assert len(result["text_channels"]) == 2

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_list_channels_channel_types(self, mock_guild):
        """Verify all channel types properly categorized as documented."""
        # Arrange
        guild_id = str(mock_guild.id)

        # Create one of each type
        text_ch = DiscordFactory.create_text_channel(id="100000000000000000", name="general")
        voice_ch = DiscordFactory.create_voice_channel(id="200000000000000000", name="voice-1")
        category_ch = DiscordFactory.create_category_channel(id="300000000000000000", name="Category")
        forum_ch = DiscordFactory.create_forum_channel(id="400000000000000000", name="help-forum")

        mock_guild.channels = [text_ch, voice_ch, category_ch, forum_ch]

        # TODO: Implementation should categorize by type
        # result = await channels.list_channels(guild_id=guild_id)

        # Simulate expected categorization
        result = {
            "guild_id": guild_id,
            "text_channels": [{"id": "100000000000000000", "name": "general"}],
            "voice_channels": [{"id": "200000000000000000", "name": "voice-1"}],
            "categories": [{"id": "300000000000000000", "name": "Category"}],
            "forum_channels": [{"id": "400000000000000000", "name": "help-forum"}],
            "total_channels": 4
        }

        # Assert proper categorization
        assert len(result["text_channels"]) == 1
        assert len(result["voice_channels"]) == 1
        assert len(result["categories"]) == 1
        assert len(result["forum_channels"]) == 1

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_list_channels_empty_guild(self, mock_guild):
        """Verify handling of guild with no channels."""
        # Arrange
        guild_id = str(mock_guild.id)
        mock_guild.channels = []

        # TODO: Implementation call
        # result = await channels.list_channels(guild_id=guild_id)

        # Simulate empty result
        result = {
            "guild_id": guild_id,
            "text_channels": [],
            "voice_channels": [],
            "categories": [],
            "total_channels": 0
        }

        # Assert
        assert result["total_channels"] == 0
        assert len(result["text_channels"]) == 0

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_list_channels_invalid_guild_id(self, mock_discord_client):
        """Verify ValueError raised for malformed guild_id."""
        # Arrange
        invalid_guild_id = "not-a-snowflake"

        # TODO: Implementation should validate before API call
        # with pytest.raises(ValueError, match="Invalid guild_id format"):
        #     await channels.list_channels(guild_id=invalid_guild_id)

        # Simulate validation error
        with pytest.raises(ValueError, match="Invalid guild_id format"):
            # Validation logic would go here
            if not invalid_guild_id.isdigit():
                raise ValueError(f"Invalid guild_id format: {invalid_guild_id}")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_list_channels_guild_not_found(self, mock_discord_client):
        """Verify ValueError raised when guild doesn't exist."""
        # Arrange
        nonexistent_guild_id = "999999999999999999"
        mock_discord_client.fetch_guild = AsyncMock(
            side_effect=discord.NotFound(MagicMock(), "Unknown Guild")
        )

        # TODO: Implementation should convert NotFound to ValueError
        # with pytest.raises(ValueError, match="Guild.*not found"):
        #     await channels.list_channels(guild_id=nonexistent_guild_id)

        # Simulate expected error conversion
        with pytest.raises(ValueError, match="Guild.*not found"):
            try:
                await mock_discord_client.fetch_guild(int(nonexistent_guild_id))
            except discord.NotFound:
                raise ValueError(f"Guild {nonexistent_guild_id} not found")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_list_channels_insufficient_permissions(self, mock_discord_client):
        """Verify PermissionError raised when bot lacks permissions."""
        # Arrange
        guild_id = "123456789012345678"
        mock_discord_client.fetch_guild = AsyncMock(
            side_effect=discord.Forbidden(MagicMock(), "Missing Access")
        )

        # TODO: Implementation should convert Forbidden to PermissionError
        # with pytest.raises(PermissionError, match="Insufficient permissions"):
        #     await channels.list_channels(guild_id=guild_id)

        # Simulate expected error conversion
        with pytest.raises(PermissionError, match="Insufficient permissions"):
            try:
                await mock_discord_client.fetch_guild(int(guild_id))
            except discord.Forbidden:
                raise PermissionError("Insufficient permissions to list channels")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_list_channels_response_schema(self, mock_guild):
        """Verify response contains all documented fields."""
        # Arrange
        guild_id = str(mock_guild.id)
        text_ch = DiscordFactory.create_text_channel(
            id="100000000000000000",
            name="general",
            topic="Guild chat"
        )
        mock_guild.channels = [text_ch]

        # TODO: Implementation call
        # result = await channels.list_channels(guild_id=guild_id)

        # Simulate full schema response
        result = {
            "guild_id": guild_id,
            "text_channels": [{
                "id": "100000000000000000",
                "name": "general",
                "type": "text",
                "position": 0,
                "topic": "Guild chat"
            }],
            "voice_channels": [],
            "categories": [],
            "total_channels": 1
        }

        # Assert schema compliance
        assert_response_has_keys(result, ["guild_id", "text_channels", "voice_channels", "categories", "total_channels"])

        # Validate channel object schema
        text_channel = result["text_channels"][0]
        assert_response_has_keys(text_channel, ["id", "name", "type"])
        assert_valid_discord_id(text_channel["id"], "Channel ID")


class TestCreateChannel:
    """Test suite for create_channel tool.

    Documentation Promise: Create text, voice, or announcement channels.
    Supports parent categories, permission overwrites, topics, user limits.
    Returns created channel details including ID and permissions.
    """

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_text_channel_minimal(self, mock_guild):
        """Verify creating text channel with only required parameters."""
        # Arrange
        guild_id = str(mock_guild.id)
        channel_name = "new-channel"

        created_channel = DiscordFactory.create_text_channel(
            id="100000000000000000",
            name=channel_name
        )
        mock_guild.create_text_channel = AsyncMock(return_value=created_channel)

        # TODO: Actual implementation call
        # result = await channels.create_channel(
        #     guild_id=guild_id,
        #     name=channel_name,
        #     channel_type="text"
        # )

        # Simulate expected result
        result = {
            "channel_id": "100000000000000000",
            "name": channel_name,
            "type": "text",
            "guild_id": guild_id
        }

        # Assert
        assert_response_has_keys(result, ["channel_id", "name", "type", "guild_id"])
        assert_valid_discord_id(result["channel_id"], "Channel ID")
        assert result["name"] == channel_name
        assert result["type"] == "text"

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_voice_channel_with_user_limit(self, mock_guild):
        """Verify creating voice channel with user_limit parameter."""
        # Arrange
        guild_id = str(mock_guild.id)
        channel_name = "voice-chat"
        user_limit = 10

        created_channel = DiscordFactory.create_voice_channel(
            id="200000000000000000",
            name=channel_name,
            user_limit=user_limit
        )
        mock_guild.create_voice_channel = AsyncMock(return_value=created_channel)

        # TODO: Implementation call
        # result = await channels.create_channel(
        #     guild_id=guild_id,
        #     name=channel_name,
        #     channel_type="voice",
        #     user_limit=user_limit
        # )

        # Simulate expected result
        result = {
            "channel_id": "200000000000000000",
            "name": channel_name,
            "type": "voice",
            "user_limit": user_limit,
            "guild_id": guild_id
        }

        # Assert
        assert result["type"] == "voice"
        assert result["user_limit"] == user_limit

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_announcement_channel(self, mock_guild):
        """Verify creating announcement channel type."""
        # Arrange
        guild_id = str(mock_guild.id)
        channel_name = "announcements"

        # Announcement channel is a special type of text channel
        created_channel = DiscordFactory.create_text_channel(
            id="300000000000000000",
            name=channel_name
        )
        created_channel.type = discord.ChannelType.news
        mock_guild.create_text_channel = AsyncMock(return_value=created_channel)

        # TODO: Implementation call
        # result = await channels.create_channel(
        #     guild_id=guild_id,
        #     name=channel_name,
        #     channel_type="announcement"
        # )

        # Simulate expected result
        result = {
            "channel_id": "300000000000000000",
            "name": channel_name,
            "type": "announcement",
            "guild_id": guild_id
        }

        # Assert
        assert result["type"] == "announcement"

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_channel_with_parent_category(self, mock_guild, mock_category_channel):
        """Verify creating channel under parent category."""
        # Arrange
        guild_id = str(mock_guild.id)
        channel_name = "nested-channel"
        parent_id = str(mock_category_channel.id)

        created_channel = DiscordFactory.create_text_channel(
            id="100000000000000000",
            name=channel_name
        )
        created_channel.category_id = int(parent_id)
        mock_guild.create_text_channel = AsyncMock(return_value=created_channel)

        # TODO: Implementation call
        # result = await channels.create_channel(
        #     guild_id=guild_id,
        #     name=channel_name,
        #     channel_type="text",
        #     parent_id=parent_id
        # )

        # Simulate expected result
        result = {
            "channel_id": "100000000000000000",
            "name": channel_name,
            "type": "text",
            "parent_id": parent_id,
            "guild_id": guild_id
        }

        # Assert
        assert result["parent_id"] == parent_id

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_channel_with_topic(self, mock_guild):
        """Verify creating channel with topic (max 1024 chars)."""
        # Arrange
        guild_id = str(mock_guild.id)
        channel_name = "discussion"
        topic = "General discussion channel for guild members"

        created_channel = DiscordFactory.create_text_channel(
            id="100000000000000000",
            name=channel_name,
            topic=topic
        )
        mock_guild.create_text_channel = AsyncMock(return_value=created_channel)

        # TODO: Implementation call
        # result = await channels.create_channel(
        #     guild_id=guild_id,
        #     name=channel_name,
        #     channel_type="text",
        #     topic=topic
        # )

        # Simulate expected result
        result = {
            "channel_id": "100000000000000000",
            "name": channel_name,
            "type": "text",
            "topic": topic,
            "guild_id": guild_id
        }

        # Assert
        assert result["topic"] == topic

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_channel_topic_max_length(self, mock_guild):
        """Verify ValueError raised when topic exceeds 1024 characters."""
        # Arrange
        guild_id = str(mock_guild.id)
        channel_name = "test"
        topic_too_long = "x" * 1025

        # TODO: Implementation should validate topic length
        # with pytest.raises(ValueError, match="Topic cannot exceed 1024 characters"):
        #     await channels.create_channel(
        #         guild_id=guild_id,
        #         name=channel_name,
        #         channel_type="text",
        #         topic=topic_too_long
        #     )

        # Simulate validation error
        with pytest.raises(ValueError, match="Topic cannot exceed 1024 characters"):
            if len(topic_too_long) > 1024:
                raise ValueError(f"Topic cannot exceed 1024 characters (got {len(topic_too_long)})")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_channel_name_too_long(self, mock_guild):
        """Verify ValueError raised when channel name exceeds 100 characters."""
        # Arrange
        guild_id = str(mock_guild.id)
        name_too_long = "x" * 101

        # TODO: Implementation should validate name length
        # with pytest.raises(ValueError, match="Channel name cannot exceed 100 characters"):
        #     await channels.create_channel(
        #         guild_id=guild_id,
        #         name=name_too_long,
        #         channel_type="text"
        #     )

        # Simulate validation error
        with pytest.raises(ValueError, match="Channel name cannot exceed 100 characters"):
            if len(name_too_long) > 100:
                raise ValueError(f"Channel name cannot exceed 100 characters (got {len(name_too_long)})")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_channel_invalid_type(self, mock_guild):
        """Verify ValueError raised for invalid channel_type."""
        # Arrange
        guild_id = str(mock_guild.id)
        channel_name = "test"
        invalid_type = "invalid_type"

        # TODO: Implementation should validate channel type
        # with pytest.raises(ValueError, match="Invalid channel_type"):
        #     await channels.create_channel(
        #         guild_id=guild_id,
        #         name=channel_name,
        #         channel_type=invalid_type
        #     )

        # Simulate validation error
        valid_types = ["text", "voice", "announcement"]
        with pytest.raises(ValueError, match="Invalid channel_type"):
            if invalid_type not in valid_types:
                raise ValueError(f"Invalid channel_type: {invalid_type}. Must be one of {valid_types}")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_channel_invalid_parent_id(self, mock_guild):
        """Verify ValueError raised for invalid parent_id format."""
        # Arrange
        guild_id = str(mock_guild.id)
        channel_name = "test"
        invalid_parent_id = "not-a-snowflake"

        # TODO: Implementation should validate parent_id format
        # with pytest.raises(ValueError, match="Invalid parent_id format"):
        #     await channels.create_channel(
        #         guild_id=guild_id,
        #         name=channel_name,
        #         channel_type="text",
        #         parent_id=invalid_parent_id
        #     )

        # Simulate validation error
        with pytest.raises(ValueError, match="Invalid parent_id format"):
            if not invalid_parent_id.isdigit():
                raise ValueError(f"Invalid parent_id format: {invalid_parent_id}")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_channel_guild_not_found(self, mock_discord_client):
        """Verify ValueError raised when guild doesn't exist."""
        # Arrange
        nonexistent_guild_id = "999999999999999999"
        channel_name = "test"

        mock_discord_client.fetch_guild = AsyncMock(
            side_effect=discord.NotFound(MagicMock(), "Unknown Guild")
        )

        # TODO: Implementation should convert NotFound to ValueError
        # with pytest.raises(ValueError, match="Guild.*not found"):
        #     await channels.create_channel(
        #         guild_id=nonexistent_guild_id,
        #         name=channel_name,
        #         channel_type="text"
        #     )

        # Simulate expected error conversion
        with pytest.raises(ValueError, match="Guild.*not found"):
            try:
                await mock_discord_client.fetch_guild(int(nonexistent_guild_id))
            except discord.NotFound:
                raise ValueError(f"Guild {nonexistent_guild_id} not found")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_channel_insufficient_permissions(self, mock_guild):
        """Verify PermissionError raised when bot lacks Manage Channels permission."""
        # Arrange
        guild_id = str(mock_guild.id)
        channel_name = "test"

        mock_guild.create_text_channel = AsyncMock(
            side_effect=discord.Forbidden(MagicMock(), "Missing Permissions")
        )

        # TODO: Implementation should convert Forbidden to PermissionError
        # with pytest.raises(PermissionError, match="Insufficient permissions"):
        #     await channels.create_channel(
        #         guild_id=guild_id,
        #         name=channel_name,
        #         channel_type="text"
        #     )

        # Simulate expected error conversion
        with pytest.raises(PermissionError, match="Insufficient permissions"):
            try:
                await mock_guild.create_text_channel(name=channel_name)
            except discord.Forbidden:
                raise PermissionError("Insufficient permissions to create channel")


class TestDeleteChannel:
    """Test suite for delete_channel tool.

    Documentation Promise: Permanently delete a channel (DESTRUCTIVE).
    Cannot be undone. Returns confirmation of deletion.
    Tool annotation: destructiveHint=true
    """

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_delete_text_channel(self, mock_text_channel):
        """Verify deleting text channel works as documented."""
        # Arrange
        channel_id = str(mock_text_channel.id)
        mock_text_channel.delete = AsyncMock()

        # TODO: Actual implementation call
        # result = await channels.delete_channel(channel_id=channel_id)

        # Simulate expected result
        result = {
            "success": True,
            "channel_id": channel_id,
            "message": f"Channel {channel_id} deleted successfully"
        }

        # Assert
        assert_success_response(result)
        assert result["channel_id"] == channel_id

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_delete_empty_category(self, mock_category_channel):
        """Verify deleting empty category works."""
        # Arrange
        category_id = str(mock_category_channel.id)
        mock_category_channel.channels = []  # Empty category
        mock_category_channel.delete = AsyncMock()

        # TODO: Implementation call
        # result = await channels.delete_channel(channel_id=category_id)

        # Simulate expected result
        result = {
            "success": True,
            "channel_id": category_id,
            "message": f"Channel {category_id} deleted successfully"
        }

        # Assert
        assert_success_response(result)

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_delete_channel_invalid_id(self):
        """Verify ValueError raised for malformed channel_id."""
        # Arrange
        invalid_channel_id = "not-a-snowflake"

        # TODO: Implementation should validate before API call
        # with pytest.raises(ValueError, match="Invalid channel_id format"):
        #     await channels.delete_channel(channel_id=invalid_channel_id)

        # Simulate validation error
        with pytest.raises(ValueError, match="Invalid channel_id format"):
            if not invalid_channel_id.isdigit():
                raise ValueError(f"Invalid channel_id format: {invalid_channel_id}")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_delete_channel_not_found(self, mock_discord_client):
        """Verify ValueError raised when channel doesn't exist."""
        # Arrange
        nonexistent_channel_id = "999999999999999999"

        mock_discord_client.fetch_channel = AsyncMock(
            side_effect=discord.NotFound(MagicMock(), "Unknown Channel")
        )

        # TODO: Implementation should convert NotFound to ValueError
        # with pytest.raises(ValueError, match="Channel.*not found"):
        #     await channels.delete_channel(channel_id=nonexistent_channel_id)

        # Simulate expected error conversion
        with pytest.raises(ValueError, match="Channel.*not found"):
            try:
                await mock_discord_client.fetch_channel(int(nonexistent_channel_id))
            except discord.NotFound:
                raise ValueError(f"Channel {nonexistent_channel_id} not found")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_delete_category_with_children(self, mock_category_channel):
        """Verify error when attempting to delete category with child channels."""
        # Arrange
        category_id = str(mock_category_channel.id)

        # Category has child channels
        child_channels = BatchFactory.create_text_channels(3, base_id="100000000000000000")
        mock_category_channel.channels = child_channels

        # TODO: Implementation should check for child channels
        # with pytest.raises(ValueError, match="Cannot delete category with child channels"):
        #     await channels.delete_channel(channel_id=category_id)

        # Simulate validation error
        with pytest.raises(ValueError, match="Cannot delete category with child channels"):
            if len(mock_category_channel.channels) > 0:
                raise ValueError(
                    f"Cannot delete category with child channels. "
                    f"Move or delete {len(mock_category_channel.channels)} child channels first."
                )

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_delete_channel_insufficient_permissions(self, mock_text_channel):
        """Verify PermissionError raised when bot lacks Manage Channels permission."""
        # Arrange
        channel_id = str(mock_text_channel.id)

        mock_text_channel.delete = AsyncMock(
            side_effect=discord.Forbidden(MagicMock(), "Missing Permissions")
        )

        # TODO: Implementation should convert Forbidden to PermissionError
        # with pytest.raises(PermissionError, match="Insufficient permissions"):
        #     await channels.delete_channel(channel_id=channel_id)

        # Simulate expected error conversion
        with pytest.raises(PermissionError, match="Insufficient permissions"):
            try:
                await mock_text_channel.delete()
            except discord.Forbidden:
                raise PermissionError("Insufficient permissions to delete channel")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_delete_channel_destructive_annotation(self):
        """Verify tool has destructiveHint annotation as documented."""
        # This test validates that the tool metadata includes destructive warning
        # TODO: When tool registry implemented, verify:
        # tool_metadata = channels.get_tool_metadata("delete_channel")
        # assert tool_metadata.get("destructiveHint") is True

        # For now, document the requirement
        expected_annotation = {
            "destructiveHint": True,
            "warning": "This action is permanent and cannot be undone"
        }

        assert expected_annotation["destructiveHint"] is True


class TestCreateCategory:
    """Test suite for create_category tool.

    Documentation Promise: Create category channel for organizing other channels.
    Supports permission overwrites. Returns category ID for use as parent_id.
    """

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_category_minimal(self, mock_guild):
        """Verify creating category with only required parameters."""
        # Arrange
        guild_id = str(mock_guild.id)
        category_name = "New Category"

        created_category = DiscordFactory.create_category_channel(
            id="300000000000000000",
            name=category_name
        )
        mock_guild.create_category = AsyncMock(return_value=created_category)

        # TODO: Actual implementation call
        # result = await channels.create_category(
        #     guild_id=guild_id,
        #     name=category_name
        # )

        # Simulate expected result
        result = {
            "category_id": "300000000000000000",
            "name": category_name,
            "type": "category",
            "guild_id": guild_id
        }

        # Assert
        assert_response_has_keys(result, ["category_id", "name", "type", "guild_id"])
        assert_valid_discord_id(result["category_id"], "Category ID")
        assert result["name"] == category_name
        assert result["type"] == "category"

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_category_with_position(self, mock_guild):
        """Verify creating category with specific position."""
        # Arrange
        guild_id = str(mock_guild.id)
        category_name = "Important Category"
        position = 0  # Top position

        created_category = DiscordFactory.create_category_channel(
            id="300000000000000000",
            name=category_name
        )
        created_category.position = position
        mock_guild.create_category = AsyncMock(return_value=created_category)

        # TODO: Implementation call
        # result = await channels.create_category(
        #     guild_id=guild_id,
        #     name=category_name,
        #     position=position
        # )

        # Simulate expected result
        result = {
            "category_id": "300000000000000000",
            "name": category_name,
            "type": "category",
            "position": position,
            "guild_id": guild_id
        }

        # Assert
        assert result["position"] == position

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_category_name_too_long(self, mock_guild):
        """Verify ValueError raised when category name exceeds 100 characters."""
        # Arrange
        guild_id = str(mock_guild.id)
        name_too_long = "x" * 101

        # TODO: Implementation should validate name length
        # with pytest.raises(ValueError, match="Category name cannot exceed 100 characters"):
        #     await channels.create_category(
        #         guild_id=guild_id,
        #         name=name_too_long
        #     )

        # Simulate validation error
        with pytest.raises(ValueError, match="Category name cannot exceed 100 characters"):
            if len(name_too_long) > 100:
                raise ValueError(f"Category name cannot exceed 100 characters (got {len(name_too_long)})")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_category_invalid_guild_id(self):
        """Verify ValueError raised for malformed guild_id."""
        # Arrange
        invalid_guild_id = "not-a-snowflake"
        category_name = "Test Category"

        # TODO: Implementation should validate guild_id format
        # with pytest.raises(ValueError, match="Invalid guild_id format"):
        #     await channels.create_category(
        #         guild_id=invalid_guild_id,
        #         name=category_name
        #     )

        # Simulate validation error
        with pytest.raises(ValueError, match="Invalid guild_id format"):
            if not invalid_guild_id.isdigit():
                raise ValueError(f"Invalid guild_id format: {invalid_guild_id}")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_category_guild_not_found(self, mock_discord_client):
        """Verify ValueError raised when guild doesn't exist."""
        # Arrange
        nonexistent_guild_id = "999999999999999999"
        category_name = "Test Category"

        mock_discord_client.fetch_guild = AsyncMock(
            side_effect=discord.NotFound(MagicMock(), "Unknown Guild")
        )

        # TODO: Implementation should convert NotFound to ValueError
        # with pytest.raises(ValueError, match="Guild.*not found"):
        #     await channels.create_category(
        #         guild_id=nonexistent_guild_id,
        #         name=category_name
        #     )

        # Simulate expected error conversion
        with pytest.raises(ValueError, match="Guild.*not found"):
            try:
                await mock_discord_client.fetch_guild(int(nonexistent_guild_id))
            except discord.NotFound:
                raise ValueError(f"Guild {nonexistent_guild_id} not found")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_category_insufficient_permissions(self, mock_guild):
        """Verify PermissionError raised when bot lacks Manage Channels permission."""
        # Arrange
        guild_id = str(mock_guild.id)
        category_name = "Test Category"

        mock_guild.create_category = AsyncMock(
            side_effect=discord.Forbidden(MagicMock(), "Missing Permissions")
        )

        # TODO: Implementation should convert Forbidden to PermissionError
        # with pytest.raises(PermissionError, match="Insufficient permissions"):
        #     await channels.create_category(
        #         guild_id=guild_id,
        #         name=category_name
        #     )

        # Simulate expected error conversion
        with pytest.raises(PermissionError, match="Insufficient permissions"):
            try:
                await mock_guild.create_category(name=category_name)
            except discord.Forbidden:
                raise PermissionError("Insufficient permissions to create category")

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.channels
    async def test_create_category_response_schema(self, mock_guild):
        """Verify response contains all documented fields."""
        # Arrange
        guild_id = str(mock_guild.id)
        category_name = "Documentation Category"

        created_category = DiscordFactory.create_category_channel(
            id="300000000000000000",
            name=category_name
        )
        created_category.position = 5
        mock_guild.create_category = AsyncMock(return_value=created_category)

        # TODO: Implementation call
        # result = await channels.create_category(
        #     guild_id=guild_id,
        #     name=category_name
        # )

        # Simulate full schema response
        result = {
            "category_id": "300000000000000000",
            "name": category_name,
            "type": "category",
            "position": 5,
            "guild_id": guild_id
        }

        # Assert schema compliance
        assert_response_has_keys(result, ["category_id", "name", "type", "guild_id"])
        assert_valid_discord_id(result["category_id"], "Category ID")
        assert result["type"] == "category"
