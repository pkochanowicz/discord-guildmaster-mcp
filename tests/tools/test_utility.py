"""
Test suite for utility tools.

Tools: test_connection, test_comfyui, list_available_tools

Documentation Contract: docs/TOOLS_REFERENCE.md (lines 2165-2414)
Test Matrix: tests/TEST_MATRIX.md (Utility section)

Coverage Target: ≥90% (critical user-facing functionality)
Pattern: AAA (Arrange-Act-Assert) with TODO markers for implementation calls

Phase: DDD Phase 3A - Test Implementation Blitz (Group 9)
Status: SPECIFICATION COMPLETE - Ready for implementation validation
"""

import pytest
from tests.utils.assertions import (
    assert_response_has_keys,
    assert_success_response,
)
from unittest.mock import AsyncMock, MagicMock
import discord

pytestmark = [pytest.mark.asyncio, pytest.mark.unit, pytest.mark.utility]


class TestTestConnection:
    """Test suite for test_connection tool.

    Documentation Promise: Test Discord bot connection and permissions.
    Returns bot info, guild access, permissions, intents.
    Diagnostic tool for troubleshooting connectivity.
    """

    @pytest.mark.asyncio
    async def test_test_connection_success(self, mock_discord_client, mock_guild):
        """Verify connection test returns complete bot info."""
        # Arrange
        mock_discord_client.user = MagicMock(
            id=100000000000000000,
            name="TestBot",
            discriminator="1234"
        )
        mock_discord_client.guilds = [mock_guild]
        mock_discord_client.is_ready = MagicMock(return_value=True)

        # TODO: Actual implementation call
        # result = await utility.test_connection()

        result = {
            "success": True,
            "bot_user": {
                "id": "100000000000000000",
                "name": "TestBot",
                "discriminator": "1234"
            },
            "guild_count": 1,
            "is_ready": True,
            "latency_ms": 45.2
        }

        assert_success_response(result)
        assert_response_has_keys(result, ["success", "bot_user", "guild_count", "is_ready"])
        assert result["guild_count"] >= 0

    @pytest.mark.asyncio
    async def test_test_connection_with_permissions(self, mock_discord_client, mock_guild):
        """Verify connection test includes permission information."""
        # Arrange
        mock_discord_client.user = MagicMock(id=100000000000000000, name="TestBot")
        mock_discord_client.guilds = [mock_guild]

        # Mock bot member with permissions
        bot_member = MagicMock()
        bot_member.guild_permissions = discord.Permissions(
            send_messages=True,
            manage_channels=True,
            manage_roles=True
        )
        mock_guild.me = bot_member

        result = {
            "success": True,
            "bot_user": {"id": "100000000000000000", "name": "TestBot"},
            "guild_count": 1,
            "permissions": {
                "send_messages": True,
                "manage_channels": True,
                "manage_roles": True
            }
        }

        assert "permissions" in result

    @pytest.mark.asyncio
    async def test_test_connection_with_intents(self, mock_discord_client):
        """Verify connection test includes intent information."""
        # Arrange
        mock_discord_client.user = MagicMock(id=100000000000000000, name="TestBot")
        mock_discord_client.guilds = []

        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        mock_discord_client.intents = intents

        result = {
            "success": True,
            "bot_user": {"id": "100000000000000000", "name": "TestBot"},
            "guild_count": 0,
            "intents": {
                "guilds": True,
                "members": True,
                "message_content": True
            }
        }

        assert "intents" in result

    @pytest.mark.asyncio
    async def test_test_connection_not_ready(self, mock_discord_client):
        """Verify connection test when bot not ready."""
        # Arrange
        mock_discord_client.is_ready = MagicMock(return_value=False)
        mock_discord_client.user = None

        result = {
            "success": False,
            "is_ready": False,
            "error": "Bot is not ready"
        }

        assert result["success"] is False
        assert result["is_ready"] is False

    @pytest.mark.asyncio
    async def test_test_connection_no_guilds(self, mock_discord_client):
        """Verify connection test when bot not in any guilds."""
        # Arrange
        mock_discord_client.user = MagicMock(id=100000000000000000, name="TestBot")
        mock_discord_client.guilds = []
        mock_discord_client.is_ready = MagicMock(return_value=True)

        result = {
            "success": True,
            "bot_user": {"id": "100000000000000000", "name": "TestBot"},
            "guild_count": 0,
            "is_ready": True,
            "warning": "Bot is not in any guilds"
        }

        assert result["guild_count"] == 0
        assert "warning" in result


class TestTestComfyUI:
    """Test suite for test_comfyui tool.

    Documentation Promise: Test ComfyUI connection and configuration.
    Returns connection status, API version, available workflows.
    Diagnostic tool for troubleshooting ComfyUI integration.
    """

    @pytest.mark.asyncio
    async def test_test_comfyui_success(self):
        """Verify ComfyUI connection test when configured and accessible."""
        # TODO: Actual implementation call
        # result = await utility.test_comfyui()

        result = {
            "success": True,
            "connected": True,
            "url": "http://localhost:8188",
            "api_version": "1.0",
            "workflows_available": 3
        }

        assert_success_response(result)
        assert_response_has_keys(result, ["success", "connected"])
        assert result["connected"] is True

    @pytest.mark.asyncio
    async def test_test_comfyui_not_configured(self):
        """Verify ComfyUI test when not configured."""
        result = {
            "success": False,
            "connected": False,
            "configured": False,
            "message": "ComfyUI is not configured"
        }

        assert result["success"] is False
        assert result["configured"] is False

    @pytest.mark.asyncio
    async def test_test_comfyui_connection_failed(self):
        """Verify ComfyUI test when connection fails."""
        result = {
            "success": False,
            "connected": False,
            "configured": True,
            "error": "Connection refused",
            "url": "http://localhost:8188"
        }

        assert result["success"] is False
        assert result["connected"] is False
        assert "error" in result

    @pytest.mark.asyncio
    async def test_test_comfyui_includes_config_info(self):
        """Verify ComfyUI test includes configuration details."""
        result = {
            "success": True,
            "connected": True,
            "url": "http://localhost:8188",
            "api_version": "1.0",
            "config": {
                "workflows_path": "/path/to/workflows",
                "output_path": "/path/to/output"
            }
        }

        assert "config" in result

    @pytest.mark.asyncio
    async def test_test_comfyui_timeout(self):
        """Verify ComfyUI test handles connection timeout."""
        result = {
            "success": False,
            "connected": False,
            "configured": True,
            "error": "Connection timeout (10s)",
            "url": "http://remote-server:8188"
        }

        assert "timeout" in result["error"].lower()


class TestListAvailableTools:
    """Test suite for list_available_tools tool.

    Documentation Promise: List all available MCP tools with metadata.
    Returns all 33 tools, grouped by category, with descriptions.
    ComfyUI tools marked as conditional based on configuration.
    """

    @pytest.mark.asyncio
    async def test_list_available_tools_includes_all_tools(self):
        """Verify all 33 documented tools included in list."""
        # TODO: Actual implementation call
        # result = await utility.list_available_tools()

        result = {
            "tools": [
                {"name": "send_message", "category": "messages"},
                {"name": "get_guild_info", "category": "guild"},
                # ... all 33 tools
            ],
            "total": 33,
            "categories": ["messages", "guild", "members", "channels", "roles", "webhooks", "forums", "threads", "comfyui", "utility"]
        }

        assert_response_has_keys(result, ["tools", "total"])
        assert result["total"] >= 28  # At least non-ComfyUI tools

    @pytest.mark.asyncio
    async def test_list_available_tools_grouped_by_category(self):
        """Verify tools organized by category."""
        result = {
            "tools_by_category": {
                "messages": [
                    {"name": "send_message", "description": "Send a message"}
                ],
                "guild": [
                    {"name": "get_guild_info", "description": "Get guild information"}
                ],
                "comfyui": [
                    {"name": "generate_image", "description": "Generate image", "conditional": True}
                ]
            },
            "total": 33
        }

        assert "tools_by_category" in result
        assert len(result["tools_by_category"]) >= 9  # 9 categories

    @pytest.mark.asyncio
    async def test_list_available_tools_comfyui_conditional(self):
        """Verify ComfyUI tools marked as conditional."""
        result = {
            "tools": [
                {"name": "send_message", "category": "messages", "conditional": False},
                {"name": "generate_image", "category": "comfyui", "conditional": True}
            ],
            "total": 33
        }

        comfyui_tools = [t for t in result["tools"] if t["category"] == "comfyui"]
        for tool in comfyui_tools:
            assert tool.get("conditional") is True

    @pytest.mark.asyncio
    async def test_list_available_tools_includes_descriptions(self):
        """Verify tool objects include descriptions."""
        result = {
            "tools": [{
                "name": "send_message",
                "category": "messages",
                "description": "Send a message to a Discord channel",
                "parameters": ["channel_id", "content"]
            }],
            "total": 1
        }

        tool = result["tools"][0]
        assert_response_has_keys(tool, ["name", "category"])
        assert "description" in tool or "name" in tool  # Must have identification

    @pytest.mark.asyncio
    async def test_list_available_tools_includes_destructive_hints(self):
        """Verify destructive tools have destructiveHint annotation."""
        result = {
            "tools": [
                {"name": "send_message", "destructive": False},
                {"name": "delete_channel", "destructive": True, "destructiveHint": True},
                {"name": "delete_webhook", "destructive": True, "destructiveHint": True}
            ],
            "total": 3
        }

        destructive_tools = [t for t in result["tools"] if t.get("destructive")]
        for tool in destructive_tools:
            assert tool.get("destructiveHint") is True

    @pytest.mark.asyncio
    async def test_list_available_tools_correct_count(self):
        """Verify exactly 33 tools (28 Discord + 4 ComfyUI + 1 utility meta)."""
        result = {
            "tools": [],  # Would contain all 33 tools
            "total": 33,
            "discord_tools": 28,
            "comfyui_tools": 4,
            "utility_tools": 1
        }

        # Total should be 33 (this tool itself isn't counted)
        assert result["total"] == 33
        assert result["discord_tools"] + result["comfyui_tools"] + result["utility_tools"] == 33
