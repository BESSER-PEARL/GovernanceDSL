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
    ActionEnum, Label, PullRequest, Issue, Patch, Repository,
    PassedTests, LabelCondition
)
from utils.attribute_converters import (
    str_to_status_enum, str_to_action_enum, deadline_to_timedelta
)
from metamodel.governance import (
    SinglePolicy, Project, Activity, Task, Role, Individual,
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

        # Maps to track scopes and participants predefined
        self.__scopes_map = {}
        self.__participants_map = {}

        # Policy tree structure
        self.policy_tree = {}  # Maps policy ID to PolicyNode
        self.policy_stack = []  # Tracks the current policy context
        self.composed_policy_stack = []  # Tracks the current composed policies
        self.referenced_policies = set()  # Track policies referenced by others (like default policies)

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
                participants = self.__policy_participants_map.get(node.policy_id, set())
                conditions = self.__policy_conditions_map.get(node.policy_id, set())
                base_policy = SinglePolicy(name=node.policy_id,
                                            conditions=conditions,
                                            participants=participants,
                                            decision_type=decision_type,
                                            scope=scope)
                
                match node.policy_type:
                    case "ConsensusPolicy":
                        if len(self.__policy_parameters_map.get(node.policy_id, {})) > 0:
                            raise UndefinedAttributeException("parameters",
                                                            message="ConsensusPolicy cannot have parameters.")
                        node.policy_object = ConsensusPolicy.from_policy(base_policy)
                    case "LazyConsensusPolicy":
                        if len(self.__policy_parameters_map.get(node.policy_id, {})) > 0:
                            raise UndefinedAttributeException("parameters",
                                                            message="LazyConsensusPolicy cannot have parameters.")
                        node.policy_object = LazyConsensusPolicy.from_policy(base_policy)
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

    def _register_decision_type_with_current_policy(self, decision_obj):
        """
        Registers a decision type object (BooleanDecision, StringList, ElementList) with the current policy.
        
        Args:
            decision_obj: The decision type object to register
            
        Raises:
            RuntimeError: If not within a policy context
        """
        # Get the current policy context
        if not self.policy_stack:
            raise RuntimeError("Attempting to access policy stack, but it is empty.")
        
        current_policy_id = self.policy_stack[-1].policy_id
        
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
            id_tokens = ctx.repoID().ID()
            if len(id_tokens) > 1:  # If there are two IDs (owner/repo format)
                owner = id_tokens[0].getText()
                repo = id_tokens[1].getText()
                repo_id = f"{owner}/{repo}"
            else:  # If there's just one ID it means it is the user or organization
                repo_id = id_tokens[0].getText()
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
                        if t.taskContent() and t.taskContent().status():
                            status = str_to_status_enum(t.taskContent().status().statusEnum().getText())
                        
                        task = None
                        
                        # Handle GitHub extension elements
                        if t.taskType():
                            task_type_str = t.taskType().getText().lower()
                            
                            # Create the GitHub element (PullRequest or Issue)
                            gh_element = None
                            labels = None
                            
                            # Process labels if present
                            if t.taskContent().actionWithLabels():
                                label_count = len(t.taskContent().actionWithLabels().labels().ID())
                                labels = set()
                                for i in range(label_count):
                                    l_id = t.taskContent().actionWithLabels().labels().ID(i).getText()
                                    labels.add(Label(name=l_id))
                            
                            # Create the appropriate GitHub element based on task type
                            if task_type_str == "pull request":
                                gh_element = PullRequest(name=task_name, labels=labels)
                            elif task_type_str == "issue":
                                gh_element = Issue(name=task_name, labels=labels)
                            
                            # Extract action for Patch
                            action = None
                            if t.taskContent().action():
                                action = str_to_action_enum(t.taskContent().action().actionEnum().getText())
                            elif t.taskContent().actionWithLabels():
                                action = str_to_action_enum(t.taskContent().actionWithLabels().action().actionEnum().getText())
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
                        task.activity = activity
                        tasks.add(task)
                        self.__scopes_map[task_name] = task
                            
                    activity.tasks = tasks
                activity.project = project
                activities.add(activity)
                self.__scopes_map[activity.name] = activity
            project.activities = activities         
        
        self.__scopes_map[project_name] = project

    def enterAct(self, ctx:govdslParser.ActContext):
        activity_name = ctx.activity().ID().getText()
        activity = Activity(name=activity_name, status=None)
        if ctx.activity().task():
            tasks = set()
            for t in ctx.activity().task():
                task_name = t.ID().getText()
                
                # Extract status if present
                status = None
                if t.taskContent() and t.taskContent().status():
                    status = str_to_status_enum(t.taskContent().status().statusEnum().getText())
                
                task = None
                
                # Handle GitHub extension elements
                if t.taskType():
                    task_type_str = t.taskType().getText().lower()
                    
                    # Create the GitHub element (PullRequest or Issue)
                    gh_element = None
                    labels = None
                    
                    # Process labels if present
                    if t.taskContent().actionWithLabels():
                        label_count = len(t.taskContent().actionWithLabels().labels().ID())
                        labels = set()
                        for i in range(label_count):
                            l_id = t.taskContent().actionWithLabels().labels().ID(i).getText()
                            labels.add(Label(name=l_id))
                    
                    # Create the appropriate GitHub element based on task type
                    if task_type_str == "pull request":
                        gh_element = PullRequest(name=task_name, labels=labels)
                    elif task_type_str == "issue":
                        gh_element = Issue(name=task_name, labels=labels)
                    
                    # Extract action for Patch
                    action = None
                    if t.taskContent().action():
                        action = str_to_action_enum(t.taskContent().action().actionEnum().getText())
                    elif t.taskContent().actionWithLabels():
                        action = str_to_action_enum(t.taskContent().actionWithLabels().action().actionEnum().getText())
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

                task.activity = activity
                tasks.add(task)
                self.__scopes_map[task_name] = task
            activity.tasks = tasks
        self.__scopes_map[activity_name] = activity

    def enterTsk(self, ctx:govdslParser.TskContext):
        t = ctx.task()
        task_name = ctx.task().ID().getText()
        # Extract status if present
        status = None
        if t.taskContent() and t.taskContent().status():
            status = str_to_status_enum(t.taskContent().status().statusEnum().getText())
        
        task = None
        
        # Handle GitHub extension elements
        if t.taskType():
            task_type_str = t.taskType().getText().lower()
            
            # Create the GitHub element (PullRequest or Issue)
            gh_element = None
            labels = None
            
            # Process labels if present
            if t.taskContent().actionWithLabels():
                label_count = len(t.taskContent().actionWithLabels().labels().ID())
                labels = set()
                for i in range(label_count):
                    l_id = t.taskContent().actionWithLabels().labels().ID(i).getText()
                    labels.add(Label(name=l_id))
            
            # Create the appropriate GitHub element based on task type
            if task_type_str == "pull request":
                gh_element = PullRequest(name=task_name, labels=labels)
            elif task_type_str == "issue":
                gh_element = Issue(name=task_name, labels=labels)
            
            # Extract action for Patch
            action = None
            if t.taskContent().action():
                action = str_to_action_enum(t.taskContent().action().actionEnum().getText())
            elif t.taskContent().actionWithLabels():
                action = str_to_action_enum(t.taskContent().actionWithLabels().action().actionEnum().getText())
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

        self.__scopes_map[task_name] = task

    def enterPolicyParticipants(self, ctx:govdslParser.PolicyParticipantsContext):
        participants_list = ctx.partID()

        for p in participants_list:
            participant = self.__participants_map.get(p.ID().getText())
            if not participant:
                raise UndefinedAttributeException("participant", message="Participant not defined.")
            if p.hasRole():
                if not isinstance(participant, Individual):
                    raise UndefinedAttributeException("role", message="hasRole attribute can only be applied to individual.")
                role_name = p.hasRole().participantID().ID().getText()
                # Find the role object, has to be already defined
                role_obj = self.__participants_map.get(role_name)
                if role_obj:
                    # Create hasRole relationship
                    current_policy_id = self.policy_stack[-1].policy_id
                    scope = self.__policy_scopes_map.get(current_policy_id)
                    if scope:
                        role_assignment = hasRole(f"{participant.name}_{role_name}", role_obj, participant, scope)
                        participant.role = role_assignment
                    else:
                        raise UndefinedAttributeException("scope", message="No scope defined for role assignment (Hint: Might be a parsing error).")
                else:
                    raise UndefinedAttributeException("role", message="No role defined for this role assignment.")
            self._register_participant_with_current_policy(participant)
                
    def enterRoleID(self, ctx:govdslParser.RolesContext): 

        roleID = ctx.ID().getText()
        role = Role(name=roleID)
        if ctx.participantID():
            individuals = set()
            for p in ctx.participantID():
                participant = self.__participants_map.get(p.ID().getText())
                if not participant:
                    # Individual might not be defined yet, so we create it; Can be enriched later
                    participant = Individual(name=p.ID().getText())
                    self.__participants_map[participant.name] = participant
                individuals.add(participant)
            role.individuals = individuals
        self.__participants_map[roleID] = role
     
    def enterIndividual(self, ctx:govdslParser.IndividualContext):
        name = ctx.participantID().ID().getText()
        individual = Individual(name=name)
                
        if ctx.voteValue():
            individual.vote_value = float(ctx.voteValue().FLOAT().getText())
        
        if ctx.profile():
            gender = None
            race = None
            if ctx.profile().gender():
                gender = ctx.profile().gender().ID().getText()
            if ctx.profile().race():
                race = ctx.profile().race().ID().getText()
            profile = Profile(name=ctx.profile().ID().getText(),
                              gender=gender,
                              race=race)
            individual.profile = profile
            
        self.__participants_map[name] = individual

    def enterAgent(self, ctx:govdslParser.AgentContext):
        name = ctx.participantID().ID().getText()
        agent = Agent(name=name)
                
        if ctx.voteValue():
            agent.vote_value = float(ctx.voteValue().FLOAT().getText())
        if ctx.confidence():
            agent.confidence = float(ctx.confidence().FLOAT().getText())
            
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
        # TODO: This condition needs more refinement. We will include primitive types.
        excluded = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.ParticipantIDContext)
        
        excluded_objs = set()
        for e in excluded:
            excluded_name = e.ID().getText()
            excluded_participant = None
            if excluded_name in self.__policy_participants_map:
                # Get the existing individual object; 
                # Check also if it is an Individual for name collision with Roles (which should not happen, though)
                excluded_participant = next(p for p in self.__policy_participants_map if p.name == excluded_name and isinstance(p, Individual)) 
            else:
                # We create an Individual (TODO: Maybe add primitive types)
                excluded_participant = Individual(name=excluded_name)
            excluded_objs.add(excluded_participant)

        # we just put a name by default
        cond = ParticipantExclusion(name="partExcl", excluded=excluded_objs)
        self._register_condition_with_current_policy(cond)

    def enterMinParticipant(self, ctx:govdslParser.MinParticipantContext):
        min_participants_value = int(ctx.SIGNED_INT().getText())
        condition = MinimumParticipant(name="minParticipantsCondition",
                                    min_participants=min_participants_value)
        self._register_condition_with_current_policy(condition)

    def enterVetoRight(self, ctx:govdslParser.VetoRightContext):
        vetoers = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.ParticipantIDContext)
        vetoer_obj = set()
        # Vetoers might not be participants of the current policy
        for v in vetoers:
            # Check if the vetoer is already registered
            vetoer_name = v.ID().getText()
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

    def enterPassedTests(self, ctx:govdslParser.PassedTestsContext):
        
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
            # Create the PassedTests object
            test_condition = PassedTests(name="passedTestsCondition", evaluation_mode=evaluation_mode)
            self._register_condition_with_current_policy(test_condition)

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
        if not self.policy_stack:
            raise RuntimeError("Attempting to access policy stack, but it is empty.")
        
        current_policy_id = self.policy_stack[-1].policy_id
        
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
            if ctx.default().nestedPolicy().nestedSinglePolicy():
                default_ctx = ctx.default().nestedPolicy().nestedSinglePolicy().ID().getText()
            elif ctx.default().nestedPolicy().nestedComposedPolicy():
                default_ctx = ctx.default().nestedPolicy().nestedComposedPolicy().ID().getText()
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