#!/usr/bin/env python3
"""
Query tool for Arch Linux package state repository.
Allows searching and querying package information across all repositories.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple


class PackageStateQuery:
    """Query package states from the repository directories."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.repos = self._discover_repos()
    
    def _discover_repos(self) -> List[Path]:
        """Discover all repository directories."""
        repos = []
        for item in self.repo_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                repos.append(item)
        return sorted(repos)
    
    # Package state file format constants
    EXPECTED_FIELDS = 4  # package-name version1 version2 commit-hash
    
    def _parse_package_line(self, line: str) -> Tuple[str, str, str, str]:
        """Parse a package state line.
        
        Returns: (package_name, version, previous_version, commit_hash)
        """
        parts = line.strip().split()
        if len(parts) >= self.EXPECTED_FIELDS:
            return parts[0], parts[1], parts[2], parts[3]
        return "", "", "", ""
    
    def search_package(self, package_name: str) -> List[Dict[str, str]]:
        """Search for a package across all repositories."""
        results = []
        for repo in self.repos:
            package_file = repo / package_name
            if package_file.exists():
                with open(package_file, 'r') as f:
                    content = f.read().strip()
                    if content:
                        name, ver1, ver2, commit = self._parse_package_line(content)
                        results.append({
                            'repository': repo.name,
                            'package': name,
                            'version': ver1,
                            'previous_version': ver2,
                            'commit': commit
                        })
        return results
    
    def list_packages(self, repo_name: str = None) -> List[str]:
        """List all packages in a repository or all repositories."""
        packages = []
        repos_to_check = [r for r in self.repos if r.name == repo_name] if repo_name else self.repos
        
        for repo in repos_to_check:
            if repo.is_dir():
                for package_file in repo.iterdir():
                    if package_file.is_file() and not package_file.name.startswith('.'):
                        packages.append(f"{repo.name}/{package_file.name}")
        
        return sorted(packages)
    
    def get_package_info(self, package_name: str, repo_name: str) -> Dict[str, str]:
        """Get detailed information about a specific package in a repository."""
        repo_path = self.repo_path / repo_name / package_name
        if repo_path.exists():
            with open(repo_path, 'r') as f:
                content = f.read().strip()
                if content:
                    name, ver1, ver2, commit = self._parse_package_line(content)
                    return {
                        'repository': repo_name,
                        'package': name,
                        'version': ver1,
                        'previous_version': ver2,
                        'commit': commit
                    }
        return {}


def main():
    parser = argparse.ArgumentParser(
        description='Query Arch Linux package state repository'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for a package')
    search_parser.add_argument('package', help='Package name to search for')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List packages')
    list_parser.add_argument('--repo', help='Repository name to list packages from')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get package information')
    info_parser.add_argument('package', help='Package name')
    info_parser.add_argument('repo', help='Repository name')
    
    # Repos command
    subparsers.add_parser('repos', help='List all repositories')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    query = PackageStateQuery()
    
    if args.command == 'search':
        results = query.search_package(args.package)
        if results:
            print(f"Found '{args.package}' in {len(results)} repository/repositories:")
            for result in results:
                commit_short = result['commit'][:8] if len(result['commit']) >= 8 else result['commit']
                print(f"  {result['repository']}: {result['package']} {result['version']} (commit: {commit_short})")
        else:
            print(f"Package '{args.package}' not found in any repository")
            sys.exit(1)
    
    elif args.command == 'list':
        packages = query.list_packages(args.repo)
        if packages:
            if args.repo:
                print(f"Packages in {args.repo}:")
            else:
                print("All packages:")
            for package in packages:
                print(f"  {package}")
        else:
            print(f"No packages found{' in ' + args.repo if args.repo else ''}")
    
    elif args.command == 'info':
        info = query.get_package_info(args.package, args.repo)
        if info:
            print(f"Package: {info['package']}")
            print(f"Repository: {info['repository']}")
            print(f"Version: {info['version']}")
            print(f"Commit: {info['commit']}")
        else:
            print(f"Package '{args.package}' not found in repository '{args.repo}'")
            sys.exit(1)
    
    elif args.command == 'repos':
        print("Available repositories:")
        for repo in query.repos:
            count = sum(1 for _ in repo.iterdir())
            print(f"  {repo.name} ({count} packages)")


if __name__ == '__main__':
    main()
