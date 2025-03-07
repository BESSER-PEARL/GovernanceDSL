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
    InvalidVotesException, UndefinedAttributeException, 
    EmptySetException
)
from metamodel.governance import (
    SinglePolicy, Activity, MajorityRule, Task, TaskTypeEnum,
    Role, Deadline, RatioMajorityRule, LeaderDrivenRule, VotingCondition,
    StatusEnum, PlatformEnum, Project, Individual
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
            self.assertEqual(len(policy.scopes), 2)
            scopes = list(policy.scopes)

            # Find and verify the Task scope
            task_scope = next((s for s in scopes if s.name == "TestTask"), None)
            self.assertIsNotNone(task_scope, "TestTask scope not found")
            self.assertIsInstance(task_scope, Task)
            self.assertEqual(task_scope.task_type, TaskTypeEnum.PULL_REQUEST)
            self.assertEqual(task_scope.status, StatusEnum.COMPLETED)

            # Find and verify the Project scope
            project_scope = next((s for s in scopes if s.name == "TestProjectGH"), None)
            self.assertIsNotNone(project_scope, "TestProjectGH scope not found")
            self.assertIsInstance(project_scope, Project)
            self.assertEqual(project_scope.platform, PlatformEnum.GITHUB)
            self.assertEqual(project_scope.project_id, "owner/repo")
            
            # Test rule content
            self.assertEqual(len(policy.rules), 1)
            rule = next(iter(policy.rules))
            self.assertIsInstance(rule, MajorityRule)
            self.assertEqual(rule.name, "majorityRule")
            
            # Test rule's participants
            self.assertEqual(len(rule.participants), 1)
            participant = next(iter(rule.participants))
            self.assertIsInstance(participant, Role)
            self.assertEqual(participant.name, "Maintainers")
            
            # Test rule's conditions
            self.assertEqual(len(rule.conditions), 2)
            
            # Test Deadline condition
            deadline_conditions = {c for c in rule.conditions if isinstance(c, Deadline)}
            self.assertEqual(len(deadline_conditions), 1)
            deadline = next(iter(deadline_conditions))
            self.assertEqual(deadline.name, "reviewDeadline")
            self.assertEqual(deadline.offset, timedelta(days=14))
            
            # Test VotingCondition condition
            voting_conditions = {c for c in rule.conditions if isinstance(c, VotingCondition)}
            self.assertEqual(len(voting_conditions), 1)
            vot_cond = next(iter(voting_conditions))
            self.assertEqual(vot_cond.name, "votCond")
            self.assertEqual(vot_cond.minVotes, 2)
            self.assertEqual(vot_cond.ratio, 1)
            
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
            self.assertEqual(len(policy.scopes), 2)
            scopes = list(policy.scopes)

            # Find and verify the Project scope
            project_scope = next((s for s in scopes if s.name == "TestProject"), None)
            self.assertIsNotNone(project_scope, "TestProject scope not found")
            self.assertIsInstance(project_scope, Project)
            self.assertEqual(project_scope.platform, PlatformEnum.GITHUB)
            self.assertEqual(project_scope.project_id, "owner/repo")

            # Find and verify the Activity scope
            activity_scope = next((s for s in scopes if s.name == "TestActivity"), None)
            self.assertIsNotNone(activity_scope, "TestActivity scope not found")
            self.assertIsInstance(activity_scope, Activity)
            
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
            self.assertEqual(len(policy.scopes), 3)
            scopes = list(policy.scopes)

            # Find and verify the Project scope
            project_scope = next((s for s in scopes if s.name == "TestProject"), None)
            self.assertIsNotNone(project_scope, "TestProject scope not found")
            self.assertIsInstance(project_scope, Project)
            self.assertEqual(project_scope.platform, PlatformEnum.GITHUB)
            self.assertEqual(project_scope.project_id, "owner/repo")

            # Find and verify the Activity scope
            activity_scope = next((s for s in scopes if s.name == "TestActivity"), None)
            self.assertIsNotNone(activity_scope, "TestActivity scope not found")
            self.assertIsInstance(activity_scope, Activity)

            # Find and verify the Task scope
            task_scope = next((s for s in scopes if s.name == "TestTask"), None)
            self.assertIsNotNone(task_scope, "TestTask scope not found")
            self.assertIsInstance(task_scope, Task)
            self.assertEqual(task_scope.task_type, TaskTypeEnum.PULL_REQUEST)
            self.assertEqual(task_scope.status, StatusEnum.COMPLETED)
            
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
            self.assertIsInstance(participant, Individual)
            self.assertEqual(participant.name, "Leader")

    def test_invalid_rule_reference(self):
        """Test the creation of a policy with an invalid rule reference."""
        with open(self.test_cases_path / "invalid_examples/invalid_rule_reference.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.policy()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            
            with self.assertRaises(UndefinedAttributeException):
                walker.walk(listener, tree)

if __name__ == '__main__':
    unittest.main()