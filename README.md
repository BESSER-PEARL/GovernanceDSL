# A DSL to define and enforce governance policies

This repository contains the definition of a domain-specific language (DSL) for governance policies (the engine for the enforcement of the policies is available [here](https://github.com/BESSER-PEARL/GovernanceDecisionEngine)).

## Contents

The repository structure is divided in four folders:
* `grammar/`: This folder contains the definition of the grammar, or concrete syntax, of our DSL. We used [ANTLR](https://www.antlr.org/) to define our concrete syntax, see [`govdsl.g4`](grammar/govdsl.g4) for the implementation.
* `metamodel/`: This folder contains the metamodel of the abstract syntax of our DSL. Since the metamodel has been created using the [BESSER Web Modeling Editor](https://editor.besser-pearl.org/) we provide several files:
    - [`metamodel.json`](metamodel/governance.py): The JSON representation that can be used to open the metamodel in the editor.
    - [`metamodel.png`](metamodel/metamodel.png): A PNG image of the metamodel.
    - [`metamodel.py`](metamodel/governance.py): The implementation of the classes of the metamodel as Python classes.
* `tests/`: This folder contains the tests. There are three subfolders for the examples:
    - `invalid_examples`: Here we define with our DSL different invalid policies (e.g., the required number of votes is negative).
    - `NL_examples`: Here we define the examples in natural language, which can come from existing repositories (`NL_examples/real-world/` folder) or created from us (`NL_examples/artifical/`).
    - `valid_examples`: Here we define with our DSL different valid policies, which can come from `NL_examples/`.
* `utils/`: This folder contains additional support for the definitions of exceptions, extensions of our metamodel (e.g., GitHub), and data structure support for the parser.

## Tests

When contributing to incorporate new tests in natural language (`NL_examples/`) we recommend using the following template:

```
Original repo: URL (or we can also report "owner/name" if repository is from GitHub)
Access date: Date you accessed the repository
Reporter: Jordi/Javi
Policy: If multiple, enter a new line for each.
```
