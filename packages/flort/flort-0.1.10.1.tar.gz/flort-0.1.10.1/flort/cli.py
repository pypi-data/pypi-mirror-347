#!/usr/bin/env python3
"""
Flort - File Concatenation and Project Overview Tool

This module provides functionality to create a consolidated view of a project's
source code by combining multiple files into a single output file. It can generate
directory trees, create Python module outlines, and concatenate source files while
respecting various filtering options.

The tool is particularly useful for:
- Creating project overviews
- Generating documentation
- Sharing code in a single file
- Analyzing project structure

Usage:
    flort [DIRECTORY...] [--extension...] [options]

Example:
    flort . --py --js --output=project.txt --hidden
"""

import os
import argparse
import logging
from datetime import datetime
from pathlib import Path

from .utils import generate_tree, write_file, configure_logging, print_configuration, count_file_tokens, archive_file
from .traverse import get_paths, get_files_from_glob_patterns
from .concatinate_files import concat_files
from .python_outline import python_outline_files
from .curses_selector import select_files


def main() -> None:
    """
    Main entry point for the Flort tool.

    This function:
    1. Sets up argument parsing with detailed help messages
    2. Configures logging based on verbosity
    3. Processes command line arguments
    4. Generates the output file containing:
        - Directory tree (optional)
        - Python module outline (if requested)
        - Concatenated source files (unless disabled)

    Returns:
        None

    Raises:
        SystemExit: If required arguments are missing or invalid
    """
    output_file = f"{os.path.basename(os.getcwd())}.flort.txt"
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create argument parser with comprehensive help
    parser = argparse.ArgumentParser(
        description="flort: create a single file of all given extensions, "
                    "recursively for all directories given. Ignores binary files.",
        prog='flort',
        add_help=False,
        prefix_chars='-',
        allow_abbrev=False
    )

    parser.add_argument('directories', metavar='directories',
                        help='Directories to list files from, defaults to the current working directory.',
                        default=".", type=str, nargs='*')
    parser.add_argument('-h', '--help', action='help',
                        help='Show this help message and exit.')
    parser.add_argument('-i', '--ignore-dirs', type=str,
                        help='Directories to ignore (comma-separated list).')
    parser.add_argument('-o', '--output', type=str,
                        help='Output file path. Defaults to the basename of the current directory '
                            'if not specified. "stdio" will output to console.', default=output_file)
    parser.add_argument('-O', '--outline', action='store_true',
                        help='Create an outline of the files instead of a source dump.')
    parser.add_argument('-n', '--no-dump', action='store_true',
                        help='Do not dump the source files')
    parser.add_argument('-t', '--no-tree', action='store_true',
                        help='Do not print the tree at the beginning.')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Include all files regardless of extensions.')
    parser.add_argument('-H', '--hidden', action='store_true',
                        help='Include hidden files.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose logging (INFO level).')
    parser.add_argument('-f', '--include-files', type=str,
                        help='Comma-separated list of files to include regardless of search filter.')
    parser.add_argument('-u', '--ui', action='store_true',
                    help='Launch interactive file selector UI')
    parser.add_argument('-g', '--glob', type=str,
                        help='Glob patterns to match files recursively (comma-separated list).',
                        metavar='GLOB')
    parser.add_argument('-z', '--archive', type=str, choices=['zip', 'tar.gz'],
                        help='Archive the output file using the specified format.')    
    parser.add_argument('-e', '--extensions', type=str,
                    help='File extensions to include (comma-separated, without dots: py,js,txt)')

    args, unknown_args = parser.parse_known_args()

    # Configure logging based on verbosity flag
    configure_logging(args.verbose)

    # Process ignore_dirs argument
    if args.ignore_dirs:
        ignore_dirs = [Path(ignore_dir).resolve() for ignore_dir in args.ignore_dirs.split(',')]
    else:
        ignore_dirs = []

  
    # If the output file exists, delete it first to prevent including it in the path list
    output_path = Path(args.output)
    if output_path.exists() and args.output != "stdio":
        try:
            output_path.unlink()
            logging.info(f"Deleted existing output file: {args.output}")
        except Exception as e:
            logging.warning(f"Could not delete existing output file: {args.output} - {e}")
    

    # Then in the code, instead of parsing unknown args:
    extensions = []
    if args.extensions:
        extensions = [f".{ext.strip()}" for ext in args.extensions.split(',')]
    
    if args.ui:
        included_files = args.include_files.split(',') if args.include_files else None
        included_dirs = args.directories if args.directories and args.directories[0] != "." else None
        
        result = select_files(
            start_path="." if not args.directories or args.directories[0] == "." else args.directories[0],
            preselected_filters=extensions,
            included_files=included_files,
            ignored_dirs=ignore_dirs,
            included_dirs=included_dirs
        )

        if result is None:
            return
            
        # Update settings based on UI selection
        extensions.extend(result["file_types"])
        extensions = list(set(extensions))  # Remove duplicates
        
        # Add ignored directories from UI
        ignore_dirs.extend([Path(p) for p in result["ignored"]])
        
        # Override directories with selected ones
        selected_dirs = [str(Path(p)) for p in result["selected"] if Path(p).is_dir()]
        if selected_dirs:
            args.directories = selected_dirs


    # Log configuration settings
    print_configuration(
        args.directories,
        extensions,
        args.all,
        args.hidden,
        ignore_dirs
    )

    # Validate extensions or --all flag
    if not extensions and not args.all and not args.glob:
        logging.error("No extensions or glob provided and --all flag not set. No files to process.")
        return

    # Initialize output file with timestamp
    write_file(args.output, f"## Florted: {current_datetime}\n", 'w')

    # Get list of files to process
    path_list = get_paths(
        args.directories,
        extensions=extensions,
        include_all=args.all,
        include_hidden=args.hidden,
        ignore_dirs=ignore_dirs
    )

    # Process glob patterns if provided
    if args.glob:
        glob_patterns = [pattern.strip() for pattern in args.glob.split(',')]
        print(f"Searching for glob patterns: {glob_patterns} in directories: {args.directories}")
        
        # Create a list of directories to search
        search_dirs = [Path(d).resolve() for d in args.directories]
        
        # Process each glob pattern
        for pattern in glob_patterns:
            # Search in each directory
            for base_dir in search_dirs:
                print(f"Searching for {pattern} in {base_dir}")
                
                # Skip if not a directory
                if not base_dir.is_dir():
                    print(f"Skipping {base_dir} - not a directory")
                    continue
                    
                # Find files matching the pattern
                for file_path in base_dir.glob('**/' + pattern):
                    if not file_path.is_file():
                        continue
                        
                    # Check if in ignored directory
                    should_ignore = False
                    for ignore_dir in ignore_dirs:
                        try:
                            file_path.relative_to(ignore_dir)
                            should_ignore = True
                            break
                        except ValueError:
                            pass
                    
                    if not should_ignore:
                        print(f"Found: {file_path}")
                        try:
                            rel_path = str(file_path.relative_to(Path.cwd()))
                        except ValueError:
                            rel_path = str(file_path)
                            
                        # Check if not already in path_list
                        if not any(str(item.get("path")) == str(file_path) for item in path_list):
                            path_list.append({
                                "path": file_path,
                                "relative_path": rel_path,
                                "depth": len(file_path.parts) - len(Path.cwd().parts),
                                "type": "file"
                            })
                            
    # Add included files from --include-files option
    if args.include_files:
        for file_str in args.include_files.split(','):
            file_path = Path(file_str.strip()).resolve()
            if file_path.exists() and file_path.is_file():
                try:
                    rel_path = str(file_path.relative_to(Path.cwd()))
                except ValueError:
                    rel_path = str(file_path)
                path_list.append({
                    "path": file_path,
                    "relative_path": rel_path,
                    "depth": 1,
                    "type": "file"
                })
            else:
                logging.warning(f"Included file not found or invalid: {file_str}")

   # Exclude the output file from the path list if it somehow got included
    output_path_resolved = output_path.resolve()
    path_list = [item for item in path_list if item["path"].resolve() != output_path_resolved]


    print(f"Output to {args.output}")

    # Generate directory tree if not disabled
    if not args.no_tree:
        generate_tree(path_list, args.output)
    # Generate Python outline if requested
    if args.outline:
        python_outline_files(path_list, args.output)

    # Concatenate source files if not disabled
    if not args.no_dump:
        concat_files(path_list, args.output)

    print(count_file_tokens(args.output))

    # Archive the output file if requested
    if args.archive:
        archive_path = archive_file(args.output, args.archive)
        print(f"Archive created: {archive_path}")

    print("")

    print(count_file_tokens(args.output))
    print("")

if __name__ == "__main__":
    main()

