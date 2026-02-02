#!/usr/bin/env python3
"""
Query helper script for consolidated repository format.
Provides fast searching and listing of packages.
"""

import sys
import argparse
from pathlib import Path
import re

def search_package(repo_path, package_name, exact=False):
    """Search for a package across all consolidated files"""
    results = []
    
    for file_path in Path(repo_path).glob("*.txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if line.startswith('#'):
                    continue
                
                parts = line.strip().split()
                if not parts:
                    continue
                
                pkg_name = parts[0]
                
                if exact and pkg_name == package_name:
                    results.append({
                        'repository': file_path.stem,
                        'line': line_num,
                        'data': line.strip()
                    })
                elif not exact and package_name.lower() in pkg_name.lower():
                    results.append({
                        'repository': file_path.stem,
                        'line': line_num,
                        'data': line.strip()
                    })
    
    return results

def list_repository(repo_path, repo_name):
    """List all packages in a repository"""
    file_path = Path(repo_path) / f"{repo_name}.txt"
    
    if not file_path.exists():
        return None
    
    packages = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.startswith('#') and line.strip():
                packages.append(line.strip())
    
    return packages

def list_all_repositories(repo_path):
    """List all available repositories"""
    repos = []
    for file_path in sorted(Path(repo_path).glob("*.txt")):
        with open(file_path, 'r', encoding='utf-8') as f:
            count = sum(1 for line in f if not line.startswith('#') and line.strip())
        repos.append({
            'name': file_path.stem,
            'file': file_path.name,
            'packages': count
        })
    return repos

def main():
    parser = argparse.ArgumentParser(
        description='Query Arch Linux State Repository (Consolidated Format)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for a package
  %(prog)s search firefox
  
  # Exact package name search
  %(prog)s search firefox --exact
  
  # List all packages in a repository
  %(prog)s list extra-x86_64
  
  # List all repositories
  %(prog)s repos
        """)
    
    parser.add_argument('command', choices=['search', 'list', 'repos'],
                        help='Command to execute')
    parser.add_argument('query', nargs='?',
                        help='Package name or repository name')
    parser.add_argument('--exact', action='store_true',
                        help='Exact match for package search')
    parser.add_argument('--repo-path', default='.',
                        help='Path to repository (default: current directory)')
    
    args = parser.parse_args()
    
    if args.command == 'search':
        if not args.query:
            print("Error: Package name required for search")
            sys.exit(1)
        
        results = search_package(args.repo_path, args.query, args.exact)
        
        if not results:
            print(f"No packages found matching '{args.query}'")
            sys.exit(1)
        
        print(f"Found {len(results)} package(s):\n")
        for result in results:
            print(f"Repository: {result['repository']}")
            print(f"  {result['data']}")
            print()
    
    elif args.command == 'list':
        if not args.query:
            print("Error: Repository name required for list")
            sys.exit(1)
        
        packages = list_repository(args.repo_path, args.query)
        
        if packages is None:
            print(f"Error: Repository '{args.query}' not found")
            sys.exit(1)
        
        print(f"Packages in {args.query} ({len(packages)} total):\n")
        for package in packages:
            print(f"  {package}")
    
    elif args.command == 'repos':
        repos = list_all_repositories(args.repo_path)
        
        if not repos:
            print("No repositories found")
            sys.exit(1)
        
        print("Available repositories:\n")
        print(f"{'Repository':<40s} {'File':<30s} {'Packages':>10s}")
        print("-" * 82)
        for repo in repos:
            print(f"{repo['name']:<40s} {repo['file']:<30s} {repo['packages']:>10,}")
        
        print()
        total = sum(r['packages'] for r in repos)
        print(f"{'Total':<40s} {len(repos)} files {total:>20,} packages")

if __name__ == '__main__':
    main()
