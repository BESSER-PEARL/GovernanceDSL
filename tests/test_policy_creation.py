import unittest
from datetime import timedelta
import io
from pathlib import Path

from antlr4 import (
    InputStream, CommonTokenStream, ParseTreeWalker
)
from grammar.govdslLexer import govdslLexer
from grammar.govdslParser import govdslParser
from grammar.PolicyCreationListener import PolicyCreationListener
from grammar.govErrorListener import govErrorListener
from utils.exceptions import (
    InvalidVotesException, UndefinedRuleException, 
    UndefinedConditionException, EmptySetException
)
from metamodel.governance import (
    SinglePolicy, Activity, MajorityRule, 
    Role, Deadline, RatioMajorityRule, LeaderDrivenRule, VotingCondition
)

class TestPolicyCreation(unittest.TestCase):
    def setUp(self):
        self.test_cases_path = Path(__file__).parent / "test_cases"
    
    def setup_parser(self, text):        
        lexer = govdslLexer(InputStream(text))
        stream = CommonTokenStream(lexer)
        parser = govdslParser(stream)
        
        self.output = io.StringIO()
        self.error = io.StringIO()

        parser.removeErrorListeners()        
        self.error_listener = govErrorListener(self.error)
        parser.addErrorListener(self.error_listener)  
                
        return parser

    def test_majority_rule_creation(self):
        """Test the creation of a policy with a majority rule."""
        with open(self.test_cases_path / "valid_examples/majority_policy.txt", "r") as file:
            text = file.read()
            
            # Setup parser and create model
            parser = self.setup_parser(text)
            tree = parser.policy()
            self.assertIsNotNone(tree)
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            policy = listener.get_policy()  # Changed from get_project()
            
            # Assertions
            self.assertIsInstance(policy, SinglePolicy)
            self.assertEqual(policy.name, "TestPolicy")
            
            # Test scope
            self.assertEqual(len(policy.scope), 1)
            scope = next(iter(policy.scope))
            self.assertIsInstance(scope, Activity)
            self.assertEqual(scope.name, "TestActivity")
            
            # Test rule content
            self.assertEqual(len(policy.rules), 1)
            rule = next(iter(policy.rules))
            self.assertIsInstance(rule, MajorityRule)
            self.assertEqual(rule.name, "majorityRule")
            
            # Test rule's participants
            self.assertEqual(len(rule.participants), 1)
            participant = next(iter(rule.participants))
            self.assertIsInstance(participant, Role)
            self.assertEqual(participant.name, "Committers")
            
            # Test rule's conditions
            self.assertEqual(len(rule.conditions), 2)
            
            # Test Deadline condition
            deadline_conditions = {c for c in rule.conditions if isinstance(c, Deadline)}
            self.assertEqual(len(deadline_conditions), 1)
            deadline = next(iter(deadline_conditions))
            self.assertEqual(deadline.name, "reviewDeadline")
            self.assertEqual(deadline.offset, timedelta(days=7))
            
            # Test VotingCondition condition
            voting_conditions = {c for c in rule.conditions if isinstance(c, VotingCondition)}
            self.assertEqual(len(voting_conditions), 1)
            votCond = next(iter(voting_conditions))
            self.assertEqual(votCond.name, "votCond")
            self.assertEqual(votCond.minVotes, 2)
            self.assertEqual(votCond.ratio, 0.5)
            
            # Check for parser errors
            self.assertEqual(len(self.error_listener.symbol), 0)

    def test_invalid_num_votes(self):
        """Test the creation of a policy with a majority rule having negative votes."""
        with open(self.test_cases_path / "invalid_examples/invalid_num_votes.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.policy()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            
            with self.assertRaises(InvalidVotesException):
                walker.walk(listener, tree)

    def test_ratio_rule_creation(self):
        """Test the creation of a policy with a ratio majority rule."""
        with open(self.test_cases_path / "valid_examples/ratio_policy.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.policy()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            policy = listener.get_policy()
            
            # Assertions
            self.assertIsInstance(policy, SinglePolicy)
            self.assertEqual(policy.name, "TestPolicy")
            
            # Test scope
            self.assertEqual(len(policy.scope), 1)
            scope = next(iter(policy.scope))
            self.assertIsInstance(scope, Activity)
            self.assertEqual(scope.name, "TestActivity")
            
            # Test rule content
            self.assertEqual(len(policy.rules), 1)
            rule = next(iter(policy.rules))
            self.assertIsInstance(rule, RatioMajorityRule)
            self.assertEqual(rule.name, "ratioRule")
            
            # Test rule's participants
            self.assertEqual(len(rule.participants), 1)
            participant = next(iter(rule.participants))
            self.assertIsInstance(participant, Role)
            self.assertEqual(participant.name, "Committers")
            
            # Test rule's conditions
            self.assertEqual(len(rule.conditions), 2)
            
            # Test Deadline condition
            deadline_conditions = {c for c in rule.conditions if isinstance(c, Deadline)}
            self.assertEqual(len(deadline_conditions), 1)
            deadline = next(iter(deadline_conditions))
            self.assertEqual(deadline.name, "reviewDeadline")
            self.assertEqual(deadline.offset, timedelta(days=7))
            
            # Test VotingCondition condition
            voting_conditions = {c for c in rule.conditions if isinstance(c, VotingCondition)}
            self.assertEqual(len(voting_conditions), 1)
            votCond = next(iter(voting_conditions))
            self.assertEqual(votCond.name, "votCond")
            self.assertEqual(votCond.minVotes, 2)
            self.assertEqual(votCond.ratio, 0.7)

    def test_leader_driven_rule_creation(self):
        """Test the creation of a policy with a leader driven rule."""
        with open(self.test_cases_path / "valid_examples/leader_driven_policy.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.policy()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            policy = listener.get_policy()
            
            # Assertions
            self.assertIsInstance(policy, SinglePolicy)
            self.assertEqual(policy.name, "TestPolicy")
            
            # Test scope
            self.assertEqual(len(policy.scope), 1)
            scope = next(iter(policy.scope))
            self.assertIsInstance(scope, Activity)
            self.assertEqual(scope.name, "TestActivity")
            
            # Test rules count
            self.assertEqual(len(policy.rules), 2)
            
            # Test majority rule
            majority_rule = next(r for r in policy.rules if r.name == "majorityRule")
            self.assertIsInstance(majority_rule, MajorityRule)
            
            # Test leader driven rule
            leader_rule = next(r for r in policy.rules if r.name == "leaderRule")
            self.assertIsInstance(leader_rule, LeaderDrivenRule)
            self.assertEqual(leader_rule.default, majority_rule)
            
            # Test leader rule's conditions
            deadline_conditions = {c for c in leader_rule.conditions if isinstance(c, Deadline)}
            self.assertEqual(len(deadline_conditions), 1)
            deadline = next(iter(deadline_conditions))
            self.assertEqual(deadline.name, "reviewDeadline")
            self.assertEqual(deadline.offset, timedelta(days=7))
            
            # Test leader rule's participants
            self.assertEqual(len(leader_rule.participants), 1)
            participant = next(iter(leader_rule.participants))
            self.assertIsInstance(participant, Role)
            self.assertEqual(participant.name, "Leaders")

    def test_invalid_rule_reference(self):
        """Test the creation of a policy with an invalid rule reference."""
        with open(self.test_cases_path / "invalid_examples/invalid_rule_reference.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.policy()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            
            with self.assertRaises(UndefinedRuleException):
                walker.walk(listener, tree)

if __name__ == '__main__':
    unittest.main()