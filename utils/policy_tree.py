class PolicyNode:
    def __init__(self, policy_id, policy_type):
        self.policy_id = policy_id
        self.policy_type = policy_type  # "Majority", "AbsoluteMajority", "LeaderDriven" or "phased"
        self.parent = None
        self.children = []
        self.policy_object = None  # The actual policy object (set later)
        
    def add_child(self, child_node):
        """Add a child policy node and establish the parent-child relationship"""
        self.children.append(child_node)
        child_node.parent = self
        
    def __str__(self):
        return f"{self.policy_type}Policy: {self.policy_id} (Children: {len(self.children)})"
