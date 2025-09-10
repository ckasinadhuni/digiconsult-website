#!/bin/bash

# Terminal Session Recorder for Claude
# Records all terminal output during Claude sessions

ADMIN_DIR="/home/ubuntu/claude-prompts/admin"
CURRENT_SESSION_FILE="$ADMIN_DIR/.current-session"

if [ ! -f "$CURRENT_SESSION_FILE" ]; then
    echo "No active session found for terminal recording"
    exit 1
fi

SESSION_ID=$(cat "$CURRENT_SESSION_FILE")
TRANSCRIPT_FILE="$ADMIN_DIR/terminal-$SESSION_ID.txt"

# Start recording terminal session
echo "Starting terminal recording for session: $SESSION_ID"
echo "Output will be saved to: $TRANSCRIPT_FILE"
echo "Use 'exit' or Ctrl+D to stop recording"

# Use script command to record terminal session
script -f -q "$TRANSCRIPT_FILE"

# When script exits, process the terminal log
echo "Terminal recording ended. Processing log..."

# Create a cleaned version of the terminal log
CLEAN_TRANSCRIPT="$ADMIN_DIR/terminal-$SESSION_ID-clean.txt"

# Remove terminal control characters and clean up
cat "$TRANSCRIPT_FILE" | \
    sed 's/\x1b\[[0-9;]*m//g' | \
    sed 's/\x1b\[[0-9;]*[A-Za-z]//g' | \
    sed '/^Script started/d' | \
    sed '/^Script done/d' > "$CLEAN_TRANSCRIPT"

echo "✓ Clean terminal log saved: $CLEAN_TRANSCRIPT"

# Optionally append terminal log to session file
SESSION_FILE="$ADMIN_DIR/session-$SESSION_ID.md"
if [ -f "$SESSION_FILE" ]; then
    cat >> "$SESSION_FILE" << EOF

## Terminal Session Log
**Terminal Recording:** \`terminal-$SESSION_ID-clean.txt\`

### Key Terminal Commands
\`\`\`bash
$(grep -E '^[^#]*\$' "$CLEAN_TRANSCRIPT" | head -20)
\`\`\`

EOF
    echo "✓ Terminal summary added to session file"
fi