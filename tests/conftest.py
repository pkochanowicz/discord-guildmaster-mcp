"""
Shared test fixtures for discord-guildmaster-mcp test suite.

This module provides comprehensive mocking infrastructure for testing all tools
without requiring actual Discord API or ComfyUI connections.

Phase: DDD Phase 2 - Test Suite Implementation
Generated: 2025-12-23
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, Mock
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import discord


# ============================================================================
# CORE FIXTURES - CONFIGURATION
# ============================================================================

@pytest.fixture
def mock_settings():
    """Standard test configuration with all required settings.
    
    Returns Settings object with safe test values.
    Used by most tests as base configuration.
    """
    from discord_guildmaster_mcp.config import Settings
    
    return Settings(
        discord_token="test_token_MTIzNDU2Nzg5MDEyMzQ1Njc4.Xy1234.abcdefghijk",
        discord_default_guild_id="987654321098765432",
        discord_default_channel_id="123456789012345678",
        guildmaster_theme="generic",
        comfyui_enabled=False,
        log_level="DEBUG"
    )


@pytest.fixture
def mock_settings_with_comfyui(mock_settings):
    """Configuration with ComfyUI enabled for testing image generation."""
    mock_settings.comfyui_enabled = True
    mock_settings.comfyui_host = "localhost"
    mock_settings.comfyui_port = 8188
    mock_settings.comfyui_return_mode = "base64"
    mock_settings.comfyui_timeout = 300
    return mock_settings


@pytest.fixture
def mock_settings_wow_theme(mock_settings):
    """Configuration with WoW theme for testing theme system."""
    mock_settings.guildmaster_theme = "wow"
    return mock_settings


# ============================================================================
# DISCORD CLIENT FIXTURES
# ============================================================================

@pytest.fixture
def mock_discord_client():
    """Fully mocked Discord client with common operations.
    
    Provides AsyncMock client with standard methods for:
    - Guild operations
    - Channel operations
    - Member operations
    - Message operations
    """
    client = AsyncMock(spec=discord.Client)
    client.is_ready.return_value = True
    client.is_closed.return_value = False
    client.user = MagicMock(spec=discord.ClientUser)
    client.user.id = 111111111111111111
    client.user.name = "TestBot"
    client.user.discriminator = "0001"
    
    # Guild operations
    client.get_guild = MagicMock()
    client.fetch_guild = AsyncMock()
    client.guilds = []
    
    # Channel operations
    client.get_channel = MagicMock()
    client.fetch_channel = AsyncMock()
    
    # User operations
    client.get_user = MagicMock()
    client.fetch_user = AsyncMock()
    
    return client


# ============================================================================
# DISCORD OBJECT FIXTURES - GUILD
# ============================================================================

@pytest.fixture
def mock_guild():
    """Standard Discord guild for testing.
    
    Returns AsyncMock guild with realistic data matching documentation examples.
    """
    guild = AsyncMock(spec=discord.Guild)
    guild.id = 987654321098765432
    guild.name = "Azeroth Bound"
    guild.description = "World of Warcraft Classic+ guild"
    guild.member_count = 127
    guild.max_members = 500
    guild.owner_id = 123456789012345678
    guild.verification_level = discord.VerificationLevel.medium
    guild.created_at = datetime(2023, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
    guild.icon = MagicMock()
    guild.icon.url = "https://cdn.discordapp.com/icons/987654321098765432/abc123.png"
    guild.features = ["COMMUNITY", "THREADS", "ROLE_ICONS"]
    
    # Empty collections (populated by specific tests)
    guild.channels = []
    guild.roles = []
    guild.members = []
    guild.emojis = []
    
    # Methods
    guild.fetch_member = AsyncMock()
    guild.fetch_channel = AsyncMock()
    guild.fetch_roles = AsyncMock(return_value=[])
    guild.create_role = AsyncMock()
    guild.create_text_channel = AsyncMock()
    guild.create_voice_channel = AsyncMock()
    guild.create_category = AsyncMock()
    
    return guild


# ============================================================================
# DISCORD OBJECT FIXTURES - CHANNELS
# ============================================================================

@pytest.fixture
def mock_text_channel():
    """Standard text channel for testing."""
    channel = AsyncMock(spec=discord.TextChannel)
    channel.id = 123456789012345678
    channel.name = "general"
    channel.guild = None  # Set by tests if needed
    channel.position = 0
    channel.category_id = None
    channel.topic = "General discussion"
    channel.nsfw = False
    channel.slowmode_delay = 0
    channel.created_at = datetime(2023, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
    
    # Methods
    channel.send = AsyncMock()
    channel.fetch_message = AsyncMock()
    channel.history = MagicMock()
    channel.purge = AsyncMock()
    channel.edit = AsyncMock()
    channel.delete = AsyncMock()
    channel.create_webhook = AsyncMock()
    channel.create_thread = AsyncMock()
    
    return channel


@pytest.fixture
def mock_voice_channel():
    """Standard voice channel for testing."""
    channel = AsyncMock(spec=discord.VoiceChannel)
    channel.id = 234567890123456789
    channel.name = "General Voice"
    channel.guild = None
    channel.position = 0
    channel.category_id = None
    channel.bitrate = 64000
    channel.user_limit = 0
    channel.created_at = datetime(2023, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
    
    channel.edit = AsyncMock()
    channel.delete = AsyncMock()
    
    return channel


@pytest.fixture
def mock_category_channel():
    """Standard category channel for testing."""
    category = AsyncMock(spec=discord.CategoryChannel)
    category.id = 345678901234567890
    category.name = "Guild Channels"
    category.guild = None
    category.position = 0
    category.created_at = datetime(2023, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
    category.channels = []
    
    category.edit = AsyncMock()
    category.delete = AsyncMock()
    category.create_text_channel = AsyncMock()
    category.create_voice_channel = AsyncMock()
    
    return category


@pytest.fixture
def mock_forum_channel():
    """Standard forum channel for testing."""
    channel = AsyncMock(spec=discord.ForumChannel)
    channel.id = 456789012345678901
    channel.name = "guild-discussion"
    channel.guild = None
    channel.position = 0
    channel.category_id = None
    channel.topic = "Guild discussions and announcements"
    channel.created_at = datetime(2023, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
    channel.default_auto_archive_duration = 1440
    channel.available_tags = []
    
    channel.create_thread = AsyncMock()
    channel.archived_threads = AsyncMock()
    
    return channel


# ============================================================================
# DISCORD OBJECT FIXTURES - MEMBERS & USERS
# ============================================================================

@pytest.fixture
def mock_member():
    """Standard guild member for testing."""
    member = AsyncMock(spec=discord.Member)
    member.id = 111222333444555666
    member.name = "TestUser"
    member.discriminator = "1234"
    member.display_name = "Test User"
    member.nick = "Test User"
    member.bot = False
    member.joined_at = datetime(2023, 6, 15, 10, 0, 0, tzinfo=timezone.utc)
    member.created_at = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    member.avatar = MagicMock()
    member.avatar.url = "https://cdn.discordapp.com/avatars/111222333444555666/avatar.png"
    member.status = discord.Status.online
    member.activities = []
    
    # Roles and permissions
    member.roles = []
    member.top_role = None
    member.guild_permissions = discord.Permissions.none()
    
    # Methods
    member.add_roles = AsyncMock()
    member.remove_roles = AsyncMock()
    member.edit = AsyncMock()
    member.kick = AsyncMock()
    member.ban = AsyncMock()
    member.send = AsyncMock()  # DM capability
    
    return member


@pytest.fixture
def mock_member_officer(mock_member):
    """Guild member with officer role and elevated permissions."""
    mock_role = MagicMock(spec=discord.Role)
    mock_role.id = 999888777666555444
    mock_role.name = "Officer"
    mock_role.color = discord.Color.red()
    mock_role.position = 5
    mock_role.permissions = discord.Permissions(administrator=True)
    
    mock_member.roles = [mock_role]
    mock_member.top_role = mock_role
    mock_member.guild_permissions = discord.Permissions(administrator=True)
    
    return mock_member


# ============================================================================
# DISCORD OBJECT FIXTURES - ROLES
# ============================================================================

@pytest.fixture
def mock_role():
    """Standard role for testing."""
    role = MagicMock(spec=discord.Role)
    role.id = 777888999000111222
    role.name = "Member"
    role.color = discord.Color.green()
    role.position = 1
    role.permissions = discord.Permissions(
        view_channel=True,
        send_messages=True,
        read_message_history=True
    )
    role.mentionable = False
    role.hoist = False
    role.managed = False
    role.created_at = datetime(2023, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
    
    # Methods
    role.edit = AsyncMock()
    role.delete = AsyncMock()
    
    return role


@pytest.fixture
def mock_role_admin():
    """Administrative role for testing."""
    role = MagicMock(spec=discord.Role)
    role.id = 888999000111222333
    role.name = "Administrator"
    role.color = discord.Color.gold()
    role.position = 10
    role.permissions = discord.Permissions(administrator=True)
    role.mentionable = True
    role.hoist = True
    role.managed = False
    role.created_at = datetime(2023, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
    
    role.edit = AsyncMock()
    role.delete = AsyncMock()
    
    return role


# ============================================================================
# DISCORD OBJECT FIXTURES - MESSAGES
# ============================================================================

@pytest.fixture
def mock_message():
    """Standard message for testing."""
    message = AsyncMock(spec=discord.Message)
    message.id = 222333444555666777
    message.content = "Test message content"
    message.author = None  # Set by tests
    message.channel = None  # Set by tests
    message.guild = None  # Set by tests
    message.created_at = datetime(2025, 12, 23, 10, 0, 0, tzinfo=timezone.utc)
    message.edited_at = None
    message.embeds = []
    message.attachments = []
    message.reactions = []
    message.pinned = False
    message.mention_everyone = False
    message.mentions = []
    message.role_mentions = []
    
    # Methods
    message.edit = AsyncMock()
    message.delete = AsyncMock()
    message.add_reaction = AsyncMock()
    message.remove_reaction = AsyncMock()
    message.pin = AsyncMock()
    message.unpin = AsyncMock()
    message.reply = AsyncMock()
    
    return message


# ============================================================================
# DISCORD OBJECT FIXTURES - WEBHOOKS
# ============================================================================

@pytest.fixture
def mock_webhook():
    """Standard webhook for testing."""
    webhook = AsyncMock(spec=discord.Webhook)
    webhook.id = 333444555666777888
    webhook.name = "Test Webhook"
    webhook.token = "webhook_token_abc123xyz"
    webhook.url = "https://discord.com/api/webhooks/333444555666777888/webhook_token_abc123xyz"
    webhook.channel_id = 123456789012345678
    webhook.guild_id = 987654321098765432
    webhook.avatar = None
    webhook.created_at = datetime(2025, 12, 23, 10, 0, 0, tzinfo=timezone.utc)
    
    # Methods
    webhook.send = AsyncMock()
    webhook.edit = AsyncMock()
    webhook.delete = AsyncMock()
    
    return webhook


# ============================================================================
# DISCORD OBJECT FIXTURES - THREADS
# ============================================================================

@pytest.fixture
def mock_thread():
    """Standard thread for testing."""
    thread = AsyncMock(spec=discord.Thread)
    thread.id = 444555666777888999
    thread.name = "Test Thread"
    thread.parent_id = 123456789012345678
    thread.owner_id = 111222333444555666
    thread.guild = None
    thread.archived = False
    thread.locked = False
    thread.auto_archive_duration = 1440
    thread.archive_timestamp = None
    thread.created_at = datetime(2025, 12, 23, 10, 0, 0, tzinfo=timezone.utc)
    
    # Methods
    thread.send = AsyncMock()
    thread.edit = AsyncMock()
    thread.delete = AsyncMock()
    thread.add_user = AsyncMock()
    thread.remove_user = AsyncMock()
    
    return thread


# ============================================================================
# ERROR SIMULATION FIXTURES
# ============================================================================

@pytest.fixture
def mock_discord_errors():
    """Factory for Discord error responses.
    
    Returns function that creates Discord API errors for testing error handling.
    
    Usage:
        error = mock_discord_errors("not_found")
        client.fetch_guild.side_effect = error
    """
    def create_error(error_type: str):
        """Create specific Discord API error."""
        mock_response = Mock()
        mock_response.status = 404
        mock_response.reason = "Not Found"
        
        errors = {
            "not_found": discord.NotFound(mock_response, "Not found"),
            "forbidden": discord.Forbidden(mock_response, "Forbidden"),
            "rate_limit": discord.HTTPException(mock_response, "Rate limited"),
            "invalid_data": discord.InvalidData("Invalid data"),
            "bad_request": discord.HTTPException(mock_response, "Bad request"),
        }
        return errors.get(error_type, ValueError(f"Unknown error type: {error_type}"))
    
    return create_error


# ============================================================================
# COMFYUI FIXTURES
# ============================================================================

@pytest.fixture
def mock_comfyui_client():
    """Mocked ComfyUI HTTP client for testing image generation."""
    with patch('httpx.AsyncClient') as mock_client_class:
        client = AsyncMock()
        
        # POST endpoint (queue prompt)
        client.post = AsyncMock()
        client.post.return_value.status_code = 200
        client.post.return_value.json.return_value = {
            "prompt_id": "test_job_123",
            "number": 1
        }
        
        # GET endpoint (check status)
        client.get = AsyncMock()
        client.get.return_value.status_code = 200
        client.get.return_value.json.return_value = {
            "status": "complete",
            "outputs": {
                "images": [
                    {
                        "filename": "test_image.png",
                        "subfolder": "",
                        "type": "output"
                    }
                ]
            }
        }
        
        # WebSocket connection
        client.ws_connect = AsyncMock()
        
        mock_client_class.return_value.__aenter__.return_value = client
        mock_client_class.return_value.__aexit__.return_value = AsyncMock()
        
        yield client


@pytest.fixture
def mock_comfyui_workflow():
    """Standard ComfyUI workflow for testing.
    
    Returns minimal but valid workflow structure.
    """
    return {
        "workflow": {
            "nodes": [
                {
                    "id": 1,
                    "type": "CLIPTextEncode",
                    "inputs": {"text": "{{prompt}}"},  # Template for prompt injection
                    "outputs": ["CONDITIONING"]
                },
                {
                    "id": 2,
                    "type": "KSampler",
                    "inputs": {
                        "seed": "{{seed}}",  # Template for seed injection
                        "steps": "{{steps}}",  # Template for steps injection
                        "cfg": 7.0,
                        "sampler_name": "euler",
                        "scheduler": "normal"
                    }
                },
                {
                    "id": 3,
                    "type": "SaveImage",
                    "inputs": {"filename_prefix": "guildmaster_"}
                }
            ]
        },
        "metadata": {
            "name": "test_workflow",
            "description": "Test workflow for unit tests",
            "dimensions": "512x512"
        }
    }


# ============================================================================
# THEMING FIXTURES
# ============================================================================

@pytest.fixture
def generic_theme():
    """Generic theme configuration for testing."""
    from discord_guildmaster_mcp.theming.generic import GenericTheme
    return GenericTheme()


@pytest.fixture
def wow_theme():
    """WoW theme configuration for testing."""
    from discord_guildmaster_mcp.theming.wow import WoWTheme
    return WoWTheme()


# ============================================================================
# UTILITY FIXTURES
# ============================================================================

@pytest.fixture
def mock_datetime_now():
    """Fixed datetime for testing time-dependent behavior."""
    fixed_time = datetime(2025, 12, 23, 12, 0, 0, tzinfo=timezone.utc)
    with patch('datetime.datetime') as mock_dt:
        mock_dt.now.return_value = fixed_time
        mock_dt.utcnow.return_value = fixed_time
        yield fixed_time


@pytest.fixture
def sample_audit_log_entries():
    """Sample audit log entries for testing."""
    return [
        {
            "id": "1234567890",
            "action_type": "MEMBER_KICK",
            "user_id": "111222333444555666",
            "target_id": "999888777666555444",
            "reason": "Spamming recruitment channel",
            "timestamp": "2025-12-23T10:15:00Z",
            "moderator": {
                "id": "111222333444555666",
                "name": "OfficerName#1234"
            },
            "target": {
                "id": "999888777666555444",
                "name": "SpammerName#5678"
            }
        }
    ]


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests (fast, mocked)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests (slower, may require external services)"
    )
    config.addinivalue_line(
        "markers", "comfyui: Tests requiring ComfyUI server"
    )
    config.addinivalue_line(
        "markers", "slow: Known slow tests"
    )


# ============================================================================
# ASYNC TEST SUPPORT
# ============================================================================

# pytest-asyncio is required for async tests
# All async test functions should use @pytest.mark.asyncio decorator

