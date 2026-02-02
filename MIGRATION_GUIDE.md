# Migration Guide

This guide helps you transition from the original directory-based format to the optimized consolidated format.

## Quick Start

### Option 1: Use Both Formats (Current State)
The repository currently includes both formats:
- Original: `core-any/`, `extra-x86_64/`, etc. directories
- Consolidated: `core-any.txt`, `extra-x86_64.txt`, etc. files

You can use whichever format suits your needs.

### Option 2: Fully Migrate to Consolidated Format
Follow these steps to use only the consolidated format.

## Migration Steps

### Step 1: Validate Consolidated Files

First, verify that all data has been properly consolidated:

```bash
# Count original files
find . -type f ! -path "./.git/*" -name "[!.]*" | \
  grep -v "\.txt$" | grep -v "\.py$" | grep -v "\.md$" | wc -l

# Count packages in consolidated files
cat *.txt | grep -v '^#' | wc -l

# They should match (12,678 packages)
```

### Step 2: Test Your Tools

If you have scripts or tools that use the repository:

```bash
# Original format access
cat core-any/automake

# Consolidated format equivalent
grep '^automake ' core-any.txt
```

Update your scripts to use the new format:

```bash
# Old: Find package
old_value=$(cat extra-x86_64/firefox)

# New: Find package
new_value=$(grep '^firefox ' extra-x86_64.txt)
```

### Step 3: Update Scripts

Example script migration:

**Before:**
```bash
#!/bin/bash
# List all packages in a repository
for file in extra-x86_64/*; do
    echo $(basename "$file")
done
```

**After:**
```bash
#!/bin/bash
# List all packages in a repository
grep -v '^#' extra-x86_64.txt | cut -d' ' -f1
```

Or use the provided query script:
```bash
python3 query_repository.py list extra-x86_64
```

### Step 4: Remove Original Directories

**WARNING**: Only do this after validating everything works!

```bash
# Backup first (optional)
tar -czf original-format-backup.tar.gz core-* extra-* multilib-* gnome-* kde-*

# Remove original directories
rm -rf core-any core-testing-any core-testing-x86_64 core-x86_64 \
       extra-any extra-staging-any extra-staging-x86_64 \
       extra-testing-any extra-testing-x86_64 extra-x86_64 \
       gnome-unstable-any gnome-unstable-x86_64 \
       kde-unstable-any kde-unstable-x86_64 \
       multilib-staging-x86_64 multilib-testing-x86_64 multilib-x86_64

# Commit the change
git add -A
git commit -m "Remove original directory structure, use consolidated format only"
git push
```

### Step 5: Update Documentation

Update any documentation or tools that reference the old format.

## Common Migration Patterns

### Pattern 1: Reading a Single Package

**Before:**
```python
with open(f"{repo}/{package}", "r") as f:
    data = f.read().strip()
```

**After:**
```python
import subprocess
result = subprocess.run(
    ["grep", f"^{package} ", f"{repo}.txt"],
    capture_output=True, text=True
)
data = result.stdout.strip()
```

Or use the query script:
```python
import subprocess
result = subprocess.run(
    ["python3", "query_repository.py", "search", package, "--exact"],
    capture_output=True, text=True
)
```

### Pattern 2: Listing All Packages in a Repository

**Before:**
```python
import os
packages = os.listdir(repo)
```

**After:**
```python
with open(f"{repo}.txt", "r") as f:
    packages = [line.split()[0] for line in f if not line.startswith('#')]
```

### Pattern 3: Checking if Package Exists

**Before:**
```python
import os
exists = os.path.exists(f"{repo}/{package}")
```

**After:**
```python
import subprocess
result = subprocess.run(
    ["grep", "-q", f"^{package} ", f"{repo}.txt"],
    capture_output=True
)
exists = result.returncode == 0
```

### Pattern 4: Iterating Over All Packages

**Before:**
```python
import os
for repo_dir in ["core-any", "core-x86_64", "extra-any", "extra-x86_64"]:
    for package in os.listdir(repo_dir):
        with open(f"{repo_dir}/{package}") as f:
            data = f.read().strip()
            # Process data
```

**After:**
```python
import glob
for txt_file in glob.glob("*.txt"):
    with open(txt_file) as f:
        for line in f:
            if line.startswith('#'):
                continue
            data = line.strip()
            # Process data
```

## Helper Functions

Here are some helper functions to make migration easier:

```python
def get_package_info(repo, package):
    """Get package information from consolidated format"""
    with open(f"{repo}.txt", "r") as f:
        for line in f:
            if line.startswith(f"{package} "):
                return line.strip()
    return None

def list_packages(repo):
    """List all packages in a repository"""
    packages = []
    with open(f"{repo}.txt", "r") as f:
        for line in f:
            if not line.startswith('#') and line.strip():
                packages.append(line.strip().split()[0])
    return packages

def package_exists(repo, package):
    """Check if package exists in repository"""
    with open(f"{repo}.txt", "r") as f:
        for line in f:
            if line.startswith(f"{package} "):
                return True
    return False

def get_all_packages():
    """Get all packages from all repositories"""
    import glob
    all_packages = []
    for txt_file in glob.glob("*.txt"):
        with open(txt_file) as f:
            for line in f:
                if not line.startswith('#') and line.strip():
                    repo = txt_file[:-4]  # Remove .txt
                    package_data = line.strip()
                    all_packages.append({
                        'repo': repo,
                        'data': package_data
                    })
    return all_packages
```

## Rollback Plan

If you need to rollback to the original format:

```bash
# Restore from backup
tar -xzf original-format-backup.tar.gz

# Or regenerate from consolidated files
python3 regenerate_directories.py
```

## Benefits After Migration

Once fully migrated:
- 🚀 Faster Git operations
- 💾 99.87% less disk space (inodes)
- 🔍 Simpler queries with standard tools
- 🛠️ Easier maintenance
- 📈 Better scalability

## Support

Use the provided scripts:
- `consolidate_repository.py` - Create consolidated files
- `query_repository.py` - Query the consolidated format

For issues, check `PERFORMANCE_OPTIMIZATION.md` and `BENCHMARKS.md`.
