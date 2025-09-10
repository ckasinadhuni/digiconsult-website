#!/bin/bash

# Auto Session Logger for Claude
# Creates a new session log automatically when Claude starts

CLAUDE_PROMPTS_DIR="/home/ubuntu/claude-prompts"
ADMIN_DIR="$CLAUDE_PROMPTS_DIR/admin"
TEMPLATE_FILE="$ADMIN_DIR/session-log-template.md"

# Create timestamp for session
TIMESTAMP=$(date +%Y-%m-%d-%H%M)
SESSION_FILE="$ADMIN_DIR/session-$TIMESTAMP.md"

# Check if directories exist
if [ ! -d "$CLAUDE_PROMPTS_DIR" ]; then
    echo "Claude prompts directory not found: $CLAUDE_PROMPTS_DIR"
    exit 1
fi

if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Session template not found: $TEMPLATE_FILE"
    exit 1
fi

# Copy template to new session file
cp "$TEMPLATE_FILE" "$SESSION_FILE"

# Replace placeholders with actual values
sed -i "s/\[YYYY-MM-DD\]/$(date +%Y-%m-%d)/g" "$SESSION_FILE"
sed -i "s/\[HH:MM - HH:MM\]/$(date +%H:%M) - [ONGOING]/g" "$SESSION_FILE"

# Create a simple session start entry
cat >> "$SESSION_FILE" << EOF

## Session Auto-Started
**Started at:** $(date '+%Y-%m-%d %H:%M:%S')
**Working Directory:** $(pwd)
**Session ID:** $TIMESTAMP

---
EOF

echo "✓ New Claude session created: $SESSION_FILE"
echo "✓ Session ID: $TIMESTAMP"

# Store session ID for potential later use
echo "$TIMESTAMP" > "$ADMIN_DIR/.current-session"

# Start file watcher in background
if [ ! -f "$ADMIN_DIR/.file-watcher.pid" ]; then
    nohup python3 "$ADMIN_DIR/file-watcher.py" > "$ADMIN_DIR/file-watcher.log" 2>&1 &
    echo $! > "$ADMIN_DIR/.file-watcher.pid"
    echo "✓ File watcher started"
fi

# Start session monitor in background
if [ ! -f "$ADMIN_DIR/.session-monitor.pid" ]; then
    nohup "$ADMIN_DIR/session-monitor.sh" > "$ADMIN_DIR/session-monitor.log" 2>&1 &
    echo "✓ Session monitor started"
fi