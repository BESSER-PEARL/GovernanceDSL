class InvalidParticipantException(Exception):
    """Exception raised for invalid number of participants."""
    def __init__(self, participants, message="Invalid number of participants. It must be positive."):
        self.message = message
        super().__init__(self.message)
        self.message = f"Invalid number of participants. It must be positive, but got {participants}."

    def __str__(self):
        return f'Number of participants -> {self.message}'

class InsufficientPhasesException(Exception):
    """Exception raised when a phased policy has fewer than two phases."""
    def __init__(self, policy_name, message="Phased policy must have at least two phases."):
        self.policy_name = policy_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.policy_name} -> {self.message}'

class InvalidTimeConditionException(Exception):
    """Exception raised when both offset and date are null in a Deadline or MinDecisionTime condition."""
    def __init__(self, cond_name, message="Deadline or MinDecisionTime condition must have either offset or date defined."):
        self.cond_name = cond_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.cond_name} -> {self.message}'

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

class InvalidValueException(Exception):
    """Exception raised when a value is outside of its acceptable range (typically 0-1)."""
    def __init__(self, attribute_name: str, value, min_value=0, max_value=1):
        self.attribute_name = attribute_name
        self.value = value
        self.min_value = min_value
        if attribute_name == "vote_value":
            max_value = 2
        else:
            self.max_value = max_value
        self.message = f"{attribute_name} must be between {min_value} and {max_value}, but got {value}."
        super().__init__(self.message)

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

class InvalidScopeException(Exception):
    """Exception raised when a scope is invalid or inconsistent with its parent."""
    def __init__(self, scope, scope_parent, message="Default or fallback policies must have the same scope as their parent policies."):
        self.scope = scope.name
        self.scope_parent = scope_parent.name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Scope: {self.scope} (parent: {self.scope_parent}) -> {self.message}'