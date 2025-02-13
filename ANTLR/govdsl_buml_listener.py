import warnings
from besser.BUML.metamodel.structural import DomainModel, Class, Multiplicity, Property, \
    BinaryAssociation, Generalization, Enumeration, EnumerationLiteral, Method, Parameter, \
    Method, StringType, IntegerType, FloatType, BooleanType, TimeType, DateType, DateTimeType, \
    TimeDeltaType, Constraint
from besser.BUML.metamodel.object import (
    AttributeLink, Object, DataValue, LinkEnd, Link
)
from .structuralModelDSL import (
    Role, Rule, Deadline, Project, Majority, RatioMajority, LeaderDriven,
    Role_Project, roles_from_project, project_from_role, Deadline_Project, project_from_deadline,
    Rule_Project, rules_from_project, project_from_rule,
    Role_name, Rule_name, Rule_task, Deadline_timeStamp, Deadline_name, Project_name,
    Majority_minVotes, RatioMajority_ratio
)
from .govdslParser import govdslParser
from .govdslListener import govdslListener

class BUMLGenerationListener(govdslListener):
    """
       This listener class generates a B-UML object model from a parse-tree 
       representing a govDSL textual notation
    """
    def __init__(self):
        self.__buml_object_model = None
        # self.__buml_model = read structural/import
        self.links = [] # TODO: Refactor using setters
        self.object_instances = {}

    
    def get_buml_model(self):
        """DomainModel: Retrieves the B-UML model instance."""
        return self.__buml_model
    
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
    
    def enterProject(self, ctx:govdslParser.ProjectContext):


        # Project object attributes
        project_obj_name: AttributeLink = AttributeLink(attribute=Project_name, value=DataValue(classifier=StringType, value=ctx.ID().getText()))
        # Project object
        project_obj: Object = Object(name="Project Object", classifier=Project, slots=[project_obj_name]) # WARNING: The name of the object is hardcoded. This is because we only have one project. If we have multiple projects, we need to change this to the ID. We do this because the project is accessed in the enter functions of each related objects.
        self.object_instances[project_obj.name] = project_obj
    
    def enterRoleID(self, ctx:govdslParser.RoleIDContext): # TODO: Go back to roles

        
        role_obj_name: AttributeLink = AttributeLink(attribute=Role_name, value=DataValue(classifier=StringType, value=ctx.ID().getText()))
        role_obj: Object = Object(name=ctx.ID().getText(), classifier=Role, slots=[role_obj_name])
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
            deadline_obj_name: AttributeLink = AttributeLink(attribute=Deadline_name, value=DataValue(classifier=StringType, value=d.deadlineID().ID().getText())) # TODO: IVAN: Can we access attributes like this? Also, is name necessary since object has a name attribute?
            deadline_time = str(d.INT()) + " " + d.timeUnit().getText() # TODO: Format as timeDelta
            deadline_obj_time: AttributeLink = AttributeLink(attribute=Deadline_timeStamp, value=DataValue(classifier=StringType, value=deadline_time))
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
            rule_obj_task: AttributeLink = AttributeLink(attribute=Rule_task, value=DataValue(classifier=StringType, value=r.appliedTo().getText())) # TODO: Change it to enumeration. Define an enumeration in the domain model.
            if r.ruleType().getText() == "Majority":
                rule_obj_minVotes: AttributeLink = AttributeLink(attribute=Majority_minVotes, value=DataValue(classifier=IntegerType, value=r.ruleContent.minVotes.INT()))
                rule_obj: Object = Object(name=r.ruleID().ID().getText(), classifier=Majority, slots=[rule_obj_name, rule_obj_task, rule_obj_minVotes])
            else:
                rule_obj: Object = Object(name=r.ruleID().ID().getText(), classifier=Rule, slots=[rule_obj_name, rule_obj_task])
            self.object_instances[rule_obj.name] = rule_obj # TODO: Is this good practice? Should we add it in each if/else block?

            project_link_end: LinkEnd = LinkEnd(name="project_end", association_end=project_from_rule, object=self.object_instances["Project Object"]) # WARNING: See enterProject warning.
            rule_link_end: LinkEnd = LinkEnd(name="majority_end", association_end=rules_from_project, object=rule_obj)
            rule_project_link: Link = Link(name="majority_project_link" + str(i), association=Rule_Project, connections=[rule_link_end,project_link_end])
            self.links.append(rule_project_link)
            i += 1

        def exitProject(self, ctx:govdslParser.ProjectContext):
            
            roles = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.RolesContext)
            deadlines = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.DeadlinesContext)
            rules = self.find_descendant_nodes_by_type(node=ctx,
                                                target_type=govdslParser.RulesContext)