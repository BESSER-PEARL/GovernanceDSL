**Original repo**: https://github.com/mui/material-ui

**Access date**: 25/03/2025 13:01h

**Reporter**: Adem

**Further info**: Governance on how they merge the PRs can be found in [contributing.md#how-to-increase-the-chances-of-being-accepted](https://github.com/mui/material-ui/blob/master/CONTRIBUTING.md#how-to-increase-the-chances-of-being-accepted).
I don't know how we could cover this, there is no decision-making but more of a conditions checklist. 

**Policy**: 

We will only merge a PR when all tests pass.
The following statements must be true:

- The code is formatted. If the code was changed, run `pnpm prettier`.
- The code is linted. If the code was changed, run `pnpm eslint`.
- The code is type-safe. If TypeScript sources or declarations were changed, run `pnpm typescript` to confirm that the check passes.
- The API docs are up to date. If API was changed, run `pnpm proptypes && pnpm docs:api`.
- The demos are up to date. If demos were changed, run `pnpm docs:typescript:formatted`. See [about writing demos](#2-write-the-demo-code).
- The pull request title follows the pattern `[product-name][Component] Imperative commit message`. (See: [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/) for a great explanation).
