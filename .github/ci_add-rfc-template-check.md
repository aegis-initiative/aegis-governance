## Description

Add a CI workflow and Python script to enforce RFC template compliance for all RFC markdown files. This ensures all RFCs contain required metadata and section headers as defined in RFC-0000-TEMPLATE.md.

## Motivation

Automates enforcement of documentation standards for RFCs, improving consistency and reducing manual review effort. Helps contributors and reviewers catch missing or misordered sections early.

## Type of Change

- [x] CI/CD workflow update
- [x] Documentation tooling
- [ ] Documentation update
- [ ] RFC specification change
- [ ] Protocol or schema update
- [ ] Reference implementation change
- [ ] Bug fix
- [ ] New feature

## Related Issues

<!-- No related issues directly, but aligns with documentation quality and automation goals. -->

## Changes Made

- Added .github/scripts/check_rfc_template.py to check RFCs for required headers/sections
- Added .github/workflows/rfc-template-check.yml to run the check on PRs and pushes

## Testing

- [x] CI workflow runs on PR and push
- [x] Fails if any RFC is missing required fields/sections
- [x] Manual test with RFCs missing headers/sections

## Documentation Updates

- [x] Developer documentation/tooling updated
- [ ] README updated (if needed)
- [ ] RFC documentation updated (if applicable)
- [ ] Code comments added/updated
- [ ] CHANGELOG updated (for runtime changes)
- [ ] Specification version numbers updated (if applicable)

## Specification Impact

- [x] No specification version impact

## Security Considerations

- [x] No security impact

## Breaking Changes

- [x] No breaking changes

<details>
<summary>Migration Guide (if applicable)</summary>

<!-- No migration needed. -->

</details>

## Reviewers & Collaborators

<!-- Tag relevant reviewers or contributors -->

## Checklist

- [x] Branch follows naming convention (`ci/add-rfc-template-check`)
- [x] Commits follow Conventional Commits format
- [x] All conversations resolved
- [x] Self-review completed
- [x] PR is ready for review
