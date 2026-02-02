#!/usr/bin/env python3
"""
Repository Consolidation Script
Consolidates individual package files into one file per repository directory
for improved performance.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def consolidate_directory(repo_path, dir_name):
    """
    Consolidate all files in a directory into a single text file.
    
    Args:
        repo_path: Path to the repository root
        dir_name: Name of the directory to consolidate
    
    Returns:
        Tuple of (output_file, package_count, error_count)
    """
    source_dir = Path(repo_path) / dir_name
    output_file = Path(repo_path) / f"{dir_name}.txt"
    
    if not source_dir.exists() or not source_dir.is_dir():
        print(f"Warning: Directory {dir_name} not found, skipping")
        return None, 0, 0
    
    packages = []
    error_count = 0
    
    # Read all package files
    for file_path in sorted(source_dir.iterdir()):
        if file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        packages.append(content)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                error_count += 1
    
    # Write consolidated file
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write(f"# Repository: {dir_name}\n")
        f.write(f"# Generated: {datetime.now().isoformat()}\n")
        f.write(f"# Package count: {len(packages)}\n")
        f.write(f"# Format: package-name version1 version2 commit-hash\n")
        f.write("#\n")
        
        # Package data
        for package in packages:
            f.write(package + '\n')
    
    return output_file, len(packages), error_count

def main():
    """Main consolidation function"""
    repo_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    repo_path = Path(repo_path).resolve()
    
    print("=" * 80)
    print("REPOSITORY CONSOLIDATION SCRIPT")
    print("=" * 80)
    print(f"Repository: {repo_path}")
    print()
    
    # Find all package directories (exclude .git and files)
    directories = []
    for item in repo_path.iterdir():
        if item.is_dir() and item.name != '.git':
            directories.append(item.name)
    
    directories.sort()
    
    print(f"Found {len(directories)} package directories to consolidate")
    print()
    
    total_packages = 0
    total_errors = 0
    created_files = []
    
    # Consolidate each directory
    for dir_name in directories:
        print(f"Consolidating {dir_name}...", end=' ')
        output_file, package_count, error_count = consolidate_directory(repo_path, dir_name)
        
        if output_file:
            total_packages += package_count
            total_errors += error_count
            created_files.append(output_file)
            print(f"✓ {package_count} packages → {output_file.name}")
        else:
            print("✗ Skipped")
    
    print()
    print("=" * 80)
    print("CONSOLIDATION COMPLETE")
    print("=" * 80)
    print(f"Created files: {len(created_files)}")
    print(f"Total packages: {total_packages:,}")
    print(f"Errors: {total_errors}")
    print()
    
    if created_files:
        print("Created consolidated files:")
        for file_path in created_files:
            size = file_path.stat().st_size
            print(f"  {file_path.name:40s} {size:>8,} bytes")
    
    print()
    print("To use the consolidated format:")
    print("  - Search for package: grep '^package-name ' repo-name.txt")
    print("  - List all packages: cat *.txt | grep -v '^#'")
    print("  - Count packages: cat *.txt | grep -v '^#' | wc -l")
    print()
    print("Original directories preserved. Remove them manually if no longer needed.")
    print()

if __name__ == '__main__':
    main()
