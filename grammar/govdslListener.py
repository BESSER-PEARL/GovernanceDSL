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


    # Enter a parse tree produced by govdslParser#attributes.
    def enterAttributes(self, ctx:govdslParser.AttributesContext):
        print("Enter Attributes:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#attributes.
    def exitAttributes(self, ctx:govdslParser.AttributesContext):
        print("Exit Attributes:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#project.
    def enterProject(self, ctx:govdslParser.ProjectContext):
        print("Enter Project:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#project.
    def exitProject(self, ctx:govdslParser.ProjectContext):
        print("Exit Project:", ctx.getText())
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


    # Enter a parse tree produced by govdslParser#default.
    def enterDefault(self, ctx:govdslParser.DefaultContext):
        print("Enter Default:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#default.
    def exitDefault(self, ctx:govdslParser.DefaultContext):
        print("Exit Default:", ctx.getText())
        pass


    # Enter a parse tree produced by govdslParser#scope.
    def enterScope(self, ctx:govdslParser.ScopeContext):
        print("Enter Scope:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#scope.
    def exitScope(self, ctx:govdslParser.ScopeContext):
        print("Exit Scope:", ctx.getText())
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