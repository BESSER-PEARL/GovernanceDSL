import warnings
from datetime import timedelta, datetime
from besser.BUML.metamodel.structural import (
    StringType, IntegerType, FloatType, TimeDeltaType
) # TODO: Check if necessary (for attr type validation)
from utils.policy_tree import PolicyNode
from utils.exceptions import (
    UndefinedAttributeException, DuplicateAttributeException
)
from utils.chp_extension import (
    PatchAction, MemberAction, Label, PullRequest, Repository,
    CheckCiCd, LabelCondition, MinTime, MemberLifecycle, Patch
)
from utils.attribute_converters import (
    str_to_status_enum, str_to_action_enum, deadline_to_timedelta, str_to_member_action_enum
)
from metamodel.governance import (
    AppealRight, CommunicationChannel, Human, MinDecisionTime, SinglePolicy, Project, Activity, Task, Role, Individual,
    Deadline, MajorityPolicy, AbsoluteMajorityPolicy, LeaderDrivenPolicy,
    ComposedPolicy, hasRole, ParticipantExclusion, LazyConsensusPolicy,
    ConsensusPolicy, MinimumParticipant, VetoRight, Agent, BooleanDecision,
    ElementList, StringList, EvaluationMode, Profile
)
from .govdslParser import govdslParser
from .govdslListener import govdslListener



class PolicyCreationListener(govdslListener):
    """
       This listener class generates a governance object model from a parsed DSL file.
    """
    def __init__(self):
        super().__init__()
        self.__policies = []

        # Maps to track attributes by policy ID
        self.__policy_rules_map = {}        # So we have a set for each policy. Maybe we could use a dict with the rule name as key. Same for following maps.
        self.__policy_scopes_map = {}
        self.__policy_participants_map = {}
        self.__policy_conditions_map = {}
        self.__policy_order_map = {}
        self.__policy_parameters_map = {}
        self.__policy_decision_type_map = {}
        self.__communication_channels_map = {}
        self.__appeal_policy_map = {}

        # Maps to track scopes and participants predefined
        self.__scopes_map = {}
        self.__participants_map = {}
        self.__profiles_map = {}

        # Policy tree structure
        self.policy_tree = {}  # Maps policy ID to PolicyNode
        self.policy_stack = []  # Tracks the current policy context
        self.composed_policy_stack = []  # Tracks the current composed policies
        self.referenced_policies = set()  # Track policies referenced by others (only inline default/fallback policies)

    def get_policies(self):
        """Policies: Retrieves the Policy instances."""
        return self.__policies
    
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
        
        # Same with fallback policies
        fallback_policies = set()
        for _, parameters in self.__policy_parameters_map.items():
            if 'fallback' in parameters:
                fallback_policy_id = parameters['fallback']
                if fallback_policy_id in self.policy_tree:
                    fallback_policies.add(fallback_policy_id)
        
        # Identify leaf nodes (no children)
        leaves = [node for node in self.policy_tree.values() if not node.children]
                
        # Process nodes in dependency order (defaults first, then leaves, then up the tree)
        processed = set()
        
        # First process all default policies
        to_process = [self.policy_tree[pid] for pid in default_policies if pid in self.policy_tree]
        # Then all fallback policies
        to_process.extend([self.policy_tree[pid] for pid in fallback_policies if pid in self.policy_tree])
        # Then any inline appeal policies (those present in policy_tree as nested nodes)
        appeal_inline_ids = set()
        for _, pairs in self.__appeal_policy_map.items():
            for _, target_id in pairs:
                if target_id in self.policy_tree and self.policy_tree[target_id].is_nested:
                    appeal_inline_ids.add(target_id)
        to_process.extend([self.policy_tree[pid] for pid in appeal_inline_ids if pid in self.policy_tree])
        
        # Then add leaf nodes that aren't default, fallback or appeal (inline) policies
        not_default_nor_fallback = [node for node in leaves if node.policy_id not in default_policies and node.policy_id not in fallback_policies and node.policy_id not in appeal_inline_ids]
        to_process.extend(not_default_nor_fallback)

        while to_process:
            node = to_process.pop(0)
            
            # Skip if already processed
            if node.policy_id in processed:
                continue
            
            # Get scope 
            scope = self.__policy_scopes_map.get(node.policy_id)
            
            # composed policies
            if node.policy_type == "composed":
                # Check if all children are processed
                if not all(child.policy_id in processed for child in node.children):
                    # Put back in queue and process later
                    to_process.append(node)
                    continue
                
                # Get phases (child policies) and create composed policy
                phases = [child.policy_object for child in node.children]
                order = self.__policy_order_map.get(node.policy_id)
                
                node.policy_object = ComposedPolicy(name=node.policy_id,
                                            phases=phases,
                                            sequential=order.get('sequential'),
                                            require_all=order.get('require_all'),
                                            carry_over=order.get('carry_over'),
                                            scope=scope)
                
                # Scope will be automatically propagated to children by the ComposedPolicy class
            
            else: # single policy
                decision_type = self.__policy_decision_type_map.get(node.policy_id)
                channel = self.__communication_channels_map.get(node.policy_id)
                participants = self.__policy_participants_map.get(node.policy_id, set())
                conditions = self.__policy_conditions_map.get(node.policy_id, set())
                base_policy = SinglePolicy(name=node.policy_id,
                                            conditions=conditions,
                                            participants=participants,
                                            decision_type=decision_type,
                                            channel=channel,
                                            scope=scope)
                
                match node.policy_type:
                    case "ConsensusPolicy":
                        parameters = self.__policy_parameters_map.get(node.policy_id, {})
                        fallback_policy_id = parameters.get('fallback')
                        
                        fallback_policy = None
                        if fallback_policy_id:
                            # Check if it's a root policy reference
                            if fallback_policy_id in [n.policy_id for n in not_default_nor_fallback]:
                                if fallback_policy_id not in processed:
                                    # Process the referenced root policy first
                                    continue
                                # Find the already-processed root policy
                                fallback_node = next(n for n in not_default_nor_fallback if n.policy_id == fallback_policy_id)
                                default_policy = fallback_node.policy_object
                            else:
                                fallback_node = self.policy_tree.get(fallback_policy_id)
                                if not fallback_node:
                                    raise UndefinedAttributeException("fallback", 
                                                                f"fallback policy '{fallback_policy_id}' not found in policy tree.")
                            
                                # If the fallback policy hasn't been processed yet, prioritize it
                                if fallback_policy_id not in processed:
                                    # Move the fallback policy to the front of the processing queue
                                    to_process.insert(0, fallback_node)
                                    # Re-add the current node to process after the fallback
                                    to_process.append(node)
                                    continue
                            
                            fallback_policy = fallback_node.policy_object
                        node.policy_object = ConsensusPolicy.from_policy(base_policy, fallback=fallback_policy)
                    case "LazyConsensusPolicy":
                        parameters = self.__policy_parameters_map.get(node.policy_id, {})
                        fallback_policy_id = parameters.get('fallback')
                        
                        fallback_policy = None
                        if fallback_policy_id:
                            # Check if it's a root policy reference
                            if fallback_policy_id in [n.policy_id for n in not_default_nor_fallback]:
                                if fallback_policy_id not in processed:
                                    # Process the referenced root policy first
                                    continue
                                # Find the already-processed root policy
                                fallback_node = next(n for n in not_default_nor_fallback if n.policy_id == fallback_policy_id)
                                default_policy = fallback_node.policy_object
                            else:
                                fallback_node = self.policy_tree.get(fallback_policy_id)
                                if not fallback_node:
                                    raise UndefinedAttributeException("fallback", 
                                                                f"fallback policy '{fallback_policy_id}' not found in policy tree.")
                            
                                # If the fallback policy hasn't been processed yet, prioritize it
                                if fallback_policy_id not in processed:
                                    # Move the fallback policy to the front of the processing queue
                                    to_process.insert(0, fallback_node)
                                    # Re-add the current node to process after the fallback
                                    to_process.append(node)
                                    continue
                            
                            fallback_policy = fallback_node.policy_object
                        node.policy_object = LazyConsensusPolicy.from_policy(base_policy, fallback=fallback_policy)
                    case "MajorityPolicy":
                        parameters = self.__policy_parameters_map.get(node.policy_id, {})
                        node.policy_object = MajorityPolicy.from_policy(base_policy,  
                                                                       ratio=parameters.get('ratio'))
                    
                    case "AbsoluteMajorityPolicy":
                        parameters = self.__policy_parameters_map.get(node.policy_id, {})
                        node.policy_object = AbsoluteMajorityPolicy.from_policy(base_policy, 
                                                                               ratio=parameters.get('ratio'))
                    
                    case "LeaderDrivenPolicy":
                        parameters = self.__policy_parameters_map.get(node.policy_id, {})
                        default_policy_id = parameters.get('default')
                        
                        default_policy = None
                        if default_policy_id:
                            # Check if it's a root policy reference
                            if default_policy_id in [n.policy_id for n in not_default_nor_fallback]:
                                if default_policy_id not in processed:
                                    # Process the referenced root policy first
                                    continue
                                # Find the already-processed root policy
                                default_node = next(n for n in not_default_nor_fallback if n.policy_id == default_policy_id)
                                default_policy = default_node.policy_object
                            else:
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
                        
                        # Scope will be automatically propagated to inline default policy by the LeaderDrivenPolicy class. 
                    
                # Resolve AppealRight targets for this node (if any)
                refs = self.__appeal_policy_map.get(node.policy_id, [])
                if refs:
                    requeue = False
                    for cond_obj, target_id in refs:
                        target_node = self.policy_tree.get(target_id)
                        if not target_node:
                            raise UndefinedAttributeException("policy", f"AppealRight references an undefined policy '{target_id}'.")
                        if target_node.policy_id not in processed:
                            # Ensure target is processed first
                            to_process.insert(0, target_node)
                            to_process.append(node)
                            requeue = True
                            break
                        # Target is ready; attach it
                        cond_obj.policy = target_node.policy_object
                    if requeue:
                        # Defer current node until target(s) are built
                        continue
            
            # Mark as processed
            processed.add(node.policy_id)
            
            # Add parent to processing queue if exists and not processed
            if node.parent and node.parent.policy_id not in processed:
                to_process.append(node.parent)
        
        # Validate all policies to ensure scopes are set correctly
        for node in self.policy_tree.values():
            if hasattr(node, 'policy_object') and node.policy_object:
                node.policy_object.validate()
    
    def _current_policy_id(self) -> str:
        """
        Retrieves the policy ID of the current policy context.
        Returns:
            The policy ID of the current policy.
        Raises:
            RuntimeError: If not within a policy context
        """
        # TODO: Adapt code so that uses this helper method
        if not self.policy_stack:
            raise RuntimeError("Attempting to access policy stack, but it is empty.")
        return self.policy_stack[-1].policy_id
    
    def _get_current_policy_scope(self):
        """
        Retrieves the Scope object associated with the current policy.
        If the current policy doesn't have a scope, walks up the parent hierarchy
        to find an inherited scope (useful for nested policies like phases).
        Returns:
            The Scope object associated with the current policy or its ancestors.
        Raises:
            RuntimeError: If not within a policy context
        """
        pid = self._current_policy_id()
        
        # Check if current policy has a scope
        if pid in self.__policy_scopes_map:
            return self.__policy_scopes_map.get(pid)
        
        # Walk up the parent hierarchy to find an inherited scope
        current_node = self.policy_tree.get(pid)
        while current_node and current_node.parent:
            parent_id = current_node.parent.policy_id
            if parent_id in self.__policy_scopes_map:
                return self.__policy_scopes_map.get(parent_id)
            current_node = current_node.parent
        
        # No scope found in hierarchy
        return None

    def _resolve_project_from_scope(self, scope):
        # Project scope
        if scope is None:
            return None
        # If the scope itself is a Project (or Repository), return it
        if isinstance(scope, (Project, Repository)):
            return scope
        # Activity -> Project
        if isinstance(scope, Activity):
            return scope.project
        # Task -> Activity -> Project
        if isinstance(scope, Task) and scope.activity:
            return getattr(scope.activity, "project", None)

    def _register_scope_with_current_policy(self, scope_obj):
        """
        Registers a scope object (Activity, Project, Task) with the current policy.
        
        Args:
            scope_obj: The scope object to register
            
        Raises:
            RuntimeError: If not within a policy context
        """
        # Get the current policy context
        current_policy_id = self._current_policy_id()
        
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
        current_policy_id = self._current_policy_id()
        
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
        current_policy_id = self._current_policy_id()
        
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
        current_policy_id = self._current_policy_id()
        
        # Initialize the rules set for this policy if needed
        if current_policy_id not in self.__policy_rules_map:
            self.__policy_rules_map[current_policy_id] = set()
        
        # Associate the rule with the current policy
        self.__policy_rules_map[current_policy_id].add(rule)

    def _register_communication_channel_with_current_policy(self, channel_obj):
        """
        Registers a communication channel object with the current policy.
        
        Args:
            channel_obj: The communication channel object to register
            
        Raises:
            RuntimeError: If not within a policy context
        """
        # Get the current policy context
        current_policy_id = self._current_policy_id()
        
        # Initialize the communication channel for this policy if needed
        if current_policy_id in self.__communication_channels_map:
            raise Exception("Communication channel already defined for policy.") # TODO: Handle this case
        
        # Associate the communication channel with the current policy
        self.__communication_channels_map[current_policy_id] = channel_obj

    def _register_decision_type_with_current_policy(self, decision_obj):
        """
        Registers a decision type object (BooleanDecision, StringList, ElementList) with the current policy.
        
        Args:
            decision_obj: The decision type object to register
            
        Raises:
            RuntimeError: If not within a policy context
        """
        # Get the current policy context
        current_policy_id = self._current_policy_id()
        
        # Initialize the decision types set for this policy if needed
        if current_policy_id in self.__policy_decision_type_map:
            raise Exception("Decision type already defined for policy.") # TODO: Handle this case
        
        # Associate the decision type with the current policy
        self.__policy_decision_type_map[current_policy_id] = decision_obj

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
    
    def enterTopLevelComposedPolicy(self, ctx:govdslParser.TopLevelComposedPolicyContext):
        """When entering a top-level composed policy, create a node"""
        policy_id = ctx.ID().getText()
        node = PolicyNode(policy_id, "composed", is_nested=False)
        self.policy_tree[policy_id] = node
        self.policy_stack.append(node)
        self.composed_policy_stack.append(node)
        
    def enterNestedComposedPolicy(self, ctx:govdslParser.NestedComposedPolicyContext):
        """When entering a nested composed policy, create a node and establish parent-child relationship"""
        policy_id = ctx.ID().getText()
        node = PolicyNode(policy_id, "composed", is_nested=True)
        self.policy_tree[policy_id] = node
        
        # For nested policies, always establish parent-child relationship
        if self.policy_stack:
            self.policy_stack[-1].add_child(node)
            
        self.policy_stack.append(node)
        self.composed_policy_stack.append(node)

    def enterOrder(self, ctx:govdslParser.OrderContext):
        sequential = ctx.orderType().orderTypeValue().getText().lower() == "sequential"
        require_all = ctx.orderMode().booleanValue().getText().lower() == "true"
        carry_over = False  # Default value
        if ctx.carryOver():
            carry_over = ctx.carryOver().booleanValue().getText().lower() == "true"
                
        # Register with current composed policy
        current_policy_id = self.policy_stack[-1].policy_id if self.policy_stack else None
        if current_policy_id:
            self.__policy_order_map[current_policy_id] = {
                "sequential": sequential, 
                "require_all": require_all,
                "carry_over": carry_over
            }
        else:
            raise Exception("Handling of policy_stack is incorrect.")

    def enterScope(self, ctx:govdslParser.ScopeContext):
        try:
            self._register_scope_with_current_policy(self.__scopes_map[ctx.ID().getText()])
        except KeyError:
            raise UndefinedAttributeException("scope", message=f"Scope {ctx.ID().getText()} not defined.")

    def enterProject(self, ctx:govdslParser.ProjectContext):
        project_name = ctx.ID().getText()
        project = Project(name=project_name, status=None)

        if ctx.platform():
            platform_str = ctx.platform().getText() # This will be used when we define further platforms
            id_tokens = ctx.repoID().ID().getText()
            repo_id = id_tokens
            if '/' in id_tokens:
                owner, repo = id_tokens.split('/', 1)
                repo_id = f"{owner}/{repo}"
            project = Repository.from_project(project=project, repo_id=repo_id)
        if ctx.activity():
            activities = set()
            for act in ctx.activity():
                activity = Activity(name=act.ID().getText(), status=None)
                tasks = set()
                if act.task():
                    for t in act.task():
                        task_name = t.ID().getText()
                        # Extract status if present
                        status = None

                        if t.patchTask():
                            if t.patchTask().patchTaskContent() and t.patchTask().patchTaskContent().status():
                                status = str_to_status_enum(t.patchTask().patchTaskContent().status().statusEnum().getText())

                            task = None
                            
                            # Handle CHP extension elements
                            if t.patchTask().patchTaskType():
                                task_type_str = t.patchTask().patchTaskType().getText().lower()
                                
                                # Create the CHP element (PullRequest or Issue)
                                chp_element = None
                                labels = None
                                
                                # Process labels if present
                                if t.patchTask().patchTaskContent().actionWithLabels():
                                    label_count = len(t.patchTask().patchTaskContent().actionWithLabels().labels().ID())
                                    labels = set()
                                    for i in range(label_count):
                                        l_id = t.patchTask().patchTaskContent().actionWithLabels().labels().LABEL(i).getText()
                                        labels.add(Label(name=l_id))
                                
                                # Create the appropriate CHP element based on task type
                                if task_type_str == "pull request":
                                    chp_element = PullRequest(name=task_name, labels=labels)
                                # elif task_type_str == "issue":
                                #     chp_element = Issue(name=task_name, labels=labels)
                                
                                # Extract action for Patch
                                action = None
                                if t.patchTask().patchTaskContent().patchAction():
                                    action = str_to_action_enum(t.patchTask().patchTaskContent().patchAction().patchActionEnum().getText())
                                elif t.patchTask().patchTaskContent().actionWithLabels():
                                    action = str_to_action_enum(t.patchTask().patchTaskContent().actionWithLabels().patchAction().patchActionEnum().getText())
                                else:
                                    raise UndefinedAttributeException("action", "This task must have an action defined.")
                                
                                # Create the Patch object that references the CHP element
                                if chp_element:
                                    task = Patch(name=task_name, status=status, action=action, element=chp_element)
                                else:
                                    # Fallback if no matching CHP element type
                                    task = Task(name=task_name, status=status)
                        elif t.memberTask():
                            # MemberLifecycle task
                            action = None
                            if t.memberTask().memberTaskContent():
                                action = t.memberTask().memberTaskContent().memberAction().memberActionEnum().getText()
                                action = str_to_member_action_enum(action)
                            task = MemberLifecycle(name=task_name, status=status, action=action)
                        else:
                            # For regular tasks
                            task = Task(name=task_name, status=status)
                        task.activity = activity
                        tasks.add(task)
                        self.__scopes_map[task_name] = task
                            
                    activity.tasks = tasks
                activity.project = project
                activities.add(activity)
                self.__scopes_map[activity.name] = activity
            project.activities = activities         
        
        self.__scopes_map[project_name] = project

    def enterActivities(self, ctx:govdslParser.ActivitiesContext):
        activities = set()
        for act in ctx.activity():
            activity = Activity(name=act.ID().getText(), status=None)
            tasks = set()
            if act.task():
                for t in act.task():
                    task_name = t.ID().getText()
                    # Extract status if present

                    status = None
                    if t.patchTask():
                        if t.patchTask().patchTaskContent() and t.patchTask().patchTaskContent().status():
                            status = str_to_status_enum(t.patchTask().patchTaskContent().status().statusEnum().getText())

                        task = None
                        
                        # Handle CHP extension elements
                        if t.patchTask().patchTaskType():
                            task_type_str = t.patchTaskType().getText().lower()
                            
                            # Create the CHP element (PullRequest or Issue)
                            chp_element = None
                            labels = None
                            
                            # Process labels if present
                            if t.patchTask().patchTaskContent().actionWithLabels():
                                label_count = len(t.patchTask().patchTaskContent().actionWithLabels().labels().ID())
                                labels = set()
                                for i in range(label_count):
                                    l_id = t.patchTask().patchTaskContent().actionWithLabels().labels().LABEL(i).getText()
                                    labels.add(Label(name=l_id))
                            
                            # Create the appropriate CHP element based on task type
                            if task_type_str == "pull request":
                                chp_element = PullRequest(name=task_name, labels=labels)
                            # elif task_type_str == "issue":
                            #     chp_element = Issue(name=task_name, labels=labels)
                            
                            # Extract action for Patch
                            action = None
                            if t.patchTask().patchTaskContent().patchAction():
                                action = str_to_action_enum(t.patchTask().patchTaskContent().patchAction().patchActionEnum().getText())
                            elif t.patchTask().patchTaskContent().actionWithLabels():
                                action = str_to_action_enum(t.patchTask().patchTaskContent().actionWithLabels().patchAction().patchActionEnum().getText())
                            else:
                                raise UndefinedAttributeException("action", "This task must have an action defined.")
                            
                            # Create the Patch object that references the CHP element
                            if chp_element:
                                task = Patch(name=task_name, status=status, action=action, element=chp_element)
                            else:
                                # Fallback if no matching CHP element type
                                task = Task(name=task_name, status=status)
                    elif t.memberTask():
                        # MemberLifecycle task
                        action = None
                        if t.memberTask().memberTaskContent():
                            action = t.memberTask().memberTaskContent().memberAction().memberActionEnum().getText()
                            action = str_to_member_action_enum(action)
                        task = MemberLifecycle(name=task_name, status=status, action=action)
                    else:
                        # For regular tasks
                        task = Task(name=task_name, status=status)
                    task.activity = activity
                    tasks.add(task)
                    self.__scopes_map[task_name] = task
                        
                activity.tasks = tasks
            activities.add(activity)
            self.__scopes_map[activity.name] = activity

    def enterTasks(self, ctx:govdslParser.TasksContext):
        for t in ctx.task():
            task_name = t.ID().getText()
            # Extract status if present
            status = None

            if t.patchTask():
                if t.patchTask().patchTaskContent() and t.patchTask().patchTaskContent().status():
                    status = str_to_status_enum(t.patchTask().patchTaskContent().status().statusEnum().getText())

                task = None
                
                # Handle CHP extension elements
                if t.patchTask().patchTaskType():
                    task_type_str = t.patchTask().patchTaskType().getText().lower()

                    # Create the CHP element (PullRequest or Issue)
                    chp_element = None
                    labels = None
                    
                    # Process labels if present
                    if t.patchTask().patchTaskContent().actionWithLabels():
                        label_count = len(t.patchTask().patchTaskContent().actionWithLabels().labels().ID())
                        labels = set()
                        for i in range(label_count):
                            l_id = t.patchTask().patchTaskContent().actionWithLabels().labels().LABEL(i).getText()
                            labels.add(Label(name=l_id))

                    # Create the appropriate CHP element based on task type
                    if task_type_str == "pull request":
                        chp_element = PullRequest(name=task_name, labels=labels)
                    # elif task_type_str == "issue":
                    #     chp_element = Issue(name=task_name, labels=labels)
                    
                    # Extract action for Patch
                    action = None
                    if t.patchTask().patchTaskContent().patchAction():
                        action = str_to_action_enum(t.patchTask().patchTaskContent().patchAction().patchActionEnum().getText())
                    elif t.patchTask().patchTaskContent().actionWithLabels():
                        action = str_to_action_enum(t.patchTask().patchTaskContent().actionWithLabels().patchAction().patchActionEnum().getText())
                    else:
                        raise UndefinedAttributeException("action", "This task must have an action defined.")
                    
                    # Create the Patch object that references the CHP element
                    if chp_element:
                        task = Patch(name=task_name, status=status, action=action, element=chp_element)
                    else:
                        # Fallback if no matching CHP element type
                        task = Task(name=task_name, status=status)
            elif t.memberTask():
                # MemberLifecycle task
                action = None
                if t.memberTask().memberTaskContent():
                    action = t.memberTask().memberTaskContent().memberAction().memberActionEnum().getText()
                    action = str_to_member_action_enum(action)
                task = MemberLifecycle(name=task_name, status=status, action=action)
            else:
                # For regular tasks
                task = Task(name=task_name, status=status)
            self.__scopes_map[task_name] = task

    def enterCommunicationChannel(self, ctx:govdslParser.CommunicationChannelContext):
        channel = CommunicationChannel(name=ctx.ID().getText())
        self._register_communication_channel_with_current_policy(channel)

    def enterPolicyParticipants(self, ctx:govdslParser.PolicyParticipantsContext):
        participants_list = ctx.partID()

        for p in participants_list:
            participant = self.__participants_map.get(p.ID().getText())
            if not participant:
                raise UndefinedAttributeException("participant", message="Participant not defined.")
            if p.hasRole():
                if not isinstance(participant, Individual):
                    raise UndefinedAttributeException("role", message="hasRole attribute can only be applied to individual.")
                role_name = p.hasRole().ID().getText()
                # Find the role object, has to be already defined
                role_obj = self.__participants_map.get(role_name)
                if role_obj:
                    # Create hasRole relationship
                    current_policy_id = self.policy_stack[-1].policy_id
                    scope = self.__policy_scopes_map.get(current_policy_id)
                    if scope:
                        role_assignment = hasRole(f"{participant.name}_{role_name}", role_obj, participant, scope)
                        participant.role_assignement = role_assignment
                    else:
                        raise UndefinedAttributeException("scope", message="No scope defined for role assignment (Hint: Might be a parsing error).")
                else:
                    raise UndefinedAttributeException("role", message="No role defined for this role assignment.")
            self._register_participant_with_current_policy(participant)
                
    def enterRoles(self, ctx:govdslParser.RolesContext): 

        for role in ctx.role():
            roleID = role.ID().getText()
            role_instance = Role(name=roleID)
            if role.voteValue():
                role_instance.vote_value = float(role.voteValue().FLOAT().getText())
            self.__participants_map[roleID] = role_instance

    def enterIndividual(self, ctx:govdslParser.IndividualContext):
        name = ctx.ID().getText()
        individual = Human(name=name)
                
        if ctx.voteValue():
            individual.vote_value = float(ctx.voteValue().FLOAT().getText())
        
        if ctx.withProfile():
            profile_name = ctx.withProfile().ID().getText()
            profile = self.__profiles_map.get(profile_name)
            if not profile:
                raise UndefinedAttributeException("profile", message=f"Profile {profile_name} not defined.")
            individual.profile = profile
        
        if ctx.withRole():
            role_name = ctx.withRole().ID().getText()
            role = self.__participants_map.get(role_name)
            if not role:
                raise UndefinedAttributeException("role", message=f"Role {role_name} not defined.")
            # individual.role = role # Should the relationship be bidirectional?
            role.individuals.add(individual)
            
        self.__participants_map[name] = individual

    def enterProfile(self, ctx:govdslParser.ProfileContext):
        gender = None
        race = None
        language = None
        seen_attrs = set()
        profile_name = ctx.ID().getText()
        
        # Iterate through all profile attributes
        for attr in ctx.profileAttr():
            if attr.gender():
                if 'gender' in seen_attrs:
                    raise DuplicateAttributeException("profile", profile_name, "gender")
                seen_attrs.add('gender')
                gender = attr.gender().ID().getText()
            elif attr.race():
                if 'race' in seen_attrs:
                    raise DuplicateAttributeException("profile", profile_name, "race")
                seen_attrs.add('race')
                race = attr.race().ID().getText()
            elif attr.language():
                if 'language' in seen_attrs:
                    raise DuplicateAttributeException("profile", profile_name, "language")
                seen_attrs.add('language')
                language = attr.language().ID().getText()
        
        # Validate that at least one attribute is provided
        if not (gender or race or language):
            raise UndefinedAttributeException("profile", 
                message=f"Profile '{profile_name}' must have at least one attribute (gender, race, or language)")
        
        profile = Profile(name=profile_name,
                            gender=gender,
                            race=race,
                            language=language)
        self.__profiles_map[profile.name] = profile

    def enterAgent(self, ctx:govdslParser.AgentContext):
        name = ctx.ID().getText()
        agent = Agent(name=name)
                
        if ctx.voteValue():
            agent.vote_value = float(ctx.voteValue().FLOAT().getText())
        if ctx.confidence():
            agent.confidence = float(ctx.confidence().FLOAT().getText())
        if ctx.autonomyLevel():
            agent.autonomy_level = float(ctx.autonomyLevel().FLOAT().getText())
        if ctx.explainability():
            agent.explainability = float(ctx.explainability().FLOAT().getText())
        if ctx.withRole():
            role_name = ctx.withRole().ID().getText()
            role = self.__participants_map.get(role_name)
            if not role:
                raise UndefinedAttributeException("role", message=f"Role {role_name} not defined.")
            # agent.role = role # Should the relationship be bidirectional?
            role.individuals.add(agent)
            
        self.__participants_map[name] = agent

    def enterBooleanDecision(self, ctx:govdslParser.BooleanDecisionContext):
        decision = BooleanDecision(name="booleanDecision")
        self._register_decision_type_with_current_policy(decision)
    
    def enterStringList(self, ctx:govdslParser.StringListContext):
        ids = ctx.ID()
        string_list = set()
        for i in ids:
            string_list.add(i.getText())
        decision = StringList(name="stringList", options=string_list)
        self._register_decision_type_with_current_policy(decision)
    
    def enterElementList(self, ctx:govdslParser.ElementListContext):
        ids = ctx.ID()
        element_list = set()
        for i in ids:
            element = self.__participants_map.get(i.getText())
            if not element or not isinstance(element, Individual):
                raise UndefinedAttributeException("element", message="Individual not defined.")
            element_list.add(element)
        decision = ElementList(name="elementList", elements=element_list)
        self._register_decision_type_with_current_policy(decision)

    def enterDeadline(self, ctx:govdslParser.DeadlineContext):
        name = ctx.deadlineID().ID().getText() if ctx.deadlineID() else "deadline"
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
        
    def enterMinDecisionTime(self, ctx:govdslParser.MinDecisionTimeContext):
        name = ctx.ID().getText() if ctx.ID() else "minDecisionTime"
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

        min_decision_time = MinDecisionTime(name=name, offset=offset, date=date)
        self._register_condition_with_current_policy(min_decision_time)

    def enterParticipantExclusion(self, ctx:govdslParser.ParticipantExclusionContext):        
        excluded_ids = [e.getText() for e in ctx.ID()]
        scope = self._get_current_policy_scope()
        if scope is None:
            raise UndefinedAttributeException("scope", 
                                              message="No scope defined for policy of ParticipantExclusion (check parsing order).")
        
        if "PRAuthor" in excluded_ids:
            if not isinstance(scope, Patch) or not isinstance(getattr(scope, "element", None), PullRequest):
                raise UndefinedAttributeException(
                    "ParticipantExclusion",
                    message="Constraint violation: PRAuthor only valid when policy scope is a Patch on a PullRequest, now: {}.".format(type(scope).__name__)
                )
        if "RepoOwner" in excluded_ids:
            project = self._resolve_project_from_scope(scope)
            if not project:
                raise UndefinedAttributeException(
                    "ParticipantExclusion",
                    message="Constraint violation: RepoOwner only valid when policy scope is associated with a Repository, now: {}.".format(type(scope).__name__)
                )
        
        excluded_set = set()
        for excluded_name in excluded_ids:
            participant = self.__participants_map.get(excluded_name)
            if participant:
                excluded_set.add(participant)
                continue
            # We create an Individual if complies with default values, for now:
            # PRAuthor, RepoOwner
            if excluded_name in ["PRAuthor", "RepoOwner"]:
                excluded_set.add(Individual(name=excluded_name))
            else:
                raise UndefinedAttributeException("participant",
                                                    message="Participant {} not defined. Default values allowed: PRAuthor, RepoOwner".format(excluded_name))

        # we just put a name by default
        cond = ParticipantExclusion(name="partExcl", excluded=excluded_set)
        self._register_condition_with_current_policy(cond)

    def enterMinParticipant(self, ctx:govdslParser.MinParticipantContext):
        min_participants_value = int(ctx.SIGNED_INT().getText())
        condition = MinimumParticipant(name="minParticipantsCondition",
                                    min_participants=min_participants_value)
        self._register_condition_with_current_policy(condition)

    def enterVetoRight(self, ctx:govdslParser.VetoRightContext):
        
        vetoer_obj = set()
        # Vetoers might not be participants of the current policy
        for v in ctx.ID():
            # Check if the vetoer is already registered
            vetoer_name = v.getText()
            vetoer = None
            if vetoer_name in self.__policy_participants_map:
                # Get the existing participant object
                vetoer = next(p for p in self.__policy_participants_map if p.name == vetoer_name)
            else:
                # We create a Individual by default
                vetoer = Individual(name=vetoer_name)
            vetoer_obj.add(vetoer)
        
        # Create the VetoRight object
        veto_right_obj = VetoRight(name="VetoRightCondition", vetoers=vetoer_obj)
        
        # Register with current policy
        self._register_condition_with_current_policy(veto_right_obj)

    def enterAppealRight(self, ctx:govdslParser.AppealRightContext):
        
        # Ensure we’re inside a policy
        if not self.policy_stack:
            raise RuntimeError("Attempting to access policy stack, but it is empty.")
        current_policy_id = self.policy_stack[-1].policy_id

        # Exclude the policyReference ID (if present) from appealer IDs
        ref_id_text = ctx.policyReference().ID().getText() if ctx.policyReference() else None
        appealers_set = set()

        for a in ctx.ID():
            # Appealers must be declared in the participants block
            appealer_name = a.getText()
            # Can it happen that the policyReference ID is captured here? If so, we skip it.
            if ref_id_text and appealer_name == ref_id_text:
                continue
            appealer = self.__participants_map.get(appealer_name)
            if not appealer:
                raise UndefinedAttributeException("participant", message="Participant {} not defined.".format(appealer_name))
            appealers_set.add(appealer)

        # Create the AppealRight (policy resolved later in _construct_policy_objects)
        appeal_right_obj = AppealRight(name="AppealRightCondition", appealers=appealers_set, policy=None)
        self._register_condition_with_current_policy(appeal_right_obj)
        
        # Determine target policy (reference or inline)
        target_policy_id = None
        policy_type = None

        if ctx.policyReference():
            target_policy_id = ref_id_text
        elif ctx.nestedPolicy():
            if ctx.nestedPolicy().nestedSinglePolicy():
                target_policy_id = ctx.nestedPolicy().nestedSinglePolicy().ID().getText()
                policy_type = ctx.nestedPolicy().nestedSinglePolicy().policyType().getText()
            elif ctx.nestedPolicy().nestedComposedPolicy():
                target_policy_id = ctx.nestedPolicy().nestedComposedPolicy().ID().getText()
                policy_type = "composed"

            # Create a node for this inline (nested) appeal policy (scope inheritance)
            if target_policy_id and target_policy_id not in self.policy_tree:
                node = PolicyNode(target_policy_id, policy_type, is_nested=True)
                self.policy_tree[target_policy_id] = node
                self.referenced_policies.add(target_policy_id)
                parent_node = self.policy_stack[-1]
                parent_node.add_child(node)
                # Inherit parent scope if already set
                if current_policy_id in self.__policy_scopes_map:
                    self.__policy_scopes_map[target_policy_id] = self.__policy_scopes_map[current_policy_id]

        # Record for later resolution
        if target_policy_id:
            self.__appeal_policy_map.setdefault(current_policy_id, []).append((appeal_right_obj, target_policy_id))

    def enterCheckCiCd(self, ctx:govdslParser.CheckCiCdContext):
        
        if ctx.booleanValue().getText().lower() == "true":
            evaluation_mode = None
            if ctx.evaluationMode():
                evaluation_mode = ctx.evaluationMode().getText()
                match evaluation_mode:
                    case "pre":
                        evaluation_mode = EvaluationMode.PRE
                    case "post":
                        evaluation_mode = EvaluationMode.POST
                    case "concurrent":
                        evaluation_mode = EvaluationMode.CONCURRENT
            # Create the CheckCiCd object
            test_condition = CheckCiCd(name="checkCiCdCondition", evaluation_mode=evaluation_mode)
            self._register_condition_with_current_policy(test_condition)

    def enterMinTime(self, ctx:govdslParser.MinTimeContext):
        # TODO: We might want to check this condition is applied only on MemberLifecycle task
        offset_amount = int(ctx.offset().SIGNED_INT().getText())
        time_unit = ctx.offset().timeUnit().getText()
        offset = deadline_to_timedelta(value=offset_amount, unit=time_unit)

        evaluation_mode = None
        if ctx.evaluationMode():
            evaluation_mode = ctx.evaluationMode().getText()
            match evaluation_mode:
                case "pre":
                    evaluation_mode = EvaluationMode.PRE
                case "post":
                    evaluation_mode = EvaluationMode.POST
                case "concurrent":
                    evaluation_mode = EvaluationMode.CONCURRENT

        act_bool = True if ctx.activityBool().getText() == "Activity" else False

        min_time_condition = MinTime(name="minTimeCondition", evaluation_mode=evaluation_mode, activity=act_bool,  offset=offset)
        self._register_condition_with_current_policy(min_time_condition)

    def enterLabelsCondition(self, ctx:govdslParser.LabelsConditionContext):

        evaluation_mode = EvaluationMode.CONCURRENT
        if ctx.evaluationMode():
            ev_mode = ctx.evaluationMode().getText()
            match ev_mode:
                case "pre":
                    evaluation_mode = EvaluationMode.PRE
                case "post":
                    evaluation_mode = EvaluationMode.POST
                case "concurrent":
                    evaluation_mode = EvaluationMode.CONCURRENT

        labels = set()
        for l in ctx.ID():
            label = Label(name=l.getText())
            labels.add(label)
        
        # Check if inclusion is specified
        inclusion = True
        if ctx.include():
            inclusion = ctx.include().getText().lower() == "include"
        
        # Create the LabelCondition object
        label_condition = LabelCondition(name="labelCondition", evaluation_mode=evaluation_mode, labels=labels, inclusion=inclusion)
        
        # Register with current policy
        self._register_condition_with_current_policy(label_condition)

    def enterParameters(self, ctx:govdslParser.ParametersContext):
        # Get the current policy context
        current_policy_id = self._current_policy_id()
        
        # Initialize the parameters map for this policy if needed
        if current_policy_id not in self.__policy_parameters_map:
            self.__policy_parameters_map[current_policy_id] = {}
        
        # Extract voting parameters if present
        if ctx.votParams():
            vot_params = ctx.votParams()
            
            # I had here minVotes. Since we created the minParticipants condition, it is no longer necessary.
            # However, I keep this structure for if we want to add more parameters in the future.
            
            # Extract ratio if present
            if vot_params.ratio():
                self.__policy_parameters_map[current_policy_id]['ratio'] = float(vot_params.ratio().FLOAT().getText())
        
        # Extract default policy if present (for LeaderDrivenPolicy)
        if ctx.default():
            default_ctx = None
            if ctx.default().nestedPolicy():
                if ctx.default().nestedPolicy().nestedSinglePolicy():
                    default_ctx = ctx.default().nestedPolicy().nestedSinglePolicy().ID().getText()
                elif ctx.default().nestedPolicy().nestedComposedPolicy():
                    default_ctx = ctx.default().nestedPolicy().nestedComposedPolicy().ID().getText()
            elif ctx.default().policyReference():
                default_ctx = ctx.default().policyReference().ID().getText()
            self.__policy_parameters_map[current_policy_id]['default'] = default_ctx

        # Extract fallback policy if present (for ConsensusPolicy)
        if ctx.fallback():
            fallback_ctx = None
            if ctx.fallback().nestedPolicy():
                if ctx.fallback().nestedPolicy().nestedSinglePolicy():
                    fallback_ctx = ctx.fallback().nestedPolicy().nestedSinglePolicy().ID().getText()
                elif ctx.fallback().nestedPolicy().nestedComposedPolicy():
                    fallback_ctx = ctx.fallback().nestedPolicy().nestedComposedPolicy().ID().getText()
            elif ctx.fallback().policyReference():
                fallback_ctx = ctx.fallback().policyReference().ID().getText()
            self.__policy_parameters_map[current_policy_id]['fallback'] = fallback_ctx

    def enterDefault(self, ctx:govdslParser.DefaultContext):
        # Only for inline policies
        if ctx.policyReference():
            return
        # Get the current policy context (the LeaderDrivenPolicy)
        if not self.policy_stack:
            raise RuntimeError("Attempting to access policy stack, but it is empty.")
        
        # Extract the default policy ID
        default_policy_id = None
        policy_type = None
        if ctx.nestedPolicy().nestedSinglePolicy():
            default_policy_id = ctx.nestedPolicy().nestedSinglePolicy().ID().getText()
            policy_type = ctx.nestedPolicy().nestedSinglePolicy().policyType().getText()
        elif ctx.nestedPolicy().nestedComposedPolicy():
            default_policy_id = ctx.nestedPolicy().nestedComposedPolicy().ID().getText()
            policy_type = "composed"
        
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
    
    def enterFallback(self, ctx:govdslParser.FallbackContext):
        # Only for inline policies
        if ctx.policyReference():
            return
        # Get the current policy context (the ConsensusPolicy)
        if not self.policy_stack:
            raise RuntimeError("Attempting to access policy stack, but it is empty.")
        
        # Extract the default policy ID
        fallback_policy_id = None
        policy_type = None
        if ctx.nestedPolicy().nestedSinglePolicy():
            fallback_policy_id = ctx.nestedPolicy().nestedSinglePolicy().ID().getText()
            policy_type = ctx.nestedPolicy().nestedSinglePolicy().policyType().getText()
        elif ctx.nestedPolicy().nestedComposedPolicy():
            fallback_policy_id = ctx.nestedPolicy().nestedComposedPolicy().ID().getText()
            policy_type = "composed"
        
        # Create a node for this fallback policy
        if fallback_policy_id and fallback_policy_id not in self.policy_tree:
            # Create the fallback policy node with is_nested=True to ensure scope inheritance
            node = PolicyNode(fallback_policy_id, policy_type, is_nested=True)
            # Add the fallback attribute to distinguish from phases
            node.is_fallback = True
            self.policy_tree[fallback_policy_id] = node
            
            # Mark this policy as referenced so it's not considered a root policy
            self.referenced_policies.add(fallback_policy_id)
            
            # Set up parent-child relationship with the current policy
            if self.policy_stack:
                current_policy = self.policy_stack[-1]
                current_policy.add_child(node)
                
                # Share the scope from parent to default policy
                if current_policy.policy_id in self.__policy_scopes_map:
                    parent_scope = self.__policy_scopes_map[current_policy.policy_id]
                    self.__policy_scopes_map[fallback_policy_id] = parent_scope

    def exitGovernance(self, ctx:govdslParser.GovernanceContext):
        """When exiting the governance context, construct the policy tree"""
        # Build all objects from the tree (bottom-up)
        self._construct_policy_objects()
        
        
        root_policy_nodes = [node for node in self.policy_tree.values() 
                         if node.parent is None and node.policy_id not in self.referenced_policies]

        self.__policies = [
            node.policy_object for node in root_policy_nodes 
            if hasattr(node, 'policy_object') and node.policy_object is not None
        ]

        if len(self.__policies) < len(root_policy_nodes):
            raise Exception("Some policies were not constructed correctly. Check the policy tree.")
    
    def exitNestedSinglePolicy(self, ctx:govdslParser.NestedSinglePolicyContext):
        """When exiting a nested single policy, pop from stack"""
        self.policy_stack.pop()

    def exitNestedComposedPolicy(self, ctx:govdslParser.NestedComposedPolicyContext):
        """When exiting a nested composed policy, clear current and pop stack"""
        self.composed_policy_stack.pop()
        self.policy_stack.pop()

    def exitTopLevelSinglePolicy(self, ctx:govdslParser.TopLevelSinglePolicyContext):
        """When exiting a top-level single policy, pop from stack"""
        self.policy_stack.pop()

    def exitTopLevelComposedPolicy(self, ctx:govdslParser.TopLevelComposedPolicyContext):
        """When exiting a top-level composed policy, clear current and pop stack"""
        self.composed_policy_stack.pop()
        self.policy_stack.pop()