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
        pass

    # Exit a parse tree produced by govdslParser#governance.
    def exitGovernance(self, ctx:govdslParser.GovernanceContext):
        pass


    # Enter a parse tree produced by govdslParser#policy.
    def enterPolicy(self, ctx:govdslParser.PolicyContext):
        pass

    # Exit a parse tree produced by govdslParser#policy.
    def exitPolicy(self, ctx:govdslParser.PolicyContext):
        pass


    # Enter a parse tree produced by govdslParser#topLevelSinglePolicy.
    def enterTopLevelSinglePolicy(self, ctx:govdslParser.TopLevelSinglePolicyContext):
        pass

    # Exit a parse tree produced by govdslParser#topLevelSinglePolicy.
    def exitTopLevelSinglePolicy(self, ctx:govdslParser.TopLevelSinglePolicyContext):
        pass


    # Enter a parse tree produced by govdslParser#topLevelComposedPolicy.
    def enterTopLevelComposedPolicy(self, ctx:govdslParser.TopLevelComposedPolicyContext):
        pass

    # Exit a parse tree produced by govdslParser#topLevelComposedPolicy.
    def exitTopLevelComposedPolicy(self, ctx:govdslParser.TopLevelComposedPolicyContext):
        pass


    # Enter a parse tree produced by govdslParser#nestedSinglePolicy.
    def enterNestedSinglePolicy(self, ctx:govdslParser.NestedSinglePolicyContext):
        pass

    # Exit a parse tree produced by govdslParser#nestedSinglePolicy.
    def exitNestedSinglePolicy(self, ctx:govdslParser.NestedSinglePolicyContext):
        pass


    # Enter a parse tree produced by govdslParser#nestedComposedPolicy.
    def enterNestedComposedPolicy(self, ctx:govdslParser.NestedComposedPolicyContext):
        pass

    # Exit a parse tree produced by govdslParser#nestedComposedPolicy.
    def exitNestedComposedPolicy(self, ctx:govdslParser.NestedComposedPolicyContext):
        pass


    # Enter a parse tree produced by govdslParser#policyType.
    def enterPolicyType(self, ctx:govdslParser.PolicyTypeContext):
        pass

    # Exit a parse tree produced by govdslParser#policyType.
    def exitPolicyType(self, ctx:govdslParser.PolicyTypeContext):
        pass


    # Enter a parse tree produced by govdslParser#scopes.
    def enterScopes(self, ctx:govdslParser.ScopesContext):
        pass

    # Exit a parse tree produced by govdslParser#scopes.
    def exitScopes(self, ctx:govdslParser.ScopesContext):
        pass


    # Enter a parse tree produced by govdslParser#scope.
    def enterScope(self, ctx:govdslParser.ScopeContext):
        pass

    # Exit a parse tree produced by govdslParser#scope.
    def exitScope(self, ctx:govdslParser.ScopeContext):
        pass


    # Enter a parse tree produced by govdslParser#projects.
    def enterProjects(self, ctx:govdslParser.ProjectsContext):
        pass

    # Exit a parse tree produced by govdslParser#projects.
    def exitProjects(self, ctx:govdslParser.ProjectsContext):
        pass


    # Enter a parse tree produced by govdslParser#project.
    def enterProject(self, ctx:govdslParser.ProjectContext):
        pass

    # Exit a parse tree produced by govdslParser#project.
    def exitProject(self, ctx:govdslParser.ProjectContext):
        pass


    # Enter a parse tree produced by govdslParser#platform.
    def enterPlatform(self, ctx:govdslParser.PlatformContext):
        pass

    # Exit a parse tree produced by govdslParser#platform.
    def exitPlatform(self, ctx:govdslParser.PlatformContext):
        pass


    # Enter a parse tree produced by govdslParser#repoID.
    def enterRepoID(self, ctx:govdslParser.RepoIDContext):
        pass

    # Exit a parse tree produced by govdslParser#repoID.
    def exitRepoID(self, ctx:govdslParser.RepoIDContext):
        pass


    # Enter a parse tree produced by govdslParser#activities.
    def enterActivities(self, ctx:govdslParser.ActivitiesContext):
        pass

    # Exit a parse tree produced by govdslParser#activities.
    def exitActivities(self, ctx:govdslParser.ActivitiesContext):
        pass


    # Enter a parse tree produced by govdslParser#activity.
    def enterActivity(self, ctx:govdslParser.ActivityContext):
        pass

    # Exit a parse tree produced by govdslParser#activity.
    def exitActivity(self, ctx:govdslParser.ActivityContext):
        pass


    # Enter a parse tree produced by govdslParser#tasks.
    def enterTasks(self, ctx:govdslParser.TasksContext):
        pass

    # Exit a parse tree produced by govdslParser#tasks.
    def exitTasks(self, ctx:govdslParser.TasksContext):
        pass


    # Enter a parse tree produced by govdslParser#task.
    def enterTask(self, ctx:govdslParser.TaskContext):
        pass

    # Exit a parse tree produced by govdslParser#task.
    def exitTask(self, ctx:govdslParser.TaskContext):
        pass


    # Enter a parse tree produced by govdslParser#taskType.
    def enterTaskType(self, ctx:govdslParser.TaskTypeContext):
        pass

    # Exit a parse tree produced by govdslParser#taskType.
    def exitTaskType(self, ctx:govdslParser.TaskTypeContext):
        pass


    # Enter a parse tree produced by govdslParser#taskContent.
    def enterTaskContent(self, ctx:govdslParser.TaskContentContext):
        pass

    # Exit a parse tree produced by govdslParser#taskContent.
    def exitTaskContent(self, ctx:govdslParser.TaskContentContext):
        pass


    # Enter a parse tree produced by govdslParser#actionWithLabels.
    def enterActionWithLabels(self, ctx:govdslParser.ActionWithLabelsContext):
        pass

    # Exit a parse tree produced by govdslParser#actionWithLabels.
    def exitActionWithLabels(self, ctx:govdslParser.ActionWithLabelsContext):
        pass


    # Enter a parse tree produced by govdslParser#status.
    def enterStatus(self, ctx:govdslParser.StatusContext):
        pass

    # Exit a parse tree produced by govdslParser#status.
    def exitStatus(self, ctx:govdslParser.StatusContext):
        pass


    # Enter a parse tree produced by govdslParser#statusEnum.
    def enterStatusEnum(self, ctx:govdslParser.StatusEnumContext):
        pass

    # Exit a parse tree produced by govdslParser#statusEnum.
    def exitStatusEnum(self, ctx:govdslParser.StatusEnumContext):
        pass


    # Enter a parse tree produced by govdslParser#action.
    def enterAction(self, ctx:govdslParser.ActionContext):
        pass

    # Exit a parse tree produced by govdslParser#action.
    def exitAction(self, ctx:govdslParser.ActionContext):
        pass


    # Enter a parse tree produced by govdslParser#actionEnum.
    def enterActionEnum(self, ctx:govdslParser.ActionEnumContext):
        pass

    # Exit a parse tree produced by govdslParser#actionEnum.
    def exitActionEnum(self, ctx:govdslParser.ActionEnumContext):
        pass


    # Enter a parse tree produced by govdslParser#labels.
    def enterLabels(self, ctx:govdslParser.LabelsContext):
        pass

    # Exit a parse tree produced by govdslParser#labels.
    def exitLabels(self, ctx:govdslParser.LabelsContext):
        pass


    # Enter a parse tree produced by govdslParser#decisionType.
    def enterDecisionType(self, ctx:govdslParser.DecisionTypeContext):
        pass

    # Exit a parse tree produced by govdslParser#decisionType.
    def exitDecisionType(self, ctx:govdslParser.DecisionTypeContext):
        pass


    # Enter a parse tree produced by govdslParser#booleanDecision.
    def enterBooleanDecision(self, ctx:govdslParser.BooleanDecisionContext):
        pass

    # Exit a parse tree produced by govdslParser#booleanDecision.
    def exitBooleanDecision(self, ctx:govdslParser.BooleanDecisionContext):
        pass


    # Enter a parse tree produced by govdslParser#stringList.
    def enterStringList(self, ctx:govdslParser.StringListContext):
        pass

    # Exit a parse tree produced by govdslParser#stringList.
    def exitStringList(self, ctx:govdslParser.StringListContext):
        pass


    # Enter a parse tree produced by govdslParser#elementList.
    def enterElementList(self, ctx:govdslParser.ElementListContext):
        pass

    # Exit a parse tree produced by govdslParser#elementList.
    def exitElementList(self, ctx:govdslParser.ElementListContext):
        pass


    # Enter a parse tree produced by govdslParser#participants.
    def enterParticipants(self, ctx:govdslParser.ParticipantsContext):
        pass

    # Exit a parse tree produced by govdslParser#participants.
    def exitParticipants(self, ctx:govdslParser.ParticipantsContext):
        pass


    # Enter a parse tree produced by govdslParser#roles.
    def enterRoles(self, ctx:govdslParser.RolesContext):
        pass

    # Exit a parse tree produced by govdslParser#roles.
    def exitRoles(self, ctx:govdslParser.RolesContext):
        pass


    # Enter a parse tree produced by govdslParser#role.
    def enterRole(self, ctx:govdslParser.RoleContext):
        pass

    # Exit a parse tree produced by govdslParser#role.
    def exitRole(self, ctx:govdslParser.RoleContext):
        pass


    # Enter a parse tree produced by govdslParser#individuals.
    def enterIndividuals(self, ctx:govdslParser.IndividualsContext):
        pass

    # Exit a parse tree produced by govdslParser#individuals.
    def exitIndividuals(self, ctx:govdslParser.IndividualsContext):
        pass


    # Enter a parse tree produced by govdslParser#individualEntry.
    def enterIndividualEntry(self, ctx:govdslParser.IndividualEntryContext):
        pass

    # Exit a parse tree produced by govdslParser#individualEntry.
    def exitIndividualEntry(self, ctx:govdslParser.IndividualEntryContext):
        pass


    # Enter a parse tree produced by govdslParser#individual.
    def enterIndividual(self, ctx:govdslParser.IndividualContext):
        pass

    # Exit a parse tree produced by govdslParser#individual.
    def exitIndividual(self, ctx:govdslParser.IndividualContext):
        pass


    # Enter a parse tree produced by govdslParser#voteValue.
    def enterVoteValue(self, ctx:govdslParser.VoteValueContext):
        pass

    # Exit a parse tree produced by govdslParser#voteValue.
    def exitVoteValue(self, ctx:govdslParser.VoteValueContext):
        pass


    # Enter a parse tree produced by govdslParser#withProfile.
    def enterWithProfile(self, ctx:govdslParser.WithProfileContext):
        pass

    # Exit a parse tree produced by govdslParser#withProfile.
    def exitWithProfile(self, ctx:govdslParser.WithProfileContext):
        pass


    # Enter a parse tree produced by govdslParser#withRole.
    def enterWithRole(self, ctx:govdslParser.WithRoleContext):
        pass

    # Exit a parse tree produced by govdslParser#withRole.
    def exitWithRole(self, ctx:govdslParser.WithRoleContext):
        pass


    # Enter a parse tree produced by govdslParser#agent.
    def enterAgent(self, ctx:govdslParser.AgentContext):
        pass

    # Exit a parse tree produced by govdslParser#agent.
    def exitAgent(self, ctx:govdslParser.AgentContext):
        pass


    # Enter a parse tree produced by govdslParser#confidence.
    def enterConfidence(self, ctx:govdslParser.ConfidenceContext):
        pass

    # Exit a parse tree produced by govdslParser#confidence.
    def exitConfidence(self, ctx:govdslParser.ConfidenceContext):
        pass


    # Enter a parse tree produced by govdslParser#autonomyLevel.
    def enterAutonomyLevel(self, ctx:govdslParser.AutonomyLevelContext):
        pass

    # Exit a parse tree produced by govdslParser#autonomyLevel.
    def exitAutonomyLevel(self, ctx:govdslParser.AutonomyLevelContext):
        pass


    # Enter a parse tree produced by govdslParser#explainability.
    def enterExplainability(self, ctx:govdslParser.ExplainabilityContext):
        pass

    # Exit a parse tree produced by govdslParser#explainability.
    def exitExplainability(self, ctx:govdslParser.ExplainabilityContext):
        pass


    # Enter a parse tree produced by govdslParser#profiles.
    def enterProfiles(self, ctx:govdslParser.ProfilesContext):
        pass

    # Exit a parse tree produced by govdslParser#profiles.
    def exitProfiles(self, ctx:govdslParser.ProfilesContext):
        pass


    # Enter a parse tree produced by govdslParser#profile.
    def enterProfile(self, ctx:govdslParser.ProfileContext):
        pass

    # Exit a parse tree produced by govdslParser#profile.
    def exitProfile(self, ctx:govdslParser.ProfileContext):
        pass


    # Enter a parse tree produced by govdslParser#gender.
    def enterGender(self, ctx:govdslParser.GenderContext):
        pass

    # Exit a parse tree produced by govdslParser#gender.
    def exitGender(self, ctx:govdslParser.GenderContext):
        pass


    # Enter a parse tree produced by govdslParser#race.
    def enterRace(self, ctx:govdslParser.RaceContext):
        pass

    # Exit a parse tree produced by govdslParser#race.
    def exitRace(self, ctx:govdslParser.RaceContext):
        pass


    # Enter a parse tree produced by govdslParser#policyParticipants.
    def enterPolicyParticipants(self, ctx:govdslParser.PolicyParticipantsContext):
        pass

    # Exit a parse tree produced by govdslParser#policyParticipants.
    def exitPolicyParticipants(self, ctx:govdslParser.PolicyParticipantsContext):
        pass


    # Enter a parse tree produced by govdslParser#partID.
    def enterPartID(self, ctx:govdslParser.PartIDContext):
        pass

    # Exit a parse tree produced by govdslParser#partID.
    def exitPartID(self, ctx:govdslParser.PartIDContext):
        pass


    # Enter a parse tree produced by govdslParser#hasRole.
    def enterHasRole(self, ctx:govdslParser.HasRoleContext):
        pass

    # Exit a parse tree produced by govdslParser#hasRole.
    def exitHasRole(self, ctx:govdslParser.HasRoleContext):
        pass


    # Enter a parse tree produced by govdslParser#conditions.
    def enterConditions(self, ctx:govdslParser.ConditionsContext):
        pass

    # Exit a parse tree produced by govdslParser#conditions.
    def exitConditions(self, ctx:govdslParser.ConditionsContext):
        pass


    # Enter a parse tree produced by govdslParser#deadline.
    def enterDeadline(self, ctx:govdslParser.DeadlineContext):
        pass

    # Exit a parse tree produced by govdslParser#deadline.
    def exitDeadline(self, ctx:govdslParser.DeadlineContext):
        pass


    # Enter a parse tree produced by govdslParser#minDecisionTime.
    def enterMinDecisionTime(self, ctx:govdslParser.MinDecisionTimeContext):
        pass

    # Exit a parse tree produced by govdslParser#minDecisionTime.
    def exitMinDecisionTime(self, ctx:govdslParser.MinDecisionTimeContext):
        pass


    # Enter a parse tree produced by govdslParser#offset.
    def enterOffset(self, ctx:govdslParser.OffsetContext):
        pass

    # Exit a parse tree produced by govdslParser#offset.
    def exitOffset(self, ctx:govdslParser.OffsetContext):
        pass


    # Enter a parse tree produced by govdslParser#deadlineID.
    def enterDeadlineID(self, ctx:govdslParser.DeadlineIDContext):
        pass

    # Exit a parse tree produced by govdslParser#deadlineID.
    def exitDeadlineID(self, ctx:govdslParser.DeadlineIDContext):
        pass


    # Enter a parse tree produced by govdslParser#timeUnit.
    def enterTimeUnit(self, ctx:govdslParser.TimeUnitContext):
        pass

    # Exit a parse tree produced by govdslParser#timeUnit.
    def exitTimeUnit(self, ctx:govdslParser.TimeUnitContext):
        pass


    # Enter a parse tree produced by govdslParser#date.
    def enterDate(self, ctx:govdslParser.DateContext):
        pass

    # Exit a parse tree produced by govdslParser#date.
    def exitDate(self, ctx:govdslParser.DateContext):
        pass


    # Enter a parse tree produced by govdslParser#participantExclusion.
    def enterParticipantExclusion(self, ctx:govdslParser.ParticipantExclusionContext):
        pass

    # Exit a parse tree produced by govdslParser#participantExclusion.
    def exitParticipantExclusion(self, ctx:govdslParser.ParticipantExclusionContext):
        pass


    # Enter a parse tree produced by govdslParser#minParticipant.
    def enterMinParticipant(self, ctx:govdslParser.MinParticipantContext):
        pass

    # Exit a parse tree produced by govdslParser#minParticipant.
    def exitMinParticipant(self, ctx:govdslParser.MinParticipantContext):
        pass


    # Enter a parse tree produced by govdslParser#vetoRight.
    def enterVetoRight(self, ctx:govdslParser.VetoRightContext):
        pass

    # Exit a parse tree produced by govdslParser#vetoRight.
    def exitVetoRight(self, ctx:govdslParser.VetoRightContext):
        pass


    # Enter a parse tree produced by govdslParser#passedTests.
    def enterPassedTests(self, ctx:govdslParser.PassedTestsContext):
        pass

    # Exit a parse tree produced by govdslParser#passedTests.
    def exitPassedTests(self, ctx:govdslParser.PassedTestsContext):
        pass


    # Enter a parse tree produced by govdslParser#evaluationMode.
    def enterEvaluationMode(self, ctx:govdslParser.EvaluationModeContext):
        pass

    # Exit a parse tree produced by govdslParser#evaluationMode.
    def exitEvaluationMode(self, ctx:govdslParser.EvaluationModeContext):
        pass


    # Enter a parse tree produced by govdslParser#labelsCondition.
    def enterLabelsCondition(self, ctx:govdslParser.LabelsConditionContext):
        pass

    # Exit a parse tree produced by govdslParser#labelsCondition.
    def exitLabelsCondition(self, ctx:govdslParser.LabelsConditionContext):
        pass


    # Enter a parse tree produced by govdslParser#include.
    def enterInclude(self, ctx:govdslParser.IncludeContext):
        pass

    # Exit a parse tree produced by govdslParser#include.
    def exitInclude(self, ctx:govdslParser.IncludeContext):
        pass


    # Enter a parse tree produced by govdslParser#parameters.
    def enterParameters(self, ctx:govdslParser.ParametersContext):
        pass

    # Exit a parse tree produced by govdslParser#parameters.
    def exitParameters(self, ctx:govdslParser.ParametersContext):
        pass


    # Enter a parse tree produced by govdslParser#votParams.
    def enterVotParams(self, ctx:govdslParser.VotParamsContext):
        pass

    # Exit a parse tree produced by govdslParser#votParams.
    def exitVotParams(self, ctx:govdslParser.VotParamsContext):
        pass


    # Enter a parse tree produced by govdslParser#ratio.
    def enterRatio(self, ctx:govdslParser.RatioContext):
        pass

    # Exit a parse tree produced by govdslParser#ratio.
    def exitRatio(self, ctx:govdslParser.RatioContext):
        pass


    # Enter a parse tree produced by govdslParser#default.
    def enterDefault(self, ctx:govdslParser.DefaultContext):
        pass

    # Exit a parse tree produced by govdslParser#default.
    def exitDefault(self, ctx:govdslParser.DefaultContext):
        pass


    # Enter a parse tree produced by govdslParser#fallback.
    def enterFallback(self, ctx:govdslParser.FallbackContext):
        pass

    # Exit a parse tree produced by govdslParser#fallback.
    def exitFallback(self, ctx:govdslParser.FallbackContext):
        pass


    # Enter a parse tree produced by govdslParser#policyReference.
    def enterPolicyReference(self, ctx:govdslParser.PolicyReferenceContext):
        pass

    # Exit a parse tree produced by govdslParser#policyReference.
    def exitPolicyReference(self, ctx:govdslParser.PolicyReferenceContext):
        pass


    # Enter a parse tree produced by govdslParser#order.
    def enterOrder(self, ctx:govdslParser.OrderContext):
        pass

    # Exit a parse tree produced by govdslParser#order.
    def exitOrder(self, ctx:govdslParser.OrderContext):
        pass


    # Enter a parse tree produced by govdslParser#orderType.
    def enterOrderType(self, ctx:govdslParser.OrderTypeContext):
        pass

    # Exit a parse tree produced by govdslParser#orderType.
    def exitOrderType(self, ctx:govdslParser.OrderTypeContext):
        pass


    # Enter a parse tree produced by govdslParser#orderTypeValue.
    def enterOrderTypeValue(self, ctx:govdslParser.OrderTypeValueContext):
        pass

    # Exit a parse tree produced by govdslParser#orderTypeValue.
    def exitOrderTypeValue(self, ctx:govdslParser.OrderTypeValueContext):
        pass


    # Enter a parse tree produced by govdslParser#orderMode.
    def enterOrderMode(self, ctx:govdslParser.OrderModeContext):
        pass

    # Exit a parse tree produced by govdslParser#orderMode.
    def exitOrderMode(self, ctx:govdslParser.OrderModeContext):
        pass


    # Enter a parse tree produced by govdslParser#carryOver.
    def enterCarryOver(self, ctx:govdslParser.CarryOverContext):
        pass

    # Exit a parse tree produced by govdslParser#carryOver.
    def exitCarryOver(self, ctx:govdslParser.CarryOverContext):
        pass


    # Enter a parse tree produced by govdslParser#booleanValue.
    def enterBooleanValue(self, ctx:govdslParser.BooleanValueContext):
        pass

    # Exit a parse tree produced by govdslParser#booleanValue.
    def exitBooleanValue(self, ctx:govdslParser.BooleanValueContext):
        pass


    # Enter a parse tree produced by govdslParser#phases.
    def enterPhases(self, ctx:govdslParser.PhasesContext):
        pass

    # Exit a parse tree produced by govdslParser#phases.
    def exitPhases(self, ctx:govdslParser.PhasesContext):
        pass


    # Enter a parse tree produced by govdslParser#nestedPolicy.
    def enterNestedPolicy(self, ctx:govdslParser.NestedPolicyContext):
        pass

    # Exit a parse tree produced by govdslParser#nestedPolicy.
    def exitNestedPolicy(self, ctx:govdslParser.NestedPolicyContext):
        pass



del govdslParser