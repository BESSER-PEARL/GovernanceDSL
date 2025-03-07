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
        pass

    # Exit a parse tree produced by govdslParser#policy.
    def exitPolicy(self, ctx:govdslParser.PolicyContext):
        pass


    # Enter a parse tree produced by govdslParser#policyContent.
    def enterPolicyContent(self, ctx:govdslParser.PolicyContentContext):
        pass

    # Exit a parse tree produced by govdslParser#policyContent.
    def exitPolicyContent(self, ctx:govdslParser.PolicyContentContext):
        pass


    # Enter a parse tree produced by govdslParser#singlePolicy.
    def enterSinglePolicy(self, ctx:govdslParser.SinglePolicyContext):
        pass

    # Exit a parse tree produced by govdslParser#singlePolicy.
    def exitSinglePolicy(self, ctx:govdslParser.SinglePolicyContext):
        pass


    # Enter a parse tree produced by govdslParser#phasedPolicy.
    def enterPhasedPolicy(self, ctx:govdslParser.PhasedPolicyContext):
        pass

    # Exit a parse tree produced by govdslParser#phasedPolicy.
    def exitPhasedPolicy(self, ctx:govdslParser.PhasedPolicyContext):
        pass


    # Enter a parse tree produced by govdslParser#attributesSingle.
    def enterAttributesSingle(self, ctx:govdslParser.AttributesSingleContext):
        pass

    # Exit a parse tree produced by govdslParser#attributesSingle.
    def exitAttributesSingle(self, ctx:govdslParser.AttributesSingleContext):
        pass


    # Enter a parse tree produced by govdslParser#attributesPhased.
    def enterAttributesPhased(self, ctx:govdslParser.AttributesPhasedContext):
        pass

    # Exit a parse tree produced by govdslParser#attributesPhased.
    def exitAttributesPhased(self, ctx:govdslParser.AttributesPhasedContext):
        pass


    # Enter a parse tree produced by govdslParser#scopes.
    def enterScopes(self, ctx:govdslParser.ScopesContext):
        pass

    # Exit a parse tree produced by govdslParser#scopes.
    def exitScopes(self, ctx:govdslParser.ScopesContext):
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


    # Enter a parse tree produced by govdslParser#activity.
    def enterActivity(self, ctx:govdslParser.ActivityContext):
        pass

    # Exit a parse tree produced by govdslParser#activity.
    def exitActivity(self, ctx:govdslParser.ActivityContext):
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


    # Enter a parse tree produced by govdslParser#status.
    def enterStatus(self, ctx:govdslParser.StatusContext):
        pass

    # Exit a parse tree produced by govdslParser#status.
    def exitStatus(self, ctx:govdslParser.StatusContext):
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


    # Enter a parse tree produced by govdslParser#participantID.
    def enterParticipantID(self, ctx:govdslParser.ParticipantIDContext):
        pass

    # Exit a parse tree produced by govdslParser#participantID.
    def exitParticipantID(self, ctx:govdslParser.ParticipantIDContext):
        pass


    # Enter a parse tree produced by govdslParser#individuals.
    def enterIndividuals(self, ctx:govdslParser.IndividualsContext):
        pass

    # Exit a parse tree produced by govdslParser#individuals.
    def exitIndividuals(self, ctx:govdslParser.IndividualsContext):
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


    # Enter a parse tree produced by govdslParser#votingCondition.
    def enterVotingCondition(self, ctx:govdslParser.VotingConditionContext):
        pass

    # Exit a parse tree produced by govdslParser#votingCondition.
    def exitVotingCondition(self, ctx:govdslParser.VotingConditionContext):
        pass


    # Enter a parse tree produced by govdslParser#voteConditionID.
    def enterVoteConditionID(self, ctx:govdslParser.VoteConditionIDContext):
        pass

    # Exit a parse tree produced by govdslParser#voteConditionID.
    def exitVoteConditionID(self, ctx:govdslParser.VoteConditionIDContext):
        pass


    # Enter a parse tree produced by govdslParser#minVotes.
    def enterMinVotes(self, ctx:govdslParser.MinVotesContext):
        pass

    # Exit a parse tree produced by govdslParser#minVotes.
    def exitMinVotes(self, ctx:govdslParser.MinVotesContext):
        pass


    # Enter a parse tree produced by govdslParser#ratio.
    def enterRatio(self, ctx:govdslParser.RatioContext):
        pass

    # Exit a parse tree produced by govdslParser#ratio.
    def exitRatio(self, ctx:govdslParser.RatioContext):
        pass


    # Enter a parse tree produced by govdslParser#rules.
    def enterRules(self, ctx:govdslParser.RulesContext):
        pass

    # Exit a parse tree produced by govdslParser#rules.
    def exitRules(self, ctx:govdslParser.RulesContext):
        pass


    # Enter a parse tree produced by govdslParser#rule.
    def enterRule(self, ctx:govdslParser.RuleContext):
        pass

    # Exit a parse tree produced by govdslParser#rule.
    def exitRule(self, ctx:govdslParser.RuleContext):
        pass


    # Enter a parse tree produced by govdslParser#ruleID.
    def enterRuleID(self, ctx:govdslParser.RuleIDContext):
        pass

    # Exit a parse tree produced by govdslParser#ruleID.
    def exitRuleID(self, ctx:govdslParser.RuleIDContext):
        pass


    # Enter a parse tree produced by govdslParser#ruleType.
    def enterRuleType(self, ctx:govdslParser.RuleTypeContext):
        pass

    # Exit a parse tree produced by govdslParser#ruleType.
    def exitRuleType(self, ctx:govdslParser.RuleTypeContext):
        pass


    # Enter a parse tree produced by govdslParser#ruleContent.
    def enterRuleContent(self, ctx:govdslParser.RuleContentContext):
        pass

    # Exit a parse tree produced by govdslParser#ruleContent.
    def exitRuleContent(self, ctx:govdslParser.RuleContentContext):
        pass


    # Enter a parse tree produced by govdslParser#people.
    def enterPeople(self, ctx:govdslParser.PeopleContext):
        pass

    # Exit a parse tree produced by govdslParser#people.
    def exitPeople(self, ctx:govdslParser.PeopleContext):
        pass


    # Enter a parse tree produced by govdslParser#rangeType.
    def enterRangeType(self, ctx:govdslParser.RangeTypeContext):
        pass

    # Exit a parse tree produced by govdslParser#rangeType.
    def exitRangeType(self, ctx:govdslParser.RangeTypeContext):
        pass


    # Enter a parse tree produced by govdslParser#rangeID.
    def enterRangeID(self, ctx:govdslParser.RangeIDContext):
        pass

    # Exit a parse tree produced by govdslParser#rangeID.
    def exitRangeID(self, ctx:govdslParser.RangeIDContext):
        pass


    # Enter a parse tree produced by govdslParser#ruleConditions.
    def enterRuleConditions(self, ctx:govdslParser.RuleConditionsContext):
        pass

    # Exit a parse tree produced by govdslParser#ruleConditions.
    def exitRuleConditions(self, ctx:govdslParser.RuleConditionsContext):
        pass


    # Enter a parse tree produced by govdslParser#default.
    def enterDefault(self, ctx:govdslParser.DefaultContext):
        pass

    # Exit a parse tree produced by govdslParser#default.
    def exitDefault(self, ctx:govdslParser.DefaultContext):
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


    # Enter a parse tree produced by govdslParser#orderMode.
    def enterOrderMode(self, ctx:govdslParser.OrderModeContext):
        pass

    # Exit a parse tree produced by govdslParser#orderMode.
    def exitOrderMode(self, ctx:govdslParser.OrderModeContext):
        pass


    # Enter a parse tree produced by govdslParser#phases.
    def enterPhases(self, ctx:govdslParser.PhasesContext):
        pass

    # Exit a parse tree produced by govdslParser#phases.
    def exitPhases(self, ctx:govdslParser.PhasesContext):
        pass



del govdslParser