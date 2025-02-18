import warnings
from govdslParser import govdslParser
from govdslListener import govdslListener
from besser.BUML.metamodel.structural import (
    StringType, IntegerType, FloatType, TimeDeltaType
)
from governance import (
    Project, Role, Deadline, Rule, Majority, RatioMajority, LeaderDriven, Phased,
    CollaborationType, Stage, RangeType
)
from datetime import timedelta

class ProjectCreationListener(govdslListener):
    """
       This listener class generates a governance object model from a parsed DSL file.
    """
    def __init__(self):
        super().__init__()
        self.__project = None
        self.__roles = {}
        self.__deadlines = {}
        self.__rules = {}

    
    def get_project(self):
        """Project: Retrieves the Project instance."""
        return self.__project
    
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
    

    def enterProject(self, ctx:govdslParser.ProjectContext):

        # We define the project first, and updating the links on the go.
        self.__project = Project(name=ctx.ID().getText(), roles=None, deadlines=None, rules=None)
    
    def enterRoles(self, ctx:govdslParser.RolesContext): 

        roles = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.RoleIDContext)
        for r in roles: 
            role = Role(name=r.ID().getText())
            self.__roles[r.ID().getText()] = role
        self.__project.roles = set(self.__roles.values())

    def enterDeadlines(self, ctx:govdslParser.DeadlinesContext):

        deadlines = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.DeadlineContext)

        for d in deadlines:
            deadline_time = self.deadline_to_timedelta(amount=int(d.INT().getText()), time_unit=d.timeUnit().getText())
            deadline = Deadline(name=d.deadlineID().ID().getText(), ts=deadline_time)
            self.__deadlines[d.deadlineID().ID().getText()] = deadline
        self.__project.deadlines = set(self.__deadlines.values())

            # match d.deadlineType().getText(): # TODO: Manage subclasses

    def enterRules(self, ctx:govdslParser.RulesContext):
        
        rules = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.RuleContext)
        
        for r in rules:
            # Create base Rule instance with common attributes
            rule_name = r.ruleID().ID().getText()
            deadline_name = r.ruleContent().deadlineID().ID().getText()
            applied_to = CollaborationType[r.ruleContent().appliedTo().collaborationID().getText().replace(" ", "_").upper()]
            try:
                people = {self.__roles[role.ID().getText()] for role in self.find_descendant_nodes_by_type(node=r.ruleContent(), target_type=govdslParser.RoleIDContext)}
            except KeyError as e:
                # TODO: Define Exception type
                raise Exception(f"Role '{e.args[0]}' not defined.")
            
            if deadline_name not in self.__deadlines:
                raise Exception(f"Deadline '{deadline_name}' not defined.")
            deadline = self.__deadlines[deadline_name]

            stage = Stage(r.ruleContent().stage().stageID().getText().replace(" ", "_").upper())
            
            base_rule = Rule(name=rule_name, applied_to=applied_to, stage=stage,
                            query_filter="", deadline=deadline, people=people) # TODO: Manage query filter
        
            # Transform base rule into specific rule type
            match r.ruleType().getText():
                case "Majority":
                    min_votes = int(r.ruleContent().minVotes().INT().getText())
                    range_type = RangeType(r.ruleContent().rangeType().rangeID().getText().replace(" ", "_").upper())
                    rule = Majority.from_rule(base_rule, min_votes=min_votes, range_type=range_type)
                case "RatioMajority":
                    min_votes = int(r.ruleContent().minVotes().INT().getText())
                    range_type = RangeType(r.ruleContent().rangeType().rangeID().getText().replace(" ", "_").upper())
                    ratio = float(r.ruleContent().ratio().FLOAT().getText())
                    rule = RatioMajority.from_rule(base_rule, min_votes=min_votes, range_type=range_type, ratio=ratio)
                case "LeaderDriven":
                    default_name = r.ruleContent().default().ruleID().ID().getText()
                    if default_name not in self.__rules:
                        raise Exception(f"Rule '{default_name}' not defined.")
                    default_rule = self.__rules[default_name]
                    rule = LeaderDriven.from_rule(base_rule, default=default_rule)
                case "Phased":
                    phases_id = self.find_descendant_nodes_by_type(node=r,
                                                target_type=govdslParser.RuleIDContext)
                    phases = set()
                    for p_id in phases_id:
                        phase_rule_name = p_id.ID().getText()
                        if phase_rule_name not in self.__rules:
                            raise Exception(f"Rule '{phase_rule_name}' not defined.")
                        phase_rule = self.__rules[phase_rule_name]
                        phases.add(phase_rule)
                    rule = Phased.from_rule(base_rule, phases=phases)
                case _: 
                    raise Exception(f"Unsupported rule type: {r.ruleType().getText()}")
            self.__rules[rule_name] = rule