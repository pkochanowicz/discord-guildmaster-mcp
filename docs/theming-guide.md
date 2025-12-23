<!-- Generated: 2025-12-23 | DDD Phase 1: Documentation Genesis -->

# Theming Guide

Create custom themes for Discord Guildmaster MCP without modifying core code.

---

## Theming Philosophy

Themes provide **personality without coupling**. The core functionality remains generic; themes wrap tool names and descriptions with custom terminology.

---

## Built-in Themes

### Generic (Default)
Universal terminology for broad compatibility.

```
send_message → send_message
list_members → list_members
create_channel → create_channel
```

### WoW (World of Warcraft)
Immersive fantasy terminology for gaming communities.

```
send_message → summon_herald
list_members → muster_roster
create_channel → forge_chamber
```

---

## Creating Custom Themes

### YAML Theme File

```yaml
# themes/cyberpunk.yaml
name: "Cyberpunk Netrunner"
description: "Terminology for cyberpunk/sci-fi communities"
version: "1.0.0"

tools:
  # Guild operations
  get_guild_info:
    name: "scan_subnet"
    description: "Scan subnet metadata and node count"
    
  list_members:
    name: "enumerate_netrunners"
    description: "Enumerate active netrunners in subnet"
    
  # Messaging
  send_message:
    name: "transmit_signal"
    description: "Broadcast signal to network node"
    
  create_channel:
    name: "establish_node"
    description: "Establish new network communication node"
    
  # Map all 33 tools...
```

### Using Custom Theme

```bash
# In .env
GUILDMASTER_THEME=custom
GUILDMASTER_THEME_PATH=./themes/cyberpunk.yaml
```

---

## Theme Best Practices

1. **Maintain clarity** — Don't obscure tool purpose
2. **Be consistent** — Use coherent terminology
3. **Document rationale** — Explain theme choices
4. **Test thoroughly** — Ensure LLMs understand themed names

---

**Craft your community's personality.** ⚔️
