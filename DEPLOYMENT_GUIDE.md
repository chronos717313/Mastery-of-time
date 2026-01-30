# MkDocs Deployment Guide for DigitalOcean Droplet

This guide will help you deploy the TMT Wiki documentation on a DigitalOcean droplet.

## Resource Requirements

The MkDocs documentation server is very lightweight:

- **Recommended**: $6/month Basic Droplet
  - 1 GB RAM
  - 1 vCPU
  - 25 GB SSD
  - Ubuntu 22.04 LTS

- **Minimum**: Even $4/month droplet would work (if available)

## Quick Start

### 1. Create DigitalOcean Droplet

1. Log into DigitalOcean
2. Click "Create" → "Droplets"
3. Choose **Ubuntu 22.04 LTS**
4. Select **Basic Plan** ($6/month)
5. Choose a datacenter region close to your audience
6. Add your SSH key
7. Create droplet

### 2. Upload Project Files

From your local machine, upload the project:

```bash
# Replace YOUR_DROPLET_IP with your actual IP
scp -r Mastery-of-time root@YOUR_DROPLET_IP:/root/
```

Or use Git:

```bash
ssh root@YOUR_DROPLET_IP
git clone https://github.com/chronos717313/Mastery-of-time.git
cd Mastery-of-time
```

### 3. Run Deployment Script

```bash
ssh root@YOUR_DROPLET_IP
cd Mastery-of-time
chmod +x deploy_mkdocs_droplet.sh
sudo ./deploy_mkdocs_droplet.sh
```

### 4. Access Your Site

After deployment completes, access your documentation at:

```
http://YOUR_DROPLET_IP:8000
```

## Optional: Configure Domain Name

### With Nginx Reverse Proxy

If you have a domain name, run the script with the DOMAIN environment variable:

```bash
DOMAIN=tmt-wiki.example.com sudo ./deploy_mkdocs_droplet.sh
```

This will:
- Install nginx as a reverse proxy
- Configure it for your domain
- Set up port 80 (HTTP)

### Add HTTPS with Let's Encrypt (Recommended)

After nginx setup, run:

```bash
sudo certbot --nginx -d tmt-wiki.example.com
```

This will:
- Get a free SSL certificate from Let's Encrypt
- Configure HTTPS automatically
- Set up auto-renewal

**Don't forget to:**
- Point your domain's DNS A record to your droplet's IP address
- Wait 5-15 minutes for DNS propagation

## Managing the Service

### Check Status
```bash
sudo systemctl status mkdocs
```

### View Logs
```bash
sudo journalctl -u mkdocs -f
```

### Restart Service
```bash
sudo systemctl restart mkdocs
```

### Stop Service
```bash
sudo systemctl stop mkdocs
```

### Start Service
```bash
sudo systemctl start mkdocs
```

## Updating Content

All content is located in `/opt/tmt-wiki/docs/`

### Edit Files
```bash
sudo nano /opt/tmt-wiki/docs/index.md
```

### After Making Changes
```bash
sudo systemctl restart mkdocs
```

### Or Use Git to Update
```bash
cd /root/Mastery-of-time
git pull origin main
sudo cp -r docs/wiki/* /opt/tmt-wiki/
sudo systemctl restart mkdocs
```

## Firewall Configuration

The script automatically configures UFW (Uncomplicated Firewall):

- **Port 22 (SSH)**: Open (required for access)
- **Port 8000 (MkDocs)**: Open (if no nginx)
- **Ports 80/443 (HTTP/HTTPS)**: Open (if using nginx)

### Check Firewall Status
```bash
sudo ufw status
```

## Monitoring

### Check Disk Usage
```bash
df -h
```

### Check Memory Usage
```bash
free -h
```

### Check Service Resource Usage
```bash
top
# Then press 'u' and type 'mkdocs' to filter
```

## Backup Strategy

### Backup Content
```bash
# Create backup
sudo tar -czf ~/tmt-wiki-backup-$(date +%Y%m%d).tar.gz /opt/tmt-wiki

# Download to local machine
scp root@YOUR_DROPLET_IP:~/tmt-wiki-backup-*.tar.gz ./
```

### Automated Backups with Cron
```bash
# Add to crontab
sudo crontab -e

# Add this line (daily backup at 2 AM):
0 2 * * * tar -czf /root/backups/tmt-wiki-$(date +\%Y\%m\%d).tar.gz /opt/tmt-wiki
```

## Troubleshooting

### Service Won't Start

Check logs:
```bash
sudo journalctl -u mkdocs -xe
```

Common issues:
- Port already in use: Change PORT in the service file
- Python module missing: Reinstall dependencies
- Permission issues: Check ownership of `/opt/tmt-wiki`

### Site Not Accessible

Check firewall:
```bash
sudo ufw status
```

Check if service is running:
```bash
sudo systemctl status mkdocs
```

Test locally on droplet:
```bash
curl http://localhost:8000
```

### High Memory Usage

MkDocs itself uses minimal memory (~50-100MB). If memory is high:
- Check for runaway processes: `htop`
- Restart the service: `sudo systemctl restart mkdocs`
- Consider upgrading to next tier droplet

## Cost Optimization

For a documentation site with moderate traffic:
- **$6/month droplet**: Good for 1000+ visitors/day
- **Bandwidth**: 1TB/month included (plenty for docs)
- **Backups**: +20% ($1.20/month) - recommended

Total monthly cost: **~$7.20/month**

## Security Best Practices

1. **Keep System Updated**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Use SSH Keys** (not passwords)
   ```bash
   sudo nano /etc/ssh/sshd_config
   # Set: PasswordAuthentication no
   sudo systemctl restart sshd
   ```

3. **Enable Automatic Security Updates**
   ```bash
   sudo apt install unattended-upgrades
   sudo dpkg-reconfigure -plow unattended-upgrades
   ```

4. **Monitor Failed Login Attempts**
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   ```

5. **Use HTTPS** (with Let's Encrypt - it's free!)

## Performance Tips

### Enable Gzip Compression (Nginx)

Add to nginx config:
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml;
```

### Enable Browser Caching (Nginx)

Add to nginx config:
```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Use CDN (Optional)

For global audience, consider using Cloudflare's free CDN:
1. Sign up at cloudflare.com
2. Add your domain
3. Update nameservers
4. Enable "Always Use HTTPS"

## Support

For issues related to:
- **MkDocs**: https://www.mkdocs.org/
- **Material Theme**: https://squidfunk.github.io/mkdocs-material/
- **DigitalOcean**: https://docs.digitalocean.com/
- **This Project**: https://github.com/chronos717313/Mastery-of-time/issues
