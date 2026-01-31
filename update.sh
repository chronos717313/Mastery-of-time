#!/bin/bash
#
# Quick update script - pull latest code and restart containers
# Usage: ./update.sh
#
# Run from the project directory on the droplet

set -e

GREEN='\033[0;32m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo -e "${GREEN}Pulling latest changes...${NC}"
git fetch --all
git reset --hard origin/main

echo -e "${GREEN}Restarting containers...${NC}"
docker compose restart

echo -e "${GREEN}Done! Site updated.${NC}"
echo ""
echo "Recent logs:"
docker compose logs --tail=10
