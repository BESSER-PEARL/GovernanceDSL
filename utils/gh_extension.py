from enum import Enum
from besser.BUML.metamodel.structural import Element
from metamodel.governance import Task, StatusEnum, Project, Condition, EvaluationMode

class ActionEnum(Enum):
    MERGE = 1
    REVIEW = 2
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

class GitHubElement(Element):
    """Base class for GitHub elements like PullRequest and Issue"""
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

class PullRequest(GitHubElement):
    """Represents a Pull Request in GitHub"""
    def __init__(self, name: str, labels: set[Label] = None):
        super().__init__(name, labels)

class Issue(GitHubElement):
    """Represents an Issue in GitHub"""
    def __init__(self, name: str, labels: set[Label] = None):
        super().__init__(name, labels)

class Repository(Project):
    """Represents a GitHub Repository"""
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

class Patch(Task):
    """Represents an action (patch) that can be performed on a GitHub element"""
    def __init__(self, name: str, status: StatusEnum, action: ActionEnum, element: GitHubElement = None):
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
    def element(self, element: GitHubElement):
        self.__element = element

class PassedTests(Condition):
    """Represents the condition of passed tests for a GitHub element"""
    def __init__(self, name: str, evaluation_mode: EvaluationMode):
        super().__init__(name, evaluation_mode)