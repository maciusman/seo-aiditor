#!/bin/bash
# Smart Auto-deployment script for SEO AIditor
# Waits for active audits to complete before restarting

DEPLOY_DIR="/var/www/seo-aiditor"
LOG_FILE="$DEPLOY_DIR/deploy.log"
MAX_WAIT_TIME=600  # 10 minutes max wait for audits to complete

# Function for logging with timestamp
log() {
    echo "[$(/bin/date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Function to run command with timeout
run_with_timeout() {
    local timeout_sec=$1
    shift
    /usr/bin/timeout "$timeout_sec" "$@"
    return $?
}

# Function to check if there are active audit requests
check_active_audits() {
    # Check if any gunicorn worker is processing /api/audit-stream
    # This indicates an active audit in progress
    local active_count=$(/bin/ps aux | /bin/grep -E "gunicorn.*worker" | /bin/grep -v grep | /usr/bin/wc -l)

    # Additionally check for recent activity in logs (last 30 seconds)
    local recent_audit=$(/usr/bin/journalctl -u seoaiditor.service --since "30 seconds ago" | /bin/grep -E "\[.*%\]|STAGE" | /usr/bin/wc -l)

    if [ "$recent_audit" -gt 0 ]; then
        return 0  # Active audit found
    else
        return 1  # No active audits
    fi
}

# Function to wait for active audits to complete
wait_for_audits_completion() {
    local wait_time=0
    local check_interval=10  # Check every 10 seconds

    log "Checking for active audits before restart..."

    while check_active_audits; do
        if [ $wait_time -ge $MAX_WAIT_TIME ]; then
            log "WARNING: Max wait time ($MAX_WAIT_TIME seconds) reached. Proceeding with restart anyway."
            return 1
        fi

        log "Active audit detected. Waiting for completion... (${wait_time}s / ${MAX_WAIT_TIME}s)"
        /bin/sleep $check_interval
        wait_time=$((wait_time + check_interval))
    done

    if [ $wait_time -gt 0 ]; then
        log "✓ All audits completed after ${wait_time} seconds. Safe to restart."
    else
        log "✓ No active audits detected. Safe to restart."
    fi

    return 0
}

log "======================================="
log "Smart Deployment started"
log "======================================="

# Navigate to project directory
cd "$DEPLOY_DIR" || {
    log "ERROR: Cannot cd to $DEPLOY_DIR"
    exit 1
}

# Test GitHub connectivity
log "Testing GitHub connectivity..."
if ! run_with_timeout 5 /bin/ping -c 1 github.com &> /dev/null; then
    log "WARNING: Cannot ping github.com (may be blocked, continuing anyway)"
fi

# Check current commit
BEFORE_COMMIT=$(/usr/bin/git rev-parse HEAD 2>/dev/null || echo "unknown")
log "Current commit: $BEFORE_COMMIT"

# Fetch latest changes with timeout
log "Fetching from GitHub (timeout: 30s)..."
if run_with_timeout 30 /usr/bin/git fetch origin master >> "$LOG_FILE" 2>&1; then
    log "✓ Git fetch completed"
else
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 124 ]; then
        log "ERROR: git fetch timed out after 30s"
        /usr/bin/pkill -9 git 2>/dev/null
        exit 1
    else
        log "WARNING: git fetch returned exit code $EXIT_CODE (continuing anyway)"
    fi
fi

# Check if there are new commits
LOCAL=$(/usr/bin/git rev-parse HEAD)
REMOTE=$(/usr/bin/git rev-parse origin/master)

if [ "$LOCAL" = "$REMOTE" ]; then
    log "Already up to date. No deployment needed."
    log "======================================="
    exit 0
fi

log "New commits detected: $LOCAL -> $REMOTE"

# Pull latest changes with timeout
log "Pulling changes from origin/master (timeout: 30s)..."
if run_with_timeout 30 /usr/bin/git pull origin master >> "$LOG_FILE" 2>&1; then
    log "✓ Git pull completed"
else
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 124 ]; then
        log "ERROR: git pull timed out after 30s"
        /usr/bin/pkill -9 git 2>/dev/null
        exit 1
    else
        log "ERROR: git pull failed with exit code $EXIT_CODE"
        exit 1
    fi
fi

# Verify deployment
AFTER_COMMIT=$(/usr/bin/git rev-parse HEAD)
log "New commit: $AFTER_COMMIT"

# ==============================================================
# SMART RESTART: Wait for active audits to complete
# ==============================================================
wait_for_audits_completion

# Add small buffer after last audit completes (let response be sent)
log "Adding 5 second buffer for response transmission..."
/bin/sleep 5

# Restart application service
log "Restarting seoaiditor service (detached mode)..."

# Execute restart in background, completely detached from parent process
nohup /bin/systemctl restart seoaiditor &> /dev/null &
RESTART_PID=$!

log "✓ Service restart initiated in background (PID: $RESTART_PID)"

# Wait for service to restart and stabilize
log "Waiting 6 seconds for service to restart..."
/bin/sleep 6

# Check service status
log "Checking service status..."
if /bin/systemctl is-active --quiet seoaiditor; then
    log "✓ Smart deployment successful! Service is running."
    log "  Deployed commit: $(/usr/bin/git log -1 --oneline)"
else
    log "✗ WARNING: Service status check failed."
    log "  This may be a timing issue. Checking again in 3 seconds..."
    /bin/sleep 3
    if /bin/systemctl is-active --quiet seoaiditor; then
        log "✓ Service is now running (delayed start)."
        log "  Deployed commit: $(/usr/bin/git log -1 --oneline)"
    else
        log "✗ Deployment failed! Service is not running after 9 seconds."
        /bin/systemctl status seoaiditor &>> "$LOG_FILE"
        exit 1
    fi
fi

log "======================================="
exit 0
