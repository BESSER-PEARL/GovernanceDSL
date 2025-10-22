from datetime import timedelta
from metamodel.governance import StatusEnum
from utils.chp_extension import ActionEnum

def str_to_status_enum(status_str: str) -> StatusEnum:
    """Convert a string to a StatusEnum value."""
    status_map = {
        'completed': StatusEnum.COMPLETED,
        'accepted': StatusEnum.ACCEPTED,
        'partial': StatusEnum.PARTIAL
    }
    return status_map.get(status_str.lower())

def str_to_action_enum(action_str: str) -> ActionEnum:
    """Convert a string to an ActionEnum value."""
    action_map = {
        'merge': ActionEnum.MERGE,
        'review': ActionEnum.REVIEW,
        'all': ActionEnum.ALL
    }
    return action_map.get(action_str.lower())

def deadline_to_timedelta(value: int, unit: str) -> timedelta:
    """Convert a deadline value and unit to a timedelta."""
    unit_map = {
        'days': 'days',
        'weeks': 'weeks', 
        'months': lambda v: timedelta(days=v*30),  # approximation
        'years': lambda v: timedelta(days=v*365)   # approximation
    }
    
    if unit in ['days', 'weeks']:
        return timedelta(**{unit_map[unit]: value})
    else:
        return unit_map[unit](value)
