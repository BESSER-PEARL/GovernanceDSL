class InvalidVotesException(Exception):
    """Exception raised for invalid number of votes."""
    def __init__(self, votes, message="Invalid number of votes. It must be non-negative."):
        self.votes = votes
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.votes} -> {self.message}'
