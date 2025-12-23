"""
Factory functions for creating test Discord objects.

Provides convenient functions to create mock Discord objects with sensible
defaults, reducing boilerplate in tests.

Phase: DDD Phase 2 - Test Suite Implementation
Generated: 2025-12-23
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock
import discord


# ============================================================================
# DISCORD OBJECT FACTORIES
# ============================================================================

class DiscordFactory:
    """Factory for creating mock Discord objects with realistic defaults."""
    
    @staticmethod
    def create_guild(
        guild_id: str = "987654321098765432",
        name: str = "Test Guild",
        member_count: int = 100,
        **kwargs
    ) -> AsyncMock:
        """Create a mock guild with sensible defaults.
        
        Args:
            guild_id: Guild ID (snowflake)
            name: Guild name
            member_count: Number of members
            **kwargs: Override any guild attributes
        
        Returns:
            AsyncMock guild object
        """
        guild = AsyncMock(spec=discord.Guild)
        guild.id = int(guild_id)
        guild.name = name
        guild.member_count = member_count
        guild.description = kwargs.get("description", f"Test guild: {name}")
        guild.max_members = kwargs.get("max_members", 500)
        guild.owner_id = kwargs.get("owner_id", 123456789012345678)
        guild.verification_level = kwargs.get(
            "verification_level",
            discord.VerificationLevel.medium
        )
        guild.created_at = kwargs.get(
            "created_at",
            datetime(2023, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
        )
        
        # Icon
        guild.icon = MagicMock()
        guild.icon.url = kwargs.get(
            "icon_url",
            f"https://cdn.discordapp.com/icons/{guild_id}/test.png"
        )
        
        # Features
        guild.features = kwargs.get("features", ["COMMUNITY", "THREADS"])
        
        # Collections (empty by default, populated by tests)
        guild.channels = kwargs.get("channels", [])
        guild.roles = kwargs.get("roles", [])
        guild.members = kwargs.get("members", [])
        guild.emojis = kwargs.get("emojis", [])
        
        # Methods
        guild.fetch_member = AsyncMock()
        guild.fetch_channel = AsyncMock()
        guild.fetch_roles = AsyncMock(return_value=guild.roles)
        guild.create_role = AsyncMock()
        guild.create_text_channel = AsyncMock()
        guild.create_voice_channel = AsyncMock()
        guild.create_category = AsyncMock()
        
        return guild
    
    @staticmethod
    def create_member(
        user_id: str = "111222333444555666",
        name: str = "TestUser",
        discriminator: str = "1234",
        display_name: Optional[str] = None,
        **kwargs
    ) -> AsyncMock:
        """Create a mock member with sensible defaults.
        
        Args:
            user_id: User ID (snowflake)
            name: Username
            discriminator: User discriminator
            display_name: Display name/nickname
            **kwargs: Override any member attributes
        
        Returns:
            AsyncMock member object
        """
        member = AsyncMock(spec=discord.Member)
        member.id = int(user_id)
        member.name = name
        member.discriminator = discriminator
        member.display_name = display_name or name
        member.nick = kwargs.get("nick", display_name)
        member.bot = kwargs.get("bot", False)
        
        # Timestamps
        member.joined_at = kwargs.get(
            "joined_at",
            datetime(2023, 6, 15, 10, 0, 0, tzinfo=timezone.utc)
        )
        member.created_at = kwargs.get(
            "created_at",
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        )
        
        # Avatar
        member.avatar = MagicMock()
        member.avatar.url = kwargs.get(
            "avatar_url",
            f"https://cdn.discordapp.com/avatars/{user_id}/test.png"
        )
        
        # Status and activities
        member.status = kwargs.get("status", discord.Status.online)
        member.activities = kwargs.get("activities", [])
        
        # Roles and permissions
        member.roles = kwargs.get("roles", [])
        member.top_role = kwargs.get("top_role", None)
        member.guild_permissions = kwargs.get(
            "guild_permissions",
            discord.Permissions.none()
        )
        
        # Methods
        member.add_roles = AsyncMock()
        member.remove_roles = AsyncMock()
        member.edit = AsyncMock()
        member.kick = AsyncMock()
        member.ban = AsyncMock()
        member.send = AsyncMock()
        
        return member
    
    @staticmethod
    def create_role(
        role_id: str = "777888999000111222",
        name: str = "Member",
        color: Optional[discord.Color] = None,
        position: int = 1,
        **kwargs
    ) -> MagicMock:
        """Create a mock role with sensible defaults.
        
        Args:
            role_id: Role ID (snowflake)
            name: Role name
            color: Role color
            position: Role position in hierarchy
            **kwargs: Override any role attributes
        
        Returns:
            MagicMock role object
        """
        role = MagicMock(spec=discord.Role)
        role.id = int(role_id)
        role.name = name
        role.color = color or discord.Color.default()
        role.position = position
        
        # Permissions
        role.permissions = kwargs.get(
            "permissions",
            discord.Permissions(view_channel=True, send_messages=True)
        )
        
        # Flags
        role.mentionable = kwargs.get("mentionable", False)
        role.hoist = kwargs.get("hoist", False)
        role.managed = kwargs.get("managed", False)
        
        # Timestamps
        role.created_at = kwargs.get(
            "created_at",
            datetime(2023, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        )
        
        # Methods
        role.edit = AsyncMock()
        role.delete = AsyncMock()
        
        return role
    
    @staticmethod
    def create_text_channel(
        channel_id: str = "123456789012345678",
        name: str = "general",
        **kwargs
    ) -> AsyncMock:
        """Create a mock text channel with sensible defaults."""
        channel = AsyncMock(spec=discord.TextChannel)
        channel.id = int(channel_id)
        channel.name = name
        channel.guild = kwargs.get("guild", None)
        channel.position = kwargs.get("position", 0)
        channel.category_id = kwargs.get("category_id", None)
        channel.topic = kwargs.get("topic", None)
        channel.nsfw = kwargs.get("nsfw", False)
        channel.slowmode_delay = kwargs.get("slowmode_delay", 0)
        channel.created_at = kwargs.get(
            "created_at",
            datetime(2023, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        )
        
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
    
    @staticmethod
    def create_voice_channel(
        channel_id: str = "234567890123456789",
        name: str = "General Voice",
        **kwargs
    ) -> AsyncMock:
        """Create a mock voice channel with sensible defaults."""
        channel = AsyncMock(spec=discord.VoiceChannel)
        channel.id = int(channel_id)
        channel.name = name
        channel.guild = kwargs.get("guild", None)
        channel.position = kwargs.get("position", 0)
        channel.category_id = kwargs.get("category_id", None)
        channel.bitrate = kwargs.get("bitrate", 64000)
        channel.user_limit = kwargs.get("user_limit", 0)
        channel.created_at = kwargs.get(
            "created_at",
            datetime(2023, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        )
        
        channel.edit = AsyncMock()
        channel.delete = AsyncMock()
        
        return channel
    
    @staticmethod
    def create_category(
        category_id: str = "345678901234567890",
        name: str = "Guild Channels",
        **kwargs
    ) -> AsyncMock:
        """Create a mock category channel with sensible defaults."""
        category = AsyncMock(spec=discord.CategoryChannel)
        category.id = int(category_id)
        category.name = name
        category.guild = kwargs.get("guild", None)
        category.position = kwargs.get("position", 0)
        category.created_at = kwargs.get(
            "created_at",
            datetime(2023, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        )
        category.channels = kwargs.get("channels", [])
        
        category.edit = AsyncMock()
        category.delete = AsyncMock()
        category.create_text_channel = AsyncMock()
        category.create_voice_channel = AsyncMock()
        
        return category
    
    @staticmethod
    def create_forum_channel(
        channel_id: str = "456789012345678901",
        name: str = "guild-discussion",
        **kwargs
    ) -> AsyncMock:
        """Create a mock forum channel with sensible defaults."""
        channel = AsyncMock(spec=discord.ForumChannel)
        channel.id = int(channel_id)
        channel.name = name
        channel.guild = kwargs.get("guild", None)
        channel.position = kwargs.get("position", 0)
        channel.category_id = kwargs.get("category_id", None)
        channel.topic = kwargs.get("topic", None)
        channel.created_at = kwargs.get(
            "created_at",
            datetime(2023, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        )
        channel.default_auto_archive_duration = kwargs.get("auto_archive_duration", 1440)
        channel.available_tags = kwargs.get("tags", [])
        
        channel.create_thread = AsyncMock()
        channel.archived_threads = AsyncMock()
        
        return channel
    
    @staticmethod
    def create_message(
        message_id: str = "222333444555666777",
        content: str = "Test message",
        author: Optional[Any] = None,
        channel: Optional[Any] = None,
        **kwargs
    ) -> AsyncMock:
        """Create a mock message with sensible defaults."""
        message = AsyncMock(spec=discord.Message)
        message.id = int(message_id)
        message.content = content
        message.author = author
        message.channel = channel
        message.guild = kwargs.get("guild", None)
        message.created_at = kwargs.get(
            "created_at",
            datetime(2025, 12, 23, 10, 0, 0, tzinfo=timezone.utc)
        )
        message.edited_at = kwargs.get("edited_at", None)
        message.embeds = kwargs.get("embeds", [])
        message.attachments = kwargs.get("attachments", [])
        message.reactions = kwargs.get("reactions", [])
        message.pinned = kwargs.get("pinned", False)
        message.mention_everyone = kwargs.get("mention_everyone", False)
        message.mentions = kwargs.get("mentions", [])
        message.role_mentions = kwargs.get("role_mentions", [])
        
        # Methods
        message.edit = AsyncMock()
        message.delete = AsyncMock()
        message.add_reaction = AsyncMock()
        message.remove_reaction = AsyncMock()
        message.pin = AsyncMock()
        message.unpin = AsyncMock()
        message.reply = AsyncMock()
        
        return message
    
    @staticmethod
    def create_webhook(
        webhook_id: str = "333444555666777888",
        name: str = "Test Webhook",
        channel_id: str = "123456789012345678",
        **kwargs
    ) -> AsyncMock:
        """Create a mock webhook with sensible defaults."""
        webhook = AsyncMock(spec=discord.Webhook)
        webhook.id = int(webhook_id)
        webhook.name = name
        webhook.token = kwargs.get("token", "webhook_token_abc123xyz")
        webhook.url = kwargs.get(
            "url",
            f"https://discord.com/api/webhooks/{webhook_id}/{webhook.token}"
        )
        webhook.channel_id = int(channel_id)
        webhook.guild_id = kwargs.get("guild_id", 987654321098765432)
        webhook.avatar = kwargs.get("avatar", None)
        webhook.created_at = kwargs.get(
            "created_at",
            datetime(2025, 12, 23, 10, 0, 0, tzinfo=timezone.utc)
        )
        
        # Methods
        webhook.send = AsyncMock()
        webhook.edit = AsyncMock()
        webhook.delete = AsyncMock()
        
        return webhook
    
    @staticmethod
    def create_thread(
        thread_id: str = "444555666777888999",
        name: str = "Test Thread",
        parent_id: str = "123456789012345678",
        **kwargs
    ) -> AsyncMock:
        """Create a mock thread with sensible defaults."""
        thread = AsyncMock(spec=discord.Thread)
        thread.id = int(thread_id)
        thread.name = name
        thread.parent_id = int(parent_id)
        thread.owner_id = kwargs.get("owner_id", 111222333444555666)
        thread.guild = kwargs.get("guild", None)
        thread.archived = kwargs.get("archived", False)
        thread.locked = kwargs.get("locked", False)
        thread.auto_archive_duration = kwargs.get("auto_archive_duration", 1440)
        thread.archive_timestamp = kwargs.get("archive_timestamp", None)
        thread.created_at = kwargs.get(
            "created_at",
            datetime(2025, 12, 23, 10, 0, 0, tzinfo=timezone.utc)
        )
        
        # Methods
        thread.send = AsyncMock()
        thread.edit = AsyncMock()
        thread.delete = AsyncMock()
        thread.add_user = AsyncMock()
        thread.remove_user = AsyncMock()
        
        return thread


# ============================================================================
# BATCH FACTORIES
# ============================================================================

class BatchFactory:
    """Factory for creating collections of objects."""
    
    @staticmethod
    def create_members(count: int, **kwargs) -> List[AsyncMock]:
        """Create multiple members with incrementing IDs."""
        members = []
        base_id = int(kwargs.get("base_id", "111111111111111111"))
        
        for i in range(count):
            member = DiscordFactory.create_member(
                user_id=str(base_id + i),
                name=f"User{i}",
                display_name=f"User {i}",
                **kwargs
            )
            members.append(member)
        
        return members
    
    @staticmethod
    def create_roles(count: int, **kwargs) -> List[MagicMock]:
        """Create multiple roles with incrementing IDs and positions."""
        roles = []
        base_id = int(kwargs.get("base_id", "777777777777777777"))
        
        for i in range(count):
            role = DiscordFactory.create_role(
                role_id=str(base_id + i),
                name=f"Role{i}",
                position=i,
                **kwargs
            )
            roles.append(role)
        
        return roles
    
    @staticmethod
    def create_channels(count: int, channel_type: str = "text", **kwargs) -> List[AsyncMock]:
        """Create multiple channels with incrementing IDs."""
        channels = []
        base_id = int(kwargs.get("base_id", "123123123123123123"))
        
        for i in range(count):
            if channel_type == "text":
                channel = DiscordFactory.create_text_channel(
                    channel_id=str(base_id + i),
                    name=f"channel-{i}",
                    **kwargs
                )
            elif channel_type == "voice":
                channel = DiscordFactory.create_voice_channel(
                    channel_id=str(base_id + i),
                    name=f"Voice {i}",
                    **kwargs
                )
            elif channel_type == "category":
                channel = DiscordFactory.create_category(
                    category_id=str(base_id + i),
                    name=f"Category {i}",
                    **kwargs
                )
            elif channel_type == "forum":
                channel = DiscordFactory.create_forum_channel(
                    channel_id=str(base_id + i),
                    name=f"forum-{i}",
                    **kwargs
                )
            else:
                raise ValueError(f"Unknown channel type: {channel_type}")
            
            channels.append(channel)
        
        return channels
    
    @staticmethod
    def create_messages(count: int, **kwargs) -> List[AsyncMock]:
        """Create multiple messages with incrementing IDs."""
        messages = []
        base_id = int(kwargs.get("base_id", "222222222222222222"))
        
        for i in range(count):
            message = DiscordFactory.create_message(
                message_id=str(base_id + i),
                content=f"Message {i}",
                **kwargs
            )
            messages.append(message)
        
        return messages


# ============================================================================
# COMFYUI FACTORIES
# ============================================================================

class ComfyUIFactory:
    """Factory for creating ComfyUI-related test data."""
    
    @staticmethod
    def create_workflow(
        name: str = "test_workflow",
        dimensions: str = "512x512",
        **kwargs
    ) -> Dict[str, Any]:
        """Create a ComfyUI workflow for testing."""
        return {
            "workflow": {
                "nodes": kwargs.get("nodes", [
                    {
                        "id": 1,
                        "type": "CLIPTextEncode",
                        "inputs": {"text": "{{prompt}}"}
                    },
                    {
                        "id": 2,
                        "type": "KSampler",
                        "inputs": {
                            "seed": "{{seed}}",
                            "steps": "{{steps}}",
                            "cfg": 7.0
                        }
                    }
                ])
            },
            "metadata": {
                "name": name,
                "description": kwargs.get("description", f"Test workflow: {name}"),
                "dimensions": dimensions
            }
        }
    
    @staticmethod
    def create_generation_response(
        status: str = "complete",
        job_id: str = "test_job_123",
        **kwargs
    ) -> Dict[str, Any]:
        """Create a ComfyUI generation response."""
        response = {
            "job_id": job_id,
            "status": status
        }
        
        if status == "complete":
            response.update({
                "image_url": kwargs.get(
                    "image_url",
                    "http://localhost:8188/view/test_image.png"
                ),
                "seed": kwargs.get("seed", 42),
                "workflow": kwargs.get("workflow", "test_workflow"),
                "duration_seconds": kwargs.get("duration", 30.5)
            })
        elif status == "failed":
            response["error"] = kwargs.get("error", "Generation failed")
        elif status == "processing":
            response["progress"] = kwargs.get("progress", 50)
        
        return response


# ============================================================================
# ERROR FACTORIES
# ============================================================================

class ErrorFactory:
    """Factory for creating error responses."""
    
    @staticmethod
    def create_not_found_error(resource_type: str = "Resource") -> discord.NotFound:
        """Create a NotFound error."""
        from unittest.mock import Mock
        mock_response = Mock()
        mock_response.status = 404
        mock_response.reason = "Not Found"
        return discord.NotFound(mock_response, f"{resource_type} not found")
    
    @staticmethod
    def create_forbidden_error(action: str = "perform this action") -> discord.Forbidden:
        """Create a Forbidden error."""
        from unittest.mock import Mock
        mock_response = Mock()
        mock_response.status = 403
        mock_response.reason = "Forbidden"
        return discord.Forbidden(mock_response, f"Missing permission to {action}")
    
    @staticmethod
    def create_http_exception(message: str = "HTTP error") -> discord.HTTPException:
        """Create an HTTPException."""
        from unittest.mock import Mock
        mock_response = Mock()
        mock_response.status = 500
        mock_response.reason = "Internal Server Error"
        return discord.HTTPException(mock_response, message)


