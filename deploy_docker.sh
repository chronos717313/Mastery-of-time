#!/bin/bash
#
# Docker-based Deployment Script for DigitalOcean Droplet
# Usage:
#   1. SSH to droplet: ssh root@your-droplet-ip
#   2. Clone repo: git clone https://github.com/chronos717313/Mastery-of-time.git
#   3. cd Mastery-of-time
#   4. chmod +x deploy_docker.sh
#   5. sudo ./deploy_docker.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "TMT Wiki - Docker Deployment"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

# Step 1: Install Docker if not present
echo -e "${GREEN}[1/3] Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    apt-get update
    apt-get install -y ca-certificates curl gnupg
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    systemctl enable docker
    systemctl start docker
    echo -e "${GREEN}Docker installed successfully${NC}"
else
    echo "Docker already installed: $(docker --version)"
fi

# Step 2: Configure firewall
echo -e "${GREEN}[2/3] Configuring firewall...${NC}"
if command -v ufw &> /dev/null; then
    ufw allow ssh
    ufw allow 80/tcp
    echo "y" | ufw enable || true
    echo "Firewall configured (port 80 open)"
else
    echo -e "${YELLOW}UFW not found, skipping firewall${NC}"
fi

# Step 3: Start container
echo -e "${GREEN}[3/3] Starting Docker container...${NC}"
cd "$PROJECT_DIR"

docker compose up -d

# Wait and show status
sleep 5
docker compose ps

DROPLET_IP=$(hostname -I | awk '{print $1}')

echo ""
echo "=========================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "Site available at:"
echo "  http://$DROPLET_IP"
echo ""
echo "Management commands:"
echo "  docker compose logs -f       # View logs"
echo "  docker compose restart       # Restart"
echo "  docker compose down          # Stop"
echo ""
echo "To update content:"
echo "  git pull && docker compose restart"
echo ""
