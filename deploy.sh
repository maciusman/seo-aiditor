#!/bin/bash
# Auto-deployment script for SEO AIditor
# Triggered by GitHub webhook on git push

DEPLOY_DIR="/var/www/seo-aiditor"
LOG_FILE="$DEPLOY_DIR/deploy.log"

# Function for logging with timestamp (full path to date)
log() {
    echo "[$(/bin/date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Function to run command with timeout (full path)
run_with_timeout() {
    local timeout_sec=$1
    shift
    /usr/bin/timeout "$timeout_sec" "$@"
    return $?
}

log "======================================="
log "Deployment started"
log "======================================="

# Navigate to project directory
cd "$DEPLOY_DIR" || {
    log "ERROR: Cannot cd to $DEPLOY_DIR"
    exit 1
}

# Test GitHub connectivity (full path to ping)
log "Testing GitHub connectivity..."
if ! run_with_timeout 5 /bin/ping -c 1 github.com &> /dev/null; then
    log "WARNING: Cannot ping github.com (may be blocked, continuing anyway)"
fi

# Check current commit (full path to git)
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
        # Kill any hanging git processes
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

# Restart application service (no sudo needed - script runs as root)
log "Restarting seoaiditor service..."
if /bin/systemctl restart seoaiditor >> "$LOG_FILE" 2>&1; then
    log "✓ Service restart initiated"
else
    log "ERROR: Failed to restart service"
    exit 1
fi

# Wait for service to stabilize
/bin/sleep 3

# Check service status
if /bin/systemctl is-active --quiet seoaiditor; then
    log "✓ Deployment successful! Service is running."
    log "  Deployed commit: $(/usr/bin/git log -1 --oneline)"
else
    log "✗ Deployment failed! Service is not running."
    /bin/systemctl status seoaiditor >> "$LOG_FILE" 2>&1
    exit 1
fi

log "======================================="
exit 0
