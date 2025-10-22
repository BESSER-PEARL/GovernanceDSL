from datetime import timedelta
from metamodel.governance import StatusEnum
from utils.chp_extension import PatchAction, MemberAction

def str_to_status_enum(status_str: str) -> StatusEnum:
    """Convert a string to a StatusEnum value."""
    status_map = {
        'completed': StatusEnum.COMPLETED,
        'accepted': StatusEnum.ACCEPTED,
        'partial': StatusEnum.PARTIAL
    }
    return status_map.get(status_str.lower())

def str_to_action_enum(action_str: str) -> PatchAction:
    """Convert a string to a PatchAction value."""
    action_map = {
        'merge': PatchAction.MERGE,
        'review': PatchAction.REVIEW,
        'all': PatchAction.ALL
    }
    return action_map.get(action_str.lower())

def str_to_member_action_enum(action_str: str) -> MemberAction:
    """Convert a string to a MemberAction value."""
    action_map = {
        'onboard': MemberAction.ONBOARD,
        'remove': MemberAction.REMOVE
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
