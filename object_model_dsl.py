from besser.BUML.metamodel.structural import (
    Class, Property, Method, Parameter,
    BinaryAssociation, Generalization, DomainModel,
    Enumeration, EnumerationLiteral, Multiplicity,
    StringType, IntegerType, FloatType, BooleanType,
    TimeType, DateType, DateTimeType, TimeDeltaType,
    Constraint
)
from besser.BUML.metamodel.object import *
import datetime

#######################################
#       structural model definition   #
#######################################

# Generated from Modeling Editor

# Enumerations
TaskType: Enumeration = Enumeration(
    name="TaskType",
    literals={
            EnumerationLiteral(name="ALL"),
			EnumerationLiteral(name="ISSUE"),
			EnumerationLiteral(name="PULL_REQUEST")
    }
)

# Classes
Role = Class(name="Role")
Rule = Class(name="Rule")
Deadline = Class(name="Deadline")
Project = Class(name="Project")
Majority = Class(name="Majority")
RatioMajority = Class(name="RatioMajority")
LeaderDriven = Class(name="LeaderDriven")

# Role class attributes and methods
Role_name: Property = Property(name="name", type=StringType)
Role.attributes={Role_name}

# Rule class attributes and methods
Rule_name: Property = Property(name="name", type=StringType)
Rule_task: Property = Property(name="task", type=TaskType)
Rule.attributes={Rule_name, Rule_task}

# Deadline class attributes and methods
Deadline_timeStamp: Property = Property(name="timeStamp", type=StringType)
Deadline_name: Property = Property(name="name", type=StringType)
Deadline.attributes={Deadline_timeStamp, Deadline_name}

# Project class attributes and methods
Project_name: Property = Property(name="name", type=StringType)
Project.attributes={Project_name}

# Majority class attributes and methods
Majority_minVotes: Property = Property(name="minVotes", type=IntegerType)
Majority.attributes={Majority_minVotes}

# RatioMajority class attributes and methods
RatioMajority_ratio: Property = Property(name="ratio", type=FloatType)
RatioMajority.attributes={RatioMajority_ratio}

# LeaderDriven class attributes and methods


# Relationships
# Modified from the generated code TODO: Check if definitions are correct, some of them are overwritten, should we change the name?
project_from_role = Property(name="project", type=Project, multiplicity=Multiplicity(1, 1), is_composite=True)
roles_from_project = Property(name="roles", type=Role, multiplicity=Multiplicity(1, 9999))
Role_Project: BinaryAssociation = BinaryAssociation(
    name="Role_Project",
    ends={project_from_role, roles_from_project}
)

people = Property(name="people", type=Role, multiplicity=Multiplicity(1, 9999))
rules_from_role = Property(name="rules", type=Rule, multiplicity=Multiplicity(0, 9999))
Rule_Role: BinaryAssociation = BinaryAssociation(
    name="Rule_Role",
    ends={people, rules_from_role}
)

rules_from_project = Property(name="rules", type=Rule, multiplicity=Multiplicity(0, 9999))
project_from_rule = Property(name="project", type=Project, multiplicity=Multiplicity(1, 1), is_composite=True)
Rule_Project: BinaryAssociation = BinaryAssociation(
    name="Rule_Project",
    ends={rules_from_project, project_from_rule}
)

default = Property(name="default", type=Rule, multiplicity=Multiplicity(1, 1))
leaderDrivenRules = Property(name="leaderDrivenRules", type=LeaderDriven, multiplicity=Multiplicity(0, 9999))
LeaderDriven_Rule: BinaryAssociation = BinaryAssociation(
    name="LeaderDriven_Rule",
    ends={default, leaderDrivenRules}
)

deadlines = Property(name="deadlines", type=Deadline, multiplicity=Multiplicity(0, 9999))
project_from_deadline = Property(name="project", type=Project, multiplicity=Multiplicity(1, 1), is_composite=True)
Deadline_Project: BinaryAssociation = BinaryAssociation(
    name="Deadline_Project",
    ends={deadlines, project_from_deadline}
)

deadline = Property(name="deadline", type=Deadline, multiplicity=Multiplicity(1, 1))
rules_from_deadline = Property(name="rules", type=Rule, multiplicity=Multiplicity(0, 9999))
Rule_Deadline: BinaryAssociation = BinaryAssociation(
    name="Rule_Deadline",
    ends={deadline, rules_from_deadline}
)

# Generalizations
gen_RatioMajority_Majority = Generalization(general=Majority, specific=RatioMajority)
gen_Majority_Rule = Generalization(general=Rule, specific=Majority)
gen_LeaderDriven_Rule = Generalization(general=Rule, specific=LeaderDriven)

# Domain Model
domain_model = DomainModel(
    name="Class Diagram",
    types={Role, Rule, Deadline, Project, Majority, RatioMajority, LeaderDriven, TaskType},
    associations={Role_Project, Rule_Role, Rule_Project, LeaderDriven_Rule, Deadline_Project, Rule_Deadline},
    generalizations={gen_RatioMajority_Majority, gen_Majority_Rule, gen_LeaderDriven_Rule}
)


#######################################
#       object model definition       #
#######################################

# Project object attributes
project_obj_name: AttributeLink = AttributeLink(attribute=Project_name, value=DataValue(classifier=StringType, value="myProject"))
# Project object
project_obj: Object = Object(name="Project Object", classifier=Project, slots=[project_obj_name])

# Role object attributes
role_obj_committer_name: AttributeLink = AttributeLink(attribute=Role_name, value=DataValue(classifier=StringType, value="Committers"))
# Role object
role_obj_committer: Object = Object(name="Role Object", classifier=Role, slots=[role_obj_committer_name])

# Role object attributes
role_obj_contributor_name: AttributeLink = AttributeLink(attribute=Role_name, value=DataValue(classifier=StringType, value="Contributors"))
# Role object
role_obj_contributor: Object = Object(name="Role Object", classifier=Role, slots=[role_obj_contributor_name])

# Deadline object attributes
deadline_obj_7_days_timeStamp: AttributeLink = AttributeLink(attribute=Deadline_timeStamp, value=DataValue(classifier=StringType, value="7 days")) # TODO: Change type to deltaTime
deadline_obj_7_days_name: AttributeLink = AttributeLink(attribute=Deadline_name, value=DataValue(classifier=StringType, value="myDeadline"))
# Deadline object
deadline_obj_7_days: Object = Object(name="Deadline Object", classifier=Deadline, slots=[deadline_obj_7_days_timeStamp, deadline_obj_7_days_name])

# Deadline object attributes
deadline_obj_2_days_timeStamp: AttributeLink = AttributeLink(attribute=Deadline_timeStamp, value=DataValue(classifier=StringType, value="2 days")) # TODO: Change type to deltaTime
deadline_obj_2_days_name: AttributeLink = AttributeLink(attribute=Deadline_name, value=DataValue(classifier=StringType, value="my2Deadline"))
# Deadline object
deadline_obj_2_days: Object = Object(name="Deadline Object", classifier=Deadline, slots=[deadline_obj_2_days_timeStamp, deadline_obj_2_days_name])

# Majority object attributes
majority_obj_minVotes: AttributeLink = AttributeLink(attribute=Majority_minVotes, value=DataValue(classifier=IntegerType, value=0))
majority_obj_name: AttributeLink = AttributeLink(attribute=Rule_name, value=DataValue(classifier=StringType, value="myMajorityRule"))
majority_obj_task: AttributeLink = AttributeLink(attribute=Rule_task, value=DataValue(classifier=TaskType, value="ISSUE"))
# Majority object
majority_obj: Object = Object(name="Majority Object", classifier=Majority, slots=[majority_obj_minVotes])

## TODO: Check if hierarchy are defined as above.
# # Rule object attributes
# rule_obj_name: AttributeLink = AttributeLink(attribute=Rule_name, value=DataValue(classifier=StringType, value="myMajorityRule"))
# rule_obj_task: AttributeLink = AttributeLink(attribute=Rule_task, value=DataValue(classifier=TaskType, value="ISSUE"))
# # Rule object
# rule_obj: Object = Object(name="Rule Object", classifier=Rule, slots=[rule_obj_name, rule_obj_task])

## Links

# Project object and Role object link
project_link_end1: LinkEnd = LinkEnd(name="project_end1", association_end=project_from_role, object=project_obj)
role_link_end_committer: LinkEnd = LinkEnd(name="role_end_committer", association_end=roles_from_project, object=role_obj_committer)
role_project_link: Link = Link(name="role_project_link", association=Role_Project, connections=[project_link_end1,role_link_end_committer])

project_link_end2: LinkEnd = LinkEnd(name="project_end2", association_end=project_from_role, object=project_obj)
role_link_end_contributor: LinkEnd = LinkEnd(name="role_end_contributor", association_end=roles_from_project, object=role_obj_contributor)
role_project_link2: Link = Link(name="role_project_link2", association=Role_Project, connections=[project_link_end2,role_link_end_contributor])

# Project object and Deadline object link
project_link_end3: LinkEnd = LinkEnd(name="project_end3", association_end=project_from_deadline, object=project_obj)
deadline_link_end_7_days: LinkEnd = LinkEnd(name="deadline_end", association_end=deadlines, object=deadline_obj_7_days)
deadline_project_link: Link = Link(name="deadline_project_link", association=Deadline_Project, connections=[project_link_end3,deadline_link_end_7_days])

project_link_end4: LinkEnd = LinkEnd(name="project_end4", association_end=project_from_deadline, object=project_obj)
deadline_link_end_2_days: LinkEnd = LinkEnd(name="deadline_end2", association_end=deadlines, object=deadline_obj_2_days)
deadline_project_link2: Link = Link(name="deadline_project_link2", association=Deadline_Project, connections=[project_link_end4,deadline_link_end_2_days])

# Project object and Majority object link
project_link_end5: LinkEnd = LinkEnd(name="project_end5", association_end=project_from_rule, object=project_obj)
majority_link_end1: LinkEnd = LinkEnd(name="majority_end1", association_end=rules_from_project, object=majority_obj)
majority_project_link: Link = Link(name="majority_project_link", association=Rule_Project, connections=[majority_link_end1,project_link_end5])

# Majority object and Role object link
role_link_end_committer2: LinkEnd = LinkEnd(name="role_end_committer2", association_end=roles_from_project, object=role_obj_committer)
majority_link_end2: LinkEnd = LinkEnd(name="majority_end2", association_end=rules_from_role, object=majority_obj)
role_majority_link: Link = Link(name="role_majority_link", association=Rule_Role, connections=[role_link_end_committer2,majority_link_end2])

# Majority object and Deadline object link
deadline_link_end_7_days2: LinkEnd = LinkEnd(name="deadline_end2", association_end=deadlines, object=deadline_obj_7_days)
majority_link_end3: LinkEnd = LinkEnd(name="majority_end3", association_end=rules_from_deadline, object=majority_obj)
deadline_majority_link: Link = Link(name="deadline_majority_link", association=Rule_Deadline, connections=[deadline_link_end_7_days2,majority_link_end3])


# Object model definition
object_model: ObjectModel = ObjectModel(name="Object model", instances={project_obj, deadline_obj_2_days, deadline_obj_7_days, role_obj_committer, role_obj_contributor, majority_obj}, links={role_project_link, role_project_link2, deadline_project_link, deadline_project_link2, majority_project_link, role_majority_link, deadline_majority_link})