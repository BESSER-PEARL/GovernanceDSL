"""
Governance DSL Form Builder
A Gradio-based interface for creating governance policies through forms
"""

import gradio as gr
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class GovernanceFormBuilder:
    def __init__(self):
        self.form_data = {
            'scopes': {},
            'participants': {},
            'policies': {}
        }
        # Track added conditions for current policy being edited
        self.current_policy_conditions = []
        
    def create_interface(self):
        """Create the main Gradio interface"""
        with gr.Blocks(
            title="Governance Policy Builder",
            theme=gr.themes.Soft(),
            css="""
            .main-container { max-width: 1200px; margin: auto; }
            .form-section { padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; margin: 10px 0; }
            .preview-panel { background-color: #f8f9fa; padding: 15px; border-radius: 8px; }
            """
        ) as interface:
            
            gr.Markdown("# 🏛️ Governance Policy Builder")
            gr.Markdown("Define governance rules for your software project using an intuitive form interface.")
            
            # State to store form data across tabs
            form_state = gr.State(self.form_data)
            
            with gr.Row():
                with gr.Column(scale=3, elem_classes=["main-container"]):
                    with gr.Tabs():
                        with gr.Tab("🎯 Scopes", id="scopes"):
                            scope_components = self._create_scope_forms()
                            
                        with gr.Tab("👥 Participants", id="participants"):
                            participant_components = self._create_participant_forms()
                            
                        with gr.Tab("📋 Policies", id="policies"):
                            policy_components = self._create_policy_forms()
                            
                with gr.Column(scale=2):
                    self._create_preview_panel()
            
            # Update handlers
            self._setup_event_handlers(scope_components, participant_components, policy_components, form_state)
            
        return interface
    
    def _create_scope_forms(self):
        """Create forms for defining scopes (Projects, Activities, Tasks)"""
        gr.Markdown("## Define Project Scopes")
        gr.Markdown("Set up the organizational structure of your project.")
        
        with gr.Accordion("Projects", open=True):
            gr.Markdown("### Define Projects")
            gr.Markdown("*Format: One per line as `ProjectName | Platform | Repository`*")
            gr.Markdown("*Platform and Repository are optional. Examples:*")
            gr.Markdown("- `MyProject` (no platform/repo)")
            gr.Markdown("- `K8sProject | GitHub | kubernetes/kubernetes`")
            
            projects_text = gr.Textbox(
                label="Projects",
                placeholder="MyProject | GitHub | owner/repo\nAnotherProject",
                lines=3,
                info="Define multiple projects, one per line"
            )
        
        with gr.Accordion("Activities", open=False):
            gr.Markdown("### Define Activities")
            gr.Markdown("*Format: One per line as `ActivityName | ParentProject` (ParentProject is optional)*")
            gr.Markdown("*Examples:*")
            gr.Markdown("- `CodeReview` (root-level activity)")
            gr.Markdown("- `TestActivity | MyProject` (belongs to MyProject)")
            
            activities_text = gr.Textbox(
                label="Activities",
                placeholder="CodeReview\nTestActivity | MyProject",
                lines=3,
                info="Define multiple activities, one per line"
            )
            
        with gr.Accordion("Tasks", open=False):
            gr.Markdown("### Define Tasks")
            gr.Markdown("*Format: One per line as `TaskName | Parent | Type | Action`*")
            gr.Markdown("*Parent, Type, and Action are optional. Examples:*")
            gr.Markdown("- `MergeTask` (minimal task)")
            gr.Markdown("- `PRMerge | CodeReview` (task with parent)")
            gr.Markdown("- `PRMerge | CodeReview | Pull request | merge` (full definition)")
            
            tasks_text = gr.Textbox(
                label="Tasks",
                placeholder="MergeTask\nPRMerge | CodeReview\nFullTask | CodeReview | Pull request | merge",
                lines=4,
                info="Define multiple tasks, one per line"
            )
        
        return {
            'projects_text': projects_text,
            'activities_text': activities_text,
            'tasks_text': tasks_text
        }
    
    def _create_participant_forms(self):
        """Create forms for defining participants (Roles, Individuals, Agents)"""
        gr.Markdown("## Define Participants")
        gr.Markdown("Set up the people and roles involved in governance decisions.")
        
        with gr.Accordion("Profiles", open=True):
            gr.Markdown("### Define Profiles")
            gr.Markdown("*Create diversity profiles for tracking inclusive governance*")
            gr.Markdown("*Both gender and race are optional - you can define profiles with just one attribute or both*")
            
            with gr.Row():
                profile_name = gr.Textbox(
                    label="Profile Name",
                    placeholder="e.g., diverse_profile, senior_dev_profile",
                    info="Unique name for this profile"
                )
                
            with gr.Row():
                profile_gender = gr.Dropdown(
                    label="Gender (Optional)",
                    choices=["", "male", "female", "non-binary", "other"],
                    value="",
                    allow_custom_value=True,
                    info="Leave empty if not applicable"
                )
                
                profile_race = gr.Dropdown(
                    label="Race/Ethnicity (Optional)", 
                    choices=["", "asian", "black", "hispanic", "white", "mixed", "other"],
                    value="",
                    allow_custom_value=True,
                    info="Leave empty if not applicable"
                )
            
            with gr.Row():
                add_profile_btn = gr.Button("➕ Add Profile", variant="secondary")
                clear_profiles_btn = gr.Button("🗑️ Clear All", variant="secondary")
            
            # Display added profiles
            profiles_display = gr.Textbox(
                label="Added Profiles",
                lines=4,
                interactive=False,
                placeholder="No profiles added yet. Remember: profiles must have at least gender OR race defined.",
                info="Profiles you've added will appear here"
            )
            
            # Hidden component to store profiles data
            profiles_data = gr.State([])
        
        with gr.Accordion("Roles", open=True):
            gr.Markdown("### Define Roles")
            gr.Markdown("*Format: Comma-separated list*")
            
            roles_text = gr.Textbox(
                label="Roles",
                placeholder="e.g., maintainer, reviewer, approver, owner",
                info="List the different roles in your project"
            )
        
        with gr.Accordion("Individuals", open=True):
            gr.Markdown("### Individual Participants")
            gr.Markdown("*Define individual human participants with optional attributes*")
            gr.Markdown("*All attributes except name are optional*")
            
            with gr.Row():
                individual_name = gr.Textbox(
                    label="Individual Name",
                    placeholder="e.g., john_doe, jane_smith",
                    info="Unique name for this individual"
                )
                
            with gr.Row():
                individual_vote_value = gr.Number(
                    label="Vote Value (Optional)",
                    value=None,
                    minimum=0.0,
                    maximum=2.0,
                    step=0.1,
                    info="Weight of this individual's vote (default: 1.0)"
                )
                
                individual_profile = gr.Dropdown(
                    label="Profile (Optional)",
                    choices=[],  # Will be populated dynamically from added profiles
                    value=None,
                    allow_custom_value=False,
                    info="Diversity profile for this individual"
                )
                
            with gr.Row():
                individual_role = gr.Dropdown(
                    label="Role (Optional)",
                    choices=[],  # Will be populated dynamically from roles text
                    value=None,
                    allow_custom_value=False,
                    info="Role assignment for this individual"
                )
                
            with gr.Row():
                add_individual_btn = gr.Button("➕ Add Individual", variant="secondary")
                clear_individuals_btn = gr.Button("🗑️ Clear All", variant="secondary")
            
            # Display added individuals
            individuals_display = gr.Textbox(
                label="Added Individuals",
                lines=4,
                interactive=False,
                placeholder="No individuals added yet",
                info="Individual participants you've added will appear here"
            )
            
            # Hidden component to store individuals data
            individuals_data = gr.State([])
            
        with gr.Accordion("Agents", open=True):
            gr.Markdown("### Automated Participants")
            gr.Markdown("*Define automated systems that participate in decisions*")
            gr.Markdown("*All attributes except name are optional*")
            
            with gr.Row():
                agent_name = gr.Textbox(
                    label="Agent Name",
                    placeholder="e.g., k8s-ci-robot, dependabot",
                    info="Unique name for this automated agent"
                )
                
            with gr.Row():
                agent_confidence = gr.Number(
                    label="Confidence (Optional)",
                    value=None,
                    minimum=0.0,
                    maximum=1.0,
                    step=0.1,
                    placeholder="Enter value (0.0-1.0)",
                    info="Agent's confidence level (0.0 to 1.0)"
                )
                
                agent_autonomy_level = gr.Number(
                    label="Autonomy Level (Optional)",
                    value=None,
                    minimum=0.0,
                    maximum=1.0,
                    step=0.1,
                    placeholder="Enter value (0.0-1.0)",
                    info="Agent's autonomy level (0.0 to 1.0)"
                )
                
            with gr.Row():
                agent_explainability = gr.Number(
                    label="Explainability (Optional)",
                    value=None,
                    minimum=0.0,
                    maximum=1.0,
                    step=0.1,
                    placeholder="Enter value (0.0-1.0)",
                    info="Agent's explainability level (0.0 to 1.0)"
                )
                
                agent_role = gr.Dropdown(
                    label="Role (Optional)",
                    choices=[],  # Will be populated dynamically from roles text
                    value=None,
                    allow_custom_value=False,
                    info="Role assignment for this agent"
                )
                
            with gr.Row():
                add_agent_btn = gr.Button("➕ Add Agent", variant="secondary")
                clear_agents_btn = gr.Button("🗑️ Clear All", variant="secondary")
            
            # Display added agents
            agents_display = gr.Textbox(
                label="Added Agents",
                lines=4,
                interactive=False,
                placeholder="No agents added yet",
                info="Automated agents you've added will appear here"
            )
            
            # Hidden component to store agents data
            agents_data = gr.State([])
        
        return {
            'profile_name': profile_name,
            'profile_gender': profile_gender,
            'profile_race': profile_race,
            'add_profile_btn': add_profile_btn,
            'clear_profiles_btn': clear_profiles_btn,
            'profiles_display': profiles_display,
            'profiles_data': profiles_data,
            'roles_text': roles_text,
            'individual_name': individual_name,
            'individual_vote_value': individual_vote_value,
            'individual_profile': individual_profile,
            'individual_role': individual_role,
            'add_individual_btn': add_individual_btn,
            'clear_individuals_btn': clear_individuals_btn,
            'individuals_display': individuals_display,
            'individuals_data': individuals_data,
            'agent_name': agent_name,
            'agent_confidence': agent_confidence,
            'agent_autonomy_level': agent_autonomy_level,
            'agent_explainability': agent_explainability,
            'agent_role': agent_role,
            'add_agent_btn': add_agent_btn,
            'clear_agents_btn': clear_agents_btn,
            'agents_display': agents_display,
            'agents_data': agents_data
        }
    
    def _create_policy_forms(self):
        """Create forms for defining policies"""
        gr.Markdown("## Define Governance Policies")
        gr.Markdown("Configure the decision-making rules for your project.")
        
        with gr.Accordion("Add New Policy", open=True):
            gr.Markdown("### Create a New Policy")
            gr.Markdown("*Define individual policies and add them to your governance structure*")
            gr.Markdown("**Note:** Fields marked with * are mandatory")
            
            with gr.Row():
                policy_name = gr.Textbox(
                    label="Policy Name *",
                    placeholder="e.g., pr_merge_policy",
                    info="A unique name for this policy (required)"
                )
                
                policy_type = gr.Dropdown(
                    label="Policy Type",
                    choices=[
                        "MajorityPolicy",
                        "AbsoluteMajorityPolicy", 
                        "ConsensusPolicy",
                        "LazyConsensusPolicy",
                        "LeaderDrivenPolicy",
                        "VotingPolicy",
                        "ComposedPolicy"
                    ],
                    value="MajorityPolicy",
                    info="Type of decision-making process"
                )
            
            with gr.Row():
                policy_scope = gr.Dropdown(
                    label="Policy Scope *",
                    choices=[],  # Will be populated dynamically from defined scopes
                    value=None,
                    allow_custom_value=True,
                    info="Select the scope this policy applies to (required)"
                )
                
                # Participants for this policy
                policy_participants = gr.Dropdown(
                    label="Policy Participants *",
                    choices=[],  # Will be populated dynamically from defined participants
                    value=None,
                    allow_custom_value=True,
                    multiselect=True,
                    info="Select participants from defined roles/individuals (required)"
                )
            
            with gr.Row():
                # Decision type
                decision_type = gr.Dropdown(
                    label="Decision Type",
                    choices=["BooleanDecision", "StringList", "ElementList"],
                    value="BooleanDecision"
                )
                
                # Options for StringList and ElementList
                decision_options = gr.Textbox(
                    label="Decision Options",
                    placeholder="e.g., joe, george (for ElementList/StringList)",
                    visible=False,
                    info="Comma-separated options for StringList/ElementList decisions"
                )
                
                # Parameters (for voting policies)
                voting_ratio = gr.Slider(
                    label="Voting Ratio",
                    minimum=0.0,
                    maximum=1.0,
                    value=1.0,
                    step=0.1,
                    visible=True,  # Start visible since MajorityPolicy is default
                    info="Required ratio of positive votes (1.0 = unanimous)"
                )
            
            with gr.Row():
                # Default policy for LeaderDrivenPolicy
                default_decision = gr.Dropdown(
                    label="Default Policy",
                    choices=[],  # Will be populated with other defined policies
                    value=None,
                    allow_custom_value=True,
                    visible=False,
                    info="Default policy when leader doesn't participate (Showing only policies with same scope)"
                )
                
                # Fallback policy for ConsensusPolicy and LazyConsensusPolicy
                fallback_policy = gr.Dropdown(
                    label="Fallback Policy",
                    choices=[],  # Will be populated with other defined policies
                    value=None,
                    allow_custom_value=True,
                    visible=False,
                    info="Policy to use when consensus cannot be reached (Showing only policies with same scope)"
                )
            
            # Conditions section
            gr.Markdown("#### Policy Conditions (Optional)")
            
            with gr.Row():
                condition_type = gr.Dropdown(
                    label="Add Condition",
                    choices=[
                        "",  # Empty option for no condition
                        "Deadline",
                        "MinDecisionTime", 
                        "ParticipantExclusion",
                        "MinParticipants",
                        "VetoRight",
                        "LabelCondition"
                    ],
                    value="",
                    info="Select a condition type to add to this policy"
                )
            

            
            # Condition-specific fields (initially hidden)
            with gr.Row():
                # VetoRight condition
                veto_participants = gr.Dropdown(
                    label="Veto Right Participants",
                    choices=[],  # Will be populated from participants
                    value=None,
                    multiselect=True,
                    allow_custom_value=True,
                    visible=False,
                    info="Participants who can veto this decision"
                )
                
                # ParticipantExclusion condition
                excluded_participants = gr.Dropdown(
                    label="Excluded Participants",
                    choices=[],  # Will be populated from participants
                    value=None,
                    multiselect=True,
                    allow_custom_value=True,
                    visible=False,
                    info="Participants excluded from this decision"
                )
            
            with gr.Row():
                # MinParticipants condition
                min_participants = gr.Number(
                    label="Minimum Participants",
                    value=None,
                    visible=False,
                    info="Minimum number of participants required (≥1)"
                )
            
            # Deadline condition fields
            with gr.Row():
                deadline_offset_value = gr.Number(
                    label="Deadline Offset Value",
                    value=None,
                    visible=False,
                    info="Time offset number (≥1, e.g., 7 for '7 days')"
                )
                
                deadline_offset_unit = gr.Dropdown(
                    label="Deadline Offset Unit",
                    choices=["days", "weeks", "months", "years"],
                    value="days",
                    visible=False,
                    info="Time unit for the offset"
                )
            
            with gr.Row():
                deadline_date = gr.Textbox(
                    label="Deadline Date (DD/MM/YYYY)",
                    placeholder="e.g., 25/12/2024",
                    visible=False,
                    info="Specific deadline date (optional, can be used with or without offset)"
                )
            
            # MinDecisionTime condition fields  
            with gr.Row():
                min_decision_offset_value = gr.Number(
                    label="Min Decision Time Offset Value",
                    value=None,
                    visible=False,
                    info="Minimum time offset number (≥1, e.g., 2 for '2 days')"
                )
                
                min_decision_offset_unit = gr.Dropdown(
                    label="Min Decision Time Offset Unit",
                    choices=["days", "weeks", "months", "years"],
                    value="days",
                    visible=False,
                    info="Time unit for the minimum decision time"
                )
            
            with gr.Row():
                min_decision_date = gr.Textbox(
                    label="Min Decision Date (DD/MM/YYYY)",
                    placeholder="e.g., 01/01/2024",
                    visible=False,
                    info="Specific minimum decision date (optional, can be used with or without offset)"
                )
            
            with gr.Row():
                # LabelCondition fields
                label_condition_type = gr.Dropdown(
                    label="Label Condition Type",
                    choices=["pre", "post"],
                    value="pre",
                    visible=False,
                    info="When to check labels (pre/post decision)"
                )
                
                label_condition_operator = gr.Dropdown(
                    label="Label Operator",
                    choices=["", "not"],
                    value="",
                    visible=False,
                    info="Label condition operator (empty for required, 'not' for forbidden)"
                )
            
            with gr.Row():
                label_condition_labels = gr.Textbox(
                    label="Labels",
                    placeholder="e.g., lgtm, approved",
                    visible=False,
                    info="Comma-separated list of labels"
                )
            
            # Condition management buttons
            with gr.Row():
                add_condition_btn = gr.Button("➕ Add Condition", variant="secondary")
                clear_conditions_btn = gr.Button("🗑️ Clear All", variant="secondary")
            
            # Added conditions display (adaptive height)
            added_conditions_list = gr.Textbox(
                label="Added Conditions",
                value="",
                interactive=False,
                lines=2,
                max_lines=10,
                info="List of conditions added to this policy"
            )
            
            with gr.Row():
                add_policy_btn = gr.Button("➕ Add Policy", variant="secondary")
                clear_policies_btn = gr.Button("🗑️ Clear All", variant="secondary")
            
            # Display added policies
            policies_display = gr.Textbox(
                label="Added Policies",
                lines=6,
                interactive=False,
                placeholder="No policies added yet. Create policies to define your governance rules.",
                info="Policies you've added will appear here"
            )
            
            # Hidden component to store policies data
            policies_data = gr.State([])
        

        
        with gr.Accordion("🔄 Composed Policy (Multi-phase)", open=False):
            gr.Markdown("### Create Complex Multi-Phase Governance Policies")
            gr.Markdown("Composed policies orchestrate multiple existing policies in sequence or parallel.")
            
            # Basic composed policy information
            with gr.Row():
                composed_policy_name = gr.Textbox(
                    label="Composed Policy Name *",
                    placeholder="e.g., TwoPhaseReview, ComplexApproval",
                    info="Unique name for this composed policy"
                )
                
                composed_policy_scope = gr.Dropdown(
                    label="Composed Policy Scope *",
                    choices=[],  # Will be populated dynamically from defined scopes
                    value=None,
                    allow_custom_value=True,
                    info="Select the scope this composed policy applies to (required)"
                )
            
            # Execution configuration
            gr.Markdown("**⚙️ Execution Configuration**")
            with gr.Row():
                execution_type = gr.Dropdown(
                    label="Execution Type",
                    choices=["sequential", "parallel"],
                    value="sequential",
                    info="Sequential: phases run one after another; Parallel: phases run simultaneously"
                )
                
                require_all = gr.Checkbox(
                    label="Require All Phases",
                    value=True,
                    info="Must all phases succeed for the composed policy to succeed?"
                )
                
                carry_over = gr.Checkbox(
                    label="Carry Over Results",
                    value=True,
                    info="Pass results between phases? (Only applicable for sequential execution)"
                )
            
            # Phase management
            gr.Markdown("**📋 Phase Management**")
            gr.Markdown("Define each phase as a separate policy. Phases will inherit the composed policy's scope.")
            
            # Phase policy definition (similar to single policy form)
            with gr.Row():
                phase_name = gr.Textbox(
                    label="Phase Name *",
                    placeholder="e.g., ReviewPhase, ApprovalPhase",
                    info="Unique name for this phase"
                )
                
                phase_type = gr.Dropdown(
                    label="Phase Policy Type",
                    choices=[
                        "MajorityPolicy", 
                        "LeaderDrivenPolicy", 
                        "AbsoluteMajorityPolicy", 
                        "ConsensusPolicy", 
                        "LazyConsensusPolicy", 
                        "VotingPolicy"
                    ],
                    value="MajorityPolicy",
                    info="Type of decision-making process for this phase"
                )
            
            with gr.Row():
                # Participants for this phase
                phase_participants = gr.Dropdown(
                    label="Phase Participants *",
                    choices=[],  # Will be populated dynamically from defined participants
                    value=None,
                    allow_custom_value=True,
                    multiselect=True,
                    info="Select participants for this phase"
                )
                
                # Decision type for the phase
                phase_decision_type = gr.Dropdown(
                    label="Phase Decision Type",
                    choices=["BooleanDecision", "StringList", "ElementList"],
                    value="BooleanDecision"
                )
            
            with gr.Row():
                # Options for StringList and ElementList
                phase_decision_options = gr.Textbox(
                    label="Phase Decision Options",
                    placeholder="e.g., joe, george (for ElementList/StringList)",
                    visible=False,
                    info="Comma-separated options for StringList/ElementList decisions"
                )
                
                # Parameters (for voting policies)
                phase_voting_ratio = gr.Slider(
                    label="Phase Voting Ratio",
                    minimum=0.0,
                    maximum=1.0,
                    value=1.0,
                    step=0.1,
                    visible=True,  # Start visible since MajorityPolicy is default for phases too
                    info="Required ratio of positive votes (1.0 = unanimous)"
                )
            
            # Phase-specific policy attributes (default/fallback)
            with gr.Row():
                phase_default_decision = gr.Dropdown(
                    label="Phase Default Decision",
                    choices=[],
                    value=None,
                    visible=False,
                    info="Default policy for LeaderDrivenPolicy phases"
                )
                
                phase_fallback_policy = gr.Dropdown(
                    label="Phase Fallback Policy", 
                    choices=[],
                    value=None,
                    visible=False,
                    info="Fallback policy for Consensus/LazyConsensus phases"
                )
            
            with gr.Row():
                add_phase_btn = gr.Button("➕ Add Phase", variant="secondary")
                clear_phases_btn = gr.Button("🗑️ Clear All Phases", variant="secondary")
            
            # Display added phases
            added_phases_list = gr.Textbox(
                label="Added Phases",
                value="",
                interactive=False,
                lines=1,
                max_lines=8,
                info="Phases that will be executed in this composed policy"
            )
            
            # Composed policy actions
            with gr.Row():
                add_composed_policy_btn = gr.Button("➕ Add Composed Policy", variant="primary")
                clear_composed_policies_btn = gr.Button("🗑️ Clear All", variant="secondary")
            
            # Display added composed policies
            composed_policies_display = gr.Textbox(
                label="Added Composed Policies",
                lines=6,
                interactive=False,
                placeholder="No composed policies added yet. Create composed policies to define complex multi-phase governance.",
                info="Composed policies you've added will appear here"
            )
            
            # Hidden component to store composed policies data
            composed_policies_data = gr.State([])
        
        return {
            'policy_name': policy_name,
            'policy_type': policy_type,
            'policy_scope': policy_scope,
            'policy_participants': policy_participants,
            'decision_type': decision_type,
            'decision_options': decision_options,
            'voting_ratio': voting_ratio,
            'default_decision': default_decision,
            'fallback_policy': fallback_policy,
            'condition_type': condition_type,
            'veto_participants': veto_participants,
            'excluded_participants': excluded_participants,
            'min_participants': min_participants,
            'deadline_offset_value': deadline_offset_value,
            'deadline_offset_unit': deadline_offset_unit,
            'deadline_date': deadline_date,
            'min_decision_offset_value': min_decision_offset_value,
            'min_decision_offset_unit': min_decision_offset_unit,
            'min_decision_date': min_decision_date,
            'label_condition_type': label_condition_type,
            'label_condition_operator': label_condition_operator,
            'label_condition_labels': label_condition_labels,
            'add_condition_btn': add_condition_btn,
            'clear_conditions_btn': clear_conditions_btn,
            'added_conditions_list': added_conditions_list,
            'add_policy_btn': add_policy_btn,
            'clear_policies_btn': clear_policies_btn,
            'policies_display': policies_display,
            'policies_data': policies_data,
            # Composed Policy components
            'composed_policy_name': composed_policy_name,
            'composed_policy_scope': composed_policy_scope,
            'execution_type': execution_type,
            'require_all': require_all,
            'carry_over': carry_over,
            # Phase definition components
            'phase_name': phase_name,
            'phase_type': phase_type,
            'phase_participants': phase_participants,
            'phase_decision_type': phase_decision_type,
            'phase_decision_options': phase_decision_options,
            'phase_voting_ratio': phase_voting_ratio,
            'phase_default_decision': phase_default_decision,
            'phase_fallback_policy': phase_fallback_policy,
            'add_phase_btn': add_phase_btn,
            'clear_phases_btn': clear_phases_btn,
            'added_phases_list': added_phases_list,
            'add_composed_policy_btn': add_composed_policy_btn,
            'clear_composed_policies_btn': clear_composed_policies_btn,
            'composed_policies_display': composed_policies_display,
            'composed_policies_data': composed_policies_data
        }
    
    def _create_preview_panel(self):
        """Create the live preview panel"""
        gr.Markdown("## 👁️ Live Preview")
        gr.Markdown("Generated DSL code will appear here as you fill the form.")
        
        self.preview_code = gr.Textbox(
            label="Generated DSL",
            lines=25,
            max_lines=25,
            interactive=False,
            elem_classes=["preview-panel"],
            show_copy_button=True
        )
        
        # Action buttons
        with gr.Row():
            generate_btn = gr.Button("🔄 Refresh Preview", variant="secondary")
            download_btn = gr.Button("💾 Download DSL", variant="primary")
            load_example_btn = gr.Button("📋 Load Example", variant="secondary")
        
        return {
            'preview_code': self.preview_code,
            'generate_btn': generate_btn,
            'download_btn': download_btn,
            'load_example_btn': load_example_btn
        }
    
    def _setup_event_handlers(self, scope_components, participant_components, policy_components, form_state):
        """Set up event handlers for form interactions"""
        
        def add_profile(name, gender, race, current_profiles):
            """Add a new profile to the list"""
            if not name.strip():
                display_text = self._format_profiles_display(current_profiles)
                error_message = f"❌ Error: Please enter a profile name\n\n{display_text}" if current_profiles else "❌ Error: Please enter a profile name"
                return current_profiles, error_message, "", "", "", None
            
            # Check if profile already exists
            if any(p['name'] == name.strip() for p in current_profiles):
                display_text = self._format_profiles_display(current_profiles)
                error_message = f"❌ Error: Profile name already exists\n\n{display_text}" if current_profiles else "❌ Error: Profile name already exists"
                return current_profiles, error_message, "", "", "", None
            
            # Validate that at least one attribute is provided
            if not gender and not race:
                display_text = self._format_profiles_display(current_profiles)
                error_message = f"❌ Error: Profiles must have either a race or gender value\n\n{display_text}" if current_profiles else "❌ Error: Profiles must have either a race or gender value"
                return current_profiles, error_message, "", "", "", None
            
            # Create new profile
            new_profile = {
                'name': name.strip(),
                'gender': gender if gender else None,
                'race': race if race else None
            }
            
            updated_profiles = current_profiles + [new_profile]
            
            # Update display
            display_text = self._format_profiles_display(updated_profiles)
            success_message = f"✅ Profile '{new_profile['name']}' added successfully!\n\n{display_text}"
            
            return updated_profiles, success_message, "", "", "", None  # Clear individual profile selection
        
        def clear_profiles():
            """Clear all profiles"""
            return [], "No profiles added yet", None
        
        def add_individual(name, vote_value, profile, role, current_individuals, current_profiles, roles_text):
            """Add a new individual to the list"""
            if not name.strip():
                return current_individuals, "❌ Please enter an individual name", "", 1.0, None, None
            
            # Check if individual already exists
            if any(i['name'] == name.strip() for i in current_individuals):
                return current_individuals, "❌ Individual name already exists", "", 1.0, None, None
            
            # Create new individual
            new_individual = {
                'name': name.strip(),
                'vote_value': vote_value if vote_value != 1.0 else None,  # Only store if different from default
                'profile': profile if profile else None,
                'role': role if role else None
            }
            
            updated_individuals = current_individuals + [new_individual]
            
            # Update display
            display_text = self._format_individuals_display(updated_individuals)
            success_message = f"✅ Individual '{new_individual['name']}' added successfully!\n\n{display_text}"
            
            # Update dropdown choices for next individual
            profile_choices = [p['name'] for p in current_profiles] if current_profiles else []
            role_choices = [role.strip() for role in roles_text.split(',') if role.strip()] if roles_text else []
            
            return updated_individuals, success_message, "", 1.0, None, None
        
        def clear_individuals():
            """Clear all individuals"""
            return [], "No individuals added yet"
        
        def update_individual_dropdowns(roles_text, current_profiles):
            """Update individual dropdown choices when roles or profiles change"""
            profile_choices = [p['name'] for p in current_profiles] if current_profiles else []
            role_choices = [role.strip() for role in roles_text.split(',') if role.strip()] if roles_text else []
            
            return gr.Dropdown(choices=profile_choices, value=None), gr.Dropdown(choices=role_choices, value=None)
        
        def add_agent(name, confidence, autonomy_level, explainability, role, current_agents, roles_text):
            """Add a new agent to the list"""
            if not name.strip():
                return current_agents, "❌ Please enter an agent name", "", None, None, None, None
            
            # Check if agent already exists
            if any(a['name'] == name.strip() for a in current_agents):
                return current_agents, "❌ Agent name already exists", "", None, None, None, None
            
            # Create new agent
            new_agent = {
                'name': name.strip(),
                'confidence': confidence if confidence is not None else None,
                'autonomy_level': autonomy_level if autonomy_level is not None else None,
                'explainability': explainability if explainability is not None else None,
                'role': role if role else None
            }
            
            updated_agents = current_agents + [new_agent]
            
            # Update display
            display_text = self._format_agents_display(updated_agents)
            success_message = f"✅ Agent '{new_agent['name']}' added successfully!\n\n{display_text}"
            
            # Update role dropdown choices for next agent
            role_choices = [role.strip() for role in roles_text.split(',') if role.strip()] if roles_text else []
            
            return updated_agents, success_message, "", None, None, None, None
        
        def clear_agents():
            """Clear all agents"""
            return [], "No agents added yet"
        
        def update_agent_role_dropdown(roles_text):
            """Update agent role dropdown when roles text changes"""
            role_choices = [role.strip() for role in roles_text.split(',') if role.strip()] if roles_text else []
            return gr.Dropdown(choices=role_choices, value=None)
        
        def update_scope_dropdown(projects_text, activities_text, tasks_text):
            """Update policy scope dropdown when scope definitions change"""
            scope_choices = self._extract_scope_names(projects_text, activities_text, tasks_text)
            return gr.Dropdown(choices=scope_choices, value=None)
        
        def update_participant_dropdown(roles_text, individuals_data, agents_data):
            """Update policy participants dropdown when participant definitions change"""
            participant_choices = self._extract_participant_names(roles_text, individuals_data, agents_data)
            return (
                gr.Dropdown(choices=participant_choices, value=None),  # policy_participants
                gr.Dropdown(choices=participant_choices, value=None),  # veto_participants
                gr.Dropdown(choices=participant_choices, value=None)   # excluded_participants
            )
        
        def update_phase_participant_dropdown(roles_text, individuals_data, agents_data):
            """Update phase participants dropdown when participant definitions change"""
            participant_choices = self._extract_participant_names(roles_text, individuals_data, agents_data)
            return gr.Dropdown(choices=participant_choices, value=None)
        
        def update_policy_reference_dropdowns(policies_data, current_scope=None):
            """Update default and fallback policy dropdowns when policies change or scope changes"""
            if not policies_data or not current_scope:
                # If no policies exist OR no scope is specified, show no policies
                policy_choices = []
            else:
                # Filter policies to only show those with the same scope
                policy_choices = [p['name'] for p in policies_data if p.get('scope') == current_scope]
                
            return (
                gr.Dropdown(choices=policy_choices),  # default_decision
                gr.Dropdown(choices=policy_choices)   # fallback_policy  
            )
        
        def update_policy_reference_dropdowns_on_scope_change(policies_data, current_scope=None):
            """Update and clear default and fallback policy dropdowns when scope changes"""
            if not policies_data or not current_scope:
                # If no policies exist OR no scope is specified, show no policies
                policy_choices = []
            else:
                # Filter policies to only show those with the same scope
                policy_choices = [p['name'] for p in policies_data if p.get('scope') == current_scope]
                
            return (
                gr.Dropdown(choices=policy_choices, value=None),  # default_decision - clear selection
                gr.Dropdown(choices=policy_choices, value=None)   # fallback_policy - clear selection
            )
        
        def update_policy_type_visibility(policy_type):
            """Update visibility of policy-specific attributes based on policy type"""
            show_default = policy_type == "LeaderDrivenPolicy"
            show_fallback = policy_type in ["ConsensusPolicy", "LazyConsensusPolicy"]
            show_voting_ratio = policy_type in ["MajorityPolicy", "AbsoluteMajorityPolicy", "VotingPolicy"]
            
            return (
                gr.Dropdown(visible=show_default),  # default_decision
                gr.Dropdown(visible=show_fallback),  # fallback_policy
                gr.Slider(visible=show_voting_ratio)  # voting_ratio
            )
        
        def update_decision_options_visibility(decision_type):
            """Update visibility of decision options based on decision type"""
            show_options = decision_type in ["StringList", "ElementList"]
            return gr.Textbox(visible=show_options)
        
        def update_condition_visibility(condition_type):
            """Update visibility of condition fields based on condition type"""
            show_veto = condition_type == "VetoRight"
            show_exclusion = condition_type == "ParticipantExclusion"
            show_min_participants = condition_type == "MinParticipants"
            show_deadline = condition_type == "Deadline"
            show_min_decision = condition_type == "MinDecisionTime"
            show_label = condition_type == "LabelCondition"
            
            return [
                gr.Dropdown(visible=show_veto),       # veto_participants
                gr.Dropdown(visible=show_exclusion),  # excluded_participants 
                gr.Number(visible=show_min_participants), # min_participants
                gr.Number(visible=show_deadline),     # deadline_offset_value
                gr.Dropdown(visible=show_deadline),   # deadline_offset_unit
                gr.Textbox(visible=show_deadline),    # deadline_date
                gr.Number(visible=show_min_decision), # min_decision_offset_value
                gr.Dropdown(visible=show_min_decision), # min_decision_offset_unit
                gr.Textbox(visible=show_min_decision), # min_decision_date
                gr.Dropdown(visible=show_label),     # label_condition_type
                gr.Dropdown(visible=show_label),     # label_condition_operator
                gr.Textbox(visible=show_label)       # label_condition_labels
            ]
        
        def add_policy(name, policy_type, scope, participants, decision_type, decision_options, voting_ratio, 
                      default_decision, fallback_policy, condition_type, veto_participants, excluded_participants,
                      min_participants, deadline_offset_value, deadline_offset_unit, deadline_date,
                      min_decision_offset_value, min_decision_offset_unit, min_decision_date,
                      label_condition_type, label_condition_operator, label_condition_labels, 
                      added_conditions_list, current_policies):
            """Add a new policy to the list"""
            # Validate policy name (mandatory)
            if not name.strip():
                display_text = self._format_policies_display(current_policies)
                error_message = f"❌ Error: Please enter a policy name\n\n{display_text}" if current_policies else "❌ Error: Please enter a policy name"
                return current_policies, error_message
            
            # Validate policy scope (mandatory)
            if not scope:
                display_text = self._format_policies_display(current_policies)
                error_message = f"❌ Error: Please select a policy scope\n\n{display_text}" if current_policies else "❌ Error: Please select a policy scope"
                return current_policies, error_message
            
            # Validate policy participants (mandatory)
            if not participants or (isinstance(participants, list) and len(participants) == 0):
                display_text = self._format_policies_display(current_policies)
                error_message = f"❌ Error: Please select at least one participant\n\n{display_text}" if current_policies else "❌ Error: Please select at least one participant"
                return current_policies, error_message
            
            # Check if policy already exists
            if any(p['name'] == name.strip() for p in current_policies):
                display_text = self._format_policies_display(current_policies)
                error_message = f"❌ Error: Policy name '{name.strip()}' already exists\n\n{display_text}"
                return current_policies, error_message
            
            # Create new policy
            new_policy = {
                'name': name.strip(),
                'type': policy_type,
                'scope': scope if scope else None,
                'participants': participants if participants else None,
                'decision_type': decision_type,
                'decision_options': decision_options if decision_type in ["StringList", "ElementList"] and decision_options else None,
                'voting_ratio': voting_ratio if policy_type in ["MajorityPolicy", "AbsoluteMajorityPolicy", "VotingPolicy"] else None,
                'default_decision': default_decision if policy_type == "LeaderDrivenPolicy" else None,
                'fallback_policy': fallback_policy if policy_type in ["ConsensusPolicy", "LazyConsensusPolicy"] else None,
                # Store the dynamically added conditions
                'added_conditions': added_conditions_list.strip() if added_conditions_list else None,
                # Keep backward compatibility with single condition fields for now
                'condition_type': condition_type if condition_type else None,
                'veto_participants': veto_participants if condition_type == "VetoRight" else None,
                'excluded_participants': excluded_participants if condition_type == "ParticipantExclusion" else None,
                'min_participants': min_participants if condition_type == "MinParticipants" else None,
                'deadline_offset_value': deadline_offset_value if condition_type == "Deadline" else None,
                'deadline_offset_unit': deadline_offset_unit if condition_type == "Deadline" else None,
                'deadline_date': deadline_date if condition_type == "Deadline" else None,
                'min_decision_offset_value': min_decision_offset_value if condition_type == "MinDecisionTime" else None,
                'min_decision_offset_unit': min_decision_offset_unit if condition_type == "MinDecisionTime" else None,
                'min_decision_date': min_decision_date if condition_type == "MinDecisionTime" else None,
                'label_condition_type': label_condition_type if condition_type == "LabelCondition" else None,
                'label_condition_operator': label_condition_operator if condition_type == "LabelCondition" else None,
                'label_condition_labels': label_condition_labels if condition_type == "LabelCondition" else None
            }
            
            updated_policies = current_policies + [new_policy]
            
            # Update display
            display_text = self._format_policies_display(updated_policies)
            success_message = f"✅ Policy '{new_policy['name']}' added successfully!\n\n{display_text}"
            
            # For successful addition, return updated policies and success message
            return updated_policies, success_message
        
        def clear_policies():
            """Clear all policies"""
            return [], "No policies added yet"

        def add_condition(condition_type, veto_participants, excluded_participants, min_participants,
                         deadline_offset_value, deadline_offset_unit, deadline_date,
                         min_decision_offset_value, min_decision_offset_unit, min_decision_date,
                         label_condition_type, label_condition_operator, label_condition_labels,
                         current_conditions_text):
            """Add a condition to the current policy"""
            
            # Parse existing conditions from the display text (ignore error messages and success messages)
            existing_conditions = []
            if current_conditions_text.strip():
                for line in current_conditions_text.strip().split('\n'):
                    line = line.strip()
                    # Skip error messages, success messages, and empty lines
                    if line and not line.startswith('❌ Error:') and not line.startswith('✅'):
                        existing_conditions.append(line)
            
            # Helper function to format the conditions display with error
            def format_conditions_with_error(error_msg):
                if existing_conditions:
                    conditions_text = '\n'.join(existing_conditions)
                    return f"❌ Error: {error_msg}\n\n{conditions_text}"
                else:
                    return f"❌ Error: {error_msg}"
            
            # Helper function to return error with all condition fields reset
            def return_error(error_msg):
                return (
                    format_conditions_with_error(error_msg),  # added_conditions_list
                    gr.Dropdown(value=""),  # condition_type
                    gr.Dropdown(value=None),  # veto_participants
                    gr.Dropdown(value=None),  # excluded_participants
                    None,  # min_participants
                    None,  # deadline_offset_value  
                    "days",  # deadline_offset_unit
                    "",  # deadline_date
                    None,  # min_decision_offset_value
                    "days",  # min_decision_offset_unit
                    "",  # min_decision_date
                    "pre",  # label_condition_type
                    "",  # label_condition_operator
                    ""  # label_condition_labels
                )
            
            if not condition_type:
                return return_error("Please select a condition type")
            
            # Check for duplicates (except LabelCondition)
            existing_types = []
            for condition in existing_conditions:
                if condition.startswith('Deadline'):
                    existing_types.append('Deadline')
                elif condition.startswith('MinDecisionTime'):
                    existing_types.append('MinDecisionTime')
                elif condition.startswith('ParticipantExclusion'):
                    existing_types.append('ParticipantExclusion')
                elif condition.startswith('MinParticipants'):
                    existing_types.append('MinParticipants')
                elif condition.startswith('VetoRight'):
                    existing_types.append('VetoRight')
                # LabelCondition can have multiple entries, so we don't track it
            
            if condition_type != "LabelCondition" and condition_type in existing_types:
                return return_error(f"{condition_type} already exists. Only LabelCondition can be added multiple times.")
            
            # Create the condition string
            condition_str = ""
            
            if condition_type == "VetoRight":
                if not veto_participants:
                    return return_error("Please specify veto participants")
                # veto_participants is already a list from multiselect dropdown
                participants_list = [p.strip() for p in veto_participants if p.strip()] if isinstance(veto_participants, list) else [veto_participants.strip()]
                condition_str = f"VetoRight: {', '.join(participants_list)}"
                
            elif condition_type == "ParticipantExclusion":
                if not excluded_participants:
                    return return_error("Please specify excluded participants")
                # excluded_participants is already a list from multiselect dropdown
                participants_list = [p.strip() for p in excluded_participants if p.strip()] if isinstance(excluded_participants, list) else [excluded_participants.strip()]
                condition_str = f"ParticipantExclusion: {', '.join(participants_list)}"
                
            elif condition_type == "MinParticipants":
                if not min_participants or min_participants < 1:
                    return return_error("Please specify minimum participants (≥1)")
                condition_str = f"MinParticipants: {min_participants}"
                
            elif condition_type == "Deadline":
                parts = []
                if deadline_offset_value and deadline_offset_unit:
                    if deadline_offset_value < 1:
                        return return_error("Deadline offset value must be ≥1")
                    parts.append(f"{deadline_offset_value} {deadline_offset_unit}")
                if deadline_date and deadline_date.strip():
                    parts.append(deadline_date.strip())
                if not parts:
                    return return_error("Please specify deadline offset or date")
                condition_str = f"Deadline: {', '.join(parts)}"
                
            elif condition_type == "MinDecisionTime":
                parts = []
                if min_decision_offset_value and min_decision_offset_unit:
                    if min_decision_offset_value < 1:
                        return return_error("Minimum decision time offset value must be ≥1")
                    parts.append(f"{min_decision_offset_value} {min_decision_offset_unit}")
                if min_decision_date and min_decision_date.strip():
                    parts.append(min_decision_date.strip())
                if not parts:
                    return return_error("Please specify minimum decision time offset or date")
                condition_str = f"MinDecisionTime: {', '.join(parts)}"
                
            elif condition_type == "LabelCondition":
                if not label_condition_labels:
                    return return_error("Please specify labels")
                labels = [l.strip() for l in label_condition_labels.split(',') if l.strip()]
                if not labels:
                    return return_error("Please specify valid labels")
                
                type_part = label_condition_type if label_condition_type else "pre"
                operator_part = f" {label_condition_operator}" if label_condition_operator else ""
                condition_str = f"LabelCondition {type_part}{operator_part}: {', '.join(labels)}"
            
            if condition_str:
                # Add to existing conditions and format success message
                updated_conditions = existing_conditions + [condition_str]
                conditions_text = '\n'.join(updated_conditions)
                success_message = f"✅ {condition_type} condition added successfully!\n\n{conditions_text}"
                return (
                    success_message,  # added_conditions_list
                    gr.Dropdown(value=""),  # condition_type
                    gr.Dropdown(value=None),  # veto_participants
                    gr.Dropdown(value=None),  # excluded_participants
                    None,  # min_participants
                    None,  # deadline_offset_value
                    "days",  # deadline_offset_unit
                    "",  # deadline_date
                    None,  # min_decision_offset_value
                    "days",  # min_decision_offset_unit
                    "",  # min_decision_date
                    "pre",  # label_condition_type
                    "",  # label_condition_operator
                    ""  # label_condition_labels
                )
            
            return return_error("Unable to add condition")
        
        def clear_conditions():
            """Clear all conditions for the current policy"""
            return ""
        
        # Composed Policy Functions
        def add_phase(phase_name, phase_type, phase_participants, phase_decision_type, phase_decision_options, 
                     phase_voting_ratio, phase_default_decision, phase_fallback_policy, current_phases_text):
            """Add a phase to the current composed policy"""
            # Parse existing phases from the display text (ignore error messages and success messages)
            existing_phases = []
            if current_phases_text.strip():
                for line in current_phases_text.strip().split('\n'):
                    line = line.strip()
                    # Skip error messages, success messages, and empty lines
                    if line and not line.startswith('❌ Error:') and not line.startswith('✅'):
                        existing_phases.append(line)
            
            # Helper function to format the phases display with error
            def format_phases_with_error(error_msg):
                if existing_phases:
                    phases_text = '\n'.join(existing_phases)
                    return f"❌ Error: {error_msg}\n\n{phases_text}"
                else:
                    return f"❌ Error: {error_msg}"
            
            # Helper function to return error with all phase fields reset
            def return_phase_error(error_msg):
                return (
                    format_phases_with_error(error_msg),  # added_phases_list
                    "",  # phase_name
                    "MajorityPolicy",  # phase_type
                    [],  # phase_participants - use empty list
                    "BooleanDecision",  # phase_decision_type
                    "",  # phase_decision_options
                    1.0,  # phase_voting_ratio
                    None,  # phase_default_decision
                    None   # phase_fallback_policy
                )
            
            # Validate phase name (mandatory)
            if not phase_name.strip():
                return return_phase_error("Please enter a phase name")
            
            # Check for duplicates
            phase_names = [line.split(' (')[0] for line in existing_phases]  # Extract names from display format
            if phase_name.strip() in phase_names:
                return return_phase_error(f"Phase '{phase_name.strip()}' already exists")
            
            # Validate phase participants (mandatory)
            if not phase_participants or (isinstance(phase_participants, list) and len(phase_participants) == 0):
                return return_phase_error("Please select at least one participant for this phase")
            
            # Create phase display string
            participants_list = phase_participants if isinstance(phase_participants, list) else [phase_participants]
            phase_display = f"{phase_name.strip()} ({phase_type}) → participants: {', '.join(participants_list)}"
            
            # Add type-specific details
            details = []
            if phase_decision_type != "BooleanDecision":
                details.append(f"decision: {phase_decision_type}")
            
            # Show voting ratio for voting-related policies (always show, not just when != 1.0)
            if phase_type in ["MajorityPolicy", "AbsoluteMajorityPolicy", "VotingPolicy"]:
                details.append(f"ratio: {phase_voting_ratio}")
            
            # Show default decision only for LeaderDrivenPolicy
            if phase_type == "LeaderDrivenPolicy" and phase_default_decision:
                details.append(f"default: {phase_default_decision}")
            
            # Show fallback policy only for ConsensusPolicy and LazyConsensusPolicy
            if phase_type in ["ConsensusPolicy", "LazyConsensusPolicy"] and phase_fallback_policy:
                details.append(f"fallback: {phase_fallback_policy}")
            
            # Show decision options if specified and not BooleanDecision
            if phase_decision_options and phase_decision_options.strip() and phase_decision_type != "BooleanDecision":
                options_clean = phase_decision_options.strip()
                details.append(f"options: {options_clean}")
            
            if details:
                phase_display += f", {', '.join(details)}"
            
            # Add to existing phases and format success message
            updated_phases = existing_phases + [phase_display]
            phases_text = '\n'.join(updated_phases)
            success_message = f"✅ Phase '{phase_name.strip()}' added successfully!\n\n{phases_text}"
            
            return (
                success_message,  # added_phases_list
                "",  # phase_name - clear
                "MajorityPolicy",  # phase_type - reset
                [],  # phase_participants - use empty list
                "BooleanDecision",  # phase_decision_type - reset
                "",  # phase_decision_options - clear
                1.0,  # phase_voting_ratio - reset
                None,  # phase_default_decision - clear
                None   # phase_fallback_policy - clear
            )
        
        def clear_phases():
            """Clear all phases for the current composed policy"""
            return ""
        
        def add_composed_policy(name, scope, execution_type, require_all, carry_over, phases_text, current_composed_policies):
            """Add a new composed policy to the list"""
            # Validate composed policy name (mandatory)
            if not name.strip():
                display_text = self._format_composed_policies_display(current_composed_policies)
                error_message = f"❌ Error: Please enter a composed policy name\n\n{display_text}" if current_composed_policies else "❌ Error: Please enter a composed policy name"
                return current_composed_policies, error_message
            
            # Validate composed policy scope (mandatory)
            if not scope:
                display_text = self._format_composed_policies_display(current_composed_policies)
                error_message = f"❌ Error: Please select a composed policy scope\n\n{display_text}" if current_composed_policies else "❌ Error: Please select a composed policy scope"
                return current_composed_policies, error_message
            
            # Validate phases (at least one phase required)
            phases = []
            if phases_text.strip():
                for line in phases_text.strip().split('\n'):
                    line = line.strip()
                    # Skip error messages, success messages, and empty lines
                    if line and not line.startswith('❌ Error:') and not line.startswith('✅'):
                        phases.append(line)
            
            if not phases:
                display_text = self._format_composed_policies_display(current_composed_policies)
                error_message = f"❌ Error: Please add at least one phase\n\n{display_text}" if current_composed_policies else "❌ Error: Please add at least one phase"
                return current_composed_policies, error_message
            
            # Check if composed policy already exists
            if any(p['name'] == name.strip() for p in current_composed_policies):
                display_text = self._format_composed_policies_display(current_composed_policies)
                error_message = f"❌ Error: Composed policy name '{name.strip()}' already exists\n\n{display_text}"
                return current_composed_policies, error_message
            
            # Create new composed policy
            new_composed_policy = {
                'type': 'ComposedPolicy',
                'name': name.strip(),
                'scope': scope,
                'execution_type': execution_type,
                'require_all': require_all,
                'carry_over': carry_over,
                'phases': phases
            }
            
            # Add to the list
            updated_composed_policies = current_composed_policies + [new_composed_policy]
            display_text = self._format_composed_policies_display(updated_composed_policies)
            success_message = f"✅ Composed policy '{name.strip()}' added successfully!\n\n{display_text}"
            
            return updated_composed_policies, success_message
        
        def clear_composed_policies():
            """Clear all composed policies"""
            return [], "No composed policies added yet"
        
        def add_composed_policy_and_clear_form(name, scope, execution_type, require_all, carry_over, phases_text, current_composed_policies):
            """Add composed policy and clear form fields only on success"""
            # First try to add the composed policy
            policies_result, display_result = add_composed_policy(
                name, scope, execution_type, require_all, carry_over, phases_text, current_composed_policies
            )
            
            # Check if the addition was successful (no error message)
            if "❌ Error:" not in display_result:
                # Success: clear the form fields
                return (
                    policies_result, display_result,  # composed_policies_data, composed_policies_display
                    "",  # composed_policy_name - clear
                    None,  # composed_policy_scope - clear
                    "sequential",  # execution_type - reset to default
                    True,  # require_all - reset to default
                    True,  # carry_over - reset to default
                    ""   # added_phases_list - clear
                )
            else:
                # Error: keep form as is, only update composed policies display
                return (
                    policies_result, display_result,  # composed_policies_data, composed_policies_display
                    name, scope, execution_type, require_all, carry_over,  # Keep form values
                    phases_text  # Keep phases
                )
        

        def add_policy_and_clear_form(name, policy_type, scope, participants, decision_type, decision_options, voting_ratio, 
                                     default_decision, fallback_policy, condition_type, veto_participants, excluded_participants,
                                     min_participants, deadline_offset_value, deadline_offset_unit, deadline_date,
                                     min_decision_offset_value, min_decision_offset_unit, min_decision_date, 
                                     label_condition_type, label_condition_operator, label_condition_labels, 
                                     added_conditions_list, current_policies):
            """Add policy and clear form fields only on success"""
            # First try to add the policy
            policies_result, display_result = add_policy(
                name, policy_type, scope, participants, decision_type, decision_options, voting_ratio, 
                default_decision, fallback_policy, condition_type, veto_participants, excluded_participants,
                min_participants, deadline_offset_value, deadline_offset_unit, deadline_date,
                min_decision_offset_value, min_decision_offset_unit, min_decision_date,
                label_condition_type, label_condition_operator, label_condition_labels, 
                added_conditions_list, current_policies
            )
            
            # Check if the addition was successful (no error message)
            if "❌ Error:" not in display_result:
                # Success: clear the form and update dropdowns
                # Since we're clearing the form (scope will be None), show all policies
                fallback_choices = [p['name'] for p in policies_result]
                return (
                    policies_result, display_result,  # policies_data, policies_display
                    "", "MajorityPolicy", None, [], "BooleanDecision", "", 1.0,  # Clear form fields - use empty list for participants
                    gr.Dropdown(choices=fallback_choices, visible=False),  # default_decision
                    gr.Dropdown(choices=fallback_choices, visible=False),  # fallback_policy
                    "", [], [], None, None, "days", "", None, "days", "", "pre", "", "", ""  # Clear condition fields - use empty lists for participant dropdowns
                )
            else:
                # Error: keep form as is, only update policies display
                return (
                    policies_result, display_result,  # policies_data, policies_display
                    name, policy_type, scope, participants, decision_type, decision_options, voting_ratio,  # Keep form values
                    default_decision, fallback_policy,  # Keep current values
                    condition_type, veto_participants, excluded_participants, min_participants,  # Keep basic condition values
                    deadline_offset_value, deadline_offset_unit, deadline_date,  # Keep deadline values
                    min_decision_offset_value, min_decision_offset_unit, min_decision_date,  # Keep min decision values
                    label_condition_type, label_condition_operator, label_condition_labels,  # Keep label condition values
                    added_conditions_list  # Keep added conditions list
                )
        
        def update_preview(*args):
            """Update the preview based on current form values"""
            try:
                dsl_code = self._generate_dsl_from_form(*args)
                return dsl_code
            except Exception as e:
                return f"Error generating DSL: {str(e)}"
        
        def load_example():
            """Load an example configuration"""
            example_dsl = """Scopes: 
    Projects :
        ExampleProject from GitHub : owner/repo {
            Activities :
                ExampleActivity {
                    Tasks :
                        ExampleTask : Pull request {
                            Action : merge
                        }
                }
        }
Participants:
    Profiles:
        diverse_profile {
            gender : non-binary
            race : mixed
        }
    Roles : maintainer, reviewer, approver
    Individuals :
        john_doe {
            vote value : 0.8
            profile : diverse_profile
            role : maintainer
        },
        (Agent) security-bot {
            confidence : 0.9
            autonomy level: 0.8
            explainability: 1.0
            role : reviewer
        }
MajorityPolicy example_policy {
    Scope: ExampleTask
    DecisionType as BooleanDecision
    Participant list : maintainer, john_doe
    Conditions:
        MinParticipants : 2
    Parameters:
        ratio: 1.0
}"""
            return example_dsl
        
        # Get all form components for change tracking
        all_components = []
        all_components.extend(scope_components.values())
        all_components.extend(participant_components.values())
        all_components.extend(policy_components.values())
        
        # Profile management handlers
        participant_components['add_profile_btn'].click(
            fn=add_profile,
            inputs=[
                participant_components['profile_name'],
                participant_components['profile_gender'],
                participant_components['profile_race'],
                participant_components['profiles_data']
            ],
            outputs=[
                participant_components['profiles_data'],
                participant_components['profiles_display'],
                participant_components['profile_name'],        # Clear name field
                participant_components['profile_gender'],      # Clear gender field
                participant_components['profile_race'],        # Clear race field
                participant_components['individual_profile']   # Update individual profile dropdown
            ]
        )
        
        participant_components['clear_profiles_btn'].click(
            fn=clear_profiles,
            outputs=[
                participant_components['profiles_data'],
                participant_components['profiles_display'],
                participant_components['individual_profile']  # Also clear individual profile dropdown
            ]
        )
        
        # Update individual profile dropdown when profiles data changes
        participant_components['profiles_data'].change(
            fn=lambda profiles_data: gr.Dropdown(choices=[p['name'] for p in profiles_data] if profiles_data else [], value=None),
            inputs=[participant_components['profiles_data']],
            outputs=[participant_components['individual_profile']]
        )
        
        # Individual management handlers
        participant_components['add_individual_btn'].click(
            fn=add_individual,
            inputs=[
                participant_components['individual_name'],
                participant_components['individual_vote_value'],
                participant_components['individual_profile'],
                participant_components['individual_role'],
                participant_components['individuals_data'],
                participant_components['profiles_data'],    # For profile dropdown choices
                participant_components['roles_text']        # For role dropdown choices
            ],
            outputs=[
                participant_components['individuals_data'],
                participant_components['individuals_display'],
                participant_components['individual_name'],       # Clear name field
                participant_components['individual_vote_value'], # Reset vote value
                participant_components['individual_profile'],    # Update profile dropdown
                participant_components['individual_role']        # Update role dropdown
            ]
        )
        
        participant_components['clear_individuals_btn'].click(
            fn=clear_individuals,
            outputs=[
                participant_components['individuals_data'],
                participant_components['individuals_display']
            ]
        )
        
        # Agent management handlers
        participant_components['add_agent_btn'].click(
            fn=add_agent,
            inputs=[
                participant_components['agent_name'],
                participant_components['agent_confidence'],
                participant_components['agent_autonomy_level'],
                participant_components['agent_explainability'],
                participant_components['agent_role'],
                participant_components['agents_data'],
                participant_components['roles_text']        # For role dropdown choices
            ],
            outputs=[
                participant_components['agents_data'],
                participant_components['agents_display'],
                participant_components['agent_name'],           # Clear name field
                participant_components['agent_confidence'],     # Clear confidence field
                participant_components['agent_autonomy_level'], # Clear autonomy level field
                participant_components['agent_explainability'], # Clear explainability field
                participant_components['agent_role']            # Update role dropdown
            ]
        )
        
        participant_components['clear_agents_btn'].click(
            fn=clear_agents,
            outputs=[
                participant_components['agents_data'],
                participant_components['agents_display']
            ]
        )
        
        # Update individual and agent dropdowns when roles text changes
        participant_components['roles_text'].change(
            fn=update_individual_dropdowns,
            inputs=[
                participant_components['roles_text'],
                participant_components['profiles_data']
            ],
            outputs=[
                participant_components['individual_profile'],
                participant_components['individual_role']
            ]
        )
        
        # Update agent role dropdown when roles text changes
        participant_components['roles_text'].change(
            fn=update_agent_role_dropdown,
            inputs=[participant_components['roles_text']],
            outputs=[participant_components['agent_role']]
        )
        
        # Update policy scope dropdown when scope definitions change
        for scope_component in [scope_components['projects_text'], scope_components['activities_text'], scope_components['tasks_text']]:
            scope_component.change(
                fn=update_scope_dropdown,
                inputs=[
                    scope_components['projects_text'],
                    scope_components['activities_text'],
                    scope_components['tasks_text']
                ],
                outputs=[policy_components['policy_scope']]
            )
        
        # Update policy participants dropdown when participant definitions change
        for participant_component in [participant_components['roles_text'], participant_components['individuals_data'], participant_components['agents_data']]:
            participant_component.change(
                fn=update_participant_dropdown,
                inputs=[
                    participant_components['roles_text'],
                    participant_components['individuals_data'],
                    participant_components['agents_data']
                ],
                outputs=[
                    policy_components['policy_participants'],
                    policy_components['veto_participants'],
                    policy_components['excluded_participants']
                ]
            )
        
        # Update policy-specific attribute visibility when policy type changes
        policy_components['policy_type'].change(
            fn=update_policy_type_visibility,
            inputs=[policy_components['policy_type']],
            outputs=[
                policy_components['default_decision'],
                policy_components['fallback_policy'],
                policy_components['voting_ratio']
            ]
        )
        
        # Update decision options visibility when decision type changes
        policy_components['decision_type'].change(
            fn=update_decision_options_visibility,
            inputs=[policy_components['decision_type']],
            outputs=[policy_components['decision_options']]
        )
        
        # Update condition field visibility when condition type changes
        policy_components['condition_type'].change(
            fn=update_condition_visibility,
            inputs=[policy_components['condition_type']],
            outputs=[
                policy_components['veto_participants'],
                policy_components['excluded_participants'],
                policy_components['min_participants'],
                policy_components['deadline_offset_value'],
                policy_components['deadline_offset_unit'],
                policy_components['deadline_date'],
                policy_components['min_decision_offset_value'],
                policy_components['min_decision_offset_unit'],
                policy_components['min_decision_date'],
                policy_components['label_condition_type'],
                policy_components['label_condition_operator'],
                policy_components['label_condition_labels']
            ]
        )
        
        # Policy management handlers
        policy_components['add_policy_btn'].click(
            fn=add_policy_and_clear_form,
            inputs=[
                policy_components['policy_name'],
                policy_components['policy_type'],
                policy_components['policy_scope'],
                policy_components['policy_participants'],
                policy_components['decision_type'],
                policy_components['decision_options'],
                policy_components['voting_ratio'],
                policy_components['default_decision'],
                policy_components['fallback_policy'],
                policy_components['condition_type'],
                policy_components['veto_participants'],
                policy_components['excluded_participants'],
                policy_components['min_participants'],
                policy_components['deadline_offset_value'],
                policy_components['deadline_offset_unit'],
                policy_components['deadline_date'],
                policy_components['min_decision_offset_value'],
                policy_components['min_decision_offset_unit'],
                policy_components['min_decision_date'],
                policy_components['label_condition_type'],
                policy_components['label_condition_operator'],
                policy_components['label_condition_labels'],
                policy_components['added_conditions_list'],
                policy_components['policies_data']
            ],
            outputs=[
                policy_components['policies_data'],
                policy_components['policies_display'],
                policy_components['policy_name'],        # Clear/keep name field
                policy_components['policy_type'],        # Reset/keep policy type
                policy_components['policy_scope'],       # Clear/keep scope
                policy_components['policy_participants'], # Clear/keep participants - use component, not new dropdown
                policy_components['decision_type'],      # Reset/keep decision type
                policy_components['decision_options'],   # Clear/keep decision options
                policy_components['voting_ratio'],       # Reset/keep voting ratio
                policy_components['default_decision'],   # Update/keep default decision
                policy_components['fallback_policy'],    # Update/keep fallback policy
                policy_components['condition_type'],     # Clear/keep condition type
                policy_components['veto_participants'],  # Clear/keep veto participants
                policy_components['excluded_participants'], # Clear/keep excluded participants
                policy_components['min_participants'],   # Reset/keep min participants
                policy_components['deadline_offset_value'], # Reset/keep deadline offset value
                policy_components['deadline_offset_unit'], # Reset/keep deadline offset unit
                policy_components['deadline_date'],      # Reset/keep deadline date
                policy_components['min_decision_offset_value'], # Reset/keep min decision offset value
                policy_components['min_decision_offset_unit'], # Reset/keep min decision offset unit
                policy_components['min_decision_date'],  # Reset/keep min decision date
                policy_components['label_condition_type'], # Reset/keep label condition type
                policy_components['label_condition_operator'], # Reset/keep label operator
                policy_components['label_condition_labels'], # Clear/keep label condition labels
                policy_components['added_conditions_list'] # Clear/keep added conditions list
            ]
        )
        
        policy_components['clear_policies_btn'].click(
            fn=clear_policies,
            outputs=[
                policy_components['policies_data'],
                policy_components['policies_display']
            ]
        )
        
        # Condition management handlers
        policy_components['add_condition_btn'].click(
            fn=add_condition,
            inputs=[
                policy_components['condition_type'],
                policy_components['veto_participants'],
                policy_components['excluded_participants'],
                policy_components['min_participants'],
                policy_components['deadline_offset_value'],
                policy_components['deadline_offset_unit'],
                policy_components['deadline_date'],
                policy_components['min_decision_offset_value'],
                policy_components['min_decision_offset_unit'],
                policy_components['min_decision_date'],
                policy_components['label_condition_type'],
                policy_components['label_condition_operator'],
                policy_components['label_condition_labels'],
                policy_components['added_conditions_list']
            ],
            outputs=[
                policy_components['added_conditions_list'],      # success/error message
                policy_components['condition_type'],            # reset dropdown
                policy_components['veto_participants'],         # reset multiselect
                policy_components['excluded_participants'],     # reset multiselect
                policy_components['min_participants'],          # reset number
                policy_components['deadline_offset_value'],     # reset number
                policy_components['deadline_offset_unit'],      # reset dropdown
                policy_components['deadline_date'],             # reset textbox
                policy_components['min_decision_offset_value'], # reset number
                policy_components['min_decision_offset_unit'],  # reset dropdown
                policy_components['min_decision_date'],         # reset textbox
                policy_components['label_condition_type'],      # reset dropdown
                policy_components['label_condition_operator'],  # reset textbox
                policy_components['label_condition_labels']     # reset textbox
            ]
        )
        
        policy_components['clear_conditions_btn'].click(
            fn=clear_conditions,
            outputs=[
                policy_components['added_conditions_list']
            ]
        )
        
        # Update policy reference dropdowns when policies change
        policy_components['policies_data'].change(
            fn=update_policy_reference_dropdowns,
            inputs=[
                policy_components['policies_data'],
                policy_components['policy_scope']
            ],
            outputs=[
                policy_components['default_decision'],
                policy_components['fallback_policy']
            ]
        )
        
        # Update policy reference dropdowns when policy scope changes (and clear current selections)
        policy_components['policy_scope'].change(
            fn=update_policy_reference_dropdowns_on_scope_change,
            inputs=[
                policy_components['policies_data'],
                policy_components['policy_scope']
            ],
            outputs=[
                policy_components['default_decision'],
                policy_components['fallback_policy']
            ]
        )
        
        # Composed Policy management handlers
        policy_components['add_phase_btn'].click(
            fn=add_phase,
            inputs=[
                policy_components['phase_name'],
                policy_components['phase_type'],
                policy_components['phase_participants'],
                policy_components['phase_decision_type'],
                policy_components['phase_decision_options'],
                policy_components['phase_voting_ratio'],
                policy_components['phase_default_decision'],
                policy_components['phase_fallback_policy'],
                policy_components['added_phases_list']
            ],
            outputs=[
                policy_components['added_phases_list'],
                policy_components['phase_name'],
                policy_components['phase_type'],
                policy_components['phase_participants'],
                policy_components['phase_decision_type'],
                policy_components['phase_decision_options'],
                policy_components['phase_voting_ratio'],
                policy_components['phase_default_decision'],
                policy_components['phase_fallback_policy']
            ]
        )
        
        policy_components['clear_phases_btn'].click(
            fn=clear_phases,
            outputs=[
                policy_components['added_phases_list']
            ]
        )
        
        policy_components['add_composed_policy_btn'].click(
            fn=add_composed_policy_and_clear_form,
            inputs=[
                policy_components['composed_policy_name'],
                policy_components['composed_policy_scope'],
                policy_components['execution_type'],
                policy_components['require_all'],
                policy_components['carry_over'],
                policy_components['added_phases_list'],
                policy_components['composed_policies_data']
            ],
            outputs=[
                policy_components['composed_policies_data'],
                policy_components['composed_policies_display'],
                policy_components['composed_policy_name'],
                policy_components['composed_policy_scope'],
                policy_components['execution_type'],
                policy_components['require_all'],
                policy_components['carry_over'],
                policy_components['added_phases_list']
            ]
        )
        
        policy_components['clear_composed_policies_btn'].click(
            fn=clear_composed_policies,
            outputs=[
                policy_components['composed_policies_data'],
                policy_components['composed_policies_display']
            ]
        )
        
        # Update phase participant dropdown when participant definitions change
        for participant_component in [participant_components['roles_text'], participant_components['individuals_data'], participant_components['agents_data']]:
            participant_component.change(
                fn=update_phase_participant_dropdown,
                inputs=[
                    participant_components['roles_text'],
                    participant_components['individuals_data'],
                    participant_components['agents_data']
                ],
                outputs=[
                    policy_components['phase_participants']
                ]
            )
        
        # Update phase policy type visibility when phase type changes
        policy_components['phase_type'].change(
            fn=update_policy_type_visibility,
            inputs=[policy_components['phase_type']],
            outputs=[
                policy_components['phase_default_decision'],
                policy_components['phase_fallback_policy'],
                policy_components['phase_voting_ratio']
            ]
        )
        
        # Update phase decision options visibility when phase decision type changes
        policy_components['phase_decision_type'].change(
            fn=update_decision_options_visibility,
            inputs=[policy_components['phase_decision_type']],
            outputs=[policy_components['phase_decision_options']]
        )
        
        # Update composed policy scope dropdown when scope definitions change
        for scope_component in [scope_components['projects_text'], scope_components['activities_text'], scope_components['tasks_text']]:
            scope_component.change(
                fn=update_scope_dropdown,
                inputs=[
                    scope_components['projects_text'],
                    scope_components['activities_text'],
                    scope_components['tasks_text']
                ],
                outputs=[policy_components['composed_policy_scope']]
            )
        
        # Set up change handlers for preview updates
        preview_components = []
        preview_components.extend(scope_components.values())
        preview_components.extend([
            participant_components['profiles_data'],
            participant_components['roles_text'],
            participant_components['individuals_data'],
            participant_components['agents_data']
        ])
        # Include both single policies and composed policies data for preview
        preview_components.append(policy_components['policies_data'])
        preview_components.append(policy_components['composed_policies_data'])
        
        for component in preview_components:
            if hasattr(component, 'change'):
                component.change(
                    fn=update_preview,
                    inputs=preview_components,
                    outputs=self.preview_code
                )
        
        # Load example button
        if hasattr(self, '_create_preview_panel'):
            # This will be connected properly when we have the preview panel components
            pass
    
    def _generate_dsl_from_form(self, *form_values):
        """Generate DSL code from form inputs"""
        # Extract form values (in the order they appear in the interface)
        (projects_text, activities_text, tasks_text, profiles_data, roles_text, individuals_data, agents_data,
         policies_data, composed_policies_data) = form_values
        
        dsl_parts = []
        
        # Parse multi-line inputs
        projects = self._parse_projects(projects_text)
        activities = self._parse_activities(activities_text)
        tasks = self._parse_tasks(tasks_text)
        profiles = profiles_data if profiles_data else []  # profiles_data is already structured
        individuals = individuals_data if individuals_data else []  # individuals_data is already structured
        agents = agents_data if agents_data else []  # agents_data is already structured
        
        # Generate Scopes section
        scope_parts = []
        
        # Get all project names (explicit + implicit from activity parents)
        explicit_project_names = {p['name'] for p in projects}
        implicit_project_names = {a['parent'] for a in activities if a['parent'] and a['parent'] not in explicit_project_names}
        all_project_names = explicit_project_names | implicit_project_names
        
        # Get all activity names (explicit + implicit from task parents)
        explicit_activity_names = {a['name'] for a in activities}
        implicit_activity_names = {t['parent'] for t in tasks if t['parent'] and t['parent'] not in explicit_activity_names and t['parent'] not in all_project_names}
        all_activity_names = explicit_activity_names | implicit_activity_names
        
        # Generate Projects with their hierarchical structure
        if all_project_names:
            scope_parts.append("    Projects :")
        
        for project_name in all_project_names:
            # Get explicit project info if available
            explicit_project = next((p for p in projects if p['name'] == project_name), None)
            
            if explicit_project and explicit_project['platform']:
                scope_parts.append(f"        Project {project_name} from {explicit_project['platform']} : {explicit_project['repo']} {{")
            else:
                scope_parts.append(f"        Project {project_name} {{")
            
            # Find activities belonging to this project
            project_activities = [a for a in activities if a['parent'] == project_name]
            if project_activities:
                scope_parts.append("            activities :")
                for activity in project_activities:
                    scope_parts.append(f"                {activity['name']} {{")
                    
                    # Find tasks belonging to this activity
                    activity_tasks = [t for t in tasks if t['parent'] == activity['name']]
                    if activity_tasks:
                        scope_parts.append("                    tasks :")
                        for task in activity_tasks:
                            if task['type'] and task['action']:
                                scope_parts.append(f"                        {task['name']} : {task['type']} {{")
                                scope_parts.append(f"                            Action : {task['action']}")
                                scope_parts.append("                        }")
                            elif task['type']:
                                scope_parts.append(f"                        {task['name']} : {task['type']}")
                            else:
                                scope_parts.append(f"                        {task['name']}")
                    
                    scope_parts.append("            }")
            
            scope_parts.append("    }")
        
        # Generate root-level Activities (explicit + implicit from task parents)
        root_activities = [a for a in activities if not a['parent']]
        
        # Add implicit activities referenced by tasks but not explicitly defined
        for implicit_activity_name in implicit_activity_names:
            root_activities.append({'name': implicit_activity_name, 'parent': None})
        
        if root_activities:
            scope_parts.append("    Activities :")
            for activity in root_activities:
                activity_name = activity['name']
                scope_parts.append(f"        {activity_name} {{")
                
                # Find tasks belonging to this activity
                activity_tasks = [t for t in tasks if t['parent'] == activity_name]
                if activity_tasks:
                    scope_parts.append("            tasks :")
                    for task in activity_tasks:
                        if task['type'] and task['action']:
                            scope_parts.append(f"                {task['name']} : {task['type']} {{")
                            scope_parts.append(f"                    Action : {task['action']}")
                            scope_parts.append("                }")
                        elif task['type']:
                            scope_parts.append(f"                {task['name']} : {task['type']}")
                        else:
                            scope_parts.append(f"                {task['name']}")
                
                scope_parts.append("        }")
        
        # Generate root-level Tasks (only tasks with no parent or parent that's a project)
        root_tasks = [t for t in tasks if not t['parent'] or t['parent'] in all_project_names]
        if root_tasks:
            scope_parts.append("    Tasks :")
            for task in root_tasks:
                if task['type'] and task['action']:
                    scope_parts.append(f"        {task['name']} : {task['type']} {{")
                    scope_parts.append(f"            Action : {task['action']}")
                    scope_parts.append("        }")
                elif task['type']:
                    scope_parts.append(f"        {task['name']} : {task['type']}")
                else:
                    scope_parts.append(f"        {task['name']}")
        
        # Add Scopes section if we have any scope content
        if scope_parts:
            dsl_parts.append("Scopes:")
            dsl_parts.extend(scope_parts)
        
        # Generate Participants section
        participants_section = []
        
        # Add Profiles section
        if profiles:
            participants_section.append("    Profiles:")
            for profile in profiles:
                participants_section.append(f"        {profile['name']} {{")
                if profile.get('gender'):
                    participants_section.append(f"            gender : {profile['gender']}")
                if profile.get('race'):
                    participants_section.append(f"            race : {profile['race']}")
                participants_section.append("        }")
        
        # Add Roles section
        if roles_text.strip():
            roles_list = [role.strip() for role in roles_text.split(',') if role.strip()]
            participants_section.append(f"    Roles : {', '.join(roles_list)}")
        
        # Add Individuals section
        if individuals or agents:
            participants_section.append("    Individuals :")
            
            # Add regular individuals
            for individual in individuals:
                line_parts = [f"        {individual['name']}"]
                if individual.get('vote_value') or individual.get('profile') or individual.get('role'):
                    line_parts[0] += " {"
                    attributes = []
                    if individual.get('vote_value'):
                        attributes.append(f"            vote value : {individual['vote_value']}")
                    if individual.get('profile'):
                        attributes.append(f"            profile : {individual['profile']}")
                    if individual.get('role'):
                        attributes.append(f"            role : {individual['role']}")
                    
                    if attributes:
                        participants_section.extend(line_parts)
                        participants_section.extend(attributes)
                        participants_section.append("        },")
                    else:
                        participants_section.append(f"        {individual['name']},")
                else:
                    participants_section.append(f"        {individual['name']},")
            
            # Add agents
            for agent in agents:
                line_parts = [f"        (Agent) {agent['name']}"]
                if any(agent.get(key) for key in ['confidence', 'autonomy_level', 'explainability', 'role']):
                    line_parts[0] += " {"
                    attributes = []
                    if agent.get('confidence'):
                        attributes.append(f"            confidence : {agent['confidence']}")
                    if agent.get('autonomy_level'):
                        attributes.append(f"            autonomy level: {agent['autonomy_level']}")
                    if agent.get('explainability'):
                        attributes.append(f"            explainability: {agent['explainability']}")
                    if agent.get('role'):
                        attributes.append(f"            role : {agent['role']}")
                    
                    if attributes:
                        participants_section.extend(line_parts)
                        participants_section.extend(attributes)
                        participants_section.append("        },")
                    else:
                        participants_section.append(f"        (Agent) {agent['name']},")
                else:
                    participants_section.append(f"        (Agent) {agent['name']},")
        
        if participants_section:
            dsl_parts.append("Participants:")
            dsl_parts.extend(participants_section)
        
        # Generate Policies section
        policies = policies_data if policies_data else []
        for policy in policies:
            if policy.get('name') and policy.get('type'):
                policy_type = policy['type']
                policy_name = policy['name']
                
                dsl_parts.append(f"{policy_type} {policy_name} {{")
                
                if policy.get('scope'):
                    dsl_parts.append(f"    Scope: {policy['scope']}")
                
                if policy.get('decision_type'):
                    if policy.get('decision_options') and policy['decision_type'] in ["StringList", "ElementList"]:
                        dsl_parts.append(f"    DecisionType as {policy['decision_type']} : {policy['decision_options']}")
                    else:
                        dsl_parts.append(f"    DecisionType as {policy['decision_type']}")
                
                if policy.get('participants'):
                    # Handle multiselect participants
                    if isinstance(policy['participants'], list):
                        participants = [p.strip() for p in policy['participants'] if p.strip()]
                    else:
                        participants = [p.strip() for p in str(policy['participants']).split(',') if p.strip()]
                    if participants:
                        dsl_parts.append(f"    Participant list : {', '.join(participants)}")
                
                # Parameters
                parameters = []
                if policy_type in ["MajorityPolicy", "AbsoluteMajorityPolicy", "VotingPolicy"] and policy.get('voting_ratio'):
                    parameters.append(f"        ratio: {policy['voting_ratio']}")
                
                # Add default decision for LeaderDrivenPolicy
                if policy_type == "LeaderDrivenPolicy" and policy.get('default_decision'):
                    parameters.append(f"        default: {policy['default_decision']}")
                
                # Add fallback policy for ConsensusPolicy and LazyConsensusPolicy
                if policy_type in ["ConsensusPolicy", "LazyConsensusPolicy"] and policy.get('fallback_policy'):
                    parameters.append(f"        fallback: {policy['fallback_policy']}")
                
                if parameters:
                    dsl_parts.append("    Parameters:")
                    dsl_parts.extend(parameters)
                
                # Add conditions
                conditions = []
                
                # Use the dynamically added conditions if available
                if policy.get('added_conditions'):
                    condition_lines = [line.strip() for line in policy['added_conditions'].split('\n') if line.strip()]
                    for condition_line in condition_lines:
                        # Convert from display format to DSL format
                        if condition_line.startswith('VetoRight:'):
                            conditions.append(f"        {condition_line.replace(':', ' :')}")
                        elif condition_line.startswith('ParticipantExclusion:'):
                            conditions.append(f"        {condition_line.replace(':', ' :')}")
                        elif condition_line.startswith('MinParticipants:'):
                            conditions.append(f"        {condition_line.replace(':', ' :')}")
                        elif condition_line.startswith('Deadline:'):
                            condition_content = condition_line.split(':', 1)[1].strip()
                            conditions.append(f"        Deadline : {condition_content}")
                        elif condition_line.startswith('MinDecisionTime:'):
                            condition_content = condition_line.split(':', 1)[1].strip()
                            conditions.append(f"        MinDecisionTime : {condition_content}")
                        elif condition_line.startswith('LabelCondition'):
                            # Parse LabelCondition format: "LabelCondition pre not : label1, label2"
                            condition_content = condition_line.split(':', 1)[1].strip()
                            condition_prefix = condition_line.split(':', 1)[0].strip()
                            conditions.append(f"        {condition_prefix} : {condition_content}")
                
                # Fallback to single condition fields for backward compatibility
                elif policy.get('condition_type'):
                    condition_type = policy['condition_type']
                    
                    if condition_type == "VetoRight" and policy.get('veto_participants'):
                        if isinstance(policy['veto_participants'], list):
                            veto_list = ', '.join(policy['veto_participants'])
                        else:
                            veto_list = str(policy['veto_participants'])
                        conditions.append(f"        VetoRight : {veto_list}")
                    
                    elif condition_type == "ParticipantExclusion" and policy.get('excluded_participants'):
                        if isinstance(policy['excluded_participants'], list):
                            exclusion_list = ', '.join(policy['excluded_participants'])
                        else:
                            exclusion_list = str(policy['excluded_participants'])
                        conditions.append(f"        ParticipantExclusion : {exclusion_list}")
                    
                    elif condition_type == "MinParticipants" and policy.get('min_participants'):
                        conditions.append(f"        MinParticipants : {policy['min_participants']}")
                    
                    elif condition_type == "Deadline":
                        deadline_parts = []
                        if policy.get('deadline_offset_value') and policy.get('deadline_offset_unit'):
                            deadline_parts.append(f"{policy['deadline_offset_value']} {policy['deadline_offset_unit']}")
                        if policy.get('deadline_date') and policy['deadline_date'].strip():
                            if deadline_parts:
                                deadline_parts.append(f", {policy['deadline_date']}")
                            else:
                                deadline_parts.append(policy['deadline_date'])
                        if deadline_parts:
                            conditions.append(f"        Deadline policy_deadline : {''.join(deadline_parts)}")
                    
                    elif condition_type == "MinDecisionTime":
                        min_decision_parts = []
                        if policy.get('min_decision_offset_value') and policy.get('min_decision_offset_unit'):
                            min_decision_parts.append(f"{policy['min_decision_offset_value']} {policy['min_decision_offset_unit']}")
                        if policy.get('min_decision_date') and policy['min_decision_date'].strip():
                            if min_decision_parts:
                                min_decision_parts.append(f", {policy['min_decision_date']}")
                            else:
                                min_decision_parts.append(policy['min_decision_date'])
                        if min_decision_parts:
                            conditions.append(f"        MinDecisionTime min_time_id : {''.join(min_decision_parts)}")
                    
                    elif condition_type == "LabelCondition" and policy.get('label_condition_labels'):
                        label_type = policy.get('label_condition_type', 'pre')
                        label_operator = policy.get('label_condition_operator', '')
                        labels = policy['label_condition_labels']
                        
                        if label_operator:
                            conditions.append(f"        LabelCondition {label_type} {label_operator} : {labels}")
                        else:
                            conditions.append(f"        LabelCondition {label_type} : {labels}")
                
                if conditions:
                    dsl_parts.append("    Conditions:")
                    dsl_parts.extend(conditions)
                
                dsl_parts.append("}")
        
        # Generate Composed Policies section
        composed_policies = composed_policies_data if composed_policies_data else []
        for composed_policy in composed_policies:
            if composed_policy.get('name') and composed_policy.get('type') == 'ComposedPolicy':
                policy_name = composed_policy['name']
                
                dsl_parts.append(f"ComposedPolicy {policy_name} {{")
                
                if composed_policy.get('scope'):
                    dsl_parts.append(f"    Scope: {composed_policy['scope']}")
                
                # Add execution order configuration
                if composed_policy.get('execution_type') or composed_policy.get('require_all') is not None or composed_policy.get('carry_over') is not None:
                    dsl_parts.append("    Order:")
                    
                    if composed_policy.get('execution_type'):
                        dsl_parts.append(f"        Execution: {composed_policy['execution_type']}")
                    
                    if composed_policy.get('require_all') is not None:
                        require_val = "true" if composed_policy['require_all'] else "false"
                        dsl_parts.append(f"        RequireAll: {require_val}")
                    
                    if composed_policy.get('carry_over') is not None:
                        carry_val = "true" if composed_policy['carry_over'] else "false"
                        dsl_parts.append(f"        CarryOver: {carry_val}")
                
                # Add phases
                if composed_policy.get('phases'):
                    dsl_parts.append("    Phases {")
                    
                    for phase_display in composed_policy['phases']:
                        # Parse phase from display format: "PhaseName (PolicyType) → participants: p1, p2"
                        if ' (' in phase_display and ') →' in phase_display:
                            # Extract phase name and type
                            name_part = phase_display.split(' (')[0].strip()
                            type_part = phase_display.split(' (')[1].split(')')[0].strip()
                            
                            # Extract participants and details from display format
                            participants_part = ""
                            decision_type = "BooleanDecision"  # default
                            ratio = None
                            default_decision = None
                            fallback_policy = None
                            options = None
                            
                            # Parse the display string more carefully
                            if 'participants: ' in phase_display:
                                after_participants = phase_display.split('participants: ')[1]
                                
                                # Extract participants (everything before the first comma with a keyword)
                                if ', decision:' in after_participants:
                                    participants_part = after_participants.split(', decision:')[0]
                                elif ', ratio:' in after_participants:
                                    participants_part = after_participants.split(', ratio:')[0]
                                elif ', default:' in after_participants:
                                    participants_part = after_participants.split(', default:')[0]
                                elif ', fallback:' in after_participants:
                                    participants_part = after_participants.split(', fallback:')[0]
                                elif ', options:' in after_participants:
                                    participants_part = after_participants.split(', options:')[0]
                                else:
                                    participants_part = after_participants
                            
                            # Extract parameters from the details section
                            if ', decision: ' in phase_display:
                                decision_type = phase_display.split(', decision: ')[1].split(',')[0].strip()
                            
                            if ', ratio: ' in phase_display:
                                ratio = phase_display.split(', ratio: ')[1].split(',')[0].strip()
                            
                            if ', default: ' in phase_display:
                                default_decision = phase_display.split(', default: ')[1].split(',')[0].strip()
                            
                            if ', fallback: ' in phase_display:
                                fallback_policy = phase_display.split(', fallback: ')[1].split(',')[0].strip()
                            
                            if ', options: ' in phase_display:
                                options = phase_display.split(', options: ')[1].strip()
                            
                            # Generate DSL for this phase
                            dsl_parts.append(f"        {type_part} {name_part} {{")
                            dsl_parts.append(f"            DecisionType as {decision_type}")
                            
                            if participants_part:
                                participants_list = [p.strip() for p in participants_part.split(',')]
                                dsl_parts.append(f"            Participant list: {', '.join(participants_list)}")
                            
                            # Add parameters section if any parameters exist
                            parameters = []
                            if ratio:
                                parameters.append(f"                ratio: {ratio}")
                            if default_decision:
                                parameters.append(f"                default: {default_decision}")
                            if fallback_policy:
                                parameters.append(f"                fallback: {fallback_policy}")
                            if options:
                                parameters.append(f"                options: {options}")
                            
                            if parameters:
                                dsl_parts.append("            Parameters:")
                                dsl_parts.extend(parameters)
                            
                            dsl_parts.append("        }")
                    
                    dsl_parts.append("    }")
                
                dsl_parts.append("}")
        
        return '\n'.join(dsl_parts) if dsl_parts else "# Fill the form to generate DSL code"

    def _parse_projects(self, projects_text):
        """Parse projects from multi-line text format"""
        projects = []
        if not projects_text.strip():
            return projects
            
        for line in projects_text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
                
            parts = [p.strip() for p in line.split('|')]
            project = {
                'name': parts[0] if parts else '',
                'platform': parts[1] if len(parts) > 1 and parts[1] else None,
                'repo': parts[2] if len(parts) > 2 and parts[2] else None
            }
            if project['name']:
                projects.append(project)
        
        return projects
    
    def _parse_activities(self, activities_text):
        """Parse activities from multi-line text format"""
        activities = []
        if not activities_text.strip():
            return activities
            
        for line in activities_text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
                
            parts = [p.strip() for p in line.split('|')]
            activity = {
                'name': parts[0] if parts else '',
                'parent': parts[1] if len(parts) > 1 and parts[1] else None
            }
            if activity['name']:
                activities.append(activity)
        
        return activities
    
    def _parse_tasks(self, tasks_text):
        """Parse tasks from multi-line text format: TaskName | Parent | Type | Action"""
        tasks = []
        if not tasks_text.strip():
            return tasks
            
        for line in tasks_text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
                
            parts = [p.strip() for p in line.split('|')]
            task = {
                'name': parts[0] if parts else '',
                'parent': parts[1] if len(parts) > 1 and parts[1] else None,
                'type': parts[2] if len(parts) > 2 and parts[2] else None,
                'action': parts[3] if len(parts) > 3 and parts[3] else None
            }
            if task['name']:
                tasks.append(task)
        
        return tasks


    
    def _format_individuals_display(self, individuals):
        """Format individuals for display in the text area"""
        if not individuals:
            return "No individuals added yet"
        
        display_lines = [f"👥 {len(individuals)} individual(s) defined:", ""]
        for i, individual in enumerate(individuals, 1):
            line = f"{i}. {individual['name']}"
            attributes = []
            if individual.get('vote_value'):
                attributes.append(f"🗳️ vote: {individual['vote_value']}")
            if individual.get('profile'):
                attributes.append(f"📋 profile: {individual['profile']}")
            if individual.get('role'):
                attributes.append(f"👔 role: {individual['role']}")
            
            if attributes:
                line += f" → {', '.join(attributes)}"
            
            display_lines.append(line)
        
        return '\n'.join(display_lines)
    
    def _format_agents_display(self, agents):
        """Format agents for display in the text area"""
        if not agents:
            return "No agents added yet"
        
        display_lines = [f"🤖 {len(agents)} agent(s) defined:", ""]
        for i, agent in enumerate(agents, 1):
            line = f"{i}. {agent['name']}"
            attributes = []
            if agent.get('confidence') is not None:
                attributes.append(f"🔍 confidence: {agent['confidence']}")
            if agent.get('autonomy_level') is not None:
                attributes.append(f"⚡ autonomy: {agent['autonomy_level']}")
            if agent.get('explainability') is not None:
                attributes.append(f"💡 explainability: {agent['explainability']}")
            if agent.get('role'):
                attributes.append(f"👔 role: {agent['role']}")
            
            if attributes:
                line += f" → {', '.join(attributes)}"
            
            display_lines.append(line)
        
        return '\n'.join(display_lines)
    
    def _parse_agents(self, agents_text):
        """Parse agents from multi-line text format: Name | confidence | autonomy_level | explainability | role"""
        agents = []
        if not agents_text.strip():
            return agents
            
        for line in agents_text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
                
            parts = [p.strip() for p in line.split('|')]
            agent = {'name': parts[0]}
            
            if len(parts) > 1 and parts[1]:
                try:
                    agent['confidence'] = float(parts[1])
                except ValueError:
                    pass  # Skip invalid confidence values
                    
            if len(parts) > 2 and parts[2]:
                try:
                    agent['autonomy_level'] = float(parts[2])
                except ValueError:
                    pass  # Skip invalid autonomy level values
                    
            if len(parts) > 3 and parts[3]:
                try:
                    agent['explainability'] = float(parts[3])
                except ValueError:
                    pass  # Skip invalid explainability values
                    
            if len(parts) > 4 and parts[4]:
                agent['role'] = parts[4]
                
            agents.append(agent)
        
        return agents

    def _format_profiles_display(self, profiles):
        """Format profiles for display in the text area"""
        if not profiles:
            return "No profiles added yet"
        
        display_lines = [f"📊 {len(profiles)} profile(s) defined:", ""]
        for i, profile in enumerate(profiles, 1):
            line = f"{i}. {profile['name']}"
            attributes = []
            if profile.get('gender'):
                attributes.append(f"👤 gender: {profile['gender']}")
            if profile.get('race'):
                attributes.append(f"🌍 race: {profile['race']}")
            
            if attributes:
                line += f" → {', '.join(attributes)}"
            
            display_lines.append(line)
        
        return '\n'.join(display_lines)
    
    def _extract_scope_names(self, projects_text, activities_text, tasks_text):
        """Extract all scope names (projects, activities, tasks) for dropdown choices"""
        scope_names = []
        
        # Parse and extract project names
        projects = self._parse_projects(projects_text)
        for project in projects:
            if project['name']:
                scope_names.append(project['name'])
        
        # Parse and extract activity names
        activities = self._parse_activities(activities_text)
        for activity in activities:
            if activity['name']:
                scope_names.append(activity['name'])
        
        # Parse and extract task names
        tasks = self._parse_tasks(tasks_text)
        for task in tasks:
            if task['name']:
                scope_names.append(task['name'])
        
        return sorted(list(set(scope_names)))  # Remove duplicates and sort
    
    def _extract_participant_names(self, roles_text, individuals_data, agents_data):
        """Extract all participant names (roles, individuals, agents) for dropdown choices"""
        participant_names = []
        
        # Extract role names
        if roles_text.strip():
            roles = [role.strip() for role in roles_text.split(',') if role.strip()]
            participant_names.extend(roles)
        
        # Extract individual names
        if individuals_data:
            for individual in individuals_data:
                if individual.get('name'):
                    participant_names.append(individual['name'])
        
        # Extract agent names
        if agents_data:
            for agent in agents_data:
                if agent.get('name'):
                    participant_names.append(f"(Agent) {agent['name']}")
        
        return sorted(list(set(participant_names)))  # Remove duplicates and sort
    
    def _format_policies_display(self, policies):
        """Format policies for display in the text area"""
        if not policies:
            return "No policies added yet"
        
        display_lines = [f"📋 {len(policies)} policy(ies) defined:", ""]
        for i, policy in enumerate(policies, 1):
            line = f"{i}. {policy['name']} ({policy['type']})"
            
            details = []
            if policy.get('scope'):
                details.append(f"🎯 scope: {policy['scope']}")
            if policy.get('participants'):
                participant_list = policy['participants'] if isinstance(policy['participants'], list) else [policy['participants']]
                details.append(f"👥 participants: {', '.join(participant_list)}")
            if policy.get('decision_type'):
                details.append(f"🔹 decision: {policy['decision_type']}")
            
            # Add type-specific parameters
            if policy['type'] in ["MajorityPolicy", "AbsoluteMajorityPolicy", "VotingPolicy"] and policy.get('voting_ratio'):
                details.append(f"📊 ratio: {policy['voting_ratio']}")
            if policy['type'] == "LeaderDrivenPolicy" and policy.get('default_decision'):
                details.append(f"⚡ default: {policy['default_decision']}")
            if policy['type'] == "ConsensusPolicy" and policy.get('fallback_policy'):
                details.append(f"🔄 fallback: {policy['fallback_policy']}")
            
            if details:
                line += f" → {', '.join(details)}"
            
            display_lines.append(line)
        
        return '\n'.join(display_lines)
    
    def _format_composed_policies_display(self, composed_policies):
        """Format composed policies for display in the text area"""
        if not composed_policies:
            return "No composed policies added yet"
        
        display_lines = [f"🔄 {len(composed_policies)} composed policy(ies) defined:", ""]
        for i, policy in enumerate(composed_policies, 1):
            line = f"{i}. {policy['name']} (ComposedPolicy)"
            
            details = []
            if policy.get('scope'):
                details.append(f"🎯 scope: {policy['scope']}")
            if policy.get('execution_type'):
                details.append(f"⚙️ execution: {policy['execution_type']}")
            if policy.get('require_all') is not None:
                details.append(f"✅ require all: {'yes' if policy['require_all'] else 'no'}")
            if policy.get('carry_over') is not None:
                details.append(f"📄 carry over: {'yes' if policy['carry_over'] else 'no'}")
            if policy.get('phases'):
                phases_count = len(policy['phases'])
                phases_list = ', '.join(policy['phases'][:3])  # Show first 3 phases
                if phases_count > 3:
                    phases_list += f" (+{phases_count - 3} more)"
                details.append(f"📋 phases ({phases_count}): {phases_list}")
            
            if details:
                line += f" → {', '.join(details)}"
            
            display_lines.append(line)
        
        return '\n'.join(display_lines)


def main():
    """Main function to run the Gradio interface"""
    builder = GovernanceFormBuilder()
    interface = builder.create_interface()
    
    return interface

if __name__ == "__main__":
    interface = main()
    interface.launch(
        server_name="localhost",
        server_port=7860,
        share=False,
        debug=True
    )