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
docker compose down
docker compose up -d

echo -e "${GREEN}Applying nginx configuration...${NC}"
sleep 5  # Wait for containers to fully start
docker exec tmt-nginx sh -c 'cat > /config/nginx/site-confs/default.conf << '\''EOF'\''
## Version 2025/07/18 - Changelog: https://github.com/linuxserver/docker-swag/commits/master/root/defaults/nginx/site-confs/default.conf.sample

# redirect all traffic to https
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    location / {
        return 301 https://$host$request_uri;
    }
}

# main server block
server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;

    server_name mastery-of-time.org www.mastery-of-time.org;

    include /config/nginx/ssl.conf;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src '\''self'\'' http: https: data: blob: '\''unsafe-inline'\''" always;

    # Proxy to MkDocs
    location / {
        proxy_pass http://mkdocs:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # ACME challenge for Let'\''s Encrypt
    location /.well-known/acme-challenge/ {
        alias /config/letsencrypt/acme-challenge/;
    }

    # deny access to .htaccess/.htpasswd files
    location ~ /\.ht {
        deny all;
    }
}

# enable subdomain method reverse proxy confs
include /config/nginx/proxy-confs/*.subdomain.conf;
EOF'

echo -e "${GREEN}Reloading nginx...${NC}"
docker exec tmt-nginx nginx -s reload

echo -e "${GREEN}Done! Site updated with HTTPS.${NC}"
echo ""
echo "Recent logs:"
docker compose logs --tail=10
