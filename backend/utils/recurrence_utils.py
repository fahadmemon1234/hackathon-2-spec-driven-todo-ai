"""
Utility functions for handling recurrence rules.

This module provides functions to parse and calculate
recurrence patterns for recurring tasks.
"""

import sys
import os
# Add the backend directory to the path so we can import from other modules if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from typing import Optional
from dateutil.rrule import rrulestr


def calculate_next_occurrence(recurrence_rule: str, start_date: datetime) -> Optional[datetime]:
    """
    Calculate the next occurrence based on the recurrence rule.
    
    Args:
        recurrence_rule: The recurrence rule in iCalendar RRULE format
                        (e.g., "FREQ=DAILY", "FREQ=WEEKLY;BYDAY=MO,WE")
        start_date: The date to calculate the next occurrence from
        
    Returns:
        The next occurrence date/time, or None if invalid rule
    """
    try:
        rule = rrulestr(recurrence_rule, dtstart=start_date)
        next_occurrence = next(rule.after(start_date))
        return next_occurrence
    except Exception as e:
        print(f"Error parsing recurrence rule '{recurrence_rule}': {e}")
        return None


def validate_recurrence_rule(recurrence_rule: str) -> bool:
    """
    Validate if the recurrence rule is in a proper format.
    
    Args:
        recurrence_rule: The recurrence rule to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not recurrence_rule or not isinstance(recurrence_rule, str):
        return False
    
    # Basic validation - check if it looks like an RRULE
    upper_rule = recurrence_rule.upper()
    if not upper_rule.startswith("FREQ="):
        return False
    
    # Check if FREQ value is valid
    freq_parts = [part for part in upper_rule.split(';') if part.startswith('FREQ=')]
    if not freq_parts:
        return False
    
    freq_value = freq_parts[0].split('=')[1]
    valid_freqs = {'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY'}
    if freq_value not in valid_freqs:
        return False
    
    return True