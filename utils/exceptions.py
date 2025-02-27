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

class UndefinedConditionException(Exception): # Maybe we could have a generic UndefinedElementException
    """Exception raised when a referenced condition is not defined."""
    def __init__(self, condition_name, message="Condition not defined."):
        self.condition_name = condition_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.condition_name} -> {self.message}'

class InvalidDeadlineException(Exception):
    """Exception raised when both offset and date are null in a Deadline."""
    def __init__(self, deadline_name, message="Deadline must have either offset or date defined."):
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

class UndefinedParticipantException(Exception):
    """Exception raised when a referenced participant is not defined."""
    def __init__(self, participant_name, message="Participant not defined."):
        self.participant_name = participant_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.participant_name} -> {self.message}'

class UndefinedScopeException(Exception):
    """Exception raised when a referenced scope is not defined."""
    def __init__(self, scope_name, message="Scope not defined."):
        self.scope_name = scope_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.scope_name} -> {self.message}'

class EmptySetException(Exception):
    """Exception raised when a set (of conditions, participants, etc.) is empty. This checks for cardinality of 1 or more."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class InvalidRatioException(Exception):
    """Exception raised when a ratio is not between 0 and 1."""
    def __init__(self, ratio, message="Ratio must be between 0 and 1."):
        self.ratio = ratio
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.ratio} -> {self.message}'

