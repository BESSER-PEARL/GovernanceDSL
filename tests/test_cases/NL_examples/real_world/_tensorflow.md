**Original repo**: https://github.com/tensorflow/tensorflow

**Access date**: 08/04/2025

**Reporter**: Adem

**Further info**: Guideline in [contributing.md](https://github.com/tensorflow/tensorflow/blob/master/CONTRIBUTING.md). They showcase the [typical PR flow](https://github.com/tensorflow/tensorflow/blob/master/CONTRIBUTING.md#typical-pull-request-workflow--), also visual in: ![graphic flow](https://user-images.githubusercontent.com/42785357/187579207-9924eb32-da31-47bb-99f9-d8bf1aa238ad.png)

**Policy**: 

PR landing:
1. New PR:
    * Conditions (quality checks): CLA is signed, PR has sufficient description, if applicable unit tests are added, if it is a reasonable contribution (meaning it is not a single liner cosmetic PR).
        * <ins>*How should we implement this? Is it a bit too fine-grained, right?*</ins>
    * Participants: They only say "we". It is different from reviewer role (see below), i guess. 
2. Valid?
    * If so: Assign reviewer
    * If not: Request for changes (send it back or on a rare occasion we may reject it)
3. Review:
    * Reviewer puts LGTM (PR approved) or need additional changes (PR requested to make the suggested change(s))
    * This cycle repeats itself until the PR gets approved:
        * Note: As a friendly reminder, we may reach out to you if the PR is awaiting your response for more than 2 weeks. (<ins>*But, is this a deadline? I don't think so, feels more like a reminder*</ins>)
4. Approved:
    * Gets labeled with `kokoro:force-run` and initiated CI/CD.
    * Can't move forward if tests fail:
        * Requests for changes
    * If pass, code moved to internal code base with a job (capybara)
5. Copy to Google Internal codebase and run internal CI:
    * Apply internal tests for integration with dependencies and the rest of the system.
    * If needed, asked the PR author.
    * If passed, PR merged both internally and externally (GH).