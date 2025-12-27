# Discord Guildmaster MCP - Production Dockerfile
# Multi-stage build for optimal image size

# ============================================================================
# Stage 1: Builder - Install dependencies
# ============================================================================
FROM python:3.12-slim AS builder

# Install uv for fast package installation
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml README.md ./

# Install dependencies to /app/.venv
RUN uv venv /app/.venv && \
    . /app/.venv/bin/activate && \
    uv pip install -e ".[comfyui]"

# ============================================================================
# Stage 2: Runtime - Minimal production image
# ============================================================================
FROM python:3.12-slim

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 guildmaster && \
    mkdir -p /app && \
    chown -R guildmaster:guildmaster /app

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder --chown=guildmaster:guildmaster /app/.venv /app/.venv

# Copy application code
COPY --chown=guildmaster:guildmaster discord_guildmaster_mcp/ ./discord_guildmaster_mcp/
COPY --chown=guildmaster:guildmaster workflows/ ./workflows/
COPY --chown=guildmaster:guildmaster README.md ./

# Switch to non-root user
USER guildmaster

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import discord_guildmaster_mcp; print('healthy')" || exit 1

# Default command (stdio mode)
CMD ["python", "-m", "discord_guildmaster_mcp.server"]

# Labels
LABEL org.opencontainers.image.title="Discord Guildmaster MCP"
LABEL org.opencontainers.image.description="MCP server for Discord guild management"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="Azeroth Bound Development Guild"
LABEL org.opencontainers.image.licenses="AGPL-3.0"
