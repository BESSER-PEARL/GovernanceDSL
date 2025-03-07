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
        print("Enter Policy:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#policy.
    def exitPolicy(self, ctx:govdslParser.PolicyContext):
        print("Exit Policy:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#policyContent.
    def enterPolicyContent(self, ctx:govdslParser.PolicyContentContext):
        print("Enter PolicyContent:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#policyContent.
    def exitPolicyContent(self, ctx:govdslParser.PolicyContentContext):
        print("Exit PolicyContent:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#singlePolicy.
    def enterSinglePolicy(self, ctx:govdslParser.SinglePolicyContext):
        print("Enter SinglePolicy:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#singlePolicy.
    def exitSinglePolicy(self, ctx:govdslParser.SinglePolicyContext):
        print("Exit SinglePolicy:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#phasedPolicy.
    def enterPhasedPolicy(self, ctx:govdslParser.PhasedPolicyContext):
        print("Enter PhasedPolicy:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#phasedPolicy.
    def exitPhasedPolicy(self, ctx:govdslParser.PhasedPolicyContext):
        print("Exit PhasedPolicy:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#attributesSingle.
    def enterAttributesSingle(self, ctx:govdslParser.AttributesSingleContext):
        print("Enter AttributesSingle:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#attributesSingle.
    def exitAttributesSingle(self, ctx:govdslParser.AttributesSingleContext):
        print("Exit AttributesSingle:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#attributesPhased.
    def enterAttributesPhased(self, ctx:govdslParser.AttributesPhasedContext):
        print("Enter AttributesPhased:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#attributesPhased.
    def exitAttributesPhased(self, ctx:govdslParser.AttributesPhasedContext):
        print("Exit AttributesPhased:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#scopes.
    def enterScopes(self, ctx:govdslParser.ScopesContext):
        print("Enter Scopes:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#scopes.
    def exitScopes(self, ctx:govdslParser.ScopesContext):
        print("Exit Scopes:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#project.
    def enterProject(self, ctx:govdslParser.ProjectContext):
        print("Enter Project:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#project.
    def exitProject(self, ctx:govdslParser.ProjectContext):
        print("Exit Project:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#platform.
    def enterPlatform(self, ctx:govdslParser.PlatformContext):
        print("Enter Platform:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#platform.
    def exitPlatform(self, ctx:govdslParser.PlatformContext):
        print("Exit Platform:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#repoID.
    def enterRepoID(self, ctx:govdslParser.RepoIDContext):
        print("Enter RepoID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#repoID.
    def exitRepoID(self, ctx:govdslParser.RepoIDContext):
        print("Exit RepoID:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#activity.
    def enterActivity(self, ctx:govdslParser.ActivityContext):
        print("Enter Activity:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#activity.
    def exitActivity(self, ctx:govdslParser.ActivityContext):
        print("Exit Activity:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#task.
    def enterTask(self, ctx:govdslParser.TaskContext):
        print("Enter Task:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#task.
    def exitTask(self, ctx:govdslParser.TaskContext):
        print("Exit Task:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#taskType.
    def enterTaskType(self, ctx:govdslParser.TaskTypeContext):
        print("Enter TaskType:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#taskType.
    def exitTaskType(self, ctx:govdslParser.TaskTypeContext):
        print("Exit TaskType:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#taskContent.
    def enterTaskContent(self, ctx:govdslParser.TaskContentContext):
        print("Enter TaskContent:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#taskContent.
    def exitTaskContent(self, ctx:govdslParser.TaskContentContext):
        print("Exit TaskContent:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#status.
    def enterStatus(self, ctx:govdslParser.StatusContext):
        print("Enter Status:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#status.
    def exitStatus(self, ctx:govdslParser.StatusContext):
        print("Exit Status:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#participants.
    def enterParticipants(self, ctx:govdslParser.ParticipantsContext):
        print("Enter Participants:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#participants.
    def exitParticipants(self, ctx:govdslParser.ParticipantsContext):
        print("Exit Participants:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#roles.
    def enterRoles(self, ctx:govdslParser.RolesContext):
        print("Enter Roles:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#roles.
    def exitRoles(self, ctx:govdslParser.RolesContext):
        print("Exit Roles:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#participantID.
    def enterParticipantID(self, ctx:govdslParser.ParticipantIDContext):
        print("Enter ParticipantID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#participantID.
    def exitParticipantID(self, ctx:govdslParser.ParticipantIDContext):
        print("Exit ParticipantID:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#individuals.
    def enterIndividuals(self, ctx:govdslParser.IndividualsContext):
        print("Enter Individuals:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#individuals.
    def exitIndividuals(self, ctx:govdslParser.IndividualsContext):
        print("Exit Individuals:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#conditions.
    def enterConditions(self, ctx:govdslParser.ConditionsContext):
        print("Enter Conditions:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#conditions.
    def exitConditions(self, ctx:govdslParser.ConditionsContext):
        print("Exit Conditions:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#deadline.
    def enterDeadline(self, ctx:govdslParser.DeadlineContext):
        print("Enter Deadline:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#deadline.
    def exitDeadline(self, ctx:govdslParser.DeadlineContext):
        print("Exit Deadline:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#offset.
    def enterOffset(self, ctx:govdslParser.OffsetContext):
        print("Enter Offset:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#offset.
    def exitOffset(self, ctx:govdslParser.OffsetContext):
        print("Exit Offset:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#deadlineID.
    def enterDeadlineID(self, ctx:govdslParser.DeadlineIDContext):
        print("Enter DeadlineID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#deadlineID.
    def exitDeadlineID(self, ctx:govdslParser.DeadlineIDContext):
        print("Exit DeadlineID:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#timeUnit.
    def enterTimeUnit(self, ctx:govdslParser.TimeUnitContext):
        print("Enter TimeUnit:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#timeUnit.
    def exitTimeUnit(self, ctx:govdslParser.TimeUnitContext):
        print("Exit TimeUnit:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#date.
    def enterDate(self, ctx:govdslParser.DateContext):
        print("Enter Date:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#date.
    def exitDate(self, ctx:govdslParser.DateContext):
        print("Exit Date:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#votingCondition.
    def enterVotingCondition(self, ctx:govdslParser.VotingConditionContext):
        print("Enter VotingCondition:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#votingCondition.
    def exitVotingCondition(self, ctx:govdslParser.VotingConditionContext):
        print("Exit VotingCondition:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#voteConditionID.
    def enterVoteConditionID(self, ctx:govdslParser.VoteConditionIDContext):
        print("Enter VoteConditionID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#voteConditionID.
    def exitVoteConditionID(self, ctx:govdslParser.VoteConditionIDContext):
        print("Exit VoteConditionID:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#minVotes.
    def enterMinVotes(self, ctx:govdslParser.MinVotesContext):
        print("Enter MinVotes:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#minVotes.
    def exitMinVotes(self, ctx:govdslParser.MinVotesContext):
        print("Exit MinVotes:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#ratio.
    def enterRatio(self, ctx:govdslParser.RatioContext):
        print("Enter Ratio:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#ratio.
    def exitRatio(self, ctx:govdslParser.RatioContext):
        print("Exit Ratio:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#rules.
    def enterRules(self, ctx:govdslParser.RulesContext):
        print("Enter Rules:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#rules.
    def exitRules(self, ctx:govdslParser.RulesContext):
        print("Exit Rules:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#rule.
    def enterRule(self, ctx:govdslParser.RuleContext):
        print("Enter Rule:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#rule.
    def exitRule(self, ctx:govdslParser.RuleContext):
        print("Exit Rule:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#ruleID.
    def enterRuleID(self, ctx:govdslParser.RuleIDContext):
        print("Enter RuleID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#ruleID.
    def exitRuleID(self, ctx:govdslParser.RuleIDContext):
        print("Exit RuleID:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#ruleType.
    def enterRuleType(self, ctx:govdslParser.RuleTypeContext):
        print("Enter RuleType:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#ruleType.
    def exitRuleType(self, ctx:govdslParser.RuleTypeContext):
        print("Exit RuleType:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#ruleContent.
    def enterRuleContent(self, ctx:govdslParser.RuleContentContext):
        print("Enter RuleContent:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#ruleContent.
    def exitRuleContent(self, ctx:govdslParser.RuleContentContext):
        print("Exit RuleContent:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#people.
    def enterPeople(self, ctx:govdslParser.PeopleContext):
        print("Enter People:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#people.
    def exitPeople(self, ctx:govdslParser.PeopleContext):
        print("Exit People:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#rangeType.
    def enterRangeType(self, ctx:govdslParser.RangeTypeContext):
        print("Enter RangeType:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#rangeType.
    def exitRangeType(self, ctx:govdslParser.RangeTypeContext):
        print("Exit RangeType:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#rangeID.
    def enterRangeID(self, ctx:govdslParser.RangeIDContext):
        print("Enter RangeID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#rangeID.
    def exitRangeID(self, ctx:govdslParser.RangeIDContext):
        print("Exit RangeID:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#ruleConditions.
    def enterRuleConditions(self, ctx:govdslParser.RuleConditionsContext):
        print("Enter RuleConditions:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#ruleConditions.
    def exitRuleConditions(self, ctx:govdslParser.RuleConditionsContext):
        print("Exit RuleConditions:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#default.
    def enterDefault(self, ctx:govdslParser.DefaultContext):
        print("Enter Default:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#default.
    def exitDefault(self, ctx:govdslParser.DefaultContext):
        print("Exit Default:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#order.
    def enterOrder(self, ctx:govdslParser.OrderContext):
        print("Enter Order:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#order.
    def exitOrder(self, ctx:govdslParser.OrderContext):
        print("Exit Order:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#orderType.
    def enterOrderType(self, ctx:govdslParser.OrderTypeContext):
        print("Enter OrderType:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#orderType.
    def exitOrderType(self, ctx:govdslParser.OrderTypeContext):
        print("Exit OrderType:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#orderMode.
    def enterOrderMode(self, ctx:govdslParser.OrderModeContext):
        print("Enter OrderMode:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#orderMode.
    def exitOrderMode(self, ctx:govdslParser.OrderModeContext):
        print("Exit OrderMode:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#phases.
    def enterPhases(self, ctx:govdslParser.PhasesContext):
        print("Enter Phases:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#phases.
    def exitPhases(self, ctx:govdslParser.PhasesContext):
        print("Exit Phases:", ctx.getText())
        pass
    
del govdslParser