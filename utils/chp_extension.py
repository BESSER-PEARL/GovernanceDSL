from enum import Enum
from besser.BUML.metamodel.structural import Element
from metamodel.governance import Task, StatusEnum, Project, Condition, EvaluationMode

class ActionEnum(Enum):
    MERGE = 1
    REVIEW = 2
    ALL = 3

class MemberAction(Enum):
    ONBOARD = 1
    REMOVE = 2
    ALL = 3

class Label(Element):
    def __init__(self, name: str):
        self.name = name
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name

class CHPElement(Element):
    """Base class for code-hosting platform elements like PullRequest and Issue"""
    def __init__(self, name: str, labels: set[Label] = None):
        self.name = name
        self.labels = labels
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name
        
    @property
    def labels(self):
        return self.__labels
    
    @labels.setter
    def labels(self, labels: set[Label]):
        self.__labels = labels

class PullRequest(CHPElement):
    """Represents a Pull Request in code-hosting platforms"""
    def __init__(self, name: str, labels: set[Label] = None):
        super().__init__(name, labels)

class Issue(CHPElement):
    """Represents an Issue in code-hosting platforms"""
    def __init__(self, name: str, labels: set[Label] = None):
        super().__init__(name, labels)

class Repository(Project):
    """Represents a code-hosting platform Repository"""
    def __init__(self, name: str, status: StatusEnum, repo_id: str):
        super().__init__(name, status)
        self.repo_id = repo_id

    @classmethod
    def from_project(cls, project: Project, repo_id: str):
        repo = cls(name=project.name, status=project.status, 
                        repo_id=repo_id)
        return repo
    
    @property
    def repo_id(self) -> str:
        return self.__repo_id
    
    @repo_id.setter
    def repo_id(self, repo_id: str):
        self.__repo_id = repo_id

class MemberLifecycle(Task):
    """Represents the lifecycle of a member in a code-hosting platform"""
    def __init__(self, name: str, status: StatusEnum, action: MemberAction):
        super().__init__(name, status)
        self.action = action
    
    @property
    def action(self) -> MemberAction:
        return self.__action

    @action.setter
    def action(self, action: MemberAction):
        self.__action = action

class Patch(Task):
    """Represents an action (patch) that can be performed on a CHP element"""
    def __init__(self, name: str, status: StatusEnum, action: ActionEnum, element: CHPElement = None):
        super().__init__(name, status)
        self.action = action
        self.element = element
    
    @property
    def action(self):
        return self.__action
    
    @action.setter
    def action(self, action: ActionEnum):
        self.__action = action
    
    @property
    def element(self):
        return self.__element
    
    @element.setter
    def element(self, element: CHPElement):
        self.__element = element

class CheckCiCd(Condition):
    """Represents the condition of check CI/CD for a CHP element"""
    def __init__(self, name: str, evaluation_mode: EvaluationMode):
        super().__init__(name, evaluation_mode)

class LabelCondition(Condition):
    """Represents a condition based on labels for a CHP element"""
    def __init__(self, name: str, evaluation_mode: EvaluationMode, labels: set[Label], inclusion: bool = True):
        super().__init__(name, evaluation_mode)
        self.labels = labels
        self.inclusion = inclusion
    
    @property
    def labels(self):
        return self.__labels
    
    @labels.setter
    def labels(self, labels: set[Label]):
        self.__labels = labels

    @property
    def inclusion(self):
        return self.__inclusion
    
    @inclusion.setter
    def inclusion(self, inclusion: bool):
        self.__inclusion = inclusion