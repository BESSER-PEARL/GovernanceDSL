**Original repo**: https://github.com/golang/go

**Access date**: 26/03/2025 9:33h

**Reporter**: Adem

**Further info**: Info about voting conventions (along with contribution details) can be found in their [docs](https://go.dev/doc/contribute). They have a section for [Voting Conventions](https://go.dev/doc/contribute#votes), there they say that votes can be +1, or +2:
    - +2: The change is approved for being merged. Only Go maintainers (also referred to as “approvers”) can cast a +2 vote.
    - +1: The change looks good, but either the reviewer is requesting minor changes before approving it, or they are not a maintainer and cannot approve it, but would like to encourage an approval.

**Policy**:

- To be submitted, a change must have a Code-Review +2 from a maintainer. 
- Maintainers can also apply a Hold +1 vote to the change, to mark a change that should not be submitted now.
- To be submitted, a change must not have any Hold +1 votes from a maintainer. (<ins>*This would be veto right, right?*</ins>)
- Finally, to be submitted, a change must have the involvement of two Google employees, either as the uploader of the change or as a reviewer voting at least Code-Review +1. This requirement is for compliance and supply chain security reasons. 