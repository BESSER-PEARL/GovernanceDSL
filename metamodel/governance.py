from enum import Enum
from datetime import timedelta
from besser.BUML.metamodel.structural import NamedElement
from utils.exceptions import (
    InvalidVotesException, EmptySetException, 
    InvalidRatioException, 
)


# Scope hierarchy
class Scope(NamedElement):
    def __init__(self, name: str):
        super().__init__(name)

class Project(Scope):
    def __init__(self, name: str):
        super().__init__(name)

class Activity(Scope):
    def __init__(self, name: str):
        super().__init__(name)

class Task(Scope):
    def __init__(self, name: str):
        super().__init__(name)

# Rule
class Participant(NamedElement):
    def __init__(self, name: str):
        super().__init__(name)

class Individual(Participant):
    def __init__(self, name: str):
        super().__init__(name)

class Role(Participant):
    def __init__(self, name: str):
        super().__init__(name)


class Condition(NamedElement):
    def __init__(self, name: str):
        super().__init__(name)

class Deadline(Condition):
    def __init__(self, name: str, ts: timedelta):
        super().__init__(name)
        self.ts = ts
    
    @property
    def ts(self) -> timedelta:
        return self.__ts
    
    @ts.setter
    def ts(self, ts: timedelta):
        self.__ts = ts

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

class MajorityRule(Rule):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], min_votes: int):
        super().__init__(name, conditions, participants)
        self.min_votes = min_votes
    
    @classmethod
    def from_rule(cls, rule: Rule, min_votes: int):
        majority = cls(name=rule.name, conditions=rule.conditions, 
                      participants=rule.participants, min_votes=min_votes)
        return majority
    
    @property
    def min_votes(self) -> int:
        return self.__min_votes
    
    @min_votes.setter
    def min_votes(self, min_votes: int):
        if min_votes < 0:
            raise InvalidVotesException(min_votes)
        self.__min_votes = min_votes

class RatioMajorityRule(MajorityRule):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], min_votes: int, ratio: float):
        super().__init__(name, conditions, participants, min_votes)
        self.ratio = ratio
    
    @classmethod
    def from_rule(cls, rule: MajorityRule, min_votes: int, ratio: float):
        ratio_majority = cls(name=rule.name, conditions=rule.conditions, 
                             participants=rule.participants, min_votes=min_votes, ratio=ratio)
        return ratio_majority
    
    @property
    def ratio(self) -> float:
        return self.__ratio
    
    @ratio.setter
    def ratio(self, ratio: float):
        if ratio < 0 or ratio > 1:
            raise InvalidRatioException(ratio)
        self.__ratio = ratio
    
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