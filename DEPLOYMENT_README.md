# TMT Wiki Deployment Options

Three easy ways to deploy the TMT documentation website.

## Quick Comparison

| Method | Difficulty | Time | Best For |
|--------|-----------|------|----------|
| **Automated Script** | Easy | 5 min | Production deployment on Ubuntu |
| **Docker** | Easy | 2 min | Quick local testing or any OS |
| **Manual** | Medium | 10 min | Learning or custom setup |

---

## Option 1: Automated Script (Recommended for Production)

**Best for:** DigitalOcean droplets, Ubuntu/Debian servers

### Requirements
- Ubuntu 22.04 or Debian 11+ server
- Root or sudo access
- Internet connection

### Steps

1. **Upload project to your server:**
   ```bash
   scp -r Mastery-of-time root@YOUR_SERVER_IP:/root/
   ```

2. **Run the deployment script:**
   ```bash
   ssh root@YOUR_SERVER_IP
   cd Mastery-of-time
   chmod +x deploy_mkdocs_droplet.sh
   sudo ./deploy_mkdocs_droplet.sh
   ```

3. **Access your site:**
   ```
   http://YOUR_SERVER_IP:8000
   ```

### With Custom Domain

```bash
DOMAIN=wiki.yourdomain.com sudo ./deploy_mkdocs_droplet.sh
```

Then add HTTPS:
```bash
sudo certbot --nginx -d wiki.yourdomain.com
```

**See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete documentation.**

---

## Option 2: Docker (Fastest for Testing)

**Best for:** Local development, testing, or any OS with Docker

### Requirements
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose (included with Docker Desktop)

### Steps

1. **Navigate to project directory:**
   ```bash
   cd Mastery-of-time
   ```

2. **Start the server:**
   ```bash
   docker-compose up -d
   ```

3. **Access your site:**
   ```
   http://localhost:8000
   ```

### Management Commands

```bash
# View logs
docker-compose logs -f

# Stop server
docker-compose down

# Restart server
docker-compose restart

# Rebuild (after changes)
docker-compose up -d --build
```

### Deploy Docker on DigitalOcean

1. Create Ubuntu droplet with Docker pre-installed
2. Upload project:
   ```bash
   scp -r Mastery-of-time root@YOUR_SERVER_IP:/root/
   ```
3. Run on server:
   ```bash
   ssh root@YOUR_SERVER_IP
   cd Mastery-of-time
   docker-compose up -d
   ```

---

## Option 3: Manual Installation

**Best for:** Custom configurations, learning

### On Ubuntu/Debian

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv git

# 3. Create project directory
sudo mkdir -p /opt/tmt-wiki
cd /opt/tmt-wiki

# 4. Copy wiki files
cp -r /path/to/Mastery-of-time/docs/wiki/* .

# 5. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install MkDocs
pip install --upgrade pip
pip install mkdocs mkdocs-material pymdown-extensions

# 7. Install project dependencies
pip install -r /path/to/Mastery-of-time/scripts/requirements.txt

# 8. Run server
mkdocs serve --dev-addr 0.0.0.0:8000
```

### On Windows (Local Development)

```powershell
# 1. Install Python from python.org (3.10+)

# 2. Navigate to project
cd C:\path\to\Mastery-of-time\docs\wiki

# 3. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate

# 4. Install dependencies
pip install mkdocs mkdocs-material pymdown-extensions
pip install -r ..\..\scripts\requirements.txt

# 5. Run server
mkdocs serve
```

Access at: `http://127.0.0.1:8000`

### On macOS (Local Development)

```bash
# 1. Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python
brew install python

# 3. Navigate to project
cd ~/Mastery-of-time/docs/wiki

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install mkdocs mkdocs-material pymdown-extensions
pip install -r ../../scripts/requirements.txt

# 6. Run server
mkdocs serve
```

Access at: `http://127.0.0.1:8000`

---

## Resource Requirements

### Minimum (Development/Testing)
- **RAM:** 512 MB
- **CPU:** 1 core
- **Storage:** 5 GB
- **Cost:** Free (local) or $4-6/month (cloud)

### Recommended (Production)
- **RAM:** 1 GB
- **CPU:** 1 vCPU
- **Storage:** 10 GB SSD
- **Bandwidth:** 1 TB/month
- **Cost:** $6-12/month

### DigitalOcean Droplet Options

| Plan | RAM | vCPU | Storage | Transfer | Price |
|------|-----|------|---------|----------|-------|
| Basic | 1 GB | 1 | 25 GB | 1 TB | $6/mo |
| Basic | 2 GB | 1 | 50 GB | 2 TB | $12/mo |

**Recommendation:** Start with $6/month Basic droplet. It's plenty for 1000+ daily visitors.

---

## Next Steps After Deployment

### 1. Configure Domain (Optional but Recommended)

- Update DNS A record to point to your droplet IP
- Wait 5-15 minutes for propagation
- Redeploy with domain: `DOMAIN=wiki.example.com sudo ./deploy_mkdocs_droplet.sh`

### 2. Enable HTTPS (Recommended)

```bash
sudo certbot --nginx -d wiki.example.com
```

Free SSL certificate from Let's Encrypt, auto-renews every 90 days.

### 3. Customize Content

Edit files in:
- Production: `/opt/tmt-wiki/docs/`
- Docker: `./docs/wiki/docs/`
- Local: `./docs/wiki/docs/`

After changes:
- Production: `sudo systemctl restart mkdocs`
- Docker: `docker-compose restart`
- Local: Changes auto-reload

### 4. Set Up Backups

```bash
# Manual backup
sudo tar -czf ~/tmt-wiki-backup-$(date +%Y%m%d).tar.gz /opt/tmt-wiki

# Automated daily backups (add to crontab)
0 2 * * * tar -czf /root/backups/tmt-wiki-$(date +\%Y\%m\%d).tar.gz /opt/tmt-wiki
```

### 5. Monitor Performance

```bash
# Check service status
sudo systemctl status mkdocs

# View logs
sudo journalctl -u mkdocs -f

# Check resource usage
htop
```

---

## Troubleshooting

### Port 8000 already in use

**Solution 1:** Change port in docker-compose.yml or systemd service
```yaml
ports:
  - "8080:8000"  # Use port 8080 instead
```

**Solution 2:** Find and stop the conflicting process
```bash
sudo lsof -i :8000
sudo kill <PID>
```

### Site not accessible from internet

1. **Check firewall:**
   ```bash
   sudo ufw status
   sudo ufw allow 8000/tcp
   ```

2. **Check service is running:**
   ```bash
   sudo systemctl status mkdocs
   ```

3. **Test locally first:**
   ```bash
   curl http://localhost:8000
   ```

### Python dependencies fail to install

```bash
# Install system dependencies
sudo apt install -y python3-dev build-essential

# Try installing again
pip install --no-cache-dir -r requirements.txt
```

### Docker container won't start

```bash
# View logs
docker-compose logs mkdocs

# Rebuild container
docker-compose down
docker-compose up -d --build
```

---

## Performance Tips

1. **Enable Gzip in nginx** (auto-configured if using script with DOMAIN)
2. **Use Cloudflare** free CDN for better global performance
3. **Optimize images** in docs folder (compress PNGs, use WebP)
4. **Enable browser caching** in nginx config

---

## Security Checklist

- [ ] SSH key authentication enabled (not password)
- [ ] Firewall configured (UFW)
- [ ] Automatic security updates enabled
- [ ] HTTPS enabled with Let's Encrypt
- [ ] Regular backups scheduled
- [ ] Fail2ban installed (protects against brute force)

---

## Getting Help

- **Deployment Issues:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **MkDocs Questions:** https://www.mkdocs.org/
- **Docker Questions:** https://docs.docker.com/
- **Project Issues:** https://github.com/chronos717313/Mastery-of-time/issues

---

## Cost Summary

### DIY Hosting (DigitalOcean)
- Droplet: $6/month
- Domain: $12/year (~$1/month)
- Backup: $1.20/month (optional)
- **Total:** ~$8/month = $96/year

### Alternative: Managed Hosting
- GitHub Pages: FREE (but no server-side processing)
- Netlify: FREE tier available
- ReadTheDocs: FREE for open source

**Recommendation:** Start with DigitalOcean $6/month droplet for full control and scalability.
