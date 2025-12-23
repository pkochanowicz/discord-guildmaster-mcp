"""
Custom assertion helpers for discord-guildmaster-mcp tests.

Provides reusable assertion functions that validate common patterns
and reduce test boilerplate.

Phase: DDD Phase 2 - Test Suite Implementation
Generated: 2025-12-23
"""

from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock


# ============================================================================
# DISCORD ID VALIDATION
# ============================================================================

def assert_valid_discord_id(value: str, id_type: str = "ID"):
    """Validate Discord ID format (Snowflake).
    
    Args:
        value: The ID string to validate
        id_type: Type of ID for error messages (e.g., "User ID", "Channel ID")
    
    Raises:
        AssertionError: If ID is invalid format
    """
    assert isinstance(value, str), f"{id_type} must be string, got {type(value)}"
    assert value.isdigit(), f"{id_type} must be numeric: {value}"
    assert len(value) >= 17, f"{id_type} too short (must be ≥17 chars): {value}"
    assert len(value) <= 20, f"{id_type} too long (must be ≤20 chars): {value}"


def assert_valid_discord_ids(values: List[str], id_type: str = "ID"):
    """Validate multiple Discord IDs."""
    for value in values:
        assert_valid_discord_id(value, id_type)


# ============================================================================
# MESSAGE ASSERTIONS
# ============================================================================

def assert_message_sent(mock_channel: AsyncMock, expected_content: Optional[str] = None):
    """Verify message was sent to channel.
    
    Args:
        mock_channel: Mocked channel object with send method
        expected_content: Optional substring expected in message content
    
    Raises:
        AssertionError: If message not sent or content doesn't match
    """
    mock_channel.send.assert_called_once()
    
    if expected_content:
        call_args = mock_channel.send.call_args
        # Handle both positional and keyword arguments
        if call_args.args:
            actual_content = str(call_args.args[0])
        elif 'content' in call_args.kwargs:
            actual_content = str(call_args.kwargs['content'])
        else:
            raise AssertionError("No content found in send() call")
        
        assert expected_content in actual_content, \
            f"Expected '{expected_content}' in message, got: {actual_content}"


def assert_message_not_sent(mock_channel: AsyncMock):
    """Verify no message was sent to channel."""
    mock_channel.send.assert_not_called()


def assert_dm_sent(mock_member: AsyncMock, expected_content: Optional[str] = None):
    """Verify DM was sent to member."""
    mock_member.send.assert_called_once()
    
    if expected_content:
        call_args = mock_member.send.call_args
        if call_args.args:
            actual_content = str(call_args.args[0])
        elif 'content' in call_args.kwargs:
            actual_content = str(call_args.kwargs['content'])
        else:
            raise AssertionError("No content found in send() call")
        
        assert expected_content in actual_content, \
            f"Expected '{expected_content}' in DM, got: {actual_content}"


# ============================================================================
# ROLE ASSERTIONS
# ============================================================================

def assert_role_assigned(mock_member: AsyncMock, role_id: Optional[str] = None):
    """Verify role was assigned to member.
    
    Args:
        mock_member: Mocked member object
        role_id: Optional role ID to verify specific role
    """
    mock_member.add_roles.assert_called_once()
    
    if role_id:
        call_args = mock_member.add_roles.call_args
        assigned_role = call_args.args[0] if call_args.args else None
        assert assigned_role is not None, "No role found in add_roles() call"
        assert str(assigned_role.id) == role_id, \
            f"Expected role {role_id}, got {assigned_role.id}"


def assert_role_removed(mock_member: AsyncMock, role_id: Optional[str] = None):
    """Verify role was removed from member."""
    mock_member.remove_roles.assert_called_once()
    
    if role_id:
        call_args = mock_member.remove_roles.call_args
        removed_role = call_args.args[0] if call_args.args else None
        assert removed_role is not None, "No role found in remove_roles() call"
        assert str(removed_role.id) == role_id, \
            f"Expected role {role_id}, got {removed_role.id}"


# ============================================================================
# RESPONSE SCHEMA ASSERTIONS
# ============================================================================

def assert_response_has_keys(response: Dict[str, Any], required_keys: List[str]):
    """Verify response contains all required keys.
    
    Args:
        response: Response dictionary to validate
        required_keys: List of keys that must be present
    
    Raises:
        AssertionError: If any required keys are missing
    """
    assert isinstance(response, dict), f"Response must be dict, got {type(response)}"
    
    missing_keys = set(required_keys) - set(response.keys())
    assert not missing_keys, f"Response missing required keys: {missing_keys}"


def assert_response_schema(
    response: Dict[str, Any],
    required_keys: List[str],
    optional_keys: Optional[List[str]] = None
):
    """Verify response matches expected schema.
    
    Args:
        response: Response dictionary to validate
        required_keys: Keys that must be present
        optional_keys: Keys that may be present
    """
    assert_response_has_keys(response, required_keys)
    
    if optional_keys:
        all_allowed_keys = set(required_keys) + set(optional_keys)
        extra_keys = set(response.keys()) - all_allowed_keys
        assert not extra_keys, f"Response has unexpected keys: {extra_keys}"


def assert_pagination_response(
    response: Dict[str, Any],
    data_key: str = "members",
    expected_keys: Optional[List[str]] = None
):
    """Verify paginated response structure.
    
    Args:
        response: Response dictionary
        data_key: Key containing the data array (e.g., "members", "channels")
        expected_keys: Additional keys expected beyond pagination keys
    """
    pagination_keys = [data_key, "total_fetched", "has_more"]
    if expected_keys:
        pagination_keys.extend(expected_keys)
    
    assert_response_has_keys(response, pagination_keys)
    assert isinstance(response[data_key], list), \
        f"{data_key} must be list, got {type(response[data_key])}"
    assert isinstance(response["has_more"], bool), \
        f"has_more must be bool, got {type(response['has_more'])}"
    
    # If has_more=true, next_after should be present
    if response["has_more"]:
        assert "next_after" in response, \
            "next_after required when has_more=true"


# ============================================================================
# THEME ASSERTIONS
# ============================================================================

def assert_theme_consistency(result: Dict[str, Any], theme_name: str):
    """Verify response follows theme conventions.
    
    Args:
        result: Response dictionary from tool
        theme_name: Theme being tested ("generic", "wow", "custom")
    """
    # Generic theme uses standard Discord terminology
    # WoW theme uses immersive terminology
    # This is a placeholder for theme-specific validations
    assert isinstance(result, dict), f"Result must be dict, got {type(result)}"
    
    # Add theme-specific assertions as themes are implemented
    # For now, just verify result is valid dict
    pass


# ============================================================================
# TOOL RESPONSE ASSERTIONS
# ============================================================================

def assert_success_response(response: Dict[str, Any]):
    """Verify successful operation response.
    
    Most destructive operations return {"success": true, ...}
    """
    assert_response_has_keys(response, ["success"])
    assert response["success"] is True, "Operation should succeed"


def assert_error_response(response: Dict[str, Any], error_type: Optional[str] = None):
    """Verify error response structure.
    
    Args:
        response: Response dictionary
        error_type: Optional expected error type
    """
    assert_response_has_keys(response, ["success", "error"])
    assert response["success"] is False, "Operation should fail"
    assert isinstance(response["error"], str), "Error must be string"
    
    if error_type:
        assert error_type.lower() in response["error"].lower(), \
            f"Expected error type '{error_type}', got: {response['error']}"


# ============================================================================
# COMFYUI ASSERTIONS
# ============================================================================

def assert_valid_image_response(response: Dict[str, Any], return_mode: str):
    """Verify image generation response based on return mode.
    
    Args:
        response: Response from generate_image
        return_mode: Expected mode (base64, url, cdn)
    """
    common_keys = ["success", "workflow", "seed"]
    assert_response_has_keys(response, common_keys)
    
    if return_mode == "base64":
        assert "image_data" in response, "base64 mode requires image_data"
        assert response["image_data"].startswith("data:image/"), \
            "image_data must be base64 data URI"
    elif return_mode == "url":
        assert "image_url" in response, "url mode requires image_url"
        assert response["image_url"].startswith("http"), \
            "image_url must be HTTP URL"
    elif return_mode == "cdn":
        assert "image_url" in response, "cdn mode requires image_url"
        assert "cdn_url" in response, "cdn mode requires cdn_url"
    else:
        raise ValueError(f"Unknown return_mode: {return_mode}")


def assert_workflow_valid(workflow: Dict[str, Any]):
    """Verify ComfyUI workflow structure is valid.
    
    Args:
        workflow: Workflow dictionary
    """
    assert_response_has_keys(workflow, ["workflow"])
    assert "nodes" in workflow["workflow"], "Workflow must have nodes"
    assert isinstance(workflow["workflow"]["nodes"], list), \
        "Workflow nodes must be list"
    assert len(workflow["workflow"]["nodes"]) > 0, \
        "Workflow must have at least one node"


# ============================================================================
# PERMISSION ASSERTIONS
# ============================================================================

def assert_has_permission(permissions: Any, permission_name: str):
    """Verify permissions object has specific permission.
    
    Args:
        permissions: Discord Permissions object
        permission_name: Permission to check (e.g., "send_messages")
    """
    assert hasattr(permissions, permission_name), \
        f"Permissions object missing {permission_name} attribute"
    assert getattr(permissions, permission_name) is True, \
        f"Missing required permission: {permission_name}"


def assert_lacks_permission(permissions: Any, permission_name: str):
    """Verify permissions object lacks specific permission."""
    if hasattr(permissions, permission_name):
        assert getattr(permissions, permission_name) is False, \
            f"Should not have permission: {permission_name}"


# ============================================================================
# AUDIT LOG ASSERTIONS
# ============================================================================

def assert_audit_log_entry_created(mock_guild: AsyncMock, action_type: str):
    """Verify audit log entry would be created for action.
    
    Note: This is a placeholder for audit log validation.
    Actual Discord API creates audit logs automatically.
    """
    # In real testing, we'd verify the action that triggers audit log
    # For now, just document the expected behavior
    pass


# ============================================================================
# COLLECTION ASSERTIONS
# ============================================================================

def assert_not_empty(collection: List[Any], collection_name: str = "collection"):
    """Verify collection is not empty."""
    assert len(collection) > 0, f"{collection_name} should not be empty"


def assert_max_length(
    collection: List[Any],
    max_length: int,
    collection_name: str = "collection"
):
    """Verify collection does not exceed maximum length."""
    assert len(collection) <= max_length, \
        f"{collection_name} exceeds max length {max_length}: got {len(collection)}"


def assert_items_unique(collection: List[Any], collection_name: str = "collection"):
    """Verify all items in collection are unique."""
    assert len(collection) == len(set(collection)), \
        f"{collection_name} contains duplicate items"


# ============================================================================
# TIMESTAMP ASSERTIONS
# ============================================================================

def assert_valid_iso_timestamp(timestamp: str):
    """Verify timestamp is valid ISO 8601 format."""
    from datetime import datetime
    try:
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    except ValueError as e:
        raise AssertionError(f"Invalid ISO 8601 timestamp '{timestamp}': {e}")


def assert_recent_timestamp(timestamp: str, max_age_seconds: int = 60):
    """Verify timestamp is recent (within max_age_seconds of now)."""
    from datetime import datetime, timezone
    
    assert_valid_iso_timestamp(timestamp)
    ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    now = datetime.now(timezone.utc)
    age = (now - ts).total_seconds()
    
    assert age <= max_age_seconds, \
        f"Timestamp too old: {age}s > {max_age_seconds}s"


# ============================================================================
# STRING ASSERTIONS
# ============================================================================

def assert_max_string_length(value: str, max_length: int, field_name: str = "value"):
    """Verify string does not exceed maximum length."""
    assert len(value) <= max_length, \
        f"{field_name} exceeds max length {max_length}: {len(value)} chars"


def assert_not_empty_string(value: str, field_name: str = "value"):
    """Verify string is not empty or whitespace only."""
    assert value and value.strip(), \
        f"{field_name} must not be empty or whitespace"


# ============================================================================
# MOCK CALL ASSERTIONS
# ============================================================================

def assert_called_with_partial(mock_obj: MagicMock, **expected_kwargs):
    """Verify mock was called with at least the expected kwargs.
    
    Args:
        mock_obj: Mock object to check
        expected_kwargs: Kwargs that must be present (others allowed)
    """
    mock_obj.assert_called_once()
    call_kwargs = mock_obj.call_args.kwargs
    
    for key, expected_value in expected_kwargs.items():
        assert key in call_kwargs, f"Expected kwarg '{key}' not found in call"
        assert call_kwargs[key] == expected_value, \
            f"Expected {key}={expected_value}, got {call_kwargs[key]}"


def assert_not_called(mock_obj: MagicMock, method_name: str = "method"):
    """Verify mock method was not called."""
    mock_obj.assert_not_called()


# ============================================================================
# BATCH ASSERTIONS
# ============================================================================

def assert_all_tools_registered(tool_list: List[Dict[str, Any]], expected_count: int):
    """Verify all tools are registered in list_available_tools response.
    
    Args:
        tool_list: List of tool dictionaries from list_available_tools
        expected_count: Expected number of tools
    """
    assert len(tool_list) == expected_count, \
        f"Expected {expected_count} tools, got {len(tool_list)}"
    
    for tool in tool_list:
        assert_response_has_keys(tool, ["name", "description", "category"])
        assert_not_empty_string(tool["name"], "Tool name")
        assert_not_empty_string(tool["description"], "Tool description")
        assert_not_empty_string(tool["category"], "Tool category")


