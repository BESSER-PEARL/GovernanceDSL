from enum import Enum
from datetime import timedelta
from besser.BUML.metamodel.structural import NamedElement



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

class Development(Activity):
    def __init__(self, name: str):
        super().__init__(name)

class Task(Scope):
    def __init__(self, name: str):
        super().__init__(name)

class PullRequestReview(Task):
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
            raise ValueError("Rule must have at least one condition")
        self.__conditions = conditions

    @property
    def participants(self) -> set[Participant]:
        return self.__participants
    
    @participants.setter
    def participants(self, participants: set[Participant]):
        if not participants:  # Only check for None or empty
            raise ValueError("Rule must have at least one participant")
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
            raise ValueError("min_votes must be greater than 0")
        self.__min_votes = min_votes
    

# Policy
class Policy(NamedElement):
    """A Policy must have at least one rule and one scope."""
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
            raise ValueError("Policy must have at least one rule")
        self.__rules = rules
    
    @property
    def scope(self) -> set[Scope]:
        return self.__scope
    
    @scope.setter
    def scope(self, scope: set[Scope]):
        if not scope:  # Only check for None or empty
            raise ValueError("Policy must have at least one scope")
        self.__scope = scope

class PhasedPolicy(NamedElement):
    def __init__(self, name: str, policies: set[Policy]):
        super().__init__(name)
        self.policies = policies
    
    @property
    def policies(self) -> set[Policy]:
        return self.__policies
    
    @policies.setter
    def policies(self, policies: set[Policy]):
        if not policies:  # Only check for None or empty
            raise ValueError("PhasedPolicy must have at least one policy")
        self.__policies = policies