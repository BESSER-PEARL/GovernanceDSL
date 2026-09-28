"""Regression coverage for condition evaluation modes in parsed policies."""

import unittest
from datetime import timedelta

from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker

from governancedsl.grammar.PolicyCreationListener import PolicyCreationListener
from governancedsl.grammar.govdslLexer import govdslLexer
from governancedsl.grammar.govdslParser import govdslParser
from governancedsl.metamodel.governance import (
    AppealRight,
    Deadline,
    EvaluationMode,
    Individual,
    MinDecisionTime,
    MinimumParticipant,
    ParticipantExclusion,
    VetoRight,
)
from governancedsl.utils.chp_extension import CheckCiCd, LabelCondition, MinTime


class ConditionModeTests(unittest.TestCase):
    def parse_conditions(self, conditions):
        source = f"""Scopes:
    Tasks : reviewTask
Participants:
    Individuals : alice, bob
MajorityPolicy testPolicy {{
    Scope: reviewTask
    DecisionType as BooleanDecision
    Participant list : alice, bob
    Conditions:
        {conditions}
}}
"""
        lexer = govdslLexer(InputStream(source))
        parser = govdslParser(CommonTokenStream(lexer))
        tree = parser.governance()
        self.assertEqual(parser.getNumberOfSyntaxErrors(), 0)
        listener = PolicyCreationListener()
        ParseTreeWalker().walk(listener, tree)
        return listener.get_policies()[0].conditions

    def test_metamodel_constructors_default_to_concurrent(self):
        alice = Individual(name="alice")
        conditions = (
            ParticipantExclusion(name="exclusion", excluded={alice}),
            MinimumParticipant(name="minimum", min_participants=1),
            VetoRight(name="veto", vetoers={alice}),
        )
        for condition in conditions:
            with self.subTest(condition=type(condition).__name__):
                self.assertIs(condition.evaluation_mode, EvaluationMode.CONCURRENT)

    def test_parsed_conditions_without_mode(self):
        conditions = self.parse_conditions("""Deadline : 7 days
        MinDecisionTime : 1 days
        ParticipantExclusion : alice
        MinParticipants : 2
        VetoRight : bob
        CheckCiCd : true
        MinTime of Activity : 3 days
        LabelCondition : urgent""")
        expected = {
            ParticipantExclusion: EvaluationMode.CONCURRENT,
            MinimumParticipant: EvaluationMode.CONCURRENT,
            VetoRight: EvaluationMode.CONCURRENT,
            CheckCiCd: EvaluationMode.CONCURRENT,
            MinTime: EvaluationMode.CONCURRENT,
            LabelCondition: EvaluationMode.CONCURRENT,
            Deadline: None,
            MinDecisionTime: None,
        }
        self.assertEqual(len(conditions), len(expected))
        for condition_type, mode in expected.items():
            with self.subTest(condition=condition_type.__name__):
                condition = next(c for c in conditions if isinstance(c, condition_type))
                self.assertIs(condition.evaluation_mode, mode)

    def test_explicit_modes_are_preserved(self):
        for qualifier, mode in (
            ("pre", EvaluationMode.PRE),
            ("concurrent", EvaluationMode.CONCURRENT),
            ("post", EvaluationMode.POST),
        ):
            with self.subTest(qualifier=qualifier):
                conditions = self.parse_conditions(f"""CheckCiCd {qualifier}: true
        MinTime {qualifier} of Activity: 3 days
        LabelCondition {qualifier}: urgent""")
                self.assertEqual(len(conditions), 3)
                for condition_type in (CheckCiCd, MinTime, LabelCondition):
                    condition = next(c for c in conditions if isinstance(c, condition_type))
                    self.assertIs(condition.evaluation_mode, mode)

    def test_appeal_right_mode_is_unchanged(self):
        appeal = AppealRight(name="appeal", appealers={Individual(name="alice")})
        self.assertIsNone(appeal.evaluation_mode)
        self.assertIsNone(Deadline(name="deadline", offset=timedelta(days=1), date=None).evaluation_mode)
        self.assertIsNone(MinDecisionTime(name="minimum", offset=timedelta(days=1), date=None).evaluation_mode)


if __name__ == "__main__":
    unittest.main()
