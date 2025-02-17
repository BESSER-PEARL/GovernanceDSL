import warnings
from besser.BUML.metamodel.structural import (
    StringType, IntegerType, FloatType, TimeDeltaType
)
from besser.BUML.metamodel.object import (
    AttributeLink, Object, DataValue, LinkEnd, Link, ObjectModel
)
from structuralModelDSL import (
    Role, Rule, Deadline, Project, Majority, RatioMajority, LeaderDriven,
    Role_Project, roles_from_project, project_from_role, Deadline_Project, project_from_deadline,
    Rule_Project, rules_from_project, project_from_rule,
    Role_name, Rule_name, Rule_task, Deadline_timeStamp, Deadline_name, Project_name,
    Majority_minVotes, RatioMajority_ratio, rules_from_role, people, Rule_Role,
    rules_from_deadline, deadline_from_rule, Rule_Deadline, TaskType, default,
    leaderDriven_rules, LeaderDriven_Rule, Phased, phases_from_rule, Phased_Rule,
)
from govdslParser import govdslParser
from govdslListener import govdslListener
from datetime import timedelta

class BUMLGenerationListener(govdslListener):
    """
       This listener class generates a B-UML object model from a parse-tree 
       representing a govDSL textual notation
    """
    def __init__(self):
        super().__init__()
        self.__buml_object_model = None
        # self.__buml_model = read structural/import
        self.links = [] # TODO: Refactor using setters; is it needed? Since names can be repeated...
        self.object_instances = {}

    
    # def get_buml_model(self):
    #     """DomainModel: Retrieves the B-UML model instance."""
    #     return self.__buml_model
    
    def get_buml_object_model(self):
        """ObjectModel: Retrieves the B-UML object model instance."""
        return self.__buml_object_model
    
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
    
    def find_people_from_rule(self, rule: govdslParser.RuleContext) -> list[str]:
        """
        Finds all roles associated with a rule.

        Args:
            rule: The rule node to search for associated roles.
        
        Returns:
            A list of role IDs associated with the rule.
        """
        people_roles_list = self.find_descendant_nodes_by_type(node=rule,
                                            target_type=govdslParser.RoleIDContext)
        people_list = []
        for p in people_roles_list:
            people_list.append(p.ID().getText())
        return people_list
    
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
        
        # Project object attributes
        project_obj_name: AttributeLink = AttributeLink(attribute=Project_name, value=DataValue(classifier=StringType, value=ctx.ID().getText()))
        # Project object
        project_obj: Object = Object(name="Project Object", classifier=Project, slots=[project_obj_name]) # WARNING: The name of the object is hardcoded. This is because we only have one project. If we have multiple projects, we need to change this to the ID. We do this because the project is accessed in the enter functions of each related objects.
        self.object_instances[project_obj.name] = project_obj
    
    def enterRoles(self, ctx:govdslParser.RolesContext): 

        roles = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.RoleIDContext)

        # We grab all descendants from Roles because we need to define all the role objects. 
        # For instantiating objects we cannot do it in enterRoleID since it is called from other rules (which will be associations)
        for r in roles: 
            role_obj_name: AttributeLink = AttributeLink(attribute=Role_name, value=DataValue(classifier=StringType, value=r.ID().getText()))
            role_obj: Object = Object(name=r.ID().getText(), classifier=Role, slots=[role_obj_name])
            self.object_instances[role_obj.name] = role_obj


            project_link_end: LinkEnd = LinkEnd(name="project_end", association_end=project_from_role, object=self.object_instances["Project Object"]) # WARNING: See enterProject warning.
            role_link_end: LinkEnd = LinkEnd(name="role_end", association_end=roles_from_project, object=role_obj)
            role_project_link: Link = Link(name="role_project_link", association=Role_Project, connections=[project_link_end,role_link_end]) # I am naming the links with a number to avoid duplicates. Is it required?
            self.links.append(role_project_link)

    def enterDeadlines(self, ctx:govdslParser.DeadlinesContext):

        deadlines = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.DeadlineContext)
        i = 0
        for d in deadlines:
            deadline_obj_name: AttributeLink = AttributeLink(attribute=Deadline_name, value=DataValue(classifier=StringType, value=d.deadlineID().ID().getText()))
            deadline_time = self.deadline_to_timedelta(amount=int(d.INT().getText()), time_unit=d.timeUnit().getText())
            deadline_obj_time: AttributeLink = AttributeLink(attribute=Deadline_timeStamp, value=DataValue(classifier=TimeDeltaType, value=deadline_time))
            deadline_obj: Object = Object(name=d.deadlineID().ID().getText(), classifier=Deadline, slots=[deadline_obj_name, deadline_obj_time])
            self.object_instances[deadline_obj.name] = deadline_obj

            project_link_end3: LinkEnd = LinkEnd(name="project_end", association_end=project_from_deadline, object=self.object_instances["Project Object"]) # WARNING: See enterProject warning.
            deadline_link_end_7_days: LinkEnd = LinkEnd(name="deadline_end", association_end=deadlines, object=deadline_obj)
            deadline_project_link: Link = Link(name="deadline_project_link" + str(i), association=Deadline_Project, connections=[project_link_end3,deadline_link_end_7_days])
            self.links.append(deadline_project_link)
            i += 1

    def enterRules(self, ctx:govdslParser.RulesContext):
        
        rules = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.RuleContext)
        
        i = 0
        for r in rules:
            rule_obj_name: AttributeLink = AttributeLink(attribute=Rule_name, value=DataValue(classifier=StringType, value=r.ruleID().ID().getText()))
            rule_obj_task: AttributeLink = AttributeLink(attribute=Rule_task, value=DataValue(classifier=TaskType, value=r.ruleContent().appliedTo().taskID().getText())) # TODO: Change it to enumeration. There is no validation on the type. Now it is saved as Pull request, but it should be TaskType.PULL_REQUEST
            rule_obj: Object = Object(name=None, classifier=None, slots=None)
            match r.ruleType().getText():
                case "Majority":
                    rule_obj_minVotes: AttributeLink = AttributeLink(attribute=Majority_minVotes, value=DataValue(classifier=IntegerType, value=int(r.ruleContent().minVotes().INT().getText())))
                    rule_obj.name = r.ruleID().ID().getText()
                    rule_obj.classifier = Majority
                    rule_obj.slots = [rule_obj_name, rule_obj_task, rule_obj_minVotes]
                    # rule_obj: Object = Object(name=r.ruleID().ID().getText(), classifier=Majority, slots=[rule_obj_name, rule_obj_task, rule_obj_minVotes])
                case "RatioMajority":
                    rule_obj_minVotes: AttributeLink = AttributeLink(attribute=Majority_minVotes, value=DataValue(classifier=IntegerType, value=int(r.ruleContent().minVotes().INT().getText())))
                    rule_obj_ratio: AttributeLink = AttributeLink(attribute=RatioMajority_ratio, value=DataValue(classifier=FloatType, value=float(r.ruleContent().ratio().FLOAT().getText())))
                    rule_obj.name = r.ruleID().ID().getText()
                    rule_obj.classifier = RatioMajority
                    rule_obj.slots = [rule_obj_name, rule_obj_task, rule_obj_minVotes, rule_obj_ratio]
                    # rule_obj: Object = Object(name=r.ruleID().ID().getText(), classifier=RatioMajority, slots=[rule_obj_name, rule_obj_task, rule_obj_minVotes, rule_obj_ratio])
                case "LeaderDriven":
                    rule_obj.name = r.ruleID().ID().getText()
                    rule_obj.classifier = LeaderDriven
                    rule_obj.slots = [rule_obj_name, rule_obj_task]
                    # rule_obj: Object = Object(name=r.ruleID().ID().getText(), classifier=LeaderDriven, slots=[rule_obj_name, rule_obj_task])

                    default_link_end: LinkEnd = LinkEnd(name="default_end", association_end=default, object=self.object_instances[r.ruleContent().default().ruleID().ID().getText()]) 
                    rule_link_end: LinkEnd = LinkEnd(name="rule_end", association_end=leaderDriven_rules, object=rule_obj)
                    rule_project_link: Link = Link(name="leaderDriven_default_link", association=LeaderDriven_Rule, connections=[rule_link_end,default_link_end])
                    self.links.append(rule_project_link)
                case "Phased":
                    rule_obj.name = r.ruleID().ID().getText()
                    rule_obj.classifier = Phased
                    rule_obj.slots = [rule_obj_name, rule_obj_task]
                    # rule_obj: Object = Object(name=r.ruleID().ID().getText(), classifier=Phased, slots=[rule_obj_name, rule_obj_task])

                    phases = self.find_descendant_nodes_by_type(node=r,
                                                target_type=govdslParser.PhasesContext)
                    
                    for p in phases:
                        phased_link_end: LinkEnd = LinkEnd(name="phased_end", association_end=phases_from_rule, object=self.object_instances[p.ruleID().ID().getText()]) 
                        rule_link_end: LinkEnd = LinkEnd(name="rule_end", association_end=phases, object=rule_obj)
                        rule_project_link: Link = Link(name="phased_phases_link", association=Phased_Rule, connections=[rule_link_end,phased_link_end])
                        self.links.append(rule_project_link)

                case _: # Since Rule class is not abstract we could create a default rule object. To change in the model?
                    rule_obj: Object = Object(name=r.ruleID().ID().getText(), classifier=Rule, slots=[rule_obj_name, rule_obj_task])
            
            self.object_instances[rule_obj.name] = rule_obj 

            project_link_end: LinkEnd = LinkEnd(name="project_end", association_end=project_from_rule, object=self.object_instances["Project Object"]) # WARNING: See enterProject warning.
            rule_link_end: LinkEnd = LinkEnd(name="rule_end", association_end=rules_from_project, object=rule_obj)
            rule_project_link: Link = Link(name="rule_project_link" + str(i), association=Rule_Project, connections=[rule_link_end,project_link_end])
            self.links.append(rule_project_link)

            # WARNING: We can set the links here if, and only if, the roles and deadlines are defined before the rules (as in the example)
            people_from_rule = self.find_people_from_rule(r)
            j = 0
            for p in people_from_rule:
                role_link_end: LinkEnd = LinkEnd(name="role_end", association_end=people, object=self.object_instances[p])
                rule_link_end: LinkEnd = LinkEnd(name="rule_end", association_end=rules_from_role, object=rule_obj)
                role_rule_link: Link = Link(name="role_rule_link" + str(j), association=Rule_Role, connections=[role_link_end,rule_link_end])
                self.links.append(role_rule_link)
                j += 1
            
            # TODO: Naming cannot go like this. We need to find a way to name the links properly. If we have multiple rules, we will have multiple links with the same name.
            deadline_link_end: LinkEnd = LinkEnd(name="deadline_end", association_end=deadline_from_rule, object=self.object_instances[r.ruleContent().deadlineID().ID().getText()]) 
            rule_link_end: LinkEnd = LinkEnd(name="rule_end", association_end=rules_from_deadline, object=rule_obj)
            deadline_rule_link: Link = Link(name="deadline_rule_link", association=Rule_Deadline, connections=[deadline_link_end,rule_link_end])
            self.links.append(deadline_rule_link)

            i += 1

        

    def exitProject(self, ctx:govdslParser.ProjectContext):
        
        # We can now create the object model
        self.__buml_object_model = ObjectModel(name="Object Model", instances=list(self.object_instances.values()), links=self.links)
