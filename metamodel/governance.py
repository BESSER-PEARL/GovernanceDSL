from enum import Enum
from datetime import timedelta, datetime  
from besser.BUML.metamodel.structural import NamedElement
from utils.exceptions import (
    InvalidVotesException, EmptySetException,
    InvalidRatioException, InvalidDeadlineException,
    UndefinedAttributeException
)

# Enums
class PlatformEnum(Enum):
    GITHUB = 1

class TaskTypeEnum(Enum):
    PULL_REQUEST = 1
    ISSUE = 2

# Scope hierarchy
class Scope(NamedElement):
    def __init__(self, name: str):
        super().__init__(name)

class Project(Scope):
    def __init__(self, name: str, platform: PlatformEnum, project_id: str):
        super().__init__(name)
        self.platform = platform
        self.project_id = project_id
    
    @property
    def platform(self) -> PlatformEnum:
        return self.__platform
    
    @platform.setter
    def platform(self, platform: PlatformEnum):
        if not isinstance(platform, PlatformEnum):
            raise UndefinedAttributeException("platform", platform)
        self.__platform = platform
    
    @property
    def project_id(self) -> str:
        return self.__project_id
    
    @project_id.setter
    def project_id(self, project_id: str):
        self.__project_id = project_id

class Activity(Scope):
    def __init__(self, name: str):
        super().__init__(name)

class Task(Scope):
    def __init__(self, name: str, task_type: TaskTypeEnum):
        super().__init__(name)
        self.task_type = task_type

    @property
    def task_type(self) -> TaskTypeEnum:
        return self.__task_type
    
    @task_type.setter
    def task_type(self, task_type: TaskTypeEnum):
        if not isinstance(task_type, TaskTypeEnum):
            raise UndefinedAttributeException("task_type", task_type)
        self.__task_type = task_type

# Participant
class Participant(NamedElement):
    def __init__(self, name: str):
        super().__init__(name)

class Individual(Participant):
    def __init__(self, name: str):
        super().__init__(name)

class Role(Participant):
    def __init__(self, name: str):
        super().__init__(name)

class hasRole(NamedElement):
    def __init__(self, name: str, role: Role, individual: Individual, scope: Scope):
        super().__init__(name)
        self.role = role
        self.individual = individual
        self.scope = scope
    
    @property
    def role(self) -> Role:
        return self.__role
    
    @role.setter
    def role(self, role: Role):
        if role is None:
            raise UndefinedAttributeException("role", None)
        self.__role = role
    
    @property
    def individual(self) -> Individual:
        return self.__individual
    
    @individual.setter
    def individual(self, individual: Individual):
        if individual is None:
            raise UndefinedAttributeException("individual", None)
        self.__individual = individual
    
    @property
    def scope(self) -> Scope:
        return self.__scope
    
    @scope.setter
    def scope(self, scope: Scope):
        if scope is None:
            raise UndefinedAttributeException("scope", None)
        self.__scope = scope


# Condition
class Condition(NamedElement):
    def __init__(self, name: str):
        super().__init__(name)

class Deadline(Condition):
    def __init__(self, name: str, offset: timedelta, date: datetime):
        super().__init__(name)
        if offset is None and date is None:
            raise InvalidDeadlineException(name)
        self.offset = offset
        self.date = date
    
    @property
    def offset(self) -> timedelta:
        return self.__offset
    
    @offset.setter
    def offset(self, offset: timedelta):
        if offset is None and self.date is None:
            raise InvalidDeadlineException(self.name)
        self.__offset = offset

    @property
    def date(self) -> datetime:
        return self.__date
    
    @date.setter
    def date(self, date: datetime):
        if date is None and self.offset is None:
            raise InvalidDeadlineException(self.name)
        self.__date = date

class VotingCondition(Condition):
    def __init__(self, name: str, minVotes: int, ratio: float):
        super().__init__(name)
        self.minVotes = minVotes
        self.ratio = ratio
    
    @property
    def minVotes(self) -> int:
        return self.__minVotes
    
    @minVotes.setter
    def minVotes(self, minVotes: int):
        if minVotes and minVotes < 0:
            raise InvalidVotesException("Number of votes must be non-negative.")
        self.__minVotes = minVotes
    
    @property
    def ratio(self) -> float:
        return self.__ratio
    
    @ratio.setter
    def ratio(self, ratio: float):
        if ratio and (ratio < 0 or ratio > 1):
            raise InvalidRatioException("Ratio must be between 0 and 1.")
        self.__ratio = ratio


# Rule
class Rule(NamedElement):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant]):
        super().__init__(name)
        self.conditions = conditions
        self.participants = participants
    
    @property
    def conditions(self) -> set[Condition]:
        return self.__conditions
    
    @conditions.setter
    def conditions(self, conditions: set[Condition]):
        if not conditions:  # Only check for None or empty
            raise EmptySetException("Rule must have at least one condition")
        self.__conditions = conditions

    @property
    def participants(self) -> set[Participant]:
        return self.__participants
    
    @participants.setter
    def participants(self, participants: set[Participant]):
        if not participants:  # Only check for None or empty
            raise EmptySetException("Rule must have at least one participant")
        self.__participants = participants

class VotingRule(Rule):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant]):
        super().__init__(name, conditions, participants)
    
    @classmethod
    def from_rule(cls, rule: Rule):
        voting = cls(name=rule.name, conditions=rule.conditions, participants=rule.participants)
        return voting


class MajorityRule(VotingRule):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant]):
        super().__init__(name, conditions, participants)
    
    @classmethod
    def from_rule(cls, rule: Rule):
        majority = cls(name=rule.name, conditions=rule.conditions, 
                      participants=rule.participants)
        return majority

class RatioMajorityRule(MajorityRule):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant]):
        super().__init__(name, conditions, participants)
    
    @classmethod
    def from_rule(cls, rule: MajorityRule):
        ratio_majority = cls(name=rule.name, conditions=rule.conditions, 
                           participants=rule.participants)
        return ratio_majority

class LeaderDrivenRule(Rule):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], default: Rule):
        super().__init__(name, conditions, participants)
        self.default = default
    
    @classmethod
    def from_rule(cls, rule: Rule, default: Rule):
        leader_driven = cls(name=rule.name, conditions=rule.conditions, 
                            participants=rule.participants, default=default)
        return leader_driven

    @property
    def default(self) -> Rule:
        return self.__default
    
    @default.setter
    def default(self, default: Rule):
        if not default:
            raise EmptySetException("LeaderDrivenRule must have a default rule")
        self.__default = default

# Policy
class Policy(NamedElement):
    """A Policy must have at least one rule and one scope."""
    def __init__(self, name: str):
        super().__init__(name)

class SinglePolicy(Policy):
    def __init__(self, name: str, rules: set[Rule], scopes: set[Scope]):
        super().__init__(name)
        self.rules = rules
        self.scope = scopes

    @property
    def rules(self) -> set[Rule]:
        return self.__rules
    
    @rules.setter
    def rules(self, rules: set[Rule]):
        if not rules:  # Only check for None or empty
            raise EmptySetException("Policy must have at least one rule")
        self.__rules = rules
    
    @property
    def scope(self) -> set[Scope]:
        return self.__scope
    
    @scope.setter
    def scope(self, scope: set[Scope]):
        if not scope:  # Only check for None or empty
            raise EmptySetException("Policy must have at least one scope")
        self.__scope = scope

class PhasedPolicy(Policy):
    """A PhasedPolicy must have at least one phase."""
    def __init__(self, name: str, phases: set[SinglePolicy]):
        super().__init__(name)
        self.phases = phases
    
    @property
    def phases(self) -> set[SinglePolicy]:
        return self.__phases
    
    @phases.setter
    def phases(self, phases: set[SinglePolicy]):
        if not phases:  # Only check for None or empty
            raise EmptySetException("PhasedPolicy must have at least one phase.")
        self.__phases = phases