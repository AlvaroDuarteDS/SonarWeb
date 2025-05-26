import os
import tempfile
import shutil
from typing import Optional, List


class FileManager:
    def __init__(self):
        self.temp_dirs: List[str] = []

    def create_temp_dir(self, prefix: str) -> str:
        """Create a temporary directory"""
        temp_dir = os.path.join(tempfile.gettempdir(), prefix)
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        self.temp_dirs.append(temp_dir)
        return temp_dir

    def cleanup_temp_files(self):
        """Clean up all temporary directories"""
        for temp_dir in self.temp_dirs:
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    print(f"Cleaned up: {temp_dir}")
            except Exception as e:
                print(f"Error cleaning up {temp_dir}: {e}")

    def ensure_dir_exists(self, directory: str):
        """Ensure directory exists"""
        os.makedirs(directory, exist_ok=True)

    def delete_file_safe(self, file_path: str) -> bool:
        """Safely delete a file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
        return False
