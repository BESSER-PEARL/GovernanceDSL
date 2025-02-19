# See: https://github.com/BESSER-PEARL/governanceDSL/issues/6

# Generated B-UML Model
from besser.BUML.metamodel.structural import (
    Class, Property, Method, Parameter,
    BinaryAssociation, Generalization, DomainModel,
    Enumeration, EnumerationLiteral, Multiplicity,
    StringType, IntegerType, FloatType, BooleanType,
    TimeType, DateType, DateTimeType, TimeDeltaType,
    Constraint
)

# Enumerations
VotingThreshold: Enumeration = Enumeration(
    name="VotingThreshold",
    literals={
            EnumerationLiteral(name="XXX%"),
			EnumerationLiteral(name="Majority"),
			EnumerationLiteral(name="AbsoluteMajority")
    }
)

# Classes
Conditions = Class(name="Conditions")
Activity = Class(name="Activity")
VotingRule = Class(name="VotingRule")
Deadline = Class(name="Deadline")
Task = Class(name="Task")
PullRequestReview = Class(name="PullRequestReview")
Individual = Class(name="Individual")
Role = Class(name="Role")
Rule = Class(name="Rule")
Development = Class(name="Development")
Project = Class(name="Project")
Scope = Class(name="Scope")
Participants = Class(name="Participants")
Policy = Class(name="Policy")

# Conditions class attributes and methods
Conditions_attribute: Property = Property(name="attribute", type=StringType)
Conditions.attributes={Conditions_attribute}

# Activity class attributes and methods
Activity_attribute: Property = Property(name="attribute", type=StringType)
Activity.attributes={Activity_attribute}

# VotingRule class attributes and methods
VotingRule_type: Property = Property(name="type", type=VotingThreshold)
VotingRule.attributes={VotingRule_type}

# Deadline class attributes and methods
Deadline_int: Property = Property(name="int", type=StringType)
Deadline_maxDate: Property = Property(name="maxDate", type=DateType)
Deadline.attributes={Deadline_int, Deadline_maxDate}

# Task class attributes and methods
Task_attribute: Property = Property(name="attribute", type=StringType)
Task.attributes={Task_attribute}

# PullRequestReview class attributes and methods
PullRequestReview_attribute: Property = Property(name="attribute", type=StringType)
PullRequestReview.attributes={PullRequestReview_attribute}

# Individual class attributes and methods
Individual_attribute: Property = Property(name="attribute", type=StringType)
Individual.attributes={Individual_attribute}

# Role class attributes and methods
Role_attribute: Property = Property(name="attribute", type=StringType)
Role.attributes={Role_attribute}

# Rule class attributes and methods
Rule_int: Property = Property(name="int", type=StringType)
Rule.attributes={Rule_int}

# Development class attributes and methods
Development_attribute: Property = Property(name="attribute", type=StringType)
Development.attributes={Development_attribute}

# Project class attributes and methods
Project_attribute: Property = Property(name="attribute", type=StringType)
Project.attributes={Project_attribute}

# Scope class attributes and methods
Scope_attribute: Property = Property(name="attribute", type=StringType)
Scope.attributes={Scope_attribute}

# Participants class attributes and methods
Participants_attribute: Property = Property(name="attribute", type=StringType)
Participants.attributes={Participants_attribute}

# Policy class attributes and methods
Policy_attribute: Property = Property(name="attribute", type=StringType)
Policy.attributes={Policy_attribute}

# Relationships
Conditions_Rule: BinaryAssociation = BinaryAssociation(
    name="Conditions_Rule",
    ends={
        Property(name="", type=Rule, multiplicity=Multiplicity(0, 9999)),
        Property(name="", type=Conditions, multiplicity=Multiplicity(0, 9999))
    }
)
Policy_Rule: BinaryAssociation = BinaryAssociation(
    name="Policy_Rule",
    ends={
        Property(name="", type=Rule, multiplicity=Multiplicity(0, 9999)),
        Property(name="", type=Policy, multiplicity=Multiplicity(1, 1))
    }
)
Scope_Policy: BinaryAssociation = BinaryAssociation(
    name="Scope_Policy",
    ends={
        Property(name="impactedElement", type=Scope, multiplicity=Multiplicity(0, 9999)),
        Property(name="", type=Policy, multiplicity=Multiplicity(0, 1))
    }
)
Project_Activity: BinaryAssociation = BinaryAssociation(
    name="Project_Activity",
    ends={
        Property(name="", type=Activity, multiplicity=Multiplicity(0, 9999)),
        Property(name="", type=Project, multiplicity=Multiplicity(1, 1))
    }
)
Activity_Task: BinaryAssociation = BinaryAssociation(
    name="Activity_Task",
    ends={
        Property(name="", type=Activity, multiplicity=Multiplicity(1, 1)),
        Property(name="", type=Task, multiplicity=Multiplicity(0, 9999))
    }
)
Has: BinaryAssociation = BinaryAssociation(
    name="Has",
    ends={
        Property(name="", type=Role, multiplicity=Multiplicity(0, 9999)),
        Property(name="", type=Individual, multiplicity=Multiplicity(1, 1))
    }
)
Rule_Participants: BinaryAssociation = BinaryAssociation(
    name="Rule_Participants",
    ends={
        Property(name="", type=Participants, multiplicity=Multiplicity(0, 9999)),
        Property(name="", type=Rule, multiplicity=Multiplicity(1, 1))
    }
)

# Generalizations
gen_PullRequestReview_Task = Generalization(general=Task, specific=PullRequestReview)
gen_Role_Participants = Generalization(general=Participants, specific=Role)
gen_Project_Scope = Generalization(general=Scope, specific=Project)
gen_VotingRule_Rule = Generalization(general=Rule, specific=VotingRule)
gen_Activity_Scope = Generalization(general=Scope, specific=Activity)
gen_Deadline_Conditions = Generalization(general=Conditions, specific=Deadline)
gen_Task_Scope = Generalization(general=Scope, specific=Task)
gen_Individual_Participants = Generalization(general=Participants, specific=Individual)
gen_Development_Activity = Generalization(general=Activity, specific=Development)

# Domain Model
domain_model = DomainModel(
    name="Class Diagram",
    types={Conditions, Activity, VotingRule, Deadline, Task, PullRequestReview, Individual, Role, Rule, Development, Project, Scope, Participants, Policy, VotingThreshold},
    associations={Conditions_Rule, Policy_Rule, Scope_Policy, Project_Activity, Activity_Task, Has, Rule_Participants},
    generalizations={gen_PullRequestReview_Task, gen_Role_Participants, gen_Project_Scope, gen_VotingRule_Rule, gen_Activity_Scope, gen_Deadline_Conditions, gen_Task_Scope, gen_Individual_Participants, gen_Development_Activity}
)
