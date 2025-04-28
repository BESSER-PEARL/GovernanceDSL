# Generated from govdsl.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .govdslParser import govdslParser
else:
    from govdslParser import govdslParser

# This class defines a complete listener for a parse tree produced by govdslParser.
class govdslListener(ParseTreeListener):

    # Enter a parse tree produced by govdslParser#policy.
    def enterPolicy(self, ctx:govdslParser.PolicyContext):
        print(f"Enter policy: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#policy.
    def exitPolicy(self, ctx:govdslParser.PolicyContext):
        print(f"Exit policy: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#topLevelSinglePolicy.
    def enterTopLevelSinglePolicy(self, ctx:govdslParser.TopLevelSinglePolicyContext):
        print(f"Enter topLevelSinglePolicy: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#topLevelSinglePolicy.
    def exitTopLevelSinglePolicy(self, ctx:govdslParser.TopLevelSinglePolicyContext):
        print(f"Exit topLevelSinglePolicy: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#topLevelComposedPolicy.
    def enterTopLevelComposedPolicy(self, ctx:govdslParser.TopLevelComposedPolicyContext):
        print(f"Enter topLevelComposedPolicy: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#topLevelComposedPolicy.
    def exitTopLevelComposedPolicy(self, ctx:govdslParser.TopLevelComposedPolicyContext):
        print(f"Exit topLevelComposedPolicy: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#nestedSinglePolicy.
    def enterNestedSinglePolicy(self, ctx:govdslParser.NestedSinglePolicyContext):
        print(f"Enter nestedSinglePolicy: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#nestedSinglePolicy.
    def exitNestedSinglePolicy(self, ctx:govdslParser.NestedSinglePolicyContext):
        print(f"Exit nestedSinglePolicy: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#nestedComposedPolicy.
    def enterNestedComposedPolicy(self, ctx:govdslParser.NestedComposedPolicyContext):
        print(f"Enter nestedComposedPolicy: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#nestedComposedPolicy.
    def exitNestedComposedPolicy(self, ctx:govdslParser.NestedComposedPolicyContext):
        print(f"Exit nestedComposedPolicy: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#policyType.
    def enterPolicyType(self, ctx:govdslParser.PolicyTypeContext):
        print(f"Enter policyType: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#policyType.
    def exitPolicyType(self, ctx:govdslParser.PolicyTypeContext):
        print(f"Exit policyType: {ctx.getText()}")


    # Enter a parse tree produced by govdslParser#scope.
    def enterScope(self, ctx:govdslParser.ScopeContext):
        print(f"Enter scope: {ctx.getText()}")

    # Exit a parse tree produced by govdslParser#scope.
    def exitScope(self, ctx:govdslParser.ScopeContext):
        print(f"Exit scope: {ctx.getText()}")

    def enterProject(self, ctx:govdslParser.ProjectContext):
        print(f"Enter project: {ctx.getText()}")

    def exitProject(self, ctx:govdslParser.ProjectContext):
        print(f"Exit project: {ctx.getText()}")

    def enterPlatform(self, ctx:govdslParser.PlatformContext):
        print(f"Enter platform: {ctx.getText()}")

    def exitPlatform(self, ctx:govdslParser.PlatformContext):
        print(f"Exit platform: {ctx.getText()}")

    def enterRepoID(self, ctx:govdslParser.RepoIDContext):
        print(f"Enter repoID: {ctx.getText()}")

    def exitRepoID(self, ctx:govdslParser.RepoIDContext):
        print(f"Exit repoID: {ctx.getText()}")

    def enterActivity(self, ctx:govdslParser.ActivityContext):
        print(f"Enter activity: {ctx.getText()}")

    def exitActivity(self, ctx:govdslParser.ActivityContext):
        print(f"Exit activity: {ctx.getText()}")

    def enterTask(self, ctx:govdslParser.TaskContext):
        print(f"Enter task: {ctx.getText()}")

    def exitTask(self, ctx:govdslParser.TaskContext):
        print(f"Exit task: {ctx.getText()}")

    def enterTaskType(self, ctx:govdslParser.TaskTypeContext):
        print(f"Enter taskType: {ctx.getText()}")

    def exitTaskType(self, ctx:govdslParser.TaskTypeContext):
        print(f"Exit taskType: {ctx.getText()}")

    def enterTaskContent(self, ctx:govdslParser.TaskContentContext):
        print(f"Enter taskContent: {ctx.getText()}")

    def exitTaskContent(self, ctx:govdslParser.TaskContentContext):
        print(f"Exit taskContent: {ctx.getText()}")

    def enterActionWithLabels(self, ctx:govdslParser.ActionWithLabelsContext):
        print(f"Enter actionWithLabels: {ctx.getText()}")

    def exitActionWithLabels(self, ctx:govdslParser.ActionWithLabelsContext):
        print(f"Exit actionWithLabels: {ctx.getText()}")

    def enterStatus(self, ctx:govdslParser.StatusContext):
        print(f"Enter status: {ctx.getText()}")

    def exitStatus(self, ctx:govdslParser.StatusContext):
        print(f"Exit status: {ctx.getText()}")

    def enterStatusEnum(self, ctx:govdslParser.StatusEnumContext):
        print(f"Enter statusEnum: {ctx.getText()}")

    def exitStatusEnum(self, ctx:govdslParser.StatusEnumContext):
        print(f"Exit statusEnum: {ctx.getText()}")

    def enterAction(self, ctx:govdslParser.ActionContext):
        print(f"Enter action: {ctx.getText()}")

    def exitAction(self, ctx:govdslParser.ActionContext):
        print(f"Exit action: {ctx.getText()}")

    def enterActionEnum(self, ctx:govdslParser.ActionEnumContext):
        print(f"Enter actionEnum: {ctx.getText()}")

    def exitActionEnum(self, ctx:govdslParser.ActionEnumContext):
        print(f"Exit actionEnum: {ctx.getText()}")

    def enterLabels(self, ctx:govdslParser.LabelsContext):
        print(f"Enter labels: {ctx.getText()}")

    def exitLabels(self, ctx:govdslParser.LabelsContext):
        print(f"Exit labels: {ctx.getText()}")

    def enterParticipants(self, ctx:govdslParser.ParticipantsContext):
        print(f"Enter participants: {ctx.getText()}")

    def exitParticipants(self, ctx:govdslParser.ParticipantsContext):
        print(f"Exit participants: {ctx.getText()}")

    def enterRoles(self, ctx:govdslParser.RolesContext):
        print(f"Enter roles: {ctx.getText()}")

    def exitRoles(self, ctx:govdslParser.RolesContext):
        print(f"Exit roles: {ctx.getText()}")

    def enterParticipantID(self, ctx:govdslParser.ParticipantIDContext):
        print(f"Enter participantID: {ctx.getText()}")

    def exitParticipantID(self, ctx:govdslParser.ParticipantIDContext):
        print(f"Exit participantID: {ctx.getText()}")

    def enterIndividuals(self, ctx:govdslParser.IndividualsContext):
        print(f"Enter individuals: {ctx.getText()}")

    def exitIndividuals(self, ctx:govdslParser.IndividualsContext):
        print(f"Exit individuals: {ctx.getText()}")

    def enterIndividualEntry(self, ctx:govdslParser.IndividualEntryContext):
        print(f"Enter individualEntry: {ctx.getText()}")

    def exitIndividualEntry(self, ctx:govdslParser.IndividualEntryContext):
        print(f"Exit individualEntry: {ctx.getText()}")

    def enterIndividual(self, ctx:govdslParser.IndividualContext):
        print(f"Enter individual: {ctx.getText()}")

    def exitIndividual(self, ctx:govdslParser.IndividualContext):
        print(f"Exit individual: {ctx.getText()}")

    def enterHasRole(self, ctx:govdslParser.HasRoleContext):
        print(f"Enter hasRole: {ctx.getText()}")

    def exitHasRole(self, ctx:govdslParser.HasRoleContext):
        print(f"Exit hasRole: {ctx.getText()}")

    def enterVoteValue(self, ctx:govdslParser.VoteValueContext):
        print(f"Enter voteValue: {ctx.getText()}")

    def exitVoteValue(self, ctx:govdslParser.VoteValueContext):
        print(f"Exit voteValue: {ctx.getText()}")

    def enterAgent(self, ctx:govdslParser.AgentContext):
        print(f"Enter agent: {ctx.getText()}")

    def exitAgent(self, ctx:govdslParser.AgentContext):
        print(f"Exit agent: {ctx.getText()}")

    def enterConfidence(self, ctx:govdslParser.ConfidenceContext):
        print(f"Enter confidence: {ctx.getText()}")

    def exitConfidence(self, ctx:govdslParser.ConfidenceContext):
        print(f"Exit confidence: {ctx.getText()}")

    def enterConditions(self, ctx:govdslParser.ConditionsContext):
        print(f"Enter conditions: {ctx.getText()}")

    def exitConditions(self, ctx:govdslParser.ConditionsContext):
        print(f"Exit conditions: {ctx.getText()}")

    def enterDeadline(self, ctx:govdslParser.DeadlineContext):
        print(f"Enter deadline: {ctx.getText()}")

    def exitDeadline(self, ctx:govdslParser.DeadlineContext):
        print(f"Exit deadline: {ctx.getText()}")

    def enterOffset(self, ctx:govdslParser.OffsetContext):
        print(f"Enter offset: {ctx.getText()}")

    def exitOffset(self, ctx:govdslParser.OffsetContext):
        print(f"Exit offset: {ctx.getText()}")

    def enterDeadlineID(self, ctx:govdslParser.DeadlineIDContext):
        print(f"Enter deadlineID: {ctx.getText()}")

    def exitDeadlineID(self, ctx:govdslParser.DeadlineIDContext):
        print(f"Exit deadlineID: {ctx.getText()}")

    def enterTimeUnit(self, ctx:govdslParser.TimeUnitContext):
        print(f"Enter timeUnit: {ctx.getText()}")

    def exitTimeUnit(self, ctx:govdslParser.TimeUnitContext):
        print(f"Exit timeUnit: {ctx.getText()}")

    def enterDate(self, ctx:govdslParser.DateContext):
        print(f"Enter date: {ctx.getText()}")

    def exitDate(self, ctx:govdslParser.DateContext):
        print(f"Exit date: {ctx.getText()}")

    def enterParticipantExclusion(self, ctx:govdslParser.ParticipantExclusionContext):
        print(f"Enter participantExclusion: {ctx.getText()}")

    def exitParticipantExclusion(self, ctx:govdslParser.ParticipantExclusionContext):
        print(f"Exit participantExclusion: {ctx.getText()}")

    def enterMinParticipant(self, ctx:govdslParser.MinParticipantContext):
        print(f"Enter minParticipant: {ctx.getText()}")

    def exitMinParticipant(self, ctx:govdslParser.MinParticipantContext):
        print(f"Exit minParticipant: {ctx.getText()}")

    def enterVetoRight(self, ctx:govdslParser.VetoRightContext):
        print(f"Enter vetoRight: {ctx.getText()}")

    def exitVetoRight(self, ctx:govdslParser.VetoRightContext):
        print(f"Exit vetoRight: {ctx.getText()}")

    def enterPassedTests(self, ctx:govdslParser.PassedTestsContext):
        print(f"Enter passedTests: {ctx.getText()}")

    def exitPassedTests(self, ctx:govdslParser.PassedTestsContext):
        print(f"Exit passedTests: {ctx.getText()}")

    def enterParameters(self, ctx:govdslParser.ParametersContext):
        print(f"Enter parameters: {ctx.getText()}")

    def exitParameters(self, ctx:govdslParser.ParametersContext):
        print(f"Exit parameters: {ctx.getText()}")

    def enterVotParams(self, ctx:govdslParser.VotParamsContext):
        print(f"Enter votParams: {ctx.getText()}")

    def exitVotParams(self, ctx:govdslParser.VotParamsContext):
        print(f"Exit votParams: {ctx.getText()}")

    def enterRatio(self, ctx:govdslParser.RatioContext):
        print(f"Enter ratio: {ctx.getText()}")

    def exitRatio(self, ctx:govdslParser.RatioContext):
        print(f"Exit ratio: {ctx.getText()}")

    def enterDefault(self, ctx:govdslParser.DefaultContext):
        print(f"Enter default: {ctx.getText()}")

    def exitDefault(self, ctx:govdslParser.DefaultContext):
        print(f"Exit default: {ctx.getText()}")

    def enterOrder(self, ctx:govdslParser.OrderContext):
        print(f"Enter order: {ctx.getText()}")

    def exitOrder(self, ctx:govdslParser.OrderContext):
        print(f"Exit order: {ctx.getText()}")

    def enterOrderType(self, ctx:govdslParser.OrderTypeContext):
        print(f"Enter orderType: {ctx.getText()}")

    def exitOrderType(self, ctx:govdslParser.OrderTypeContext):
        print(f"Exit orderType: {ctx.getText()}")

    def enterOrderTypeValue(self, ctx:govdslParser.OrderTypeValueContext):
        print(f"Enter orderTypeValue: {ctx.getText()}")

    def exitOrderTypeValue(self, ctx:govdslParser.OrderTypeValueContext):
        print(f"Exit orderTypeValue: {ctx.getText()}")

    def enterOrderMode(self, ctx:govdslParser.OrderModeContext):
        print(f"Enter orderMode: {ctx.getText()}")

    def exitOrderMode(self, ctx:govdslParser.OrderModeContext):
        print(f"Exit orderMode: {ctx.getText()}")

    def enterCarryOver(self, ctx:govdslParser.CarryOverContext):
        print(f"Enter carryOver: {ctx.getText()}")

    def exitCarryOver(self, ctx:govdslParser.CarryOverContext):
        print(f"Exit carryOver: {ctx.getText()}")

    def enterBooleanValue(self, ctx:govdslParser.BooleanValueContext):
        print(f"Enter booleanValue: {ctx.getText()}")

    def exitBooleanValue(self, ctx:govdslParser.BooleanValueContext):
        print(f"Exit booleanValue: {ctx.getText()}")

    def enterPhases(self, ctx:govdslParser.PhasesContext):
        print(f"Enter phases: {ctx.getText()}")

    def exitPhases(self, ctx:govdslParser.PhasesContext):
        print(f"Exit phases: {ctx.getText()}")

    def enterNestedPolicy(self, ctx:govdslParser.NestedPolicyContext):
        print(f"Enter nestedPolicy: {ctx.getText()}")

    def exitNestedPolicy(self, ctx:govdslParser.NestedPolicyContext):
        print(f"Exit nestedPolicy: {ctx.getText()}")


del govdslParser