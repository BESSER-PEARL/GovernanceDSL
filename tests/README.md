# Tests

This folder contains unit tests and test cases for validating the Governance DSL parser and model creation.

## Run the tests

From the repository root:

```bash
python -m unittest tests.test_policy_creation -v
```

Run all discovered tests under this folder:

```bash
python -m unittest discover tests -v
```

## Folder overview

- `test_policy_creation.py`: Main unit test module. It parses DSL inputs and checks valid model creation as well as expected errors for invalid inputs.
- `test_cases/`: Input files used by the tests.
- `test_cases/valid_examples/`: DSL examples that should parse and build valid governance models.
- `test_cases/invalid_examples/`: DSL examples that should fail and raise specific exceptions.
- `test_cases/NL_examples/`: Natural-language governance examples (artificial and real-world) used as reference material and additional examples.
