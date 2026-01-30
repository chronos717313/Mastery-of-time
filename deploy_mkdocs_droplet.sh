#!/bin/bash
#
# MkDocs Deployment Script for DigitalOcean Droplet (Ubuntu/Debian)
# Usage:
#   1. Upload this script and your project to the droplet
#   2. Run: chmod +x deploy_mkdocs_droplet.sh
#   3. Run: sudo ./deploy_mkdocs_droplet.sh
#
# This will:
# - Install Python 3 and dependencies
# - Install MkDocs with Material theme
# - Set up systemd service for auto-start
# - Configure nginx as reverse proxy (optional)
# - Set up firewall rules

set -e  # Exit on any error

echo "=========================================="
echo "MkDocs Deployment Script for DO Droplet"
echo "=========================================="
echo ""

# Configuration
PROJECT_DIR="/opt/tmt-wiki"
SERVICE_USER="mkdocs"
PORT=8000
DOMAIN="${DOMAIN:-}"  # Set DOMAIN env var before running for nginx setup

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

# Update system
echo -e "${GREEN}[1/8] Updating system packages...${NC}"
apt-get update
apt-get upgrade -y

# Install Python 3 and pip
echo -e "${GREEN}[2/8] Installing Python 3 and pip...${NC}"
apt-get install -y python3 python3-pip python3-venv git

# Create service user
echo -e "${GREEN}[3/8] Creating service user...${NC}"
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd -r -s /bin/bash -d "$PROJECT_DIR" -m "$SERVICE_USER"
    echo "Created user: $SERVICE_USER"
else
    echo "User $SERVICE_USER already exists"
fi

# Create project directory
echo -e "${GREEN}[4/8] Setting up project directory...${NC}"
mkdir -p "$PROJECT_DIR"

# Check if we're running from the project directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -f "$SCRIPT_DIR/docs/wiki/mkdocs.yml" ]; then
    echo "Copying project files from current directory..."
    cp -r "$SCRIPT_DIR/docs/wiki"/* "$PROJECT_DIR/"

    # Also copy scripts directory if it exists (for requirements.txt)
    if [ -d "$SCRIPT_DIR/scripts" ]; then
        echo "Copying scripts directory..."
        mkdir -p "$PROJECT_DIR/../scripts"
        cp -r "$SCRIPT_DIR/scripts" "$PROJECT_DIR/../"
    fi
else
    echo -e "${YELLOW}Warning: mkdocs.yml not found in expected location${NC}"
    echo "You'll need to manually copy your wiki files to $PROJECT_DIR"
    echo "Press Enter to continue or Ctrl+C to cancel..."
    read
fi

# Create Python virtual environment
echo -e "${GREEN}[5/8] Setting up Python virtual environment...${NC}"
cd "$PROJECT_DIR"
python3 -m venv venv
source venv/bin/activate

# Install MkDocs and dependencies
echo "Installing MkDocs and Material theme..."
pip install --upgrade pip
pip install mkdocs mkdocs-material pymdown-extensions

# Install project dependencies from requirements.txt if it exists
if [ -f "$SCRIPT_DIR/scripts/requirements.txt" ]; then
    echo "Installing project dependencies from requirements.txt..."
    pip install -r "$SCRIPT_DIR/scripts/requirements.txt"
elif [ -f "$PROJECT_DIR/../scripts/requirements.txt" ]; then
    echo "Installing project dependencies from requirements.txt..."
    pip install -r "$PROJECT_DIR/../scripts/requirements.txt"
else
    echo -e "${YELLOW}No requirements.txt found, installing common scientific packages...${NC}"
    pip install numpy scipy matplotlib astropy
fi

# Set ownership
chown -R "$SERVICE_USER:$SERVICE_USER" "$PROJECT_DIR"

# Create systemd service
echo -e "${GREEN}[6/8] Creating systemd service...${NC}"
cat > /etc/systemd/system/mkdocs.service << EOF
[Unit]
Description=MkDocs Documentation Server
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/mkdocs serve --dev-addr 0.0.0.0:$PORT
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
systemctl daemon-reload
systemctl enable mkdocs.service
systemctl start mkdocs.service

echo -e "${GREEN}MkDocs service started!${NC}"
sleep 2
systemctl status mkdocs.service --no-pager

# Configure firewall
echo -e "${GREEN}[7/8] Configuring firewall...${NC}"
if command -v ufw &> /dev/null; then
    ufw allow ssh
    ufw allow $PORT/tcp
    echo "y" | ufw enable
    echo "Firewall configured (port $PORT opened)"
else
    echo -e "${YELLOW}UFW not found, skipping firewall configuration${NC}"
fi

# Optional: Install and configure nginx
echo -e "${GREEN}[8/8] Nginx setup (optional)...${NC}"
if [ -n "$DOMAIN" ]; then
    echo "Setting up nginx reverse proxy for domain: $DOMAIN"
    apt-get install -y nginx certbot python3-certbot-nginx

    cat > /etc/nginx/sites-available/mkdocs << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

    ln -sf /etc/nginx/sites-available/mkdocs /etc/nginx/sites-enabled/
    nginx -t && systemctl reload nginx

    # Allow HTTP/HTTPS through firewall
    if command -v ufw &> /dev/null; then
        ufw allow 'Nginx Full'
    fi

    echo ""
    echo -e "${GREEN}Nginx configured!${NC}"
    echo "To enable HTTPS with Let's Encrypt, run:"
    echo "  sudo certbot --nginx -d $DOMAIN"
else
    echo -e "${YELLOW}No DOMAIN specified, skipping nginx setup${NC}"
    echo "If you want nginx later, run:"
    echo "  DOMAIN=your-domain.com sudo ./deploy_mkdocs_droplet.sh"
fi

# Display results
echo ""
echo "=========================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "MkDocs is now running at:"
if [ -n "$DOMAIN" ]; then
    echo "  http://$DOMAIN"
else
    DROPLET_IP=$(hostname -I | awk '{print $1}')
    echo "  http://$DROPLET_IP:$PORT"
fi
echo ""
echo "Service management commands:"
echo "  sudo systemctl status mkdocs   # Check status"
echo "  sudo systemctl restart mkdocs  # Restart service"
echo "  sudo systemctl stop mkdocs     # Stop service"
echo "  sudo systemctl start mkdocs    # Start service"
echo "  sudo journalctl -u mkdocs -f   # View logs"
echo ""
echo "Project location: $PROJECT_DIR"
echo "Edit content in: $PROJECT_DIR/docs/"
echo "After changes run: sudo systemctl restart mkdocs"
echo ""
