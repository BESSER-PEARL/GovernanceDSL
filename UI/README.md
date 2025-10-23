# Governance DSL Form Builder

A Gradio-based web interface for creating and editing governance policies using an intuitive form-based editor.

## Overview

The Form Builder provides a user-friendly way to define governance policies without writing DSL code directly. It includes:

- **Scope Tab**: Create projects, activities, and tasks.
- **Participant Tab**: Define profiles, roles, individuals, and agents.
- **Policy Tab**: Set up single or composed governance policies.
- **Live Preview**: View generated DSL code in real-time.
- **Download**: Export your governance policy as a text file, or just copy it from the live preview!

## Running Locally

To test the form builder locally run inside this folder:

```bash
pip install -r requirements.txt
python run_ui.py
```

This will start a local Gradio server at `http://localhost:7860`

## Online Version

The form builder is also available online (hosted on GitHub Pages using [Gradio Lite](https://www.gradio.app/4.44.1/guides/gradio-lite)):

**[Governance DSL Form Builder - Online](https://besser-pearl.github.io/GovernanceDSL/)**

The online version runs entirely in your browser using WebAssembly (Pyodide), with no backend server required.

## Usage

1. Fill out the form sections for your governance structure.
2. Watch the DSL code generate in the Live Preview panel.
3. Download your policy using the "✅ Prepare Policy for Download" button.
4. You can then use the generated `.txt` in the [Decision Engine](github.com/BESSER-PEARL/GovernanceDecisionEngine).

## File Structure

- `governance_form_builder.py` - Main form builder class
- `run_ui.py` - Local server launcher
- `requirements.txt` - Python dependencies
