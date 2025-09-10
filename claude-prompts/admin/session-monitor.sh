#!/bin/bash

# Session Monitor - Tracks session activity and handles cleanup

ADMIN_DIR="/home/ubuntu/claude-prompts/admin"
CURRENT_SESSION_FILE="$ADMIN_DIR/.current-session"
PID_FILE="$ADMIN_DIR/.session-monitor.pid"

# Function to cleanup session on exit
cleanup_session() {
    echo "Session monitor shutting down..."
    if [ -f "$CURRENT_SESSION_FILE" ]; then
        SESSION_ID=$(cat "$CURRENT_SESSION_FILE")
        SESSION_FILE="$ADMIN_DIR/session-$SESSION_ID.md"
        
        if [ -f "$SESSION_FILE" ]; then
            # Update session with automatic termination
            END_TIME=$(date +%H:%M)
            sed -i "s/\[ONGOING\]/$END_TIME (auto-terminated)/g" "$SESSION_FILE"
            
            # Add termination note
            cat >> "$SESSION_FILE" << EOF

## Session Auto-Terminated
**Terminated at:** $(date '+%Y-%m-%d %H:%M:%S')
**Reason:** System logout or session timeout detected

---
*Session automatically closed by session monitor*
EOF
        fi
        
        # Clean up current session marker
        rm -f "$CURRENT_SESSION_FILE"
    fi
    
    # Remove PID file
    rm -f "$PID_FILE"
    exit 0
}

# Set up signal handlers
trap cleanup_session SIGTERM SIGINT SIGHUP EXIT

# Store PID for monitoring
echo $$ > "$PID_FILE"

# Monitor session activity
while true; do
    # Check if current session still exists
    if [ ! -f "$CURRENT_SESSION_FILE" ]; then
        echo "No active session found, exiting monitor"
        exit 0
    fi
    
    # Check for user logout indicators
    if ! who | grep -q "$(whoami)"; then
        echo "User logout detected, cleaning up session"
        cleanup_session
    fi
    
    # Update session heartbeat
    SESSION_ID=$(cat "$CURRENT_SESSION_FILE" 2>/dev/null)
    if [ -n "$SESSION_ID" ]; then
        HEARTBEAT_FILE="$ADMIN_DIR/.session-$SESSION_ID-heartbeat"
        date > "$HEARTBEAT_FILE"
    fi
    
    # Sleep for 30 seconds
    sleep 30
done