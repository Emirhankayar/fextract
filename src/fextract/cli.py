#!/usr/bin/env python3
"""
fextract - Fast multithreaded file extraction and compression tool
"""

import argparse
import pathlib
import sys
import time
import zipfile
from fextract.modules.f_ext import FastExt
from fextract.modules.f_cmp import FastComp

def format_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def main():
    parser = argparse.ArgumentParser(
        description="Fast multithreaded file extraction and compression tool",
        epilog="Examples:\n"
               "  fextract -x archive.zip                    # Extract to current directory\n"
               "  fextract -x archive.zip mydir              # Extract to specific directory\n"
               "  fextract -c mydir                          # Compress to current directory\n"
               "  fextract -c mydir archive.zip              # Compress to specific file\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("-x", "--extract", action="store_true", 
                          help="Extract files from archive")
    operation.add_argument("-c", "--compress", action="store_true", 
                          help="Compress files into archive")
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("-v", "--verbose", action="store_true", 
                             help="Verbose output (show progress and file list)")
    parser.add_argument("input", 
                       help="Input file (for extraction) or directory/file (for compression)")
    parser.add_argument("output", nargs="?", default=".", 
                       help="Output directory or file (default: current directory)")
    parser.add_argument("--version", action="version", version="fextract 1.0.0")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return 1
    verbose = args.verbose 
    input_path = pathlib.Path(args.input)
    output_path = args.output
    start_time = time.time()
    
    try:
        if args.extract:
            if not input_path.exists():
                print(f"Error: Input file '{input_path}' does not exist", file=sys.stderr)
                return 1
            if not input_path.is_file():
                print(f"Error: Input must be a file for extraction", file=sys.stderr)
                return 1
            if not input_path.suffix.lower() == '.zip':
                print(f"Warning: Input file doesn't have .zip extension")
            output_dir = pathlib.Path(output_path)
            output_dir.mkdir(parents=True, exist_ok=True)
            extractor = FastExt(verbose=verbose)
            total_size = extractor.extract(
                str(input_path), 
                str(output_dir), 
            )
            if verbose:
                print(f"Extracted '{input_path.name}' to '{output_dir.resolve()}' ({format_size(total_size)})")

        
        elif args.compress:
            if not input_path.exists():
                print(f"Error: Input path '{input_path}' does not exist", file=sys.stderr)
                return 1

            if args.output in {".", "./"}:
                if input_path.is_file():
                    output_path = input_path.with_suffix(".zip")
                else:
                    output_path = pathlib.Path(f"{input_path.name}.zip")
            else:
                output_path = pathlib.Path(args.output)
                if not output_path.name.endswith(".zip"):
                    output_path = output_path.with_suffix(".zip")

            compressor = FastComp(verbose=verbose)
            total_files = compressor.compress(
                input_path,
                str(output_path)
            )

            if verbose:
                print(f"Compressed {total_files} file(s) into {output_path}")

    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 1
    except PermissionError as e:
        print(f"Error: Permission denied - {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except zipfile.BadZipFile:
        print(f"Error: '{input_path}' is not a valid zip file", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    end_time = time.time()
    if verbose:
        print(f"Execution time: {end_time - start_time:.4f} seconds")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
