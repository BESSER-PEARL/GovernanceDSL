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
    EmptySetException, InvalidValueException
)
from metamodel.governance import (
    SinglePolicy, Activity, Task, 
    Role, Deadline, MajorityPolicy, 
    StatusEnum, PlatformEnum, Project, Individual, PhasedPolicy, OrderEnum,
    AbsoluteMajorityPolicy, LeaderDrivenPolicy 
)
from utils.gh_extension import ActionEnum, PullRequest

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

    def test_majority_policy_creation(self):
        """Test the creation of a policy with majority voting parameters."""
        with open(self.test_cases_path / "valid_examples/majority_policy.txt", "r") as file:
            text = file.read()
            
            # Setup parser and create model
            parser = self.setup_parser(text)
            tree = parser.policy()
            self.assertIsNotNone(tree)
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            policy = listener.get_policy()
            
            # Assertions
            self.assertIsInstance(policy, MajorityPolicy)
            self.assertEqual(policy.name, "TestPolicy")
            
            # Test scope
            self.assertIsNotNone(policy.scope)
            scope = policy.scope
            self.assertIsInstance(scope, Project)
            self.assertEqual(scope.name, "TestProjectGH")
            self.assertEqual(scope.platform, PlatformEnum.GITHUB)
            self.assertEqual(scope.project_id, "owner/repo")
            
            # Test participants
            self.assertEqual(len(policy.participants), 2)
            
            # Test Individual participant
            individuals = {p for p in policy.participants if isinstance(p, Individual)}
            self.assertEqual(len(individuals), 1)
            individual = next(iter(individuals))
            self.assertEqual(individual.name, "Joe")
            self.assertEqual(individual.confidence, 0.7)
            
            # Test role assignment for individual
            self.assertIsNotNone(individual.role)
            self.assertEqual(individual.role.name, "Joe_Maintainer")
            
            # Test Role participant
            roles = {p for p in policy.participants if isinstance(p, Role)}
            self.assertEqual(len(roles), 1)
            role = next(iter(roles))
            self.assertEqual(role.name, "Maintainer")
            
            # Test conditions
            self.assertEqual(len(policy.conditions), 1)
            condition = next(iter(policy.conditions))
            self.assertIsInstance(condition, Deadline)
            self.assertEqual(condition.name, "reviewDeadline")
            self.assertEqual(condition.offset, timedelta(days=14))
            
            # Test voting parameters
            self.assertEqual(policy.minVotes, 2)
            self.assertEqual(policy.ratio, 0.5)
            
            # Check parser errors
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
                
    def test_invalid_confidence(self):
        """Test the creation of a policy with an individual having confidence value outside [0,1]."""
        with open(self.test_cases_path / "invalid_examples/invalid_confidence.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.policy()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            
            with self.assertRaises(InvalidValueException):
                walker.walk(listener, tree)

    def test_absolute_majority_policy_creation(self):
        """Test the creation of a policy with an absolute majority policy."""
        with open(self.test_cases_path / "valid_examples/absolute_majority_policy.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.policy()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            policy = listener.get_policy()
            
            # Assertions
            self.assertIsInstance(policy, AbsoluteMajorityPolicy)
            self.assertEqual(policy.name, "TestPolicy")
            
            # Test scope
            self.assertIsNotNone(policy.scope)
            scope = policy.scope
            self.assertIsInstance(scope, Project)
            self.assertEqual(scope.name, "TestProject")
            self.assertEqual(scope.platform, PlatformEnum.GITHUB)
            self.assertEqual(scope.project_id, "owner/repo")
            
            # Test participants
            self.assertEqual(len(policy.participants), 1)
            participant = next(iter(policy.participants))
            self.assertIsInstance(participant, Role)
            self.assertEqual(participant.name, "Committers")
            
            # Test conditions
            self.assertEqual(len(policy.conditions), 1)
            condition = next(iter(policy.conditions))
            self.assertIsInstance(condition, Deadline)
            self.assertEqual(condition.name, "reviewDeadline")
            self.assertEqual(condition.offset, timedelta(days=7))
            
            # Test voting parameters
            self.assertEqual(policy.minVotes, 2)
            self.assertEqual(policy.ratio, 0.7)

    def test_leader_driven_policy_creation(self):
        """Test the creation of a policy with a leader driven policy."""
        with open(self.test_cases_path / "valid_examples/leader_driven_policy.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.policy()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            policy = listener.get_policy()
            
            # Assertions
            self.assertIsInstance(policy, LeaderDrivenPolicy)
            self.assertEqual(policy.name, "TestPolicy")
            
            # Test scope
            self.assertIsNotNone(policy.scope)
            scope = policy.scope
            self.assertIsInstance(scope, Project)
            self.assertEqual(scope.name, "TestProject")
            self.assertEqual(scope.platform, PlatformEnum.GITHUB)
            self.assertEqual(scope.project_id, "owner/repo")
            
            # Test leader participants
            self.assertEqual(len(policy.participants), 1)
            participant = next(iter(policy.participants))
            self.assertIsInstance(participant, Individual)
            self.assertEqual(participant.name, "Leader")
            
            # Test conditions
            self.assertEqual(len(policy.conditions), 1)
            condition = next(iter(policy.conditions))
            self.assertIsInstance(condition, Deadline)
            self.assertEqual(condition.name, "reviewDeadline")
            self.assertEqual(condition.offset, timedelta(days=7))
            
            # Test default policy
            self.assertIsNotNone(policy.default)
            default_policy = policy.default
            self.assertIsInstance(default_policy, MajorityPolicy)
            self.assertEqual(default_policy.name, "defaultPolicy")
            
            # Test default policy participants
            self.assertEqual(len(default_policy.participants), 1)
            default_participant = next(iter(default_policy.participants))
            self.assertIsInstance(default_participant, Role)
            self.assertEqual(default_participant.name, "Maintainers")
            
            # Test default policy conditions
            self.assertEqual(len(default_policy.conditions), 1)
            default_condition = next(iter(default_policy.conditions))
            self.assertIsInstance(default_condition, Deadline)
            self.assertEqual(default_condition.name, "reviewDeadline")
            self.assertEqual(default_condition.offset, timedelta(days=7))

            # Test default policy scope
            self.assertIsNotNone(default_policy.scope)
            scope = default_policy.scope
            self.assertIsInstance(scope, Project)
            self.assertEqual(scope.name, "TestProject")
            self.assertEqual(scope.platform, PlatformEnum.GITHUB)
            self.assertEqual(scope.project_id, "owner/repo")
            
            # Test default policy parameters
            self.assertEqual(default_policy.minVotes, 2)

    def test_phased_policy_creation(self):
        """Test the creation of a phased policy. Based on the HFC governance policy."""
        with open(self.test_cases_path / "valid_examples/hfc_governance.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.policy()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            policy = listener.get_policy()
            
            # Assertions
            self.assertIsInstance(policy, PhasedPolicy)
            self.assertEqual(policy.name, "phasedPolicy")
            self.assertEqual(policy.order, OrderEnum.SEQUENTIAL_EXCLUSIVE)
            
            # Test phases count
            self.assertEqual(len(policy.phases), 2)
            phases = list(policy.phases)
            
            # Test first phase
            phase_1 = next((p for p in phases if p.name == "phase_1"), None)
            self.assertIsNotNone(phase_1, "Phase 1 not found")
            self.assertIsInstance(phase_1, MajorityPolicy)
            
            # Test phase 1 scope
            self.assertIsNotNone(phase_1.scope)
            task_scope = phase_1.scope
            self.assertIsInstance(task_scope, PullRequest)
            self.assertEqual(task_scope.name, "TestTask")
            self.assertEqual(task_scope.action, ActionEnum.MERGE)
            # Check for labels
            self.assertIsNone(task_scope.labels)
            
            # Test phase 1 participants
            self.assertEqual(len(phase_1.participants), 1)
            participant = next(iter(phase_1.participants))
            self.assertIsInstance(participant, Role)
            self.assertEqual(participant.name, "Maintainers")
            
            # Test phase 1 conditions
            self.assertEqual(len(phase_1.conditions), 1)
            deadline = next(iter(phase_1.conditions))
            self.assertIsInstance(deadline, Deadline)
            self.assertEqual(deadline.name, "reviewDeadline")
            self.assertEqual(deadline.offset, timedelta(days=14))
            
            # Test phase 1 voting parameters
            self.assertEqual(phase_1.minVotes, 2)
            self.assertEqual(phase_1.ratio, 1.0)
            
            # Test second phase
            phase_2 = next((p for p in phases if p.name == "phase_2"), None)
            self.assertIsNotNone(phase_2, "Phase 2 not found")
            self.assertIsInstance(phase_2, MajorityPolicy)
            
            # Test phase 2 scope
            self.assertIsNotNone(phase_2.scope)
            task_scope = phase_2.scope
            self.assertIsInstance(task_scope, PullRequest)
            self.assertEqual(task_scope.name, "TestTask")
            self.assertEqual(task_scope.action, ActionEnum.MERGE)
            # Check for labels
            self.assertIsNone(task_scope.labels)
            
            # Test phase 2 participants
            self.assertEqual(len(phase_2.participants), 1)
            participant = next(iter(phase_2.participants))
            self.assertIsInstance(participant, Role)
            self.assertEqual(participant.name, "Maintainers")
            
            # Test phase 2 conditions (none in this phase)
            self.assertEqual(len(phase_2.conditions), 0)
            
            # Test phase 2 voting parameters
            self.assertEqual(phase_2.minVotes, 1)
            self.assertEqual(phase_2.ratio, 1.0)

if __name__ == '__main__':
    unittest.main()