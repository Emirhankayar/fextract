import os
import bisect
import shutil
import zipfile
import pathlib
import threading
import concurrent.futures

class FastExt:
    """MAIN CLASS FOR THE EXTRACTOR"""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.extracted_files = []
        self.log_lock = threading.Lock()
    
    def _log(self, msg:str):
        if self.verbose:
            with self.log_lock:
                print(msg)

    def _extract_member(
        self, zf: zipfile.ZipFile, member: zipfile.ZipInfo, output_dir: str
    ) -> int:
        target_path = pathlib.Path(output_dir) / member.filename
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with zf.open(member) as src, open(target_path, "wb") as dst:
            shutil.copyfileobj(src, dst)
        with self.log_lock:
            bisect.insort(self.extracted_files, member.filename)
        return member.file_size

    def extract(self, input_dir: str, output_dir: str) -> int:
        with zipfile.ZipFile(input_dir, "r") as zf:
            members = [m for m in zf.infolist() if not m.is_dir()]
            self._log(f"[>>] Unzipping {len(members)} files...")
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
            self._log("[>>] Extracted files:")
            for fname in self.extracted_files:
                self._log(fname)
            return total