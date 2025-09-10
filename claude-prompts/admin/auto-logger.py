#!/usr/bin/env python3

"""
Automatic Claude Code Logger
Captures prompts and responses using Claude Code hooks
"""

import json
import sys
import os
import datetime
from pathlib import Path

# Configuration
ADMIN_DIR = Path("/home/ubuntu/claude-prompts/admin")
CURRENT_SESSION_FILE = ADMIN_DIR / ".current-session"

def get_current_session_file():
    """Get the current session file path"""
    if not CURRENT_SESSION_FILE.exists():
        return None
    
    session_id = CURRENT_SESSION_FILE.read_text().strip()
    return ADMIN_DIR / f"session-{session_id}.md"

def log_user_prompt(prompt_text):
    """Log user prompt to current session"""
    session_file = get_current_session_file()
    if not session_file or not session_file.exists():
        return
    
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Read current content
    content = session_file.read_text()
    
    # Find insertion point (before "## Files Created/Modified" or at end)
    insert_markers = [
        "## Files Created/Modified",
        "## Key Learnings", 
        "## Session Rating",
        "## Session Ended"
    ]
    
    insert_pos = len(content)
    for marker in insert_markers:
        pos = content.find(marker)
        if pos != -1:
            insert_pos = min(insert_pos, pos)
    
    # Create prompt entry
    prompt_entry = f"""
### Prompt ({timestamp})
**Command/Request:**
```
{prompt_text}
```

**Output/Response:**
```
[Response will be captured automatically]
```

**Notes:** Automatically logged

---

"""
    
    # Insert the prompt
    new_content = content[:insert_pos] + prompt_entry + content[insert_pos:]
    session_file.write_text(new_content)

def log_tool_use(tool_name, parameters, result):
    """Log tool usage to current session"""
    session_file = get_current_session_file()
    if not session_file or not session_file.exists():
        return
    
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Read current content and find the last prompt entry to update
    content = session_file.read_text()
    
    # Look for the last "[Response will be captured automatically]" placeholder
    placeholder = "[Response will be captured automatically]"
    last_placeholder_pos = content.rfind(placeholder)
    
    if last_placeholder_pos != -1:
        # Replace placeholder with actual tool usage
        tool_info = f"Tool: {tool_name}\nParameters: {json.dumps(parameters, indent=2)}\nResult: {str(result)[:500]}..."
        
        new_content = (
            content[:last_placeholder_pos] + 
            tool_info + 
            content[last_placeholder_pos + len(placeholder):]
        )
        session_file.write_text(new_content)

def main():
    """Main entry point for hook execution"""
    if len(sys.argv) < 2:
        return
    
    hook_type = sys.argv[1]
    
    try:
        if hook_type == "user_prompt_submit":
            # Read prompt from stdin
            prompt_text = sys.stdin.read().strip()
            log_user_prompt(prompt_text)
            
        elif hook_type == "post_tool_use":
            # Tool information passed as arguments
            tool_name = sys.argv[2] if len(sys.argv) > 2 else "unknown"
            # For now, just log that a tool was used
            session_file = get_current_session_file()
            if session_file and session_file.exists():
                content = session_file.read_text()
                placeholder = "[Response will be captured automatically]"
                if placeholder in content:
                    tool_info = f"Tool used: {tool_name} at {datetime.datetime.now().strftime('%H:%M:%S')}"
                    content = content.replace(placeholder, tool_info, 1)
                    session_file.write_text(content)
                    
    except Exception as e:
        # Log errors to a debug file
        debug_file = ADMIN_DIR / "auto-logger-debug.log"
        with open(debug_file, "a") as f:
            f.write(f"{datetime.datetime.now()}: Error in auto-logger: {str(e)}\n")

if __name__ == "__main__":
    main()