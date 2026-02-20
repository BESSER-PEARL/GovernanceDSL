"""
Governance DSL Form Builder
A Gradio-based interface for creating governance policies through forms
"""
import gradio as gr
from typing import Optional
import os
from datetime import datetime
import urllib.parse
import copy
import re
import tempfile
                

class GovernanceFormBuilder:
    def __init__(self):
        self.form_data = {
            'scopes': {},
            'participants': {},
            'policies': {}
        }
        # Track added conditions for current policy being edited
        self.current_policy_conditions = []
        # Preview component placeholder (initialized in _create_preview_panel)
        self.preview_code: Optional[gr.Textbox] = None

        self.TEMPLATES = {
            "Simple Majority Vote": {
                "description": (
                    "**Simple Majority Vote** — The most common governance model.\n\n"
                    "Decisions pass when **more than half** of the participating voters approve.\n\n"
                    "Best for: Pull request approvals, routine decisions, community votes."
                ),
                "projects": [{"name": "MyProject", "platform": None, "repo": None}],
                "activities": [],
                "tasks": [],
                "profiles": [],
                "roles": [{"name": "Voter", "vote_value": None}],
                "individuals": [],
                "agents": [],
                "policies": [
                    {
                        "name": "majority_policy",
                        "type": "MajorityPolicy",
                        "scope": "MyProject",
                        "participants": ["Voter"],
                        "decision_type": "BooleanDecision",
                        "decision_options": None,
                        "voting_ratio": 0.5,
                        "default_decision": None,
                        "fallback_policy": None,
                        "communication_channel": None,
                        "added_conditions": None,
                        "condition_type": None,
                        "veto_participants": None,
                        "excluded_participants": None,
                        "min_participants": None,
                        "deadline_offset_value": None,
                        "deadline_offset_unit": None,
                        "deadline_date": None,
                        "min_decision_offset_value": None,
                        "min_decision_offset_unit": None,
                        "min_decision_date": None,
                        "label_condition_type": None,
                        "label_condition_operator": None,
                        "label_condition_labels": None,
                    }
                ],
                "composed_policies": [],
            },
            "Two-Thirds Supermajority": {
                "description": (
                    "**Two-Thirds Supermajority** — For high-stakes decisions.\n\n"
                    "Requires **at least 2/3** of participating voters to approve.\n\n"
                    "Best for: Constitutional changes, major architecture decisions, removing maintainers."
                ),
                "projects": [{"name": "MyProject", "platform": None, "repo": None}],
                "activities": [],
                "tasks": [],
                "profiles": [],
                "roles": [{"name": "Voter", "vote_value": None}],
                "individuals": [],
                "agents": [],
                "policies": [
                    {
                        "name": "supermajority_policy",
                        "type": "MajorityPolicy",
                        "scope": "MyProject",
                        "participants": ["Voter"],
                        "decision_type": "BooleanDecision",
                        "decision_options": None,
                        "voting_ratio": 0.67,
                        "default_decision": None,
                        "fallback_policy": None,
                        "communication_channel": None,
                        "added_conditions": None,
                        "condition_type": None,
                        "veto_participants": None,
                        "excluded_participants": None,
                        "min_participants": None,
                        "deadline_offset_value": None,
                        "deadline_offset_unit": None,
                        "deadline_date": None,
                        "min_decision_offset_value": None,
                        "min_decision_offset_unit": None,
                        "min_decision_date": None,
                        "label_condition_type": None,
                        "label_condition_operator": None,
                        "label_condition_labels": None,
                    }
                ],
                "composed_policies": [],
            },
            "Consensus (Unanimous Agreement)": {
                "description": (
                    "**Consensus** — Everyone must agree.\n\n"
                    "All participants must explicitly approve for a decision to pass. "
                    "If any member objects, the decision is blocked.\n\n"
                    "Best for: Small teams, critical security decisions, foundational governance changes."
                ),
                "projects": [{"name": "MyProject", "platform": None, "repo": None}],
                "activities": [],
                "tasks": [],
                "profiles": [],
                "roles": [{"name": "Member", "vote_value": None}],
                "individuals": [],
                "agents": [],
                "policies": [
                    {
                        "name": "consensus_policy",
                        "type": "ConsensusPolicy",
                        "scope": "MyProject",
                        "participants": ["Member"],
                        "decision_type": "BooleanDecision",
                        "decision_options": None,
                        "voting_ratio": None,
                        "default_decision": None,
                        "fallback_policy": None,
                        "communication_channel": None,
                        "added_conditions": None,
                        "condition_type": None,
                        "veto_participants": None,
                        "excluded_participants": None,
                        "min_participants": None,
                        "deadline_offset_value": None,
                        "deadline_offset_unit": None,
                        "deadline_date": None,
                        "min_decision_offset_value": None,
                        "min_decision_offset_unit": None,
                        "min_decision_date": None,
                        "label_condition_type": None,
                        "label_condition_operator": None,
                        "label_condition_labels": None,
                    }
                ],
                "composed_policies": [],
            },
            "Lazy Consensus (Silence = Approval)": {
                "description": (
                    "**Lazy Consensus** — Silence means approval.\n\n"
                    "A proposal is assumed approved unless someone explicitly objects within the decision window. "
                    "If objections arise, the process falls back to a majority vote.\n\n"
                    "Best for: Low-risk changes, documentation updates, dependency bumps."
                ),
                "projects": [{"name": "MyProject", "platform": None, "repo": None}],
                "activities": [],
                "tasks": [],
                "profiles": [],
                "roles": [{"name": "Member", "vote_value": None}],
                "individuals": [],
                "agents": [],
                "policies": [
                    {
                        "name": "fallback_vote",
                        "type": "MajorityPolicy",
                        "scope": "MyProject",
                        "participants": ["Member"],
                        "decision_type": "BooleanDecision",
                        "decision_options": None,
                        "voting_ratio": 0.5,
                        "default_decision": None,
                        "fallback_policy": None,
                        "communication_channel": None,
                        "added_conditions": None,
                        "condition_type": None,
                        "veto_participants": None,
                        "excluded_participants": None,
                        "min_participants": None,
                        "deadline_offset_value": None,
                        "deadline_offset_unit": None,
                        "deadline_date": None,
                        "min_decision_offset_value": None,
                        "min_decision_offset_unit": None,
                        "min_decision_date": None,
                        "label_condition_type": None,
                        "label_condition_operator": None,
                        "label_condition_labels": None,
                    },
                    {
                        "name": "lazy_consensus_policy",
                        "type": "LazyConsensusPolicy",
                        "scope": "MyProject",
                        "participants": ["Member"],
                        "decision_type": "BooleanDecision",
                        "decision_options": None,
                        "voting_ratio": None,
                        "default_decision": None,
                        "fallback_policy": "fallback_vote",
                        "communication_channel": None,
                        "added_conditions": None,
                        "condition_type": None,
                        "veto_participants": None,
                        "excluded_participants": None,
                        "min_participants": None,
                        "deadline_offset_value": None,
                        "deadline_offset_unit": None,
                        "deadline_date": None,
                        "min_decision_offset_value": None,
                        "min_decision_offset_unit": None,
                        "min_decision_date": None,
                        "label_condition_type": None,
                        "label_condition_operator": None,
                        "label_condition_labels": None,
                    },
                ],
                "composed_policies": [],
            },
            "Leader-Driven (with Default Vote Fallback)": {
                "description": (
                    "**Leader-Driven** — One person decides, with a safety net.\n\n"
                    "A designated leader (e.g., Tech Lead, BDFL) makes the call. "
                    "If the leader is unavailable, the decision falls back to a majority vote among members.\n\n"
                    "Best for: Fast-moving teams, time-sensitive decisions, benevolent dictator models."
                ),
                "projects": [{"name": "MyProject", "platform": None, "repo": None}],
                "activities": [],
                "tasks": [],
                "profiles": [],
                "roles": [
                    {"name": "Leader", "vote_value": None},
                    {"name": "Member", "vote_value": None},
                ],
                "individuals": [],
                "agents": [],
                "policies": [
                    {
                        "name": "default_vote",
                        "type": "MajorityPolicy",
                        "scope": "MyProject",
                        "participants": ["Member"],
                        "decision_type": "BooleanDecision",
                        "decision_options": None,
                        "voting_ratio": 0.5,
                        "default_decision": None,
                        "fallback_policy": None,
                        "communication_channel": None,
                        "added_conditions": None,
                        "condition_type": None,
                        "veto_participants": None,
                        "excluded_participants": None,
                        "min_participants": None,
                        "deadline_offset_value": None,
                        "deadline_offset_unit": None,
                        "deadline_date": None,
                        "min_decision_offset_value": None,
                        "min_decision_offset_unit": None,
                        "min_decision_date": None,
                        "label_condition_type": None,
                        "label_condition_operator": None,
                        "label_condition_labels": None,
                    },
                    {
                        "name": "leader_policy",
                        "type": "LeaderDrivenPolicy",
                        "scope": "MyProject",
                        "participants": ["Leader"],
                        "decision_type": "BooleanDecision",
                        "decision_options": None,
                        "voting_ratio": None,
                        "default_decision": "default_vote",
                        "fallback_policy": None,
                        "communication_channel": None,
                        "added_conditions": None,
                        "condition_type": None,
                        "veto_participants": None,
                        "excluded_participants": None,
                        "min_participants": None,
                        "deadline_offset_value": None,
                        "deadline_offset_unit": None,
                        "deadline_date": None,
                        "min_decision_offset_value": None,
                        "min_decision_offset_unit": None,
                        "min_decision_date": None,
                        "label_condition_type": None,
                        "label_condition_operator": None,
                        "label_condition_labels": None,
                    },
                ],
                "composed_policies": [],
            },
            "Absolute Majority": {
                "description": (
                    "**Absolute Majority** — Counted against *all* eligible members.\n\n"
                    "Unlike a simple majority (counted among those who voted), an absolute majority counts "
                    "against **every eligible participant**, including those who did not vote. "
                    "Abstentions and no-shows count as 'no'.\n\n"
                    "Best for: Formal governance bodies, elections, constitutional amendments."
                ),
                "projects": [{"name": "MyProject", "platform": None, "repo": None}],
                "activities": [],
                "tasks": [],
                "profiles": [],
                "roles": [{"name": "Voter", "vote_value": None}],
                "individuals": [],
                "agents": [],
                "policies": [
                    {
                        "name": "absolute_majority_policy",
                        "type": "AbsoluteMajorityPolicy",
                        "scope": "MyProject",
                        "participants": ["Voter"],
                        "decision_type": "BooleanDecision",
                        "decision_options": None,
                        "voting_ratio": 0.5,
                        "default_decision": None,
                        "fallback_policy": None,
                        "communication_channel": None,
                        "added_conditions": None,
                        "condition_type": None,
                        "veto_participants": None,
                        "excluded_participants": None,
                        "min_participants": None,
                        "deadline_offset_value": None,
                        "deadline_offset_unit": None,
                        "deadline_date": None,
                        "min_decision_offset_value": None,
                        "min_decision_offset_unit": None,
                        "min_decision_date": None,
                        "label_condition_type": None,
                        "label_condition_operator": None,
                        "label_condition_labels": None,
                    }
                ],
                "composed_policies": [],
            },
        }
        
    def create_interface(self):
        """Create the main Gradio interface"""
        with gr.Blocks(
            title="Governance Policy Builder",
            theme=gr.themes.Soft(),
            css="""
            .main-container { display: flex !important; flex-direction: column !important; justify-content: flex-start !important; align-items: stretch !important; height: 100%; }
            .form-section { padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; margin: 10px 0; }
            .preview-panel { background-color: #f8f9fa; padding: 15px; border-radius: 8px; }
            .scope-hint { font-size: 0.92em; color: #555; background: #f0f4ff; border-left: 3px solid #4a7dff; padding: 8px 12px; margin: 6px 0 12px 0; border-radius: 0 4px 4px 0; }
            .template-card {
                background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 100%);
                border: 1px solid #c2d6ff;
                border-radius: 10px;
                padding: 16px 20px;
                margin: 10px 0;
            }
            /* Dark mode override — Gradio adds .dark to <body> */
            .dark .template-card {
                background: linear-gradient(135deg, #1e2a45 0%, #1a2035 100%);
                border: 1px solid #3a5080;
                color: #e8eaf6 !important;
            }
            .template-status-ok {
                color: #2e7d32;
                font-weight: 600;
            }
            """
        ) as ui:
            
            gr.Markdown("# 🏛️ Governance Policy Builder")
            gr.Markdown("Define governance rules for your software project using our form interface.\n\n"
                        "**How it works:**\n\n"
                        "1. **Define scopes**: Set up the structure of your project by adding projects, activities, and tasks where governance will apply.\n"
                        "2. **Add participants**: Specify the roles, individuals, and agents who can take part in governance decisions.\n"
                        "3. **Create policies**: Build governance policies by selecting from your defined scopes and participants.\n\n"
                        "**Follow the steps in order. As you complete each section, your options in the next will update automatically.** " 
                        "Each added element can be previewed in the Live Preview panel. "
                        "When finished, you can download your generated governance policy.")
            
            # State to store form data across tabs
            form_state = gr.State(self.form_data)
            
            with gr.Row():
                with gr.Column(scale=3, elem_classes=["main-container"]):
                    with gr.Tabs():
                        with gr.Tab("⚡ Quick Start", id="templates"):
                            template_components = self._create_template_tab()
                        with gr.Tab("🎯 Scopes", id="scopes"):
                            scope_components = self._create_scope_forms()
                            
                        with gr.Tab("👥 Participants", id="participants"):
                            participant_components = self._create_participant_forms()
                            
                        with gr.Tab("📋 Policies", id="policies"):
                            policy_components = self._create_policy_forms()
                            
                with gr.Column(scale=2):
                    preview_components = self._create_preview_panel()
            
            # Update handlers
            self._setup_event_handlers(template_components, scope_components, participant_components, policy_components, preview_components, form_state)
            
        return ui
    
    def _create_template_tab(self):
        """Create the Quick Start template tab"""
        gr.Markdown("## ⚡ Quick Start — Choose a Governance Template")
        gr.Markdown(
            "Select a pre-built governance template to get started quickly. "
            "The template will populate all form fields (Scopes, Participants, Policies) automatically.\n\n"
            "After applying a template you can **switch to the other tabs to customize** "
            "any detail — refine participants, add more policies, etc."
        )

        template_dropdown = gr.Dropdown(
            label="Choose a Template",
            choices=list(self.TEMPLATES.keys()),
            value=None,
            info="Pick a governance model to auto-fill the form"
        )

        template_description = gr.Markdown(
            value="*Select a template above to see its description.*",
            elem_classes=["template-card"]
        )

        # Let users customize the project platform before applying, potentially sharing repo URL
        repo_link_mode = gr.Radio(
            label="Link to a repository? (optional)",
            choices=["No", "Via URL", "Manual"],
            value="No",
            info="Connect the template project to a GitHub or GitLab repository"
        )

        # Via URL inputs (hidden by default) 
        repo_url_input = gr.Textbox(
            label="Repository URL",
            placeholder="https://github.com/owner/repo  or  https://gitlab.com/owner/repo",
            info="Paste the full URL of your repository",
            visible=False
        )

        # Manual inputs (hidden by default) 
        with gr.Row(visible=False) as manual_repo_row:
            repo_platform = gr.Dropdown(
                label="Platform",
                choices=["GitHub", "GitLab"],
                value="GitHub",
            )
            repo_owner = gr.Textbox(
                label="Repository Owner",
                placeholder="e.g., kubernetes",
                info="The user or organisation that owns the repository"
            )
            repo_name = gr.Textbox(
                label="Repository Name",
                placeholder="e.g., kubernetes",
                info="The repository name"
            )

        apply_template_btn = gr.Button(
            "🚀 Apply Template",
            variant="primary"
        )

        template_status = gr.Markdown(value="")

        return {
            'template_dropdown': template_dropdown,
            'template_description': template_description,
            'repo_link_mode': repo_link_mode,
            'repo_url_input': repo_url_input,
            'manual_repo_row': manual_repo_row,
            'repo_platform': repo_platform,
            'repo_owner': repo_owner,
            'repo_name': repo_name,
            'apply_template_btn': apply_template_btn,
            'template_status': template_status,
        }
    
    def _create_scope_forms(self):
        """Create forms for defining scopes (Projects, Activities, Tasks)"""
        gr.Markdown("## Define Scopes for your Governance Policies")
        gr.Markdown(
            "Scopes form a **hierarchy**: Project → Activity → Task. "
            "Governance policies can be assigned at any level, and **a policy on a higher scope applies to all its children** unless overridden.\n\n"
            "**How scope inheritance works:**\n\n"
            "```\n" 
            "Project (e.g., Kubernetes)\n"
            "  └── Activity (e.g., CodeReview)         → policy: 2 approvals required\n"
            "       └── Task (e.g., APIChangeReview)   → policy: 3 approvals from API team (overrides activity)\n"
            "       └── Task (e.g., DocFixReview)      → no policy → inherits activity's 2-approval rule\n"
            "```\n"
            "The most specific rule wins: a task-level policy **overrides** its parent activity's policy. If a task has no policy of its own, it inherits from its parent activity (or project).\n"
            "> **Tip:** You only need to create tasks when you need *different* governance at a more granular level. If all code reviews follow the same rules, a single Activity is enough."
        )
        
        # PROJECTS
        with gr.Accordion("Projects", open=False):
            gr.Markdown("### Define Projects")
            with gr.Accordion("ℹ️ What is a Project?", open=False):
                gr.Markdown("A **Project** is the highest-level scope — typically corresponding to a software project or repository. "
                         "All activities and tasks you create later can be nested under a project. "
                         "Only the project name is required; platform and repository details are optional and used to link policies to a specific repository.")
            
            with gr.Row():
                project_name = gr.Textbox(
                    label="Project Name *",
                    placeholder="e.g., kubernetes, GovernanceDSL, MyProject",
                    info="A unique identifier for this project (e.g., the name of your open-source  repository). Must be unique across all scopes."
                )
                
                project_repo_mode = gr.Radio(
                    label="Link to a repository?",
                    choices=["No", "Via URL", "Manual"],
                    value="No",
                    info="Connect this project to a GitHub or GitLab repository"
                )
            # Via URL
            with gr.Row():
                project_repo_url = gr.Textbox(
                    label="Repository URL",
                    placeholder="e.g., https://github.com/BESSER-PEARL/governanceDSL",
                    info="The full URL of the repository (e.g., https://github.com/BESSER-PEARL/governanceDSL)",
                    visible=False
                )
            # Manual
            with gr.Row(visible=False) as project_manual_repo_row:
                project_platform = gr.Dropdown(
                    label="Platform",
                    choices=["GitHub", "GitLab"],
                    value="GitHub",
                )
                project_repo_owner = gr.Textbox(
                    label="Repository Owner *",
                    placeholder="e.g., BESSER-PEARL",
                    info="The GitHub/GitLab username or organization that owns the repository"
                )
                project_repo_name = gr.Textbox(
                    label="Repository Name *",
                    placeholder="e.g., governanceDSL",
                    info="The repository name"
                )
            
            with gr.Row():
                add_project_btn = gr.Button("➕ Add Project", variant="secondary")
                clear_projects_btn = gr.Button("🗑️ Clear All", variant="secondary")
            
            # Display added projects
            projects_display = gr.Textbox(
                label="Added Projects",
                lines=4,
                interactive=False,
                placeholder="No projects added yet. Add a project to define the top-level scope for your governance policies."
            )
            
            # Hidden component to store projects data
            projects_data = gr.State([])
        
        # ACTIVITIES: uses ℹ️ accordion for contextual help 
        with gr.Accordion("Activities", open=False):
            gr.Markdown("### Define Activities")
            
            with gr.Accordion("ℹ️ What is an Activity?", open=False):
                gr.Markdown("""
An **Activity** represents a *category of collaborative work* — a recurring type of process 
that happens within a project.

Think of it as a **class of work, not a single instance**. For example:
- ✅ `CodeReview` → means *all code reviews in general*
- ❌ `Merge of a Pull Request` → that's a specific instance, not an activity (can be defined as a Task instead)

You can assign a governance policy to an activity so that **every instance** of that work 
follows the same rules. A policy on an activity applies to all its child tasks unless overridden.

**Common examples:** `CodeReview`, `ReleaseManagement`, `Documentation`, `IssueTriaging`
""")
            
            with gr.Row():
                activity_name = gr.Textbox(
                    label="Activity Name *",
                    placeholder="e.g., CodeReview, ReleaseManagement, Documentation",
                    info="A unique name for this category of work (e.g., 'CodeReview' covers all code reviews)"
                )
                
                activity_parent = gr.Dropdown(
                    label="Parent Project (Optional)",
                    choices=[],  # Will be populated dynamically from added projects
                    value=None,
                    allow_custom_value=False,
                    info="Assign this activity to a project — policies on the project will also apply here unless overridden"
                )
            
            with gr.Row():
                add_activity_btn = gr.Button("➕ Add Activity", variant="secondary")
                clear_activities_btn = gr.Button("🗑️ Clear All", variant="secondary")
            
            # Display added activities
            activities_display = gr.Textbox(
                label="Added Activities",
                lines=4,
                interactive=False,
                placeholder="No activities added yet. Add activities to represent categories of work (e.g., CodeReview, ReleaseManagement).",
                info="Activities are the middle level of the scope hierarchy — they group related tasks"
            )
            
            # Hidden component to store activities data
            activities_data = gr.State([])
            
        # TASKS: uses Markdown with tables inside accordions 
        with gr.Accordion("Tasks", open=False):
            gr.Markdown("### Define Tasks")
            
            with gr.Accordion("ℹ️ What is a Task?", open=False):
                gr.Markdown("A **Task** is the most granular scope — a *specific, concrete type of action* within an activity (e.g., merging a pull request or onboarding a member). "
                         "Define a task when you need a governance rule for a particular type of action. "
                         "If not, the activity's policy will apply by default.")
            
            with gr.Row():
                task_name = gr.Textbox(
                    label="Task Name *",
                    placeholder="e.g., PRMerge, HotfixApproval, APIChangeReview",
                    info="A unique name for this specific action type (the most granular governance target)"
                )
                
                task_parent = gr.Dropdown(
                    label="Parent Activity (Optional)",
                    choices=[],  # Will be populated dynamically from activities only
                    value=None,
                    allow_custom_value=False,
                    info="Assign this task to an activity — it inherits the activity's policy unless it has its own"
                )
            
            with gr.Row():
                task_type = gr.Dropdown(
                    label="Type (Optional)",
                    choices=["", "Pull request", "MemberLifecycle"],
                    value="",
                    info="The platform-level object type this task corresponds to (e.g., Pull Request or member lifecycle event)"
                )
                
                task_action = gr.Dropdown(
                    label="Action (Optional)",
                    choices=[""],
                    value="",
                    info="The specific platform action (e.g., 'merge', 'onboard') — only shown when a Type is selected",
                    visible=False
                )
            
            with gr.Row():
                add_task_btn = gr.Button("➕ Add Task", variant="secondary")
                clear_tasks_btn = gr.Button("🗑️ Clear All", variant="secondary")
            
            # Display added tasks
            tasks_display = gr.Textbox(
                label="Added Tasks",
                lines=4,
                interactive=False,
                placeholder="No tasks added yet. Add tasks for specific actions that need their own governance rules (e.g., PRMerge, HotfixApproval).",
                info="Tasks are the most granular scope level — a task-level policy overrides its parent activity's policy"
            )
            
            # Hidden component to store tasks data
            tasks_data = gr.State([])
        
        return {
            'project_name': project_name,
            'project_repo_mode': project_repo_mode,
            'project_repo_url': project_repo_url,
            'project_manual_repo_row': project_manual_repo_row,
            'project_platform': project_platform,
            'project_repo_owner': project_repo_owner,
            'project_repo_name': project_repo_name,
            'add_project_btn': add_project_btn,
            'clear_projects_btn': clear_projects_btn,
            'projects_display': projects_display,
            'projects_data': projects_data,
            'activity_name': activity_name,
            'activity_parent': activity_parent,
            'add_activity_btn': add_activity_btn,
            'clear_activities_btn': clear_activities_btn,
            'activities_display': activities_display,
            'activities_data': activities_data,
            'task_name': task_name,
            'task_parent': task_parent,
            'task_type': task_type,
            'task_action': task_action,
            'add_task_btn': add_task_btn,
            'clear_tasks_btn': clear_tasks_btn,
            'tasks_display': tasks_display,
            'tasks_data': tasks_data
        }
    
    def _create_participant_forms(self):
        """Create forms for defining participants (Roles, Individuals, Agents)"""
        gr.Markdown("## Define Participants")
        gr.Markdown(
            "Define the people, roles, and automated systems that drive your project's governance. These entities are the \"Who\" behind every policy. "
            "Define the people, roles, and automated systems involved in your project's governance.\n\n"
            "In this section, you will set up the participants who will later be assigned to specific governance policies. "
            "Participants (Roles, Individuals, or Agents) can have a custom **Vote Value** (1.0 by default) representing their influence in decisions. \n\n"
            "> **Note:** Names must be unique across all participants (roles, individuals and agents)"
        )
        
        with gr.Accordion("Roles", open=False):
            gr.Markdown("### Define Roles")
            with gr.Accordion("ℹ️ What is a Role?", open=False):
                gr.Markdown(
                    """
                    A **Role** represents a formal position or structural group within your project (e.g., `Maintainer`, `Reviewer`).

                    Instead of naming every person in a policy, you point the policy to a **Role**. This makes your governance "future-proof":
                    ```text
                    [Policy: PR Merge] ──▶ Requires: [Role: Maintainer]
                                                  │
                            ┌───────────────────────┴──────────────────────┐
                    [Individual: Alice]      [Individual: Bob]      [Individual: Charlie]
                    ```
                    **Vote value** defines the weight of this role's vote in decision-making. If an individual has already a vote value defined, that will override the role's vote value for that individual.

                    """
                )
            
            with gr.Row():
                role_name = gr.Textbox(
                    label="Role Name *",
                    placeholder="e.g., maintainer, reviewer, approver, owner"
                    # info="Unique name for this role (required - must be unique across all participants)"
                )
                
                role_vote_value = gr.Number(
                    label="Vote Value (Optional)",
                    value=1.0,
                    step=0.1,
                    info="Weight of this role's vote (must be >= 0.0, default: 1.0)"
                )
            
            with gr.Row():
                add_role_btn = gr.Button("➕ Add Role", variant="secondary")
                clear_roles_btn = gr.Button("🗑️ Clear All", variant="secondary")
            
            # Display added roles
            roles_display = gr.Textbox(
                label="Added Roles",
                lines=4,
                interactive=False,
                placeholder="No roles added yet. Create roles to define project responsibilities.",
                info="Roles you've added will appear here"
            )
            
            # Hidden component to store roles data
            roles_data = gr.State([])
        
        with gr.Accordion("Individuals", open=False):
            gr.Markdown("### Individual Participants")
            with gr.Accordion("ℹ️ What is an Individual?", open=False):
                gr.Markdown(
                    """
                    An **Individual** represents a specific human participant in your project:
                    *   **Position:** Can be assigned a **Role**.
                    *   **Diversity:** Can be linked to a **Profile**.
                    *   **Custom Power:** You can override an individual's **Vote Value** to give them more/less influence than their role suggests.
                    """
                )
            
            with gr.Row():
                individual_name = gr.Textbox(
                    label="Individual Name",
                    placeholder="e.g., john_doe, jane_smith"
                    # info="Unique name for this individual"
                )
                individual_vote_value = gr.Number(
                    label="Vote Value (Optional)",
                    value=1.0,
                    step=0.1,
                    info="Weight of this individual's vote (must be >= 0.0, default: 1.0)"
                )

            with gr.Row():
                individual_profile = gr.Dropdown(
                    label="Profile (Optional)",
                    choices=[],  # Will be populated dynamically from added profiles
                    value=None,
                    allow_custom_value=False,
                    info="Diversity profile for this individual.\n\n ⚠️ Be sure to create profiles first in the Profiles section below if you want to assign them here!"
                )
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
            
        with gr.Accordion("Agents", open=False):
            gr.Markdown("### Automated Participants")
            with gr.Accordion("ℹ️ What is an Agent?", open=False):
                gr.Markdown(
                    """
                    An **Agent** is an automated system or bot that participates in decisions. 
                    Agents can be assigned a role and have additional attributes to specify their influence and trustworthiness in the decision-making process.
                    Agents are evaluated based on three "Trust Metrics" that the engine uses to calculate their final weight:

                    1. **Confidence:** How much do we trust the agent's logic/output?
                    2. **Autonomy:** Does the agent act independently or require human supervision?
                    3. **Explainability:** Can the agent provide clear reasons for its "vote" or action?

                    ```text
                    [Metric Scores] ──Σ──▶ [Calculated Influence] ──▶ [Governance Decision]
                    ```
                    """
                )
            
            with gr.Row():
                agent_name = gr.Textbox(
                    label="Agent Name",
                    placeholder="e.g., k8s-ci-robot, dependabot"
                    # info="Unique name for this automated agent (no spaces allowed)"
                )
                
                agent_vote_value = gr.Number(
                    label="Vote Value (Optional)",
                    value=1.0,
                    step=0.1,
                    info="Weight of this agent's vote (must be >= 0.0, default: 1.0)"
                )
                
            with gr.Row():
                agent_confidence = gr.Number(
                    label="Confidence (Optional)",
                    value=None,
                    step=0.1,
                    placeholder="Enter value (0.0-1.0)",
                    info="How much trust is placed in this agent's outputs (0.0 = no trust, 1.0 = full trust)"
                )
                
                agent_autonomy_level = gr.Number(
                    label="Autonomy Level (Optional)",
                    value=None,
                    step=0.1,
                    placeholder="Enter value (0.0-1.0)",
                    info="Degree of independent action the agent can take without human approval (0.0 = fully supervised, 1.0 = fully autonomous)"
                )
                
            with gr.Row():
                agent_explainability = gr.Number(
                    label="Explainability (Optional)",
                    value=None,
                    step=0.1,
                    placeholder="Enter value (0.0-1.0)",
                    info="Ability of the agent to provide understandable justifications for its decisions (0.0 = opaque, 1.0 = fully explainable)"
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
        
        with gr.Accordion("Profiles", open=False):
            gr.Markdown("### Define Profiles")
            with gr.Accordion("ℹ️ What is a Profile?", open=False):
                gr.Markdown("A **Profile** is a set of diversity attributes (such as gender, race, or language) used to track and promote inclusivity. "
                "Once defined, profiles can be assigned to **Individuals** to reflect the diverse composition of your project's decision-makers."
            )
            
            with gr.Row():
                profile_name = gr.Textbox(
                    label="Profile Name",
                    placeholder="e.g., female_profile",
                    info="Unique name for this profile"
                )
                
            with gr.Row():
                profile_gender = gr.Dropdown(
                    label="Gender (Optional)",
                    choices=["", "male", "female", "non-binary", "other"],
                    value="",
                    allow_custom_value=False,
                    info="Leave empty if not applicable"
                )
                
                profile_race = gr.Dropdown(
                    label="Race/Ethnicity (Optional)", 
                    choices=["", "asian", "black", "hispanic", "white", "mixed", "other"],
                    value="",
                    allow_custom_value=False,
                    info="Leave empty if not applicable"
                )
                
                profile_language = gr.Dropdown(
                    label="Language (Optional)",
                    choices=["", "english", "spanish", "french", "german", "chinese", "japanese", "other"],
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
                placeholder="No profiles added yet. Remember: profiles must have at least one attribute (gender, race, or language).",
                info="Profiles you've added will appear here"
            )
            
            # Hidden component to store profiles data
            profiles_data = gr.State([])

        return {
            'profile_name': profile_name,
            'profile_gender': profile_gender,
            'profile_race': profile_race,
            'profile_language': profile_language,
            'add_profile_btn': add_profile_btn,
            'clear_profiles_btn': clear_profiles_btn,
            'profiles_display': profiles_display,
            'profiles_data': profiles_data,
            'role_name': role_name,
            'role_vote_value': role_vote_value,
            'add_role_btn': add_role_btn,
            'clear_roles_btn': clear_roles_btn,
            'roles_display': roles_display,
            'roles_data': roles_data,
            'individual_name': individual_name,
            'individual_vote_value': individual_vote_value,
            'individual_profile': individual_profile,
            'individual_role': individual_role,
            'add_individual_btn': add_individual_btn,
            'clear_individuals_btn': clear_individuals_btn,
            'individuals_display': individuals_display,
            'individuals_data': individuals_data,
            'agent_name': agent_name,
            'agent_vote_value': agent_vote_value,
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
        gr.Markdown(
            "Configure how decisions are made by linking your **Scopes** (where) with **Participants** (who).\n\n"
            "We can define two main categories of policies:\n"
            "* **Simple Policies**: Single-step rules like \"Majority Vote\" or \"Technical Lead Approval\".\n"
            "* **Composed Policies**: Multi-phase workflows (e.g., a Community Vote followed by a Board Approval). "
        )
        
        with gr.Accordion("Simple Policy", open=False):
            gr.Markdown("### Create a Single-step Policy")
            with gr.Accordion("ℹ️ What is a Policy?", open=False):
                gr.Markdown(
                    """
                    A **Policy** defines the rules for how decisions are made within a specific scope.

                    Available Types:
                    *   **Voting:** evaluated either by the number of votes actually cast (`MajorityPolicy`) or by the total number of eligible members (`AbsoluteMajorityPolicy`). Can be customized with different ratios (e.g., 2/3 majority).
                    *   **Consensus:** Requires agreement from all; **Lazy Consensus** assumes agreement unless someone objects. Both can include fallback policies for when consensus cannot be reached.
                    *   **Leader-Driven:** Decisions made by a specific lead (with optional default policy if lead is not available).

                    > **Note:** Fallback policies must be created **before** the main policy and share the same scope.
                    """
                )
            
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
                        "VotingPolicy"
                    ],
                    value="MajorityPolicy",
                    info="Type of decision-making process"
                )
            
            with gr.Row():
                policy_scope = gr.Dropdown(
                    label="Policy Scope *",
                    choices=[],  # Will be populated dynamically from defined scopes
                    value=None,
                    allow_custom_value=False,
                    info="Select the scope this policy applies to (required)"
                )
                
                # Participants for this policy
                policy_participants = gr.Dropdown(
                    label="Policy Participants *",
                    choices=[],  # Will be populated dynamically from defined participants
                    value=None,
                    allow_custom_value=False,
                    multiselect=True,
                    info="Select participants from defined roles/individuals (required)"
                )
            
            # Optional communication channel for this policy
            with gr.Row():
                communication_channel = gr.Textbox(
                    label="Communication Channel (Optional)",
                    placeholder="e.g., slack, email, github",
                    info="Medium used for decision discussion/notification"
                )
            
            with gr.Row():
                # Decision type
                decision_type = gr.Dropdown(
                    label="Decision Type",
                    choices=["BooleanDecision", "StringList", "ElementList"],
                    value="BooleanDecision"
                )
                
                # Options for StringList
                decision_options = gr.Textbox(
                    label="Decision Options",
                    placeholder="e.g., option1, option2, option3 (for StringList)",
                    visible=False,
                    info="Comma-separated custom options for StringList decisions"
                )
                
                # Options for ElementList (Individual names)
                decision_options_element_list = gr.Dropdown(
                    label="Decision Options",
                    choices=[],
                    value=None,
                    allow_custom_value=False,
                    multiselect=True,
                    visible=False,
                    interactive=True,
                    info="Select individual(s) for ElementList decisions"
                )
                
                
                # Parameters (for voting policies)
                voting_ratio = gr.Slider(
                    label="Voting Ratio",
                    value=0.5,
                    step=0.1,
                    maximum=1.0,
                    visible=True,  # Start visible since MajorityPolicy is default
                    info="Required ratio of positive votes (1.0 = unanimous). Default is 0.5."
                )
            
            with gr.Row():
                # Default policy for LeaderDrivenPolicy
                default_decision = gr.Dropdown(
                    label="Default Policy",
                    choices=[],  # Will be populated with other defined policies
                    value=None,
                    allow_custom_value=False,
                    visible=False,
                    info="Default policy when leader doesn't participate (Showing only policies with same scope)"
                )
                
                # Fallback policy for ConsensusPolicy and LazyConsensusPolicy
                fallback_policy = gr.Dropdown(
                    label="Fallback Policy",
                    choices=[],  # Will be populated with other defined policies
                    value=None,
                    allow_custom_value=False,
                    visible=False,
                    info="Policy to use when consensus cannot be reached (Showing only policies with same scope)"
                )
            
            # Conditions section wrapped in a visual box
            with gr.Group():
                gr.Markdown("#### Policy Conditions (Optional)")
                with gr.Accordion("ℹ️ What are Conditions?", open=False):
                    gr.Markdown(
                        """
                        **Conditions** are additional constraints that must be met before, during or after a policy to be resolved.

                        Condition Categories:
                        *   **⏰ Time Management:**
                            *   `Deadline`: Maximum time allowed.
                            *   `MinDecisionTime`: Minimum discussion period before a decision.
                        *   **👥 Participation:**
                            *   `MinParticipants`: Ensures a quorum is reached.
                            *   **Veto Right**: Grants specific individuals the power to block a proposal.
                            *   **Participant Exclusion**: Prevents specific members from voting (e.g., conflict of interest).
                        *   **⚙️ Technical:**
                            *   `CheckCiCd`: Requires automated tests to pass.
                            *   `LabelCondition`: Checks for specific GitHub/GitLab labels.
                            *   `MinTime`: Checks for member activity/inactivity history.
                            *   ⏱️ Evaluation Timing. Technical conditions can be checked at different stages:
                                1.  **Pre:** Before the decision starts.
                                2.  **Concurrent:** While the decision is being made.
                                3.  **Post:** After the logic finishes but before the result is finalized.
                        """
                    )
                
                # Add visual containment with padding
                # We add left and right spacers to make it visual that it's contained
                with gr.Row():
                    gr.HTML("")
                    with gr.Column(scale=100): 
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
                                    "CheckCiCd",
                                    "MinTime",
                                    "LabelCondition"
                                ],
                                value="",
                                info="Select a condition type to add to this policy"
                            )
                        
                        # Condition-specific fields (initially hidden)
                        with gr.Row():
                            veto_participants = gr.Dropdown(
                                label="Veto Right Participants",
                                choices=[],  # Will be populated from participants
                                value=None,
                                multiselect=True,
                                allow_custom_value=False,
                                visible=False,
                                info="Participants who can veto this decision (does not allow default values yet, such as Author, RepoOwner, etc.)"
                            )
                        
                            # ParticipantExclusion condition
                            excluded_participants = gr.Dropdown(
                                label="Excluded Participants",
                                choices=[],  # Will be populated from participants
                                value=None,
                                multiselect=True,
                                allow_custom_value=False,
                                visible=False,
                                info="Participants excluded from this decision (does not allow default values yet, such as Author, RepoOwner, etc.)"
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
                            
                            deadline_date = gr.Textbox(
                                label="Deadline Date (DD/MM/YYYY)",
                                placeholder="e.g., 25/12/2024",
                                visible=False,
                                info="Specific deadline date (optional, can be used with or without offset)"
                            )
                        
                        # MinDecisionTime condition fields  
                        with gr.Row():
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
                            
                            min_decision_date = gr.Textbox(
                                label="Min Decision Date (DD/MM/YYYY)",
                                placeholder="e.g., 01/01/2024",
                                visible=False,
                                info="Specific minimum decision date (optional, can be used with or without offset)"
                            )
                        
                        # CheckCiCd condition fields
                        with gr.Row():
                            with gr.Row():
                                check_ci_cd_evaluation_mode = gr.Dropdown(
                                    label="Evaluation Mode",
                                    choices=["", "pre", "post", "concurrent"],
                                    value="",
                                    visible=False,
                                    info="When to evaluate CI/CD checks (pre/post/concurrent)"
                                )
                                
                                check_ci_cd_value = gr.Checkbox(
                                    label="Check",
                                    value=True,
                                    visible=False,
                                    info="Whether CI/CD checks must pass (true/false)"
                                )
                        
                        with gr.Row():
                            with gr.Row():
                                # LabelCondition fields
                                label_condition_type = gr.Dropdown(
                                    label="Evaluation Mode",
                                    choices=["", "pre", "post", "concurrent"],
                                    value="",
                                    visible=False,
                                    info="When to check labels (pre/post/concurrent)"
                                )
                                
                                label_condition_operator = gr.Dropdown(
                                    label="Label Operator",
                                    choices=["", "not"],
                                    value="",
                                    visible=False,
                                    info="Label condition operator (empty for required, 'not' for forbidden)"
                                )
                            
                            label_condition_labels = gr.Textbox(
                                label="Labels",
                                placeholder="e.g., lgtm, approved",
                                visible=False,
                                info="Comma-separated list of labels"
                            )
                        
                        # MinTime condition fields
                        with gr.Row():
                            with gr.Row():
                                min_time_evaluation_mode = gr.Dropdown(
                                    label="Evaluation Mode",
                                    choices=["", "pre", "post", "concurrent"],
                                    value="",
                                    visible=False,
                                    info="When to evaluate MinTime (pre/post/concurrent, optional)"
                                )
                                
                                min_time_activity = gr.Dropdown(
                                    label="Activity Type",
                                    choices=["Activity", "InActivity"],
                                    value="Activity",
                                    visible=False,
                                    info="Check for activity or inactivity"
                                )
                            
                            with gr.Row():
                                min_time_offset_value = gr.Number(
                                    label="MinTime Offset Value",
                                    value=None,
                                    visible=False,
                                    info="Time offset number (≥1, e.g., 7 for '7 days')"
                                )
                                
                                min_time_offset_unit = gr.Dropdown(
                                    label="MinTime Offset Unit",
                                    choices=["days", "weeks", "months", "years"],
                                    value="days",
                                    visible=False,
                                    info="Time unit for the MinTime offset"
                                )
                        
                        # Condition management buttons
                        with gr.Row():
                            with gr.Row():
                                add_condition_btn = gr.Button("➕ Add Condition", variant="secondary")
                                clear_conditions_btn = gr.Button("🗑️ Clear All", variant="secondary")

                        # Added conditions display (adaptive height)
                        with gr.Row():
                            added_conditions_list = gr.Textbox(
                                label="Added Conditions",
                                value="",
                                interactive=False,
                                lines=2,
                                max_lines=10,
                                info="List of conditions added to this policy"
                            )
                        with gr.Row():
                            gr.HTML("") # Vertical spacer
                    gr.HTML("")  # End of visual containment
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
        

        
        with gr.Accordion(" Composed Policy (Multi-phase)", open=False):
            gr.Markdown("### Create Complex Multi-Phase Governance Policies")
            with gr.Accordion("ℹ️ What is a Composed Policy?", open=False):
                gr.Markdown(
                    """
                    A **Composed Policy** orchestrates multiple phases into one complex workflow. Each phase can have its own policy type, participants, conditions, and communication channels, but they will all be linked together under a single composed policy name and scope.

                    Execution patterns:
                    * **Sequential (Phase 1 → Phase 2)**
                        *Perfect for "Review then Approve" workflows.*
                        ```text
                        [Phase 1: RFC Discussion] ───(Success)───▶ [Phase 2: Formal Vote] ──▶ Result
                        ```
                    * **Parallel (Phase 1 & Phase 2 at once)**
                        *Great for requiring simultaneous approvals from different departments.*
                        ```text
                                  ┌──▶ [Phase A: Security Audit] ──┐
                        [Start] ──┤                                ├──▶ { All Pass? } ──▶ Result
                                  └──▶ [Phase B: Legal Review] ────┘
                        ```
                    
                    Further configuration options:
                    *   **Carry Over:** Whether results should be carried over between phases (e.g., votes cast on the first phase are available in the second phase). *(only applicable for sequential execution).*
                    *   **Require All:** Decide if every single phase must succeed for the final decision to pass.

                    Policy types and conditions are the same as those available for single policies, see the section above for reference.
                    """
                )
            
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
                    allow_custom_value=False,
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
                    allow_custom_value=False,
                    multiselect=True,
                    info="Select participants for this phase"
                )
                
                # Decision type for the phase
                phase_decision_type = gr.Dropdown(
                    label="Phase Decision Type",
                    choices=["BooleanDecision", "StringList", "ElementList"],
                    value="BooleanDecision"
                )
            
            # Optional communication channel for this phase
            with gr.Row():
                phase_communication_channel = gr.Textbox(
                    label="Phase Communication Channel (Optional)",
                    placeholder="e.g., slack, email, github",
                    info="Medium used for this phase's communication"
                )
            
            with gr.Row():
                # Options for StringList
                phase_decision_options = gr.Textbox(
                    label="Phase Decision Options",
                    placeholder="e.g., option1, option2, option3 (for StringList)",
                    visible=False,
                    info="Comma-separated custom options for StringList decisions"
                )
                
                # Options for ElementList (Individual names)
                phase_decision_options_element_list = gr.Dropdown(
                    label="Phase Decision Options",
                    choices=[],
                    value=None,
                    allow_custom_value=False,
                    multiselect=True,
                    visible=False,
                    interactive=True,
                    info="Select individual(s) for ElementList decisions"
                )
                
                # Parameters (for voting policies)
                phase_voting_ratio = gr.Slider(
                    label="Phase Voting Ratio",
                    value=0.5,
                    step=0.1,
                    maximum=1.0,
                    visible=True,  # Start visible since MajorityPolicy is default for phases too
                    info="Required ratio of positive votes (1.0 = unanimous). Default is 0.5."
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
            
            # Phase Conditions Section
            with gr.Group():
                gr.Markdown("#### 📜 Phase Conditions (Optional)")
                gr.Markdown("*Configure additional rules and constraints for this phase*")
                
                # Add visual containment with padding following same structure
                with gr.Row():
                    gr.HTML("")  # Left spacer
                    with gr.Column(scale=100):  # Main content area
                        with gr.Row():
                            phase_condition_type = gr.Dropdown(
                                label="Add Condition",
                                choices=[
                                    "",  # Empty option for no condition
                                    "Deadline",
                                    "MinDecisionTime", 
                                    "ParticipantExclusion",
                                    "MinParticipants",
                                    "VetoRight",
                                    "CheckCiCd",
                                    "MinTime",
                                    "LabelCondition"
                                ],
                                value="",
                                info="Select a condition type to add to this phase"
                            )
                        # VetoRight condition
                        with gr.Row():
                            phase_veto_participants = gr.Dropdown(
                                label="Veto Participants",
                                choices=[],  # Will be populated from participants
                                value=None,
                                multiselect=True,
                                allow_custom_value=False,
                                visible=False,
                                info="Participants with veto power for this phase"
                            )
                
                        # ParticipantExclusion condition
                        with gr.Row():
                            phase_excluded_participants = gr.Dropdown(
                                label="Excluded Participants",
                                choices=[],  # Will be populated from participants
                                value=None,
                                multiselect=True,
                                allow_custom_value=False,
                                visible=False,
                                info="Participants excluded from this phase decision"
                            )
                
                        # MinParticipants condition
                        with gr.Row():
                            phase_min_participants = gr.Number(
                                label="Minimum Participants",
                                value=None,
                                visible=False,
                                info="Minimum number of participants required for this phase (≥1)"
                            )
                
                        # Deadline condition fields
                        with gr.Row():
                            with gr.Row():
                                phase_deadline_offset_value = gr.Number(
                                    label="Deadline Offset Value",
                                    value=None,
                                    visible=False,
                                    info="Time offset number (≥1, e.g., 7 for '7 days')"
                                )
                                
                                phase_deadline_offset_unit = gr.Dropdown(
                                    label="Deadline Offset Unit",
                                    choices=["days", "weeks", "months", "years"],
                                    value="days",
                                    visible=False,
                                    info="Time unit for the offset"
                                )
                            
                            phase_deadline_date = gr.Textbox(
                                label="Deadline Date (DD/MM/YYYY)",
                                placeholder="e.g., 25/12/2024",
                                visible=False,
                                info="Specific deadline date (optional, can be used with or without offset)"
                            )
                
                        # MinDecisionTime condition fields  
                        with gr.Row():
                            with gr.Row():
                                phase_min_decision_offset_value = gr.Number(
                                    label="Min Decision Time Offset Value",
                                    value=None,
                                    visible=False,
                                    info="Minimum time offset number (≥1, e.g., 2 for '2 days')"
                                )
                                
                                phase_min_decision_offset_unit = gr.Dropdown(
                                    label="Min Decision Time Offset Unit",
                                    choices=["days", "weeks", "months", "years"],
                                    value="days",
                                    visible=False,
                                    info="Time unit for the minimum decision time"
                                )
                            
                            phase_min_decision_date = gr.Textbox(
                                label="Min Decision Date (DD/MM/YYYY)",
                                placeholder="e.g., 01/01/2024",
                                visible=False,
                                info="Specific minimum decision date (optional, can be used with or without offset)"
                            )
                
                        # CheckCiCd condition fields
                        with gr.Row():
                            with gr.Row():
                                phase_check_ci_cd_evaluation_mode = gr.Dropdown(
                                    label="Evaluation Mode",
                                    choices=["", "pre", "post", "concurrent"],
                                    value="",
                                    visible=False,
                                    info="When to evaluate CI/CD checks (pre/post/concurrent)"
                                )
                                
                                phase_check_ci_cd_value = gr.Checkbox(
                                    label="Check",
                                    value=True,
                                    visible=False,
                                    info="Whether CI/CD checks must pass (true/false)"
                                )
                
                        # LabelCondition fields
                        with gr.Row():
                            with gr.Row():
                                phase_label_condition_type = gr.Dropdown(
                                    label="Evaluation Mode",
                                    choices=["", "pre", "post", "concurrent"],
                                    value="",
                                    visible=False,
                                    info="When to check labels (pre/post/concurrent)"
                                )
                                
                                phase_label_condition_operator = gr.Dropdown(
                                    label="Label Operator",
                                    choices=["", "not"],
                                    value="",
                                    visible=False,
                                    info="Label condition operator (empty for required, 'not' for forbidden)"
                                )
                            
                            phase_label_condition_labels = gr.Textbox(
                                label="Labels",
                                placeholder="e.g., lgtm, approved",
                                visible=False,
                                info="Comma-separated list of labels"
                            )
                        
                        # Phase MinTime condition fields
                        with gr.Row():
                            with gr.Row():
                                phase_min_time_evaluation_mode = gr.Dropdown(
                                    label="Evaluation Mode",
                                    choices=["", "pre", "post", "concurrent"],
                                    value="",
                                    visible=False,
                                    info="When to evaluate MinTime (pre/post/concurrent, optional)"
                                )
                                
                                phase_min_time_activity = gr.Dropdown(
                                    label="Activity Type",
                                    choices=["Activity", "InActivity"],
                                    value="Activity",
                                    visible=False,
                                    info="Check for activity or inactivity"
                                )
                            
                            with gr.Row():
                                phase_min_time_offset_value = gr.Number(
                                    label="MinTime Offset Value",
                                    value=None,
                                    visible=False,
                                    info="Time offset number (≥1, e.g., 7 for '7 days')"
                                )
                                
                                phase_min_time_offset_unit = gr.Dropdown(
                                    label="MinTime Offset Unit",
                                    choices=["days", "weeks", "months", "years"],
                                    value="days",
                                    visible=False,
                                    info="Time unit for the MinTime offset"
                                )
                
                        # Phase condition management buttons
                        with gr.Row():
                            with gr.Row():
                                add_phase_condition_btn = gr.Button("➕ Add Condition", variant="secondary")
                                clear_phase_conditions_btn = gr.Button("🗑️ Clear All", variant="secondary")
                
                        # Added phase conditions display
                        with gr.Row():
                            added_phase_conditions_list = gr.Textbox(
                                label="Added Conditions",
                                value="",
                                interactive=False,
                                lines=2,
                                max_lines=10,
                                info="List of conditions added to this phase"
                            )
                        with gr.Row():
                            gr.HTML("") # Vertical spacer
                    gr.HTML("")
            
            # Phase management buttons
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
            'communication_channel': communication_channel,
            'decision_type': decision_type,
            'decision_options': decision_options,
            'decision_options_element_list': decision_options_element_list,
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
            'check_ci_cd_evaluation_mode': check_ci_cd_evaluation_mode,
            'check_ci_cd_value': check_ci_cd_value,
            'label_condition_type': label_condition_type,
            'label_condition_operator': label_condition_operator,
            'label_condition_labels': label_condition_labels,
            'min_time_evaluation_mode': min_time_evaluation_mode,
            'min_time_activity': min_time_activity,
            'min_time_offset_value': min_time_offset_value,
            'min_time_offset_unit': min_time_offset_unit,
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
            'phase_communication_channel': phase_communication_channel,
            'phase_decision_type': phase_decision_type,
            'phase_decision_options': phase_decision_options,
            'phase_decision_options_element_list': phase_decision_options_element_list,
            'phase_voting_ratio': phase_voting_ratio,
            'phase_default_decision': phase_default_decision,
            'phase_fallback_policy': phase_fallback_policy,
            # Phase condition components
            'phase_condition_type': phase_condition_type,
            'phase_veto_participants': phase_veto_participants,
            'phase_excluded_participants': phase_excluded_participants,
            'phase_min_participants': phase_min_participants,
            'phase_deadline_offset_value': phase_deadline_offset_value,
            'phase_deadline_offset_unit': phase_deadline_offset_unit,
            'phase_deadline_date': phase_deadline_date,
            'phase_min_decision_offset_value': phase_min_decision_offset_value,
            'phase_min_decision_offset_unit': phase_min_decision_offset_unit,
            'phase_min_decision_date': phase_min_decision_date,
            'phase_check_ci_cd_evaluation_mode': phase_check_ci_cd_evaluation_mode,
            'phase_check_ci_cd_value': phase_check_ci_cd_value,
            'phase_label_condition_type': phase_label_condition_type,
            'phase_label_condition_operator': phase_label_condition_operator,
            'phase_label_condition_labels': phase_label_condition_labels,
            'phase_min_time_evaluation_mode': phase_min_time_evaluation_mode,
            'phase_min_time_activity': phase_min_time_activity,
            'phase_min_time_offset_value': phase_min_time_offset_value,
            'phase_min_time_offset_unit': phase_min_time_offset_unit,
            'add_phase_condition_btn': add_phase_condition_btn,
            'clear_phase_conditions_btn': clear_phase_conditions_btn,
            'added_phase_conditions_list': added_phase_conditions_list,
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
            generate_btn = gr.Button("🔄 Refresh Preview", variant="secondary", visible=False)
            download_btn = gr.Button(
                value="✅ Prepare Policy for Download",
                variant="primary"
            )
            load_example_btn = gr.Button("📋 Load Example", variant="secondary", visible=False)
        
        # Download file component - will output the policy file for download
        download_file = gr.File(label="Download Policy", visible=True)
        
        return {
            'preview_code': self.preview_code,
            'generate_btn': generate_btn,
            'download_btn': download_btn,
            'load_example_btn': load_example_btn,
            'download_file': download_file
        }
    
    def _setup_event_handlers(self, template_components, scope_components, participant_components, policy_components, preview_components, _form_state):
        """Set up event handlers for form interactions"""
        
        # Helper function to validate date format (DD/MM/YYYY)
        def validate_date_format(date_string):
            """Validate date string is in DD/MM/YYYY format. Returns (is_valid, error_message)"""
            if not date_string or not date_string.strip():
                return True, ""  # Date is optional
            
            date_string = date_string.strip()
            # Check format DD/MM/YYYY
            pattern = r'^(\d{1,2})/(\d{1,2})/(\d{4})$'
            match = re.match(pattern, date_string)
            
            if not match:
                return False, "Date must be in DD/MM/YYYY format (e.g., 25/12/2024)"
            
            day, month, year = map(int, match.groups())
            
            # Validate day
            if day < 1 or day > 31:
                return False, "Day must be between 1 and 31"
            
            # Validate month
            if month < 1 or month > 12:
                return False, "Month must be between 1 and 12"
            
            # Validate year (reasonable range)
            if year < 1900 or year > 2100:
                return False, "Year must be between 1900 and 2100"
            
            return True, ""
        
        def update_repo_link_visibility(mode):
            """Show/hide repository input fields based on the selected mode."""
            show_url = (mode == "Via URL")
            show_manual = (mode == "Manual")
            return (
                gr.Textbox(visible=show_url), # repo_url_input
                gr.Row(visible=show_manual),  # manual_repo_row
            )
        
        def autofill_from_url(url: str):
            """Parse the URL and populate manual fields as a convenience."""
            if not url or not url.strip():
                return (
                    gr.Dropdown(value="GitHub"),
                    gr.Textbox(value=""),
                    gr.Textbox(value=""),
                    ""  # status
                )
            platform, owner, name = self._parse_repo_url(url.strip())
            if platform:
                status = f"✅ Detected: **{platform}** — `{owner}/{name}`"
            else:
                status = "⚠️ Could not parse URL. Check the format: `https://github.com/owner/repo`"
                platform, owner, name = "GitHub", "", ""

            return (
                gr.Dropdown(value=platform),
                gr.Textbox(value=owner),
                gr.Textbox(value=name),
                status
            )

        def apply_template(template_name,
                   repo_link_mode, repo_url_input,
                   repo_platform, repo_owner, repo_name,
                   current_projects, current_activities, current_tasks,
                   current_profiles, current_roles, current_individuals, current_agents,
                   current_policies, current_composed_policies):
            """Apply a selected template, replacing all current data."""
            if not template_name:
                return (
                    current_projects, current_activities, current_tasks, 
                    current_profiles, current_roles, current_individuals, current_agents,
                    current_policies, current_composed_policies,
                    self._format_projects_display(current_projects),
                    self._format_activities_display(current_activities),
                    self._format_tasks_display(current_tasks),
                    self._format_profiles_display(current_profiles),
                    self._format_roles_display(current_roles),
                    self._format_individuals_display(current_individuals),
                    self._format_agents_display(current_agents),
                    self._format_policies_display(current_policies),
                    self._format_composed_policies_display(current_composed_policies),
                    "❌ Please select a template first."
                )

            template = copy.deepcopy(self.TEMPLATES[template_name])
            
            # Resolve repository details 
            resolved_platform = None
            resolved_repo = None      # stored as "owner/repo" string

            if repo_link_mode == "Via URL":
                if not repo_url_input or not repo_url_input.strip():
                    # URL mode selected but field is empty
                    return (
                        current_projects, current_activities, current_tasks,
                        current_profiles, current_roles, current_individuals, current_agents,
                        current_policies, current_composed_policies,
                        self._format_projects_display(current_projects),
                        self._format_activities_display(current_activities),
                        self._format_tasks_display(current_tasks),
                        self._format_profiles_display(current_profiles),
                        self._format_roles_display(current_roles),
                        self._format_individuals_display(current_individuals),
                        self._format_agents_display(current_agents),
                        self._format_policies_display(current_policies),
                        self._format_composed_policies_display(current_composed_policies),
                        "❌ Please enter a repository URL, or switch the link mode to 'No'."
                    )
                parsed_platform, parsed_owner, parsed_repo_name = self._parse_repo_url(repo_url_input.strip())
                if not parsed_platform:
                    # URL was entered but couldn't be parsed
                    return (
                        current_projects, current_activities, current_tasks,
                        current_profiles, current_roles, current_individuals, current_agents,
                        current_policies, current_composed_policies,
                        self._format_projects_display(current_projects),
                        self._format_activities_display(current_activities),
                        self._format_tasks_display(current_tasks),
                        self._format_profiles_display(current_profiles),
                        self._format_roles_display(current_roles),
                        self._format_individuals_display(current_individuals),
                        self._format_agents_display(current_agents),
                        self._format_policies_display(current_policies),
                        self._format_composed_policies_display(current_composed_policies),
                        f"❌ Invalid repository URL: `{repo_url_input.strip()}`\n\n"
                        "Expected format: `https://platform.com/owner/repo`"
                    )
                resolved_platform = parsed_platform
                resolved_repo = f"{parsed_owner}/{parsed_repo_name}"
            elif repo_link_mode == "Manual":
                if not repo_owner or not repo_owner.strip() or not repo_name or not repo_name.strip():
                    return (
                        current_projects, current_activities, current_tasks,
                        current_profiles, current_roles, current_individuals, current_agents,
                        current_policies, current_composed_policies,
                        self._format_projects_display(current_projects),
                        self._format_activities_display(current_activities),
                        self._format_tasks_display(current_tasks),
                        self._format_profiles_display(current_profiles),
                        self._format_roles_display(current_roles),
                        self._format_individuals_display(current_individuals),
                        self._format_agents_display(current_agents),
                        self._format_policies_display(current_policies),
                        self._format_composed_policies_display(current_composed_policies),
                        f"❌ Please enter both owner and repo name for manual linking."
                    )
                resolved_platform = repo_platform if repo_platform else "GitHub"
                resolved_repo = f"{repo_owner.strip()}/{repo_name.strip()}"

            # Inject platform + repo into the first project of the template
            if resolved_platform and resolved_repo:
                project_name_in_template = template["projects"][0]["name"] if template["projects"] else "MyProject"
                for p in template["projects"]:
                    if p["name"] == project_name_in_template:
                        p["platform"] = resolved_platform
                        p["repo"] = resolved_repo

            # Build return values: data states + display texts + status message
            projects = template["projects"]
            activities = template["activities"]
            tasks = template["tasks"]
            profiles = template["profiles"]
            roles = template["roles"]
            individuals = template["individuals"]
            agents = template["agents"]
            policies = template["policies"]
            composed_policies = template["composed_policies"]

            repo_info = f" (linked to **{resolved_platform}**: `{resolved_repo}`)" if resolved_platform else ""
            status_msg = f"✅ Template **\"{template_name}\"** applied{repo_info}! Switch to the other tabs to further customize your governance setup."

            return (
                projects, activities, tasks,
                profiles, roles, individuals, agents,
                policies, composed_policies,
                # Display texts for each section
                self._format_projects_display(projects),
                self._format_activities_display(activities),
                self._format_tasks_display(tasks),
                self._format_profiles_display(profiles),
                self._format_roles_display(roles),
                self._format_individuals_display(individuals),
                self._format_agents_display(agents),
                self._format_policies_display(policies),
                self._format_composed_policies_display(composed_policies),
                # Status
                status_msg
            )
        
        def update_template_description(template_name):
            """Update the description panel when user selects a template."""
            if not template_name or template_name not in self.TEMPLATES:
                return "*Select a template above to see its description.*"
            return self.TEMPLATES[template_name]["description"]
        
        def add_profile(name, gender, race, language, current_profiles):
            """Add a new profile to the list"""
            if not name.strip():
                display_text = self._format_profiles_display(current_profiles)
                error_message = f"❌ Error: Please enter a profile name\n\n{display_text}" if current_profiles else "❌ Error: Please enter a profile name"
                return current_profiles, error_message, name, gender, race, language, None
            
            # Validate no spaces in name
            if ' ' in name.strip():
                display_text = self._format_profiles_display(current_profiles)
                error_message = f"❌ Error: Profile name cannot contain spaces (use underscores instead, e.g., 'my_profile')\n\n{display_text}" if current_profiles else "❌ Error: Profile name cannot contain spaces (use underscores instead, e.g., 'my_profile')"
                return current_profiles, error_message, name, gender, race, language, None
            
            # Check if profile already exists
            if any(p['name'] == name.strip() for p in current_profiles):
                display_text = self._format_profiles_display(current_profiles)
                error_message = f"❌ Error: Profile name already exists\n\n{display_text}" if current_profiles else "❌ Error: Profile name already exists"
                return current_profiles, error_message, name, gender, race, language, None
            
            # Validate that at least one attribute is provided
            if not gender and not race and not language:
                display_text = self._format_profiles_display(current_profiles)
                error_message = f"❌ Error: Profiles must have at least one attribute (gender, race, or language)\n\n{display_text}" if current_profiles else "❌ Error: Profiles must have at least one attribute (gender, race, or language)"
                return current_profiles, error_message, name, gender, race, language, None
            
            # Create new profile
            new_profile = {
                'name': name.strip(),
                'gender': gender if gender else None,
                'race': race if race else None,
                'language': language if language else None
            }
            
            updated_profiles = current_profiles + [new_profile]
            
            # Update display
            display_text = self._format_profiles_display(updated_profiles)
            success_message = f"✅ Profile '{new_profile['name']}' added successfully!\n\n{display_text}"
            
            return updated_profiles, success_message, "", "", "", "", None  # Clear individual profile selection
        
        def clear_profiles():
            """Clear all profiles"""
            return [], "No profiles added yet", None
        
        def add_role(name, vote_value, current_roles, current_individuals, current_agents):
            """Add a new role to the list"""
            if not name.strip():
                display_text = self._format_roles_display(current_roles)
                error_message = f"❌ Error: Please enter a role name\n\n{display_text}" if current_roles else "❌ Error: Please enter a role name"
                return current_roles, error_message, name, vote_value
            
            # Validate no spaces in name
            if ' ' in name.strip():
                display_text = self._format_roles_display(current_roles)
                error_message = f"❌ Error: Role name cannot contain spaces (use underscores instead, e.g., 'my_role')\n\n{display_text}" if current_roles else "❌ Error: Role name cannot contain spaces (use underscores instead, e.g., 'my_role')"
                return current_roles, error_message, name, vote_value
            
            # Validate vote_value is not negative if provided
            if vote_value is not None and vote_value < 0.0:
                display_text = self._format_roles_display(current_roles)
                error_message = f"❌ Error: Vote value cannot be negative\n\n{display_text}" if current_roles else "❌ Error: Vote value cannot be negative"
                return current_roles, error_message, name, vote_value
            
            # Check for global name uniqueness across all participant types
            role_name = name.strip()
            
            # Check against existing individuals
            if any(i['name'] == role_name for i in current_individuals):
                display_text = self._format_roles_display(current_roles)
                error_message = f"❌ Error: Name '{role_name}' already exists as an individual\n\n{display_text}" if current_roles else f"❌ Error: Name '{role_name}' already exists as an individual"
                return current_roles, error_message, name, vote_value
            
            # Check against existing agents
            if any(a['name'] == role_name for a in current_agents):
                display_text = self._format_roles_display(current_roles)
                error_message = f"❌ Error: Name '{role_name}' already exists as an agent\n\n{display_text}" if current_roles else f"❌ Error: Name '{role_name}' already exists as an agent"
                return current_roles, error_message, name, vote_value
            
            # Check against existing roles
            if any(r['name'] == role_name for r in current_roles):
                display_text = self._format_roles_display(current_roles)
                error_message = f"❌ Error: Role name already exists\n\n{display_text}" if current_roles else "❌ Error: Role name already exists"
                return current_roles, error_message, name, vote_value
            
            # Add new role with optional vote value
            new_role = {
                'name': role_name,
                'vote_value': vote_value if vote_value != 1.0 else None  # Only store if different from default 1.0
            }
            updated_roles = current_roles + [new_role]
            display_text = self._format_roles_display(updated_roles)
            success_message = f"✅ Role '{role_name}' added successfully!\n\n{display_text}"
            return updated_roles, success_message, "", None
        
        def clear_all_roles():
            """Clear all roles"""
            return [], "No roles added yet. Create roles to define project responsibilities.", "", None
        
        def add_individual(name, vote_value, profile, role, current_individuals, current_profiles, current_roles, current_agents):
            """Add a new individual to the list"""
            if not name.strip():
                return current_individuals, "❌ Please enter an individual name", name, vote_value, profile, role
            
            # Validate no spaces in name
            if ' ' in name.strip():
                return current_individuals, "❌ Individual name cannot contain spaces (use underscores instead, e.g., 'john_doe')", name, vote_value, profile, role
            
            # Validate vote_value is not negative if provided
            if vote_value is not None and vote_value < 0.0:
                return current_individuals, "❌ Vote value cannot be negative", name, vote_value, profile, role
            
            # Check for global name uniqueness across all participant types
            individual_name = name.strip()
            
            # Check against existing roles
            if any(r['name'] == individual_name for r in current_roles):
                return current_individuals, f"❌ Name '{individual_name}' already exists as a role", name, vote_value, profile, role
            
            # Check against existing agents
            if any(a['name'] == individual_name for a in current_agents):
                return current_individuals, f"❌ Name '{individual_name}' already exists as an agent", name, vote_value, profile, role
            
            # Check against existing individuals
            if any(i['name'] == individual_name for i in current_individuals):
                return current_individuals, "❌ Individual name already exists", name, vote_value, profile, role
            
            # Create new individual
            new_individual = {
                'name': name.strip(),
                'vote_value': vote_value if vote_value not in (None, 1.0) else None,  # Only store if different from default 1.0
                'profile': profile if profile else None,
                'role': role if role else None
            }
            
            updated_individuals = current_individuals + [new_individual]
            
            # Update display
            display_text = self._format_individuals_display(updated_individuals)
            success_message = f"✅ Individual '{new_individual['name']}' added successfully!\n\n{display_text}"
            
            # Update dropdown choices for next individual
            return updated_individuals, success_message, "", 1.0, None, None
        
        def clear_individuals():
            """Clear all individuals"""
            return [], "No individuals added yet"
        
        def update_individual_dropdowns(current_roles, current_profiles):
            """Update individual dropdown choices when roles or profiles change"""
            return (
                gr.Dropdown(choices=[p['name'] for p in current_profiles] if current_profiles else [], value=None),
                gr.Dropdown(choices=[r['name'] for r in current_roles] if current_roles else [], value=None)
            )
        
        def add_agent(name, vote_value, confidence, autonomy_level, explainability, role, current_agents, current_roles, current_individuals):
            """Add a new agent to the list"""
            if not name.strip():
                return current_agents, "❌ Please enter an agent name", name, vote_value, confidence, autonomy_level, explainability, role
            
            # Validate no spaces in name
            if ' ' in name.strip():
                return current_agents, "❌ Agent name cannot contain spaces (use underscores instead, e.g., 'my_agent')", name, vote_value, confidence, autonomy_level, explainability, role
            
            # Validate vote_value is not negative if provided
            if vote_value is not None and vote_value < 0.0:
                return current_agents, "❌ Vote value cannot be negative", name, vote_value, confidence, autonomy_level, explainability, role
            
            # Validate agent attribute ranges (must be between 0.0 and 1.0)
            if confidence is not None and (confidence < 0.0 or confidence > 1.0):
                return current_agents, "❌ Confidence must be between 0.0 and 1.0", name, vote_value, confidence, autonomy_level, explainability, role
            
            if autonomy_level is not None and (autonomy_level < 0.0 or autonomy_level > 1.0):
                return current_agents, "❌ Autonomy Level must be between 0.0 and 1.0", name, vote_value, confidence, autonomy_level, explainability, role
            
            if explainability is not None and (explainability < 0.0 or explainability > 1.0):
                return current_agents, "❌ Explainability must be between 0.0 and 1.0", name, vote_value, confidence, autonomy_level, explainability, role
            
            # Check for global name uniqueness across all participant types
            agent_name = name.strip()
            
            # Check against existing roles
            if any(r['name'] == agent_name for r in current_roles):
                return current_agents, f"❌ Name '{agent_name}' already exists as a role", name, vote_value, confidence, autonomy_level, explainability, role
            
            # Check against existing individuals
            if any(i['name'] == agent_name for i in current_individuals):
                return current_agents, f"❌ Name '{agent_name}' already exists as an individual", name, vote_value, confidence, autonomy_level, explainability, role
            
            # Check against existing agents
            if any(a['name'] == agent_name for a in current_agents):
                return current_agents, "❌ Agent name already exists", name, vote_value, confidence, autonomy_level, explainability, role
            
            # Create new agent
            new_agent = {
                'name': name.strip(),
                'vote_value': vote_value if vote_value != 1.0 else None,  # Only store if different from default 1.0
                'confidence': confidence if confidence is not None else None,
                'autonomy_level': autonomy_level if autonomy_level is not None else None,
                'explainability': explainability if explainability is not None else None,
                'role': role if role else None
            }
            
            updated_agents = current_agents + [new_agent]
            
            # Update display
            display_text = self._format_agents_display(updated_agents)
            success_message = f"✅ Agent '{new_agent['name']}' added successfully!\n\n{display_text}"
            
            return updated_agents, success_message, "", 1.0, None, None, None, None
        
        def clear_agents():
            """Clear all agents"""
            return [], "No agents added yet"
        
        def update_agent_role_dropdown(current_roles):
            """Update agent role dropdown when roles change"""
            return gr.Dropdown(choices=[r['name'] for r in current_roles] if current_roles else [], value=None)
        
        # Scope event handlers
        def add_project(name, platform, repo_owner, repo_name, current_projects, current_activities=None, current_tasks=None):
            """Add a new project to the list"""
            if not name.strip():
                display_text = self._format_projects_display(current_projects)
                error_message = f"❌ Error: Please enter a project name\n\n{display_text}" if current_projects else "❌ Error: Please enter a project name"
                return current_projects, error_message, name, platform, repo_owner, repo_name
            
            # Validate no spaces in name
            if ' ' in name.strip():
                display_text = self._format_projects_display(current_projects)
                error_message = f"❌ Error: Project name cannot contain spaces (use underscores instead, e.g., 'my_project')\n\n{display_text}" if current_projects else "❌ Error: Project name cannot contain spaces (use underscores instead, e.g., 'my_project')"
                return current_projects, error_message, name, platform, repo_owner, repo_name
            if repo_owner is not None and ' ' in repo_owner.strip():
                display_text = self._format_projects_display(current_projects)
                error_message = f"❌ Error: Repository owner name cannot contain spaces\n\n{display_text}" if current_projects else "❌ Error: Repository owner name cannot contain spaces"
                return current_projects, error_message, name, platform, repo_owner, repo_name
            if repo_name is not None and ' ' in repo_name.strip():
                display_text = self._format_projects_display(current_projects)
                error_message = f"❌ Error: Repository name cannot contain spaces\n\n{display_text}" if current_projects else "❌ Error: Repository name cannot contain spaces"
                return current_projects, error_message, name, platform, repo_owner, repo_name
            
            # Check for global name uniqueness across projects, activities, and tasks
            project_name = name.strip()
            
            # Check against existing projects
            if any(p['name'] == project_name for p in current_projects):
                display_text = self._format_projects_display(current_projects)
                error_message = f"❌ Error: Project name already exists\n\n{display_text}" if current_projects else "❌ Error: Project name already exists"
                return current_projects, error_message, name, platform, repo_owner, repo_name
            
            # Check against existing activities (if provided)
            if current_activities and any(a['name'] == project_name for a in current_activities):
                display_text = self._format_projects_display(current_projects)
                error_message = f"❌ Error: Name '{project_name}' already exists as an activity\n\n{display_text}" if current_projects else f"❌ Error: Name '{project_name}' already exists as an activity"
                return current_projects, error_message, name, platform, repo_owner, repo_name
            
            # Check against existing tasks (if provided)
            if current_tasks and any(t['name'] == project_name for t in current_tasks):
                display_text = self._format_projects_display(current_projects)
                error_message = f"❌ Error: Name '{project_name}' already exists as a task\n\n{display_text}" if current_projects else f"❌ Error: Name '{project_name}' already exists as a task"
                return current_projects, error_message, name, platform, repo_owner, repo_name
            
            # Validate platform and repository relationship
            if platform and platform.strip():
                if not repo_owner or not repo_owner.strip():
                    display_text = self._format_projects_display(current_projects)
                    error_message = f"❌ Error: Repository owner is required when a platform is selected\n\n{display_text}" if current_projects else "❌ Error: Repository owner is required when a platform is selected"
                    return current_projects, error_message, name, platform, repo_owner, repo_name
                if not repo_name or not repo_name.strip():
                    display_text = self._format_projects_display(current_projects)
                    error_message = f"❌ Error: Repository name is required when a platform is selected\n\n{display_text}" if current_projects else "❌ Error: Repository name is required when a platform is selected"
                    return current_projects, error_message, name, platform, repo_owner, repo_name
                
                # Check for duplicate platform-repository combination
                full_repo = f"{repo_owner.strip()}/{repo_name.strip()}"
                if any(p.get('platform') == platform.strip() and p.get('repo') == full_repo for p in current_projects):
                    display_text = self._format_projects_display(current_projects)
                    error_message = f"❌ Error: Repository {full_repo} already exists for {platform}\n\n{display_text}" if current_projects else f"❌ Error: Repository {full_repo} already exists for {platform}"
                    return current_projects, error_message, name, platform, repo_owner, repo_name
            
            # Create new project
            new_project = {
                'name': name.strip(),
                'platform': platform.strip() if platform and platform.strip() else None,
                'repo': f"{repo_owner.strip()}/{repo_name.strip()}" if repo_owner and repo_owner.strip() and repo_name and repo_name.strip() else None
            }
            
            updated_projects = current_projects + [new_project]
            success_message = self._format_projects_display(updated_projects)
            
            return updated_projects, success_message, "", "", "", ""
        
        def clear_projects():
            """Clear all projects"""
            return [], "No projects added yet. Create projects to define your organizational structure."
        
        def add_activity(name, parent, current_activities, current_projects):
            """Add a new activity to the list"""
            if not name.strip():
                display_text = self._format_activities_display(current_activities)
                error_message = f"❌ Error: Please enter an activity name\n\n{display_text}" if current_activities else "❌ Error: Please enter an activity name"
                return current_activities, error_message, name, parent
            
            # Validate no spaces in name
            if ' ' in name.strip():
                display_text = self._format_activities_display(current_activities)
                error_message = f"❌ Error: Activity name cannot contain spaces (use underscores instead, e.g., 'my_activity')\n\n{display_text}" if current_activities else "❌ Error: Activity name cannot contain spaces (use underscores instead, e.g., 'my_activity')"
                return current_activities, error_message, name, parent
            
            # Check for global name uniqueness across projects and activities
            activity_name = name.strip()
            
            # Check against existing projects
            if any(p['name'] == activity_name for p in current_projects):
                display_text = self._format_activities_display(current_activities)
                error_message = f"❌ Error: Name '{activity_name}' already exists as a project\n\n{display_text}" if current_activities else f"❌ Error: Name '{activity_name}' already exists as a project"
                return current_activities, error_message, name, parent
            
            # Check against existing activities
            if any(a['name'] == activity_name for a in current_activities):
                display_text = self._format_activities_display(current_activities)
                error_message = f"❌ Error: Activity name already exists\n\n{display_text}" if current_activities else "❌ Error: Activity name already exists"
                return current_activities, error_message, name, parent
            
            # Create new activity
            new_activity = {
                'name': activity_name,
                'parent': parent if parent else None
            }
            
            updated_activities = current_activities + [new_activity]
            success_message = self._format_activities_display(updated_activities)
            
            return updated_activities, success_message, "", None
        
        def clear_activities():
            """Clear all activities"""
            return [], "No activities added yet. Create activities to organize your project workflow."
        
        def update_activity_parent_dropdown(current_projects):
            """Update activity parent dropdown when projects change"""
            project_choices = [p['name'] for p in current_projects]
            return gr.Dropdown(choices=project_choices, value=None)
        
        def add_task(name, parent, task_type, action, current_tasks, current_projects, current_activities):
            """Add a new task to the list"""
            if not name.strip():
                display_text = self._format_tasks_display(current_tasks)
                error_message = f"❌ Error: Please enter a task name\n\n{display_text}" if current_tasks else "❌ Error: Please enter a task name"
                return current_tasks, error_message, name, parent, task_type, action
            
            # Validate no spaces in name
            if ' ' in name.strip():
                display_text = self._format_tasks_display(current_tasks)
                error_message = f"❌ Error: Task name cannot contain spaces (use underscores instead, e.g., 'my_task')\n\n{display_text}" if current_tasks else "❌ Error: Task name cannot contain spaces (use underscores instead, e.g., 'my_task')"
                return current_tasks, error_message, name, parent, task_type, action
            
            # Check for global name uniqueness across projects, activities, and tasks
            task_name = name.strip()
            
            # Check against existing projects
            if any(p['name'] == task_name for p in current_projects):
                display_text = self._format_tasks_display(current_tasks)
                error_message = f"❌ Error: Name '{task_name}' already exists as a project\n\n{display_text}" if current_tasks else f"❌ Error: Name '{task_name}' already exists as a project"
                return current_tasks, error_message, name, parent, task_type, action
            
            # Check against existing activities
            if any(a['name'] == task_name for a in current_activities):
                display_text = self._format_tasks_display(current_tasks)
                error_message = f"❌ Error: Name '{task_name}' already exists as an activity\n\n{display_text}" if current_tasks else f"❌ Error: Name '{task_name}' already exists as an activity"
                return current_tasks, error_message, name, parent, task_type, action
            
            # Check against existing tasks
            if any(t['name'] == task_name for t in current_tasks):
                display_text = self._format_tasks_display(current_tasks)
                error_message = f"❌ Error: Task name already exists\n\n{display_text}" if current_tasks else "❌ Error: Task name already exists"
                return current_tasks, error_message, name, parent, task_type, action
            
            # Validate parent is an activity (if provided)
            if parent and parent.strip():
                if not any(a['name'] == parent for a in current_activities):
                    display_text = self._format_tasks_display(current_tasks)
                    error_message = f"❌ Error: Parent '{parent}' is not a valid activity\n\n{display_text}" if current_tasks else f"❌ Error: Parent '{parent}' is not a valid activity"
                    return current_tasks, error_message, name, parent, task_type, action
            
            # Create new task
            new_task = {
                'name': task_name,
                'parent': parent if parent and parent.strip() else None,
                'type': task_type if task_type and task_type.strip() else None,
                'action': action if action and action.strip() else None
            }
            
            updated_tasks = current_tasks + [new_task]
            success_message = self._format_tasks_display(updated_tasks)
            
            return updated_tasks, success_message, "", None, "", ""
        
        def clear_tasks():
            """Clear all tasks"""
            return [], "No tasks added yet. Create tasks to define specific governance actions."
        
        def update_task_action_dropdown(task_type):
            """Update task action dropdown based on task type"""
            if task_type == "Pull request":
                action_choices = ["", "merge", "review"]
                return gr.Dropdown(choices=action_choices, value="", visible=True)
            elif task_type == "MemberLifecycle":
                action_choices = ["", "onboard", "remove"]
                return gr.Dropdown(choices=action_choices, value="", visible=True)
            else:
                # Empty type - hide action dropdown
                return gr.Dropdown(choices=[""], value="", visible=False)
        
        def update_task_parent_dropdown(current_activities):
            """Update task parent dropdown when activities change (tasks can only have activities as parents)"""
            parent_choices = [a['name'] for a in current_activities]
            return gr.Dropdown(choices=parent_choices, value=None)
        
        def update_scope_dropdown(projects_data, activities_data, tasks_data):
            """Update policy scope dropdown when scope definitions change"""
            scope_choices = []
            
            # Extract names from structured data
            for project in projects_data:
                if project['name']:
                    scope_choices.append(project['name'])
            for activity in activities_data:
                if activity['name']:
                    scope_choices.append(activity['name'])
            for task in tasks_data:
                if task['name']:
                    scope_choices.append(task['name'])
            
            return gr.Dropdown(choices=sorted(list(set(scope_choices))), value=None)
        
        def update_participant_dropdown(roles_data, individuals_data, agents_data):
            """Update policy participants dropdown when participant definitions change"""
            participant_choices = self._extract_participant_names(roles_data, individuals_data, agents_data)
            return (
                gr.Dropdown(choices=participant_choices, value=None),  # policy_participants
                gr.Dropdown(choices=participant_choices, value=None),  # veto_participants
                gr.Dropdown(choices=participant_choices, value=None),  # excluded_participants
                gr.Dropdown(choices=participant_choices, value=None),  # phase_participants
                gr.Dropdown(choices=participant_choices, value=None),  # phase_veto_participants
                gr.Dropdown(choices=participant_choices, value=None)   # phase_excluded_participants
            )
        
        def update_phase_participant_dropdown(roles_data, individuals_data, agents_data):
            """Update phase participants dropdown when participant definitions change"""
            participant_choices = self._extract_participant_names(roles_data, individuals_data, agents_data)
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
            show_string_list = decision_type == "StringList"
            show_element_list = decision_type == "ElementList"
            return (
                gr.update(visible=show_string_list),
                gr.update(visible=show_element_list)
            )
        
        def update_condition_visibility(condition_type):
            """Update visibility of condition fields based on condition type"""
            show_veto = condition_type == "VetoRight"
            show_exclusion = condition_type == "ParticipantExclusion"
            show_min_participants = condition_type == "MinParticipants"
            show_deadline = condition_type == "Deadline"
            show_min_decision = condition_type == "MinDecisionTime"
            show_check_ci_cd = condition_type == "CheckCiCd"
            show_label = condition_type == "LabelCondition"
            show_min_time = condition_type == "MinTime"
            
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
                gr.Dropdown(visible=show_check_ci_cd),     # check_ci_cd_evaluation_mode
                gr.Checkbox(visible=show_check_ci_cd),     # check_ci_cd_value
                gr.Dropdown(visible=show_label),     # label_condition_type
                gr.Dropdown(visible=show_label),     # label_condition_operator
                gr.Textbox(visible=show_label),      # label_condition_labels
                gr.Dropdown(visible=show_min_time),  # min_time_evaluation_mode
                gr.Dropdown(visible=show_min_time),  # min_time_activity
                gr.Number(visible=show_min_time),    # min_time_offset_value
                gr.Dropdown(visible=show_min_time)   # min_time_offset_unit
            ]
        
        def add_policy(name, policy_type, scope, participants, decision_type, decision_options, voting_ratio, 
                    default_decision, fallback_policy, condition_type, veto_participants, excluded_participants,
                    min_participants, deadline_offset_value, deadline_offset_unit, deadline_date,
                    min_decision_offset_value, min_decision_offset_unit, min_decision_date,
            label_condition_type, label_condition_operator, label_condition_labels, 
            communication_channel,
                    added_conditions_list, current_policies):
            """Add a new policy to the list"""
            # Validate policy name (mandatory)
            if not name.strip():
                display_text = self._format_policies_display(current_policies)
                error_message = f"❌ Error: Please enter a policy name\n\n{display_text}" if current_policies else "❌ Error: Please enter a policy name"
                return current_policies, error_message
            if ' ' in name.strip():
                display_text = self._format_policies_display(current_policies)
                error_message = f"❌ Error: Policy name cannot contain spaces (use underscores instead, e.g., 'my_policy')\n\n{display_text}" if current_policies else "❌ Error: Policy name cannot contain spaces (use underscores instead, e.g., 'my_policy')"
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

            if voting_ratio is not None and (voting_ratio < 0.0 or voting_ratio > 1.0):
                display_text = self._format_policies_display(current_policies)
                error_message = f"❌ Error: Voting ratio must be between 0.0 and 1.0\n\n{display_text}" if current_policies else "❌ Error: Voting ratio must be between 0.0 and 1.0"
                return current_policies, error_message
            
            # Check if policy already exists
            if any(p['name'] == name.strip() for p in current_policies):
                display_text = self._format_policies_display(current_policies)
                error_message = f"❌ Error: Policy name '{name.strip()}' already exists\n\n{display_text}"
                return current_policies, error_message
            
            # Handle decision_options: convert list to string for ElementList, keep string for StringList
            final_decision_options = None
            if decision_type in ["StringList", "ElementList"] and decision_options:
                if decision_type == "ElementList" and isinstance(decision_options, list):
                    # Convert list from multiselect dropdown to comma-separated string
                    final_decision_options = ",".join(decision_options) if decision_options else None
                else:
                    # StringList: use as-is (already a string from textbox)
                    final_decision_options = decision_options
            
            # Create new policy
            new_policy = {
                'name': name.strip(),
                'type': policy_type,
                'scope': scope if scope else None,
                'participants': participants if participants else None,
                'decision_type': decision_type,
                'decision_options': final_decision_options,
                'voting_ratio': voting_ratio if policy_type in ["MajorityPolicy", "AbsoluteMajorityPolicy", "VotingPolicy"] else None,
                'default_decision': default_decision if policy_type == "LeaderDrivenPolicy" else None,
                'fallback_policy': fallback_policy if policy_type in ["ConsensusPolicy", "LazyConsensusPolicy"] else None,
                'communication_channel': communication_channel.strip() if communication_channel and communication_channel.strip() else None,
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
            # Clear all policies
            return [], "No policies added yet"

        def add_condition(condition_type, veto_participants, excluded_participants, min_participants,
                        deadline_offset_value, deadline_offset_unit, deadline_date,
                        min_decision_offset_value, min_decision_offset_unit, min_decision_date,
                        check_ci_cd_evaluation_mode, check_ci_cd_value,
                        label_condition_type, label_condition_operator, label_condition_labels,
                        min_time_evaluation_mode, min_time_activity, min_time_offset_value, min_time_offset_unit,
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
            
            # Helper function to return error while keeping form values
            def return_error(error_msg):
                return (
                    format_conditions_with_error(error_msg),  # added_conditions_list
                    condition_type,  # keep condition_type
                    veto_participants,  # keep veto_participants
                    excluded_participants,  # keep excluded_participants
                    min_participants,  # keep min_participants
                    deadline_offset_value,  # keep deadline_offset_value
                    deadline_offset_unit,  # keep deadline_offset_unit
                    deadline_date,  # keep deadline_date
                    min_decision_offset_value,  # keep min_decision_offset_value
                    min_decision_offset_unit,  # keep min_decision_offset_unit
                    min_decision_date,  # keep min_decision_date
                    check_ci_cd_evaluation_mode,  # keep check_ci_cd_evaluation_mode
                    check_ci_cd_value,  # keep check_ci_cd_value
                    label_condition_type,  # keep label_condition_type
                    label_condition_operator,  # keep label_condition_operator
                    label_condition_labels,  # keep label_condition_labels
                    min_time_evaluation_mode,  # keep min_time_evaluation_mode
                    min_time_activity,  # keep min_time_activity
                    min_time_offset_value,  # keep min_time_offset_value
                    min_time_offset_unit  # keep min_time_offset_unit
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
                elif condition.startswith('MinTime'):
                    existing_types.append('MinTime')
                elif condition.startswith('CheckCiCd'):
                    existing_types.append('CheckCiCd')
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
                    is_valid, error_msg = validate_date_format(deadline_date)
                    if not is_valid:
                        return return_error(f"Deadline date error: {error_msg}")
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
                    is_valid, error_msg = validate_date_format(min_decision_date)
                    if not is_valid:
                        return return_error(f"Minimum decision time date error: {error_msg}")
                    parts.append(min_decision_date.strip())
                if not parts:
                    return return_error("Please specify minimum decision time offset or date")
                condition_str = f"MinDecisionTime: {', '.join(parts)}"
                
            elif condition_type == "CheckCiCd":
                # CheckCiCd: evaluation_mode (optional) and boolean value (true/false)
                evaluation_part = f"{check_ci_cd_evaluation_mode} " if check_ci_cd_evaluation_mode and check_ci_cd_evaluation_mode.strip() else ""
                check_value = "true" if check_ci_cd_value else "false"
                condition_str = f"CheckCiCd {evaluation_part}: {check_value}"
                
            elif condition_type == "MinTime":
                # MinTime: evaluation_mode (optional), activity (required), offset value and unit (required)
                if not min_time_activity or not min_time_activity.strip():
                    return return_error("Please specify activity type (Activity/InActivity)")
                if not min_time_offset_value or min_time_offset_value < 1:
                    return return_error("Please specify MinTime offset value (≥1)")
                if not min_time_offset_unit:
                    return return_error("Please specify MinTime offset unit")
                # Build with optional evaluation mode
                evaluation_part = f"{min_time_evaluation_mode} " if min_time_evaluation_mode and min_time_evaluation_mode.strip() else ""
                condition_str = f"MinTime {evaluation_part}of {min_time_activity}: {min_time_offset_value} {min_time_offset_unit}".rstrip()
                
            elif condition_type == "LabelCondition":
                if not label_condition_labels:
                    return return_error("Please specify labels")
                labels = [l.strip() for l in label_condition_labels.split(',') if l.strip()]
                if not labels:
                    return return_error("Please specify valid labels")
                
                # Build the condition string with optional evaluation mode
                evaluation_part = f"{label_condition_type} " if label_condition_type and label_condition_type.strip() else ""
                operator_part = f"{label_condition_operator} " if label_condition_operator else ""
                condition_str = f"LabelCondition {evaluation_part}{operator_part}: {', '.join(labels)}".rstrip()
            
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
                    "",  # check_ci_cd_evaluation_mode
                    True,  # check_ci_cd_value
                    "",  # label_condition_type
                    "",  # label_condition_operator
                    "",  # label_condition_labels
                    "",  # min_time_evaluation_mode
                    "Activity",  # min_time_activity
                    None,  # min_time_offset_value
                    "days"  # min_time_offset_unit
                )
            
            return return_error("Unable to add condition")
        
        def clear_conditions():
            """Clear all conditions for the current policy"""
            return ""
        
        def add_phase_condition(phase_condition_type, phase_veto_participants, phase_excluded_participants, 
                            phase_min_participants, phase_deadline_offset_value, phase_deadline_offset_unit, 
                            phase_deadline_date, phase_min_decision_offset_value, phase_min_decision_offset_unit, 
                            phase_min_decision_date, phase_check_ci_cd_evaluation_mode, phase_check_ci_cd_value,
                            phase_label_condition_type, phase_label_condition_operator, 
                            phase_label_condition_labels, phase_min_time_evaluation_mode, phase_min_time_activity,
                            phase_min_time_offset_value, phase_min_time_offset_unit, current_phase_conditions_text):
            """Add a condition to the current phase"""
            
            # Parse existing conditions from the display text (ignore error messages and success messages)
            existing_conditions = []
            if current_phase_conditions_text.strip():
                for line in current_phase_conditions_text.strip().split('\n'):
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
            
            # Helper function to return error while keeping form values
            def return_error(error_msg):
                return (
                    format_conditions_with_error(error_msg),  # added_phase_conditions_list
                    phase_condition_type,  # keep phase_condition_type
                    phase_veto_participants,  # keep phase_veto_participants
                    phase_excluded_participants,  # keep phase_excluded_participants
                    phase_min_participants,  # keep phase_min_participants
                    phase_deadline_offset_value,  # keep phase_deadline_offset_value
                    phase_deadline_offset_unit,  # keep phase_deadline_offset_unit
                    phase_deadline_date,  # keep phase_deadline_date
                    phase_min_decision_offset_value,  # keep phase_min_decision_offset_value
                    phase_min_decision_offset_unit,  # keep phase_min_decision_offset_unit
                    phase_min_decision_date,  # keep phase_min_decision_date
                    phase_check_ci_cd_evaluation_mode,  # keep phase_check_ci_cd_evaluation_mode
                    phase_check_ci_cd_value,  # keep phase_check_ci_cd_value
                    phase_label_condition_type,  # keep phase_label_condition_type
                    phase_label_condition_operator,  # keep phase_label_condition_operator
                    phase_label_condition_labels,  # keep phase_label_condition_labels
                    phase_min_time_evaluation_mode,  # keep phase_min_time_evaluation_mode
                    phase_min_time_activity,  # keep phase_min_time_activity
                    phase_min_time_offset_value,  # keep phase_min_time_offset_value
                    phase_min_time_offset_unit  # keep phase_min_time_offset_unit
                )
            
            if not phase_condition_type:
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
                elif condition.startswith('MinTime'):
                    existing_types.append('MinTime')
                elif condition.startswith('CheckCiCd'):
                    existing_types.append('CheckCiCd')
                # LabelCondition can have multiple entries, so we don't track it
            
            if phase_condition_type != "LabelCondition" and phase_condition_type in existing_types:
                return return_error(f"{phase_condition_type} already exists. Only LabelCondition can be added multiple times.")
            
            # Create the condition string
            condition_str = ""
            
            if phase_condition_type == "VetoRight":
                if not phase_veto_participants:
                    return return_error("Please specify veto participants")
                participants_list = [p.strip() for p in phase_veto_participants if p.strip()] if isinstance(phase_veto_participants, list) else [phase_veto_participants.strip()]
                condition_str = f"VetoRight: {', '.join(participants_list)}"
                
            elif phase_condition_type == "ParticipantExclusion":
                if not phase_excluded_participants:
                    return return_error("Please specify excluded participants")
                participants_list = [p.strip() for p in phase_excluded_participants if p.strip()] if isinstance(phase_excluded_participants, list) else [phase_excluded_participants.strip()]
                condition_str = f"ParticipantExclusion: {', '.join(participants_list)}"
                
            elif phase_condition_type == "MinParticipants":
                if not phase_min_participants or phase_min_participants < 1:
                    return return_error("Please specify minimum participants (≥1)")
                condition_str = f"MinParticipants: {phase_min_participants}"
                
            elif phase_condition_type == "Deadline":
                parts = []
                if phase_deadline_offset_value and phase_deadline_offset_unit:
                    if phase_deadline_offset_value < 1:
                        return return_error("Deadline offset value must be ≥1")
                    parts.append(f"{phase_deadline_offset_value} {phase_deadline_offset_unit}")
                if phase_deadline_date and phase_deadline_date.strip():
                    is_valid, error_msg = validate_date_format(phase_deadline_date)
                    if not is_valid:
                        return return_error(f"Deadline date error: {error_msg}")
                    parts.append(phase_deadline_date.strip())
                if not parts:
                    return return_error("Please specify deadline offset or date")
                condition_str = f"Deadline: {', '.join(parts)}"
                
            elif phase_condition_type == "MinDecisionTime":
                parts = []
                if phase_min_decision_offset_value and phase_min_decision_offset_unit:
                    if phase_min_decision_offset_value < 1:
                        return return_error("Minimum decision time offset value must be ≥1")
                    parts.append(f"{phase_min_decision_offset_value} {phase_min_decision_offset_unit}")
                if phase_min_decision_date and phase_min_decision_date.strip():
                    is_valid, error_msg = validate_date_format(phase_min_decision_date)
                    if not is_valid:
                        return return_error(f"Minimum decision time date error: {error_msg}")
                    parts.append(phase_min_decision_date.strip())
                if not parts:
                    return return_error("Please specify minimum decision time offset or date")
                condition_str = f"MinDecisionTime: {', '.join(parts)}"
                
            elif phase_condition_type == "CheckCiCd":
                # CheckCiCd: evaluation_mode (optional) and boolean value (true/false)
                evaluation_part = f"{phase_check_ci_cd_evaluation_mode} " if phase_check_ci_cd_evaluation_mode and phase_check_ci_cd_evaluation_mode.strip() else ""
                check_value = "true" if phase_check_ci_cd_value else "false"
                condition_str = f"CheckCiCd {evaluation_part}: {check_value}"
                
            elif phase_condition_type == "MinTime":
                # MinTime: evaluation_mode (optional), activity (required), offset value and unit (required)
                if not phase_min_time_activity or not phase_min_time_activity.strip():
                    return return_error("Please specify activity type (Activity/InActivity)")
                if not phase_min_time_offset_value or phase_min_time_offset_value < 1:
                    return return_error("Please specify MinTime offset value (≥1)")
                if not phase_min_time_offset_unit:
                    return return_error("Please specify MinTime offset unit")
                # Build with optional evaluation mode
                evaluation_part = f"{phase_min_time_evaluation_mode} " if phase_min_time_evaluation_mode and phase_min_time_evaluation_mode.strip() else ""
                condition_str = f"MinTime {evaluation_part}of {phase_min_time_activity}: {phase_min_time_offset_value} {phase_min_time_offset_unit}".rstrip()
                
            elif phase_condition_type == "LabelCondition":
                if not phase_label_condition_labels:
                    return return_error("Please specify labels")
                labels = [l.strip() for l in phase_label_condition_labels.split(',') if l.strip()]
                if not labels:
                    return return_error("Please specify valid labels")
                
                # Build the condition string with optional evaluation mode
                evaluation_part = f"{phase_label_condition_type} " if phase_label_condition_type and phase_label_condition_type.strip() else ""
                operator_part = f"{phase_label_condition_operator} " if phase_label_condition_operator else ""
                condition_str = f"LabelCondition {evaluation_part}{operator_part}: {', '.join(labels)}".rstrip()
            
            if condition_str:
                # Add to existing conditions and format success message
                updated_conditions = existing_conditions + [condition_str]
                conditions_text = '\n'.join(updated_conditions)
                success_message = f"✅ {phase_condition_type} condition added successfully!\n\n{conditions_text}"
                return (
                    success_message,  # added_phase_conditions_list
                    gr.Dropdown(value=""),  # phase_condition_type
                    gr.Dropdown(value=None),  # phase_veto_participants
                    gr.Dropdown(value=None),  # phase_excluded_participants
                    None,  # phase_min_participants
                    None,  # phase_deadline_offset_value
                    "days",  # phase_deadline_offset_unit
                    "",  # phase_deadline_date
                    None,  # phase_min_decision_offset_value
                    "days",  # phase_min_decision_offset_unit
                    "",  # phase_min_decision_date
                    "",  # phase_check_ci_cd_evaluation_mode
                    True,  # phase_check_ci_cd_value
                    "",  # phase_label_condition_type
                    "",  # phase_label_condition_operator
                    "",  # phase_label_condition_labels
                    "",  # phase_min_time_evaluation_mode
                    "Activity",  # phase_min_time_activity
                    None,  # phase_min_time_offset_value
                    "days"  # phase_min_time_offset_unit
                )
            
            return return_error("Unable to add condition")
        
        def clear_phase_conditions():
            """Clear all conditions for the current phase"""
            return ""
        
        def update_phase_condition_visibility(phase_condition_type):
            """Update visibility of phase condition fields based on condition type"""
            show_veto = phase_condition_type == "VetoRight"
            show_exclusion = phase_condition_type == "ParticipantExclusion"
            show_min_participants = phase_condition_type == "MinParticipants"
            show_deadline = phase_condition_type == "Deadline"
            show_min_decision = phase_condition_type == "MinDecisionTime"
            show_check_ci_cd = phase_condition_type == "CheckCiCd"
            show_label = phase_condition_type == "LabelCondition"
            show_min_time = phase_condition_type == "MinTime"
            
            return [
                gr.Dropdown(visible=show_veto),       # phase_veto_participants
                gr.Dropdown(visible=show_exclusion),  # phase_excluded_participants 
                gr.Number(visible=show_min_participants), # phase_min_participants
                gr.Number(visible=show_deadline),     # phase_deadline_offset_value
                gr.Dropdown(visible=show_deadline),   # phase_deadline_offset_unit
                gr.Textbox(visible=show_deadline),    # phase_deadline_date
                gr.Number(visible=show_min_decision), # phase_min_decision_offset_value
                gr.Dropdown(visible=show_min_decision), # phase_min_decision_offset_unit
                gr.Textbox(visible=show_min_decision), # phase_min_decision_date
                gr.Dropdown(visible=show_check_ci_cd),     # phase_check_ci_cd_evaluation_mode
                gr.Checkbox(visible=show_check_ci_cd),     # phase_check_ci_cd_value
                gr.Dropdown(visible=show_label),     # phase_label_condition_type
                gr.Dropdown(visible=show_label),     # phase_label_condition_operator
                gr.Textbox(visible=show_label),      # phase_label_condition_labels
                gr.Dropdown(visible=show_min_time),  # phase_min_time_evaluation_mode
                gr.Dropdown(visible=show_min_time),  # phase_min_time_activity
                gr.Number(visible=show_min_time),    # phase_min_time_offset_value
                gr.Dropdown(visible=show_min_time)   # phase_min_time_offset_unit
            ]
        
        # Composed Policy Functions
        def add_phase(phase_name, phase_type, phase_participants, phase_decision_type, phase_decision_options, 
                    phase_voting_ratio, phase_default_decision, phase_fallback_policy, phase_communication_channel, 
                    current_phases_text, added_phase_conditions_text):
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

            # Helper function to return error while keeping form values
            def return_phase_error(error_msg):
                return (
                    format_phases_with_error(error_msg),  # added_phases_list
                    phase_name,  # keep phase_name
                    phase_type,  # keep phase_type
                    phase_participants,  # keep phase_participants
                    phase_decision_type,  # keep phase_decision_type
                    phase_decision_options,  # keep phase_decision_options
                    phase_voting_ratio,  # keep phase_voting_ratio
                    phase_default_decision,  # keep phase_default_decision
                    phase_fallback_policy,  # keep phase_fallback_policy
                    phase_communication_channel,   # keep phase_communication_channel
                    added_phase_conditions_text    # keep added_phase_conditions_text
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
            if phase_decision_options and phase_decision_type != "BooleanDecision":
                # Handle both string (StringList) and list (ElementList) inputs
                if isinstance(phase_decision_options, list):
                    options_clean = ",".join(phase_decision_options) if phase_decision_options else ""
                else:
                    options_clean = phase_decision_options.strip() if isinstance(phase_decision_options, str) else str(phase_decision_options)
                
                if options_clean:  # Only add if not empty after processing
                    details.append(f"options: {options_clean}")

            # Optional communication channel detail
            if phase_communication_channel and phase_communication_channel.strip():
                details.append(f"channel: {phase_communication_channel.strip()}")

            if details:
                phase_display += f", {', '.join(details)}"

            # Append conditions to the phase display if any
            if added_phase_conditions_text and added_phase_conditions_text.strip():
                # Filter out error/success messages from conditions
                clean_conditions = []
                for line in added_phase_conditions_text.strip().split('\n'):
                    line = line.strip()
                    if line and not line.startswith('❌') and not line.startswith('✅'):
                        clean_conditions.append(line)
                if clean_conditions:
                    phase_display += f" [Conditions: {'; '.join(clean_conditions)}]"

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
                None,   # phase_fallback_policy - clear
                "",     # phase_communication_channel - clear
                ""      # added_phase_conditions_text - clear conditions
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
                                    communication_channel,
                                    added_conditions_list, current_policies):
            """Add policy and clear form fields only on success"""
            # First try to add the policy
            policies_result, display_result = add_policy(
                name, policy_type, scope, participants, decision_type, decision_options, voting_ratio, 
                default_decision, fallback_policy, condition_type, veto_participants, excluded_participants,
                min_participants, deadline_offset_value, deadline_offset_unit, deadline_date,
                min_decision_offset_value, min_decision_offset_unit, min_decision_date,
                label_condition_type, label_condition_operator, label_condition_labels, 
                communication_channel,
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
                    "", [], [], None, None, "days", "", None, "days", "", "pre", "", "", "",  # Clear condition fields - use empty lists for participant dropdowns
                    ""  # communication_channel clear
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
                    added_conditions_list,  # Keep added conditions list
                    communication_channel  # keep
                )

        def update_preview(*args):
            """Update the preview based on current form values"""
            return self._generate_dsl_from_form(*args)

        # removed unused local load_example (can be reintroduced and wired when enabling example loading)

        # Scope management handlers - Project-specific helpers
        def add_project_and_clear_form(name, repo_mode, repo_url, platform, repo_owner, repo_name, current_projects, current_activities, current_tasks):
            """Add project and return cleared form with proper repository visibility"""
            if repo_mode == "No":
                platform = ""
                repo_owner = ""
                repo_name = ""
            # Resolve platform/owner/name from URL if mode is "Via URL"
            elif repo_mode == "Via URL":
                if not repo_url or not repo_url.strip():
                    display_text = self._format_projects_display(current_projects)
                    error = f"❌ Please enter a repository URL, or switch to 'No'.\n\n{display_text}" if current_projects else "❌ Please enter a repository URL, or switch to 'No'."
                    return (
                        current_projects, error, name,
                        repo_mode,
                        gr.Textbox(value="", visible=True),   # project_repo_url stays visible
                        gr.Row(visible=False),                # project_manual_repo_row
                        platform, 
                        repo_owner,
                        repo_name
                    )
                parsed_platform, parsed_owner, parsed_repo_name = self._parse_repo_url(repo_url.strip())
                if not parsed_platform:
                    display_text = self._format_projects_display(current_projects)
                    error = f"❌ Invalid URL: `{repo_url.strip()}`. Expected: `https://github.com/owner/repo` or similar.\n\n{display_text}" if current_projects else f"❌ Invalid URL: `{repo_url.strip()}`.\n\nExpected: `https://github.com/owner/repo`"
                    return (
                        current_projects, error, name,
                        repo_mode,
                        gr.Textbox(value=repo_url, visible=True),  # keep URL visible for correction
                        gr.Row(visible=False),
                        platform, 
                        repo_owner,
                        repo_name
                    )
                platform = parsed_platform
                repo_owner = parsed_owner
                repo_name = parsed_repo_name

            # First add the project
            updated_projects, message, new_name, new_platform, new_repo_owner, new_repo_name = add_project(
                name, platform, repo_owner, repo_name, current_projects, current_activities, current_tasks
            )

            
            is_url_mode = repo_mode == "Via URL"
            is_manual_mode = repo_mode == "Manual"
            # Check if the addition was successful (no error message)
            if "❌ Error:" not in message:
                # Success: clear and hide repo fields since platform is cleared
                return ( # TODO: Check if visibility logic is correct for all modes
                    updated_projects, message, "", repo_mode, 
                    gr.Textbox(value="", visible=is_url_mode), 
                    gr.Row(visible=is_manual_mode),
                    "GitHub", # platform cleared
                    "", # repo_owner cleared
                    "" # repo_name cleared 
                )
            else:
                # Error: keep the values and maintain proper visibility of repo fields
                return (
                    updated_projects, message, new_name, 
                    repo_mode,
                    gr.Textbox(visible=is_url_mode),
                    gr.Row(visible=is_manual_mode),   
                    new_platform if new_platform and new_platform.strip() else "GitHub",
                    new_repo_owner,                                          new_repo_name,
                )

        template_components['template_dropdown'].change(
            fn=update_template_description,
            inputs=[template_components['template_dropdown']],
            outputs=[template_components['template_description']]
        )

        template_components['repo_link_mode'].change(
            fn=update_repo_link_visibility,
            inputs=[template_components['repo_link_mode']],
            outputs=[
                template_components['repo_url_input'],
                template_components['manual_repo_row'],
            ]
        )

        template_components['repo_url_input'].change(
            fn=autofill_from_url,
            inputs=[template_components['repo_url_input']],
            outputs=[
                template_components['repo_platform'],
                template_components['repo_owner'],
                template_components['repo_name'],
                template_components['template_status'],
            ]
        )

        template_components['apply_template_btn'].click(
            fn=apply_template,
            inputs=[
                template_components['template_dropdown'],
                template_components['repo_link_mode'],
                template_components['repo_url_input'],
                template_components['repo_platform'],
                template_components['repo_owner'],
                template_components['repo_name'],
                # Current state components (to return unchanged if no template selected)
                scope_components['projects_data'],
                scope_components['activities_data'],
                scope_components['tasks_data'],
                participant_components['profiles_data'],
                participant_components['roles_data'],
                participant_components['individuals_data'],
                participant_components['agents_data'],
                policy_components['policies_data'],
                policy_components['composed_policies_data'],
            ],
            outputs=[
                # Data states
                scope_components['projects_data'],
                scope_components['activities_data'],
                scope_components['tasks_data'],
                participant_components['profiles_data'],
                participant_components['roles_data'],
                participant_components['individuals_data'],
                participant_components['agents_data'],
                policy_components['policies_data'],
                policy_components['composed_policies_data'],
                # Display components
                scope_components['projects_display'],
                scope_components['activities_display'],
                scope_components['tasks_display'],
                participant_components['profiles_display'],
                participant_components['roles_display'],
                participant_components['individuals_display'],
                participant_components['agents_display'],
                policy_components['policies_display'],
                policy_components['composed_policies_display'],
                # Template status
                template_components['template_status'],
            ]
        )
        # TODO: To be applied if gradio-lite does not auto-update
        #         .then(
        #     fn=update_preview,
        #     inputs=[
        #         scope_components['projects_data'],
        #         scope_components['activities_data'],
        #         scope_components['tasks_data'],
        #         participant_components['profiles_data'],
        #         participant_components['roles_data'],
        #         participant_components['individuals_data'],
        #         participant_components['agents_data'],
        #         policy_components['policies_data'],
        #         policy_components['composed_policies_data'],
        #     ],
        #     outputs=[preview_components['preview_code']]
        # )
        
        scope_components['add_project_btn'].click(
            fn=add_project_and_clear_form,
            inputs=[
                scope_components['project_name'],
                scope_components['project_repo_mode'],
                scope_components['project_repo_url'], 
                scope_components['project_platform'],
                scope_components['project_repo_owner'],
                scope_components['project_repo_name'],
                scope_components['projects_data'],
                scope_components['activities_data'],
                scope_components['tasks_data']
            ],
            outputs=[
                scope_components['projects_data'],
                scope_components['projects_display'],
                scope_components['project_name'], 
                scope_components['project_repo_mode'],
                scope_components['project_repo_url'],
                scope_components['project_manual_repo_row'],
                # TODO: Check if fields are cleared
                scope_components['project_platform'],    # Clear platform field
                scope_components['project_repo_owner'],  # Clear and hide repo owner field
                scope_components['project_repo_name']    # Clear and hide repo name field
            ]
        )

        def clear_projects_and_reset_form():
            """Clear all projects and reset form with proper repository visibility"""
            projects_data, display_message = clear_projects()
            # TODO: Check returns
            return (
                projects_data,
                display_message,
                "",
                "No",
                gr.Textbox(value="", visible=False),   
                gr.Row(visible=False),
                "GitHub",
                "",
                ""
            )

        scope_components['clear_projects_btn'].click(
            fn=clear_projects_and_reset_form,
            outputs=[
                scope_components['projects_data'],
                scope_components['projects_display'],
                scope_components['project_name'],
                scope_components['project_repo_mode'],
                scope_components['project_repo_url'],
                scope_components['project_manual_repo_row'],
                # TODO: Check if needed
                scope_components['project_platform'],
                scope_components['project_repo_owner'],  
                scope_components['project_repo_name']   
            ]
        )
        
        # Show/hide repository fields based on platform selection
        scope_components['project_repo_mode'].change(
            fn=update_repo_link_visibility,
            inputs=[scope_components['project_repo_mode']],
            outputs=[
                scope_components['project_repo_url'],
                scope_components['project_manual_repo_row'],
            ]
        )
        scope_components['project_repo_url'].change(
            fn=lambda url: autofill_from_url(url)[:3], # To not overwrite project list
            inputs=[scope_components['project_repo_url']],
            outputs=[
                scope_components['project_platform'],
                scope_components['project_repo_owner'],
                scope_components['project_repo_name'],
            ]
        )
        
        # Activity management
        scope_components['add_activity_btn'].click(
            fn=add_activity,
            inputs=[
                scope_components['activity_name'],
                scope_components['activity_parent'],
                scope_components['activities_data'],
                scope_components['projects_data']
            ],
            outputs=[
                scope_components['activities_data'],
                scope_components['activities_display'],
                scope_components['activity_name'],       # Clear name field
                scope_components['activity_parent']      # Clear parent field
            ]
        )
        
        scope_components['clear_activities_btn'].click(
            fn=clear_activities,
            outputs=[
                scope_components['activities_data'],
                scope_components['activities_display']
            ]
        )
        
        # Task management
        scope_components['add_task_btn'].click(
            fn=add_task,
            inputs=[
                scope_components['task_name'],
                scope_components['task_parent'],
                scope_components['task_type'],
                scope_components['task_action'],
                scope_components['tasks_data'],
                scope_components['projects_data'],
                scope_components['activities_data']
            ],
            outputs=[
                scope_components['tasks_data'],
                scope_components['tasks_display'],
                scope_components['task_name'],           # Clear name field
                scope_components['task_parent'],         # Clear parent field
                scope_components['task_type'],           # Clear type field
                scope_components['task_action']          # Clear action field
            ]
        )
        
        scope_components['clear_tasks_btn'].click(
            fn=clear_tasks,
            outputs=[
                scope_components['tasks_data'],
                scope_components['tasks_display']
            ]
        )
        
        # Update activity parent dropdown when projects change
        scope_components['projects_data'].change(
            fn=update_activity_parent_dropdown,
            inputs=[scope_components['projects_data']],
            outputs=[scope_components['activity_parent']]
        )
        
        # Update task parent dropdown when activities change (tasks can only have activities as parents)
        scope_components['activities_data'].change(
            fn=update_task_parent_dropdown,
            inputs=[scope_components['activities_data']],
            outputs=[scope_components['task_parent']]
        )
        
        # Update task action dropdown when task type changes
        scope_components['task_type'].change(
            fn=update_task_action_dropdown,
            inputs=[scope_components['task_type']],
            outputs=[scope_components['task_action']]
        )
        # Profile management handlers
        participant_components['add_profile_btn'].click(
            fn=add_profile,
            inputs=[
                participant_components['profile_name'],
                participant_components['profile_gender'],
                participant_components['profile_race'],
                participant_components['profile_language'],
                participant_components['profiles_data']
            ],
            outputs=[
                participant_components['profiles_data'],
                participant_components['profiles_display'],
                participant_components['profile_name'],        # Clear name field
                participant_components['profile_gender'],      # Clear gender field
                participant_components['profile_race'],        # Clear race field
                participant_components['profile_language'],    # Clear language field
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
        
        # Roles management handlers
        participant_components['add_role_btn'].click(
            fn=add_role,
            inputs=[
                participant_components['role_name'],
                participant_components['role_vote_value'],
                participant_components['roles_data'],
                participant_components['individuals_data'],
                participant_components['agents_data']
            ],
            outputs=[
                participant_components['roles_data'], 
                participant_components['roles_display'], 
                participant_components['role_name'],
                participant_components['role_vote_value']
            ]
        )
        
        participant_components['clear_roles_btn'].click(
            fn=clear_all_roles,
            inputs=[],
            outputs=[
                participant_components['roles_data'], 
                participant_components['roles_display'], 
                participant_components['role_name'],
                participant_components['role_vote_value']
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
                participant_components['roles_data'],        # For global uniqueness check
                participant_components['agents_data']         # For global uniqueness check
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
                participant_components['agent_vote_value'],
                participant_components['agent_confidence'],
                participant_components['agent_autonomy_level'],
                participant_components['agent_explainability'],
                participant_components['agent_role'],
                participant_components['agents_data'],
                participant_components['roles_data'],        # For global uniqueness check
                participant_components['individuals_data']    # For global uniqueness check
            ],
            outputs=[
                participant_components['agents_data'],
                participant_components['agents_display'],
                participant_components['agent_name'],           # Clear name field
                participant_components['agent_vote_value'],     # Reset vote value to default
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
        
        # Update individual and agent dropdowns when roles data changes
        participant_components['roles_data'].change(
            fn=update_individual_dropdowns,
            inputs=[
                participant_components['roles_data'],
                participant_components['profiles_data']
            ],
            outputs=[
                participant_components['individual_profile'],
                participant_components['individual_role']
            ]
        )
        
        # Update agent role dropdown when roles data changes
        participant_components['roles_data'].change(
            fn=update_agent_role_dropdown,
            inputs=[participant_components['roles_data']],
            outputs=[participant_components['agent_role']]
        )
        
        # Update ElementList dropdowns when individuals change (for both single and phase policies)
        def update_element_list_dropdowns(individuals_data):
            """Update ElementList dropdowns when individuals change"""
            individual_names = [i['name'] for i in individuals_data] if individuals_data else []
            return (
                gr.Dropdown(choices=individual_names, value=None, interactive=True),  # decision_options_element_list
                gr.Dropdown(choices=individual_names, value=None, interactive=True)   # phase_decision_options_element_list
            )
        
        participant_components['individuals_data'].change(
            fn=update_element_list_dropdowns,
            inputs=[participant_components['individuals_data']],
            outputs=[policy_components['decision_options_element_list'], policy_components['phase_decision_options_element_list']]
        )
        
        # Update policy scope dropdown when scope definitions change
        for scope_component in [scope_components['projects_data'], scope_components['activities_data'], scope_components['tasks_data']]:
            scope_component.change(
                fn=update_scope_dropdown,
                inputs=[
                    scope_components['projects_data'],
                    scope_components['activities_data'],
                    scope_components['tasks_data']
                ],
                outputs=[policy_components['policy_scope']]
            )
        
        # Update policy participants dropdown when participant definitions change
        for participant_component in [participant_components['roles_data'], participant_components['individuals_data'], participant_components['agents_data']]:
            participant_component.change(
                fn=update_participant_dropdown,
                inputs=[
                    participant_components['roles_data'],
                    participant_components['individuals_data'],
                    participant_components['agents_data']
                ],
                outputs=[
                    policy_components['policy_participants'],
                    policy_components['veto_participants'],
                    policy_components['excluded_participants'],
                    policy_components['phase_participants'],
                    policy_components['phase_veto_participants'],
                    policy_components['phase_excluded_participants']
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
            outputs=[policy_components['decision_options'], policy_components['decision_options_element_list']]
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
                policy_components['check_ci_cd_evaluation_mode'],
                policy_components['check_ci_cd_value'],
                policy_components['label_condition_type'],
                policy_components['label_condition_operator'],
                policy_components['label_condition_labels'],
                policy_components['min_time_evaluation_mode'],
                policy_components['min_time_activity'],
                policy_components['min_time_offset_value'],
                policy_components['min_time_offset_unit']
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
                policy_components['communication_channel'],
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
                policy_components['added_conditions_list'], # Clear/keep added conditions list
                policy_components['communication_channel'] # Clear/keep communication channel
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
                policy_components['check_ci_cd_evaluation_mode'],
                policy_components['check_ci_cd_value'],
                policy_components['label_condition_type'],
                policy_components['label_condition_operator'],
                policy_components['label_condition_labels'],
                policy_components['min_time_evaluation_mode'],
                policy_components['min_time_activity'],
                policy_components['min_time_offset_value'],
                policy_components['min_time_offset_unit'],
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
                policy_components['check_ci_cd_evaluation_mode'], # reset dropdown
                policy_components['check_ci_cd_value'],         # reset checkbox
                policy_components['label_condition_type'],      # reset dropdown
                policy_components['label_condition_operator'],  # reset textbox
                policy_components['label_condition_labels'],    # reset textbox
                policy_components['min_time_evaluation_mode'],  # reset dropdown
                policy_components['min_time_activity'],         # reset dropdown
                policy_components['min_time_offset_value'],     # reset number
                policy_components['min_time_offset_unit']       # reset dropdown
            ]
        )
        
        policy_components['clear_conditions_btn'].click(
            fn=clear_conditions,
            outputs=[
                policy_components['added_conditions_list']
            ]
        )
        
        # Phase condition event handlers
        policy_components['phase_condition_type'].change(
            fn=update_phase_condition_visibility,
            inputs=[policy_components['phase_condition_type']],
            outputs=[
                policy_components['phase_veto_participants'],
                policy_components['phase_excluded_participants'],
                policy_components['phase_min_participants'],
                policy_components['phase_deadline_offset_value'],
                policy_components['phase_deadline_offset_unit'],
                policy_components['phase_deadline_date'],
                policy_components['phase_min_decision_offset_value'],
                policy_components['phase_min_decision_offset_unit'],
                policy_components['phase_min_decision_date'],
                policy_components['phase_check_ci_cd_evaluation_mode'],
                policy_components['phase_check_ci_cd_value'],
                policy_components['phase_label_condition_type'],
                policy_components['phase_label_condition_operator'],
                policy_components['phase_label_condition_labels'],
                policy_components['phase_min_time_evaluation_mode'],
                policy_components['phase_min_time_activity'],
                policy_components['phase_min_time_offset_value'],
                policy_components['phase_min_time_offset_unit']
            ]
        )
        
        policy_components['add_phase_condition_btn'].click(
            fn=add_phase_condition,
            inputs=[
                policy_components['phase_condition_type'],
                policy_components['phase_veto_participants'],
                policy_components['phase_excluded_participants'],
                policy_components['phase_min_participants'],
                policy_components['phase_deadline_offset_value'],
                policy_components['phase_deadline_offset_unit'],
                policy_components['phase_deadline_date'],
                policy_components['phase_min_decision_offset_value'],
                policy_components['phase_min_decision_offset_unit'],
                policy_components['phase_min_decision_date'],
                policy_components['phase_check_ci_cd_evaluation_mode'],
                policy_components['phase_check_ci_cd_value'],
                policy_components['phase_label_condition_type'],
                policy_components['phase_label_condition_operator'],
                policy_components['phase_label_condition_labels'],
                policy_components['phase_min_time_evaluation_mode'],
                policy_components['phase_min_time_activity'],
                policy_components['phase_min_time_offset_value'],
                policy_components['phase_min_time_offset_unit'],
                policy_components['added_phase_conditions_list']
            ],
            outputs=[
                policy_components['added_phase_conditions_list'],      # success/error message
                policy_components['phase_condition_type'],            # reset dropdown
                policy_components['phase_veto_participants'],         # reset multiselect
                policy_components['phase_excluded_participants'],     # reset multiselect
                policy_components['phase_min_participants'],          # reset number
                policy_components['phase_deadline_offset_value'],     # reset number
                policy_components['phase_deadline_offset_unit'],      # reset dropdown
                policy_components['phase_deadline_date'],             # reset textbox
                policy_components['phase_min_decision_offset_value'], # reset number
                policy_components['phase_min_decision_offset_unit'],  # reset dropdown
                policy_components['phase_min_decision_date'],         # reset textbox
                policy_components['phase_check_ci_cd_evaluation_mode'], # reset dropdown
                policy_components['phase_check_ci_cd_value'],         # reset checkbox
                policy_components['phase_label_condition_type'],      # reset dropdown
                policy_components['phase_label_condition_operator'],  # reset textbox
                policy_components['phase_label_condition_labels'],    # reset textbox
                policy_components['phase_min_time_evaluation_mode'],  # reset dropdown
                policy_components['phase_min_time_activity'],         # reset dropdown
                policy_components['phase_min_time_offset_value'],     # reset number
                policy_components['phase_min_time_offset_unit']       # reset dropdown
            ]
        )
        
        policy_components['clear_phase_conditions_btn'].click(
            fn=clear_phase_conditions,
            outputs=[
                policy_components['added_phase_conditions_list']
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
                policy_components['phase_communication_channel'],
                policy_components['added_phases_list'],
                policy_components['added_phase_conditions_list']
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
                policy_components['phase_fallback_policy'],
                policy_components['phase_communication_channel'],
                policy_components['added_phase_conditions_list']
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
        for participant_component in [participant_components['roles_data'], participant_components['individuals_data'], participant_components['agents_data']]:
            participant_component.change(
                fn=update_phase_participant_dropdown,
                inputs=[
                    participant_components['roles_data'],
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
            outputs=[policy_components['phase_decision_options'], policy_components['phase_decision_options_element_list']]
        )
        
        # Update composed policy scope dropdown when scope definitions change
        for scope_component in [scope_components['projects_data'], scope_components['activities_data'], scope_components['tasks_data']]:
            scope_component.change(
                fn=update_scope_dropdown,
                inputs=[
                    scope_components['projects_data'],
                    scope_components['activities_data'],
                    scope_components['tasks_data']
                ],
                outputs=[policy_components['composed_policy_scope']]
            )
        
        # Set up change handlers for preview updates
        preview_data_components = []
        # Scope data components (projects, activities, tasks)
        preview_data_components.extend([
            scope_components['projects_data'],
            scope_components['activities_data'],
            scope_components['tasks_data']
        ])
        # Participant components
        preview_data_components.extend([
            participant_components['profiles_data'],
            participant_components['roles_data'],
            participant_components['individuals_data'],
            participant_components['agents_data']
        ])
        # Include both single policies and composed policies data for preview
        preview_data_components.append(policy_components['policies_data'])
        preview_data_components.append(policy_components['composed_policies_data'])
        
        for component in preview_data_components:
            if hasattr(component, 'change'):
                component.change(
                    fn=update_preview,
                    inputs=preview_data_components,
                    outputs=preview_components['preview_code']
                )
        
        # Load example button
        if hasattr(self, '_create_preview_panel'):
            # This will be connected properly when we have the preview panel components
            pass
        
        # Download DSL button handler - use gr.File for download
        def download_dsl(preview_text):
            """Generate a downloadable file"""
            
            if not preview_text or preview_text.startswith("# Fill the form"):
                preview_text = "# Fill the form to generate a governance policy"
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = "governance_policy_" + timestamp + ".txt"
            
            # Write to a temporary file with the proper name
            try:
                # Get temp directory
                temp_dir = tempfile.gettempdir()
                if not temp_dir or temp_dir == '/':
                    temp_dir = '/tmp'
                
                # Create the file with the desired name
                temp_path = os.path.join(temp_dir, filename)
                with open(temp_path, 'w') as f:
                    f.write(preview_text)
                
                # Return just the file path
                return temp_path
            except Exception:
                # If file creation fails, try in current directory
                try:
                    with open(filename, 'w') as f:
                        f.write(preview_text)
                    return filename
                except:
                    return None
        
        # Wire the "Download Policy" button to download the file
        preview_components['download_btn'].click(
            fn=download_dsl,
            inputs=[preview_components['preview_code']],
            outputs=preview_components['download_file']
        )
    
    def _format_float(self, value):
        """Format a number as a FLOAT (with decimal point) for DSL compliance"""
        if value is None:
            return None
        # Convert to float and format with decimal point
        float_val = float(value)
        # If it's a whole number, add .0; otherwise keep as is
        if float_val == int(float_val):
            return f"{int(float_val)}.0"
        else:
            return str(float_val)
    
    def _parse_repo_url(self, url: str):
        """
        Parse a GitHub or GitLab URL into (platform, owner, repo_name).
        Returns (None, None, None) if the URL is not recognisable.

        Supported patterns:
            https://github.com/owner/repo
            https://github.com/owner/repo.git
            https://github.com/owner/repo/tree/main
            https://gitlab.com/owner/repo
            https://gitlab.com/group/subgroup/repo  (returns group/subgroup as owner)
        """
        url = url.strip().rstrip('/')

        github_pattern = re.compile(
            r'https?://github\.com/([^/]+)/([^/\s]+?)(?:\.git)?(?:/.*)?$'
        )
        gitlab_pattern = re.compile(
            r'https?://gitlab\.com/(.+)/([^/\s]+?)(?:\.git)?(?:/.*)?$'
        )

        m = github_pattern.match(url)
        if m:
            return "GitHub", m.group(1), m.group(2)

        m = gitlab_pattern.match(url)
        if m:
            return "GitLab", m.group(1), m.group(2)

        return None, None, None
    
    def _generate_dsl_from_form(self, *form_values):
        """Generate DSL code from form inputs"""
        # Extract form values (in the order they appear in the interface)
        (projects_data, activities_data, tasks_data, profiles_data, roles_data, individuals_data, agents_data,
        policies_data, composed_policies_data) = form_values
        
        dsl_parts = []
        
        # Use structured data directly (no need to parse text anymore)
        projects = projects_data if projects_data else []
        activities = activities_data if activities_data else []
        tasks = tasks_data if tasks_data else []
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
        
        # Generate Projects with their hierarchical structure
        if all_project_names:
            scope_parts.append("    Projects :")
        
        for project_name in all_project_names:
            # Get explicit project info if available
            explicit_project = next((p for p in projects if p['name'] == project_name), None)
            
            if explicit_project and explicit_project['platform']:
                scope_parts.append(f"        {project_name} from {explicit_project['platform']} : {explicit_project['repo']}")
            else:
                scope_parts.append(f"        {project_name}")
            
            # Find activities belonging to this project
            project_activities = [a for a in activities if a['parent'] == project_name]
            if project_activities:
                scope_parts[-1] += " {"  # Add opening brace to project
                scope_parts.append("            Activities :")
                for activity in project_activities:
                    scope_parts.append(f"                {activity['name']}")
                    
                    # Find tasks belonging to this activity
                    activity_tasks = [t for t in tasks if t['parent'] == activity['name']]
                    if activity_tasks:
                        scope_parts[-1] += " {"  # Add opening brace to activity
                        scope_parts.append("                    Tasks :")
                        for task in activity_tasks:
                            if task['type'] and task['action']:
                                scope_parts.append(f"                        {task['name']} : {task['type']} {{")
                                scope_parts.append(f"                            Action : {task['action']}")
                                scope_parts.append("                        }")
                            elif task['type']:
                                scope_parts.append(f"                        {task['name']} : {task['type']}")
                            else:
                                scope_parts.append(f"                        {task['name']}")
                    
                        scope_parts.append("                }")
            
                scope_parts.append("        }")
        
        # Generate root-level Activities (explicit + implicit from task parents)
        root_activities = [a for a in activities if not a['parent']]
        
        # Add implicit activities referenced by tasks but not explicitly defined
        for implicit_activity_name in implicit_activity_names:
            root_activities.append({'name': implicit_activity_name, 'parent': None})
        
        if root_activities:
            scope_parts.append("    Activities :")
            for activity in root_activities:
                activity_name = activity['name']
                scope_parts.append(f"        {activity_name}")
                
                # Find tasks belonging to this activity
                activity_tasks = [t for t in tasks if t['parent'] == activity_name]
                if activity_tasks:
                    scope_parts[-1] += " {"  # Add opening brace to activity
                    scope_parts.append("            Tasks :")
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
                if profile.get('language'):
                    participants_section.append(f"            language : {profile['language']}")
                participants_section.append("        }")
        
        # Add Roles section
        if roles_data:
            participants_section.append("    Roles :")
            for role in roles_data:
                line = f"        {role['name']}"
                if role.get('vote_value') is not None:
                    formatted_vote = self._format_float(role['vote_value'])
                    line += f" {{ vote value : {formatted_vote} }}"
                    participants_section.append(line + ",")
                else:
                    participants_section.append(line + ",")
        
        # Add Individuals section
        if individuals or agents:
            participants_section.append("    Individuals :")
            
            # Add regular individuals
            for individual in individuals:
                line_parts = [f"        {individual['name']}"]
                if individual.get('vote_value') is not None or individual.get('profile') or individual.get('role'):
                    line_parts[0] += " {"
                    attributes = []
                    if individual.get('vote_value') is not None:
                        formatted_vote = self._format_float(individual['vote_value'])
                        attributes.append(f"            vote value : {formatted_vote}")
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
                has_attributes = (agent.get('vote_value') is not None or 
                                agent.get('confidence') is not None or 
                                agent.get('autonomy_level') is not None or 
                                agent.get('explainability') is not None or 
                                agent.get('role'))
                if has_attributes:
                    line_parts[0] += " {"
                    attributes = []
                    if agent.get('vote_value') is not None:
                        formatted_vote = self._format_float(agent['vote_value'])
                        attributes.append(f"            vote value : {formatted_vote}")
                    if agent.get('confidence'):
                        formatted_confidence = self._format_float(agent['confidence'])
                        attributes.append(f"            confidence : {formatted_confidence}")
                    if agent.get('autonomy_level'):
                        formatted_autonomy = self._format_float(agent['autonomy_level'])
                        attributes.append(f"            autonomy level: {formatted_autonomy}")
                    if agent.get('explainability'):
                        formatted_explainability = self._format_float(agent['explainability'])
                        attributes.append(f"            explainability: {formatted_explainability}")
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
            if participants_section[-1].endswith(","):
                participants_section[-1] = participants_section[-1][:-1]
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
                # Optional communication channel (must appear immediately after participants)
                if policy.get('communication_channel'):
                    dsl_parts.append(f"    CommunicationChannel : {policy['communication_channel']}")
                
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
                        elif condition_line.startswith('CheckCiCd'):
                            # Handles CheckCiCd [evaluation]: true/false
                            condition_content = condition_line.split(':', 1)[1].strip() if ':' in condition_line else ""
                            condition_prefix = condition_line.split(':', 1)[0].strip()
                            if condition_content:
                                conditions.append(f"        {condition_prefix} : {condition_content}")
                            else:
                                conditions.append(f"        {condition_prefix}")
                        elif condition_line.startswith('MinTime'):
                            # Handles MinTime [evaluation] of [Activity/InActivity]: [offset]
                            condition_content = condition_line.split(':', 1)[1].strip() if ':' in condition_line else ""
                            condition_prefix = condition_line.split(':', 1)[0].strip()
                            if condition_content:
                                conditions.append(f"        {condition_prefix} : {condition_content}")
                            else:
                                conditions.append(f"        {condition_prefix}")
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
                            conditions.append(f"        Deadline : {', '.join(deadline_parts)}")
                    
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
                            conditions.append(f"        MinDecisionTime : {', '.join(min_decision_parts)}")
                    
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

                # Parameters (must come after conditions)
                parameters = []
                if policy_type in ["MajorityPolicy", "AbsoluteMajorityPolicy", "VotingPolicy"] and policy.get('voting_ratio'):
                    # Skip ratio if it's the default value of 0.5
                    if policy['voting_ratio'] != 0.5:
                        formatted_ratio = self._format_float(policy['voting_ratio'])
                        parameters.append(f"        ratio: {formatted_ratio}")
                
                # Add default decision for LeaderDrivenPolicy
                if policy_type == "LeaderDrivenPolicy" and policy.get('default_decision'):
                    parameters.append(f"        default: {policy['default_decision']}")
                
                # Add fallback policy for ConsensusPolicy and LazyConsensusPolicy
                if policy_type in ["ConsensusPolicy", "LazyConsensusPolicy"] and policy.get('fallback_policy'):
                    parameters.append(f"        fallback: {policy['fallback_policy']}")
                
                if parameters:
                    dsl_parts.append("    Parameters:")
                    dsl_parts.extend(parameters)
                
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
                        # Parse phase from display format: "PhaseName (PolicyType) → participants: p1, p2 [Conditions: ...]"
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
                            channel = None
                            phase_conditions = []
                            
                            # Parse the display string more carefully
                            if 'participants: ' in phase_display:
                                after_participants = phase_display.split('participants: ')[1]
                                
                                # Extract conditions if present (check for [Conditions: ...])
                                if ' [Conditions: ' in after_participants:
                                    base_part = after_participants.split(' [Conditions: ')[0]
                                    conditions_part = after_participants.split(' [Conditions: ')[1].rstrip(']')
                                    # Parse conditions: split by comma, then strip and add to list
                                    phase_conditions = [c.strip() for c in conditions_part.split(';')]
                                else:
                                    base_part = after_participants
                                
                                # Extract participants (everything before the first comma with a keyword)
                                if ', decision:' in base_part:
                                    participants_part = base_part.split(', decision:')[0]
                                elif ', ratio:' in base_part:
                                    participants_part = base_part.split(', ratio:')[0]
                                elif ', default:' in base_part:
                                    participants_part = base_part.split(', default:')[0]
                                elif ', fallback:' in base_part:
                                    participants_part = base_part.split(', fallback:')[0]
                                elif ', options:' in base_part:
                                    participants_part = base_part.split(', options:')[0]
                                else:
                                    participants_part = base_part
                            
                            # Extract parameters from the details section
                            if ', decision: ' in phase_display:
                                decision_type = phase_display.split(', decision: ')[1].split(',')[0].split(' [')[0].strip()
                            
                            if ', ratio: ' in phase_display:
                                ratio = phase_display.split(', ratio: ')[1].split(',')[0].split(' [')[0].strip()
                            
                            if ', default: ' in phase_display:
                                default_decision = phase_display.split(', default: ')[1].split(',')[0].split(' [')[0].strip()
                            
                            if ', fallback: ' in phase_display:
                                fallback_policy = phase_display.split(', fallback: ')[1].split(',')[0].split(' [')[0].strip()
                            
                            if ', options: ' in phase_display:
                                options = phase_display.split(', options: ')[1].split(' [')[0].strip()
                            if ', channel: ' in phase_display:
                                channel = phase_display.split(', channel: ')[1].split(',')[0].split(' [')[0].strip()
                            
                            # Generate DSL for this phase
                            dsl_parts.append(f"        {type_part} {name_part} {{")
                            dsl_parts.append(f"            DecisionType as {decision_type}")
                            
                            if participants_part:
                                participants_list = [p.strip() for p in participants_part.split(',')]
                                dsl_parts.append(f"            Participant list: {', '.join(participants_list)}")
                            
                            # Optional communication channel for phase
                            if channel:
                                dsl_parts.append(f"            CommunicationChannel : {channel}")
                            
                            # Add conditions if present
                            if phase_conditions:
                                dsl_parts.append("            Conditions:")
                                for condition in phase_conditions:
                                    # Convert from display format to DSL format
                                    if condition.startswith('VetoRight:'):
                                        dsl_parts.append(f"                {condition.replace(':', ' :')}")
                                    elif condition.startswith('ParticipantExclusion:'):
                                        dsl_parts.append(f"                {condition.replace(':', ' :')}")
                                    elif condition.startswith('MinParticipants:'):
                                        dsl_parts.append(f"                {condition.replace(':', ' :')}")
                                    elif condition.startswith('Deadline:'):
                                        condition_content = condition.split(':', 1)[1].strip()
                                        dsl_parts.append(f"                Deadline : {condition_content}")
                                    elif condition.startswith('MinDecisionTime:'):
                                        condition_content = condition.split(':', 1)[1].strip()
                                        dsl_parts.append(f"                MinDecisionTime : {condition_content}")
                                    elif condition.startswith('CheckCiCd'):
                                        # Handles CheckCiCd [evaluation]: true/false
                                        condition_content = condition.split(':', 1)[1].strip() if ':' in condition else ""
                                        condition_prefix = condition.split(':', 1)[0].strip()
                                        if condition_content:
                                            dsl_parts.append(f"                {condition_prefix} : {condition_content}")
                                        else:
                                            dsl_parts.append(f"                {condition_prefix}")
                                    elif condition.startswith('MinTime'):
                                        # Handles MinTime [evaluation] of [Activity/InActivity]: [offset]
                                        condition_content = condition.split(':', 1)[1].strip() if ':' in condition else ""
                                        condition_prefix = condition.split(':', 1)[0].strip()
                                        if condition_content:
                                            dsl_parts.append(f"                {condition_prefix} : {condition_content}")
                                        else:
                                            dsl_parts.append(f"                {condition_prefix}")
                                    elif condition.startswith('LabelCondition'):
                                        # Parse LabelCondition format: "LabelCondition pre not : label1, label2"
                                        condition_content = condition.split(':', 1)[1].strip() if ':' in condition else ""
                                        condition_prefix = condition.split(':')[0].strip()
                                        if condition_content:
                                            dsl_parts.append(f"                {condition_prefix} : {condition_content}")
                                        else:
                                            dsl_parts.append(f"                {condition_prefix}")
                            
                            # Add parameters section if any parameters exist
                            parameters = []
                            if ratio:
                                # Skip ratio if it's the default value of 0.5
                                if ratio != 0.5:
                                    formatted_ratio = self._format_float(ratio)
                                    parameters.append(f"                ratio: {formatted_ratio}")
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
            
            # Always show vote value
            vote_value = individual.get('vote_value')
            if vote_value is None:
                vote_value = 1.0  # Show default if not set
            attributes.append(f"🗳️ vote: {vote_value}")
            
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
            
            # Always show vote value
            vote_value = agent.get('vote_value')
            if vote_value is None:
                vote_value = 1.0  # Show default if not set
            attributes.append(f"🗳️ vote: {vote_value}")
            
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
            if profile.get('language'):
                attributes.append(f"🌐 language: {profile['language']}")
            
            if attributes:
                line += f" → {', '.join(attributes)}"
            
            display_lines.append(line)
        
        return '\n'.join(display_lines)

    def _format_roles_display(self, roles):
        """Format roles for display in the text area"""
        if not roles:
            return "No roles added yet. Create roles to define project responsibilities."
        
        display_lines = [f"👥 {len(roles)} role(s) defined:", ""]
        for i, role in enumerate(roles, 1):
            vote_value = role.get('vote_value')
            if vote_value is None:
                vote_value = 1.0  # Show default if not set
            line = f"{i}. 🔹 **{role['name']}** (vote value: {vote_value})"
            display_lines.append(line)
        
        return '\n'.join(display_lines)

    def _format_projects_display(self, projects):
        """Format projects for display in the text area"""
        if not projects:
            return "No projects added yet. Create projects to define your organizational structure."
        
        display_lines = [f"🏗️ {len(projects)} project(s) defined:", ""]
        for i, project in enumerate(projects, 1):
            line = f"{i}. {project['name']}"
            details = []
            if project.get('platform'):
                details.append(f"📦 platform: {project['platform']}")
            if project.get('repo'):
                details.append(f"📂 repo: {project['repo']}")
            
            if details:
                line += f" → {', '.join(details)}"
            
            display_lines.append(line)
        
        return '\n'.join(display_lines)
    
    def _format_activities_display(self, activities):
        """Format activities for display in the text area"""
        if not activities:
            return "No activities added yet. Create activities to organize your project workflow."
        
        display_lines = [f"⚡ {len(activities)} activit(ies) defined:", ""]
        for i, activity in enumerate(activities, 1):
            line = f"{i}. {activity['name']}"
            if activity.get('parent'):
                line += f" → 📋 parent: {activity['parent']}"
            
            display_lines.append(line)
        
        return '\n'.join(display_lines)
    
    def _format_tasks_display(self, tasks):
        """Format tasks for display in the text area"""
        if not tasks:
            return "No tasks added yet. Create tasks to define specific governance actions."
        
        display_lines = [f"✅ {len(tasks)} task(s) defined:", ""]
        for i, task in enumerate(tasks, 1):
            line = f"{i}. {task['name']}"
            details = []
            if task.get('parent'):
                details.append(f"📋 parent: {task['parent']}")
            if task.get('type'):
                details.append(f"🏷️ type: {task['type']}")
            if task.get('action'):
                details.append(f"⚙️ action: {task['action']}")
            
            if details:
                line += f" → {', '.join(details)}"
            
            display_lines.append(line)
        
        return '\n'.join(display_lines)
    
    def _extract_scope_names(self, projects_data, activities_data, tasks_data):
        """Extract all scope names (projects, activities, tasks) for dropdown choices"""
        scope_names = []
        
        # Extract project names
        for project in projects_data if projects_data else []:
            if project.get('name'):
                scope_names.append(project['name'])
        
        # Extract activity names
        for activity in activities_data if activities_data else []:
            if activity.get('name'):
                scope_names.append(activity['name'])
        
        # Extract task names
        for task in tasks_data if tasks_data else []:
            if task.get('name'):
                scope_names.append(task['name'])
        
        return sorted(list(set(scope_names)))  # Remove duplicates and sort
    
    def _extract_participant_names(self, roles_data, individuals_data, agents_data):
        """Extract all participant names (roles, individuals, agents) for dropdown choices"""
        participant_names = []
        
        # Extract role names
        if roles_data:
            participant_names.extend([role['name'] for role in roles_data])
        
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
                # Skip displaying ratio if it's the default value of 0.5
                if policy['voting_ratio'] != 0.5:
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
    app = builder.create_interface()
    
    return app

if __name__ == "__main__":
    app = main()
    app.launch(
        server_name="localhost",
        server_port=7860,
        share=False,
        debug=True
    )