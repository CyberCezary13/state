# Repository State Repo

This repository contains the current state and history for the Arch Linux package repos, so whenever a package is updated, moved, uploaded or removed the change will be recorded in this repository.

## Repository Structure

The repository is organized into directories by repository name and architecture:

- `core-any`, `core-x86_64` - Core packages (architecture-independent and x86_64)
- `core-testing-any`, `core-testing-x86_64` - Core testing packages
- `extra-any`, `extra-x86_64` - Extra packages
- `extra-testing-any`, `extra-testing-x86_64` - Extra testing packages
- `extra-staging-any`, `extra-staging-x86_64` - Extra staging packages
- `multilib-x86_64` - Multilib packages
- `multilib-testing-x86_64`, `multilib-staging-x86_64` - Multilib testing and staging
- `gnome-unstable-any`, `gnome-unstable-x86_64` - GNOME unstable packages
- `kde-unstable-any`, `kde-unstable-x86_64` - KDE unstable packages

Each package file contains a single line with the format:
```
package-name version1 version2 commit-hash
```

## Query Tool

A Python utility script `query_packages.py` is provided to query package information:

### Usage Examples

**Search for a package across all repositories:**
```bash
./query_packages.py search python
```

**List all repositories:**
```bash
./query_packages.py repos
```

**List packages in a specific repository:**
```bash
./query_packages.py list --repo core-x86_64
```

**Get detailed information about a specific package:**
```bash
./query_packages.py info python core-x86_64
```

### Requirements

Python 3.6 or higher is required to run the query tool.

## License

The contents of this repository are considered trivial and therefore not subject to a license.

## Logo

The Logo uses the <a href="https://www.flaticon.com/free-icons/ssd" title="ssd icons">Ssd icons created by Freepik - Flaticon</a> and was created by members of the Arch Linux project.
