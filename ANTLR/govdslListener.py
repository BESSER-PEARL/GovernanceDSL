# Generated from govdsl.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .govdslParser import govdslParser
else:
    from govdslParser import govdslParser

# This class defines a complete listener for a parse tree produced by govdslParser.
class govdslListener(ParseTreeListener):
    # Enter a parse tree produced by govdslParser#project.
    def enterProject(self, ctx:govdslParser.ProjectContext):
        print("Enter project:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#project.
    def exitProject(self, ctx:govdslParser.ProjectContext):
        print("Exit project:", ctx.getText())
        pass

    # Enter a parse tree produced by govdslParser#attributes.
    def enterAttributes(self, ctx:govdslParser.AttributesContext):
        print("Enter attributes:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#attributes.
    def exitAttributes(self, ctx:govdslParser.AttributesContext):
        print("Exit attributes:", ctx.getText())
        pass

    # Enter a parse tree produced by govdslParser#roles.
    def enterRoles(self, ctx:govdslParser.RolesContext):
        print("Enter roles:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#roles.
    def exitRoles(self, ctx:govdslParser.RolesContext):
        print("Exit roles:", ctx.getText())
        pass

    # Enter a parse tree produced by govdslParser#roleID.
    def enterRoleID(self, ctx:govdslParser.RoleIDContext):
        print("Enter roleID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#roleID.
    def exitRoleID(self, ctx:govdslParser.RoleIDContext):
        print("Exit roleID:", ctx.getText())
        pass

    # Enter a parse tree produced by govdslParser#deadlines.
    def enterDeadlines(self, ctx:govdslParser.DeadlinesContext):
        print("Enter deadlines:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#deadlines.
    def exitDeadlines(self, ctx:govdslParser.DeadlinesContext):
        print("Exit deadlines:", ctx.getText())
        pass

    # Enter a parse tree produced by govdslParser#deadline.
    def enterDeadline(self, ctx:govdslParser.DeadlineContext):
        print("Enter deadline:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#deadline.
    def exitDeadline(self, ctx:govdslParser.DeadlineContext):
        print("Exit deadline:", ctx.getText())
        pass

    # Enter a parse tree produced by govdslParser#deadlineID.
    def enterDeadlineID(self, ctx:govdslParser.DeadlineIDContext):
        print("Enter deadlineID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#deadlineID.
    def exitDeadlineID(self, ctx:govdslParser.DeadlineIDContext):
        print("Exit deadlineID:", ctx.getText())
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

    # Enter a parse tree produced by govdslParser#ruleContent.
    def enterRuleContent(self, ctx:govdslParser.RuleContentContext):
        print("Enter ruleContent:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#ruleContent.
    def exitRuleContent(self, ctx:govdslParser.RuleContentContext):
        print("Exit ruleContent:", ctx.getText())
        pass

    # Enter a parse tree produced by govdslParser#appliedTo.
    def enterAppliedTo(self, ctx:govdslParser.AppliedToContext):
        print("Enter appliedTo:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#appliedTo.
    def exitAppliedTo(self, ctx:govdslParser.AppliedToContext):
        print("Exit appliedTo:", ctx.getText())
        pass

    # Enter a parse tree produced by govdslParser#taskID.
    def enterTaskID(self, ctx:govdslParser.TaskIDContext):
        print("Enter taskID:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#taskID.
    def exitTaskID(self, ctx:govdslParser.TaskIDContext):
        print("Exit taskID:", ctx.getText())
        pass

    # Enter a parse tree produced by govdslParser#people.
    def enterPeople(self, ctx:govdslParser.PeopleContext):
        print("Enter people:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#people.
    def exitPeople(self, ctx:govdslParser.PeopleContext):
        print("Exit people:", ctx.getText())
        pass

    # Enter a parse tree produced by govdslParser#minVotes.
    def enterMinVotes(self, ctx:govdslParser.MinVotesContext):
        print("Enter minVotes:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#minVotes.
    def exitMinVotes(self, ctx:govdslParser.MinVotesContext):
        print("Exit minVotes:", ctx.getText())
        pass

    # Enter a parse tree produced by govdslParser#timeUnit.
    def enterTimeUnit(self, ctx:govdslParser.TimeUnitContext):
        print("Enter timeUnit:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#timeUnit.
    def exitTimeUnit(self, ctx:govdslParser.TimeUnitContext):
        print("Exit timeUnit:", ctx.getText())
        pass

    # Enter a parse tree produced by govdslParser#ruleType.
    def enterRuleType(self, ctx:govdslParser.RuleTypeContext):
        print("Enter ruleType:", ctx.getText())
        pass

    # Exit a parse tree produced by govdslParser#ruleType.
    def exitRuleType(self, ctx:govdslParser.RuleTypeContext):
        print("Exit ruleType:", ctx.getText())
        pass
   


del govdslParser