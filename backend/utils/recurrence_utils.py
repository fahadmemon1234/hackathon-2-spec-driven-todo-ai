from datetime import datetime, timedelta
from typing import Optional


def calculate_next_occurrence(recurrence_rule: str, current_date: datetime) -> Optional[datetime]:
    """
    Calculate the next occurrence based on the recurrence rule.
    Supports daily, weekly, monthly, yearly patterns.
    """
    if not recurrence_rule:
        return None
    
    # Parse recurrence rule (simple format: DAILY, WEEKLY, MONTHLY, YEARLY)
    rule = recurrence_rule.upper()
    
    if rule == "DAILY":
        return current_date + timedelta(days=1)
    elif rule == "WEEKLY":
        return current_date + timedelta(weeks=1)
    elif rule == "MONTHLY":
        # Simple monthly calculation (adding ~30 days)
        return current_date + timedelta(days=30)
    elif rule == "YEARLY":
        return current_date + timedelta(days=365)
    else:
        # For more complex rules, you might want to use a library like dateutil
        # For now, return None for unsupported rules
        return None