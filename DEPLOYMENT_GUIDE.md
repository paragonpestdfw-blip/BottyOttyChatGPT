# BottyOtty Deployment Guide for pestresource.com

## Overview
This guide covers deploying the BottyOtty Discord bot to pestresource.com domain.

## Prerequisites
- Python 3.9 or higher
- Discord Bot Token
- Server/hosting environment (Railway, Heroku, or VPS)
- Domain access to pestresource.com

## Project Structure
```
BottyOttyChatGPT/
├── main.py                          # Main bot application
├── requirements.txt                 # Python dependencies
├── Procfile.txt                     # Process configuration
├── railway.json                     # Railway deployment config
├── robots.txt                       # SEO configuration
├── Admin Panel v18.html             # Web-based admin interface
├── BottyOtty Dashboard v18.html     # Bot dashboard
├── BottyOtty Help & User Guide v18.html
├── BottyOtty Reports v18.html       # Reporting interface
└── Quick Launch v18.html            # Quick start guide
```

## Step 1: Prepare Environment Variables

Create a `.env` file (or configure in your hosting platform):

```bash
# Discord Bot Configuration
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CLIENT_ID=your_client_id_here
DISCORD_CLIENT_SECRET=your_client_secret_here

# Optional: Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# Optional: API Configuration
API_URL=https://pestresource.com/api
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Current dependencies:
- discord.py
- python-dotenv
- (check requirements.txt for complete list)

## Step 3: Railway Deployment (Recommended)

Railway is pre-configured with `railway.json`:

1. **Connect Repository:**
   ```bash
   railway login
   railway link
   ```

2. **Set Environment Variables:**
   ```bash
   railway variables set DISCORD_BOT_TOKEN=your_token_here
   ```

3. **Deploy:**
   ```bash
   railway up
   ```

4. **Custom Domain:**
   - Go to Railway dashboard
   - Settings → Domains
   - Add custom domain: `bot.pestresource.com` or subdomain
   - Update DNS records as instructed

## Step 4: Alternative Hosting Options

### Option A: Heroku
```bash
heroku create bottyotty-pestresource
heroku config:set DISCORD_BOT_TOKEN=your_token_here
git push heroku main
```

### Option B: VPS/Dedicated Server
```bash
# Clone repository
git clone https://github.com/paragonpestdfw-blip/BottyOttyChatGPT.git
cd BottyOttyChatGPT

# Install dependencies
pip install -r requirements.txt

# Run with systemd (create /etc/systemd/system/bottyotty.service)
[Unit]
Description=BottyOtty Discord Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/BottyOttyChatGPT
Environment="DISCORD_BOT_TOKEN=your_token"
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable bottyotty
sudo systemctl start bottyotty
```

## Step 5: Web Interface Deployment

### Hosting HTML Files

1. **Upload to Web Server:**
   ```bash
   # Example: Using SCP to upload to pestresource.com
   scp *.html user@pestresource.com:/var/www/html/bot/
   scp robots.txt user@pestresource.com:/var/www/html/
   ```

2. **Configure Nginx (if applicable):**
   ```nginx
   server {
       listen 80;
       server_name pestresource.com www.pestresource.com;

       # Redirect to HTTPS
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl http2;
       server_name pestresource.com www.pestresource.com;

       ssl_certificate /etc/ssl/certs/pestresource.com.crt;
       ssl_certificate_key /etc/ssl/private/pestresource.com.key;

       root /var/www/html;
       index index.html;

       # Bot dashboard
       location /bot/ {
           try_files $uri $uri/ =404;
       }

       # Admin panel
       location /bot/admin {
           alias /var/www/html/bot/Admin Panel v18.html;
       }

       # Dashboard
       location /bot/dashboard {
           alias /var/www/html/bot/BottyOtty Dashboard v18.html;
       }

       # Reports
       location /bot/reports {
           alias /var/www/html/bot/BottyOtty Reports v18.html;
       }

       # Help guide
       location /bot/help {
           alias /var/www/html/bot/BottyOtty Help & User Guide v18.html;
       }
   }
   ```

3. **Configure Apache (alternative):**
   ```apache
   <VirtualHost *:443>
       ServerName pestresource.com
       DocumentRoot /var/www/html

       SSLEngine on
       SSLCertificateFile /etc/ssl/certs/pestresource.com.crt
       SSLCertificateKeyFile /etc/ssl/private/pestresource.com.key

       <Directory /var/www/html/bot>
           Options Indexes FollowSymLinks
           AllowOverride All
           Require all granted
       </Directory>

       # Friendly URLs
       Alias /bot/admin "/var/www/html/bot/Admin Panel v18.html"
       Alias /bot/dashboard "/var/www/html/bot/BottyOtty Dashboard v18.html"
       Alias /bot/reports "/var/www/html/bot/BottyOtty Reports v18.html"
       Alias /bot/help "/var/www/html/bot/BottyOtty Help & User Guide v18.html"
   </VirtualHost>
   ```

## Step 6: Discord Bot Setup

1. **Create Discord Application:**
   - Go to https://discord.com/developers/applications
   - Click "New Application"
   - Name it "BottyOtty" (or your preferred name)

2. **Create Bot User:**
   - Go to "Bot" section
   - Click "Add Bot"
   - Copy the bot token → use as `DISCORD_BOT_TOKEN`

3. **Set Bot Permissions:**
   Required permissions:
   - Read Messages/View Channels
   - Send Messages
   - Manage Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Add Reactions
   - Use Slash Commands

4. **Generate Invite URL:**
   - Go to "OAuth2" → "URL Generator"
   - Select scopes: `bot`, `applications.commands`
   - Select permissions (from step 3)
   - Copy generated URL
   - Use URL to invite bot to your server

## Step 7: Admin Panel Configuration

1. **Open Admin Panel:**
   - Navigate to `https://pestresource.com/bot/admin`

2. **Configure Auto-Sync:**
   - Enable "Automatically sync with Discord bot"
   - Set sync interval (default: 30 seconds)

3. **Set API URL:**
   - Configure bot API endpoint
   - Test connection

4. **Configure Permissions:**
   - Set up team member permissions
   - Define role-based access

## Step 8: Post-Deployment Checks

1. **Verify Bot is Online:**
   ```bash
   # Check bot status in Discord
   # Bot should show as "Online" with green indicator
   ```

2. **Test Slash Commands:**
   ```
   /help - Should display help information
   /ping - Should respond with latency
   ```

3. **Test Admin Panel:**
   - Open Admin Panel
   - Verify configuration saves
   - Check auto-sync functionality

4. **Check Logs:**
   ```bash
   # Railway
   railway logs

   # Heroku
   heroku logs --tail

   # VPS/systemd
   sudo journalctl -u bottyotty -f
   ```

## Step 9: SSL/HTTPS Setup

For pestresource.com, ensure HTTPS is enabled:

1. **Using Let's Encrypt (Free):**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot --nginx -d pestresource.com -d www.pestresource.com
   ```

2. **Auto-renewal:**
   ```bash
   sudo certbot renew --dry-run
   ```

## Step 10: Monitoring & Maintenance

1. **Set Up Monitoring:**
   - Use Railway/Heroku built-in monitoring
   - Or use UptimeRobot for external monitoring

2. **Regular Backups:**
   - Backup configuration files
   - Export admin panel settings regularly

3. **Update Schedule:**
   ```bash
   # Pull latest changes
   git pull origin main

   # Update dependencies
   pip install -r requirements.txt --upgrade

   # Restart bot
   railway restart  # or equivalent for your platform
   ```

## Troubleshooting

### Bot Won't Start
- Check `DISCORD_BOT_TOKEN` is set correctly
- Verify Python version is 3.9+
- Check logs for error messages

### Admin Panel Not Loading
- Verify HTML files are uploaded correctly
- Check web server configuration
- Ensure robots.txt allows crawling

### Auto-Sync Not Working
- Verify API URL is configured
- Check network connectivity between dashboard and bot
- Review sync interval settings

### Permission Errors
- Verify bot has required Discord permissions
- Check role hierarchy in Discord server
- Review admin panel permission settings

## Security Best Practices

1. **Keep Tokens Secret:**
   - Never commit tokens to git
   - Use environment variables
   - Rotate tokens periodically

2. **Restrict Admin Panel Access:**
   - Use IP whitelisting if possible
   - Implement authentication layer
   - Use HTTPS only

3. **Regular Updates:**
   - Keep discord.py updated
   - Monitor security advisories
   - Update dependencies regularly

## Support & Resources

- Repository: https://github.com/paragonpestdfw-blip/BottyOttyChatGPT
- Discord.py Docs: https://discordpy.readthedocs.io/
- Railway Docs: https://docs.railway.app/

## Quick Reference URLs

After deployment, your bot interfaces will be available at:
- Admin Panel: https://pestresource.com/bot/admin
- Dashboard: https://pestresource.com/bot/dashboard
- Reports: https://pestresource.com/bot/reports
- Help Guide: https://pestresource.com/bot/help

---

*Last updated: December 2025*
