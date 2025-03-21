# Generated B-UML Model
from besser.BUML.metamodel.structural import (
    Class, Property, Method, Parameter,
    BinaryAssociation, Generalization, DomainModel,
    Enumeration, EnumerationLiteral, Multiplicity,
    StringType, IntegerType, FloatType, BooleanType,
    TimeType, DateType, DateTimeType, TimeDeltaType,
    AnyType, Constraint
)

# Enumerations
StatusEnum: Enumeration = Enumeration(
    name="StatusEnum",
    literals={
            EnumerationLiteral(name="COMPLETED"),
			EnumerationLiteral(name="ACCEPT"),
			EnumerationLiteral(name="PARTIAL")
    }
)

OrderEnum: Enumeration = Enumeration(
    name="OrderEnum",
    literals={
            EnumerationLiteral(name="SEQUENTIAL_EXCLUSIVE"),
			EnumerationLiteral(name="SEQUENTIAL_INCLUSIV")
    }
)

# Classes
Project = Class(name="Project")
Activity = Class(name="Activity")
Task = Class(name="Task")
Scope = Class(name="Scope", is_abstract=True)
Policy = Class(name="Policy", is_abstract=True)
ComposedPolicy = Class(name="ComposedPolicy")
SinglePolicy = Class(name="SinglePolicy", is_abstract=True)
LeaderDrivenPolicy = Class(name="LeaderDrivenPolicy")
VotingPolicy = Class(name="VotingPolicy", is_abstract=True)
Condition = Class(name="Condition", is_abstract=True)
Deadline = Class(name="Deadline")
Participant = Class(name="Participant", is_abstract=True)
Individual = Class(name="Individual")
Role = Class(name="Role")
hasRole = Class(name="hasRole")
Collaboration = Class(name="Collaboration")
Vote = Class(name="Vote")
Interaction = Class(name="Interaction")
Decision = Class(name="Decision")
Metadata = Class(name="Metadata", is_abstract=True)
TagBased = Class(name="TagBased")
Priority = Class(name="Priority")
Tag = Class(name="Tag")
<<github>>Repository = Class(name="<<github>>Repository")
MajorityPolic = Class(name="MajorityPolic")
AbsoluteMajorityPolicy = Class(name="AbsoluteMajorityPolicy")
<<github>>Patch = Class(name="<<github>>Patch")
<<github>>Label = Class(name="<<github>>Label")
<<github>>PullRequest = Class(name="<<github>>PullRequest")
ParticipantExclusion = Class(name="ParticipantExclusion")

# Project class attributes and methods

# Activity class attributes and methods

# Task class attributes and methods

# Scope class attributes and methods
Scope_status: Property = Property(name="status", type=StatusEnum)
Scope.attributes={Scope_status}

# Policy class attributes and methods

# ComposedPolicy class attributes and methods
ComposedPolicy_order: Property = Property(name="order", type=OrderEnum)
ComposedPolicy.attributes={ComposedPolicy_order}

# SinglePolicy class attributes and methods

# LeaderDrivenPolicy class attributes and methods

# VotingPolicy class attributes and methods
VotingPolicy_minVotes: Property = Property(name="minVotes", type=IntegerType)
VotingPolicy_ratio: Property = Property(name="ratio", type=FloatType)
VotingPolicy.attributes={VotingPolicy_ratio, VotingPolicy_minVotes}

# Condition class attributes and methods

# Deadline class attributes and methods
Deadline_offset: Property = Property(name="offset", type=TimeDeltaType)
Deadline_date: Property = Property(name="date", type=DateTimeType)
Deadline.attributes={Deadline_date, Deadline_offset}

# Participant class attributes and methods

# Individual class attributes and methods
Individual_confidence: Property = Property(name="confidence", type=FloatType)
Individual.attributes={Individual_confidence}

# Role class attributes and methods

# hasRole class attributes and methods

# Collaboration class attributes and methods
Collaboration_id: Property = Property(name="id", type=StringType)
Collaboration_rationale: Property = Property(name="rationale", type=StringType)
Collaboration.attributes={Collaboration_rationale, Collaboration_id}

# Vote class attributes and methods
Vote_agreement: Property = Property(name="agreement", type=BooleanType)
Vote_timestamp: Property = Property(name="timestamp", type=FloatType)
Vote_rationale: Property = Property(name="rationale", type=StringType)
Vote.attributes={Vote_rationale, Vote_agreement, Vote_timestamp}

# Interaction class attributes and methods

# Decision class attributes and methods
Decision_accepted: Property = Property(name="accepted", type=BooleanType)
Decision_timestamp: Property = Property(name="timestamp", type=FloatType)
Decision.attributes={Decision_timestamp, Decision_accepted}

# Metadata class attributes and methods

# TagBased class attributes and methods

# Priority class attributes and methods
Priority_value: Property = Property(name="value", type=StringType)
Priority.attributes={Priority_value}

# Tag class attributes and methods
Tag_value: Property = Property(name="value", type=StringType)
Tag.attributes={Tag_value}

# <<github>>Repository class attributes and methods
<<github>>Repository_id: Property = Property(name="id", type=StringType)
<<github>>Repository.attributes={<<github>>Repository_id}

# MajorityPolic class attributes and methods

# AbsoluteMajorityPolicy class attributes and methods

# <<github>>Patch class attributes and methods

# <<github>>Label class attributes and methods
<<github>>Label_name: Property = Property(name="name", type=StringType)
<<github>>Label.attributes={<<github>>Label_name}

# <<github>>PullRequest class attributes and methods
<<github>>PullRequest_has_open_issues: Property = Property(name="has_open_issues", type=BooleanType)
<<github>>PullRequest.attributes={<<github>>PullRequest_has_open_issues}

# ParticipantExclusion class attributes and methods

# Relationships
Individual_hasRole: BinaryAssociation = BinaryAssociation(
    name="Individual_hasRole",
    ends={
        Property(name="individual", type=Individual, multiplicity=Multiplicity(1, 1)),
        Property(name="hasrole_1", type=hasRole, multiplicity=Multiplicity(1, 1))
    }
)
hasRole_Scope: BinaryAssociation = BinaryAssociation(
    name="hasRole_Scope",
    ends={
        Property(name="hasrole_2", type=hasRole, multiplicity=Multiplicity(0, 9999)),
        Property(name="scope", type=Scope, multiplicity=Multiplicity(1, 1))
    }
)
Participant_SinglePolicy: BinaryAssociation = BinaryAssociation(
    name="Participant_SinglePolicy",
    ends={
        Property(name="participants", type=Participant, multiplicity=Multiplicity(1, 9999)),
        Property(name="singlepolicy", type=SinglePolicy, multiplicity=Multiplicity(0, 9999))
    }
)
SinglePolicy_LeaderDrivenPolicy: BinaryAssociation = BinaryAssociation(
    name="SinglePolicy_LeaderDrivenPolicy",
    ends={
        Property(name="default", type=SinglePolicy, multiplicity=Multiplicity(1, 1)),
        Property(name="leaderdrivenpolicy", type=LeaderDrivenPolicy, multiplicity=Multiplicity(0, 9999))
    }
)
<<github>>PullRequest_<<github>>Label: BinaryAssociation = BinaryAssociation(
    name="<<github>>PullRequest_<<github>>Label",
    ends={
        Property(name="<<github>>pullrequest", type=<<github>>PullRequest, multiplicity=Multiplicity(0, 9999)),
        Property(name="labels", type=<<github>>Label, multiplicity=Multiplicity(0, 9999))
    }
)
SinglePolicy_Condition: BinaryAssociation = BinaryAssociation(
    name="SinglePolicy_Condition",
    ends={
        Property(name="singlepolicy_1", type=SinglePolicy, multiplicity=Multiplicity(1, 1)),
        Property(name="conditions", type=Condition, multiplicity=Multiplicity(0, 9999))
    }
)
Policy_ComposedPolicy: BinaryAssociation = BinaryAssociation(
    name="Policy_ComposedPolicy",
    ends={
        Property(name="phases", type=Policy, multiplicity=Multiplicity(1, 9999)),
        Property(name="composedpolicy", type=ComposedPolicy, multiplicity=Multiplicity(1, 1), is_composite=True)
    }
)
Scope_Policy: BinaryAssociation = BinaryAssociation(
    name="Scope_Policy",
    ends={
        Property(name="scopes", type=Scope, multiplicity=Multiplicity(1, 1)),
        Property(name="policy", type=Policy, multiplicity=Multiplicity(0, 1))
    }
)
Individual_Interaction: BinaryAssociation = BinaryAssociation(
    name="Individual_Interaction",
    ends={
        Property(name="individual_1", type=Individual, multiplicity=Multiplicity(0, 9999)),
        Property(name="interaction", type=Interaction, multiplicity=Multiplicity(1, 1))
    }
)
Collaboration_Interaction: BinaryAssociation = BinaryAssociation(
    name="Collaboration_Interaction",
    ends={
        Property(name="collaborations", type=Collaboration, multiplicity=Multiplicity(0, 9999)),
        Property(name="interaction_1", type=Interaction, multiplicity=Multiplicity(1, 1), is_composite=True)
    }
)
Role_hasRole: BinaryAssociation = BinaryAssociation(
    name="Role_hasRole",
    ends={
        Property(name="role", type=Role, multiplicity=Multiplicity(1, 1)),
        Property(name="hasrole", type=hasRole, multiplicity=Multiplicity(0, 9999))
    }
)
Decision_Interaction: BinaryAssociation = BinaryAssociation(
    name="Decision_Interaction",
    ends={
        Property(name="decisions", type=Decision, multiplicity=Multiplicity(0, 9999)),
        Property(name="interaction_2", type=Interaction, multiplicity=Multiplicity(1, 1), is_composite=True)
    }
)
Vote_Individual: BinaryAssociation = BinaryAssociation(
    name="Vote_Individual",
    ends={
        Property(name="votes", type=Vote, multiplicity=Multiplicity(0, 9999)),
        Property(name="individual_2", type=Individual, multiplicity=Multiplicity(1, 1))
    }
)
Activity_Task: BinaryAssociation = BinaryAssociation(
    name="Activity_Task",
    ends={
        Property(name="activity", type=Activity, multiplicity=Multiplicity(0, 1)),
        Property(name="tasks", type=Task, multiplicity=Multiplicity(0, 9999))
    }
)
Vote_Collaboration: BinaryAssociation = BinaryAssociation(
    name="Vote_Collaboration",
    ends={
        Property(name="votes", type=Vote, multiplicity=Multiplicity(0, 9999)),
        Property(name="collaboration", type=Collaboration, multiplicity=Multiplicity(1, 1), is_composite=True)
    }
)
Vote_Decision: BinaryAssociation = BinaryAssociation(
    name="Vote_Decision",
    ends={
        Property(name="votes", type=Vote, multiplicity=Multiplicity(0, 9999)),
        Property(name="part_of", type=Decision, multiplicity=Multiplicity(1, 1))
    }
)
Decision_SinglePolicy: BinaryAssociation = BinaryAssociation(
    name="Decision_SinglePolicy",
    ends={
        Property(name="decision", type=Decision, multiplicity=Multiplicity(0, 9999)),
        Property(name="rule", type=SinglePolicy, multiplicity=Multiplicity(0, 1))
    }
)
Metadata_Collaboration: BinaryAssociation = BinaryAssociation(
    name="Metadata_Collaboration",
    ends={
        Property(name="metadata", type=Metadata, multiplicity=Multiplicity(1, 1)),
        Property(name="collaboration_1", type=Collaboration, multiplicity=Multiplicity(1, 1), is_composite=True)
    }
)
Tag_TagBased: BinaryAssociation = BinaryAssociation(
    name="Tag_TagBased",
    ends={
        Property(name="tags", type=Tag, multiplicity=Multiplicity(0, 9999)),
        Property(name="tagbased", type=TagBased, multiplicity=Multiplicity(1, 1), is_composite=True)
    }
)
Collaboration_Scope: BinaryAssociation = BinaryAssociation(
    name="Collaboration_Scope",
    ends={
        Property(name="collaboration_2", type=Collaboration, multiplicity=Multiplicity(1, 1)),
        Property(name="scope", type=Scope, multiplicity=Multiplicity(0, 1))
    }
)
Project_Activity: BinaryAssociation = BinaryAssociation(
    name="Project_Activity",
    ends={
        Property(name="project", type=Project, multiplicity=Multiplicity(0, 1)),
        Property(name="activities", type=Activity, multiplicity=Multiplicity(0, 9999))
    }
)
ParticipantExclusion_Individual: BinaryAssociation = BinaryAssociation(
    name="ParticipantExclusion_Individual",
    ends={
        Property(name="participantexclusion", type=ParticipantExclusion, multiplicity=Multiplicity(0, 9999)),
        Property(name="participant", type=Individual, multiplicity=Multiplicity(1, 1))
    }
)
<<github>>Patch_<<github>>PullRequest: BinaryAssociation = BinaryAssociation(
    name="<<github>>Patch_<<github>>PullRequest",
    ends={
        Property(name="<<github>>patch", type=<<github>>Patch, multiplicity=Multiplicity(0, 9999)),
        Property(name="pr", type=<<github>>PullRequest, multiplicity=Multiplicity(0, 1))
    }
)

# Generalizations
gen_Activity_Scope = Generalization(general=Scope, specific=Activity)
gen_Project_Scope = Generalization(general=Scope, specific=Project)
gen_Task_Scope = Generalization(general=Scope, specific=Task)
gen_ComposedPolicy_Policy = Generalization(general=Policy, specific=ComposedPolicy)
gen_<<github>>Patch_Task = Generalization(general=Task, specific=<<github>>Patch)
gen_Role_Participant = Generalization(general=Participant, specific=Role)
gen_Individual_Participant = Generalization(general=Participant, specific=Individual)
gen_VotingPolicy_SinglePolicy = Generalization(general=SinglePolicy, specific=VotingPolicy)
gen_LeaderDrivenPolicy_SinglePolicy = Generalization(general=SinglePolicy, specific=LeaderDrivenPolicy)
gen_Deadline_Condition = Generalization(general=Condition, specific=Deadline)
gen_Priority_Metadata = Generalization(general=Metadata, specific=Priority)
gen_SinglePolicy_Policy = Generalization(general=Policy, specific=SinglePolicy)
gen_TagBased_Metadata = Generalization(general=Metadata, specific=TagBased)
gen_MajorityPolic_VotingPolicy = Generalization(general=VotingPolicy, specific=MajorityPolic)
gen_AbsoluteMajorityPolicy_VotingPolicy = Generalization(general=VotingPolicy, specific=AbsoluteMajorityPolicy)
gen_<<github>>Repository_Project = Generalization(general=Project, specific=<<github>>Repository)
gen_ParticipantExclusion_Condition = Generalization(general=Condition, specific=ParticipantExclusion)


# OCL Constraints
constraint_VotingPolicy_0_1: Constraint = Constraint(
    name="constraint_VotingPolicy_0_1",
    context=VotingPolicy,
    expression="context VotingPolicy inv ratioDecimal: self.ratio >= 0 and self.ratio <= 1",
    language="OCL"
)
constraint_Deadline_2_1: Constraint = Constraint(
    name="constraint_Deadline_2_1",
    context=Deadline,
    expression="context Deadline inv AtLeastOneNonNull:self.offset <> null or self.date <> null",
    language="OCL"
)
constraint_Individual_4_1: Constraint = Constraint(
    name="constraint_Individual_4_1",
    context=Individual,
    expression="context Individual inv confidenceDecimal: self.confidence>= 0 and self.confidenc<= 1",
    language="OCL"
)

# Domain Model
domain_model = DomainModel(
    name="UMLClassDiagram",
    types={Project, Activity, Task, Scope, Policy, ComposedPolicy, SinglePolicy, LeaderDrivenPolicy, VotingPolicy, Condition, Deadline, Participant, Individual, Role, hasRole, Collaboration, Vote, Interaction, Decision, Metadata, TagBased, Priority, Tag, <<github>>Repository, MajorityPolic, AbsoluteMajorityPolicy, <<github>>Patch, <<github>>Label, <<github>>PullRequest, ParticipantExclusion, StatusEnum, OrderEnum},
    associations={Individual_hasRole, hasRole_Scope, Participant_SinglePolicy, SinglePolicy_LeaderDrivenPolicy, <<github>>PullRequest_<<github>>Label, SinglePolicy_Condition, Policy_ComposedPolicy, Scope_Policy, Individual_Interaction, Collaboration_Interaction, Role_hasRole, Decision_Interaction, Vote_Individual, Activity_Task, Vote_Collaboration, Vote_Decision, Decision_SinglePolicy, Metadata_Collaboration, Tag_TagBased, Collaboration_Scope, Project_Activity, ParticipantExclusion_Individual, <<github>>Patch_<<github>>PullRequest},
    constraints={constraint_VotingPolicy_0_1, constraint_Deadline_2_1, constraint_Individual_4_1},
    generalizations={gen_Activity_Scope, gen_Project_Scope, gen_Task_Scope, gen_ComposedPolicy_Policy, gen_<<github>>Patch_Task, gen_Role_Participant, gen_Individual_Participant, gen_VotingPolicy_SinglePolicy, gen_LeaderDrivenPolicy_SinglePolicy, gen_Deadline_Condition, gen_Priority_Metadata, gen_SinglePolicy_Policy, gen_TagBased_Metadata, gen_MajorityPolic_VotingPolicy, gen_AbsoluteMajorityPolicy_VotingPolicy, gen_<<github>>Repository_Project, gen_ParticipantExclusion_Condition}
)
