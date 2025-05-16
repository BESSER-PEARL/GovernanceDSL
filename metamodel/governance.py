from enum import Enum
from datetime import timedelta, datetime  
from besser.BUML.metamodel.structural import Element
from utils.exceptions import (
    InvalidParticipantException, EmptySetException,
    InvalidValueException, InvalidDeadlineException,
    UndefinedAttributeException
)

# Enums
class StatusEnum(Enum):
    COMPLETED = 1
    ACCEPTED = 2
    PARTIAL = 3

class EvaluationMode(Enum):
    PRE = 1
    POST = 2
    CONCURRENT = 3

# Scope hierarchy
class Scope(Element):
    def __init__(self, name: str, status: StatusEnum):
        self.name = name
        self.status = status
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def status(self) -> StatusEnum:
        return self.__status
    
    @status.setter
    def status(self, status: StatusEnum):
        if status is not None and not isinstance(status, StatusEnum): # We can have None values
            raise UndefinedAttributeException("status", status)
        self.__status = status

class Project(Scope):
    def __init__(self, name: str, status: StatusEnum):
        super().__init__(name, status)
        self.__activities = None

    @property
    def activities(self) -> set['Activity']:
        return self.__activities
    
    @activities.setter
    def activities(self, activities: set['Activity']):
        self.__activities = activities
    
class Activity(Scope):
    def __init__(self, name: str, status: StatusEnum):
        super().__init__(name, status)
        self.__tasks = None
        self.__project = None

    @property
    def tasks(self) -> set['Task']:
        return self.__tasks
    
    @tasks.setter
    def tasks(self, tasks: set['Task']):
        self.__tasks = tasks

    @property
    def project(self) -> Project:
        return self.__project
    
    @project.setter
    def project(self, project: Project):
        self.__project = project
    

class Task(Scope):
    def __init__(self, name: str, status: StatusEnum):
        super().__init__(name, status)
        self.__activity = None

    @property
    def activity(self) -> Activity:
        return self.__activity
    
    @activity.setter
    def activity(self, activity: Activity):
        self.__activity = activity

# Participant
class Participant(Element):
    def __init__(self, name: str):
        self.name = name

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name

    def __eq__(self, value):
        if not isinstance(value, Participant):
            return False
        return self.name == value.name
    
    def __hash__(self):
        return hash(self.name)
    
class Profile(Element):
    def __init__(self, name: str, gender: str, race: str):
        self.name = name
        self.gender = gender
        self.race = race

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def gender(self) -> str:
        return self.__gender
    
    @gender.setter
    def gender(self, gender: str):
        self.__gender = gender

    @property
    def race(self) -> str:
        return self.__race
    
    @race.setter
    def race(self, race: str):
        self.__race = race

class Individual(Participant):
    def __init__(self, name: str, vote_value: float = 1.0, profile: Profile = None):
        super().__init__(name)
        self.__role_assignement = None
        self.vote_value = vote_value 
        self.profile = profile
    
    @property
    def role_assignement(self) -> 'hasRole':
        return self.__role_assignement
    
    @role_assignement.setter
    def role(self, role_assignement: 'hasRole'):
        self.__role_assignement = role_assignement

    @property
    def vote_value(self) -> float:
        return self.__vote_value
    
    @vote_value.setter
    def vote_value(self, vote_value: float):
        if vote_value < 0:
            raise InvalidValueException("vote_value", vote_value)
        self.__vote_value = vote_value
    
    @property
    def profile(self) -> Profile:
        return self.__profile
    
    @profile.setter
    def profile(self, profile: Profile):
        self.__profile = profile

class Agent(Individual):
    def __init__(self, name: str, confidence: float = 1.0):
        super().__init__(name, confidence)

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
        self.__individuals = None
    
    @property
    def individuals(self) -> set[Individual]:
        return self.__individuals
    
    @individuals.setter
    def individuals(self, individuals: set[Individual]):
        self.__individuals = individuals

class hasRole(Element):
    def __init__(self, name: str, role: Role, individual: Individual, scope: Scope):
        self.name = name
        self.role = role
        self.individual = individual
        self.scope = scope

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name
    
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
class Condition(Element):
    def __init__(self, name: str, evaluation_mode: EvaluationMode = None):
        self.name = name
        self.evaluation_mode = evaluation_mode

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def evaluation_mode(self) -> EvaluationMode:
        return self.__evaluation_mode
    
    @evaluation_mode.setter
    def evaluation_mode(self, evaluation_mode: EvaluationMode):
        self.__evaluation_mode = evaluation_mode

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

class ParticipantExclusion(Condition):
    def __init__(self, name: str, excluded: set[Individual]):
        super().__init__(name)
        self.excluded = excluded
    
    @property
    def excluded(self) -> set[Individual]:
        return self.__excluded
    
    @excluded.setter
    def excluded(self, excluded: set[Individual]):
        if excluded is None:
            raise UndefinedAttributeException("excluded", message="Participant relationship (excluded) must be defined.")
        self.__excluded = excluded

class MinimumParticipant(Condition):
    def __init__(self, name: str, min_participants: int):
        super().__init__(name)
        self.min_participants = min_participants
    
    @property
    def min_participants(self) -> int:
        return self.__min_participants
    
    @min_participants.setter
    def min_participants(self, min_participants: int):
        if min_participants < 1:
            raise InvalidParticipantException(min_participants)
        self.__min_participants = min_participants

class VetoRight(Condition):
    def __init__(self, name: str, vetoers: set[Participant]):
        super().__init__(name)
        self.vetoers = vetoers
    
    @property
    def vetoers(self) -> set[Participant]:
        return self.__vetoers
    
    @vetoers.setter
    def vetoers(self, vetoers: set[Participant]):
        self.__vetoers = vetoers

# DecisionType
class DecisionType(Element):
    def __init__(self, name: str):
        self.name = name

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name

class BooleanDecision(DecisionType):
    def __init__(self, name: str):
        super().__init__(name)

class CandidateChoice(DecisionType):
    def __init__(self, name: str):
        super().__init__(name)

class ElementList(CandidateChoice):
    def __init__(self, name: str, elements: set[Element]):
        super().__init__(name)
        self.elements = elements
    
    @property
    def elements(self) -> set[Element]:
        return self.__elements
    
    @elements.setter
    def elements(self, elements: set[Element]):
        if not elements:
            raise EmptySetException("elements")
        self.__elements = elements

class StringList(CandidateChoice):
    def __init__(self, name: str, options: set[str]):
        super().__init__(name)
        self.options = options

    @property
    def options(self) -> set[str]:
        return self.__options
    
    @options.setter
    def options(self, options: set[str]):
        if not options:
            raise EmptySetException("options")
        self.__options = options

# Policy hierarchy
class Policy(Element):
    """A Policy must have a scope, but it can be set after initialization."""
    def __init__(self, name: str, scope: Scope = None):
        self.name = name
        self.scope = scope
        self.__parent = None
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name
        
    @property
    def scope(self) -> Scope:
        return self.__scope
    
    @scope.setter
    def scope(self, scope: Scope):
        self.__scope = scope

    @property
    def parent(self) -> 'ComposedPolicy | None':  # String literal for forward reference
        return self.__parent
    
    @parent.setter
    def parent(self, parent: 'ComposedPolicy | None'):
        self.__parent = parent
    
    def validate(self):
        """Validates that the policy has all required properties before execution."""
        if not self.scope:
            raise EmptySetException("Policy must have a scope before execution")

class SinglePolicy(Policy):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], 
                 decision_type: DecisionType, scope: Scope = None):
        super().__init__(name, scope)
        self.conditions = conditions
        self.participants = participants
        self.decision_type = decision_type
        self.scope = scope
    
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
    
    @property
    def decision_type(self) -> DecisionType:
        return self.__decision_type
    
    @decision_type.setter
    def decision_type(self, decision_type: DecisionType):
        if decision_type is None:
            raise UndefinedAttributeException("decision_type", None)
        self.__decision_type = decision_type


class ConsensusPolicy(SinglePolicy):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], 
                 decision_type: DecisionType, scope: Scope):
        super().__init__(name, conditions, participants, decision_type, scope)

    @classmethod
    def from_policy(cls, policy: SinglePolicy):
        consensus = cls(name=policy.name, conditions=policy.conditions, 
                        participants=policy.participants, decision_type=policy.decision_type,
                        scope=policy.scope)
        return consensus
    

class LazyConsensusPolicy(SinglePolicy):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], 
                 decision_type: DecisionType, scope: Scope):
        super().__init__(name, conditions, participants, decision_type, scope)

    @classmethod
    def from_policy(cls, policy: SinglePolicy):
        lazy_consensus = cls(name=policy.name, conditions=policy.conditions, 
                             participants=policy.participants, decision_type=policy.decision_type,
                             scope=policy.scope)
        return lazy_consensus


class VotingPolicy(SinglePolicy):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], 
                 decision_type : DecisionType, scope: Scope, ratio: float = None):
        super().__init__(name, conditions, participants, decision_type, scope)
        self.ratio = ratio
    
    @classmethod
    def from_policy(cls, policy: SinglePolicy, ratio: float = None):
        voting = cls(name=policy.name, conditions=policy.conditions, 
                     participants=policy.participants, decision_type=policy.decision_type,
                     scope=policy.scope, ratio=ratio)
        return voting
    
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
                 decision_type: DecisionType, scope: Scope, ratio: float = None):
        super().__init__(name, conditions, participants, decision_type, scope, ratio)
    
    @classmethod
    def from_policy(cls, policy: SinglePolicy, ratio: float = None):
        if isinstance(policy, VotingPolicy):
            # Preserveratio if coming from VotingPolicy
            ratio = policy.ratio if ratio is None else ratio
        
        majority = cls(name=policy.name, conditions=policy.conditions, 
                       participants=policy.participants, decision_type=policy.decision_type,
                       scope=policy.scope, ratio=ratio)
        return majority


class AbsoluteMajorityPolicy(VotingPolicy):
    """AbsoluteMajorityPolicy extends VotingPolicy"""
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], 
                 decision_type: DecisionType, scope: Scope, ratio: float = None):
        super().__init__(name, conditions, participants, decision_type, scope, ratio)
    
    @classmethod
    def from_policy(cls, policy: SinglePolicy, ratio: float = None):
        if isinstance(policy, VotingPolicy):
            # Preserve ratio if coming from VotingPolicy
            ratio = policy.ratio if ratio is None else ratio
        
        abs_majority = cls(name=policy.name, conditions=policy.conditions, 
                           participants=policy.participants, decision_type=policy.decision_type,
                           scope=policy.scope, ratio=ratio)
        return abs_majority


class LeaderDrivenPolicy(SinglePolicy):
    """LeaderDrivenPolicy extends SinglePolicy and references another SinglePolicy as default"""
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], 
                 decision_type: DecisionType, scope: Scope, default: SinglePolicy = None):
        # Initialize default first to avoid issues during object creation
        self.__default = None
        super().__init__(name, conditions, participants, decision_type, scope)
        # Now set default through the property setter
        self.default = default
    
    @classmethod
    def from_policy(cls, policy: SinglePolicy, default: SinglePolicy):
        leader_driven = cls(name=policy.name, conditions=policy.conditions, 
                            participants=policy.participants, decision_type=policy.decision_type,
                            scope=policy.scope, default=default)
        return leader_driven

    @property
    def default(self) -> SinglePolicy:
        return self.__default
    
    @default.setter
    def default(self, default: SinglePolicy):
        self.__default = default
        # Only propagate scope after default is set
        if self.scope and default:
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


class ComposedPolicy(Policy):
    """A ComposedPolicy must have at least one phase."""
    def __init__(self, name: str, phases: list[Policy], sequential: bool, require_all: bool, carry_over: bool, scope: Scope = None):
        super().__init__(name, scope)
        self.phases = phases
        self.sequential = sequential
        self.require_all = require_all
        self.carry_over = carry_over # TODO: this does not make sense in parallel phases. Handle this.
        self.propagate_scope()
    
    @property
    def phases(self) -> list[Policy]:
        return self.__phases
    
    @phases.setter
    def phases(self, phases: list[Policy]):
        if not phases:  # Only check for None or empty
            raise EmptySetException("ComposedPolicy must have at least one phase.")
        self.__phases = phases

        # Set the parent reference for each phase
        for phase in phases:
            phase.parent = self
    
    @property
    def sequential(self) -> bool:
        return self.__sequential
    
    @sequential.setter
    def sequential(self, sequential: bool):
        self.__sequential = sequential

    @property
    def require_all(self) -> bool:
        return self.__require_all
    
    @require_all.setter
    def require_all(self, require_all: bool):
        self.__require_all = require_all

    @property
    def carry_over(self) -> bool:
        return self.__carry_over
    
    @carry_over.setter
    def carry_over(self, carry_over: bool):
        self.__carry_over = carry_over
    
    def propagate_scope(self):
        """Propagates the current scope to all child phases if set."""
        if self.scope and hasattr(self, '_ComposedPolicy__phases'):
            for phase in self.phases:
                phase.scope = self.scope
    
    @property
    def scope(self) -> Scope:
        return super().scope

    @scope.setter
    def scope(self, scope: Scope):
        super(ComposedPolicy, type(self)).scope.fset(self, scope)
        self.propagate_scope()