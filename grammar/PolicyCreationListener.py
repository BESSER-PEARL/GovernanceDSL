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
    ActionEnum, Label, PullRequest, Issue, Patch, Repository, GitHubElement
)
from utils.attribute_converters import (
    str_to_status_enum, str_to_action_enum, deadline_to_timedelta
)
from metamodel.governance import (
    SinglePolicy, Project, Activity, Task, Role, Individual,
    Deadline, MajorityPolicy, AbsoluteMajorityPolicy, LeaderDrivenPolicy,
    PhasedPolicy, OrderEnum, hasRole, ParticipantExclusion
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
        """Construct policy objects from leaves to root using the new scope propagation approach"""
        # First identify all default policies that need to be processed first
        default_policies = set()
        for _, parameters in self.__policy_parameters_map.items():
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
            
            # Get scope - now we can use None initially and set it later
            scope = self.__policy_scopes_map.get(node.policy_id)
            
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
                
                node.policy_object = PhasedPolicy(name=node.policy_id,
                                            phases=phases,
                                            order=order,
                                            scope=scope)
                
                # Scope will be automatically propagated to children by the PhasedPolicy class
            
            else: # single policy
                participants = self.__policy_participants_map.get(node.policy_id, set())
                conditions = self.__policy_conditions_map.get(node.policy_id, set())
                base_policy = SinglePolicy(name=node.policy_id,
                                            conditions=conditions,
                                            participants=participants,
                                            scope=scope)
                
                match node.policy_type:
                    case "MajorityPolicy":
                        parameters = self.__policy_parameters_map.get(node.policy_id, {})
                        node.policy_object = MajorityPolicy.from_policy(base_policy, 
                                                                       minVotes=parameters.get('minVotes'), 
                                                                       ratio=parameters.get('ratio'))
                    
                    case "AbsoluteMajorityPolicy":
                        parameters = self.__policy_parameters_map.get(node.policy_id, {})
                        node.policy_object = AbsoluteMajorityPolicy.from_policy(base_policy, 
                                                                               minVotes=parameters.get('minVotes'), 
                                                                               ratio=parameters.get('ratio'))
                    
                    case "LeaderDrivenPolicy":
                        parameters = self.__policy_parameters_map.get(node.policy_id, {})
                        if 'default' not in parameters:
                            raise UndefinedAttributeException("default", 
                                                            message="LeaderDrivenPolicy must have a default policy defined.")
                        
                        default_policy_id = parameters['default']
                        default_node = self.policy_tree.get(default_policy_id)
                        
                        if not default_node:
                            raise UndefinedAttributeException("default", 
                                                            f"Default policy '{default_policy_id}' not found in policy tree.")
                        
                        # If the default policy hasn't been processed yet, prioritize it
                        if default_policy_id not in processed:
                            # Move the default policy to the front of the processing queue
                            to_process.insert(0, default_node)
                            # Re-add the current node to process after the default
                            to_process.append(node)
                            continue
                            
                        default_policy = default_node.policy_object
                        node.policy_object = LeaderDrivenPolicy.from_policy(base_policy, default=default_policy)
                        
                        # Scope will be automatically propagated to default policy by the LeaderDrivenPolicy class
            
            # Mark as processed
            processed.add(node.policy_id)
            
            # Add parent to processing queue if exists and not processed
            if node.parent and node.parent.policy_id not in processed:
                to_process.append(node.parent)
        
        # Validate all policies to ensure scopes are set correctly
        for node in self.policy_tree.values():
            if hasattr(node, 'policy_object') and node.policy_object:
                node.policy_object.validate()
    
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
        
        # Handle GitHub extension elements
        if ctx.taskType():
            task_type_str = ctx.taskType().getText().lower()
            
            # Create the GitHub element (PullRequest or Issue)
            gh_element = None
            labels = None
            
            # Process labels if present
            if ctx.taskContent().actionWithLabels():
                label_count = len(ctx.taskContent().actionWithLabels().labels().ID())
                labels = set()
                for i in range(label_count):
                    l_id = ctx.taskContent().actionWithLabels().labels().ID(i).getText()
                    labels.add(Label(name=l_id))
            
            # Create the appropriate GitHub element based on task type
            if task_type_str == "pull request":
                gh_element = PullRequest(name=task_name, labels=labels)
            elif task_type_str == "issue":
                gh_element = Issue(name=task_name, labels=labels)
            
            # Extract action for Patch
            action = None
            if ctx.taskContent().action():
                action = str_to_action_enum(ctx.taskContent().action().actionEnum().getText())
            elif ctx.taskContent().actionWithLabels():
                action = str_to_action_enum(ctx.taskContent().actionWithLabels().action().actionEnum().getText())
            else:
                raise UndefinedAttributeException("action", "This task must have an action defined.")
            
            # Create the Patch object that references the GitHub element
            if gh_element:
                task = Patch(name=task_name, status=status, action=action, element=gh_element)
            else:
                # Fallback if no matching GitHub element type
                task = Task(name=task_name, status=status)
        else:
            # For regular tasks
            task = Task(name=task_name, status=status)
            
        self._register_scope_with_current_policy(task)
    
    def enterProject(self, ctx:govdslParser.ProjectContext):
        project_name = ctx.ID().getText()

        if ctx.platform():
            platform_str = ctx.platform().getText() # This will be used when we define further platforms
            id_tokens = ctx.repoID().ID()
            if len(id_tokens) > 1:  # If there are two IDs (owner/repo format)
                owner = id_tokens[0].getText()
                repo = id_tokens[1].getText()
                repo_id = f"{owner}/{repo}"
            else:  # If there's just one ID it means it is the user or organization
                repo_id = id_tokens[0].getText()
            status = None  # Status is usually set later
            repository = Repository(name=project_name, status=status, repo_id=repo_id)
        
            self._register_scope_with_current_policy(repository)
        else:
            project = Project(name=project_name, status=None)
            self._register_scope_with_current_policy(project)
        
    def enterRoles(self, ctx:govdslParser.RolesContext): 

        roles = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.ParticipantIDContext)
        for r in roles:
            role = Role(name=r.ID().getText())
            self._register_participant_with_current_policy(role) # WARNING: This might generate conflict if there is a role with the same name as a individual
    
    def enterIndividuals(self, ctx:govdslParser.IndividualsContext):
        individuals = self.find_descendant_nodes_by_type(node=ctx,
                                                            target_type=govdslParser.IndividualContext)
        
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
                    
            if i.confidence():
                individual.confidence = float(i.confidence().FLOAT().getText())
              
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
    
    def enterParticipantExclusion(self, ctx:govdslParser.ParticipantExclusionContext):
        # TODO: This condition needs more refinement. We will include primitive types, and multiple individuals
        individual = Individual(name=ctx.participantID().ID().getText())
        cond = ParticipantExclusion(name=ctx.ID().getText(), participant=individual)
        self._register_condition_with_current_policy(cond)

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
            if ctx.default().nestedPolicy().nestedSinglePolicy():
                default_ctx = ctx.default().nestedPolicy().nestedSinglePolicy().ID().getText()
            elif ctx.default().nestedPolicy().nestedPhasedPolicy():
                default_ctx = ctx.default().nestedPolicy().nestedPhasedPolicy().ID().getText()
            self.__policy_parameters_map[current_policy_id]['default'] = default_ctx

    def enterDefault(self, ctx:govdslParser.DefaultContext):
        # Get the current policy context (the LeaderDrivenPolicy)
        if not self.policy_stack:
            raise RuntimeError("Attempting to access policy stack, but it is empty.")
        
        # Extract the default policy ID
        default_policy_id = None
        policy_type = None
        if ctx.nestedPolicy().nestedSinglePolicy():
            default_policy_id = ctx.nestedPolicy().nestedSinglePolicy().ID().getText()
            policy_type = ctx.nestedPolicy().nestedSinglePolicy().policyType().getText()
        elif ctx.nestedPolicy().nestedPhasedPolicy():
            default_policy_id = ctx.nestedPolicy().nestedPhasedPolicy().ID().getText()
            policy_type = "phased"
        
        # Create a node for this default policy
        if default_policy_id and default_policy_id not in self.policy_tree:
            # Create the default policy node with is_nested=True to ensure scope inheritance
            node = PolicyNode(default_policy_id, policy_type, is_nested=True)
            # Add the is_default attribute to distinguish from phases
            node.is_default = True
            self.policy_tree[default_policy_id] = node
            
            # Mark this policy as referenced so it's not considered a root policy
            self.referenced_policies.add(default_policy_id)
            
            # Set up parent-child relationship with the current policy
            if self.policy_stack:
                current_policy = self.policy_stack[-1]
                current_policy.add_child(node)
                
                # Share the scope from parent to default policy
                if current_policy.policy_id in self.__policy_scopes_map:
                    parent_scope = self.__policy_scopes_map[current_policy.policy_id]
                    self.__policy_scopes_map[default_policy_id] = parent_scope

    def exitPolicy(self, ctx:govdslParser.PolicyContext):
        """Final policy construction using the tree structure"""
        # Build all objects from the tree (bottom-up)
        self._construct_policy_objects()
        
        # Set the root policy as the main policy, excluding referenced policies
        root_policies = [node for node in self.policy_tree.values() 
                         if node.parent is None and node.policy_id not in self.referenced_policies]

        # Should never enter here, but just in case
        if len(root_policies) != 1:
            raise Exception(f"Grammar violation: Found {len(root_policies)} root policies, but only one is allowed")        
        
        self.__policy = root_policies[0].policy_object
    
    def exitNestedSinglePolicy(self, ctx:govdslParser.NestedSinglePolicyContext):
        """When exiting a nested single policy, pop from stack"""
        self.policy_stack.pop()

    def exitNestedPhasedPolicy(self, ctx:govdslParser.NestedPhasedPolicyContext):
        """When exiting a nested phased policy, clear current and pop stack"""
        self.phased_policy_stack.pop()
        self.policy_stack.pop()

    def exitTopLevelSinglePolicy(self, ctx:govdslParser.TopLevelSinglePolicyContext):
        """When exiting a top-level single policy, pop from stack"""
        self.policy_stack.pop()

    def exitTopLevelPhasedPolicy(self, ctx:govdslParser.TopLevelPhasedPolicyContext):
        """When exiting a top-level phased policy, clear current and pop stack"""
        self.phased_policy_stack.pop()
        self.policy_stack.pop()
