#!/usr/bin/env python3

"""
File Watcher for Claude Sessions
Monitors file system changes and automatically logs them
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime
import subprocess

class FileWatcher:
    def __init__(self, watch_dirs=["/home/ubuntu"], exclude_dirs=None):
        self.watch_dirs = watch_dirs
        self.exclude_dirs = exclude_dirs or ['.git', 'node_modules', '__pycache__']
        self.admin_dir = Path("/home/ubuntu/claude-prompts/admin")
        self.current_session_file = self.admin_dir / ".current-session"
        self.last_scan = {}
        
    def get_current_session_file(self):
        """Get current session file path"""
        if not self.current_session_file.exists():
            return None
        session_id = self.current_session_file.read_text().strip()
        return self.admin_dir / f"session-{session_id}.md"
    
    def should_exclude(self, path):
        """Check if path should be excluded from monitoring"""
        path_str = str(path)
        
        # Exclude session files and heartbeats from being logged
        if 'claude-prompts/admin' in path_str and ('session-' in path_str or 'heartbeat' in path_str):
            return True
            
        # Exclude Claude internal files
        if '/.claude/' in path_str:
            return True
            
        return any(exclude in path_str for exclude in self.exclude_dirs)
    
    def scan_directory(self, directory):
        """Scan directory for file changes"""
        changes = []
        
        try:
            for root, dirs, files in os.walk(directory):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if not any(excl in d for excl in self.exclude_dirs)]
                
                for file in files:
                    file_path = Path(root) / file
                    
                    if self.should_exclude(file_path):
                        continue
                    
                    try:
                        stat = file_path.stat()
                        mtime = stat.st_mtime
                        size = stat.st_size
                        
                        file_key = str(file_path)
                        
                        if file_key in self.last_scan:
                            old_mtime, old_size = self.last_scan[file_key]
                            if mtime != old_mtime:
                                if old_size == 0 and size > 0:
                                    changes.append(('created', file_path))
                                else:
                                    changes.append(('modified', file_path))
                        else:
                            changes.append(('created', file_path))
                        
                        self.last_scan[file_key] = (mtime, size)
                        
                    except (OSError, PermissionError):
                        continue
                        
        except (OSError, PermissionError):
            pass
            
        return changes
    
    def log_file_changes(self, changes):
        """Log file changes to current session"""
        if not changes:
            return
            
        session_file = self.get_current_session_file()
        if not session_file or not session_file.exists():
            return
        
        content = session_file.read_text()
        
        # Find the "Files Created/Modified" section
        files_section = "## Files Created/Modified"
        files_pos = content.find(files_section)
        
        if files_pos == -1:
            return
        
        # Find the next section
        next_section_pos = content.find("## Key Learnings", files_pos)
        if next_section_pos == -1:
            next_section_pos = content.find("## Session Rating", files_pos)
        if next_section_pos == -1:
            next_section_pos = len(content)
        
        # Generate file change entries
        timestamp = datetime.now().strftime("%H:%M:%S")
        new_entries = []
        
        for change_type, file_path in changes:
            # Make path relative to home directory
            try:
                rel_path = file_path.relative_to(Path.home())
                display_path = f"~/{rel_path}"
            except ValueError:
                display_path = str(file_path)
            
            status_icon = "✅" if change_type == "created" else "🔄"
            new_entries.append(f"- [{timestamp}] {status_icon} **{change_type.title()}:** `{display_path}`")
        
        # Insert new entries
        insertion_point = files_pos + len(files_section) + 1
        
        # Find existing entries end
        lines = content[insertion_point:next_section_pos].split('\n')
        insert_pos = insertion_point
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('- '):
                break
            if line.startswith('- '):
                insert_pos = insertion_point + len('\n'.join(lines[:i+1])) + 1
        
        new_content = (
            content[:insert_pos] + 
            '\n' + '\n'.join(new_entries) + '\n' +
            content[insert_pos:]
        )
        
        session_file.write_text(new_content)
    
    def run(self):
        """Main monitoring loop"""
        print("Starting file watcher...")
        
        # Initial scan
        for watch_dir in self.watch_dirs:
            if Path(watch_dir).exists():
                self.scan_directory(watch_dir)
        
        while True:
            try:
                # Check if session is still active
                if not self.current_session_file.exists():
                    print("No active session, stopping file watcher")
                    break
                
                all_changes = []
                for watch_dir in self.watch_dirs:
                    if Path(watch_dir).exists():
                        changes = self.scan_directory(watch_dir)
                        all_changes.extend(changes)
                
                if all_changes:
                    print(f"Detected {len(all_changes)} file changes")
                    self.log_file_changes(all_changes)
                
                time.sleep(5)  # Check every 5 seconds
                
            except KeyboardInterrupt:
                print("File watcher stopped")
                break
            except Exception as e:
                print(f"Error in file watcher: {e}")
                time.sleep(10)

if __name__ == "__main__":
    watcher = FileWatcher()
    watcher.run()