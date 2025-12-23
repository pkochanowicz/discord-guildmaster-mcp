<!-- Generated: 2025-12-23 | DDD Phase 1: Documentation Genesis -->

# Tools Reference

Complete documentation for all 33 tools in Discord Guildmaster MCP. Each tool includes parameter schemas, return structures, usage examples, and agent-specific considerations.

---

## Table of Contents

1. [Guild Information](#guild-information) (2 tools)
2. [Member Management](#member-management) (4 tools)
3. [Role Operations](#role-operations) (3 tools)
4. [Channel Management](#channel-management) (4 tools)
5. [Messaging](#messaging) (5 tools)
6. [Webhook Management](#webhook-management) (3 tools)
7. [Forum Support](#forum-support) (3 tools)
8. [Thread Management](#thread-management) (2 tools)
9. [ComfyUI Integration](#comfyui-integration) (4 tools)
10. [Utility](#utility) (3 tools)

---

## Tool Documentation Format

Each tool is documented with:

- **Purpose**  What the tool does (optimized for LLM comprehension)
- **Parameters**  JSON schema with types, requirements, descriptions
- **Returns**  Structured response schema with examples
- **Usage Example**  Practical code example
- **Agent Considerations**  Token efficiency, safety hints, best practices

**Legend:**
- = **Read-only**  Safe for automated execution
-   **Destructive**  Modifies or deletes data
- =¡ **Token-efficient**  Pre-filtered, paginated responses

---

## Guild Information

### 1. get_guild_info

**Purpose:** Retrieve guild (server) metadata including member count, features, and configuration.

**Hints:** = Read-only | =¡ Token-efficient

**Parameters:**

```json
{
  "guild_id": {
    "type": "string",
    "required": false,
    "description": "Guild ID. Optional if DISCORD_DEFAULT_GUILD_ID is set."
  }
}
```

**Returns:**

```json
{
  "id": "987654321098765432",
  "name": "Azeroth Bound",
  "description": "World of Warcraft Classic+ guild",
  "member_count": 127,
  "max_members": 500,
  "features": ["COMMUNITY", "THREADS", "ROLE_ICONS"],
  "owner_id": "123456789012345678",
  "created_at": "2023-01-15T10:30:00Z",
  "icon_url": "https://cdn.discordapp.com/icons/...",
  "verification_level": "MEDIUM"
}
```

**Usage Example:**

```python
# With default guild ID configured
result = get_guild_info()
print(f"Guild: {result['name']} ({result['member_count']} members)")

# Explicit guild ID
result = get_guild_info(guild_id="987654321098765432")
```

**Agent Considerations:**
- Use to establish context about guild before operations
- Response is compact (< 500 tokens)
- Cache guild name/ID for subsequent tool calls

---

### 2. get_audit_log

**Purpose:** Retrieve recent administrative actions (channel creation, role changes, member kicks) from guild audit log.

**Hints:** = Read-only | =¡ Token-efficient (paginated)

**Parameters:**

```json
{
  "guild_id": {
    "type": "string",
    "required": false
  },
  "limit": {
    "type": "integer",
    "required": false,
    "default": 50,
    "description": "Maximum entries to retrieve (1-100)"
  },
  "action_type": {
    "type": "string",
    "required": false,
    "description": "Filter by action: MEMBER_KICK, MEMBER_BAN, CHANNEL_CREATE, ROLE_UPDATE, etc."
  },
  "user_id": {
    "type": "string",
    "required": false,
    "description": "Filter by user who performed action"
  }
}
```

**Returns:**

```json
{
  "guild_id": "987654321098765432",
  "entries": [
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
  ],
  "total_entries": 1,
  "has_more": false
}
```

**Usage Example:**

```python
# Get recent moderation actions
log = get_audit_log(action_type="MEMBER_KICK", limit=10)

# Review all actions by specific moderator
log = get_audit_log(user_id="111222333444555666", limit=25)
```

**Agent Considerations:**
- Use `limit` to control token usage
- Filter by `action_type` to focus on relevant events
- Useful for moderation oversight and compliance audits

---

## Member Management

### 3. list_members

**Purpose:** List guild members with optional role filtering and pagination.

**Hints:** = Read-only | =¡ Token-efficient (paginated, pre-filtered)

**Parameters:**

```json
{
  "guild_id": {
    "type": "string",
    "required": false
  },
  "limit": {
    "type": "integer",
    "required": false,
    "default": 50,
    "description": "Maximum members to return (1-1000)"
  },
  "role_id": {
    "type": "string",
    "required": false,
    "description": "Filter members by role ID"
  },
  "after": {
    "type": "string",
    "required": false,
    "description": "User ID for pagination (fetch members after this ID)"
  }
}
```

**Returns:**

```json
{
  "guild_id": "987654321098765432",
  "members": [
    {
      "id": "123456789012345678",
      "username": "GuildMaster#0001",
      "display_name": "GM - Thaldrin",
      "joined_at": "2023-01-15T12:00:00Z",
      "roles": ["Officer", "Raid Leader"],
      "top_role": {
        "id": "111111111111111111",
        "name": "Officer",
        "color": "#FF0000"
      },
      "status": "online",
      "avatar_url": "https://cdn.discordapp.com/avatars/..."
    }
  ],
  "total_fetched": 50,
  "has_more": true,
  "next_after": "987654321098765432"
}
```

**Usage Example:**

```python
# Get first 50 members
members = list_members(limit=50)

# Filter by role (e.g., "Officers")
officers = list_members(role_id="111111111111111111", limit=100)

# Pagination (fetch next page)
next_page = list_members(limit=50, after=members["next_after"])
```

**Agent Considerations:**
- Default `limit=50` balances context vs completeness
- Use `role_id` filter to reduce token usage
- `has_more=true` indicates pagination needed
- Response excludes bot users automatically

---

### 4. get_member

**Purpose:** Get detailed information about a specific guild member.

**Hints:** = Read-only

**Parameters:**

```json
{
  "guild_id": {
    "type": "string",
    "required": false
  },
  "user_id": {
    "type": "string",
    "required": true,
    "description": "Discord user ID"
  }
}
```

**Returns:**

```json
{
  "id": "123456789012345678",
  "username": "GuildMaster#0001",
  "display_name": "GM - Thaldrin",
  "discriminator": "0001",
  "avatar_url": "https://cdn.discordapp.com/avatars/...",
  "joined_at": "2023-01-15T12:00:00Z",
  "created_at": "2020-05-10T08:00:00Z",
  "roles": [
    {
      "id": "111111111111111111",
      "name": "Officer",
      "color": "#FF0000",
      "position": 5
    }
  ],
  "top_role": {
    "id": "111111111111111111",
    "name": "Officer"
  },
  "status": "online",
  "activities": ["Playing World of Warcraft"],
  "permissions": ["ADMINISTRATOR"]
}
```

**Usage Example:**

```python
# Get member details
member = get_member(user_id="123456789012345678")
print(f"{member['display_name']} joined {member['joined_at']}")

# Check member's roles
if any(role['name'] == 'Officer' for role in member['roles']):
    print("This member is an officer")
```

**Agent Considerations:**
- Use when you need full member details (not just summary)
- Includes permission information for authorization checks
- Activity/status may be empty if presence intent disabled

---

### 5. search_members

**Purpose:** Search guild members by name, nickname, or role.

**Hints:** = Read-only | =¡ Token-efficient (pre-filtered)

**Parameters:**

```json
{
  "guild_id": {
    "type": "string",
    "required": false
  },
  "query": {
    "type": "string",
    "required": true,
    "description": "Search term (matches username, display name, nickname)"
  },
  "limit": {
    "type": "integer",
    "required": false,
    "default": 25
  }
}
```

**Returns:**

```json
{
  "guild_id": "987654321098765432",
  "query": "thal",
  "results": [
    {
      "id": "123456789012345678",
      "username": "GuildMaster#0001",
      "display_name": "GM - Thaldrin",
      "nickname": "Thaldrin",
      "match_type": "nickname",
      "roles": ["Officer", "Raid Leader"]
    }
  ],
  "total_results": 1
}
```

**Usage Example:**

```python
# Search for member by name
results = search_members(query="thal")

# Search with specific limit
results = search_members(query="officer", limit=10)
```

**Agent Considerations:**
- Case-insensitive fuzzy matching
- Searches username, display_name, and nickname fields
- `match_type` indicates which field matched
- Useful for natural language queries ("find the member named...")

---

### 6. get_user_id_by_name

**Purpose:** Convert human-readable username/nickname to Discord user ID and mention format.

**Hints:** = Read-only

**Parameters:**

```json
{
  "guild_id": {
    "type": "string",
    "required": false
  },
  "name": {
    "type": "string",
    "required": true,
    "description": "Username or display name to look up"
  }
}
```

**Returns:**

```json
{
  "guild_id": "987654321098765432",
  "query": "Thaldrin",
  "user_id": "123456789012345678",
  "mention": "<@123456789012345678>",
  "username": "GuildMaster#0001",
  "display_name": "GM - Thaldrin"
}
```

**Usage Example:**

```python
# Get user ID for mention
user = get_user_id_by_name(name="Thaldrin")
send_message(
    channel_id="...",
    content=f"Welcome {user['mention']} to the guild!"
)
```

**Agent Considerations:**
- Bridges natural language ("ping Thaldrin") to Discord API
- Returns `mention` format ready for message content
- Returns `null` if user not found (handle gracefully)

---

## Role Operations

### 7. list_roles

**Purpose:** List all roles in guild with hierarchy and permissions summary.

**Hints:** = Read-only | =¡ Token-efficient

**Parameters:**

```json
{
  "guild_id": {
    "type": "string",
    "required": false
  }
}
```

**Returns:**

```json
{
  "guild_id": "987654321098765432",
  "roles": [
    {
      "id": "111111111111111111",
      "name": "Officer",
      "color": "#FF0000",
      "position": 5,
      "permissions": ["ADMINISTRATOR"],
      "mentionable": true,
      "hoisted": true,
      "member_count": 12
    },
    {
      "id": "222222222222222222",
      "name": "Member",
      "color": "#00FF00",
      "position": 1,
      "permissions": ["SEND_MESSAGES", "VIEW_CHANNEL"],
      "mentionable": false,
      "hoisted": false,
      "member_count": 115
    }
  ],
  "total_roles": 2
}
```

**Usage Example:**

```python
# Get all roles
roles = list_roles()

# Find role by name
officer_role = next(r for r in roles['roles'] if r['name'] == 'Officer')
print(f"Officer role ID: {officer_role['id']}")
```

**Agent Considerations:**
- Roles sorted by `position` (highest first)
- `hoisted=true` means role displayed separately in member list
- `member_count` useful for understanding role distribution
- Use for role selection in multi-step workflows

---

### 8. assign_role

**Purpose:** Assign a role to a guild member.

**Hints:**   Destructive | Requires Manage Roles permission

**Parameters:**

```json
{
  "guild_id": {
    "type": "string",
    "required": false
  },
  "user_id": {
    "type": "string",
    "required": true
  },
  "role_id": {
    "type": "string",
    "required": true
  },
  "reason": {
    "type": "string",
    "required": false,
    "description": "Audit log reason"
  }
}
```

**Returns:**

```json
{
  "success": true,
  "guild_id": "987654321098765432",
  "user_id": "123456789012345678",
  "role_id": "111111111111111111",
  "role_name": "Officer",
  "message": "Role 'Officer' assigned to user successfully"
}
```

**Usage Example:**

```python
# Assign officer role
result = assign_role(
    user_id="123456789012345678",
    role_id="111111111111111111",
    reason="Promoted for exceptional guild contribution"
)
```

**Agent Considerations:**
- **Requires confirmation** for automated workflows
- Check bot has permission higher than role being assigned
- `reason` populates audit log (best practice)
- Idempotent (assigning twice has no effect)

---

### 9. remove_role

**Purpose:** Remove a role from a guild member.

**Hints:**   Destructive | Requires Manage Roles permission

**Parameters:**

```json
{
  "guild_id": {
    "type": "string",
    "required": false
  },
  "user_id": {
    "type": "string",
    "required": true
  },
  "role_id": {
    "type": "string",
    "required": true
  },
  "reason": {
    "type": "string",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "guild_id": "987654321098765432",
  "user_id": "123456789012345678",
  "role_id": "111111111111111111",
  "role_name": "Officer",
  "message": "Role 'Officer' removed from user successfully"
}
```

**Usage Example:**

```python
# Remove role with audit reason
result = remove_role(
    user_id="123456789012345678",
    role_id="111111111111111111",
    reason="Stepping down from officer position"
)
```

**Agent Considerations:**
- **Requires confirmation** for automated workflows
- Idempotent (removing twice has no effect)
- Use `reason` for audit trail

---

## Channel Management

### 10. list_channels

**Purpose:** List all channels in guild organized by categories.

**Hints:** = Read-only | =¡ Token-efficient

**Parameters:**

```json
{
  "guild_id": {
    "type": "string",
    "required": false
  },
  "type": {
    "type": "string",
    "required": false,
    "description": "Filter by type: text, voice, category, announcement, forum, thread"
  }
}
```

**Returns:**

```json
{
  "guild_id": "987654321098765432",
  "categories": [
    {
      "id": "111111111111111111",
      "name": "Guild Management",
      "position": 0,
      "channels": [
        {
          "id": "222222222222222222",
          "name": "announcements",
          "type": "announcement",
          "position": 0,
          "topic": "Important guild announcements",
          "nsfw": false
        },
        {
          "id": "333333333333333333",
          "name": "officer-chat",
          "type": "text",
          "position": 1,
          "topic": "Officer-only discussion",
          "nsfw": false
        }
      ]
    }
  ],
  "uncategorized": [],
  "total_channels": 2
}
```

**Usage Example:**

```python
# Get all channels
channels = list_channels()

# Get only text channels
text_channels = list_channels(type="text")

# Find channel by name
announcements = next(
    ch for cat in channels['categories']
    for ch in cat['channels']
    if ch['name'] == 'announcements'
)
```

**Agent Considerations:**
- Organized by category for better context
- Use `type` filter to reduce response size
- Includes `topic` for channel descriptions
- Useful for channel discovery in multi-step workflows

---

### 11. create_channel

**Purpose:** Create a new text channel with optional category placement.

**Hints:**   Destructive | Requires Manage Channels permission

**Parameters:**

```json
{
  "guild_id": {
    "type": "string",
    "required": false
  },
  "name": {
    "type": "string",
    "required": true,
    "description": "Channel name (lowercase, hyphens, no spaces)"
  },
  "type": {
    "type": "string",
    "required": false,
    "default": "text",
    "description": "Channel type: text, announcement, voice"
  },
  "category_id": {
    "type": "string",
    "required": false,
    "description": "Parent category ID"
  },
  "topic": {
    "type": "string",
    "required": false,
    "description": "Channel topic/description"
  },
  "nsfw": {
    "type": "boolean",
    "required": false,
    "default": false
  },
  "reason": {
    "type": "string",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "channel": {
    "id": "444444444444444444",
    "name": "event-planning",
    "type": "text",
    "category_id": "111111111111111111",
    "topic": "Plan upcoming guild events",
    "position": 3,
    "created_at": "2025-12-23T10:30:00Z"
  },
  "message": "Channel 'event-planning' created successfully"
}
```

**Usage Example:**

```python
# Create simple text channel
channel = create_channel(
    name="event-planning",
    topic="Plan upcoming guild events"
)

# Create channel in specific category
channel = create_channel(
    name="raid-strategy",
    category_id="111111111111111111",
    topic="Discuss raid tactics and strategies",
    reason="Requested by raid leader"
)
```

**Agent Considerations:**
- **Requires confirmation** for automated workflows
- Channel names automatically converted to lowercase with hyphens
- Returns channel ID for immediate use
- Consider using `category_id` for organization

---

### 12. delete_channel

**Purpose:** Delete a channel permanently.

**Hints:**   Destructive | Requires Manage Channels permission

**Parameters:**

```json
{
  "channel_id": {
    "type": "string",
    "required": true
  },
  "reason": {
    "type": "string",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "channel_id": "444444444444444444",
  "message": "Channel deleted successfully"
}
```

**Usage Example:**

```python
# Delete channel with audit reason
result = delete_channel(
    channel_id="444444444444444444",
    reason="Event concluded, channel no longer needed"
)
```

**Agent Considerations:**
- **Requires explicit confirmation**  this is permanent
- Cannot be undone
- Deletes all messages in channel
- Always provide `reason` for audit trail

---

### 13. create_category

**Purpose:** Create a channel category for organizing channels.

**Hints:**   Destructive | Requires Manage Channels permission

**Parameters:**

```json
{
  "guild_id": {
    "type": "string",
    "required": false
  },
  "name": {
    "type": "string",
    "required": true
  },
  "position": {
    "type": "integer",
    "required": false,
    "description": "Position in channel list (0 = top)"
  },
  "reason": {
    "type": "string",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "category": {
    "id": "555555555555555555",
    "name": "EVENTS",
    "type": "category",
    "position": 2,
    "created_at": "2025-12-23T10:45:00Z"
  },
  "message": "Category 'EVENTS' created successfully"
}
```

**Usage Example:**

```python
# Create category for events
category = create_category(
    name="EVENTS",
    position=2,
    reason="Organizing event channels"
)

# Use category ID for subsequent channel creation
event_channel = create_channel(
    name="raid-night",
    category_id=category['category']['id']
)
```

**Agent Considerations:**
- Categories conventionally use UPPERCASE names
- Use `position` to control display order
- Returns category ID for organizing channels

---

## Messaging

### 14. send_message

**Purpose:** Send a message to a channel with optional embed support.

**Hints:**   Destructive (creates content) | Requires Send Messages permission

**Parameters:**

```json
{
  "channel_id": {
    "type": "string",
    "required": false,
    "description": "Optional if DISCORD_DEFAULT_CHANNEL_ID is set"
  },
  "content": {
    "type": "string",
    "required": false,
    "description": "Message text content (max 2000 characters)"
  },
  "embed": {
    "type": "object",
    "required": false,
    "description": "Embedded rich content"
  },
  "tts": {
    "type": "boolean",
    "required": false,
    "default": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "message": {
    "id": "666666666666666666",
    "channel_id": "222222222222222222",
    "content": "Guild meeting tonight at 8 PM server time!",
    "timestamp": "2025-12-23T10:50:00Z",
    "author": {
      "id": "bot_user_id",
      "username": "Guildmaster MCP"
    }
  }
}
```

**Usage Example:**

```python
# Simple text message
msg = send_message(
    channel_id="222222222222222222",
    content="Guild meeting tonight at 8 PM server time!"
)

# Rich embed message
msg = send_message(
    channel_id="222222222222222222",
    embed={
        "title": "Raid Night Signup",
        "description": "Sign up for tonight's raid!",
        "color": 0xFF0000,
        "fields": [
            {"name": "Time", "value": "8:00 PM Server Time", "inline": True},
            {"name": "Raid", "value": "Molten Core", "inline": True}
        ],
        "footer": {"text": "React with  to sign up"}
    }
)
```

**Agent Considerations:**
- Combine `content` and `embed` for rich messages
- Content limited to 2000 characters
- Embed structure: `title`, `description`, `color`, `fields`, `footer`, `image`, `thumbnail`
- Returns message ID for subsequent operations (reactions, deletions)

---

### 15. read_messages

**Purpose:** Read message history from a channel with pagination.

**Hints:** = Read-only | =¡ Token-efficient (paginated)

**Parameters:**

```json
{
  "channel_id": {
    "type": "string",
    "required": false
  },
  "limit": {
    "type": "integer",
    "required": false,
    "default": 50,
    "description": "Number of messages to retrieve (1-100)"
  },
  "before": {
    "type": "string",
    "required": false,
    "description": "Message ID - get messages before this ID"
  },
  "after": {
    "type": "string",
    "required": false,
    "description": "Message ID - get messages after this ID"
  }
}
```

**Returns:**

```json
{
  "channel_id": "222222222222222222",
  "messages": [
    {
      "id": "777777777777777777",
      "author": {
        "id": "123456789012345678",
        "username": "GuildMaster#0001",
        "display_name": "GM - Thaldrin"
      },
      "content": "Everyone ready for raid tonight?",
      "timestamp": "2025-12-23T10:55:00Z",
      "edited_timestamp": null,
      "mentions": [],
      "attachments": [],
      "reactions": [
        {"emoji": "", "count": 12}
      ]
    }
  ],
  "total_fetched": 1,
  "oldest_message_id": "777777777777777777",
  "newest_message_id": "777777777777777777"
}
```

**Usage Example:**

```python
# Get recent messages
messages = read_messages(channel_id="222222222222222222", limit=50)

# Pagination - get older messages
older = read_messages(
    channel_id="222222222222222222",
    limit=50,
    before=messages['oldest_message_id']
)

# Get messages after specific point
newer = read_messages(
    channel_id="222222222222222222",
    after="777777777777777777"
)
```

**Agent Considerations:**
- **Essential for context-aware agents** (analyze chat sentiment, answer questions)
- Use `limit` to control token usage
- Messages returned in reverse chronological order (newest first)
- `before`/`after` for pagination
- Response excludes message embeds to save tokens (use `get_message` for full content)

---

### 16. delete_message

**Purpose:** Delete a message from a channel.

**Hints:**   Destructive | Requires Manage Messages permission

**Parameters:**

```json
{
  "channel_id": {
    "type": "string",
    "required": true
  },
  "message_id": {
    "type": "string",
    "required": true
  },
  "reason": {
    "type": "string",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "channel_id": "222222222222222222",
  "message_id": "777777777777777777",
  "message": "Message deleted successfully"
}
```

**Usage Example:**

```python
# Delete message with audit reason
result = delete_message(
    channel_id="222222222222222222",
    message_id="777777777777777777",
    reason="Spam content removed"
)
```

**Agent Considerations:**
- **Requires confirmation** for automated moderation
- Cannot delete messages older than 14 days (Discord limitation)
- Provide `reason` for moderation transparency
- Consider bulk delete for cleanup (use webhooks/bulk operations)

---

### 17. add_reaction

**Purpose:** Add emoji reaction to a message.

**Hints:** = Read-only (non-destructive) | Requires Add Reactions permission

**Parameters:**

```json
{
  "channel_id": {
    "type": "string",
    "required": true
  },
  "message_id": {
    "type": "string",
    "required": true
  },
  "emoji": {
    "type": "string",
    "required": true,
    "description": "Unicode emoji or custom emoji ID"
  }
}
```

**Returns:**

```json
{
  "success": true,
  "channel_id": "222222222222222222",
  "message_id": "777777777777777777",
  "emoji": "",
  "message": "Reaction added successfully"
}
```

**Usage Example:**

```python
# Add unicode emoji
result = add_reaction(
    channel_id="222222222222222222",
    message_id="777777777777777777",
    emoji=""
)

# Add custom emoji (format: name:id)
result = add_reaction(
    channel_id="222222222222222222",
    message_id="777777777777777777",
    emoji="guildcrest:123456789012345678"
)
```

**Agent Considerations:**
- Useful for interactive workflows (e.g., "React  to sign up")
- Unicode emojis: ``, `L`, `”`, `<Æ`, etc.
- Custom emojis require format `name:id`
- Idempotent (adding twice has no effect)

---

### 18. send_dm

**Purpose:** Send a direct message to a user.

**Hints:**   Destructive (creates content) | Rate-limited by Discord

**Parameters:**

```json
{
  "user_id": {
    "type": "string",
    "required": true
  },
  "content": {
    "type": "string",
    "required": true
  },
  "embed": {
    "type": "object",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "user_id": "123456789012345678",
  "message": {
    "id": "888888888888888888",
    "content": "Welcome to the guild! Check out #rules for guidelines.",
    "timestamp": "2025-12-23T11:00:00Z"
  }
}
```

**Usage Example:**

```python
# Send welcome DM
result = send_dm(
    user_id="123456789012345678",
    content="Welcome to the guild! Check out #rules for guidelines."
)

# Send DM with embed
result = send_dm(
    user_id="123456789012345678",
    embed={
        "title": "Welcome to Azeroth Bound!",
        "description": "We're excited to have you join us.",
        "color": 0x00FF00
    }
)
```

**Agent Considerations:**
- **Use sparingly**  DMs can be intrusive
- Users can block DMs from bots (handle failures gracefully)
- Rate-limited to prevent spam
- Good for onboarding workflows and private notifications

---

## Webhook Management

### 19. create_webhook

**Purpose:** Create a webhook for custom identity messaging.

**Hints:**   Destructive | Requires Manage Webhooks permission

**Parameters:**

```json
{
  "channel_id": {
    "type": "string",
    "required": true
  },
  "name": {
    "type": "string",
    "required": true,
    "description": "Webhook display name"
  },
  "avatar_url": {
    "type": "string",
    "required": false,
    "description": "Webhook avatar image URL"
  },
  "reason": {
    "type": "string",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "webhook": {
    "id": "999999999999999999",
    "name": "Guild Herald",
    "channel_id": "222222222222222222",
    "token": "webhook_token_here",
    "url": "https://discord.com/api/webhooks/999999999999999999/webhook_token_here",
    "avatar_url": "https://example.com/herald-avatar.png"
  }
}
```

**Usage Example:**

```python
# Create webhook for announcements
webhook = create_webhook(
    channel_id="222222222222222222",
    name="Guild Herald",
    avatar_url="https://example.com/herald-avatar.png",
    reason="Automated announcements"
)

# Save webhook URL for later use
webhook_url = webhook['webhook']['url']
```

**Agent Considerations:**
- Webhooks enable custom sender identity (name + avatar)
- Store `webhook['url']` for subsequent `send_webhook_message` calls
- Each channel can have up to 10 webhooks
- Use for roleplay, automated announcements, or multi-identity messaging

---

### 20. send_webhook_message

**Purpose:** Send a message via webhook with custom name and avatar.

**Hints:**   Destructive (creates content)

**Parameters:**

```json
{
  "webhook_url": {
    "type": "string",
    "required": true,
    "description": "Webhook URL from create_webhook"
  },
  "content": {
    "type": "string",
    "required": false
  },
  "username": {
    "type": "string",
    "required": false,
    "description": "Override webhook default name"
  },
  "avatar_url": {
    "type": "string",
    "required": false,
    "description": "Override webhook default avatar"
  },
  "embed": {
    "type": "object",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "message": {
    "id": "101010101010101010",
    "channel_id": "222222222222222222",
    "content": "Hear ye, hear ye! Raid night begins in one hour!",
    "timestamp": "2025-12-23T11:05:00Z",
    "webhook_id": "999999999999999999"
  }
}
```

**Usage Example:**

```python
# Send message as custom identity
msg = send_webhook_message(
    webhook_url=webhook_url,
    username="Town Crier",
    avatar_url="https://example.com/crier-avatar.png",
    content="Hear ye, hear ye! Raid night begins in one hour!"
)

# Send rich embed via webhook
msg = send_webhook_message(
    webhook_url=webhook_url,
    username="Raid Coordinator",
    embed={
        "title": "Molten Core Raid",
        "description": "Starting in 1 hour!",
        "color": 0xFF4500
    }
)
```

**Agent Considerations:**
- Perfect for roleplay or multi-character narratives
- `username` and `avatar_url` override webhook defaults per message
- Combines well with ComfyUI (generate character portrait, use as avatar)
- No rate limit (unlike bot messages)

---

### 21. delete_webhook

**Purpose:** Delete a webhook permanently.

**Hints:**   Destructive | Requires Manage Webhooks permission

**Parameters:**

```json
{
  "webhook_id": {
    "type": "string",
    "required": true
  },
  "reason": {
    "type": "string",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "webhook_id": "999999999999999999",
  "message": "Webhook deleted successfully"
}
```

**Usage Example:**

```python
# Delete webhook
result = delete_webhook(
    webhook_id="999999999999999999",
    reason="Automation no longer needed"
)
```

**Agent Considerations:**
- Permanent deletion (cannot be undone)
- Invalidates webhook URL immediately
- Clean up unused webhooks to avoid clutter

---

## Forum Support

### 22. create_forum_post

**Purpose:** Create a new forum post (thread) with optional tags.

**Hints:**   Destructive | Requires Create Posts permission in forum channels

**Parameters:**

```json
{
  "channel_id": {
    "type": "string",
    "required": true,
    "description": "Forum channel ID"
  },
  "title": {
    "type": "string",
    "required": true,
    "description": "Post title (max 100 characters)"
  },
  "content": {
    "type": "string",
    "required": true,
    "description": "Initial message content"
  },
  "tags": {
    "type": "array",
    "required": false,
    "description": "Array of tag IDs to apply"
  },
  "embed": {
    "type": "object",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "post": {
    "id": "111111111111111111",
    "channel_id": "222222222222222222",
    "title": "Tips for Leveling in Classic+",
    "author_id": "bot_user_id",
    "created_at": "2025-12-23T11:10:00Z",
    "tags": ["Guide", "Leveling"],
    "message_count": 1
  },
  "message": "Forum post created successfully"
}
```

**Usage Example:**

```python
# Create forum post with tags
post = create_forum_post(
    channel_id="222222222222222222",
    title="Tips for Leveling in Classic+",
    content="Here are some proven leveling strategies...",
    tags=["333333333333333333", "444444444444444444"]
)

# Create post with embed
post = create_forum_post(
    channel_id="222222222222222222",
    title="Raid Strategy Guide",
    content="Check out this comprehensive guide!",
    embed={
        "title": "Molten Core Boss Guide",
        "description": "Detailed tactics for each encounter",
        "color": 0xFF0000
    }
)
```

**Agent Considerations:**
- Modern Discord feature (not all servers have forums)
- `tags` array uses tag IDs from forum channel configuration
- Returns thread ID for subsequent replies
- Useful for knowledge base generation

---

### 23. reply_to_forum

**Purpose:** Reply to an existing forum post thread.

**Hints:**   Destructive | Requires Send Messages in Threads permission

**Parameters:**

```json
{
  "thread_id": {
    "type": "string",
    "required": true,
    "description": "Forum post thread ID"
  },
  "content": {
    "type": "string",
    "required": true
  },
  "embed": {
    "type": "object",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "message": {
    "id": "555555555555555555",
    "thread_id": "111111111111111111",
    "content": "Great tips! I'd also add that questing in groups speeds things up.",
    "timestamp": "2025-12-23T11:15:00Z"
  }
}
```

**Usage Example:**

```python
# Reply to forum post
reply = reply_to_forum(
    thread_id="111111111111111111",
    content="Great tips! I'd also add that questing in groups speeds things up."
)
```

**Agent Considerations:**
- Use for automated responses or summaries
- Can include embeds for rich content
- Respects thread archive status (fails if archived)

---

### 24. get_forum_post

**Purpose:** Retrieve forum post content and replies.

**Hints:** = Read-only | =¡ Token-efficient (paginated)

**Parameters:**

```json
{
  "thread_id": {
    "type": "string",
    "required": true
  },
  "limit": {
    "type": "integer",
    "required": false,
    "default": 50,
    "description": "Number of replies to retrieve"
  }
}
```

**Returns:**

```json
{
  "thread_id": "111111111111111111",
  "title": "Tips for Leveling in Classic+",
  "author": {
    "id": "123456789012345678",
    "username": "GuildMaster#0001"
  },
  "created_at": "2025-12-23T11:10:00Z",
  "tags": ["Guide", "Leveling"],
  "archived": false,
  "locked": false,
  "message_count": 12,
  "messages": [
    {
      "id": "666666666666666666",
      "author": {
        "id": "bot_user_id",
        "username": "Guildmaster MCP"
      },
      "content": "Here are some proven leveling strategies...",
      "timestamp": "2025-12-23T11:10:00Z"
    }
  ],
  "total_fetched": 12
}
```

**Usage Example:**

```python
# Get forum post with replies
post = get_forum_post(thread_id="111111111111111111", limit=50)

# Summarize discussion
summary = f"Thread '{post['title']}' has {post['message_count']} replies"
```

**Agent Considerations:**
- Useful for context gathering before replying
- `limit` controls reply pagination
- Includes thread metadata (archived, locked, tags)

---

## Thread Management

### 25. create_thread

**Purpose:** Create a thread from an existing message or as standalone thread.

**Hints:**   Destructive | Requires Create Threads permission

**Parameters:**

```json
{
  "channel_id": {
    "type": "string",
    "required": true
  },
  "name": {
    "type": "string",
    "required": true,
    "description": "Thread name (max 100 characters)"
  },
  "message_id": {
    "type": "string",
    "required": false,
    "description": "Message ID to create thread from (optional)"
  },
  "auto_archive_duration": {
    "type": "integer",
    "required": false,
    "default": 1440,
    "description": "Minutes until auto-archive: 60, 1440, 4320, 10080"
  },
  "reason": {
    "type": "string",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "thread": {
    "id": "777777777777777777",
    "name": "Raid Comp Discussion",
    "channel_id": "222222222222222222",
    "owner_id": "bot_user_id",
    "created_at": "2025-12-23T11:20:00Z",
    "auto_archive_duration": 1440,
    "archived": false
  }
}
```

**Usage Example:**

```python
# Create thread from message
thread = create_thread(
    channel_id="222222222222222222",
    message_id="888888888888888888",
    name="Raid Comp Discussion",
    auto_archive_duration=1440
)

# Create standalone thread
thread = create_thread(
    channel_id="222222222222222222",
    name="Event Planning Thread",
    auto_archive_duration=4320,
    reason="Organizing next guild event"
)
```

**Agent Considerations:**
- Threads keep discussions organized without channel clutter
- `auto_archive_duration` options: 60 (1 hour), 1440 (1 day), 4320 (3 days), 10080 (1 week)
- Returns thread ID for subsequent messaging
- Threads auto-archive after inactivity period

---

### 26. archive_thread

**Purpose:** Archive a thread to clean up discussions.

**Hints:**   Destructive | Requires Manage Threads permission

**Parameters:**

```json
{
  "thread_id": {
    "type": "string",
    "required": true
  },
  "reason": {
    "type": "string",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "thread_id": "777777777777777777",
  "message": "Thread archived successfully"
}
```

**Usage Example:**

```python
# Archive completed discussion
result = archive_thread(
    thread_id="777777777777777777",
    reason="Discussion concluded"
)
```

**Agent Considerations:**
- Archived threads hidden from active channel view
- Can be unarchived by posting new message (if not locked)
- Use for cleanup workflows

---

## ComfyUI Integration

### 27. generate_image

**Purpose:** Generate an image using ComfyUI workflow with text prompt.

**Hints:**   Slow operation (1-5 minutes) | Requires ComfyUI server

**Parameters:**

```json
{
  "workflow": {
    "type": "string",
    "required": true,
    "description": "Workflow name or path (e.g., 'portrait', 'banner', 'custom.json')"
  },
  "prompt": {
    "type": "string",
    "required": true,
    "description": "Text prompt for image generation"
  },
  "negative_prompt": {
    "type": "string",
    "required": false,
    "default": "low quality, blurry, distorted"
  },
  "seed": {
    "type": "integer",
    "required": false,
    "description": "Random seed (omit for random)"
  },
  "steps": {
    "type": "integer",
    "required": false,
    "description": "Sampling steps (workflow default if omitted)"
  }
}
```

**Returns:**

```json
{
  "success": true,
  "generation_id": "abc123xyz",
  "status": "queued",
  "workflow": "portrait",
  "prompt": "Female night elf druid with silver hair",
  "estimated_time": 120,
  "message": "Generation started. Use get_generation_status to check progress."
}
```

**Usage Example:**

```python
# Generate character portrait
gen = generate_image(
    workflow="portrait",
    prompt="Female night elf druid with silver hair, wise expression, forest background"
)

# Generate event banner
banner = generate_image(
    workflow="banner",
    prompt="Epic raid announcement, Molten Core, fiery background",
    negative_prompt="low quality, text, watermark"
)

# Custom workflow with fixed seed
custom = generate_image(
    workflow="custom-style.json",
    prompt="Guild crest with phoenix emblem",
    seed=42
)
```

**Agent Considerations:**
- **Asynchronous operation**  returns immediately, generation happens in background
- Use `get_generation_status` to poll completion
- Preset workflows: `portrait`, `banner`, `recruitment`, `emblem`
- Custom workflows: filename in `COMFYUI_WORKFLOW_DIR`
- Generation time varies: 30s (SD 1.5) to 5min (SDXL)

---

### 28. list_workflows

**Purpose:** List available ComfyUI workflows (presets + custom).

**Hints:** = Read-only

**Parameters:**

```json
{}
```

**Returns:**

```json
{
  "workflows": [
    {
      "name": "portrait",
      "path": "portrait.json",
      "description": "512×768 character portraits",
      "type": "preset"
    },
    {
      "name": "banner",
      "path": "banner.json",
      "description": "1200×400 event banners",
      "type": "preset"
    },
    {
      "name": "custom-fantasy",
      "path": "custom-fantasy.json",
      "description": "User-provided workflow",
      "type": "custom"
    }
  ],
  "total_workflows": 3
}
```

**Usage Example:**

```python
# Discover available workflows
workflows = list_workflows()

# Present options to user
for wf in workflows['workflows']:
    print(f"{wf['name']}: {wf['description']}")
```

**Agent Considerations:**
- Use for workflow discovery in interactive flows
- `type="preset"` indicates curated workflows
- `type="custom"` indicates user-provided BYOW workflows

---

### 29. get_generation_status

**Purpose:** Check status and progress of image generation.

**Hints:** = Read-only | Poll every 5-10 seconds

**Parameters:**

```json
{
  "generation_id": {
    "type": "string",
    "required": true,
    "description": "Generation ID from generate_image"
  }
}
```

**Returns:**

```json
{
  "generation_id": "abc123xyz",
  "status": "completed",
  "progress": 100,
  "workflow": "portrait",
  "prompt": "Female night elf druid with silver hair",
  "started_at": "2025-12-23T11:25:00Z",
  "completed_at": "2025-12-23T11:27:30Z",
  "elapsed_time": 150,
  "image_ready": true
}
```

**Status values:**
- `queued`  Waiting in ComfyUI queue
- `processing`  Currently generating
- `completed`  Generation finished, image ready
- `failed`  Generation failed (see `error` field)

**Usage Example:**

```python
import time

# Start generation
gen = generate_image(workflow="portrait", prompt="...")

# Poll until complete
while True:
    status = get_generation_status(generation_id=gen['generation_id'])

    if status['status'] == 'completed':
        break
    elif status['status'] == 'failed':
        print(f"Generation failed: {status.get('error')}")
        break

    print(f"Progress: {status['progress']}%")
    time.sleep(5)

# Get image
image = get_image(generation_id=gen['generation_id'])
```

**Agent Considerations:**
- **Poll, don't block**  use async patterns for multi-agent workflows
- `progress` field estimates percentage (0-100)
- `image_ready=true` means you can call `get_image`

---

### 30. get_image

**Purpose:** Retrieve generated image (base64, URL, or CDN link based on config).

**Hints:** = Read-only

**Parameters:**

```json
{
  "generation_id": {
    "type": "string",
    "required": true
  }
}
```

**Returns (COMFYUI_RETURN_MODE=base64):**

```json
{
  "generation_id": "abc123xyz",
  "status": "completed",
  "image": {
    "format": "base64",
    "data": "/9j/4AAQSkZJRgABAQAA...",
    "content_type": "image/png",
    "size_bytes": 245678
  },
  "metadata": {
    "workflow": "portrait",
    "prompt": "Female night elf druid...",
    "dimensions": {"width": 512, "height": 768},
    "seed": 42
  }
}
```

**Returns (COMFYUI_RETURN_MODE=url):**

```json
{
  "generation_id": "abc123xyz",
  "status": "completed",
  "image": {
    "format": "url",
    "url": "http://comfyui.example.com/output/abc123xyz.png",
    "content_type": "image/png"
  },
  "metadata": {...}
}
```

**Returns (COMFYUI_RETURN_MODE=cdn):**

```json
{
  "generation_id": "abc123xyz",
  "status": "completed",
  "image": {
    "format": "cdn",
    "url": "https://cdn.example.com/guild-images/abc123xyz.png",
    "content_type": "image/png",
    "cdn_provider": "s3"
  },
  "metadata": {...}
}
```

**Usage Example:**

```python
# Get image after generation completes
image = get_image(generation_id="abc123xyz")

# Use in Discord message
if image['image']['format'] == 'base64':
    # Upload to Discord
    send_message(
        channel_id="...",
        content="Check out this character portrait!",
        # Discord.py will handle base64 attachment
    )
elif image['image']['format'] == 'url':
    # Embed URL
    send_message(
        channel_id="...",
        embed={
            "title": "Character Portrait",
            "image": {"url": image['image']['url']}
        }
    )
```

**Agent Considerations:**
- `format` indicates return mode (base64, url, cdn)
- Base64 increases token usage but works with localhost ComfyUI
- URL requires publicly accessible ComfyUI server
- CDN mode best for production (persistent, embeddable)
- `metadata` includes generation parameters for reference

---

## Utility

### 31. test_connection

**Purpose:** Verify Discord bot connectivity and permissions.

**Hints:** = Read-only | Diagnostic tool

**Parameters:**

```json
{
  "guild_id": {
    "type": "string",
    "required": false
  }
}
```

**Returns:**

```json
{
  "success": true,
  "bot": {
    "id": "bot_user_id",
    "username": "Guildmaster MCP#1234",
    "discriminator": "1234",
    "avatar_url": "https://cdn.discordapp.com/avatars/..."
  },
  "guild": {
    "id": "987654321098765432",
    "name": "Azeroth Bound",
    "permissions": [
      "VIEW_CHANNEL",
      "SEND_MESSAGES",
      "MANAGE_CHANNELS",
      "MANAGE_ROLES",
      "MANAGE_WEBHOOKS"
    ]
  },
  "latency_ms": 45,
  "message": "Connection successful"
}
```

**Usage Example:**

```python
# Test connection on startup
conn = test_connection()

if conn['success']:
    print(f"Connected as {conn['bot']['username']}")
    print(f"Guild: {conn['guild']['name']}")
else:
    print("Connection failed!")
```

**Agent Considerations:**
- Use in initialization workflows to verify setup
- `permissions` array shows bot's actual permissions
- `latency_ms` indicates connection quality
- Fails gracefully with error message if bot lacks permissions

---

### 32. test_comfyui

**Purpose:** Verify ComfyUI server connectivity and status.

**Hints:** = Read-only | Diagnostic tool

**Parameters:**

```json
{}
```

**Returns:**

```json
{
  "success": true,
  "server": {
    "host": "localhost",
    "port": 8188,
    "url": "http://localhost:8188",
    "reachable": true
  },
  "queue": {
    "pending": 2,
    "running": 1
  },
  "system": {
    "device": "cuda",
    "vram_total": "24GB",
    "vram_free": "18GB"
  },
  "message": "ComfyUI server operational"
}
```

**Usage Example:**

```python
# Test ComfyUI before generation
comfy = test_comfyui()

if comfy['success']:
    print(f"ComfyUI online ({comfy['queue']['pending']} jobs queued)")
else:
    print("ComfyUI unavailable - image generation disabled")
```

**Agent Considerations:**
- Use before `generate_image` to avoid failures
- `queue` shows current load (useful for estimating wait time)
- `system` info helps debug GPU issues
- Returns graceful error if COMFYUI_ENABLED=false

---

### 33. list_available_tools

**Purpose:** Dynamic tool discovery for agents (returns all available tools with schemas).

**Hints:** = Read-only | Agent initialization

**Parameters:**

```json
{
  "category": {
    "type": "string",
    "required": false,
    "description": "Filter by category: guild, member, role, channel, message, webhook, forum, thread, comfyui, utility"
  }
}
```

**Returns:**

```json
{
  "total_tools": 33,
  "categories": {
    "guild": 2,
    "member": 4,
    "role": 3,
    "channel": 4,
    "message": 5,
    "webhook": 3,
    "forum": 3,
    "thread": 2,
    "comfyui": 4,
    "utility": 3
  },
  "tools": [
    {
      "name": "get_guild_info",
      "category": "guild",
      "description": "Retrieve guild metadata",
      "parameters": {...},
      "hints": ["readOnlyHint"],
      "token_cost_estimate": "low"
    }
  ]
}
```

**Usage Example:**

```python
# Get all tools
all_tools = list_available_tools()

# Get only messaging tools
msg_tools = list_available_tools(category="message")

# Agent initialization
print(f"Agent has access to {all_tools['total_tools']} tools")
```

**Agent Considerations:**
- Use during agent initialization to establish capabilities
- `hints` array includes `readOnlyHint`, `destructiveHint`, `idempotentHint`
- `token_cost_estimate` helps agents choose efficient operations
- Filter by `category` to specialize agent roles

---

## Usage Patterns

### Multi-Agent Workflows

Example: Weekly officer briefing generation

```python
# Agent 1: Guild Info Gatherer
guild = get_guild_info()
members = list_members(role_id="officer_role_id")
audit = get_audit_log(limit=100)

# Agent 2: Content Analyzer
messages = read_messages(channel_id="officer_chat", limit=200)
# ... analyze sentiment, extract action items

# Agent 3: Visual Designer
banner = generate_image(
    workflow="banner",
    prompt="Weekly officer briefing header, professional, guild colors"
)

# Agent 4: Publisher
webhook = create_webhook(channel_id="briefings", name="Briefing Bot")
send_webhook_message(
    webhook_url=webhook['webhook']['url'],
    username="Weekly Briefing",
    embed={
        "title": f"Officer Briefing - Week of {date}",
        "description": "...",
        "image": {"url": get_image(banner['generation_id'])['image']['url']}
    }
)
```

### Token Efficiency Best Practices

```python
#  GOOD: Use defaults, pagination, filtering
members = list_members(limit=50, role_id="officer_role_id")

# L BAD: Fetch everything, filter in-memory
all_members = list_members(limit=1000)
officers = [m for m in all_members if 'Officer' in m['roles']]

#  GOOD: Pre-filtered audit log
kicks = get_audit_log(action_type="MEMBER_KICK", limit=25)

# L BAD: Fetch all actions, filter client-side
all_actions = get_audit_log(limit=100)
kicks = [a for a in all_actions if a['action_type'] == 'MEMBER_KICK']
```

---

<div align="center">

**All 33 tools documented. Command your Discord realm with precision. ”**

</div>
