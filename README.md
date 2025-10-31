# A DSL to define and enforce governance policies

This repository contains the definition of a domain-specific language (DSL) for governance policies (the engine for the enforcement of the policies is available [here](https://github.com/BESSER-PEARL/GovernanceDecisionEngine)).
We provide details below for the contents of this repository.
The DSL provides a form-based editor, available [here](https://besser-pearl.github.io/GovernanceDSL/).

## Contents

The repository structure is divided in five folders:
* `grammar/`: This folder contains the definition of the grammar, or concrete syntax, of our DSL. We used [ANTLR](https://www.antlr.org/) to define our concrete syntax, see [`govdsl.g4`](grammar/govdsl.g4) for the implementation.
* `metamodel/`: This folder contains the metamodel of the abstract syntax of our DSL:
    - [`metamodel.py`](metamodel/governance.py): The implementation of the abstract syntax metamodel as Python classes.
    - [ocl_constraints.ocl](metamodel/ocl_constraints.ocl): Set of OCL constraints applied to the metamodel (OCL constraints are also included in the BESSER diagrams).
    - Since the metamodel has been created using the [BESSER Web Modeling Editor](https://editor.besser-pearl.org/) we provide several files under `metamodel/besser_models/` folder:
        - `.json` files: The JSON representation that can be used to open the metamodel in the editor.
        - `.svg` and `.png` files: The SVG and PNG representation for visual purposes.
        - `.drawio.png` files: We also provide the metamodel embedded in a PNG file that can be opened in the [draw.io](https://app.diagrams.net/?src=about) editor.
* `UI/`: This folder contains a Gradio-based form editor for creating governance policies interactively:
    - See [`UI/README.md`](UI/README.md) for detailed information.
    - The form-based editor is available [here](https://besser-pearl.github.io/GovernanceDSL/).
* `tests/`: This folder contains the tests. There are three subfolders inside the `test_cases/` for the examples:
    - `invalid_examples/`: Here we define with our DSL different invalid policies (e.g., the required number of votes is negative).
    - `NL_examples`: Here we define the examples in natural language, which can come from existing repositories (`NL_examples/real-world/` folder) or created from us (`NL_examples/artifical/`).
    - `valid_examples`: Here we define with our DSL different valid policies, which can also come from `NL_examples/`.
* `utils/`: This folder contains additional support for the definitions of exceptions, extensions of our metamodel (e.g., code-hosting platform extension), and data structure support for the parser.

## Tests

When contributing to incorporate new tests in natural language (`NL_examples/`) we recommend using the following template:

```
Original repo: URL (or we can also report "owner/name" if repository is from GitHub)
Access date: Date you accessed the repository
Reporter: -
Policy: If multiple, enter a new line for each.
```

### Prerequisite
- Python 3.11
- Recommended: Create a virtual environment
  (e.g. [venv](https://docs.python.org/3/library/venv.html),
  [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html))
- Clone this repository
- Install the dependencies by referencing to the requirements files:

```bash
pip install -r requirements.txt
```

### Run Tests

From the project root directory, run all tests with:

```bash
python -m unittest tests.test_policy_creation -v
```

Or run a specific test:

```bash
python -m unittest tests.test_policy_creation.testPolicyCreation.test_majority_policy_creation -v
```

**Note:** Make sure you're in the project root directory when running the tests to ensure proper module imports.