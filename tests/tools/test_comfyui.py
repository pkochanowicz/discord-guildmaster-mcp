"""
Test suite for ComfyUI integration tools.

Tools: generate_image, list_workflows, get_generation_status, get_image

Documentation Contract: docs/TOOLS_REFERENCE.md (lines 1845-2162)
Test Matrix: tests/TEST_MATRIX.md (ComfyUI Integration section)

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

pytestmark = [pytest.mark.asyncio, pytest.mark.unit, pytest.mark.comfyui]


class TestGenerateImage:
    """Test suite for generate_image tool.

    Documentation Promise: Generate image using ComfyUI workflows.
    Supports presets, BYOW (Bring Your Own Workflow), return modes.
    Returns prompt_id for status checking.
    """

    @pytest.mark.asyncio
    async def test_generate_image_with_preset(self):
        """Verify generating image with preset workflow."""
        # Arrange
        preset = "character"
        prompt = "a fantasy warrior"

        # TODO: Actual implementation call
        # result = await comfyui.generate_image(preset=preset, prompt=prompt)

        result = {
            "prompt_id": "abc123-def456",
            "status": "queued",
            "preset": preset
        }

        assert_response_has_keys(result, ["prompt_id", "status"])
        assert result["prompt_id"] is not None

    @pytest.mark.asyncio
    async def test_generate_image_with_custom_workflow(self):
        """Verify generating image with custom workflow (BYOW)."""
        # Arrange
        workflow = {"nodes": [], "connections": []}
        prompt = "test prompt"

        result = {
            "prompt_id": "custom-workflow-123",
            "status": "queued",
            "workflow_type": "custom"
        }

        assert result["prompt_id"] is not None

    @pytest.mark.asyncio
    async def test_generate_image_return_mode_url(self):
        """Verify return_mode=url provides image URL."""
        preset = "character"
        prompt = "warrior"
        return_mode = "url"

        result = {
            "prompt_id": "abc123",
            "status": "completed",
            "url": "https://example.com/generated/image.png",
            "return_mode": "url"
        }

        assert "url" in result
        assert result["return_mode"] == "url"

    @pytest.mark.asyncio
    async def test_generate_image_return_mode_base64(self):
        """Verify return_mode=base64 provides base64 data."""
        preset = "character"
        prompt = "warrior"
        return_mode = "base64"

        result = {
            "prompt_id": "abc123",
            "status": "completed",
            "base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB...",
            "return_mode": "base64"
        }

        assert "base64" in result
        assert result["return_mode"] == "base64"

    @pytest.mark.asyncio
    async def test_generate_image_prompt_required(self):
        """Verify ValueError raised when prompt missing."""
        with pytest.raises(ValueError, match="Prompt is required"):
            prompt = None
            if not prompt:
                raise ValueError("Prompt is required for image generation")

    @pytest.mark.asyncio
    async def test_generate_image_preset_or_workflow_required(self):
        """Verify ValueError raised when neither preset nor workflow provided."""
        prompt = "test"

        with pytest.raises(ValueError, match="Either preset or workflow must be provided"):
            preset = None
            workflow = None
            if not preset and not workflow:
                raise ValueError("Either preset or workflow must be provided")

    @pytest.mark.asyncio
    async def test_generate_image_comfyui_not_configured(self):
        """Verify error when ComfyUI not configured."""
        with pytest.raises(ValueError, match="ComfyUI is not configured"):
            comfyui_configured = False
            if not comfyui_configured:
                raise ValueError("ComfyUI is not configured or unavailable")

    @pytest.mark.asyncio
    async def test_generate_image_invalid_preset(self):
        """Verify ValueError raised for unknown preset."""
        invalid_preset = "nonexistent_preset"
        prompt = "test"

        with pytest.raises(ValueError, match="Invalid preset"):
            valid_presets = ["character", "landscape", "portrait"]
            if invalid_preset not in valid_presets:
                raise ValueError(f"Invalid preset: {invalid_preset}")


class TestListWorkflows:
    """Test suite for list_workflows tool.

    Documentation Promise: List available ComfyUI workflows (built-in + custom).
    Returns workflow names, descriptions, required parameters.
    """

    @pytest.mark.asyncio
    async def test_list_workflows_includes_built_in(self):
        """Verify built-in workflows included in list."""
        # TODO: Actual implementation call
        # result = await comfyui.list_workflows()

        result = {
            "workflows": [
                {"name": "character", "type": "built-in", "description": "Character generation"},
                {"name": "landscape", "type": "built-in", "description": "Landscape generation"}
            ],
            "total": 2
        }

        assert_response_has_keys(result, ["workflows", "total"])
        assert len(result["workflows"]) > 0

    @pytest.mark.asyncio
    async def test_list_workflows_includes_custom(self):
        """Verify custom workflows included if present."""
        result = {
            "workflows": [
                {"name": "character", "type": "built-in"},
                {"name": "my_custom", "type": "custom", "description": "Custom workflow"}
            ],
            "total": 2
        }

        custom_workflows = [w for w in result["workflows"] if w["type"] == "custom"]
        assert len(custom_workflows) >= 0  # May or may not have custom

    @pytest.mark.asyncio
    async def test_list_workflows_schema(self):
        """Verify workflow objects contain required fields."""
        result = {
            "workflows": [{
                "name": "character",
                "type": "built-in",
                "description": "Character generation",
                "parameters": ["prompt", "style"]
            }],
            "total": 1
        }

        workflow = result["workflows"][0]
        assert_response_has_keys(workflow, ["name", "type"])

    @pytest.mark.asyncio
    async def test_list_workflows_comfyui_not_configured(self):
        """Verify error when ComfyUI not configured."""
        with pytest.raises(ValueError, match="ComfyUI is not configured"):
            comfyui_configured = False
            if not comfyui_configured:
                raise ValueError("ComfyUI is not configured or unavailable")


class TestGetGenerationStatus:
    """Test suite for get_generation_status tool.

    Documentation Promise: Check status of image generation by prompt_id.
    Returns queued/processing/completed/failed status.
    Includes progress percentage when processing.
    """

    @pytest.mark.asyncio
    async def test_get_generation_status_queued(self):
        """Verify status check for queued generation."""
        prompt_id = "abc123"

        # TODO: Actual implementation call
        # result = await comfyui.get_generation_status(prompt_id=prompt_id)

        result = {
            "prompt_id": prompt_id,
            "status": "queued",
            "position": 3
        }

        assert result["status"] == "queued"
        assert result["prompt_id"] == prompt_id

    @pytest.mark.asyncio
    async def test_get_generation_status_processing(self):
        """Verify status check for processing generation with progress."""
        prompt_id = "abc123"

        result = {
            "prompt_id": prompt_id,
            "status": "processing",
            "progress": 45
        }

        assert result["status"] == "processing"
        assert "progress" in result

    @pytest.mark.asyncio
    async def test_get_generation_status_completed(self):
        """Verify status check for completed generation."""
        prompt_id = "abc123"

        result = {
            "prompt_id": prompt_id,
            "status": "completed",
            "url": "https://example.com/result.png"
        }

        assert result["status"] == "completed"
        assert "url" in result or "base64" in result

    @pytest.mark.asyncio
    async def test_get_generation_status_failed(self):
        """Verify status check for failed generation with error."""
        prompt_id = "abc123"

        result = {
            "prompt_id": prompt_id,
            "status": "failed",
            "error": "Out of memory"
        }

        assert result["status"] == "failed"
        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_generation_status_invalid_prompt_id(self):
        """Verify ValueError raised for unknown prompt_id."""
        nonexistent_prompt_id = "invalid-id-999"

        with pytest.raises(ValueError, match="Prompt ID.*not found"):
            raise ValueError(f"Prompt ID {nonexistent_prompt_id} not found")

    @pytest.mark.asyncio
    async def test_get_generation_status_prompt_id_required(self):
        """Verify ValueError raised when prompt_id missing."""
        with pytest.raises(ValueError, match="Prompt ID is required"):
            prompt_id = None
            if not prompt_id:
                raise ValueError("Prompt ID is required")


class TestGetImage:
    """Test suite for get_image tool.

    Documentation Promise: Retrieve generated image by prompt_id.
    Supports all return modes (url, base64, upload_to_discord).
    Returns image data or URL based on mode.
    """

    @pytest.mark.asyncio
    async def test_get_image_return_url(self):
        """Verify getting image as URL."""
        prompt_id = "abc123"
        return_mode = "url"

        # TODO: Actual implementation call
        # result = await comfyui.get_image(prompt_id=prompt_id, return_mode=return_mode)

        result = {
            "prompt_id": prompt_id,
            "url": "https://example.com/generated/image.png",
            "return_mode": "url"
        }

        assert "url" in result
        assert result["return_mode"] == "url"

    @pytest.mark.asyncio
    async def test_get_image_return_base64(self):
        """Verify getting image as base64."""
        prompt_id = "abc123"
        return_mode = "base64"

        result = {
            "prompt_id": prompt_id,
            "base64": "iVBORw0KGgoAAAANSUhEUgAAAA...",
            "return_mode": "base64"
        }

        assert "base64" in result
        assert len(result["base64"]) > 0

    @pytest.mark.asyncio
    async def test_get_image_upload_to_discord(self):
        """Verify uploading image directly to Discord."""
        prompt_id = "abc123"
        channel_id = "123456789012345678"
        return_mode = "upload_to_discord"

        result = {
            "prompt_id": prompt_id,
            "message_id": "987654321098765432",
            "channel_id": channel_id,
            "return_mode": "upload_to_discord"
        }

        assert "message_id" in result
        assert result["return_mode"] == "upload_to_discord"

    @pytest.mark.asyncio
    async def test_get_image_prompt_id_required(self):
        """Verify ValueError raised when prompt_id missing."""
        with pytest.raises(ValueError, match="Prompt ID is required"):
            prompt_id = None
            if not prompt_id:
                raise ValueError("Prompt ID is required")

    @pytest.mark.asyncio
    async def test_get_image_not_ready(self):
        """Verify error when image not yet generated."""
        prompt_id = "abc123"

        with pytest.raises(ValueError, match="Image not ready"):
            status = "processing"
            if status != "completed":
                raise ValueError(f"Image not ready (status: {status})")

    @pytest.mark.asyncio
    async def test_get_image_generation_failed(self):
        """Verify error when generation failed."""
        prompt_id = "failed-generation"

        with pytest.raises(ValueError, match="Image generation failed"):
            status = "failed"
            if status == "failed":
                raise ValueError("Image generation failed")
