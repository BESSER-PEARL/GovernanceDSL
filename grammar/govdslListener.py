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
        print("Enter policy:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#policy.
    def exitPolicy(self, ctx:govdslParser.PolicyContext):
        print("Exit policy:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#attributes.
    def enterAttributes(self, ctx:govdslParser.AttributesContext):
        print("Enter attributes:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#attributes.
    def exitAttributes(self, ctx:govdslParser.AttributesContext):
        print("Exit attributes:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#project.
    def enterProject(self, ctx:govdslParser.ProjectContext):
        print("Enter project:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#project.
    def exitProject(self, ctx:govdslParser.ProjectContext):
        print("Exit project:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#activity.
    def enterActivity(self, ctx:govdslParser.ActivityContext):
        print("Enter activity:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#activity.
    def exitActivity(self, ctx:govdslParser.ActivityContext):
        print("Exit activity:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#task.
    def enterTask(self, ctx:govdslParser.TaskContext):
        print("Enter task:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#task.
    def exitTask(self, ctx:govdslParser.TaskContext):
        print("Exit task:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#participants.
    def enterParticipants(self, ctx:govdslParser.ParticipantsContext):
        print("Enter participants:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#participants.
    def exitParticipants(self, ctx:govdslParser.ParticipantsContext):
        print("Exit participants:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#roles.
    def enterRoles(self, ctx:govdslParser.RolesContext):
        print("Enter roles:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#roles.
    def exitRoles(self, ctx:govdslParser.RolesContext):
        print("Exit roles:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#participantID.
    def enterParticipantID(self, ctx:govdslParser.ParticipantIDContext):
        print("Enter participantID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#participantID.
    def exitParticipantID(self, ctx:govdslParser.ParticipantIDContext):
        print("Exit participantID:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#individuals.
    def enterIndividuals(self, ctx:govdslParser.IndividualsContext):
        print("Enter individuals:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#individuals.
    def exitIndividuals(self, ctx:govdslParser.IndividualsContext):
        print("Exit individuals:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#conditions.
    def enterConditions(self, ctx:govdslParser.ConditionsContext):
        print("Enter conditions:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#conditions.
    def exitConditions(self, ctx:govdslParser.ConditionsContext):
        print("Exit conditions:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#deadline.
    def enterDeadline(self, ctx:govdslParser.DeadlineContext):
        print("Enter deadline:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#deadline.
    def exitDeadline(self, ctx:govdslParser.DeadlineContext):
        print("Exit deadline:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#offset.
    def enterOffset(self, ctx:govdslParser.OffsetContext):
        print("Enter offset:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#offset.
    def exitOffset(self, ctx:govdslParser.OffsetContext):
        print("Exit offset:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#deadlineID.
    def enterDeadlineID(self, ctx:govdslParser.DeadlineIDContext):
        print("Enter deadlineID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#deadlineID.
    def exitDeadlineID(self, ctx:govdslParser.DeadlineIDContext):
        print("Exit deadlineID:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#timeUnit.
    def enterTimeUnit(self, ctx:govdslParser.TimeUnitContext):
        print("Enter timeUnit:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#timeUnit.
    def exitTimeUnit(self, ctx:govdslParser.TimeUnitContext):
        print("Exit timeUnit:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#date.
    def enterDate(self, ctx:govdslParser.DateContext):
        print("Enter date:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#date.
    def exitDate(self, ctx:govdslParser.DateContext):
        print("Exit date:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#votingCondition.
    def enterVotingCondition(self, ctx:govdslParser.VotingConditionContext):
        print("Enter votingCondition:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#votingCondition.
    def exitVotingCondition(self, ctx:govdslParser.VotingConditionContext):
        print("Exit votingCondition:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#voteConditionID.
    def enterVoteConditionID(self, ctx:govdslParser.VoteConditionIDContext):
        print("Enter voteConditionID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#voteConditionID.
    def exitVoteConditionID(self, ctx:govdslParser.VoteConditionIDContext):
        print("Exit voteConditionID:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#minVotes.
    def enterMinVotes(self, ctx:govdslParser.MinVotesContext):
        print("Enter minVotes:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#minVotes.
    def exitMinVotes(self, ctx:govdslParser.MinVotesContext):
        print("Exit minVotes:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#ratio.
    def enterRatio(self, ctx:govdslParser.RatioContext):
        print("Enter ratio:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#ratio.
    def exitRatio(self, ctx:govdslParser.RatioContext):
        print("Exit ratio:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#rules.
    def enterRules(self, ctx:govdslParser.RulesContext):
        print("Enter rules:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#rules.
    def exitRules(self, ctx:govdslParser.RulesContext):
        print("Exit rules:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#rule.
    def enterRule(self, ctx:govdslParser.RuleContext):
        print("Enter rule:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#rule.
    def exitRule(self, ctx:govdslParser.RuleContext):
        print("Exit rule:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#ruleID.
    def enterRuleID(self, ctx:govdslParser.RuleIDContext):
        print("Enter ruleID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#ruleID.
    def exitRuleID(self, ctx:govdslParser.RuleIDContext):
        print("Exit ruleID:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#ruleType.
    def enterRuleType(self, ctx:govdslParser.RuleTypeContext):
        print("Enter ruleType:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#ruleType.
    def exitRuleType(self, ctx:govdslParser.RuleTypeContext):
        print("Exit ruleType:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#ruleContent.
    def enterRuleContent(self, ctx:govdslParser.RuleContentContext):
        print("Enter ruleContent:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#ruleContent.
    def exitRuleContent(self, ctx:govdslParser.RuleContentContext):
        print("Exit ruleContent:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#people.
    def enterPeople(self, ctx:govdslParser.PeopleContext):
        print("Enter people:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#people.
    def exitPeople(self, ctx:govdslParser.PeopleContext):
        print("Exit people:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#rangeType.
    def enterRangeType(self, ctx:govdslParser.RangeTypeContext):
        print("Enter rangeType:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#rangeType.
    def exitRangeType(self, ctx:govdslParser.RangeTypeContext):
        print("Exit rangeType:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#rangeID.
    def enterRangeID(self, ctx:govdslParser.RangeIDContext):
        print("Enter rangeID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#rangeID.
    def exitRangeID(self, ctx:govdslParser.RangeIDContext):
        print("Exit rangeID:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#ruleConditions.
    def enterRuleConditions(self, ctx:govdslParser.RuleConditionsContext):
        print("Enter ruleConditions:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#ruleConditions.
    def exitRuleConditions(self, ctx:govdslParser.RuleConditionsContext):
        print("Exit ruleConditions:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#conditionID.
    def enterConditionID(self, ctx:govdslParser.ConditionIDContext):
        print("Enter conditionID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#conditionID.
    def exitConditionID(self, ctx:govdslParser.ConditionIDContext):
        print("Exit conditionID:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#default.
    def enterDefault(self, ctx:govdslParser.DefaultContext):
        print("Enter default:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#default.
    def exitDefault(self, ctx:govdslParser.DefaultContext):
        print("Exit default:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#scope.
    def enterScope(self, ctx:govdslParser.ScopeContext):
        print("Enter scope:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#scope.
    def exitScope(self, ctx:govdslParser.ScopeContext):
        print("Exit scope:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#phases.
    def enterPhases(self, ctx:govdslParser.PhasesContext):
        print("Enter phases:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#phases.
    def exitPhases(self, ctx:govdslParser.PhasesContext):
        print("Exit phases:", ctx.getText())
        pass
    
del govdslParser