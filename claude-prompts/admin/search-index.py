#!/usr/bin/env python3

"""
Search Index Builder for Claude Sessions
Creates and maintains a searchable index for fast queries
"""

import json
import re
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
import argparse

class SessionSearchIndex:
    def __init__(self, index_path=None):
        if index_path is None:
            index_path = Path("/home/ubuntu/claude-prompts/admin/search-index.db")
        self.index_path = Path(index_path)
        self.admin_dir = Path("/home/ubuntu/claude-prompts/admin")
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for search index"""
        self.conn = sqlite3.connect(self.index_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                session_id TEXT UNIQUE,
                file_path TEXT,
                created_date TEXT,
                last_modified INTEGER,
                file_hash TEXT
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY,
                session_id TEXT,
                content_type TEXT,  -- 'prompt', 'response', 'file_change', 'metadata'
                content TEXT,
                timestamp TEXT,
                line_number INTEGER,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        # Create full-text search virtual table
        self.conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS content_fts USING fts5(
                content,
                content_type,
                session_id,
                timestamp
            )
        """)
        
        self.conn.commit()
    
    def get_file_hash(self, file_path):
        """Calculate MD5 hash of file for change detection"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""
    
    def needs_reindex(self, session_file):
        """Check if session file needs to be reindexed"""
        session_id = session_file.stem.replace('session-', '')
        file_stat = session_file.stat()
        current_hash = self.get_file_hash(session_file)
        
        cursor = self.conn.execute(
            "SELECT last_modified, file_hash FROM sessions WHERE session_id = ?",
            (session_id,)
        )
        result = cursor.fetchone()
        
        if not result:
            return True  # New file
        
        stored_modified, stored_hash = result
        return (file_stat.st_mtime != stored_modified or 
                current_hash != stored_hash)
    
    def parse_session_file(self, session_file):
        """Parse session file and extract searchable content"""
        try:
            content = session_file.read_text()
            session_id = session_file.stem.replace('session-', '')
            entries = []
            
            lines = content.split('\n')
            current_section = None
            current_content = []
            line_num = 0
            
            for line in lines:
                line_num += 1
                
                # Detect prompts
                if '**Command/Request:**' in line:
                    current_section = 'prompt'
                    current_content = []
                elif '**Output/Response:**' in line:
                    if current_section == 'prompt' and current_content:
                        entries.append({
                            'type': 'prompt',
                            'content': '\n'.join(current_content).strip(),
                            'line': line_num - len(current_content),
                            'timestamp': self.extract_timestamp(content, line_num)
                        })
                    current_section = 'response'
                    current_content = []
                elif line.startswith('### Prompt (') and ')' in line:
                    # Extract timestamp from prompt headers
                    timestamp = re.search(r'### Prompt \((\d{2}:\d{2}:\d{2})\)', line)
                    if timestamp:
                        current_timestamp = timestamp.group(1)
                elif re.match(r'^- \[\d{2}:\d{2}:\d{2}\].*\*\*(Created|Modified):\*\*', line):
                    # File change entries
                    entries.append({
                        'type': 'file_change',
                        'content': line,
                        'line': line_num,
                        'timestamp': self.extract_timestamp_from_line(line)
                    })
                elif current_section in ['prompt', 'response']:
                    if line.strip() and not line.startswith('**') and not line.startswith('```'):
                        current_content.append(line)
                    elif line.startswith('---') and current_content:
                        # End of section
                        entries.append({
                            'type': current_section,
                            'content': '\n'.join(current_content).strip(),
                            'line': line_num - len(current_content),
                            'timestamp': getattr(self, 'current_timestamp', None)
                        })
                        current_section = None
                        current_content = []
            
            return session_id, entries
            
        except Exception as e:
            print(f"Error parsing {session_file}: {e}")
            return None, []
    
    def extract_timestamp(self, content, around_line):
        """Extract timestamp from content around a specific line"""
        lines = content.split('\n')
        for i in range(max(0, around_line-10), min(len(lines), around_line+10)):
            timestamp = re.search(r'(\d{2}:\d{2}:\d{2})', lines[i])
            if timestamp:
                return timestamp.group(1)
        return None
    
    def extract_timestamp_from_line(self, line):
        """Extract timestamp from a line"""
        match = re.search(r'\[(\d{2}:\d{2}:\d{2})\]', line)
        return match.group(1) if match else None
    
    def index_session(self, session_file):
        """Index a single session file"""
        session_id, entries = self.parse_session_file(session_file)
        if not session_id:
            return False
        
        file_stat = session_file.stat()
        file_hash = self.get_file_hash(session_file)
        
        # Update or insert session record
        self.conn.execute("""
            INSERT OR REPLACE INTO sessions 
            (session_id, file_path, created_date, last_modified, file_hash)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session_id,
            str(session_file),
            session_id.split('-')[0] + '-' + session_id.split('-')[1] + '-' + session_id.split('-')[2],
            file_stat.st_mtime,
            file_hash
        ))
        
        # Clear existing content for this session
        self.conn.execute("DELETE FROM content WHERE session_id = ?", (session_id,))
        self.conn.execute("DELETE FROM content_fts WHERE session_id = ?", (session_id,))
        
        # Insert new content
        for entry in entries:
            self.conn.execute("""
                INSERT INTO content 
                (session_id, content_type, content, timestamp, line_number)
                VALUES (?, ?, ?, ?, ?)
            """, (
                session_id,
                entry['type'],
                entry['content'],
                entry.get('timestamp'),
                entry.get('line', 0)
            ))
            
            # Also insert into FTS table
            self.conn.execute("""
                INSERT INTO content_fts 
                (content, content_type, session_id, timestamp)
                VALUES (?, ?, ?, ?)
            """, (
                entry['content'],
                entry['type'],
                session_id,
                entry.get('timestamp', '')
            ))
        
        self.conn.commit()
        return True
    
    def build_index(self, force=False):
        """Build or update the search index"""
        session_files = list(self.admin_dir.glob('session-*.md'))
        indexed_count = 0
        
        print(f"Found {len(session_files)} session files")
        
        for session_file in session_files:
            if force or self.needs_reindex(session_file):
                if self.index_session(session_file):
                    indexed_count += 1
                    print(f"Indexed: {session_file.name}")
        
        print(f"Indexing complete. Processed {indexed_count} files.")
        return indexed_count
    
    def search(self, query, content_type=None, limit=10):
        """Search the index"""
        base_query = "SELECT session_id, content_type, content, timestamp FROM content_fts WHERE content_fts MATCH ?"
        params = [query]
        
        if content_type:
            base_query += " AND content_type = ?"
            params.append(content_type)
        
        base_query += " ORDER BY rank LIMIT ?"
        params.append(limit)
        
        cursor = self.conn.execute(base_query, params)
        return cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def main():
    parser = argparse.ArgumentParser(description='Claude Session Search Index')
    parser.add_argument('command', choices=['build', 'search', 'rebuild'],
                       help='Command to execute')
    parser.add_argument('--query', '-q', help='Search query')
    parser.add_argument('--type', '-t', choices=['prompt', 'response', 'file_change'],
                       help='Content type filter')
    parser.add_argument('--limit', '-l', type=int, default=10,
                       help='Result limit')
    parser.add_argument('--force', '-f', action='store_true',
                       help='Force rebuild of entire index')
    
    args = parser.parse_args()
    
    index = SessionSearchIndex()
    
    try:
        if args.command == 'build':
            index.build_index()
        elif args.command == 'rebuild':
            index.build_index(force=True)
        elif args.command == 'search':
            if not args.query:
                print("Error: --query required for search command")
                return 1
            
            results = index.search(args.query, args.type, args.limit)
            
            if not results:
                print("No results found.")
                return 0
            
            for session_id, content_type, content, timestamp in results:
                print(f"\n=== Session: {session_id} ({content_type}) ===")
                if timestamp:
                    print(f"Time: {timestamp}")
                print(content[:200] + "..." if len(content) > 200 else content)
                print("-" * 50)
    
    finally:
        index.close()
    
    return 0

if __name__ == "__main__":
    exit(main())