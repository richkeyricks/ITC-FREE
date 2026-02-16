# src/modules/db/db_utils.py
"""
Database Utilities - Reusable Helpers
Gravity Rule 3: DRY - No code duplication.

This module contains:
- Payload validation
- UUID helpers
- Data transformation utilities
"""

import uuid
import re
from typing import Any, Dict, List, Optional

from .db_constants import MARKETPLACE_ORDER_COLUMNS, USER_PROFILE_COLUMNS


def is_valid_uuid(value: Any) -> bool:
    """Check if a value is a valid UUID string."""
    if value is None:
        return False
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, TypeError):
        return False


def sanitize_payload(data: Dict, allowed_columns: List[str]) -> Dict:
    """
    Filter payload to only include allowed columns.
    Prevents SQL injection and schema mismatch errors.
    """
    return {k: v for k, v in data.items() if k in allowed_columns}


def prepare_order_payload(order_data: Dict) -> Dict:
    """
    Prepare marketplace order payload with proper UUID handling.
    
    - If preset_id is not a valid UUID, treat it as tier name
    - Move tier name to preset_name column
    - Set preset_id to None for tier-based orders
    """
    payload = order_data.copy()
    
    preset_id = payload.get('preset_id')
    
    # If preset_id is a tier string (not UUID), handle it
    if preset_id and not is_valid_uuid(preset_id):
        # It's a tier name like "GOLD", "PLATINUM"
        payload['preset_name'] = payload.get('preset_name') or str(preset_id)
        payload['preset_id'] = None
    
    # Sanitize to allowed columns only
    return sanitize_payload(payload, MARKETPLACE_ORDER_COLUMNS)


def prepare_profile_update(profile_data: Dict) -> Dict:
    """
    Prepare user profile update payload.
    Ensures only valid columns are included.
    """
    return sanitize_payload(profile_data, USER_PROFILE_COLUMNS)


def strip_quotes(value: str) -> str:
    """Remove surrounding quotes from environment variable values."""
    if not value:
        return value
    return value.strip().strip("'").strip('"')


def safe_get_int(value: Any, default: int = 0) -> int:
    """Safely convert value to integer."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_get_float(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
