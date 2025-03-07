import warnings
from datetime import timedelta, datetime
from besser.BUML.metamodel.structural import (
    StringType, IntegerType, FloatType, TimeDeltaType
) # TODO: Check if necessary (for attr type validation)
from utils.exceptions import (
    InvalidVotesException, 
    UndefinedAttributeException, 
    UnsupportedRuleTypeException
)
from utils.policy_tree import PolicyNode
from metamodel.governance import (
    SinglePolicy, Project, Activity, Task, Role, Individual,
    Deadline, Rule, MajorityRule, RatioMajorityRule,
    LeaderDrivenRule, VotingCondition, TaskTypeEnum, PlatformEnum,
    PhasedPolicy, OrderEnum, StatusEnum
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

        # Policy tree structure
        self.policy_tree = {}  # Maps policy ID to PolicyNode
        self.policy_stack = []  # Tracks the current policy context
        self.current_phased_policy = None  # Tracks current phased policy being processed

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
    
    def deadline_to_timedelta(self, amount:int, time_unit:str) -> timedelta:
        """
        Converts a deadline to a timedelta object.

        Args:
            amount: The amount of time to convert.
            time_unit: The unit of time to convert (e.g., days, weeks, etc.).

        Returns:
            A timedelta representation from datetime library.
        """
        if amount < 0:
            raise InvalidVotesException(amount)
        match  time_unit:
            case "days":
                return timedelta(days=amount)
            case "weeks":
                return timedelta(weeks=amount)
            case "months":
                return timedelta(weeks=amount*4) # Timedelta do not support above weeks (months, years). dateutil.relativedelta.relativedelta could be also used
            case "years":
                return timedelta(weeks=amount*52) # Approximation
            case _:
                warnings.warn(f"Unsupported time unit: {time_unit}. Defaulting to days.")
                return timedelta(days=amount)
    
    def convert_string_to_task_type(self, task_type_str: str) -> TaskTypeEnum:
        """
        Converts a string representation of a task type to the corresponding TaskTypeEnum value.
        
        Args:
            task_type_str: String representation from the grammar (e.g., "Pull request", "Issue")
            
        Returns:
            The corresponding TaskTypeEnum value
            
        Raises:
            UndefinedAttributeException if the task type string doesn't match any enum value
        """
        task_type_map = {
            "Pull request": TaskTypeEnum.PULL_REQUEST,
            "Issue": TaskTypeEnum.ISSUE
        }
        
        if task_type_str not in task_type_map:
            raise UndefinedAttributeException("task_type", task_type_str)
    
        return task_type_map[task_type_str]

    def convert_string_to_platform(self, platform_str: str) -> PlatformEnum:
        """
        Converts a string representation of a platform to the corresponding PlatformEnum value.
        
        Args:
            platform_str: String representation from the grammar (e.g., "GitHub")
            
        Returns:
            The corresponding PlatformEnum value
            
        Raises:
            UndefinedAttributeException if the platform string doesn't match any enum value
        """
        platform_map = {
            "GitHub": PlatformEnum.GITHUB, # Adapt for variants (e.g., git hub)
            # Add more platforms as needed
        }
        
        # Case-insensitive matching; we need to adapt the grammar too
        normalized_platform = platform_str.lower()
        for key, value in platform_map.items():
            if key.lower() == normalized_platform:
                return value
        
        raise UndefinedAttributeException("platform", platform_str)

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
            
            # For single policies
            if node.policy_type == "single":
                rules = self._get_rules_for_policy(node.policy_id)
                scopes = self._get_scopes_for_policy(node.policy_id)
                node.policy_object = SinglePolicy(name=node.policy_id, 
                                                rules=rules, 
                                                scopes=scopes)
            
            # For phased policies
            elif node.policy_type == "phased":
                # Check if all children are processed
                if not all(child.policy_id in processed for child in node.children):
                    # Put back in queue and process later
                    to_process.append(node)
                    continue
                
                # Get phases (child policies) and create phased policy
                phases = {child.policy_object for child in node.children}
                order = self._get_order_for_policy(node.policy_id)
                # Collect all scopes from direct children
                combined_scopes = set()
                for child in node.children:
                    if hasattr(child.policy_object, 'scopes'):
                        combined_scopes.update(child.policy_object.scopes)
                    else:
                        raise Exception(f"Child policy {child.policy_id} does not have scopes defined.")
            
                node.policy_object = PhasedPolicy(name=node.policy_id,
                                            phases=phases,
                                            order=order,
                                            scopes=combined_scopes)
            
            # Mark as processed
            processed.add(node.policy_id)
            
            # Add parent to processing queue if exists
            if node.parent and node.parent.policy_id not in processed:
                to_process.append(node.parent)
    
    def _get_rules_for_policy(self, policy_id):
        """Extract rules defined within a specific policy"""
        return self.__policy_rules_map.get(policy_id, set())
        
    def _get_scopes_for_policy(self, policy_id):
        """Extract scopes defined within a specific policy"""
        return self.__policy_scopes_map.get(policy_id, set())
        
    def _get_order_for_policy(self, policy_id):
        """Get the execution order for a phased policy"""
        return self.__policy_order_map.get(policy_id)
    
    def _get_condition_for_policy(self, policy_id):
        """Get the conditions defined within a specific policy"""
        return self.__policy_conditions_map.get(policy_id)
    
    def _get_participants_for_policy(self, policy_id):
        """Get the participants defined within a specific policy"""
        return self.__policy_participants_map.get(policy_id)
    
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
        if current_policy_id not in self.__policy_scopes_map:
            self.__policy_scopes_map[current_policy_id] = set()
        
        # Associate the scope with the current policy
        self.__policy_scopes_map[current_policy_id].add(scope_obj)

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
        node = PolicyNode(policy_id, "single")
        self.policy_tree[policy_id] = node
        
        # If we're inside a phased policy, establish parent-child relationship
        if self.current_phased_policy:
            self.current_phased_policy.add_child(node)
        
        # Push to stack to track current context
        self.policy_stack.append(node)

    def exitSinglePolicy(self, ctx:govdslParser.SinglePolicyContext):
        """When exiting a single policy, pop from stack"""
        self.policy_stack.pop()

    def enterPhasedPolicy(self, ctx:govdslParser.PhasedPolicyContext):
        """When entering a phased policy, create a node"""
        policy_id = ctx.ID().getText()
        node = PolicyNode(policy_id, "phased")
        self.policy_tree[policy_id] = node
        
        # Set as current phased policy
        self.current_phased_policy = node
        
        # Push to stack to track current context
        self.policy_stack.append(node)
    
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
        self.current_phased_policy = None
        self.policy_stack.pop()

    def enterActivity(self, ctx:govdslParser.ActivityContext):
        activity_name = ctx.ID().getText()
        activity = Activity(name=activity_name, status=None) # TODO: relationship with tasks, tasks=activity_tasks)
        # self.__project_activities[activity_name] = activity # TODO: work in relationships
        self._register_scope_with_current_policy(activity)
    
    def enterTask(self, ctx:govdslParser.TaskContext):
        task_name = ctx.ID().getText()
        task_type_str = ctx.taskType().getText()
        task_type_enum = self.convert_string_to_task_type(task_type_str)
        # Extract status if present
        status = None
        if ctx.taskContent() and ctx.taskContent().status():
            status_text = ctx.taskContent().status().getText()
            if "completed" in status_text:
                status = StatusEnum.COMPLETED
            elif "accepted" in status_text:
                status = StatusEnum.ACCEPTED
            elif "partial" in status_text:
                status = StatusEnum.PARTIAL
        task = Task(name=task_name, task_type=task_type_enum, status=status)
        self._register_scope_with_current_policy(task)
    
    def exitProject(self, ctx:govdslParser.ProjectContext):
        # For project we do exit to make the relationships. But for now, we are not defining them.
        project_name = ctx.ID().getText()
        platform_str = ctx.platform().getText()
        platform_enum = self.convert_string_to_platform(platform_str)
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
                                                target_type=govdslParser.ParticipantIDContext)
        for i in individuals:
            individual = Individual(name=i.ID().getText())
            self._register_participant_with_current_policy(individual) # WARNING: This might generate conflict if there is a individual with the same name as a role
            
    def enterDeadline(self, ctx:govdslParser.DeadlineContext):
        name = ctx.deadlineID().ID().getText()
        offset = None
        date = None
        
        # Check for offset
        if ctx.offset():
            amount = int(ctx.offset().SIGNED_INT().getText())
            time_unit = ctx.offset().timeUnit().getText()
            offset = self.deadline_to_timedelta(amount=amount, time_unit=time_unit)
        
        # Check for date
        if ctx.date():
            day = int(ctx.date().SIGNED_INT(0).getText())    # First SIGNED_INT is day
            month = int(ctx.date().SIGNED_INT(1).getText())  # Second SIGNED_INT is month
            year = int(ctx.date().SIGNED_INT(2).getText())   # Third SIGNED_INT is year
            date = datetime(year=year, month=month, day=day)
        
        deadline = Deadline(name=name, offset=offset, date=date)
        self._register_condition_with_current_policy(deadline)

    def enterVotingCondition(self, ctx:govdslParser.VotingConditionContext):
        
        name = ctx.voteConditionID().ID().getText()
        min_votes = None
        ratio = None
        if ctx.minVotes():
            min_votes = int(ctx.minVotes().SIGNED_INT().getText())
        if ctx.ratio():
            ratio = float(ctx.ratio().FLOAT().getText())
        condition = VotingCondition(name=name, minVotes=min_votes, ratio=ratio)
        self._register_condition_with_current_policy(condition)

    def enterRule(self, ctx:govdslParser.RuleContext):
        
        rule_name = ctx.ruleID().ID().getText()
        rule_type = ctx.ruleType().getText()

        current_policy_id = self.policy_stack[-1].policy_id


        conditions = set()
        if ctx.ruleContent().ruleConditions():
            condition_count = len(ctx.ruleContent().ruleConditions().ID())
            for i in range(condition_count):
                c_id = ctx.ruleContent().ruleConditions().ID(i).getText()
                try:
                    if current_policy_id in self.__policy_conditions_map: # TODO: Refactor the access to maps with a generic function.
                        for condition in self.__policy_conditions_map[current_policy_id]:
                            if condition.name == c_id:
                                conditions.add(condition)
                                break  # Found it, no need to continue searching
                        else:  # This else corresponds to the for loop (executes if no break occurred)
                            raise UndefinedAttributeException("condition", c_id)
                    else:
                        raise Exception("Policy is not inconditions map.")
                except KeyError as e:
                    raise UndefinedAttributeException("condition", c_id) from e
                
        policy_participants = self._get_participants_for_policy(current_policy_id)
        if not policy_participants:
            raise Exception(f"No participants defined in policy {current_policy_id}")

        # people = {self.__participants[participant.ID().getText()] for participant in self.find_descendant_nodes_by_type(node=ctx.ruleContent(), target_type=govdslParser.ParticipantIDContext)}
        participants = self.find_descendant_nodes_by_type(node=ctx.ruleContent(),
                                                           target_type=govdslParser.ParticipantIDContext)
        people = set()
        for p in participants:
            p_id = p.ID().getText()
            # Search in policy's participants set
            for participant in policy_participants:
                if participant.name == p_id:
                    people.add(participant)
                    break
            else:
                raise UndefinedAttributeException("participant", p_id)

        base_rule = Rule(name=rule_name, conditions=conditions, participants=people)

        # Transform base rule into specific rule type
        match rule_type:
            case "Majority":
                rule = MajorityRule.from_rule(base_rule)
            case "Ratio":
                rule = RatioMajorityRule.from_rule(base_rule)
            case "LeaderDriven":
                default_name = ctx.ruleContent().default().ruleID().ID().getText()
                if default_name not in self.__rules:
                    raise UndefinedAttributeException("rule", default_name)
                default_rule = self.__rules[default_name]
                rule = LeaderDrivenRule.from_rule(base_rule, default=default_rule)
            case _:
                raise UnsupportedRuleTypeException(ctx.ruleType().getText())
        self._register_rule_with_current_policy(rule)

    # def exitPolicy(self, ctx:govdslParser.PolicyContext):

    #     self.__policy = SinglePolicy(name=ctx.ID().getText(), rules=set(self.__rules.values()), scopes=set(self.__policy_scopes.values()))

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
        
