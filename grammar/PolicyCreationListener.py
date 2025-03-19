import warnings
from datetime import timedelta, datetime
from besser.BUML.metamodel.structural import (
    StringType, IntegerType, FloatType, TimeDeltaType
) # TODO: Check if necessary (for attr type validation)
from utils.policy_tree import PolicyNode
from utils.exceptions import (
    UndefinedAttributeException
)
from utils.gh_extension import (
    ActionEnum, Label, PullRequest
)
from utils.attribute_converters import (
    str_to_status_enum, str_to_action_enum, deadline_to_timedelta,
    str_to_platform_enum
)
from metamodel.governance import (
    SinglePolicy, Project, Activity, Task, Role, Individual,
    Deadline, MajorityPolicy, AbsoluteMajorityPolicy, LeaderDrivenPolicy,
    PhasedPolicy, OrderEnum, hasRole
)

from .govdslParser import govdslParser
from .govdslListener import govdslListener



class PolicyCreationListener(govdslListener):
    """
       This listener class generates a governance object model from a parsed DSL file.
    """
    def __init__(self):
        super().__init__()
        self.__policy = None
        self.__policy_scopes = {}
        self.__rules = {}

        # Maps to track attributes by policy ID
        self.__policy_rules_map = {}        # So we have a set for each policy. Maybe we could use a dict with the rule name as key. Same for following maps.
        self.__policy_scopes_map = {}
        self.__policy_participants_map = {}
        self.__policy_conditions_map = {}
        self.__policy_order_map = {}
        self.__policy_parameters_map = {}

        # Policy tree structure
        self.policy_tree = {}  # Maps policy ID to PolicyNode
        self.policy_stack = []  # Tracks the current policy context
        self.phased_policy_stack = []  # Tracks the current phased policies
        self.referenced_policies = set()  # Track policies referenced by others (like default policies)

    def get_policy(self):
        """Policy: Retrieves the Policy instance."""
        return self.__policy
    
    def find_descendant_nodes_by_type(self, node, target_type):
        """
        Recursively finds and returns all descendant nodes of a specified type.

        Args:
            node: The node to search for descendants. This can be any node in the parse tree.
            target_type: The type of node to match against. This should be a class type that 
                        the nodes are expected to be instances of.

        Returns:
            A list of nodes that are instances of the specified target type. 
            If no matching nodes are found, an empty list is returned.
        """
        matching_nodes = []

        if isinstance(node, target_type):
            matching_nodes.append(node)

        for i in range(node.getChildCount()):
            child = node.getChild(i)
            matching_nodes.extend(self.find_descendant_nodes_by_type(child, target_type))

        return matching_nodes
    
    def _construct_policy_objects(self):
        """Construct policy objects from leaves to root with scope inheritance"""
        # First identify all default policies that need to be processed first
        default_policies = set()
        for policy_id, parameters in self.__policy_parameters_map.items():
            if 'default' in parameters:
                default_policy_id = parameters['default']
                if default_policy_id in self.policy_tree:
                    default_policies.add(default_policy_id)
        
        # Identify leaf nodes (no children)
        leaves = [node for node in self.policy_tree.values() if not node.children]
                
        # Process nodes in dependency order (defaults first, then leaves, then up the tree)
        processed = set()
        # First process all default policies
        to_process = [self.policy_tree[pid] for pid in default_policies if pid in self.policy_tree]
        # Then add leaf nodes that aren't default policies
        to_process.extend([node for node in leaves if node.policy_id not in default_policies])
        
        while to_process:
            node = to_process.pop(0)
            
            # Skip if already processed
            if node.policy_id in processed:
                continue
            
            if node.is_nested and node.parent:
                # Inherit scope from parent for nested policies
                parent_scope = None
                if node.parent.policy_id in processed:
                    parent_scope = node.parent.policy_object.scope
                else:
                    # Parent not processed yet, requeue this node
                    to_process.append(node)
                    continue
            else:
                # Get scope directly from map for top-level policies
                parent_scope = self.__policy_scopes_map.get(node.policy_id)
                
            # phased policies
            if node.policy_type == "phased":
                # Check if all children are processed
                if not all(child.policy_id in processed for child in node.children):
                    # Put back in queue and process later
                    to_process.append(node)
                    continue
                
                # Get phases (child policies) and create phased policy
                phases = {child.policy_object for child in node.children}
                order = self.__policy_order_map.get(node.policy_id)
                # Collect all scopes from direct children
                combined_scopes = set() # TODO: Implement scope of phased policy
                
                node.policy_object = PhasedPolicy(name=node.policy_id,
                                            phases=phases,
                                            order=order,
                                            scope=parent_scope)  # Use the inherited/direct scope
            else: # single policy
                participants = self.__policy_participants_map.get(node.policy_id)
                scope = self.__policy_scopes_map.get(node.policy_id)
                conditions = self.__policy_conditions_map.get(node.policy_id)
                base_policy = SinglePolicy(name=node.policy_id,
                                                  conditions=conditions,
                                                  participants=participants,
                                                  scope=parent_scope)  # Use the inherited/direct scope
                match node.policy_type:
                    case "MajorityPolicy":
                        parameters = self.__policy_parameters_map.get(node.policy_id)
                        node.policy_object = MajorityPolicy.from_policy(base_policy, minVotes=parameters.get('minVotes'), ratio=parameters.get('ratio'))
                    case "AbsoluteMajorityPolicy":
                        parameters = self.__policy_parameters_map.get(node.policy_id)
                        node.policy_object = AbsoluteMajorityPolicy.from_policy(base_policy, minVotes=parameters.get('minVotes'), ratio=parameters.get('ratio'))
                    case "LeaderDrivenPolicy":
                        parameters = self.__policy_parameters_map.get(node.policy_id)
                        if 'default' not in parameters:
                            raise UndefinedAttributeException("default", message="LeaderDrivenPolicy must have a default policy defined.")
                        
                        default_policy_id = parameters['default']
                        default_node = self.policy_tree.get(default_policy_id)
                        
                        if not default_node:
                            raise UndefinedAttributeException("default", f"Default policy '{default_policy_id}' not found in policy tree.")
                            
                        default_policy = default_node.policy_object
                        if not default_policy:
                            # If the default policy hasn't been processed yet, prioritize it
                            if default_policy_id not in processed:
                                # Move the default policy to the front of the processing queue
                                to_process.insert(0, default_node)
                                # Re-add the current node to process after the default
                                to_process.append(node)
                                continue
                            else:
                                # This should not happen now with our improved ordering
                                raise UndefinedAttributeException("default", f"Default policy '{default_policy_id}' exists but has not been properly constructed.")
                            
                        node.policy_object = LeaderDrivenPolicy.from_policy(base_policy, default=default_policy)
            
            # Mark as processed
            processed.add(node.policy_id)
            
            # Add parent to processing queue if exists
            if node.parent and node.parent.policy_id not in processed:
                to_process.append(node.parent)
    
    def _register_scope_with_current_policy(self, scope_obj):
        """
        Registers a scope object (Activity, Project, Task) with the current policy.
        
        Args:
            scope_obj: The scope object to register
            
        Raises:
            RuntimeError: If not within a policy context
        """
        # Get the current policy context
        if not self.policy_stack:
            raise RuntimeError("Attempting to access policy stack, but it is empty.")
        
        current_policy_id = self.policy_stack[-1].policy_id
        
        # Initialize the scopes set for this policy if needed
        if current_policy_id in self.__policy_scopes_map:
            raise Exception("Scope already defined for policy.") # TODO: Handle this case
        
        # Associate the scope with the current policy
        self.__policy_scopes_map[current_policy_id] = scope_obj

    def _register_participant_with_current_policy(self, participant_obj):
        """
        Registers a participant object (Role, Individual) with the current policy.
        
        Args:
            participant_obj: The participant object to register
            
        Raises:
            RuntimeError: If not within a policy context
        """
        # Get the current policy context
        if not self.policy_stack:
            raise RuntimeError("Attempting to access policy stack, but it is empty.")
        
        current_policy_id = self.policy_stack[-1].policy_id
        
        # Initialize the participants set for this policy if needed
        if current_policy_id not in self.__policy_participants_map:
            self.__policy_participants_map[current_policy_id] = set()
        
        # Associate the participant with the current policy
        self.__policy_participants_map[current_policy_id].add(participant_obj)

    def _register_condition_with_current_policy(self, condition_obj):
        """
        Registers a condition object (VotingCondition, Deadline) with the current policy.
        
        Args:
            condition_obj: The condition object to register
            
        Raises:
            RuntimeError: If not within a policy context
        """
        # Get the current policy context
        if not self.policy_stack:
            raise RuntimeError("Attempting to access policy stack, but it is empty.")
        
        current_policy_id = self.policy_stack[-1].policy_id
        
        # Initialize the conditions set for this policy if needed
        if current_policy_id not in self.__policy_conditions_map:
            self.__policy_conditions_map[current_policy_id] = set()
        
        # Associate the condition with the current policy
        self.__policy_conditions_map[current_policy_id].add(condition_obj)
    
    def _register_rule_with_current_policy(self, rule):
        """
        Registers a rule object with the current policy.
        
        Args:
            rule: The rule object to register
            
        Raises:
            RuntimeError: If not within a policy context
        """
        # Get the current policy context
        if not self.policy_stack:
            raise RuntimeError("Attempting to access policy stack, but it is empty.")
        
        current_policy_id = self.policy_stack[-1].policy_id
        
        # Initialize the rules set for this policy if needed
        if current_policy_id not in self.__policy_rules_map:
            self.__policy_rules_map[current_policy_id] = set()
        
        # Associate the rule with the current policy
        self.__policy_rules_map[current_policy_id].add(rule)

    def enterTopLevelSinglePolicy(self, ctx:govdslParser.TopLevelSinglePolicyContext):
        """When entering a top-level single policy, create a node"""
        policy_id = ctx.ID().getText()
        node = PolicyNode(policy_id, ctx.policyType().getText(), is_nested=False)
        self.policy_tree[policy_id] = node
        self.policy_stack.append(node)
        
    def enterNestedSinglePolicy(self, ctx:govdslParser.NestedSinglePolicyContext):
        """When entering a nested single policy, create a node and establish parent-child relationship"""
        policy_id = ctx.ID().getText()
        node = PolicyNode(policy_id, ctx.policyType().getText(), is_nested=True)
        self.policy_tree[policy_id] = node
        
        # For nested policies, always establish parent-child relationship
        if self.policy_stack:
            self.policy_stack[-1].add_child(node)
            
        self.policy_stack.append(node)
    
    def enterTopLevelPhasedPolicy(self, ctx:govdslParser.TopLevelPhasedPolicyContext):
        """When entering a top-level phased policy, create a node"""
        policy_id = ctx.ID().getText()
        node = PolicyNode(policy_id, "phased", is_nested=False)
        self.policy_tree[policy_id] = node
        self.policy_stack.append(node)
        self.phased_policy_stack.append(node)
        
    def enterNestedPhasedPolicy(self, ctx:govdslParser.NestedPhasedPolicyContext):
        """When entering a nested phased policy, create a node and establish parent-child relationship"""
        policy_id = ctx.ID().getText()
        node = PolicyNode(policy_id, "phased", is_nested=True)
        self.policy_tree[policy_id] = node
        
        # For nested policies, always establish parent-child relationship
        if self.policy_stack:
            self.policy_stack[-1].add_child(node)
            
        self.policy_stack.append(node)
        self.phased_policy_stack.append(node)

    def enterOrder(self, ctx:govdslParser.OrderContext):
        order_type = ctx.orderType().getText()
        order_mode = ctx.orderMode().getText() if ctx.orderMode() else None
        order = None

        # Create the appropriate OrderEnum value
        if order_type == "Sequential":
            if order_mode == "exclusive":
                order = OrderEnum.SEQUENTIAL_EXCLUSIVE
            else: # TODO: Handle case where order mode is not specified
                order = OrderEnum.SEQUENTIAL_INCLUSIVE
        # TODO: Add other order types as needed (discuss w/ Jordi and Javi)
        
        # Register with current phased policy
        current_policy_id = self.policy_stack[-1].policy_id if self.policy_stack else None
        if current_policy_id:
            self.__policy_order_map[current_policy_id] = order
        else:
            raise Exception("Handling of policy_stack is incorrect.")

    def enterActivity(self, ctx:govdslParser.ActivityContext):
        activity_name = ctx.ID().getText()
        activity = Activity(name=activity_name, status=None) # TODO: relationship with tasks, tasks=activity_tasks)
        # self.__project_activities[activity_name] = activity # TODO: work in relationships
        self._register_scope_with_current_policy(activity)
    
    def enterTask(self, ctx:govdslParser.TaskContext):
        task_name = ctx.ID().getText()
        
        # Extract status if present
        status = None
        if ctx.taskContent().status():
            status = str_to_status_enum(ctx.taskContent().status().statusEnum().getText())
        
        task = None
        
        # That's the gh_extension part
        if ctx.taskType():
            task_type_str = ctx.taskType().getText().lower()
            if ctx.taskContent().status():
                raise UndefinedAttributeException("action", "This task must have an action defined.")
            if ctx.taskContent().action():
                action = str_to_action_enum(ctx.taskContent().action().actionEnum().getText())
                labels = None
            else: # Action with labels
                action = str_to_action_enum(ctx.taskContent().actionWithLabels().action().actionEnum().getText())
                label_count = len(ctx.taskContent().actionWithLabels().labels().ID())
                labels = set()
                for i in range(label_count):
                    l_id = ctx.taskContent().actionWithLabels().labels().ID(i).getText()
                    labels.add(Label(name=l_id))
            match task_type_str:
                case "pull request":
                    task = PullRequest(name=task_name, status=status, action=action, labels=labels) # TODO: Implement further task types
        else:
            task = Task(name=task_name, status=status)
        self._register_scope_with_current_policy(task)
    
    def enterProject(self, ctx:govdslParser.ProjectContext):
        project_name = ctx.ID().getText()
        platform_str = ctx.platform().getText()
        platform_enum = str_to_platform_enum(platform_str)
        repo_id = ctx.repoID().getText()
        project = Project(name=project_name, platform=platform_enum, project_id=repo_id, status=None) # TODO: relationship with activities, activities=set(self.__project_activities.values())
        self._register_scope_with_current_policy(project)
        
    def enterRoles(self, ctx:govdslParser.RolesContext): 

        roles = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.ParticipantIDContext)
        for r in roles:
            role = Role(name=r.ID().getText())
            self._register_participant_with_current_policy(role) # WARNING: This might generate conflict if there is a role with the same name as a individual
    
    def enterIndividuals(self, ctx:govdslParser.IndividualsContext):
        individuals = self.find_descendant_nodes_by_type(node=ctx,
                                                            target_type=govdslParser.IndividualIDContext)
        
        for i in individuals:
            i_name = i.participantID().ID().getText()
            individual = Individual(name=i_name)

            if i.hasRole():
                role_name = i.hasRole().participantID().ID().getText()
                # Find the role object, if already defined
                current_policy_id = self.policy_stack[-1].policy_id
                if current_policy_id in self.__policy_participants_map:
                    ref_role = Role(name=role_name)
                    # Check if the role exists in the set
                    if ref_role in self.__policy_participants_map[current_policy_id]:
                        # Get the actual role object from the set
                        role_obj = next(p for p in self.__policy_participants_map[current_policy_id] if p == ref_role)
                    else:
                        # Role can be created on the fly if not defined previosuly
                        role_obj = Role(name=role_name)
                        self._register_participant_with_current_policy(role_obj)

                    # Create hasRole relationship
                    scope = self.__policy_scopes_map.get(current_policy_id)
                    if scope:
                        role_assignment = hasRole(f"{i_name}_{role_name}", role_obj, individual, scope)
                        individual.role = role_assignment
                    else:
                        raise UndefinedAttributeException("scope", message="No scope defined for role assignment (Hint: Scope must be defined before Participants).")
              
            self._register_participant_with_current_policy(individual)
            
    def enterDeadline(self, ctx:govdslParser.DeadlineContext):
        name = ctx.deadlineID().ID().getText()
        offset = None
        date = None
        
        # Check for offset
        if ctx.offset():
            amount = int(ctx.offset().SIGNED_INT().getText())
            time_unit = ctx.offset().timeUnit().getText()
            offset = deadline_to_timedelta(value=amount, unit=time_unit)
        
        # Check for date
        if ctx.date():
            day = int(ctx.date().SIGNED_INT(0).getText())    # First SIGNED_INT is day
            month = int(ctx.date().SIGNED_INT(1).getText())  # Second SIGNED_INT is month
            year = int(ctx.date().SIGNED_INT(2).getText())   # Third SIGNED_INT is year
            date = datetime(year=year, month=month, day=day)
        
        deadline = Deadline(name=name, offset=offset, date=date)
        self._register_condition_with_current_policy(deadline)

    def enterParameters(self, ctx:govdslParser.ParametersContext):
        # Get the current policy context
        if not self.policy_stack:
            raise RuntimeError("Attempting to access policy stack, but it is empty.")
        
        current_policy_id = self.policy_stack[-1].policy_id
        
        # Initialize the parameters map for this policy if needed
        if current_policy_id not in self.__policy_parameters_map:
            self.__policy_parameters_map[current_policy_id] = {}
        
        # Extract voting parameters if present
        if ctx.votParams():
            vot_params = ctx.votParams()
            
            # Extract minVotes if present
            if vot_params.minVotes():
                self.__policy_parameters_map[current_policy_id]['minVotes'] = int(vot_params.minVotes().SIGNED_INT().getText())
            
            # Extract ratio if present
            if vot_params.ratio():
                self.__policy_parameters_map[current_policy_id]['ratio'] = float(vot_params.ratio().FLOAT().getText())
        
        # Extract default policy if present (for LeaderDrivenPolicy)
        elif ctx.default():
            default_ctx = None
            if ctx.default().policyContent().singlePolicy():
                default_ctx = ctx.default().policyContent().singlePolicy().ID().getText()
            elif ctx.default().policyContent().phasedPolicy():
                default_ctx = ctx.default().policyContent().phasedPolicy().ID().getText()
            self.__policy_parameters_map[current_policy_id]['default'] = default_ctx

    def enterDefault(self, ctx:govdslParser.DefaultContext):
        """When entering a default policy definition, ensure it's added to policy tree"""
        # Get the current policy context (the LeaderDrivenPolicy)
        if not self.policy_stack:
            raise RuntimeError("Attempting to access policy stack, but it is empty.")
        
        # Extract the default policy ID
        default_policy_id = None
        policy_type = None
        if ctx.policyContent().singlePolicy():
            default_policy_id = ctx.policyContent().singlePolicy().ID().getText()
            policy_type = ctx.policyContent().singlePolicy().policyType().getText()
        elif ctx.policyContent().phasedPolicy():
            default_policy_id = ctx.policyContent().phasedPolicy().ID().getText()
            policy_type = "phased"
        
        # Create a node for this default policy
        if default_policy_id and default_policy_id not in self.policy_tree:
            node = PolicyNode(default_policy_id, policy_type)
            self.policy_tree[default_policy_id] = node
            # Mark this policy as referenced so it's not considered a root policy
            self.referenced_policies.add(default_policy_id)
            
            # Set up parent-child relationship
            if self.policy_stack:
                current_policy = self.policy_stack[-1]
                # Don't add as a child to avoid it being processed as a phase

    def exitPolicy(self, ctx:govdslParser.PolicyContext):
        """Final policy construction using the tree structure"""
        # Build all objects from the tree (bottom-up)
        self._construct_policy_objects()
        
        # Set the root policy as the main policy, excluding referenced policies
        root_policies = [node for node in self.policy_tree.values() 
                         if node.parent is None and node.policy_id not in self.referenced_policies]

        # Should never enter here, but just in case
        if len(root_policies) > 1:
            raise Exception(f"Grammar violation: Found {len(root_policies)} root policies, but only one is allowed")
    
        if root_policies:
            self.__policy = root_policies[0].policy_object
        else:
            raise Exception("No root policy found. Grammar violation.")
