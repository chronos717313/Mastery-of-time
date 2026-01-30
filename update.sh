#!/bin/bash
# Quick update script for TMT Wiki
# Run after pushing changes to GitHub
# Usage: ./update.sh

set -e

cd /opt/tmt-wiki
echo "Pulling latest changes..."
git pull origin main
echo "Restarting MkDocs container..."
docker-compose restart
echo "Done! Wiki updated at https://mastery-of-time.org"
