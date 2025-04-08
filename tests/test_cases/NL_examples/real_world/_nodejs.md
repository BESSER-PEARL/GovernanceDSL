**Original repo**: https://github.com/nodejs/node

**Access date**: 25/03/2025 08:25h

**Further info**: 
    - They have a [governance.md file](https://github.com/nodejs/node/blob/main/GOVERNANCE.md)
    - Roles: Triagers, Collaborators, Technical Steering Commitee
        - Triagers in charge of assessing newly-opened issues and PRs.
        - Collaborators are contributors to the project.
        - TSC: Subset of collaborators (like an inner circle)
    - [TSC Charter](https://github.com/nodejs/TSC/blob/dc5595efcf09ceddb5cff01dce1518951f85df33/TSC-Charter.md): How TSC works.
        - For internal project decisions, Collaborators shall operate under Lazy Consensus. 
        - The TSC voting members shall establish appropriate guidelines for implementing Lazy Consensus (e.g. expected notification and review time periods) within the development process.
        - Adem: Not much details, but they use Lazy Consensus. To be considered under the Consensus hierarchy.

**Reporter**: Adem

**Policy**: 
  - PR merge: (Implemented: [nodejs_pr_merge.txt](../../valid_examples/real_world/nodejs_pr_merge.txt))
        - Two collaborators must approve a pull request before the pull request can land. (Rule)
        - (One collaborator approval is enough if the pull request has been open for more than 7 days.) (Rule)
        - ~~Approving a pull request indicates that the collaborator accepts responsibility for the change.~~ (Irrelevant)
        - Approval must be from collaborators who are not authors of the change.(Rule condition: PartExclusion)
        - If a collaborator opposes a proposed change, then the change cannot land. (ratio 100%? We could have also a Lazy Consensus in Voting Policies?)
        - The exception is if the TSC votes to approve the change despite the opposition. (Votes of TSC overcome ratio != 100%; could be a new phase)
        - ~~Usually, involving the TSC is unnecessary.~~ (Irrelevant)
        - ~~Often, discussions or further changes result in collaborators removing their opposition.~~ (Irrelevant)
    - Collaborator:
        - A collaborator is automatically made emeritus (and removed from active collaborator status) if it has been more than 12 months since the collaborator has authored or approved a commit that has landed. (I don't see it as a rule)
    - TSC:
        - If consensus-seeking fails for an issue, a collaborator may apply the tsc-agenda label. That will add it to the TSC meeting agenda. (Should we cover this kind of rules?)
    - Collaborator nomination:
        - The nomination passes if no collaborators oppose it (as described in the following section) after one week. (Rule: Lazy Voting?)
        - In the case of an objection, the TSC is responsible for working with the individuals involved and finding a resolution. (Ad-Hoc resolution?)
