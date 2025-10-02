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
            gr.Markdown("*Format: One per line as `Name | confidence | autonomy_level | explainability | role` (all optional except Name)*")
            gr.Markdown("*Examples:*")
            gr.Markdown("- `k8s-ci-robot` (minimal)")
            gr.Markdown("- `dependabot | 0.9` (with confidence)")
            gr.Markdown("- `security-bot | 0.8 | 0.9 | 1.0 | reviewer` (full definition)")
            
            agents_text = gr.Textbox(
                label="Agents",
                placeholder="k8s-ci-robot\ndependabot | 0.9\nsecurity-bot | 0.8 | 0.9 | 1.0 | reviewer",
                lines=4,
                info="Define automated systems that participate in decisions"
            )
        
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
            'agents_text': agents_text
        }
    
    def _create_policy_forms(self):
        """Create forms for defining policies"""
        gr.Markdown("## Define Governance Policies")
        gr.Markdown("Configure the decision-making rules for your project.")
        
        with gr.Accordion("Policy Basic Information", open=True):
            policy_name = gr.Textbox(
                label="Policy Name",
                placeholder="e.g., pr_merge_policy",
                info="A unique name for this policy"
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
            
            policy_scope = gr.Textbox(
                label="Policy Scope",
                placeholder="e.g., TestTask",
                info="The task/activity this policy applies to"
            )
        
        with gr.Accordion("Policy Configuration", open=True):
            # Participants for this policy
            policy_participants = gr.Textbox(
                label="Policy Participants",
                placeholder="e.g., Reviewers, Approvers",
                info="Comma-separated list of roles/individuals"
            )
            
            # Decision type
            decision_type = gr.Dropdown(
                label="Decision Type",
                choices=["BooleanDecision", "StringList", "ElementList"],
                value="BooleanDecision"
            )
            
            # Parameters (for voting policies)
            voting_ratio = gr.Slider(
                label="Voting Ratio",
                minimum=0.0,
                maximum=1.0,
                value=1.0,
                step=0.1,
                info="Required ratio of positive votes (1.0 = unanimous)"
            )
        
        with gr.Accordion("Conditions", open=False):
            gr.Markdown("### Policy Conditions")
            
            # Minimum participants
            min_participants = gr.Number(
                label="Minimum Participants",
                value=1,
                minimum=1,
                info="Minimum number of participants required"
            )
            
            # Deadline
            deadline_days = gr.Number(
                label="Deadline (days)",
                value=0,
                minimum=0,
                info="Time limit for decision (0 = no deadline)"
            )
            
            # Participant exclusions
            exclusions = gr.Textbox(
                label="Participant Exclusions",
                placeholder="e.g., PRAuthor",
                info="Participants to exclude from this policy"
            )
            
            # Label conditions
            required_labels = gr.Textbox(
                label="Required Labels",
                placeholder="e.g., lgtm, approved",
                info="Labels that must be present"
            )
            
            forbidden_labels = gr.Textbox(
                label="Forbidden Labels", 
                placeholder="e.g., do-not-merge/hold, needs-rebase",
                info="Labels that must NOT be present"
            )
        
        with gr.Accordion("Composed Policy (Multi-phase)", open=False):
            gr.Markdown("### For Complex Multi-Phase Policies")
            
            is_composed = gr.Checkbox(
                label="This is a multi-phase policy",
                value=False
            )
            
            execution_type = gr.Dropdown(
                label="Execution Type",
                choices=["sequential", "parallel"],
                value="sequential"
            )
            
            require_all = gr.Checkbox(
                label="Require All Phases",
                value=True,
                info="Must all phases succeed?"
            )
            
            carry_over = gr.Checkbox(
                label="Carry Over Results",
                value=True,
                info="Pass results between phases?"
            )
        
        return {
            'policy_name': policy_name,
            'policy_type': policy_type,
            'policy_scope': policy_scope,
            'policy_participants': policy_participants,
            'decision_type': decision_type,
            'voting_ratio': voting_ratio,
            'min_participants': min_participants,
            'deadline_days': deadline_days,
            'exclusions': exclusions,
            'required_labels': required_labels,
            'forbidden_labels': forbidden_labels,
            'is_composed': is_composed,
            'execution_type': execution_type,
            'require_all': require_all,
            'carry_over': carry_over
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
                return current_profiles, error_message, "", "", "", gr.Dropdown(choices=[p['name'] for p in current_profiles], value=None)
            
            # Check if profile already exists
            if any(p['name'] == name.strip() for p in current_profiles):
                display_text = self._format_profiles_display(current_profiles)
                error_message = f"❌ Error: Profile name already exists\n\n{display_text}" if current_profiles else "❌ Error: Profile name already exists"
                return current_profiles, error_message, "", "", "", gr.Dropdown(choices=[p['name'] for p in current_profiles], value=None)
            
            # Validate that at least one attribute is provided
            if not gender and not race:
                display_text = self._format_profiles_display(current_profiles)
                error_message = f"❌ Error: Profiles must have either a race or gender value\n\n{display_text}" if current_profiles else "❌ Error: Profiles must have either a race or gender value"
                return current_profiles, error_message, "", "", "", gr.Dropdown(choices=[p['name'] for p in current_profiles], value=None)
            
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
            
            return updated_profiles, success_message, "", "", "", gr.Dropdown(choices=[p['name'] for p in updated_profiles], value=None)  # Also update individual profile dropdown
        
        def clear_profiles():
            """Clear all profiles"""
            return [], "No profiles added yet", gr.Dropdown(choices=[], value=None)
        
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
            
            return updated_individuals, success_message, "", 1.0, gr.Dropdown(choices=profile_choices, value=None), gr.Dropdown(choices=role_choices, value=None)
        
        def clear_individuals():
            """Clear all individuals"""
            return [], "No individuals added yet"
        
        def update_individual_dropdowns(roles_text, current_profiles):
            """Update individual dropdown choices when roles or profiles change"""
            profile_choices = [p['name'] for p in current_profiles] if current_profiles else []
            role_choices = [role.strip() for role in roles_text.split(',') if role.strip()] if roles_text else []
            
            return gr.Dropdown(choices=profile_choices, value=None), gr.Dropdown(choices=role_choices, value=None)
        
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
        
        # Update individual dropdowns when roles text changes
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
        
        # Set up change handlers for preview updates
        preview_components = []
        preview_components.extend(scope_components.values())
        preview_components.extend([
            participant_components['profiles_data'],
            participant_components['roles_text'],
            participant_components['individuals_data'],
            participant_components['agents_text']
        ])
        preview_components.extend(policy_components.values())
        
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
        (projects_text, activities_text, tasks_text, profiles_data, roles_text, individuals_data, agents_text,
         policy_name, policy_type, policy_scope, policy_participants, decision_type, voting_ratio,
         min_participants, deadline_days, exclusions, required_labels,
         forbidden_labels, is_composed, execution_type, require_all, carry_over) = form_values
        
        dsl_parts = []
        
        # Parse multi-line inputs
        projects = self._parse_projects(projects_text)
        activities = self._parse_activities(activities_text)
        tasks = self._parse_tasks(tasks_text)
        profiles = profiles_data if profiles_data else []  # profiles_data is already structured
        individuals = individuals_data if individuals_data else []  # individuals_data is already structured
        agents = self._parse_agents(agents_text)
        
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
        
        # Generate Policy section
        if policy_name and policy_type:
            if is_composed:
                dsl_parts.append(f"ComposedPolicy {policy_name} {{")
            else:
                dsl_parts.append(f"{policy_type} {policy_name} {{")
            
            if policy_scope:
                dsl_parts.append(f"    Scope: {policy_scope}")
            
            if decision_type:
                dsl_parts.append(f"    DecisionType as {decision_type}")
            
            if policy_participants:
                participants = [p.strip() for p in policy_participants.split(',') if p.strip()]
                dsl_parts.append(f"    Participant list : {', '.join(participants)}")
            
            # Conditions
            conditions = []
            if exclusions:
                exclusion_list = [e.strip() for e in exclusions.split(',') if e.strip()]
                conditions.append(f"        ParticipantExclusion : {', '.join(exclusion_list)}")
            
            if min_participants > 1:
                conditions.append(f"        MinParticipants : {int(min_participants)}")
            
            if deadline_days > 0:
                conditions.append(f"        Deadline policy_deadline : {int(deadline_days)} days")
            
            if required_labels:
                label_list = [l.strip() for l in required_labels.split(',') if l.strip()]
                conditions.append(f"        LabelCondition post : {', '.join(label_list)}")
            
            if forbidden_labels:
                forbidden_list = [l.strip() for l in forbidden_labels.split(',') if l.strip()]
                conditions.append(f"        LabelCondition pre not: {', '.join(forbidden_list)}")
            
            if conditions:
                dsl_parts.append("    Conditions:")
                dsl_parts.extend(conditions)
            
            # Parameters
            if policy_type in ["MajorityPolicy", "AbsoluteMajorityPolicy", "VotingPolicy"]:
                dsl_parts.append("    Parameters:")
                dsl_parts.append(f"        ratio: {voting_ratio}")
            
            # Composed policy specifics
            if is_composed:
                dsl_parts.append("    Order :")
                dsl_parts.append(f"        Execution : {execution_type}")
                dsl_parts.append(f"        RequireAll : {'true' if require_all else 'false'}")
                dsl_parts.append(f"        CarryOver : {'true' if carry_over else 'false'}")
                dsl_parts.append("    Phases {")
                dsl_parts.append("        # Add phase definitions here")
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