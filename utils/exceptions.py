class InvalidVotesException(Exception):
    """Exception raised for invalid number of votes."""
    def __init__(self, votes, message="Invalid number of votes. It must be non-negative."):
        self.votes = votes
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.votes} -> {self.message}'

class InsufficientPhasesException(Exception):
    """Exception raised when a phased rule has fewer than two phases."""
    def __init__(self, rule_name, message="Phased rule must have at least two phases."):
        self.rule_name = rule_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.rule_name} -> {self.message}'

class UndefinedRuleException(Exception):
    """Exception raised when a referenced rule is not defined."""
    def __init__(self, rule_name, message="Rule not defined."):
        self.rule_name = rule_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.rule_name} -> {self.message}'

class UndefinedDeadlineException(Exception): # Maybe we could have a generic UndefinedElementException
    """Exception raised when a referenced deadline is not defined."""
    def __init__(self, deadline_name, message="Deadline not defined."):
        self.deadline_name = deadline_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.deadline_name} -> {self.message}'

class UnsupportedRuleTypeException(Exception):
    """Exception raised when a rule type is not supported."""
    def __init__(self, rule_type, message="Unsupported rule type."):
        self.rule_type = rule_type
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.rule_type} -> {self.message}'
