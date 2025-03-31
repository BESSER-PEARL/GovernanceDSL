**Original repo**: https://github.com/flutter/flutter

**Access date**: 26/03/2025 09:57h

**Reporter**: Adem

**Further info**: They have a [contributing.md](https://github.com/flutter/flutter/blob/master/CONTRIBUTING.md) file, where they have a section for "[Developing for Flutter](https://github.com/flutter/flutter/blob/master/CONTRIBUTING.md#developing-for-flutter)". In here they redirect to their docs, where we can find the [Tree-hygiene.md](https://github.com/flutter/flutter/blob/master/docs/contributing/Tree-hygiene.md). This page covers how to land a PR and other aspects of writing code for Flutter. In the [Overview](https://github.com/flutter/flutter/blob/master/docs/contributing/Tree-hygiene.md#overview) section of this file, points 7-9 say:

7. Get your code reviewed. You should probably reach out to the relevant expert(s) for the areas you touched and ask them to review your PR directly. GitHub sometimes recommends specific reviewers; if you're not sure who to ask, that's probably a good place to start.

8. Make sure your PR passes all the pre-commit tests. [...]

9. Once everything is green and you have an LGTM from the owners of the code you are affecting (or someone to whom they have delegated), and an LGTM from any other contributor who left comments, add the "autosubmit" label if you're in the flutter-hackers github group. A bot will land the patch when it feels like it. If you're not in the flutter-hackers group a reviewer will add the label for you.

They have further docs on [Getting a code review](https://github.com/flutter/flutter/blob/master/docs/contributing/Tree-hygiene.md#getting-a-code-review). 
However, here they do not mention how they are closing the PR (other than the above mentioned points 8 and 9).
Further info that might be valuable for the definition of the policy could be the following statement: "*Once you are satisfied with the contribution, and only once you are satisfied, use the GitHub "Approval" mechanism (an "LGTM" comment is not sufficient).*"

**Policy**: 

Landing PRs:
1. Get your code reviewed. You should probably reach out to the relevant expert(s) for the areas you touched and ask them to review your PR directly. GitHub sometimes recommends specific reviewers; if you're not sure who to ask, that's probably a good place to start.

2. Make sure your PR passes all the pre-commit tests. [...]

3. Once everything is green and you have an LGTM from the owners of the code you are affecting (or someone to whom they have delegated), and an LGTM from any other contributor who left comments, add the "autosubmit" label if you're in the flutter-hackers github group. A bot will land the patch when it feels like it. If you're not in the flutter-hackers group a reviewer will add the label for you.