from enum import Enum
from datetime import timedelta, datetime  
from besser.BUML.metamodel.structural import NamedElement
from utils.exceptions import (
    InvalidVotesException, EmptySetException,
    InvalidValueException, InvalidDeadlineException,
    UndefinedAttributeException
)

# Enums
class PlatformEnum(Enum):
    GITHUB = 1

class StatusEnum(Enum):
    COMPLETED = 1
    ACCEPTED = 2
    PARTIAL = 3

class OrderEnum(Enum):
    SEQUENTIAL_INCLUSIVE = 1
    SEQUENTIAL_EXCLUSIVE = 2

# Scope hierarchy
class Scope(NamedElement):
    def __init__(self, name: str, status: StatusEnum):
        super().__init__(name)
        self.status = status
    
    @property
    def status(self) -> StatusEnum:
        return self.__status
    
    @status.setter
    def status(self, status: StatusEnum):
        if status is not None and not isinstance(status, StatusEnum): # We can have None values
            raise UndefinedAttributeException("status", status)
        self.__status = status

class Project(Scope):
    def __init__(self, name: str, status: StatusEnum, platform: PlatformEnum, project_id: str):
        super().__init__(name, status)
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
    def __init__(self, name: str, status: StatusEnum):
        super().__init__(name, status)

class Task(Scope):
    def __init__(self, name: str, status: StatusEnum):
        super().__init__(name, status)

# Participant
class Participant(NamedElement):
    def __init__(self, name: str):
        super().__init__(name)

    def __eq__(self, value):
        if not isinstance(value, Participant):
            return False
        return self.name == value.name
    
    def __hash__(self):
        return hash(self.name)

class Individual(Participant):
    def __init__(self, name: str, confidence: float = 1.0):
        super().__init__(name)
        self.__role = None
        self.confidence = confidence
    
    @property
    def role(self) -> 'hasRole':
        return self.__role
    
    @role.setter
    def role(self, role_assignement: 'hasRole'):
        self.__role = role_assignement

    @property
    def confidence(self) -> float:
        return self.__confidence
    
    @confidence.setter
    def confidence(self, confidence: float):
        if confidence < 0 or confidence > 1:
            raise InvalidValueException("confidence", confidence)
        self.__confidence = confidence

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

# Policy hierarchy
class Policy(NamedElement):
    """A Policy must have a scope, but it can be set after initialization."""
    def __init__(self, name: str, scope: Scope = None):
        super().__init__(name)
        self.scope = scope
    
    @property
    def scope(self) -> Scope:
        return self.__scope
    
    @scope.setter
    def scope(self, scope: Scope):
        self.__scope = scope
    
    def validate(self):
        """Validates that the policy has all required properties before execution."""
        if not self.scope:
            raise EmptySetException("Policy must have a scope before execution")


class SinglePolicy(Policy):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], scope: Scope = None):
        super().__init__(name, scope)
        self.conditions = conditions
        self.participants = participants
    
    @property
    def conditions(self) -> set[Condition]:
        return self.__conditions
    
    @conditions.setter
    def conditions(self, conditions: set[Condition]):
        self.__conditions = conditions

    @property
    def participants(self) -> set[Participant]:
        return self.__participants
    
    @participants.setter
    def participants(self, participants: set[Participant]):
        if not participants:  # Only check for None or empty
            raise EmptySetException("Policy must have at least one participant")
        self.__participants = participants


class VotingPolicy(SinglePolicy):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], 
                 scope: Scope, minVotes: int = None, ratio: float = None):
        super().__init__(name, conditions, participants, scope)
        self.minVotes = minVotes
        self.ratio = ratio
    
    @classmethod
    def from_policy(cls, policy: SinglePolicy, minVotes: int = None, ratio: float = None):
        voting = cls(name=policy.name, conditions=policy.conditions, 
                     participants=policy.participants, scope=policy.scope,
                     minVotes=minVotes, ratio=ratio)
        return voting
    
    @property
    def minVotes(self) -> int:
        return self.__minVotes
    
    @minVotes.setter
    def minVotes(self, minVotes: int):
        if minVotes and minVotes < 0:
            raise InvalidVotesException("Number of votes must be positive.")
        self.__minVotes = minVotes
    
    @property
    def ratio(self) -> float:
        return self.__ratio
    
    @ratio.setter
    def ratio(self, ratio: float):
        if ratio and (ratio < 0 or ratio > 1):
            raise InvalidValueException("ratio", ratio)
        self.__ratio = ratio


class MajorityPolicy(VotingPolicy):
    """MajorityPolicy extends VotingPolicy"""
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], 
                 scope: Scope, minVotes: int = None, ratio: float = None):
        super().__init__(name, conditions, participants, scope, minVotes, ratio)
    
    @classmethod
    def from_policy(cls, policy: SinglePolicy, minVotes: int = None, ratio: float = None):
        if isinstance(policy, VotingPolicy):
            # Preserve minVotes and ratio if coming from VotingPolicy
            minVotes = policy.minVotes if minVotes is None else minVotes
            ratio = policy.ratio if ratio is None else ratio
        
        majority = cls(name=policy.name, conditions=policy.conditions, 
                       participants=policy.participants, scope=policy.scope,
                       minVotes=minVotes, ratio=ratio)
        return majority


class AbsoluteMajorityPolicy(VotingPolicy):
    """AbsoluteMajorityPolicy extends VotingPolicy"""
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], 
                 scope: Scope, minVotes: int = None, ratio: float = None):
        super().__init__(name, conditions, participants, scope, minVotes, ratio)
    
    @classmethod
    def from_policy(cls, policy: SinglePolicy, minVotes: int = None, ratio: float = None):
        if isinstance(policy, VotingPolicy):
            # Preserve minVotes and ratio if coming from VotingPolicy
            minVotes = policy.minVotes if minVotes is None else minVotes
            ratio = policy.ratio if ratio is None else ratio
        
        abs_majority = cls(name=policy.name, conditions=policy.conditions, 
                           participants=policy.participants, scope=policy.scope,
                           minVotes=minVotes, ratio=ratio)
        return abs_majority


class LeaderDrivenPolicy(SinglePolicy):
    """LeaderDrivenPolicy extends SinglePolicy and references another SinglePolicy as default"""
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], 
                 scope: Scope = None, default: SinglePolicy = None):
        # Initialize default first to avoid issues during object creation
        self.__default = None
        super().__init__(name, conditions, participants, scope)
        # Now set default through the property setter
        self.default = default
    
    @classmethod
    def from_policy(cls, policy: SinglePolicy, default: SinglePolicy):
        leader_driven = cls(name=policy.name, conditions=policy.conditions, 
                            participants=policy.participants, scope=policy.scope, 
                            default=default)
        return leader_driven

    @property
    def default(self) -> SinglePolicy:
        return self.__default
    
    @default.setter
    def default(self, default: SinglePolicy):
        if not default:
            raise EmptySetException("LeaderDrivenPolicy must have a default policy")
        self.__default = default
        # Only propagate scope after default is set
        if self.scope:
            self.default.scope = self.scope
    
    def propagate_scope(self):
        """Propagates the current scope to the default policy if set."""
        if self.scope and hasattr(self, '_LeaderDrivenPolicy__default') and self.__default:
            self.default.scope = self.scope
    
    @property
    def scope(self) -> Scope:
        return super().scope
    
    @scope.setter
    def scope(self, scope: Scope):
        super(LeaderDrivenPolicy, type(self)).scope.fset(self, scope)
        self.propagate_scope()


class PhasedPolicy(Policy):
    """A PhasedPolicy must have at least one phase."""
    def __init__(self, name: str, phases: set[Policy], order: OrderEnum, scope: Scope = None):
        super().__init__(name, scope)
        self.phases = phases
        self.order = order
        self.propagate_scope()
    
    @property
    def phases(self) -> set[Policy]:
        return self.__phases
    
    @phases.setter
    def phases(self, phases: set[Policy]):
        if not phases:  # Only check for None or empty
            raise EmptySetException("PhasedPolicy must have at least one phase.")
        self.__phases = phases
    
    @property
    def order(self) -> OrderEnum:
        return self.__order
    
    @order.setter
    def order(self, order: OrderEnum):
        if not isinstance(order, OrderEnum):
            raise UndefinedAttributeException("order", order)
        self.__order = order
    
    def propagate_scope(self):
        """Propagates the current scope to all child phases if set."""
        if self.scope and hasattr(self, '_PhasedPolicy__phases'):
            for phase in self.phases:
                phase.scope = self.scope
    
    @property
    def scope(self) -> Scope:
        return super().scope

    @scope.setter
    def scope(self, scope: Scope):
        super(PhasedPolicy, type(self)).scope.fset(self, scope)
        self.propagate_scope()