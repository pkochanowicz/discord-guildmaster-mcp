<!-- Generated: 2025-12-23 | DDD Phase 1: Documentation Genesis -->

# Troubleshooting Guide

Common issues and solutions for Discord Guildmaster MCP. If you don't find your issue here, check [GitHub Issues](https://github.com/your-org/discord-guildmaster-mcp/issues) or join the [Discord community](https://discord.gg/rM8EevEq).

---

## Installation Issues

### Python Version Errors

**Problem:** `ERROR: Python 3.11 or higher required`

**Solution:**

```bash
python3 --version  # Check version
uv python install 3.12  # Install Python 3.12
uv run --python 3.12 guildmaster  # Use specific version
```

### Module Not Found: discord

**Problem:** `ModuleNotFoundError: No module named 'discord'`

**Solution:**

```bash
source venv/bin/activate  # Activate virtual environment
pip install -e .  # Reinstall dependencies
python -c "import discord; print(discord.__version__)"  # Verify
```

---

## Discord Bot & Permissions

### Invalid Token Error

**Problem:** `discord.errors.LoginFailure: Improper token has been passed`

**Solution:**

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Select application → "Bot" tab → "Reset Token"
3. Update `.env`: `DISCORD_TOKEN=your_new_token_here`

### Privileged Intent Not Enabled

**Problem:** `Privileged intent provided is not enabled or whitelisted`

**Solution:**

1. Enable intents in Developer Portal:
    - ✅ Server Members Intent
    - ✅ Message Content Intent
2. Save and restart bot

### Missing Permissions

**Problem:** `403 Forbidden: Missing Permissions`

**Solution:**

```python
result = test_connection()
print(result['guild']['permissions'])  # Check current permissions
```

Required: View Channels, Send Messages, Manage Messages, Manage Roles, Manage Channels, Manage Webhooks

---

## ComfyUI Connection Problems

### Cannot Connect to ComfyUI Server

**Diagnosis:**

```bash
curl http://localhost:8188  # Should return HTML
nc -zv localhost 8188  # Check port
```

**Solutions:**

1. Start ComfyUI: `cd /path/to/ComfyUI && python main.py`
2. Check .env: `COMFYUI_HOST=localhost` and `COMFYUI_PORT=8188`
3. Allow firewall: `sudo ufw allow 8188`

### Generation Timeout

**Solutions:**

1. Increase timeout: `COMFYUI_TIMEOUT=900`
2. Reduce complexity: Lower steps, use faster sampler
3. Check GPU: `nvidia-smi`

### Out of VRAM

**Solutions:**

1. Use SD 1.5 instead of SDXL
2. Reduce resolution (512×512 instead of 1024×1024)
3. Enable CPU offloading in ComfyUI settings

---

## Debug Mode

Enable debug logging:

```bash
LOG_LEVEL=DEBUG
LOG_FORMAT=text
LOG_FILE=/var/log/guildmaster/debug.log
```

---

## Common Error Codes

| Code  | Meaning             | Solution                      |
| ----- | ------------------- | ----------------------------- |
| 10003 | Unknown Channel     | Verify channel ID             |
| 10004 | Unknown Guild       | Verify guild ID               |
| 10013 | Unknown User        | User not in guild             |
| 50001 | Missing Access      | Bot lacks channel access      |
| 50013 | Missing Permissions | Bot lacks required permission |

---

For more help: [GitHub Issues](https://github.com/your-org/discord-guildmaster-mcp/issues) | [Discord](https://discord.gg/rM8EevEq)
