import os
import bisect
import zipfile
import pathlib
import threading
import concurrent.futures

class FastComp:
    """MAIN CLASS FOR THE COMPRESSOR"""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.compressed_files = []
        self.log_lock = threading.Lock()
    
    def _log(self, msg: str):
        if self.verbose:
            with self.log_lock:
                print(msg)

    def _compress_file(
        self, file_path: pathlib.Path, base_path: pathlib.Path
    ) -> tuple[str, bytes, int]:
        relative_path = file_path.relative_to(base_path)
        with open(file_path, "rb") as f:
            data = f.read()
        return str(relative_path), data, len(data)

    def compress(self, input_path: str, output_file: str) -> int:
        input_path = pathlib.Path(input_path)
        
        if input_path.is_file():
            files = [input_path]
            base_path = input_path.parent
        else:
            files = [f for f in input_path.rglob("*") if f.is_file()]
            base_path = input_path
        
        self._log(f"[>>] Compressing {len(files)} files...")
        total = 0
        
        with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zf:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=os.cpu_count()
            ) as executor:
                futures = [
                    executor.submit(self._compress_file, f, base_path)
                    for f in files
                ]
                for future in concurrent.futures.as_completed(futures):
                    relative_path, data, size = future.result()
                    zf.writestr(relative_path, data)
                    with self.log_lock:
                        bisect.insort(self.compressed_files, relative_path)
                    total += size
        
        self._log("[>>] Compressed files:")
        for fname in self.compressed_files:
            self._log(fname)
        return total