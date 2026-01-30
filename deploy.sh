#!/bin/bash
# TMT Wiki - One-click deployment for Digital Ocean
# Domain: mastery-of-time.org
# Repo: https://github.com/chronos717313/Mastery-of-time
#
# Usage: curl -sSL https://raw.githubusercontent.com/chronos717313/Mastery-of-time/main/deploy.sh | sudo bash

set -e

DOMAIN="mastery-of-time.org"
REPO="https://github.com/chronos717313/Mastery-of-time.git"
BRANCH="main"
DEPLOY_DIR="/opt/tmt-wiki"

echo "=== TMT Wiki Deployment ==="
echo "Domain: $DOMAIN"
echo "Repo: $REPO"
echo ""

# 1. Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "[1/5] Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
else
    echo "[1/5] Docker already installed"
fi

# 2. Install docker-compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo "[2/5] Installing docker-compose..."
    apt-get update && apt-get install -y docker-compose
else
    echo "[2/5] docker-compose already installed"
fi

# 3. Clone or update repo
echo "[3/5] Setting up repository..."
if [ -d "$DEPLOY_DIR" ]; then
    cd "$DEPLOY_DIR"
    git fetch origin
    git checkout $BRANCH
    git pull origin $BRANCH
else
    git clone -b $BRANCH "$REPO" "$DEPLOY_DIR"
    cd "$DEPLOY_DIR"
fi

# 4. Start with Docker
echo "[4/5] Starting MkDocs container..."
docker-compose down 2>/dev/null || true
docker-compose up -d

# Wait for container to be ready
echo "Waiting for container to start..."
sleep 10

# 5. Setup Nginx + SSL
echo "[5/5] Configuring Nginx and SSL..."
apt-get install -y nginx certbot python3-certbot-nginx

cat > /etc/nginx/sites-available/tmt-wiki << 'NGINX'
server {
    listen 80;
    server_name mastery-of-time.org www.mastery-of-time.org;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX

ln -sf /etc/nginx/sites-available/tmt-wiki /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

# Get SSL certificate
echo ""
echo "Getting SSL certificate..."
certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN --redirect || {
    echo "SSL setup failed - you can run manually later:"
    echo "  certbot --nginx -d $DOMAIN -d www.$DOMAIN"
}

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "Wiki: https://$DOMAIN"
echo ""
echo "Commands:"
echo "  cd $DEPLOY_DIR && docker-compose logs -f  # View logs"
echo "  cd $DEPLOY_DIR && git pull && docker-compose restart  # Update"
echo ""
