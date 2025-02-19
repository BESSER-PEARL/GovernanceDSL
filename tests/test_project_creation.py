import unittest
from antlr4 import (
    InputStream, CommonTokenStream, ParseTreeWalker
)
from pathlib import Path
import io
from datetime import timedelta

from grammar.govdslLexer import govdslLexer
from grammar.govdslParser import govdslParser
from grammar.ProjectCreationListener import ProjectCreationListener
from grammar.govErrorListener import govErrorListener
from utils.exceptions import InvalidVotesException
from grammar.governance import (
    Project, Majority, RatioMajority, 
    LeaderDriven, Phased, Role, Deadline,
    CollaborationType, Stage, RangeType
)

class TestProjectCreation(unittest.TestCase):
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
        """Test the creation of a majority rule.
        This valid example contains a project with a single role, deadline, and rule.
        The rule is a majority rule that applies to a pull request in a task review stage.
        """
        with open(self.test_cases_path / "valid_examples/majority_rule.txt", "r") as file:
            text = file.read()
            
            # Setup parser and create model
            parser = self.setup_parser(text)
            tree = parser.project()
            self.assertIsNotNone(tree)
            
            listener = ProjectCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            project = listener.get_project()
            
            # Assertions
            self.assertIsInstance(project, Project)
            self.assertEqual(project.name, "TestProject")
            
            # Test roles
            self.assertEqual(len(project.roles), 1)
            role = next(iter(project.roles))
            self.assertIsInstance(role, Role)
            self.assertEqual(role.name, "Committers")
            
            # Test deadlines
            self.assertEqual(len(project.deadlines), 1)
            deadline = next(iter(project.deadlines))
            self.assertIsInstance(deadline, Deadline)
            self.assertEqual(deadline.name, "reviewDeadline")
            self.assertEqual(deadline.ts, timedelta(days=7))
            
            # Test rules
            self.assertEqual(len(project.rules), 1)
            rule = next(iter(project.rules))
            self.assertIsInstance(rule, Majority)
            self.assertEqual(rule.name, "majorityRule")
            self.assertEqual(rule.applied_to, CollaborationType.PULL_REQUEST)
            self.assertEqual(rule.stage, Stage.TASK_REVIEW)
            self.assertEqual(rule.range_type, RangeType.PRESENT)
            self.assertEqual(rule.min_votes, 2)
            self.assertEqual(len(rule.people), 1)
            self.assertEqual(next(iter(rule.people)).name, "Committers")
            self.assertEqual(rule.deadline.name, "reviewDeadline")
            
            # Check for parser errors
            self.assertEqual(len(self.error_listener.symbol), 0)

    def test_ratio_majority_rule_creation(self):
        """Test the creation of a ratio majority rule.
        This valid example contains a project with a single role, deadline, and rule.
        The rule is a ratio majority rule that applies to a pull request in a task review stage.
        """
        with open(self.test_cases_path / "valid_examples/ratio_majority_rule.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.project()
            
            listener = ProjectCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            project = listener.get_project()
            
            self.assertIsInstance(project, Project)
            rule = next(iter(project.rules))
            self.assertIsInstance(rule, RatioMajority)
            self.assertEqual(rule.ratio, 0.7)
            
            self.assertEqual(len(self.error_listener.symbol), 0)

    def test_leader_driven_rule_creation(self):
        """Test the creation of a leader driven rule.
        This valid example contains a project with a single role, deadline, and two rules.
        The rule is a leader driven rule that applies to a pull request in a task review stage.
        And it defaults to a majority rule.
        """
        with open(self.test_cases_path / "valid_examples/leader_driven_rule.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.project()
            
            listener = ProjectCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            project = listener.get_project()
            
            self.assertIsInstance(project, Project)
            rule = next(iter(project.rules))
            self.assertIsInstance(rule, LeaderDriven)
            self.assertIsNotNone(rule.default)
            
            self.assertEqual(len(self.error_listener.symbol), 0)

    def test_phased_rule_creation(self):
        """Test the creation of a phased rule.
        This valid example contains a project with a single role, deadline, and three
        rules, one of them a phased rule.
        The rule is a phased rule composed, in order, by the previous two rules."""
        with open(self.test_cases_path / "valid_examples/phased_rule.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.project()
            
            listener = ProjectCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            project = listener.get_project()
            
            self.assertIsInstance(project, Project)
            rule = next((r for r in project.rules if r.name == "phasedRule"), None)
            self.assertIsNotNone(rule)
            self.assertIsInstance(rule, Phased)
            self.assertTrue(len(rule.phases) > 0)
            
            self.assertEqual(len(self.error_listener.symbol), 0)

    def test_invalid_rule_reference(self):
        """Test the creation of a project with an invalid rule reference.
        This invalid example contains a project with a single role, deadline, and a  leaderDriven
        rule that defaults a non-existent rule."""
        with open(self.test_cases_path / "invalid_examples/invalid_rule_reference.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.project()
            
            listener = ProjectCreationListener()
            walker = ParseTreeWalker()
            
            with self.assertRaises(Exception):
                walker.walk(listener, tree)
    
    def test_invalid_num_votes(self):
        """Test the creation of a project with a majority rule with a negative (invalid) number of votes.
        This invalid example contains a project with a single role, deadline, and a majority rule
        that the minimum number of votes is negative."""
        with open(self.test_cases_path / "invalid_examples/invalid_num_votes.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.project()
            
            listener = ProjectCreationListener()
            walker = ParseTreeWalker()
            
            with self.assertRaises(InvalidVotesException):
                walker.walk(listener, tree)

if __name__ == '__main__':
    unittest.main()