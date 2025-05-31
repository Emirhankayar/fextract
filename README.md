# fextract 

## Installation
> https://pypi.org/project/fextract/1.0.0/

```bash
pip install fextract
```
## Usage
```
usage: fextract [-h] (-x | -c) [-v] [--version] input [output]

Fast multithreaded file extraction and compression tool

positional arguments:
  input           Input file (for extraction) or directory/file (for compression)
  output          Output directory or file (default: current directory)

options:
  -h, --help      show this help message and exit
  -x, --extract   Extract files from archive
  -c, --compress  Compress files into archive
  -v, --verbose   Verbose output (show progress and file list)
  --version       show program's version number and exit

Examples:
  fextract -x archive.zip                    # Extract to current directory
  fextract -x archive.zip mydir              # Extract to specific directory
  fextract -c mydir                          # Compress to current directory
  fextract -c mydir archive.zip              # Compress to specific file
```
