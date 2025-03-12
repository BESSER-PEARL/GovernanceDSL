from enum import Enum
from besser.BUML.metamodel.structural import NamedElement
from metamodel.governance import Task, StatusEnum

class ActionEnum(Enum):
    MERGE = 1
    REVIEW = 2
    ALL = 3

class Label(NamedElement):
    def __init__(self, name: str):
        super().__init__(name)

class PullRequest(Task):
    def __init__(self, name: str, status: StatusEnum, action: ActionEnum, labels: set[Label]):
        super().__init__(name, status)
        self.action = action
        self.labels = labels

    @property
    def action(self):
        return self.__action
    
    @action.setter
    def action(self, action: ActionEnum):
        self.__action = action  # Use the backing field instead of self.action

    @property
    def labels(self):
        return self.__labels
    
    @labels.setter
    def labels(self, labels: set[Label]):
        self.__labels = labels