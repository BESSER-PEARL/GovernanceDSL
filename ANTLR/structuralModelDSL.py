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