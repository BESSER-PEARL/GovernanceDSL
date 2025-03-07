class InvalidVotesException(Exception):
    """Exception raised for invalid number of votes."""
    def __init__(self, votes, message="Invalid number of votes. It must be non-negative."):
        self.votes = votes
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.votes} -> {self.message}'

class InsufficientPhasesException(Exception):
    """Exception raised when a phased policy has fewer than two phases."""
    def __init__(self, policy_name, message="Phased policy must have at least two phases."):
        self.policy_name = policy_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.policy_name} -> {self.message}'

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

class UndefinedAttributeException(Exception):
    """Exception raised when a referenced attribute is not defined or not supported."""
    def __init__(self, attribute_type, attribute_value=None, message=None):
        self.attribute_type = attribute_type
        self.attribute_value = attribute_value
        # Generate a default message if none provided
        if message is None:
            message = f"{attribute_type} not defined or not supported."
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        if self.attribute_value is not None:
            return f'{self.attribute_type}: {self.attribute_value} -> {self.message}'
        return f'{self.attribute_type} -> {self.message}'
