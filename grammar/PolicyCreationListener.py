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
        """Construct policy objects from leaves to root"""
        # Identify leaf nodes first (no children)
        leaves = [node for node in self.policy_tree.values() if not node.children]
                
        # Process nodes in dependency order (leaves first)
        processed = set()
        to_process = leaves.copy()
        
        while to_process:
            node = to_process.pop(0)
            
            # Skip if already processed
            if node.policy_id in processed:
                continue
            
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
                combined_scopes = set() # TODO: Implement as Jordi suggested "De moment assumim que hi ha una WFR (well-formedness rule) que diu que els scopes de les singlepolicy es el mateix si formen part de la mateixa composedpolicy. Per tant la relació entre composedpolicy i scope és una relació derivada"
                # if not node.children:
                #     raise UndefinedAttributeException("phases", f"Phased policy {node.policy_id} does not have children defined.")
                # for child in node.children:
                #     if hasattr(child.policy_object, 'scopes'):
                #         combined_scopes.update(child.policy_object.scopes)
                #     else:
                #         raise UndefinedAttributeException("scope", f"Child policy {child.policy_id} does not have scopes defined.")
            
                node.policy_object = PhasedPolicy(name=node.policy_id,
                                            phases=phases,
                                            order=order,
                                            scope=combined_scopes)
            else: # single policy
                participants = self.__policy_participants_map.get(node.policy_id)
                scope = self.__policy_scopes_map.get(node.policy_id)
                conditions = self.__policy_conditions_map.get(node.policy_id)
                base_policy = SinglePolicy(name=node.policy_id,
                                                  conditions=conditions,
                                                  participants=participants,
                                                  scope=scope)
                match node.policy_type:
                    case "MajorityPolicy": # TODO: Should we evaluate whether the parameters are well defined (i.e., votParams and default)?
                        parameters = self.__policy_parameters_map.get(node.policy_id)
                        node.policy_object = MajorityPolicy.from_policy(base_policy, minVotes=parameters.get('minVotes'), ratio=parameters.get('ratio'))
                    case "AbsoluteMajorityPolicy":
                        parameters = self.__policy_parameters_map.get(node.policy_id)
                        node.policy_object = AbsoluteMajorityPolicy.from_policy(base_policy, minVotes=parameters.get('minVotes'), ratio=parameters.get('ratio'))
                    case "LeaderDrivenPolicy":
                        parameters = self.__policy_parameters_map.get(node.policy_id)
                        if 'default' not in parameters:
                            raise UndefinedAttributeException("default", message="LeaderDrivenPolicy must have a default policy defined.")
                        default_policy = self.policy_tree.get(parameters['default']).policy_object
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

    def enterSinglePolicy(self, ctx:govdslParser.SinglePolicyContext):
        """When entering a single policy, create a node and establish relationships"""
        policy_id = ctx.ID().getText()
        node = PolicyNode(policy_id, ctx.policyType().getText())
        self.policy_tree[policy_id] = node
        
        # If we're inside a phased policy, establish parent-child relationship
        if self.phased_policy_stack:
                        self.phased_policy_stack[-1].add_child(node)
        
        # Push to stack to track current context
        self.policy_stack.append(node)

    def exitSinglePolicy(self, ctx:govdslParser.SinglePolicyContext):
        """When exiting a single policy, pop from stack"""
        self.policy_stack.pop()

    def enterPhasedPolicy(self, ctx:govdslParser.PhasedPolicyContext):
        """When entering a phased policy, create a node"""
        policy_id = ctx.ID().getText()
        node = PolicyNode(policy_id, ctx.policyType().getText())
        self.policy_tree[policy_id] = node
        
        # If we're inside another phased policy, establish parent-child relationship
        if self.phased_policy_stack:
                        self.phased_policy_stack[-1].add_child(node)
        
        # Push to stack to track current context
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

    def exitPhasedPolicy(self, ctx:govdslParser.PhasedPolicyContext):
        """When exiting a phased policy, clear current and pop stack"""
        self.phased_policy_stack.pop()
        self.policy_stack.pop()

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

    def exitPolicy(self, ctx:govdslParser.PolicyContext):
        """Final policy construction using the tree structure"""
        # Build all objects from the tree (bottom-up)
        self._construct_policy_objects()
        
        # Set the root policy as the main policy
        root_policies = [node for node in self.policy_tree.values() if node.parent is None]

        # Should never enter here, but just in case
        if len(root_policies) > 1:
            raise Exception(f"Grammar violation: Found {len(root_policies)} root policies, but only one is allowed")
    
        if root_policies:
            self.__policy = root_policies[0].policy_object
        else:
            raise Exception("No root policy found. Grammar violation.") # Same as if

