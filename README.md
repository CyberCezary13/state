# Repository State Repo

This repository contains the current state and history for the Arch Linux package repos, so whenever a package is updated, moved, uploaded or removed the change will be recorded in this repository.

## Performance Optimization

This repository has been optimized for better performance by consolidating package state files:

- **Original format**: 12,678 individual files (one per package)
- **Optimized format**: 17 consolidated text files (one per repository)
- **Performance improvement**: 99.87% reduction in file count, significantly faster Git operations

### Using the Optimized Format

The repository now provides consolidated `.txt` files for each package repository:

```bash
# Search for a package
grep '^firefox' extra-x86_64.txt

# List all packages in a repository
cat extra-x86_64.txt | grep -v '^#'

# Count packages
wc -l extra-x86_64.txt
```

### Query Helper Script

Use the provided query script for convenient access:

```bash
# List all repositories
python3 query_repository.py repos

# Search for a package
python3 query_repository.py search firefox

# List packages in a repository
python3 query_repository.py list extra-x86_64
```

### File Format

Each consolidated file contains one package per line:
```
package-name version1 version2 commit-hash
```

For detailed information about the optimization, see [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md).

## License

The contents of this repository are considered trivial and therefore not subject to a license.

## Logo

The Logo uses the <a href="https://www.flaticon.com/free-icons/ssd" title="ssd icons">Ssd icons created by Freepik - Flaticon</a> and was created by members of the Arch Linux project.
