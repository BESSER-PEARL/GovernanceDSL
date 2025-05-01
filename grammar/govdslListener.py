# Generated from govdsl.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .govdslParser import govdslParser
else:
    from govdslParser import govdslParser

# This class defines a complete listener for a parse tree produced by govdslParser.
class govdslListener(ParseTreeListener):

    # Enter a parse tree produced by govdslParser#governance.
    def enterGovernance(self, ctx:govdslParser.GovernanceContext):
        print(f"enterGovernance: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#governance.
    def exitGovernance(self, ctx:govdslParser.GovernanceContext):
        print(f"exitGovernance: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#policy.
    def enterPolicy(self, ctx:govdslParser.PolicyContext):
        print(f"enterPolicy: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#policy.
    def exitPolicy(self, ctx:govdslParser.PolicyContext):
        print(f"exitPolicy: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#topLevelSinglePolicy.
    def enterTopLevelSinglePolicy(self, ctx:govdslParser.TopLevelSinglePolicyContext):
        print(f"enterTopLevelSinglePolicy: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#topLevelSinglePolicy.
    def exitTopLevelSinglePolicy(self, ctx:govdslParser.TopLevelSinglePolicyContext):
        print(f"exitTopLevelSinglePolicy: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#topLevelComposedPolicy.
    def enterTopLevelComposedPolicy(self, ctx:govdslParser.TopLevelComposedPolicyContext):
        print(f"enterTopLevelComposedPolicy: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#topLevelComposedPolicy.
    def exitTopLevelComposedPolicy(self, ctx:govdslParser.TopLevelComposedPolicyContext):
        print(f"exitTopLevelComposedPolicy: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#nestedSinglePolicy.
    def enterNestedSinglePolicy(self, ctx:govdslParser.NestedSinglePolicyContext):
        print(f"enterNestedSinglePolicy: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#nestedSinglePolicy.
    def exitNestedSinglePolicy(self, ctx:govdslParser.NestedSinglePolicyContext):
        print(f"exitNestedSinglePolicy: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#nestedComposedPolicy.
    def enterNestedComposedPolicy(self, ctx:govdslParser.NestedComposedPolicyContext):
        print(f"enterNestedComposedPolicy: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#nestedComposedPolicy.
    def exitNestedComposedPolicy(self, ctx:govdslParser.NestedComposedPolicyContext):
        print(f"exitNestedComposedPolicy: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#policyType.
    def enterPolicyType(self, ctx:govdslParser.PolicyTypeContext):
        print(f"enterPolicyType: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#policyType.
    def exitPolicyType(self, ctx:govdslParser.PolicyTypeContext):
        print(f"exitPolicyType: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#scopes.
    def enterScopes(self, ctx:govdslParser.ScopesContext):
        print(f"enterScopes: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#scopes.
    def exitScopes(self, ctx:govdslParser.ScopesContext):
        print(f"exitScopes: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#scope.
    def enterScope(self, ctx:govdslParser.ScopeContext):
        print(f"enterScope: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#scope.
    def exitScope(self, ctx:govdslParser.ScopeContext):
        print(f"exitScope: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#project.
    def enterProject(self, ctx:govdslParser.ProjectContext):
        print(f"enterProject: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#project.
    def exitProject(self, ctx:govdslParser.ProjectContext):
        print(f"exitProject: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#platform.
    def enterPlatform(self, ctx:govdslParser.PlatformContext):
        print(f"enterPlatform: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#platform.
    def exitPlatform(self, ctx:govdslParser.PlatformContext):
        print(f"exitPlatform: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#repoID.
    def enterRepoID(self, ctx:govdslParser.RepoIDContext):
        print(f"enterRepoID: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#repoID.
    def exitRepoID(self, ctx:govdslParser.RepoIDContext):
        print(f"exitRepoID: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#activity.
    def enterActivity(self, ctx:govdslParser.ActivityContext):
        print(f"enterActivity: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#activity.
    def exitActivity(self, ctx:govdslParser.ActivityContext):
        print(f"exitActivity: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#task.
    def enterTask(self, ctx:govdslParser.TaskContext):
        print(f"enterTask: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#task.
    def exitTask(self, ctx:govdslParser.TaskContext):
        print(f"exitTask: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#taskType.
    def enterTaskType(self, ctx:govdslParser.TaskTypeContext):
        print(f"enterTaskType: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#taskType.
    def exitTaskType(self, ctx:govdslParser.TaskTypeContext):
        print(f"exitTaskType: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#taskContent.
    def enterTaskContent(self, ctx:govdslParser.TaskContentContext):
        print(f"enterTaskContent: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#taskContent.
    def exitTaskContent(self, ctx:govdslParser.TaskContentContext):
        print(f"exitTaskContent: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#actionWithLabels.
    def enterActionWithLabels(self, ctx:govdslParser.ActionWithLabelsContext):
        print(f"enterActionWithLabels: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#actionWithLabels.
    def exitActionWithLabels(self, ctx:govdslParser.ActionWithLabelsContext):
        print(f"exitActionWithLabels: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#status.
    def enterStatus(self, ctx:govdslParser.StatusContext):
        print(f"enterStatus: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#status.
    def exitStatus(self, ctx:govdslParser.StatusContext):
        print(f"exitStatus: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#statusEnum.
    def enterStatusEnum(self, ctx:govdslParser.StatusEnumContext):
        print(f"enterStatusEnum: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#statusEnum.
    def exitStatusEnum(self, ctx:govdslParser.StatusEnumContext):
        print(f"exitStatusEnum: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#action.
    def enterAction(self, ctx:govdslParser.ActionContext):
        print(f"enterAction: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#action.
    def exitAction(self, ctx:govdslParser.ActionContext):
        print(f"exitAction: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#actionEnum.
    def enterActionEnum(self, ctx:govdslParser.ActionEnumContext):
        print(f"enterActionEnum: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#actionEnum.
    def exitActionEnum(self, ctx:govdslParser.ActionEnumContext):
        print(f"exitActionEnum: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#labels.
    def enterLabels(self, ctx:govdslParser.LabelsContext):
        print(f"enterLabels: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#labels.
    def exitLabels(self, ctx:govdslParser.LabelsContext):
        print(f"exitLabels: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#participants.
    def enterParticipants(self, ctx:govdslParser.ParticipantsContext):
        print(f"enterParticipants: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#participants.
    def exitParticipants(self, ctx:govdslParser.ParticipantsContext):
        print(f"exitParticipants: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#roles.
    def enterRoles(self, ctx:govdslParser.RolesContext):
        print(f"enterRoles: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#roles.
    def exitRoles(self, ctx:govdslParser.RolesContext):
        print(f"exitRoles: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#participantID.
    def enterParticipantID(self, ctx:govdslParser.ParticipantIDContext):
        print(f"enterParticipantID: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#participantID.
    def exitParticipantID(self, ctx:govdslParser.ParticipantIDContext):
        print(f"exitParticipantID: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#individuals.
    def enterIndividuals(self, ctx:govdslParser.IndividualsContext):
        print(f"enterIndividuals: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#individuals.
    def exitIndividuals(self, ctx:govdslParser.IndividualsContext):
        print(f"exitIndividuals: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#individualEntry.
    def enterIndividualEntry(self, ctx:govdslParser.IndividualEntryContext):
        print(f"enterIndividualEntry: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#individualEntry.
    def exitIndividualEntry(self, ctx:govdslParser.IndividualEntryContext):
        print(f"exitIndividualEntry: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#individual.
    def enterIndividual(self, ctx:govdslParser.IndividualContext):
        print(f"enterIndividual: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#individual.
    def exitIndividual(self, ctx:govdslParser.IndividualContext):
        print(f"exitIndividual: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#hasRole.
    def enterHasRole(self, ctx:govdslParser.HasRoleContext):
        print(f"enterHasRole: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#hasRole.
    def exitHasRole(self, ctx:govdslParser.HasRoleContext):
        print(f"exitHasRole: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#voteValue.
    def enterVoteValue(self, ctx:govdslParser.VoteValueContext):
        print(f"enterVoteValue: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#voteValue.
    def exitVoteValue(self, ctx:govdslParser.VoteValueContext):
        print(f"exitVoteValue: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#agent.
    def enterAgent(self, ctx:govdslParser.AgentContext):
        print(f"enterAgent: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#agent.
    def exitAgent(self, ctx:govdslParser.AgentContext):
        print(f"exitAgent: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#confidence.
    def enterConfidence(self, ctx:govdslParser.ConfidenceContext):
        print(f"enterConfidence: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#confidence.
    def exitConfidence(self, ctx:govdslParser.ConfidenceContext):
        print(f"exitConfidence: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#conditions.
    def enterConditions(self, ctx:govdslParser.ConditionsContext):
        print(f"enterConditions: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#conditions.
    def exitConditions(self, ctx:govdslParser.ConditionsContext):
        print(f"exitConditions: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#deadline.
    def enterDeadline(self, ctx:govdslParser.DeadlineContext):
        print(f"enterDeadline: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#deadline.
    def exitDeadline(self, ctx:govdslParser.DeadlineContext):
        print(f"exitDeadline: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#offset.
    def enterOffset(self, ctx:govdslParser.OffsetContext):
        print(f"enterOffset: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#offset.
    def exitOffset(self, ctx:govdslParser.OffsetContext):
        print(f"exitOffset: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#deadlineID.
    def enterDeadlineID(self, ctx:govdslParser.DeadlineIDContext):
        print(f"enterDeadlineID: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#deadlineID.
    def exitDeadlineID(self, ctx:govdslParser.DeadlineIDContext):
        print(f"exitDeadlineID: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#timeUnit.
    def enterTimeUnit(self, ctx:govdslParser.TimeUnitContext):
        print(f"enterTimeUnit: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#timeUnit.
    def exitTimeUnit(self, ctx:govdslParser.TimeUnitContext):
        print(f"exitTimeUnit: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#date.
    def enterDate(self, ctx:govdslParser.DateContext):
        print(f"enterDate: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#date.
    def exitDate(self, ctx:govdslParser.DateContext):
        print(f"exitDate: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#participantExclusion.
    def enterParticipantExclusion(self, ctx:govdslParser.ParticipantExclusionContext):
        print(f"enterParticipantExclusion: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#participantExclusion.
    def exitParticipantExclusion(self, ctx:govdslParser.ParticipantExclusionContext):
        print(f"exitParticipantExclusion: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#minParticipant.
    def enterMinParticipant(self, ctx:govdslParser.MinParticipantContext):
        print(f"enterMinParticipant: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#minParticipant.
    def exitMinParticipant(self, ctx:govdslParser.MinParticipantContext):
        print(f"exitMinParticipant: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#vetoRight.
    def enterVetoRight(self, ctx:govdslParser.VetoRightContext):
        print(f"enterVetoRight: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#vetoRight.
    def exitVetoRight(self, ctx:govdslParser.VetoRightContext):
        print(f"exitVetoRight: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#passedTests.
    def enterPassedTests(self, ctx:govdslParser.PassedTestsContext):
        print(f"enterPassedTests: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#passedTests.
    def exitPassedTests(self, ctx:govdslParser.PassedTestsContext):
        print(f"exitPassedTests: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#parameters.
    def enterParameters(self, ctx:govdslParser.ParametersContext):
        print(f"enterParameters: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#parameters.
    def exitParameters(self, ctx:govdslParser.ParametersContext):
        print(f"exitParameters: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#votParams.
    def enterVotParams(self, ctx:govdslParser.VotParamsContext):
        print(f"enterVotParams: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#votParams.
    def exitVotParams(self, ctx:govdslParser.VotParamsContext):
        print(f"exitVotParams: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#ratio.
    def enterRatio(self, ctx:govdslParser.RatioContext):
        print(f"enterRatio: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#ratio.
    def exitRatio(self, ctx:govdslParser.RatioContext):
        print(f"exitRatio: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#default.
    def enterDefault(self, ctx:govdslParser.DefaultContext):
        print(f"enterDefault: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#default.
    def exitDefault(self, ctx:govdslParser.DefaultContext):
        print(f"exitDefault: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#order.
    def enterOrder(self, ctx:govdslParser.OrderContext):
        print(f"enterOrder: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#order.
    def exitOrder(self, ctx:govdslParser.OrderContext):
        print(f"exitOrder: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#orderType.
    def enterOrderType(self, ctx:govdslParser.OrderTypeContext):
        print(f"enterOrderType: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#orderType.
    def exitOrderType(self, ctx:govdslParser.OrderTypeContext):
        print(f"exitOrderType: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#orderTypeValue.
    def enterOrderTypeValue(self, ctx:govdslParser.OrderTypeValueContext):
        print(f"enterOrderTypeValue: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#orderTypeValue.
    def exitOrderTypeValue(self, ctx:govdslParser.OrderTypeValueContext):
        print(f"exitOrderTypeValue: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#orderMode.
    def enterOrderMode(self, ctx:govdslParser.OrderModeContext):
        print(f"enterOrderMode: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#orderMode.
    def exitOrderMode(self, ctx:govdslParser.OrderModeContext):
        print(f"exitOrderMode: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#carryOver.
    def enterCarryOver(self, ctx:govdslParser.CarryOverContext):
        print(f"enterCarryOver: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#carryOver.
    def exitCarryOver(self, ctx:govdslParser.CarryOverContext):
        print(f"exitCarryOver: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#booleanValue.
    def enterBooleanValue(self, ctx:govdslParser.BooleanValueContext):
        print(f"enterBooleanValue: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#booleanValue.
    def exitBooleanValue(self, ctx:govdslParser.BooleanValueContext):
        print(f"exitBooleanValue: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#phases.
    def enterPhases(self, ctx:govdslParser.PhasesContext):
        print(f"enterPhases: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#phases.
    def exitPhases(self, ctx:govdslParser.PhasesContext):
        print(f"exitPhases: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#nestedPolicy.
    def enterNestedPolicy(self, ctx:govdslParser.NestedPolicyContext):
        print(f"enterNestedPolicy: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#nestedPolicy.
    def exitNestedPolicy(self, ctx:govdslParser.NestedPolicyContext):
        print(f"exitNestedPolicy: {ctx.getText()}")



del govdslParser