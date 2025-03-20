from enum import Enum
from besser.BUML.metamodel.structural import NamedElement
from metamodel.governance import Task, StatusEnum, Project

class ActionEnum(Enum):
    MERGE = 1
    REVIEW = 2
    ALL = 3

class Label(NamedElement):
    def __init__(self, name: str):
        super().__init__(name)

class GitHubElement(NamedElement):
    """Base class for GitHub elements like PullRequest and Issue"""
    def __init__(self, name: str, labels: set[Label] = None):
        super().__init__(name)
        self.labels = labels
    
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