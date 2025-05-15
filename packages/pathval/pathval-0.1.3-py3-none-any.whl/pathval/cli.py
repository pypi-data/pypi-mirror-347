"""
pathval - CLI tool to validate file paths across different platforms

This tool recursively validates file and directory paths for compatibility
with specified platforms using the pathvalidate library.
"""

import os
import sys
import argparse
from typing import List, Optional, Set, Tuple

from pathvalidate import (
    validate_filepath,
    sanitize_filepath,
    sanitize_filename,
    ValidationError
)

PATHVAL_VER = "0.1.3"
KIND_FILE = "file"
KIND_DIR = "dir"
STDOUTPUT = "-"


class InvalidPath:
    """Store information about an invalid path."""
    
    def __init__(
        self,
        path: str,
        kind: str,
        error: Optional[str] = None,
        suggestion: Optional[str] = None
    ):
        self.path = path
        self.kind = kind
        self.error = error
        self.suggestion = suggestion
    
    def __str__(self) -> str:
        build_str = f"[{self.kind}] {self.path}\n"
        if self.error is not None:
            build_str += f"  ! {self.error}\n"
        if self.suggestion is not None:
            build_str += f"  * [SGGSTN] {self.suggestion}\n"
        return build_str
    
    def __eq__(self, other):
        if not isinstance(other, InvalidPath):
            return NotImplemented
        return self.path == other.path
    
    def __hash__(self):
        return hash(self.path)


def validate_single_path(path: str, platform: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a single path for the specified platform.
    
    Args:
        path: Path to validate
        platform: Target platform
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        validate_filepath(path, platform=platform)
        return True, None
    except ValidationError as e:
        return False, str(e)


def validate_directory_structure(
    base_dir: str,
    platform: str = "universal",
    no_error: bool = False,
    no_suggest: bool = False,
    quiet: bool = False,
    shallow: bool = False,
) -> List[InvalidPath]:
    """
    Recursively validate paths in a directory structure.
    
    Args:
        base_dir: Base directory to scan
        platform: Target platform
        no_error: Disable error reporting
        no_suggest: Disable suggestions
        quiet: Suppress progress messages
        shallow: Disable recursion
        
    Returns:
        Sorted list of invalid paths with their information
    """
    if not quiet:
        print(f"Scanning directory: {base_dir}\n")

    # Set of invalid paths
    invalid_path_set: Set[InvalidPath] = set()
    
    # Set to keep track of directories to skip
    skip_dirs: Set[str] = set()

    # Convert to absolute path for consistency
    base_dir = os.path.abspath(base_dir)

    # Determine if shallow walker or the usual recursive walker
    walker = os.walk(base_dir, topdown=True, followlinks=False)
    if shallow:
        try:
            walker = iter([next(walker)])
        except StopIteration:
            walker = iter([])
    
    # Use os.walk with followlinks=False to avoid symlink loops
    for root, dirs, files in walker:
        # Sort for alphabetic printing per walk level
        dirs.sort()
        files.sort()
        # Skip directories that are under already invalid paths
        dirs_to_remove: List[int] = []
        for i, dir_name in enumerate(dirs):
            parent_path = os.path.relpath(root, base_dir)
            dir_path = os.path.join(parent_path, dir_name) if parent_path != "." else dir_name
            
            # Skip if any parent directory is in the skip list
            should_skip = False
            for skip_dir in skip_dirs:
                if dir_path.startswith(skip_dir + os.sep):
                    should_skip = True
                    break
            
            if should_skip:
                dirs_to_remove.append(i)
                continue
            
            # Check the directory path
            is_valid, error = validate_single_path(dir_path, platform)
            if not is_valid:
                invp = InvalidPath(
                    dir_path,
                    KIND_DIR, 
                    None if no_error else error,
                    None if no_suggest else get_sanitized_path(dir_path, platform)
                )
                invalid_path_set.add(invp)
                dirs_to_remove.append(i)
                skip_dirs.add(dir_path)
                if not quiet:
                    print(invp)
        
        # Remove invalid directories in reverse order to avoid index shifting
        for i in sorted(dirs_to_remove, reverse=True):
            del dirs[i]
        
        # Check files
        for file_name in files:
            abs_file_path = os.path.join(root, file_name)
            file_path = os.path.relpath(abs_file_path, base_dir)
            
            is_valid, error = validate_single_path(file_path, platform)
            if not is_valid:
                invp = InvalidPath(
                    file_path,
                    KIND_FILE,
                    None if no_error else error,
                    None if no_suggest else get_sanitized_path(file_path, platform)
                )
                invalid_path_set.add(invp)
                if not quiet:
                    print(invp)
    
    return sorted(invalid_path_set, key=lambda invp: invp.path)


def get_sanitized_path(path: str, platform: str) -> str:
    """
    Get a sanitized version of the path.
    
    Args:
        path: Path to sanitize
        platform: Target platform
        
    Returns:
        Sanitized path
    """
    try:
        return sanitize_filepath(path, platform=platform)
    except Exception:
        # Fall back to sanitizing just the filename if the full path fails
        dirname = os.path.dirname(path)
        filename = os.path.basename(path)
        sanitized_name = sanitize_filename(filename, platform=platform)
        return os.path.join(dirname, sanitized_name)


def main():
    parser = argparse.ArgumentParser(
        description="Validate paths for compatibility across platforms",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"pathval version {PATHVAL_VER}",
        help="Print pathval version"
    )
    parser.add_argument(
        "directory",
        # nargs="?",
        # default=".",
        help="Directory to scan for invalid paths, e.g.: `pathval .`"
    )
    parser.add_argument(
        "-p", "--platform",
        choices=["universal", "windows", "linux", "macos", "posix"],
        default="universal",
        help="Target platform for validation"
    )
    parser.add_argument(
        "--no-error",
        action="store_true",
        help="Disable logging errors for invalid paths"
    )
    parser.add_argument(
        "--no-suggest",
        action="store_true",
        help="Disable sanitized suggestions for invalid paths"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress output"
    )
    parser.add_argument(
        "-s", "--shallow",
        action="store_true",
        help="Do not recurse down subdirectories"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["text", "csv", "json"],
        default="text",
        help="Output format (does nothing if no output file)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Write output to file or stdout (use `-` for stdout)"
    )

    args = parser.parse_args()

    if args.output and args.output != STDOUTPUT and os.path.exists(args.output):
        print("Error: Output file already exists", file=sys.stderr)
        return 2
    
    try:
        print()

        invalid_paths = validate_directory_structure(
            base_dir   = args.directory,
            platform   = args.platform,
            no_error   = args.no_error,
            no_suggest = args.no_suggest,
            quiet      = args.quiet,
            shallow    = args.shallow
        )

        plat = 'most' if args.platform == 'universal' else args.platform
        
        if not invalid_paths:
            if not args.quiet:
                print(f"✓ All paths compatible with {plat} platforms")
            return 0
        
        if not args.quiet:
            print(f"Found {len(invalid_paths)} invalid path(s) for {plat} platforms\n")

        if args.output:
            outstr = ""
            if args.format == "text":
                for invp in invalid_paths:
                    outstr += f"{invp}\n"
            
            elif args.format == "csv":
                outstr += "path,kind,error,suggestion\n"
                for invp in invalid_paths:
                    outstr += f'"{invp.path}","{invp.kind}","{invp.error}","{invp.suggestion}"\n'
                outstr += "\n"
            
            elif args.format == "json":
                import json
                data = {}
                for invp in invalid_paths:
                    data[invp.path] = {
                        "kind": invp.kind,
                        "error": invp.error,
                        "suggestion": invp.suggestion
                    }
                outstr = json.dumps(data, indent=2) + "\n\n"

            # Write output or print to stdout
            if args.output == STDOUTPUT:
                print(outstr, end="")
            else:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(outstr)
            print(f"Results written to {args.output}\n")
        
        return 1  # Return non-zero if invalid paths were found
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())