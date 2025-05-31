import argparse
import concurrent.futures
import os
import pathlib
import shutil
import time
import zipfile


class FastExtractor:
    """MAIN CLASS FOR THE EXTRACTOR"""

    def __init__(self, verbose:bool=True):
        self.verbose = verbose

    def _extract_member(
        self, zf: zipfile.ZipFile, member: zipfile.ZipInfo, output_dir: str
    ) -> int:
        """Extract a single zip member and return its size."""
        target_path = pathlib.Path(output_dir) / member.filename
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with zf.open(member) as src, open(target_path, "wb") as dst:
            shutil.copyfileobj(src, dst)
        return member.file_size

    def extract(self, input_dir: str, output_dir: str) -> int:
        """Extract all members using multi-threading and return total extracted size."""
        with zipfile.ZipFile(input_dir, "r") as zf:
            members = [m for m in zf.infolist() if not m.is_dir()]
            if self.verbose:
                print(f"[>>] Unzipping {len(members)} files...")
            total = 0
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=os.cpu_count()
            ) as executor:
                futures = [
                    executor.submit(self._extract_member, zf, m, output_dir)
                    for m in members
                ]
                for future in concurrent.futures.as_completed(futures):
                    total += future.result()
            return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract contents of a ZIP file.")
    parser.add_argument("input_dir", type=str, help="Path to the input ZIP file")
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=None,
        help="Optional: Path to the output directory. Defaults to input file's directory.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir or os.path.dirname(os.path.abspath(input_dir))

    start = time.time()
    f = FastExtractor(verbose=args.verbose)
    bytes_total = f.extract(args.input_dir, args.output_dir)
    end = time.time() - start
    if args.verbose:
        print(f"\nExtracted total {bytes_total / 1024:.2f} KB")
        print(f"\nExecution Time : {end:.4f} seconds")
