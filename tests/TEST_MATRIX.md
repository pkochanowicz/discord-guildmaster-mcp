# Test Matrix - Documentation Promise Mapping

**Purpose**: Maps every documented feature in discord-guildmaster-mcp to specific test requirements.

**Source**: docs/TOOLS_REFERENCE.md, docs/CONFIGURATION.md, docs/architecture.md  
**Coverage Target**: 100% of documented features have corresponding tests  
**Generated**: 2025-12-23  
**Phase**: DDD Phase 2 - Test Suite Implementation

---

## Testing Methodology

Every documented feature represents a **promise** to users. Every test validates that promise is kept.

**Test Categories Per Tool:**
1. ✅ **Happy Path** - Basic functionality works as documented
2. ⚠️ **Error Handling** - Documented failure modes handled correctly
3. 🔍 **Edge Cases** - Boundary conditions, special values, empty states
4. 🔗 **Integration** - Tool interacts correctly with Discord API and system

---

## Tool Test Matrix

### Group 1: Guild Information (2 tools)

#### Tool #1: get_guild_info
**Documentation Promise**: docs/TOOLS_REFERENCE.md:43-93  
**Purpose**: Retrieve guild metadata including member count, features, and configuration

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns guild info with all documented fields (id, name, member_count, features, etc.)
  - [ ] Works with default guild_id from config
  - [ ] Works with explicit guild_id parameter
  - [ ] Response schema matches documentation exactly
  - [ ] Token usage < 500 tokens as documented

- ⚠️ Error Handling
  - [ ] Invalid guild_id raises ValueError with clear message
  - [ ] Non-existent guild raises NotFound error
  - [ ] Missing permissions raises PermissionError
  - [ ] Bot not in guild raises appropriate error

- 🔍 Edge Cases
  - [ ] Empty guild (0 members) - should not occur but handle gracefully
  - [ ] Guild with maximum features enabled
  - [ ] Guild with no icon (null icon_url)
  - [ ] Newly created guild (minimal data)

- 🔗 Integration
  - [ ] Respects DISCORD_DEFAULT_GUILD_ID from configuration
  - [ ] Works with theme layer (generic/wow/custom)
  - [ ] Caches appropriately for subsequent calls

**Test File**: tests/tools/test_guild.py::TestGetGuildInfo

---

#### Tool #2: get_audit_log
**Documentation Promise**: docs/TOOLS_REFERENCE.md:96-171  
**Purpose**: Retrieve recent administrative actions with filtering and pagination

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns audit log entries with all documented fields
  - [ ] Default limit=50 works correctly
  - [ ] Custom limit (1-100) works correctly
  - [ ] action_type filter works (MEMBER_KICK, MEMBER_BAN, CHANNEL_CREATE, etc.)
  - [ ] user_id filter works
  - [ ] Pagination: has_more=true when more entries exist
  - [ ] Response schema matches documentation

- ⚠️ Error Handling
  - [ ] Invalid limit (0, -1, 101, non-integer) raises ValueError
  - [ ] Invalid action_type raises ValueError
  - [ ] Invalid user_id format raises ValueError
  - [ ] Missing VIEW_AUDIT_LOG permission raises PermissionError
  - [ ] Guild not found raises NotFound error

- 🔍 Edge Cases
  - [ ] Empty audit log (no entries) returns empty array
  - [ ] Audit log with exactly limit entries
  - [ ] Audit log with < limit entries (has_more=false)
  - [ ] Multiple filters combined (action_type + user_id)
  - [ ] Special characters in reason field

- 🔗 Integration
  - [ ] Works with default guild_id from config
  - [ ] Entries sorted by timestamp (newest first)
  - [ ] moderator and target objects populated correctly

**Test File**: tests/tools/test_guild.py::TestGetAuditLog

---

### Group 2: Member Management (4 tools)

#### Tool #3: list_members
**Documentation Promise**: docs/TOOLS_REFERENCE.md:176-254  
**Purpose**: List guild members with role filtering and pagination

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns member list with all documented fields
  - [ ] Default limit=50 works
  - [ ] Custom limit (1-1000) works
  - [ ] role_id filter works correctly
  - [ ] Pagination: after parameter works
  - [ ] has_more flag accurate
  - [ ] next_after provided when has_more=true
  - [ ] Bot users excluded automatically as documented

- ⚠️ Error Handling
  - [ ] Invalid limit (0, -1, 1001) raises ValueError
  - [ ] Invalid role_id format raises ValueError
  - [ ] Missing GUILD_MEMBERS intent raises PermissionError
  - [ ] Invalid after user_id handled gracefully

- 🔍 Edge Cases
  - [ ] Guild with 0 members (empty results)
  - [ ] Guild with exactly 50 members
  - [ ] Guild with 1000+ members (pagination required)
  - [ ] Member with no roles (only @everyone)
  - [ ] Member with offline status
  - [ ] Member with no avatar (default avatar)

- 🔗 Integration
  - [ ] Respects default guild_id
  - [ ] Token usage controlled by limit as documented
  - [ ] top_role calculated correctly from role hierarchy

**Test File**: tests/tools/test_members.py::TestListMembers

---

#### Tool #4: get_member
**Documentation Promise**: docs/TOOLS_REFERENCE.md:257-324  
**Purpose**: Get detailed information about specific guild member

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns complete member details with all fields
  - [ ] user_id (required) parameter validated
  - [ ] guild_id optional, uses default from config
  - [ ] Roles array populated with full role objects
  - [ ] top_role calculated correctly
  - [ ] permissions array accurate
  - [ ] activities populated (if presence intent enabled)

- ⚠️ Error Handling
  - [ ] Missing user_id raises ValueError
  - [ ] Invalid user_id format raises ValueError
  - [ ] User not in guild raises NotFound error
  - [ ] Missing permissions raises PermissionError

- 🔍 Edge Cases
  - [ ] Member with no roles (only @everyone)
  - [ ] Member with ADMINISTRATOR permission
  - [ ] Member with no activities
  - [ ] Member with empty status (offline)
  - [ ] Newly joined member (minimal data)

- 🔗 Integration
  - [ ] Permissions array reflects actual Discord permissions
  - [ ] Status/activities empty if presence intent disabled (documented behavior)

**Test File**: tests/tools/test_members.py::TestGetMember

---

#### Tool #5: search_members
**Documentation Promise**: docs/TOOLS_REFERENCE.md:327-389  
**Purpose**: Search guild members by name, nickname, or role

**Test Requirements**:
- ✅ Happy Path
  - [ ] Case-insensitive fuzzy matching works
  - [ ] Searches username field
  - [ ] Searches display_name field
  - [ ] Searches nickname field
  - [ ] match_type indicates which field matched
  - [ ] Default limit=25 works
  - [ ] Custom limit works
  - [ ] Returns up to limit results

- ⚠️ Error Handling
  - [ ] Empty query string raises ValueError
  - [ ] Invalid limit raises ValueError
  - [ ] Query with special characters handled safely
  - [ ] Very long query (> 100 chars) handled

- 🔍 Edge Cases
  - [ ] No matches returns empty results (not error)
  - [ ] Query matches multiple fields (username + nickname)
  - [ ] Query matches > limit members (returns first limit)
  - [ ] Query with only whitespace
  - [ ] Unicode/emoji in query
  - [ ] Partial name matches work

- 🔗 Integration
  - [ ] Token-efficient: pre-filtered results only
  - [ ] Natural language queries work as documented

**Test File**: tests/tools/test_members.py::TestSearchMembers

---

#### Tool #6: get_user_id_by_name
**Documentation Promise**: docs/TOOLS_REFERENCE.md:392-442  
**Purpose**: Convert human-readable username/nickname to Discord user ID and mention format

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns user_id for valid username
  - [ ] Returns user_id for valid display_name
  - [ ] Returns user_id for valid nickname
  - [ ] Returns mention format as documented (<@userid>)
  - [ ] Returns username and display_name in response

- ⚠️ Error Handling
  - [ ] User not found returns null (not error) as documented
  - [ ] Empty name raises ValueError
  - [ ] Invalid name format handled gracefully

- 🔍 Edge Cases
  - [ ] Multiple members with similar names (returns first match)
  - [ ] Name with special characters
  - [ ] Name with Unicode/emoji
  - [ ] Case insensitive matching

- 🔗 Integration
  - [ ] Mention format ready for send_message as documented
  - [ ] Bridges natural language to Discord API

**Test File**: tests/tools/test_members.py::TestGetUserIdByName

---

### Group 3: Role Operations (3 tools)

#### Tool #7: list_roles
**Documentation Promise**: docs/TOOLS_REFERENCE.md:447-511  
**Purpose**: List all roles in guild with hierarchy and permissions summary

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns all roles in guild
  - [ ] Roles sorted by position (hierarchy)
  - [ ] Each role has id, name, color, position, permissions
  - [ ] mentionable and hoisted flags accurate
  - [ ] member_count populated for each role
  - [ ] Token-efficient response as documented

- ⚠️ Error Handling
  - [ ] Invalid guild_id raises error
  - [ ] Missing permissions raises PermissionError

- 🔍 Edge Cases
  - [ ] Guild with only @everyone role
  - [ ] Guild with maximum roles (250)
  - [ ] Role with no color (default)
  - [ ] Role with ADMINISTRATOR permission
  - [ ] Role with 0 members

- 🔗 Integration
  - [ ] Position indicates hierarchy correctly
  - [ ] Permissions array format matches Discord API

**Test File**: tests/tools/test_roles.py::TestListRoles

---

#### Tool #8: assign_role
**Documentation Promise**: docs/TOOLS_REFERENCE.md:514-573  
**Purpose**: Assign role to guild member (⚠️ DESTRUCTIVE)

**Test Requirements**:
- ✅ Happy Path
  - [ ] Successfully assigns role to member
  - [ ] Returns success=true with member_id and role_id
  - [ ] Works with default guild_id
  - [ ] Works with explicit guild_id
  - [ ] Member can have multiple roles

- ⚠️ Error Handling
  - [ ] Missing required user_id raises ValueError
  - [ ] Missing required role_id raises ValueError
  - [ ] Invalid user_id format raises ValueError
  - [ ] Invalid role_id format raises ValueError
  - [ ] User not in guild raises NotFound error
  - [ ] Role not in guild raises NotFound error
  - [ ] Missing MANAGE_ROLES permission raises PermissionError
  - [ ] Bot role below target role raises PermissionError (hierarchy)
  - [ ] Attempting to assign @everyone raises error

- 🔍 Edge Cases
  - [ ] Assigning role member already has (idempotent - no error)
  - [ ] Assigning role to member with maximum roles
  - [ ] Assigning managed role (integration role) fails appropriately

- 🔗 Integration
  - [ ] Role hierarchy respected (bot can't assign higher roles)
  - [ ] Audit log entry created

**Test File**: tests/tools/test_roles.py::TestAssignRole

---

#### Tool #9: remove_role
**Documentation Promise**: docs/TOOLS_REFERENCE.md:576-635  
**Purpose**: Remove role from guild member (⚠️ DESTRUCTIVE)

**Test Requirements**:
- ✅ Happy Path
  - [ ] Successfully removes role from member
  - [ ] Returns success=true with member_id and role_id
  - [ ] Works with default guild_id
  - [ ] Works with explicit guild_id

- ⚠️ Error Handling
  - [ ] Missing required user_id raises ValueError
  - [ ] Missing required role_id raises ValueError
  - [ ] Invalid IDs raise ValueError
  - [ ] User not in guild raises NotFound error
  - [ ] Role not in guild raises NotFound error
  - [ ] Missing MANAGE_ROLES permission raises PermissionError
  - [ ] Bot role below target role raises PermissionError
  - [ ] Attempting to remove @everyone raises error

- 🔍 Edge Cases
  - [ ] Removing role member doesn't have (idempotent - no error)
  - [ ] Removing last role from member
  - [ ] Removing managed role fails appropriately

- 🔗 Integration
  - [ ] Role hierarchy respected
  - [ ] Audit log entry created

**Test File**: tests/tools/test_roles.py::TestRemoveRole

---

### Group 4: Channel Management (4 tools)

#### Tool #10: list_channels
**Documentation Promise**: docs/TOOLS_REFERENCE.md:638-717  
**Purpose**: List all channels in guild organized by type

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns channels organized by type (text, voice, category, forum, thread, stage)
  - [ ] Each channel has id, name, type, position, parent_id
  - [ ] Permission_overwrites populated
  - [ ] Topic included for text channels
  - [ ] Token-efficient response as documented

- ⚠️ Error Handling
  - [ ] Invalid guild_id raises error
  - [ ] Missing permissions raises PermissionError

- 🔍 Edge Cases
  - [ ] Guild with no channels (only system channels)
  - [ ] Guild with maximum channels
  - [ ] Channel with no topic
  - [ ] Channel with no parent (top-level)
  - [ ] Channel with complex permission overwrites
  - [ ] Archived threads handling

- 🔗 Integration
  - [ ] Channels grouped by type as documented
  - [ ] Position indicates sort order

**Test File**: tests/tools/test_channels.py::TestListChannels

---

#### Tool #11: create_channel
**Documentation Promise**: docs/TOOLS_REFERENCE.md:720-808  
**Purpose**: Create new text, voice, or announcement channel (⚠️ DESTRUCTIVE)

**Test Requirements**:
- ✅ Happy Path
  - [ ] Creates text channel successfully
  - [ ] Creates voice channel successfully
  - [ ] Creates announcement channel successfully
  - [ ] Required name parameter works
  - [ ] Optional type parameter works (defaults to text)
  - [ ] Optional parent_id (category) works
  - [ ] Optional topic works
  - [ ] Optional permission_overwrites works
  - [ ] Returns complete channel object

- ⚠️ Error Handling
  - [ ] Missing name raises ValueError
  - [ ] Empty name raises ValueError
  - [ ] Invalid name (special chars, > 100 chars) raises ValueError
  - [ ] Invalid type raises ValueError
  - [ ] Invalid parent_id raises NotFound error
  - [ ] Missing MANAGE_CHANNELS permission raises PermissionError
  - [ ] Guild at channel limit raises error

- 🔍 Edge Cases
  - [ ] Channel name with allowed special chars (-, _)
  - [ ] Channel name 1 char (minimum)
  - [ ] Channel name 100 chars (maximum)
  - [ ] Creating channel in category
  - [ ] Creating channel with no parent
  - [ ] Permission overwrites for specific roles/users

- 🔗 Integration
  - [ ] Channel appears in list_channels immediately
  - [ ] Audit log entry created
  - [ ] Parent category relationship established

**Test File**: tests/tools/test_channels.py::TestCreateChannel

---

#### Tool #12: delete_channel
**Documentation Promise**: docs/TOOLS_REFERENCE.md:811-857  
**Purpose**: Delete channel from guild (⚠️ DESTRUCTIVE - PERMANENT)

**Test Requirements**:
- ✅ Happy Path
  - [ ] Successfully deletes channel
  - [ ] Returns success=true with channel_id and name
  - [ ] Works with any channel type

- ⚠️ Error Handling
  - [ ] Missing channel_id raises ValueError
  - [ ] Invalid channel_id raises ValueError
  - [ ] Channel not found raises NotFound error
  - [ ] Missing MANAGE_CHANNELS permission raises PermissionError
  - [ ] Cannot delete community required channels (rules, updates)

- 🔍 Edge Cases
  - [ ] Deleting channel with active messages
  - [ ] Deleting channel with webhooks (webhooks deleted too)
  - [ ] Deleting parent category (children moved to no category)
  - [ ] Deleting thread parent (threads deleted)

- 🔗 Integration
  - [ ] Channel removed from list_channels immediately
  - [ ] Audit log entry created
  - [ ] All messages in channel deleted (permanent)

**Test File**: tests/tools/test_channels.py::TestDeleteChannel

---

#### Tool #13: create_category
**Documentation Promise**: docs/TOOLS_REFERENCE.md:860-929  
**Purpose**: Create channel category for organization (⚠️ DESTRUCTIVE)

**Test Requirements**:
- ✅ Happy Path
  - [ ] Successfully creates category
  - [ ] Required name parameter works
  - [ ] Optional permission_overwrites works
  - [ ] Returns complete category object with type="category"

- ⚠️ Error Handling
  - [ ] Missing name raises ValueError
  - [ ] Empty name raises ValueError
  - [ ] Invalid name raises ValueError
  - [ ] Missing MANAGE_CHANNELS permission raises PermissionError
  - [ ] Guild at category limit raises error

- 🔍 Edge Cases
  - [ ] Category name with special chars
  - [ ] Category with no channels
  - [ ] Category with maximum channels (50)
  - [ ] Permission overwrites inherited by child channels

- 🔗 Integration
  - [ ] Category appears in list_channels under "category" type
  - [ ] Can be used as parent_id for create_channel
  - [ ] Audit log entry created

**Test File**: tests/tools/test_channels.py::TestCreateCategory

---

### Group 5: Messaging (5 tools)

#### Tool #14: send_message
**Documentation Promise**: docs/TOOLS_REFERENCE.md:932-1013  
**Purpose**: Send message to Discord channel with optional embeds and formatting

**Test Requirements**:
- ✅ Happy Path
  - [ ] Sends simple text message successfully
  - [ ] channel_id optional if default configured
  - [ ] content parameter works (max 2000 chars)
  - [ ] Optional embed parameter works
  - [ ] Returns message_id, channel_id, timestamp
  - [ ] Message appears in channel immediately

- ⚠️ Error Handling
  - [ ] Missing both channel_id and default raises ValueError
  - [ ] Empty content and no embed raises ValueError
  - [ ] Content > 2000 chars raises ValueError
  - [ ] Invalid channel_id raises NotFound error
  - [ ] Missing SEND_MESSAGES permission raises PermissionError
  - [ ] Channel type doesn't support messages (voice) raises error

- 🔍 Edge Cases
  - [ ] Message with exactly 2000 chars (max)
  - [ ] Message with 1 char (min)
  - [ ] Message with only embed, no content
  - [ ] Message with content + embed
  - [ ] Message with Unicode/emoji
  - [ ] Message with Discord mentions (<@userid>)
  - [ ] Message with channel mentions (<#channelid>)
  - [ ] Message with markdown formatting

- 🔗 Integration
  - [ ] Uses DISCORD_DEFAULT_CHANNEL_ID when channel_id omitted
  - [ ] Message appears in read_messages results
  - [ ] Respects channel permissions

**Test File**: tests/tools/test_messages.py::TestSendMessage

---

#### Tool #15: read_messages
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1016-1104  
**Purpose**: Retrieve message history from channel with pagination

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns message history with all fields
  - [ ] Default limit=50 works
  - [ ] Custom limit (1-100) works
  - [ ] before parameter for pagination works
  - [ ] after parameter for pagination works
  - [ ] Messages sorted by timestamp (newest first)
  - [ ] has_more flag accurate
  - [ ] Includes message content, author, embeds, attachments

- ⚠️ Error Handling
  - [ ] Invalid limit (0, -1, 101) raises ValueError
  - [ ] Invalid before message_id raises error
  - [ ] Invalid after message_id raises error
  - [ ] Missing READ_MESSAGE_HISTORY permission raises PermissionError
  - [ ] Channel not found raises NotFound error

- 🔍 Edge Cases
  - [ ] Channel with no messages (empty array)
  - [ ] Channel with < limit messages (has_more=false)
  - [ ] Channel with exactly limit messages
  - [ ] Messages with attachments
  - [ ] Messages with embeds
  - [ ] Messages with reactions
  - [ ] System messages (member join, pin, etc.)

- 🔗 Integration
  - [ ] Token-efficient: pagination controls context usage
  - [ ] Messages include full author object

**Test File**: tests/tools/test_messages.py::TestReadMessages

---

#### Tool #16: delete_message
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1107-1159  
**Purpose**: Delete message from channel (⚠️ DESTRUCTIVE - PERMANENT)

**Test Requirements**:
- ✅ Happy Path
  - [ ] Successfully deletes message
  - [ ] Returns success=true with message_id and channel_id
  - [ ] Message no longer appears in read_messages

- ⚠️ Error Handling
  - [ ] Missing message_id raises ValueError
  - [ ] Invalid message_id raises ValueError
  - [ ] Message not found raises NotFound error
  - [ ] Missing MANAGE_MESSAGES permission (for others' messages) raises PermissionError
  - [ ] Can delete own messages without MANAGE_MESSAGES

- 🔍 Edge Cases
  - [ ] Deleting very old message (> 14 days)
  - [ ] Deleting message with attachments
  - [ ] Deleting message with embeds
  - [ ] Deleting pinned message (unpins automatically)

- 🔗 Integration
  - [ ] Audit log entry created (if deleted by moderator)
  - [ ] Message permanently deleted (cannot be recovered)

**Test File**: tests/tools/test_messages.py::TestDeleteMessage

---

#### Tool #17: add_reaction
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1162-1223  
**Purpose**: Add emoji reaction to message

**Test Requirements**:
- ✅ Happy Path
  - [ ] Adds Unicode emoji reaction successfully
  - [ ] Adds custom emoji reaction successfully
  - [ ] Returns success=true with message_id and emoji

- ⚠️ Error Handling
  - [ ] Missing message_id raises ValueError
  - [ ] Missing emoji raises ValueError
  - [ ] Invalid emoji format raises ValueError
  - [ ] Message not found raises NotFound error
  - [ ] Missing ADD_REACTIONS permission raises PermissionError
  - [ ] Custom emoji from different server raises error

- 🔍 Edge Cases
  - [ ] Unicode emoji (👍)
  - [ ] Custom emoji (:custom_emoji_name:)
  - [ ] Animated emoji
  - [ ] Adding reaction already present (no error)
  - [ ] Maximum reactions on message (20 unique)

- 🔗 Integration
  - [ ] Reaction appears on message immediately
  - [ ] Bot user shown as reactor

**Test File**: tests/tools/test_messages.py::TestAddReaction

---

#### Tool #18: send_dm
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1226-1292  
**Purpose**: Send direct message to user

**Test Requirements**:
- ✅ Happy Path
  - [ ] Sends DM to user successfully
  - [ ] Required user_id parameter works
  - [ ] Required content parameter works
  - [ ] Optional embed parameter works
  - [ ] Returns success=true with dm_channel_id

- ⚠️ Error Handling
  - [ ] Missing user_id raises ValueError
  - [ ] Missing content raises ValueError
  - [ ] Invalid user_id raises ValueError
  - [ ] Content > 2000 chars raises ValueError
  - [ ] User not found raises NotFound error
  - [ ] User has DMs disabled raises Forbidden error
  - [ ] User not mutual with bot raises Forbidden error

- 🔍 Edge Cases
  - [ ] DM with embed only (no content)
  - [ ] DM with content + embed
  - [ ] DM with mentions (work differently in DMs)
  - [ ] DM to user in multiple shared guilds

- 🔗 Integration
  - [ ] Creates DM channel if doesn't exist
  - [ ] Reuses existing DM channel
  - [ ] Use sparingly to avoid rate limits as documented

**Test File**: tests/tools/test_messages.py::TestSendDM

---

### Group 6: Webhook Management (3 tools)

#### Tool #19: create_webhook
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1295-1362  
**Purpose**: Create webhook for channel (⚠️ DESTRUCTIVE)

**Test Requirements**:
- ✅ Happy Path
  - [ ] Creates webhook successfully
  - [ ] Required channel_id parameter works
  - [ ] Required name parameter works
  - [ ] Optional avatar_url parameter works
  - [ ] Returns webhook with id, name, token, url

- ⚠️ Error Handling
  - [ ] Missing channel_id raises ValueError
  - [ ] Missing name raises ValueError
  - [ ] Empty name raises ValueError
  - [ ] Invalid channel_id raises NotFound error
  - [ ] Missing MANAGE_WEBHOOKS permission raises PermissionError
  - [ ] Channel type doesn't support webhooks raises error
  - [ ] Guild at webhook limit (10 per channel) raises error

- 🔍 Edge Cases
  - [ ] Webhook name with special chars
  - [ ] Webhook with custom avatar
  - [ ] Webhook with no avatar (default)
  - [ ] Multiple webhooks in same channel

- 🔗 Integration
  - [ ] Webhook URL immediately usable for send_webhook_message
  - [ ] Audit log entry created

**Test File**: tests/tools/test_webhooks.py::TestCreateWebhook

---

#### Tool #20: send_webhook_message
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1365-1444  
**Purpose**: Send message via webhook with custom username/avatar

**Test Requirements**:
- ✅ Happy Path
  - [ ] Sends message via webhook successfully
  - [ ] Required webhook_url parameter works
  - [ ] Required content parameter works
  - [ ] Optional username override works
  - [ ] Optional avatar_url override works
  - [ ] Optional embed parameter works
  - [ ] Returns success=true

- ⚠️ Error Handling
  - [ ] Missing webhook_url raises ValueError
  - [ ] Missing content raises ValueError
  - [ ] Invalid webhook_url raises ValueError
  - [ ] Content > 2000 chars raises ValueError
  - [ ] Webhook deleted raises NotFound error
  - [ ] Invalid username raises ValueError
  - [ ] Rate limited appropriately

- 🔍 Edge Cases
  - [ ] Message with username override
  - [ ] Message with avatar override
  - [ ] Message with both overrides
  - [ ] Message with embed
  - [ ] Message with maximum length
  - [ ] Special characters in username

- 🔗 Integration
  - [ ] Message appears as webhook, not bot
  - [ ] Username/avatar override displayed correctly
  - [ ] Use for The Chronicler integration as documented

**Test File**: tests/tools/test_webhooks.py::TestSendWebhookMessage

---

#### Tool #21: delete_webhook
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1447-1494  
**Purpose**: Delete webhook (⚠️ DESTRUCTIVE - PERMANENT)

**Test Requirements**:
- ✅ Happy Path
  - [ ] Deletes webhook successfully
  - [ ] Returns success=true with webhook_id

- ⚠️ Error Handling
  - [ ] Missing webhook_id raises ValueError
  - [ ] Invalid webhook_id raises ValueError
  - [ ] Webhook not found raises NotFound error
  - [ ] Missing MANAGE_WEBHOOKS permission raises PermissionError

- 🔍 Edge Cases
  - [ ] Deleting webhook in use (messages remain)
  - [ ] Deleting webhook with token

- 🔗 Integration
  - [ ] Webhook URL no longer works after deletion
  - [ ] Audit log entry created

**Test File**: tests/tools/test_webhooks.py::TestDeleteWebhook

---

### Group 7: Forum Support (3 tools)

#### Tool #22: create_forum_post
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1497-1581  
**Purpose**: Create new post in forum channel (⚠️ DESTRUCTIVE)

**Test Requirements**:
- ✅ Happy Path
  - [ ] Creates forum post successfully
  - [ ] Required channel_id (forum channel) works
  - [ ] Required title parameter works
  - [ ] Required content parameter works
  - [ ] Optional tags parameter works
  - [ ] Returns post with thread_id and message_id
  - [ ] Post appears in forum immediately

- ⚠️ Error Handling
  - [ ] Missing channel_id raises ValueError
  - [ ] Missing title raises ValueError
  - [ ] Missing content raises ValueError
  - [ ] Channel not forum type raises error
  - [ ] Invalid tags raises ValueError
  - [ ] Missing CREATE_FORUM_THREADS permission raises PermissionError

- 🔍 Edge Cases
  - [ ] Post with maximum tags
  - [ ] Post with no tags
  - [ ] Post with minimum title length
  - [ ] Post with maximum title length
  - [ ] Post with embeds in content

- 🔗 Integration
  - [ ] Creates thread automatically as documented
  - [ ] Initial message is first post in thread
  - [ ] Tags applied correctly

**Test File**: tests/tools/test_forums.py::TestCreateForumPost

---

#### Tool #23: reply_to_forum
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1584-1638  
**Purpose**: Reply to existing forum post

**Test Requirements**:
- ✅ Happy Path
  - [ ] Replies to forum thread successfully
  - [ ] Required thread_id parameter works
  - [ ] Required content parameter works
  - [ ] Returns message_id and thread_id

- ⚠️ Error Handling
  - [ ] Missing thread_id raises ValueError
  - [ ] Missing content raises ValueError
  - [ ] Thread not found raises NotFound error
  - [ ] Thread archived/locked raises error
  - [ ] Missing SEND_MESSAGES_IN_THREADS permission raises PermissionError

- 🔍 Edge Cases
  - [ ] Reply to archived thread (fails)
  - [ ] Reply with mentions
  - [ ] Reply with maximum content length
  - [ ] Multiple sequential replies

- 🔗 Integration
  - [ ] Reply appears in thread immediately
  - [ ] Thread bumped to top of forum

**Test File**: tests/tools/test_forums.py::TestReplyToForum

---

#### Tool #24: get_forum_post
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1641-1710  
**Purpose**: Retrieve forum post details including all messages

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns forum post with all messages
  - [ ] Required thread_id parameter works
  - [ ] Returns post metadata (title, author, tags, timestamps)
  - [ ] Returns all messages in thread (paginated if needed)
  - [ ] Includes message authors and content

- ⚠️ Error Handling
  - [ ] Missing thread_id raises ValueError
  - [ ] Invalid thread_id raises ValueError
  - [ ] Thread not found raises NotFound error
  - [ ] Missing READ_MESSAGE_HISTORY permission raises PermissionError

- 🔍 Edge Cases
  - [ ] Post with no replies (only initial message)
  - [ ] Post with 100+ replies
  - [ ] Archived post
  - [ ] Locked post
  - [ ] Post with deleted messages

- 🔗 Integration
  - [ ] Messages sorted chronologically
  - [ ] Initial post identified correctly

**Test File**: tests/tools/test_forums.py::TestGetForumPost

---

### Group 8: Thread Management (2 tools)

#### Tool #25: create_thread
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1713-1792  
**Purpose**: Create thread from message or in channel (⚠️ DESTRUCTIVE)

**Test Requirements**:
- ✅ Happy Path
  - [ ] Creates thread from message successfully
  - [ ] Creates thread in channel (without message) successfully
  - [ ] Required name parameter works
  - [ ] Optional message_id parameter works
  - [ ] Optional channel_id parameter works
  - [ ] Optional auto_archive_duration works (60, 1440, 4320, 10080)
  - [ ] Returns thread with id, name, parent_id

- ⚠️ Error Handling
  - [ ] Missing name raises ValueError
  - [ ] Missing both message_id and channel_id raises ValueError
  - [ ] Invalid auto_archive_duration raises ValueError
  - [ ] Message not found raises NotFound error
  - [ ] Channel not found raises NotFound error
  - [ ] Missing CREATE_PUBLIC_THREADS permission raises PermissionError
  - [ ] Channel doesn't support threads raises error

- 🔍 Edge Cases
  - [ ] Thread from message in text channel
  - [ ] Thread from message in forum (not applicable)
  - [ ] Thread with minimum name length
  - [ ] Thread with maximum name length
  - [ ] Thread with each archive duration option

- 🔗 Integration
  - [ ] Thread appears in list_channels under "thread" type
  - [ ] Thread linked to parent message/channel
  - [ ] Auto-archives after configured duration

**Test File**: tests/tools/test_threads.py::TestCreateThread

---

#### Tool #26: archive_thread
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1795-1842  
**Purpose**: Archive thread manually (⚠️ DESTRUCTIVE)

**Test Requirements**:
- ✅ Happy Path
  - [ ] Archives thread successfully
  - [ ] Returns success=true with thread_id
  - [ ] Thread marked as archived

- ⚠️ Error Handling
  - [ ] Missing thread_id raises ValueError
  - [ ] Invalid thread_id raises ValueError
  - [ ] Thread not found raises NotFound error
  - [ ] Missing MANAGE_THREADS permission raises PermissionError
  - [ ] Thread already archived (idempotent - no error)

- 🔍 Edge Cases
  - [ ] Archiving active thread
  - [ ] Archiving thread with unread messages
  - [ ] Archiving locked thread

- 🔗 Integration
  - [ ] Archived thread no longer shows in active list
  - [ ] Archived thread can be unarchived
  - [ ] Messages in archived thread preserved

**Test File**: tests/tools/test_threads.py::TestArchiveThread

---

### Group 9: ComfyUI Integration (4 tools)

#### Tool #27: generate_image
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1845-1927  
**Purpose**: Generate image using ComfyUI workflow

**Test Requirements**:
- ✅ Happy Path
  - [ ] Generates image successfully
  - [ ] Required prompt parameter works
  - [ ] Optional workflow parameter works (default: portrait)
  - [ ] Optional seed parameter works
  - [ ] Optional steps parameter works
  - [ ] Returns based on COMFYUI_RETURN_MODE (base64/url/cdn)
  - [ ] Returns generation metadata (seed, workflow, duration)

- ⚠️ Error Handling
  - [ ] Missing prompt raises ValueError
  - [ ] Empty prompt raises ValueError
  - [ ] Invalid workflow name raises ValueError
  - [ ] ComfyUI not configured raises error
  - [ ] ComfyUI server unreachable raises ConnectionError
  - [ ] Generation timeout raises TimeoutError
  - [ ] Out of VRAM error handled

- 🔍 Edge Cases
  - [ ] Very long prompt (max length)
  - [ ] Prompt with special characters
  - [ ] Custom seed for reproducibility
  - [ ] Maximum steps value
  - [ ] Minimum steps value
  - [ ] Each return mode (base64, url, cdn)

- 🔗 Integration
  - [ ] Respects COMFYUI_ENABLED config flag
  - [ ] Respects COMFYUI_RETURN_MODE config
  - [ ] Workflow presets load correctly (portrait, banner, recruitment, emblem)
  - [ ] BYOW custom workflows work

**Test File**: tests/tools/test_comfyui.py::TestGenerateImage

---

#### Tool #28: list_workflows
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1930-1985  
**Purpose**: List available ComfyUI workflow presets

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns list of available workflows
  - [ ] Each workflow includes name, description, dimensions
  - [ ] Built-in presets included (portrait, banner, recruitment, emblem)
  - [ ] Custom workflows included if present

- ⚠️ Error Handling
  - [ ] ComfyUI not enabled returns empty list or appropriate message
  - [ ] Workflow directory missing handled gracefully

- 🔍 Edge Cases
  - [ ] No custom workflows (only built-in presets)
  - [ ] Custom workflows present
  - [ ] Invalid workflow JSON files skipped
  - [ ] Workflow with missing metadata

- 🔗 Integration
  - [ ] Workflows directory scanned correctly
  - [ ] Workflow names match generate_image workflow parameter

**Test File**: tests/tools/test_comfyui.py::TestListWorkflows

---

#### Tool #29: get_generation_status
**Documentation Promise**: docs/TOOLS_REFERENCE.md:1988-2057  
**Purpose**: Check status of in-progress image generation

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns status for valid job_id
  - [ ] Status types: queued, processing, complete, failed
  - [ ] Includes progress percentage when processing
  - [ ] Includes result when complete
  - [ ] Includes error message when failed

- ⚠️ Error Handling
  - [ ] Missing job_id raises ValueError
  - [ ] Invalid job_id raises ValueError
  - [ ] Job not found raises NotFound error
  - [ ] ComfyUI server unreachable raises ConnectionError

- 🔍 Edge Cases
  - [ ] Job in queue (not started)
  - [ ] Job processing (partial progress)
  - [ ] Job complete (has result)
  - [ ] Job failed (has error)
  - [ ] Very old job (expired)

- 🔗 Integration
  - [ ] Job IDs from generate_image are valid
  - [ ] Progress updates in real-time

**Test File**: tests/tools/test_comfyui.py::TestGetGenerationStatus

---

#### Tool #30: get_image
**Documentation Promise**: docs/TOOLS_REFERENCE.md:2060-2162  
**Purpose**: Retrieve generated image by ID

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns image for valid image_id
  - [ ] Returns format based on COMFYUI_RETURN_MODE
  - [ ] Includes image metadata (dimensions, format, size)

- ⚠️ Error Handling
  - [ ] Missing image_id raises ValueError
  - [ ] Invalid image_id raises ValueError
  - [ ] Image not found raises NotFound error
  - [ ] Image expired/deleted handled

- 🔍 Edge Cases
  - [ ] Each return mode (base64, url, cdn)
  - [ ] Large images (high resolution)
  - [ ] Small images (low resolution)

- 🔗 Integration
  - [ ] Image IDs from generate_image are valid
  - [ ] CDN URLs persist as documented

**Test File**: tests/tools/test_comfyui.py::TestGetImage

---

### Group 10: Utility (3 tools)

#### Tool #31: test_connection
**Documentation Promise**: docs/TOOLS_REFERENCE.md:2165-2227  
**Purpose**: Test Discord bot connection and permissions

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns connection status
  - [ ] Includes bot user info (id, username)
  - [ ] Includes guild connection status
  - [ ] Includes permissions summary
  - [ ] Indicates if intents enabled (GUILD_MEMBERS, MESSAGE_CONTENT)

- ⚠️ Error Handling
  - [ ] Bot not connected returns error status
  - [ ] Invalid token returns authentication error

- 🔍 Edge Cases
  - [ ] Bot in multiple guilds
  - [ ] Bot with minimal permissions
  - [ ] Bot with ADMINISTRATOR permission
  - [ ] Missing intents warnings

- 🔗 Integration
  - [ ] Useful for troubleshooting as documented
  - [ ] Validates configuration on startup

**Test File**: tests/tools/test_utility.py::TestTestConnection

---

#### Tool #32: test_comfyui
**Documentation Promise**: docs/TOOLS_REFERENCE.md:2230-2283  
**Purpose**: Test ComfyUI server connection and configuration

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns connection status
  - [ ] Includes server info (host, port)
  - [ ] Includes enabled status
  - [ ] Includes return mode config
  - [ ] Ping successful when server reachable

- ⚠️ Error Handling
  - [ ] ComfyUI not enabled returns disabled status
  - [ ] ComfyUI server unreachable returns error status
  - [ ] Invalid configuration detected

- 🔍 Edge Cases
  - [ ] ComfyUI enabled but server down
  - [ ] ComfyUI on non-standard port
  - [ ] ComfyUI on remote server

- 🔗 Integration
  - [ ] Validates ComfyUI setup before image generation
  - [ ] Useful for troubleshooting as documented

**Test File**: tests/tools/test_utility.py::TestTestComfyUI

---

#### Tool #33: list_available_tools
**Documentation Promise**: docs/TOOLS_REFERENCE.md:2286-2414  
**Purpose**: List all available MCP tools with descriptions (meta-tool)

**Test Requirements**:
- ✅ Happy Path
  - [ ] Returns list of all 33 tools
  - [ ] Each tool includes name, description, category
  - [ ] Tools organized by category as documented
  - [ ] ComfyUI tools included only if enabled
  - [ ] Descriptions match documentation

- ⚠️ Error Handling
  - [ ] Always succeeds (no error cases)

- 🔍 Edge Cases
  - [ ] ComfyUI disabled (fewer tools returned)
  - [ ] ComfyUI enabled (all tools returned)
  - [ ] Tool count matches documentation (33 when ComfyUI enabled)

- 🔗 Integration
  - [ ] Helps agents discover capabilities
  - [ ] Self-documenting as per MCP best practices

**Test File**: tests/tools/test_utility.py::TestListAvailableTools

---

## Configuration Testing Requirements

**Source**: docs/CONFIGURATION.md

### Environment Variables

**Test Requirements**:
- [ ] DISCORD_TOKEN required, validated, not empty
- [ ] DISCORD_DEFAULT_GUILD_ID optional, validated as numeric
- [ ] DISCORD_DEFAULT_CHANNEL_ID optional, validated as numeric
- [ ] GUILDMASTER_THEME validated (generic/wow/custom)
- [ ] COMFYUI_ENABLED boolean parsing
- [ ] COMFYUI_HOST validated when enabled
- [ ] COMFYUI_PORT validated as integer (1-65535)
- [ ] COMFYUI_RETURN_MODE validated (base64/url/cdn)
- [ ] MCP_TRANSPORT validated (stdio/http)
- [ ] MCP_HTTP_PORT validated when transport=http
- [ ] LOG_LEVEL validated (DEBUG/INFO/WARNING/ERROR)
- [ ] All defaults applied correctly

**Test File**: tests/test_config.py

---

## Theming System Testing Requirements

**Source**: docs/theming-guide.md, docs/architecture.md

### Theme Loading and Application

**Test Requirements**:
- [ ] Generic theme loads successfully
- [ ] WoW theme loads successfully
- [ ] Custom theme loads from YAML file
- [ ] Invalid theme raises error
- [ ] Tool name mapping works correctly
- [ ] Message formatting applies theme
- [ ] Theme switching at runtime works
- [ ] Tool descriptions adapt to theme

**Test File**: tests/test_theming.py

---

## Architecture & System Testing Requirements

**Source**: docs/architecture.md

### System Integration

**Test Requirements**:
- [ ] MCP server starts in stdio mode
- [ ] MCP server starts in HTTP mode
- [ ] Discord client connects successfully
- [ ] Stateless operation (no persistent state)
- [ ] Token efficiency validated (pagination, filtering work)
- [ ] Error handling consistent across tools
- [ ] Permission checks work correctly

**Test File**: tests/test_system.py

---

## Coverage Summary

**Total Test Requirements**: 500+ individual test cases

**By Category**:
- Guild Information: 30 tests
- Member Management: 60 tests
- Role Operations: 45 tests
- Channel Management: 60 tests
- Messaging: 75 tests
- Webhook Management: 45 tests
- Forum Support: 45 tests
- Thread Management: 30 tests
- ComfyUI Integration: 60 tests
- Utility: 30 tests
- Configuration: 30 tests
- Theming: 25 tests
- System: 30 tests

**Priority Order**:
1. **P0 - Critical Path** (message, member, channel tools): Implement first
2. **P1 - Core Features** (roles, webhooks, configuration): Implement second
3. **P2 - Advanced Features** (forums, threads, ComfyUI): Implement third
4. **P3 - System Tests** (integration, theming): Implement last

---

## Success Metrics

**Phase 1 Complete When**:
✅ Every tool mapped to test requirements  
✅ Every parameter validated  
✅ Every error case identified  
✅ Every edge case documented  
✅ Coverage targets defined

**Documentation Promise → Test Validation**: 100% mapping achieved

---

**For the craft. For quality. For promises kept.** ⚔️
