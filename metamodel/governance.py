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
        self.conditions = []
        self.participants = []
    
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
        self.__participants = participants

class MajorityRule(Rule):
    def __init__(self, name: str, conditions: set[Condition], participants: set[Participant], min_votes: int):
        super().__init__(name, conditions, participants)
        self.min_votes = min_votes
    
    @property
    def min_votes(self) -> int:
        return self.__min_votes
    
    @min_votes.setter
    def min_votes(self, min_votes: int):
        self.__min_votes = min_votes
    

# Policy
class Policy(NamedElement):
    def __init__(self, name: str, rules: set[Rule], scope: Scope):
        super().__init__(name)
        self.rules = []
        self.scope = None

class PhasedPolicy(NamedElement):
    def __init__(self, name: str, policies: set[Policy]):
        super().__init__(name)
        self.policies = []
    
    @property
    def policies(self) -> set[Policy]:
        return self.__policies
    
    @policies.setter
    def policies(self, policies: set[Policy]):
        self.__policies = policies