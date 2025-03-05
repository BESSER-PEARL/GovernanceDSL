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
from metamodel.governance import (
    SinglePolicy, Project, Activity, Task, Role, Individual,
    Deadline, Rule, MajorityRule, RatioMajorityRule,
    LeaderDrivenRule, VotingCondition, TaskTypeEnum, PlatformEnum
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
        self.__project = None
        self.__project_activities = {}
        self.__scopes = {}
        self.__policy_scopes = {}
        self.__participants = {}
        self.__conditions = {}
        self.__rules = {}

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

    def enterActivity(self, ctx:govdslParser.ActivityContext):
        activity_name = ctx.ID().getText()
        activity = Activity(name=activity_name) # TODO: relationship with tasks, tasks=activity_tasks)
        # self.__project_activities[activity_name] = activity # TODO: work in relationships
        self.__scopes[activity_name] = activity
    
    def enterTask(self, ctx:govdslParser.TaskContext):
        task_name = ctx.ID().getText()
        task_type_str = ctx.taskType().getText()
        task_type_enum = self.convert_string_to_task_type(task_type_str)
        task = Task(name=task_name, task_type=task_type_enum)
        self.__scopes[task_name] = task

    
    def exitProject(self, ctx:govdslParser.ProjectContext):
        project_name = ctx.ID().getText()
        platform_str = ctx.platform().getText()
        platform_enum = self.convert_string_to_platform(platform_str)
        repo_id = ctx.repoID().getText()
        project = Project(name=project_name, platform=platform_enum, project_id=repo_id) # TODO: relationship with activities, activities=set(self.__project_activities.values())
        self.__scopes[project_name] = project
        
    def enterRoles(self, ctx:govdslParser.RolesContext): 

        roles = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.ParticipantIDContext)
        for r in roles:
            role = Role(name=r.ID().getText())
            self.__participants[r.ID().getText()] = role # WARNING: This might generate conflict if there is a role with the same name as a individual
    
    def enterIndividuals(self, ctx:govdslParser.IndividualsContext):
        
        individuals = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.ParticipantIDContext)
        for i in individuals:
            individual = Individual(name=i.ID().getText())
            self.__participants[i.ID().getText()] = individual
            
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
        self.__conditions[name] = deadline

    def enterVotingCondition(self, ctx:govdslParser.VotingConditionContext):
        
        name = ctx.voteConditionID().ID().getText()
        min_votes = None
        ratio = None
        if ctx.minVotes():
            min_votes = int(ctx.minVotes().SIGNED_INT().getText())
        if ctx.ratio():
            ratio = float(ctx.ratio().FLOAT().getText())
        condition = VotingCondition(name=name, minVotes=min_votes, ratio=ratio)
        self.__conditions[name] = condition 

    def enterRule(self, ctx:govdslParser.RuleContext):
        
        rule_name = ctx.ruleID().ID().getText()
        rule_type = ctx.ruleType().getText()

        conditions = set()
        if ctx.ruleContent().ruleConditions():
            condition_count = len(ctx.ruleContent().ruleConditions().ID())
            for i in range(condition_count):
                c_id = ctx.ruleContent().ruleConditions().ID(i).getText()
                try:
                    conditions.add(self.__conditions[c_id])
                except KeyError as e:
                    raise UndefinedAttributeException("condition", c_id) from e
                
        try:
            people = {self.__participants[participant.ID().getText()] for participant in self.find_descendant_nodes_by_type(node=ctx.ruleContent(), target_type=govdslParser.ParticipantIDContext)}
        except KeyError as e:
            raise UndefinedAttributeException("participant", e.args[0]) from e

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
        self.__rules[rule_name] = rule

    def enterAppliedTo(self, ctx:govdslParser.AppliedToContext):
        scope_count = len(ctx.ID())
        for i in range(scope_count):
            scope_name = ctx.ID(i).getText()
            try:
                scope = self.__scopes[scope_name]
                self.__policy_scopes[scope_name] = scope
            except KeyError as e:
                raise UndefinedAttributeException("scope", scope_name) from e

    def exitPolicy(self, ctx:govdslParser.PolicyContext):

        self.__policy = SinglePolicy(name=ctx.ID().getText(), rules=set(self.__rules.values()), scopes=set(self.__policy_scopes.values()))
