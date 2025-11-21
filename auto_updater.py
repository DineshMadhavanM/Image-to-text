import os
import time
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Set

class AutoUpdater:
    def __init__(self, project_root: str, check_interval: int = 5):
        """
        Initialize the AutoUpdater with project root directory and check interval in seconds.
        
        Args:
            project_root: Root directory of the project to monitor
            check_interval: Time in seconds between checks for file changes
        """
        self.project_root = Path(project_root)
        self.check_interval = check_interval
        self.file_hashes: Dict[str, str] = {}
        self.ignored_dirs = {'__pycache__', '.git', '.github', '.venv', 'venv'}
        self.ignored_extensions = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe'}
        self.initialize_hashes()

    def get_file_hash(self, filepath: Path) -> str:
        """Calculate MD5 hash of a file's content."""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return ""

    def should_ignore(self, path: Path) -> bool:
        """Check if a path should be ignored."""
        # Skip hidden files and directories
        if any(part.startswith('.') and part not in ['.', '..'] for part in path.parts):
            return True
            
        # Skip ignored directories and files
        if path.is_dir():
            return path.name in self.ignored_dirs
            
        return (path.suffix.lower() in self.ignored_extensions or 
                any(part in self.ignored_dirs for part in path.parts))

    def initialize_hashes(self) -> None:
        """Initialize file hashes for the entire project."""
        for root, dirs, files in os.walk(self.project_root):
            # Remove ignored directories from dirs to prevent os.walk from traversing them
            dirs[:] = [d for d in dirs if not self.should_ignore(Path(root) / d)]
            
            for file in files:
                filepath = Path(root) / file
                if not self.should_ignore(filepath):
                    self.file_hashes[str(filepath.relative_to(self.project_root))] = self.get_file_hash(filepath)

    def check_for_changes(self) -> Set[str]:
        """Check for any file changes in the project."""
        changed_files = set()
        current_files = set()
        
        # Check for new or modified files
        for root, dirs, files in os.walk(self.project_root):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not self.should_ignore(Path(root) / d)]
            
            for file in files:
                filepath = Path(root) / file
                rel_path = str(filepath.relative_to(self.project_root))
                
                if self.should_ignore(filepath):
                    continue
                    
                current_files.add(rel_path)
                current_hash = self.get_file_hash(filepath)
                
                if rel_path not in self.file_hashes:
                    print(f"New file detected: {rel_path}")
                    self.file_hashes[rel_path] = current_hash
                    changed_files.add(rel_path)
                elif current_hash != self.file_hashes[rel_path]:
                    print(f"File modified: {rel_path}")
                    self.file_hashes[rel_path] = current_hash
                    changed_files.add(rel_path)
        
        # Check for deleted files
        deleted_files = set(self.file_hashes.keys()) - current_files
        for file in deleted_files:
            print(f"File deleted: {file}")
            del self.file_hashes[file]
            changed_files.add(file)
        
        return changed_files

    def on_file_changed(self, filepath: str) -> None:
        """Handle file change event. Override this method to implement custom behavior."""
        print(f"Processing changes in: {filepath}")
        
        # Example: If it's a Python file, you could run tests or format the code
        if filepath.endswith('.py'):
            print(f"  - Detected Python file, you could run tests or formatting here")
        
        # Example: If it's a requirements file, you could update dependencies
        elif filepath == 'requirements.txt':
            print("  - Detected requirements.txt, you could run 'pip install -r requirements.txt'")

    def watch(self) -> None:
        """Start watching for file changes."""
        print(f"Watching for file changes in {self.project_root}...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                changed_files = self.check_for_changes()
                for file in changed_files:
                    self.on_file_changed(file)
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("\nStopping file watcher...")

if __name__ == "__main__":
    # Example usage
    project_root = os.path.dirname(os.path.abspath(__file__))
    updater = AutoUpdater(project_root)
    updater.watch()
