"""
Priority-related constants and validation functions for the Todo app.
"""

# Priority constants
PRIORITY_HIGH = "High"
PRIORITY_MEDIUM = "Medium"
PRIORITY_LOW = "Low"

# Valid priorities set
VALID_PRIORITIES = {PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW}


def validate_priority(priority: str) -> bool:
    """
    Validate if the given priority is one of the valid priorities.
    
    Args:
        priority: Priority level to validate
        
    Returns:
        True if priority is valid, False otherwise
    """
    return priority in VALID_PRIORITIES


def is_valid_priority(priority: str) -> bool:
    """
    Check if the given priority is valid.
    
    Args:
        priority: Priority level to check
        
    Returns:
        True if priority is valid, False otherwise
    """
    return validate_priority(priority)


def get_priority_value(priority: str) -> str:
    """
    Get the standardized priority value.
    
    Args:
        priority: Priority level to standardize
        
    Returns:
        Standardized priority value
        
    Raises:
        ValueError: If priority is not valid
    """
    if not validate_priority(priority):
        raise ValueError(f"Priority must be one of {VALID_PRIORITIES}, got {priority}")
    return priority