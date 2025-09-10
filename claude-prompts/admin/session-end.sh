#!/bin/bash

# Session End Script for Claude
# Updates the current session with end time and summary

ADMIN_DIR="/home/ubuntu/claude-prompts/admin"
CURRENT_SESSION_FILE="$ADMIN_DIR/.current-session"

if [ ! -f "$CURRENT_SESSION_FILE" ]; then
    echo "No active session found."
    exit 1
fi

SESSION_ID=$(cat "$CURRENT_SESSION_FILE")
SESSION_FILE="$ADMIN_DIR/session-$SESSION_ID.md"

if [ ! -f "$SESSION_FILE" ]; then
    echo "Session file not found: $SESSION_FILE"
    exit 1
fi

# Update end time in the session file
END_TIME=$(date +%H:%M)
sed -i "s/\[ONGOING\]/$END_TIME/g" "$SESSION_FILE"

# Calculate session duration
START_TIME=$(grep "Started at:" "$SESSION_FILE" | cut -d' ' -f5)
if [ -n "$START_TIME" ]; then
    START_SECONDS=$(date -d "$START_TIME" +%s 2>/dev/null)
    END_SECONDS=$(date +%s)
    if [ -n "$START_SECONDS" ]; then
        DURATION_MINUTES=$(( (END_SECONDS - START_SECONDS) / 60 ))
        HOURS=$(( DURATION_MINUTES / 60 ))
        MINUTES=$(( DURATION_MINUTES % 60 ))
        sed -i "s/\[X hours Y minutes\]/$HOURS hours $MINUTES minutes/g" "$SESSION_FILE"
    fi
fi

# Add session end marker
cat >> "$SESSION_FILE" << EOF

## Session Ended
**Ended at:** $(date '+%Y-%m-%d %H:%M:%S')
**Total Duration:** $HOURS hours $MINUTES minutes

---
*Session automatically logged by Claude auto-session system*
EOF

echo "✓ Session ended and logged: $SESSION_FILE"
echo "✓ Duration: $HOURS hours $MINUTES minutes"

# Clean up current session marker
rm -f "$CURRENT_SESSION_FILE"