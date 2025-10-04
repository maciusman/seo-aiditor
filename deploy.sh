#!/bin/bash
# Auto-deployment script for SEO AIditor
# Triggered by GitHub webhook on git push

set -e  # Exit on error

DEPLOY_DIR="/var/www/seo-aiditor"
LOG_FILE="$DEPLOY_DIR/deploy.log"

echo "=======================================" >> "$LOG_FILE"
echo "Deployment started at $(date)" >> "$LOG_FILE"
echo "=======================================" >> "$LOG_FILE"

# Navigate to project directory
cd "$DEPLOY_DIR"

# Fetch latest changes from GitHub
echo "Fetching from GitHub..." >> "$LOG_FILE"
git fetch origin master 2>&1 >> "$LOG_FILE"

# Check if there are new commits
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/master)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "Already up to date. No deployment needed." >> "$LOG_FILE"
    exit 0
fi

# Pull latest changes
echo "Pulling changes from origin/master..." >> "$LOG_FILE"
git pull origin master 2>&1 >> "$LOG_FILE"

# Restart application service
echo "Restarting seoaiditor service..." >> "$LOG_FILE"
sudo systemctl restart seoaiditor 2>&1 >> "$LOG_FILE"

# Wait for service to stabilize
sleep 2

# Check service status
if systemctl is-active --quiet seoaiditor; then
    echo "✓ Deployment successful! Service is running." >> "$LOG_FILE"
    echo "  Deployed commit: $(git log -1 --oneline)" >> "$LOG_FILE"
else
    echo "✗ Deployment failed! Service is not running." >> "$LOG_FILE"
    systemctl status seoaiditor >> "$LOG_FILE" 2>&1
    exit 1
fi

echo "=======================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

exit 0
