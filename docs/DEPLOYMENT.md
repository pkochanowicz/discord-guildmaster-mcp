# Deployment Guide - Discord Guildmaster MCP

## Prerequisites

### Required
- [Fly.io account](https://fly.io) (free tier available)
- [Fly CLI installed](https://fly.io/docs/hands-on/install-flyctl/)
- Discord bot token from [Discord Developer Portal](https://discord.com/developers/applications)
- Discord bot with required intents enabled:
  - Server Members Intent
  - Message Content Intent
  - Guilds Intent

### Optional
- Docker & Docker Compose (for local testing)
- ComfyUI server (for AI image generation)

---

## Local Development Setup

### 1. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Discord bot token
nano .env

# Required minimum:
DISCORD_TOKEN=your_bot_token_here
```

### 2. Run with Docker Compose
```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f guildmaster

# Stop
docker-compose down
```

### 3. Run Locally (without Docker)
```bash
# Install dependencies
uv pip install -e ".[comfyui]"

# Run server
python -m discord_guildmaster_mcp.server

# Or with specific env file
ENV_FILE=.env.integration python -m discord_guildmaster_mcp.server
```

---

## Fly.io Production Deployment

### 1. Install Fly CLI
```bash
# macOS/Linux
curl -L https://fly.io/install.sh | sh

# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Verify installation
fly version
```

### 2. Login to Fly.io
```bash
fly auth login
```

### 3. Create Fly.io App (First Time Only)
```bash
# Launch interactive setup
fly launch --no-deploy

# Or specify app name manually
fly apps create discord-guildmaster-mcp
```

**Configuration prompts:**
- Choose app name: `discord-guildmaster-mcp` (or your preference)
- Choose region: Select closest to your users (e.g., `iad` for US East)
- Setup Postgres database: **No** (we don't need a database)
- Setup Redis: **No** (we don't need Redis)
- Deploy now: **No** (we'll set secrets first)

### 4. Set Secrets
```bash
# Required: Discord bot token
fly secrets set DISCORD_TOKEN=your_actual_bot_token_here

# Optional: Default guild ID (recommended)
fly secrets set DISCORD_DEFAULT_GUILD_ID=your_guild_id

# Optional: Default channel ID
fly secrets set DISCORD_DEFAULT_CHANNEL_ID=your_channel_id

# View configured secrets (values hidden)
fly secrets list
```

### 5. Deploy
```bash
# Deploy to Fly.io
fly deploy

# Monitor deployment
fly logs

# Check status
fly status
```

### 6. Verify Deployment
```bash
# Check app status
fly status

# View recent logs
fly logs --app discord-guildmaster-mcp

# SSH into container (for debugging)
fly ssh console

# Inside container, test imports
python -c "import discord_guildmaster_mcp; print('Import successful')"
```

---

## Post-Deployment Configuration

### Bot Permissions Setup

Your Discord bot needs these permissions in the Discord Developer Portal:

**OAuth2 → URL Generator:**
- Scopes: `bot`, `applications.commands`
- Bot Permissions:
  - ✅ View Channels
  - ✅ Send Messages
  - ✅ Manage Messages
  - ✅ Read Message History
  - ✅ Manage Channels
  - ✅ Manage Roles
  - ✅ Manage Webhooks
  - ✅ View Audit Log

**Bot → Privileged Gateway Intents:**
- ✅ Server Members Intent (required for `list_members`, `get_member_info`)
- ✅ Message Content Intent (required for message operations)

### Test the Deployment
```bash
# Test with Claude Desktop
# Add to claude_desktop_config.json:
{
  "mcpServers": {
    "discord-guildmaster": {
      "command": "fly",
      "args": ["ssh", "console", "-C", "python -m discord_guildmaster_mcp.server"],
      "env": {}
    }
  }
}
```

---

## Scaling & Performance

### Increase Resources
```bash
# Scale to more CPU/memory if needed
fly scale vm shared-cpu-1x --memory 512

# View available VM sizes
fly platform vm-sizes
```

### Multi-Region Deployment
```bash
# Add another region
fly regions add lhr  # London

# Remove region
fly regions remove lhr

# List current regions
fly regions list
```

### Monitoring
```bash
# Real-time logs
fly logs

# Resource usage
fly status

# Metrics (if configured)
fly dashboard metrics
```

---

## Troubleshooting

### Issue: Bot Not Responding

**Check logs:**
```bash
fly logs --app discord-guildmaster-mcp
```

**Common causes:**
- Missing `DISCORD_TOKEN` secret
- Bot not invited to server
- Missing Discord intents
- Incorrect permissions

**Solution:**
```bash
# Verify secrets
fly secrets list

# Restart app
fly apps restart discord-guildmaster-mcp
```

### Issue: Permission Errors

**Symptoms:** `PermissionError` in logs when calling tools

**Solutions:**
1. Check bot role position in Discord server (must be above roles it manages)
2. Verify bot has required permissions in channel
3. Check Privileged Gateway Intents are enabled

### Issue: Deployment Fails

**Check build logs:**
```bash
fly logs
```

**Common issues:**
- Missing dependencies in `pyproject.toml`
- Incorrect Python version
- Docker build failures

**Solution:**
```bash
# Rebuild without cache
fly deploy --no-cache
```

### Issue: High Memory Usage

**Symptoms:** App crashes, OOM errors

**Solutions:**
```bash
# Increase memory allocation
fly scale vm shared-cpu-1x --memory 512

# Or use larger VM
fly scale vm shared-cpu-2x
```

---

## Updating the Deployment

### Deploy New Version
```bash
# Pull latest code
git pull origin main

# Deploy updated version
fly deploy

# Verify deployment
fly logs
```

### Rollback Deployment
```bash
# List recent releases
fly releases

# Rollback to previous version
fly releases rollback
```

---

## Security Best Practices

### Secrets Management

✅ **DO:**
- Use `fly secrets set` for all sensitive data
- Rotate Discord bot token regularly
- Use different bots for development/production
- Keep `.env` files in `.gitignore`

❌ **DON'T:**
- Commit `.env` files to git
- Share bot tokens in code or docs
- Use production bot token for testing
- Store secrets in `fly.toml`

### Network Security

- Fly.io automatically provides HTTPS
- Use private networking between services if needed
- Enable rate limiting if exposing HTTP endpoints

---

## Cost Optimization

### Free Tier Limits (Fly.io)

- 3 shared-cpu-1x VMs (256MB each)
- 3GB persistent storage
- 160GB outbound data transfer/month

**For discord-guildmaster-mcp:**
- Expected: **Well within free tier**
- Single VM: ~$0/month (free tier)
- Minimal storage needed
- Low bandwidth usage

### Monitoring Costs
```bash
# View current resource usage
fly status

# Check billing
fly billing
```

---

## Support & Resources

- **Fly.io Docs:** https://fly.io/docs/
- **Discord.py Docs:** https://discordpy.readthedocs.io/
- **MCP Docs:** https://modelcontextprotocol.io/
- **Project Issues:** https://github.com/your-org/discord-guildmaster-mcp/issues

---

**For the Alliance! For production deployments! For zero-downtime updates!**
