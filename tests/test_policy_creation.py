import unittest
from antlr4 import (
    InputStream, CommonTokenStream, ParseTreeWalker
)
from pathlib import Path
import io
from datetime import timedelta

from grammar.govdslLexer import govdslLexer
from grammar.govdslParser import govdslParser
from grammar.PolicyCreationListener import PolicyCreationListener
from grammar.govErrorListener import govErrorListener
from utils.exceptions import InvalidVotesException
from metamodel.governance import (
    Policy, Project, Activity, Task, Rule, MajorityRule, 
    Condition, Participant, Role, Deadline
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
        with open(self.test_cases_path / "valid_examples/majority_rule.txt", "r") as file:
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
            self.assertIsInstance(policy, Policy)
            self.assertEqual(policy.name, "TestPolicy")
            
            # Test scope
            self.assertEqual(len(policy.scope), 1)
            scope = next(iter(policy.scope))
            self.assertIsInstance(scope, Activity)
            self.assertEqual(scope.name, "TestActivity")
            
            # Test rules
            self.assertEqual(len(policy.rules), 1)
            rule = next(iter(policy.rules))
            self.assertIsInstance(rule, MajorityRule)
            self.assertEqual(rule.name, "majorityRule")
            self.assertEqual(rule.min_votes, 2)
            
            # Test rule's participants
            self.assertEqual(len(rule.participants), 1)
            participant = next(iter(rule.participants))
            self.assertIsInstance(participant, Role)
            self.assertEqual(participant.name, "Committers")
            
            # Test rule's conditions (deadline)
            self.assertEqual(len(rule.conditions), 1)
            deadline = next(iter(rule.conditions))
            self.assertIsInstance(deadline, Deadline)
            self.assertEqual(deadline.name, "reviewDeadline")
            self.assertEqual(deadline.ts, timedelta(days=7))
            
            # Check for parser errors
            self.assertEqual(len(self.error_listener.symbol), 0)

if __name__ == '__main__':
    unittest.main()