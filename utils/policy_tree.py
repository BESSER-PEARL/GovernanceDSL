class PolicyNode:
    """A node in the policy tree structure."""
    
    def __init__(self, policy_id, policy_type, is_nested=False, is_default=False, is_fallback=False):
        self.policy_id = policy_id
        self.policy_type = policy_type
        self.policy_object = None
        self.parent = None
        self.children = []
        self.is_nested = is_nested
        self.is_default = is_default
        self.is_fallback = is_fallback
    
    def add_child(self, child_node):
        """Add a child node to this node."""
        self.children.append(child_node)
        child_node.parent = self
        
    def __str__(self):
        return f"{self.policy_type}Policy: {self.policy_id} (Children: {len(self.children)})"
