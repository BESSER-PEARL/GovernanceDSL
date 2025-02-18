from besser.BUML.metamodel.structural import NamedElement
from enum import Enum
import datetime

class CollaborationType(Enum):
    PULL_REQUEST = "PULL_REQUEST"
    ALL = "ALL"
    ISSUE = "ISSUE"

class Stage(Enum):
    TASK_REVIEW = "TASK_REVIEW"
    PATCH_REVIEW = "PATCH_REVIEW"
    RELEASE = "RELEASE"
    ALL = "ALL"

class RangeType(Enum):
    PRESENT = "PRESENT"
    QUALIFIED = "QUALIFIED"



class Project(NamedElement):
    def __init__(self, name: str, roles: set[Role], rules: set[Rule], deadlines: set[Deadline]):
        super().__init__(name)
        self.roles: set[Role] = roles
        self.rules: set[Rule] = rules
        self.deadlines: set[Deadline] = deadlines
    
    @property
    def roles(self) -> set[Role]:
        return self.__roles
    
    @roles.setter
    def roles(self, roles: set[Role]):
        self.__roles = roles

    @property
    def rules(self) -> set[Rule]:
        return self.__rules
    
    @rules.setter
    def rules(self, rules: set[Rule]):
        self.__rules = rules

    @property
    def deadlines(self) -> set[Deadline]:
        return self.__deadlines
    
    @deadlines.setter
    def deadlines(self, deadlines: set[Deadline]):
        self.__deadlines = deadlines

    def __repr__(self) -> str:
        return f'Project({self.name},{self.roles},{self.rules},{self.deadlines})'
    
class Role(NamedElement):
    def __init__(self, name: str):
        super().__init__(name)
        # self.parent: Any = parent # Needed?
    

    def __repr__(self) -> str:
        return f'Role({self.name})'
    
class Deadline(NamedElement):
    def __init__(self, name: str):
        super().__init__(name)
    
    def __repr__(self) -> str:
        return f'Deadline({self.name})'

class Timer(Deadline):
    def __init__(self, name: str, timestamp: int):
        super().__init__(name)
        self.timestamp: int = timestamp
    
    def __repr__(self) -> str:
        return f'Timer({self.name},{self.timestamp})'
    
class Condition(Deadline):
    def __init__(self, name: str, expression: str):
        super().__init__(name)
        self.expression: str = expression
    
    def __repr__(self) -> str:
        return f'Condition({self.name},{self.expression})'
    
class WaitForVote(Deadline):
    def __init__(self, name: str, roles: set[Role]):
        super().__init__(name)
        self.roles: set[Role] = roles
    
    def __repr__(self) -> str:
        return f'WaitForVote({self.name},{self.roles})'
    
class Rule(NamedElement):
    def __init__(self, name: str, applied_to: CollaborationType, stage: Stage, query_filter: str, deadline: Deadline, people: set[Role]):
        super().__init__(name)
        self.applied_to: str = applied_to
        self.stage: Stage = stage
        self.query_filter: str = query_filter
        self.deadline: Deadline = deadline
        self.people: set[Role] = people
    
    @property
    def applied_to(self) -> CollaborationType:
        return self.__applied_to
    
    @applied_to.setter
    def applied_to(self, applied_to: CollaborationType):
        self.__applied_to = applied_to

    @property
    def stage(self) -> Stage:
        return self.__stage
    
    @stage.setter
    def stage(self, stage: Stage):
        self.__stage = stage

    @property
    def query_filter(self) -> str:
        return self.__query_filter
    
    @query_filter.setter
    def query_filter(self, query_filter: str):
        self.__query_filter = query_filter
    
    @property
    def deadline(self) -> Deadline:
        return self.__deadline
    
    @deadline.setter
    def deadline(self, deadline: Deadline):
        self.__deadline = deadline
    
    @property
    def people(self) -> set[Role]:
        return self.__people
    
    @people.setter
    def people(self, people: set[Role]):
        self.__people = people
    
    def __repr__(self) -> str:
        return f'Rule({self.name},{self.applied_to},{self.stage},{self.query_filter},{self.deadline},{self.people})'

class LeaderDriven(Rule):
    def __init__(self, name: str, applied_to: CollaborationType, stage: Stage, query_filter: str, deadline: Deadline, people: set[Role], default: Rule):
        super().__init__(name, applied_to, stage, query_filter, deadline, people)
        self.default: Rule = default
    
    @property
    def default(self) -> Rule:
        return self.__default

    @default.setter
    def default(self, default: Rule):
        self.__default = default
    
    def __repr__(self) -> str:
        return f'LeaderDriven({self.name},{self.applied_to},{self.stage},{self.query_filter},{self.deadline},{self.people},{self.default})'

class Majority(Rule):
    def __init__(self, name: str, applied_to: CollaborationType, stage: Stage, query_filter: str, deadline: Deadline, people: set[Role], range_type: RangeType, min_votes: int):
        super().__init__(name, applied_to, stage, query_filter, deadline, people)
        self.range_type: RangeType = range_type
        self.min_votes: int = min_votes
    
    @property
    def range_type(self) -> RangeType:
        return self.__range_type

    @range_type.setter
    def range_type(self, range_type: RangeType):
        self.__range_type = range_type

    @property
    def min_votse(self) -> int:
        return self.__min_votes

    @min_votes.setter
    def min_votes(self, min_votes: int):
        self.__min_votes = min_votes
    
    def __repr__(self) -> str:
        return f'Majority({self.name},{self.applied_to},{self.stage},{self.query_filter},{self.deadline},{self.people},{self.range_type},{self.min_votes})'
    
class RatioMajority(Majority):
    def __init__(self, name: str, applied_to: CollaborationType, stage: Stage, query_filter: str, deadline: Deadline, people: set[Role], min_votes: int, ratio: float):
        super().__init__(name, applied_to, stage, query_filter, deadline, people, RangeType.QUALIFIED, min_votes)
        self.ratio: float = ratio
    
    @property
    def ratio(self) -> float:
        return self.__ratio
    
    @ratio.setter
    def ratio(self, ratio: float):
        self.__ratio = ratio
    
    def __repr__(self) -> str:
        return f'RatioMajority({self.name},{self.applied_to},{self.stage},{self.query_filter},{self.deadline},{self.people},{self.min_votes},{self.ratio})'

class Phased(Rule):
    def __init__(self, name: str, applied_to: CollaborationType, stage: Stage, query_filter: str, deadline: Deadline, people: set[Role], phases: list[Rule]):
        super().__init__(name, applied_to, stage, query_filter, deadline, people)
        self.phases: list[Rule] = phases
    
    @property
    def phases(self) -> list[Rule]:
        return self.__phases

    @phases.setter
    def phases(self, phases: list[Rule]):
        self.__phases = phases
    
    def __repr__(self) -> str:
        return f'Phased({self.name},{self.applied_to},{self.stage},{self.query_filter},{self.deadline},{self.people},{self.phases})'
