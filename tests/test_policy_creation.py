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
    InvalidParticipantException, UndefinedAttributeException, 
    InvalidValueException
)
from metamodel.governance import (
    Role, Deadline, MajorityPolicy, Task,
    Individual, ComposedPolicy,
    AbsoluteMajorityPolicy, LeaderDrivenPolicy, ParticipantExclusion, EvaluationMode,
    LazyConsensusPolicy, MinimumParticipant, VetoRight, 
    Activity, BooleanDecision, StringList, ElementList
)
from utils.gh_extension import (
    ActionEnum, PullRequest, Repository, Patch, PassedTests,
    Label, LabelCondition
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

    def test_invalid_num_votes(self):
        """Test the creation of a policy with a majority rule having negative votes."""
        with open(self.test_cases_path / "invalid_examples/invalid_num_votes.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.governance()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            
            with self.assertRaises(InvalidParticipantException) as raised_exception:
                walker.walk(listener, tree)
            
            exception_message = str(raised_exception.exception)
            print(f"\nException message: {exception_message}")
                
    def test_invalid_vote_value(self):
        """Test the creation of a policy with an individual having vote value outside allowed range."""
        with open(self.test_cases_path / "invalid_examples/invalid_vote_value.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.governance()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            
            with self.assertRaises(InvalidValueException) as raised_exception:
                walker.walk(listener, tree)

            exception_message = str(raised_exception.exception)
            print(f"\nException message: {exception_message}")

    def test_invalid_consensus_with_parameters(self):
        """Test the creation of a consensus policy having parameters."""
        with open(self.test_cases_path / "invalid_examples/consensus_with_parameters.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.governance()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            
            with self.assertRaises(UndefinedAttributeException) as raised_exception:
                walker.walk(listener, tree)

            exception_message = str(raised_exception.exception)
            print(f"\nException message: {exception_message}")

    def test_invalid_element_list(self):
        """Test MajorityPolicy with DecisionType as ElementList referencing undefined individuals."""
        with open(self.test_cases_path / "invalid_examples/invalid_element_list.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.governance()
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            with self.assertRaises(UndefinedAttributeException) as raised_exception:
                walker.walk(listener, tree)
            exception_message = str(raised_exception.exception)
            print(f"\nException message: {exception_message}")

    def test_majority_policy_creation(self):
        """Test the creation of a policy with majority voting parameters."""
        with open(self.test_cases_path / "valid_examples/basic_examples/majority_policy.txt", "r") as file:
            text = file.read()
            
            # Setup parser and create model
            parser = self.setup_parser(text)
            tree = parser.governance()
            self.assertIsNotNone(tree)
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            policy = listener.get_policy()
            
            # Assertions
            self.assertIsInstance(policy, MajorityPolicy)
            self.assertEqual(policy.name, "TestPolicy")

            # DecisionType (now StringList)
            self.assertIsNotNone(policy.decision_type)
            self.assertIsInstance(policy.decision_type, StringList)
            self.assertEqual(policy.decision_type.name, "stringList")
            self.assertSetEqual(policy.decision_type.options, {"accept", "reject", "abstain"})
            
            # Test scope
            self.assertIsNotNone(policy.scope)
            scope = policy.scope
            self.assertIsInstance(scope, Patch)
            self.assertEqual(scope.name, "myTask")
            self.assertEqual(scope.action, ActionEnum.MERGE)
            activity_scope = scope.activity
            self.assertIsInstance(activity_scope, Activity)
            self.assertEqual(activity_scope.name, "myActivity")
            project_scope = activity_scope.project 
            self.assertIsInstance(project_scope, Repository)
            self.assertEqual(project_scope.name, "TestProjectGH")
            self.assertEqual(project_scope.repo_id, "owner/repo-with-hyphen")
            
            # Test participants
            self.assertEqual(len(policy.participants), 4) 
            
            # Test Individual participant
            individuals = [p for p in policy.participants if isinstance(p, Individual)]
            self.assertEqual(len(individuals), 2)
            # Individuals are not ordered
            individual = next((ind for ind in individuals if ind.name == "Joe"), None)
            self.assertIsNotNone(individual, "Joe not found")
            self.assertEqual(individual.name, "Joe")
            self.assertEqual(individual.vote_value, 0.7)
            self.assertIsNotNone(individual.role_assignement)
            self.assertEqual(individual.role_assignement.name, "Joe_Maintainer")
            profile = individual.profile
            self.assertIsNotNone(profile)
            self.assertEqual(profile.name, "joeProfile")
            self.assertEqual(profile.gender, "male")
            self.assertEqual(profile.race, "hispanic")

            agent = next((ind for ind in individuals if ind.name == "Mike"), None)
            self.assertIsNotNone(agent, "Mike not found")
            self.assertEqual(agent.name, "Mike")
            self.assertEqual(agent.vote_value, 1.0) # This is the default value
            self.assertEqual(agent.confidence, 0.8)
            self.assertIsNotNone(agent.role_assignement)
            self.assertEqual(agent.role_assignement.name, "Mike_Maintainer")
            
            
            # Test Role participants
            roles = [p for p in policy.participants if isinstance(p, Role)]
            self.assertEqual(len(roles), 2)
            
            # Test Maintainer role
            maintainer_role = next((r for r in roles if r.name == "Maintainer"), None)
            self.assertIsNotNone(maintainer_role, "Maintainer role not found")
            self.assertEqual(maintainer_role.name, "Maintainer")
            
            # Test Reviewer role with composed individuals
            reviewer_role = next((r for r in roles if r.name == "Reviewer"), None)
            self.assertIsNotNone(reviewer_role, "Reviewer role not found")
            self.assertEqual(reviewer_role.name, "Reviewer")
            
            # Check the individuals composed in the Reviewer role
            self.assertIsNotNone(reviewer_role.individuals, "Reviewer role should have individuals")
            self.assertEqual(len(reviewer_role.individuals), 2, "Reviewer should have 2 individuals")
            
            # Check individual members of the Reviewer role
            individuals_names = {ind.name for ind in reviewer_role.individuals}
            self.assertIn("Mike", individuals_names, "Mike should be in Reviewer role")
            self.assertIn("Alexander", individuals_names, "Alexander should be in Reviewer role")
            
            # Test conditions
            self.assertEqual(len(policy.conditions), 5)
            
            # Find and test Deadline condition
            deadline_conditions = {c for c in policy.conditions if isinstance(c, Deadline)}
            self.assertEqual(len(deadline_conditions), 1)
            deadline = next(iter(deadline_conditions))
            self.assertEqual(deadline.name, "reviewDeadline")
            self.assertEqual(deadline.offset, timedelta(days=14))
            
            # Find and test ParticipantExclusion condition
            exclusion_conditions = {c for c in policy.conditions if isinstance(c, ParticipantExclusion)}
            self.assertEqual(len(exclusion_conditions), 1)
            exclusion = next(iter(exclusion_conditions))
            self.assertEqual(exclusion.name, "partExcl")
            excluded_participants = exclusion.excluded
            self.assertEqual(len(excluded_participants), 1)
            self.assertIsInstance(excluded_participants, set)
            excluded_participant = next(iter(excluded_participants))
            self.assertIsInstance(excluded_participant, Individual)
            self.assertEqual(excluded_participant.name, "Mike")

            # Find and test MinimumParticipant condition
            min_part_conditions = {c for c in policy.conditions if isinstance(c, MinimumParticipant)}
            self.assertEqual(len(min_part_conditions), 1)
            min_part = next(iter(min_part_conditions))
            self.assertEqual(min_part.name, "minParticipantsCondition")
            self.assertEqual(min_part.min_participants, 2)

            # Find and test LabelCondition condition
            label_conditions = [c for c in policy.conditions if isinstance(c, LabelCondition)]
            self.assertEqual(len(label_conditions), 2)
            lc_1 = next(lc for lc in label_conditions if lc.evaluation_mode == EvaluationMode.PRE)
            self.assertEqual(lc_1.name, "labelCondition")
            self.assertIsInstance(lc_1, LabelCondition)
            self.assertEqual(lc_1.evaluation_mode, EvaluationMode.PRE)
            self.assertEqual(lc_1.inclusion, False)
            self.assertEqual(next(iter(lc_1.labels)).name, "Label1")
            lc_2 = next(lc for lc in label_conditions if lc.evaluation_mode == EvaluationMode.CONCURRENT)
            self.assertEqual(lc_2.name, "labelCondition")
            self.assertIsInstance(lc_2, LabelCondition)
            self.assertEqual(next(iter(lc_2.labels)).name, "Label2")
            self.assertEqual(lc_2.evaluation_mode, EvaluationMode.CONCURRENT)
            self.assertEqual(lc_2.inclusion, True)
            
            # Test voting parameters
            self.assertEqual(policy.ratio, 0.5)
            
            # Check parser errors
            self.assertEqual(len(self.error_listener.symbol), 0)

    def test_majority_policy_with_veto_right_creation(self):
        """Test the creation of a policy with a veto right condition."""
        with open(self.test_cases_path / "valid_examples/basic_examples/maj_with_veto_right.txt", "r") as file:
            text = file.read()
            
            # Setup parser and create model
            parser = self.setup_parser(text)
            tree = parser.governance()
            self.assertIsNotNone(tree)
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            policy = listener.get_policy()
            
            # Assertions
            self.assertIsInstance(policy, MajorityPolicy)
            self.assertEqual(policy.name, "TestPolicy")

            # DecisionType (ElementList)
            self.assertIsNotNone(policy.decision_type)
            self.assertIsInstance(policy.decision_type, ElementList)
            self.assertEqual(policy.decision_type.name, "elementList")
            self.assertSetEqual({ind.name for ind in policy.decision_type.elements}, {"Joe", "George"})
            
            # Test scope
            self.assertIsNotNone(policy.scope)
            scope = policy.scope
            self.assertIsInstance(scope, Task)
            self.assertEqual(scope.name, "myTask")
            
            # Test participants
            self.assertEqual(len(policy.participants), 2)
            
            # Test Role participant
            participant = [p for p in policy.participants if isinstance(p, Role)]
            self.assertEqual(len(participant), 1)
            self.assertIsInstance(participant[0], Role)
            self.assertEqual(participant[0].name, "Maintainer")

            individual = [p for p in policy.participants if isinstance(p, Individual)]
            self.assertEqual(len(individual), 1)
            self.assertIsInstance(individual[0], Individual)
            self.assertEqual(individual[0].name, "Mike")
            self.assertEqual(individual[0].profile.name, "mikeProfile")
            self.assertEqual(individual[0].profile.race, "caucasian")
            
            # Test conditions
            self.assertEqual(len(policy.conditions), 1)
            
            # Find and test VetoRight condition
            condition = next(iter(policy.conditions))
            self.assertIsInstance(condition, VetoRight)
            self.assertEqual(condition.name, "VetoRightCondition")
            
            # Verify vetoers set
            self.assertEqual(len(condition.vetoers), 2)
            po = next((v for v in condition.vetoers if v.name == "ProjectOwner"), None)
            self.assertIsInstance(po, Individual)
            self.assertEqual(po.name, "ProjectOwner")
            # We check the default creation of individuals
            diego = next((v for v in condition.vetoers if v.name == "Diego"), None)
            self.assertIsInstance(diego, Individual)
            self.assertEqual(diego.name, "Diego")

            
            # Check parser errors
            self.assertEqual(len(self.error_listener.symbol), 0)

    def test_absolute_majority_policy_creation(self):
        """Test the creation of a policy with an absolute majority policy."""
        with open(self.test_cases_path / "valid_examples/basic_examples/absolute_majority_policy.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.governance()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            policy = listener.get_policy()
            
            # Assertions
            self.assertIsInstance(policy, AbsoluteMajorityPolicy)
            self.assertEqual(policy.name, "TestPolicy")

            # DecisionType check
            self.assertIsNotNone(policy.decision_type)
            self.assertIsInstance(policy.decision_type, BooleanDecision)
            self.assertEqual(policy.decision_type.name, "booleanDecision")
            
            # Test scope
            self.assertIsNotNone(policy.scope)
            scope = policy.scope
            self.assertIsInstance(scope, Repository)
            self.assertEqual(scope.name, "TestProject")
            self.assertEqual(scope.repo_id, "owner/repo")
            
            # Test participants
            self.assertEqual(len(policy.participants), 1)
            participant = next(iter(policy.participants))
            self.assertIsInstance(participant, Role)
            self.assertEqual(participant.name, "Committers")
            
            # Test conditions
            self.assertEqual(len(policy.conditions), 2)

            # Find and test Deadline condition
            deadline_conditions = {c for c in policy.conditions if isinstance(c, Deadline)}
            deadline = next(iter(deadline_conditions))
            self.assertIsInstance(deadline, Deadline)
            self.assertEqual(deadline.name, "reviewDeadline")
            self.assertEqual(deadline.offset, timedelta(days=7))

            # Find and test PassedTests condition
            passed_tests_conditions = {c for c in policy.conditions if isinstance(c, PassedTests)}
            passed_tests = next(iter(passed_tests_conditions))
            self.assertIsInstance(passed_tests, PassedTests)
            self.assertEqual(passed_tests.name, "passedTestsCondition")
            # Add check for evaluation_mode
            self.assertEqual(passed_tests.evaluation_mode, EvaluationMode.PRE)

            # Test voting parameters
            self.assertEqual(policy.ratio, 0.7)

            # Check parser errors
            self.assertEqual(len(self.error_listener.symbol), 0)

    def test_leader_driven_policy_creation(self):
        """Test the creation of a policy with a leader driven policy."""
        with open(self.test_cases_path / "valid_examples/basic_examples/leader_driven_policy.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.governance()
            
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
            self.assertIsInstance(scope, Repository)
            self.assertEqual(scope.name, "TestProject")
            self.assertEqual(scope.repo_id, "owner/repo")
            
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
            self.assertIsInstance(scope, Repository)
            self.assertEqual(scope.name, "TestProject")
            self.assertEqual(scope.repo_id, "owner/repo")

            # Check parser errors
            self.assertEqual(len(self.error_listener.symbol), 0)

    def test_leader_driven_no_default_policy_creation(self):
        """Test the creation of a policy with a leader driven policy without a default policy."""
        with open(self.test_cases_path / "valid_examples/basic_examples/leader_driven_no_default.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.governance()
            
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
            self.assertIsInstance(scope, Activity)
            self.assertEqual(scope.name, "myActivity")
            
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
            self.assertIsNone(policy.default)

            # Check parser errors
            self.assertEqual(len(self.error_listener.symbol), 0)


    def test_composed_policy_creation(self):
        """Test the creation of a composed policy. Based on the HFC governance policy."""
        with open(self.test_cases_path / "valid_examples/real_world/hfc_governance.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.governance()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            policy = listener.get_policy()
            
            # Assertions
            self.assertIsInstance(policy, ComposedPolicy)
            self.assertEqual(policy.name, "phasedPolicy")
            
            # Test scope
            self.assertIsNotNone(policy.scope)
            scope = policy.scope
            self.assertIsInstance(scope, Patch)
            self.assertEqual(scope.name, "TestTask")
            self.assertEqual(scope.action, ActionEnum.MERGE)
            # Test the relationship with activity
            activity_scope = scope.activity
            self.assertIsNotNone(activity_scope)
            self.assertIsInstance(activity_scope, Activity)
            self.assertEqual(activity_scope.name, "TestActivity")
            # Test the relationship with project
            project_scope = activity_scope.project
            self.assertIsNotNone(project_scope)
            self.assertIsInstance(project_scope, Repository)
            self.assertEqual(project_scope.name, "HFCProject")
            
            # Test order properties
            self.assertTrue(policy.sequential, "Policy should be sequential")
            self.assertFalse(policy.require_all, "Policy should not require all phases to pass")
            self.assertTrue(policy.carry_over, "Policy should carry over results between phases")
            
            # Test phases count
            self.assertEqual(len(policy.phases), 2)
            
            # Test phases order - new test for order preservation
            self.assertEqual(policy.phases[0].name, "phase_1", "First phase should be phase_1")
            self.assertEqual(policy.phases[1].name, "phase_2", "Second phase should be phase_2")
            
            # Test first phase
            phase_1 = policy.phases[0]
            self.assertIsNotNone(phase_1, "Phase 1 not found")
            self.assertIsInstance(phase_1, MajorityPolicy)
            
            # Test phase 1 scope
            self.assertIsNotNone(phase_1.scope)
            task_scope = phase_1.scope
            self.assertIsInstance(task_scope, Patch)
            self.assertEqual(task_scope.name, "TestTask")
            self.assertEqual(task_scope.action, ActionEnum.MERGE)
            # Test the relationship with activity
            activity_scope = task_scope.activity
            self.assertIsNotNone(activity_scope)
            self.assertIsInstance(activity_scope, Activity)
            self.assertEqual(activity_scope.name, "TestActivity")
            # Test the relationship with project
            project_scope = activity_scope.project
            self.assertIsNotNone(project_scope)
            self.assertIsInstance(project_scope, Repository)
            self.assertEqual(project_scope.name, "HFCProject")
            # Check the GitHub element
            self.assertIsNotNone(task_scope.element)
            self.assertIsInstance(task_scope.element, PullRequest)
            self.assertEqual(task_scope.element.name, "TestTask")
            # Check for labels
            self.assertIsNone(task_scope.element.labels)

            # Test phase 1 parent
            self.assertIsNotNone(phase_1.parent)
            self.assertIsInstance(phase_1.parent, ComposedPolicy)
            self.assertEqual(phase_1.parent.name, "phasedPolicy")
            
            # Test phase 1 participants
            self.assertEqual(len(phase_1.participants), 1)
            participant = next(iter(phase_1.participants))
            self.assertIsInstance(participant, Role)
            self.assertEqual(participant.name, "Maintainers")
            
            # Test phase 1 conditions
            self.assertEqual(len(phase_1.conditions), 2)

            # Find and test Deadline condition
            deadline_conditions = {c for c in phase_1.conditions if isinstance(c, Deadline)}
            deadline = next(iter(deadline_conditions))
            self.assertIsInstance(deadline, Deadline)
            self.assertEqual(deadline.name, "reviewDeadline")
            self.assertEqual(deadline.offset, timedelta(days=14))

            # Find and test MinimumParticipant condition
            min_part_conditions = {c for c in phase_1.conditions if isinstance(c, MinimumParticipant)}
            self.assertEqual(len(min_part_conditions), 1)
            min_part = next(iter(min_part_conditions))
            self.assertEqual(min_part.name, "minParticipantsCondition")
            self.assertEqual(min_part.min_participants, 2)
            
            # Test phase 1 voting parameters
            self.assertEqual(phase_1.ratio, 1.0)
            
            # Test second phase
            phase_2 = policy.phases[1]
            self.assertIsNotNone(phase_2, "Phase 2 not found")
            self.assertIsInstance(phase_2, MajorityPolicy)
            
            # Test phase 2 scope
            self.assertIsNotNone(phase_2.scope)
            task_scope = phase_2.scope
            self.assertIsInstance(task_scope, Patch)
            self.assertEqual(task_scope.name, "TestTask")
            self.assertEqual(task_scope.action, ActionEnum.MERGE)
            # Test the relationship with activity
            activity_scope = task_scope.activity
            self.assertIsNotNone(activity_scope)
            self.assertIsInstance(activity_scope, Activity)
            self.assertEqual(activity_scope.name, "TestActivity")
            # Test the relationship with project
            project_scope = activity_scope.project
            self.assertIsNotNone(project_scope)
            self.assertIsInstance(project_scope, Repository)
            self.assertEqual(project_scope.name, "HFCProject")
            # Check the GitHub element
            self.assertIsNotNone(task_scope.element)
            self.assertIsInstance(task_scope.element, PullRequest)
            self.assertEqual(task_scope.element.name, "TestTask")
            # Check for labels
            self.assertIsNone(task_scope.element.labels)

            # Test phase 2 parent
            self.assertIsNotNone(phase_2.parent)
            self.assertIsInstance(phase_2.parent, ComposedPolicy)
            self.assertEqual(phase_2.parent.name, "phasedPolicy")
            
            # Test phase 2 participants
            self.assertEqual(len(phase_2.participants), 1)
            participant = next(iter(phase_2.participants))
            self.assertIsInstance(participant, Role)
            self.assertEqual(participant.name, "Maintainers")
            
            # Test phase 2 conditions
            self.assertEqual(len(phase_2.conditions), 1)
            min_part = next(iter(phase_2.conditions))
            self.assertIsInstance(min_part, MinimumParticipant)
            self.assertEqual(min_part.name, "minParticipantsCondition")
            self.assertEqual(min_part.min_participants, 1)
            
            # Test phase 2 voting parameters
            self.assertEqual(phase_2.ratio, 1.0)

            # Check parser errors
            self.assertEqual(len(self.error_listener.symbol), 0)

    def test_lazy_consensus_policy_creation(self):
        """Test the creation of a policy with a consensus voting."""
        with open(self.test_cases_path / "valid_examples/basic_examples/lazy_consensus_policy.txt", "r") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.governance()
            
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            policy = listener.get_policy()
            
            # Assertions
            self.assertIsInstance(policy, LazyConsensusPolicy)
            self.assertEqual(policy.name, "TestPolicy")
            
            # Test scope
            self.assertIsNotNone(policy.scope)
            scope = policy.scope
            self.assertIsInstance(scope, Repository)
            self.assertEqual(scope.name, "TestProject")
            self.assertEqual(scope.repo_id, "owner/repo")
            
            # Test participants
            self.assertEqual(len(policy.participants), 1)
            
            # Test Role participant
            roles = {p for p in policy.participants if isinstance(p, Role)}
            self.assertEqual(len(roles), 1)
            role = next(iter(roles))
            self.assertEqual(role.name, "Maintainer")
            
            # Test conditions (none in this policy)
            self.assertEqual(len(policy.conditions), 0)

            # Check parser errors
            self.assertEqual(len(self.error_listener.symbol), 0)

    def test_custom_example(self):
        with open(self.test_cases_path / "valid_examples/basic_examples/custom_example.txt") as file:
            text = file.read()
            parser = self.setup_parser(text)
            tree = parser.governance()
            listener = PolicyCreationListener()
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            policy = listener.get_policy()

            # Assertions
            self.assertIsInstance(policy, MajorityPolicy)
            self.assertEqual(policy.name, "TestPolicy")

            # DecisionType (BooleanDecision)
            self.assertIsNotNone(policy.decision_type)
            self.assertIsInstance(policy.decision_type, BooleanDecision)
            self.assertEqual(policy.decision_type.name, "booleanDecision")

            # Test scope
            self.assertIsNotNone(policy.scope)
            scope = policy.scope
            self.assertIsInstance(scope, Patch)
            self.assertEqual(scope.name, "TestTask")
            self.assertEqual(scope.action, ActionEnum.MERGE)
            activity_scope = scope.activity
            self.assertIsInstance(activity_scope, Activity)
            self.assertEqual(activity_scope.name, "TestActivity")
            project_scope = activity_scope.project
            self.assertIsInstance(project_scope, Repository)
            self.assertEqual(project_scope.name, "TestProjectGH")
            self.assertEqual(project_scope.repo_id, "owner/repo")

            # Test participants
            self.assertEqual(len(policy.participants), 2)
            individuals = [p for p in policy.participants if isinstance(p, Individual)]
            roles = [p for p in policy.participants if isinstance(p, Role)]
            self.assertEqual(len(individuals), 1)
            self.assertEqual(len(roles), 1)
            individual = individuals[0]
            self.assertEqual(individual.name, "Zoe")
            self.assertEqual(individual.vote_value, 0.7)
            self.assertIsNotNone(individual.role_assignement)
            self.assertEqual(individual.role_assignement.name, "Zoe_Maintainer")
            role = roles[0]
            self.assertEqual(role.name, "Maintainer")

            # Test conditions
            self.assertEqual(len(policy.conditions), 1)
            deadline = next(iter(policy.conditions))
            self.assertIsInstance(deadline, Deadline)
            self.assertEqual(deadline.name, "reviewDeadline")
            self.assertEqual(deadline.offset, timedelta(days=14))

            # Test voting parameters
            self.assertEqual(policy.ratio, 0.5)

            # Check parser errors
            self.assertEqual(len(self.error_listener.symbol), 0)


if __name__ == '__main__':
    unittest.main()