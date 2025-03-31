**Original repo**: https://github.com/microsoft/vscode

**Access date**: 26/03/2025 09:42h

**Reporter**: Adem

**Further info**: There is no info explicit, but in [contributing.md](https://github.com/microsoft/vscode/blob/main/CONTRIBUTING.md) file, they share how they automatically close issues (via GHActions), and how they address a feature request.

**Policy**: 

Automatically **closing issues**:
- Automatically close any issue marked info-needed if there has been no response in the past 7 days.
- Automatically lock issues 45 days after they are closed.

**Feature request** pipeline (they have a diagram for that):

* To put the diagram in words:
        
    1. Does the proposal match with our general product direction? For example, VS Code is a light-weight extensible text editor and as such we are not interested in turning it into a platform to implement a web browser.

    If the answer is no we close the issue as out-of-scope.

    2. Can our team afford to implement the feature? I.e. are the direct and the opportunity costs to implement the functionality and maintain it going forward reasonable compared to the size of our team?

    If the answer is no we close the issue as out-of-scope.

    3. Does the functionality described in the feature request have any reasonable chance to be implemented in the next 24 months? 24 months is longer than our roadmap which outlines the next 6-12 months. Thus, there is some crystal ball reading on our part, and we'll most likely keep more feature requests open than what we can accomplish in 24 months.

    If the answer is yes we assign the issue to the Backlog milestone.

    4. Do we think the feature request is bold and forward looking and would we like to see it be tackled at some point even if it's further out than 24 months? (Clearly, this is quite subjective.)

    If the answer is yes we assign the issue to the Backlog milestone.

    5. Has the community at large expressed interest in this functionality? I.e. has it gathered more than 20 up-votes.

    If the answer is yes we assign the issue to the Backlog otherwise the Backlog Candidates milestone.

    A bot monitors the issues assigned to Backlog Candidates. If a feature request surpasses the 20 up-votes, the bot removes the Backlog Candidates milestone and adds the Backlog milestone. If an issue is assigned to the Backlog Candidates milestone for more than 60 days, the bot will close the issue.

Diagram image: https://github.com/microsoft/vscode/wiki/Issues-Triaging#managing-feature-requests

Similarly, they have a workflow for **issue triaging**:

![image from: https://github.com/microsoft/vscode/wiki/Issues-Triaging#our-triaging-flow](67361378-4f038c00-f51d-11e9-981e-f0b6964f27ce.png)