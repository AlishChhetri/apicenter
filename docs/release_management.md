# Release Management Guide

This guide provides detailed information about the release process for APICenter.

## Table of Contents

- [Release Process Overview](#release-process-overview)
- [Versioning Strategy](#versioning-strategy)
- [GitHub Releases](#github-releases)
- [Release Checklist](#release-checklist)
- [Troubleshooting](#troubleshooting)

## Release Process Overview

APICenter uses an automated release process triggered by Git tags. When a tag matching the pattern `v*` (e.g., `v1.0.0`) is pushed to the repository, GitHub Actions automatically:

1. Builds the Python package
2. Creates a GitHub Release with release notes and distributable artifacts

This process is handled by the `.github/workflows/publish.yml` workflow.

## Versioning Strategy

APICenter follows [Semantic Versioning](https://semver.org/) (SemVer):

- **MAJOR version**: Incompatible API changes
- **MINOR version**: Backwards-compatible functionality
- **PATCH version**: Backwards-compatible bug fixes

### Pre-release Versions

Pre-release versions are supported with the following format:
- `v1.0.0-alpha1` for alpha releases
- `v1.0.0-beta2` for beta releases
- `v1.0.0-rc1` for release candidates

## GitHub Releases

The release workflow automatically creates GitHub Releases when a new tag is pushed. These releases:

- Include the built distribution packages (wheel and source)
- Have automatically generated release notes from commit messages
- Are marked as pre-releases if the tag contains `alpha`, `beta`, or `rc`

## Release Checklist

Before creating a release:

- [ ] Ensure all tests pass
- [ ] Update documentation to reflect any changes
- [ ] Update CHANGELOG.md with notable changes
- [ ] Verify the package builds correctly locally (`poetry build`)
- [ ] Check the package metadata is correct (`poetry check`)
- [ ] Determine the appropriate version number based on changes

## Creating a Release

```bash
# Update main branch
git checkout main
git pull origin main

# Determine version number (e.g., 1.0.0)
VERSION=1.0.0

# Create and push tag
git tag v$VERSION
git push origin v$VERSION

# For pre-releases
# git tag v$VERSION-beta1
# git push origin v$VERSION-beta1
```

## Troubleshooting

### Common Issues

#### Build Failures
- Ensure all dependencies are correctly specified
- Check that the package structure is valid

#### GitHub Release Failures
- Verify the GitHub Action has proper permissions (needs `contents: write`)
- Check for issues with tag format

### Getting Help

If you encounter issues not covered here:
1. Check GitHub Actions logs for detailed error messages
2. Contact the maintainers for assistance 