"""
Utility functions for handling recurrence rules (RRULE) and generating recurrence dates.
"""

from datetime import datetime, timedelta
from typing import Optional, Union
from dateutil import rrule
from dateutil.parser import parse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_rrule_string(rrule_str: str) -> Optional[rrule.rrule]:
    """
    Parse an RRULE string and return a dateutil.rrule object.
    
    Args:
        rrule_str: String in RRULE format (e.g., "FREQ=DAILY;INTERVAL=1")
        
    Returns:
        rrule object or None if invalid
    """
    try:
        # Parse the RRULE string
        parsed_rule = rrule.rrulestr(rrule_str)
        return parsed_rule
    except Exception as e:
        logger.error(f"Invalid RRULE string '{rrule_str}': {str(e)}")
        return None


def get_next_occurrence(
    rrule_str: str, 
    start_date: datetime, 
    after_date: Optional[datetime] = None
) -> Optional[datetime]:
    """
    Get the next occurrence date based on the RRULE and start date.
    
    Args:
        rrule_str: String in RRULE format (e.g., "FREQ=DAILY;INTERVAL=1")
        start_date: The start date to calculate from
        after_date: Optional date to find the next occurrence after this date
                    If None, uses start_date
        
    Returns:
        Next occurrence datetime or None if invalid
    """
    try:
        rule = parse_rrule_string(rrule_str)
        if not rule:
            return None
            
        # Use after_date if provided, otherwise use start_date
        reference_date = after_date if after_date else start_date
        
        # Find the next occurrence after the reference date
        next_occurrence = rule.after(reference_date, inc=False)
        
        return next_occurrence
    except Exception as e:
        logger.error(f"Error calculating next occurrence for '{rrule_str}' after {reference_date}: {str(e)}")
        return None


def validate_recurrence_end_condition(
    rrule_str: str,
    current_occurrence_number: int,
    max_occurrences: Optional[int] = None,
    end_date: Optional[datetime] = None
) -> bool:
    """
    Check if the recurrence should end based on end conditions.
    
    Args:
        rrule_str: String in RRULE format
        current_occurrence_number: Current occurrence number in the series
        max_occurrences: Maximum number of occurrences allowed
        end_date: End date for recurrence
        
    Returns:
        True if recurrence should end, False otherwise
    """
    # Check max occurrences condition
    if max_occurrences is not None and current_occurrence_number >= max_occurrences:
        logger.info(f"Max occurrences reached: {current_occurrence_number}/{max_occurrences}")
        return True
    
    # Check end date condition
    if end_date is not None:
        rule = parse_rrule_string(rrule_str)
        if rule:
            # Check if the next occurrence would be after the end date
            next_after_end = rule.after(end_date, inc=False)
            if next_after_end is None:
                # No more occurrences after the end date
                return True
    
    return False


def convert_frequency_to_rrule(frequency: str, interval: int = 1) -> str:
    """
    Convert a simple frequency option to an RRULE string.
    
    Args:
        frequency: Frequency option ('daily', 'weekly', 'monthly', 'yearly')
        interval: Interval between occurrences (default 1)
        
    Returns:
        RRULE string
    """
    freq_map = {
        'daily': 'DAILY',
        'weekly': 'WEEKLY',
        'monthly': 'MONTHLY',
        'yearly': 'YEARLY'
    }
    
    upper_freq = frequency.upper()
    if frequency.lower() in freq_map:
        upper_freq = freq_map[frequency.lower()]
    
    return f"FREQ={upper_freq};INTERVAL={interval}"


def get_recurrence_display_text(rrule_str: str) -> str:
    """
    Get a human-readable display text for the recurrence rule.
    
    Args:
        rrule_str: String in RRULE format
        
    Returns:
        Human-readable recurrence description
    """
    try:
        # Simple parsing to extract frequency for display
        parts = rrule_str.split(';')
        freq_part = None
        interval = 1
        
        for part in parts:
            if part.startswith('FREQ='):
                freq_part = part.split('=')[1]
            elif part.startswith('INTERVAL='):
                interval = int(part.split('=')[1])
        
        if not freq_part:
            return "Unknown recurrence"
        
        # Map frequency to display text
        freq_display = {
            'DAILY': 'Daily',
            'WEEKLY': 'Weekly',
            'MONTHLY': 'Monthly',
            'YEARLY': 'Yearly'
        }
        
        freq_text = freq_display.get(freq_part, freq_part)
        
        if interval == 1:
            return f"Repeats {freq_text.lower()}"
        else:
            return f"Repeats every {interval} {freq_text.lower()}s"
            
    except Exception as e:
        logger.error(f"Error getting recurrence display text for '{rrule_str}': {str(e)}")
        return "Repeats with custom rule"


def calculate_next_occurrence(
    rrule_str: str,
    start_date: datetime
) -> Optional[datetime]:
    """
    Calculate the next occurrence date based on the RRULE and start date.

    Args:
        rrule_str: String in RRULE format (e.g., "FREQ=DAILY;INTERVAL=1")
        start_date: The start date to calculate from

    Returns:
        Next occurrence datetime or None if invalid
    """
    try:
        rule = parse_rrule_string(rrule_str)
        if not rule:
            return None

        # Find the next occurrence after the start date
        next_occurrence = rule.after(start_date, inc=False)

        return next_occurrence
    except Exception as e:
        logger.error(f"Error calculating next occurrence for '{rrule_str}' after {start_date}: {str(e)}")
        return None


def create_rrule_with_end_conditions(
    frequency: str,
    interval: int = 1,
    end_after_occurrences: Optional[int] = None,
    end_by_date: Optional[datetime] = None
) -> str:
    """
    Create an RRULE string with end conditions.

    Args:
        frequency: Frequency option ('daily', 'weekly', 'monthly', 'yearly')
        interval: Interval between occurrences
        end_after_occurrences: End after this many occurrences (COUNT)
        end_by_date: End by this date (UNTIL)

    Returns:
        Complete RRULE string with end conditions
    """
    rrule_parts = [convert_frequency_to_rrule(frequency, interval)]

    if end_after_occurrences is not None:
        rrule_parts.append(f"COUNT={end_after_occurrences}")
    elif end_by_date is not None:
        # Format date as YYYYMMDDTHHMMSSZ
        until_date = end_by_date.strftime("%Y%m%dT%H%M%S") + "Z"
        rrule_parts.append(f"UNTIL={until_date}")

    return ";".join(rrule_parts)


def convert_ui_recurrence_options_to_rrule(
    frequency: str,
    interval: int = 1,
    end_type: Optional[str] = None,  # 'none', 'after', 'on'
    end_after_count: Optional[int] = None,
    end_date: Optional[datetime] = None
) -> str:
    """
    Convert UI recurrence options to an RRULE string.

    Args:
        frequency: Frequency option ('daily', 'weekly', 'monthly', 'yearly')
        interval: Interval between occurrences (default 1)
        end_type: Type of end condition ('none', 'after', 'on')
        end_after_count: Number of occurrences for 'after' end type
        end_date: Date for 'on' end type

    Returns:
        RRULE string with all specified options
    """
    # Start with the basic frequency and interval
    rrule_parts = [convert_frequency_to_rrule(frequency, interval)]

    # Add end conditions based on the end_type
    if end_type == 'after' and end_after_count is not None:
        rrule_parts.append(f"COUNT={end_after_count}")
    elif end_type == 'on' and end_date is not None:
        # Format date as YYYYMMDDTHHMMSSZ
        until_date = end_date.strftime("%Y%m%dT%H%M%S") + "Z"
        rrule_parts.append(f"UNTIL={until_date}")

    return ";".join(rrule_parts)