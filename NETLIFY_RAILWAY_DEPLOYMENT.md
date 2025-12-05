# Complete Deployment Guide: Netlify + Railway

**Last Updated:** December 5, 2025
**For:** BottyOtty Dashboard + Discord Bot
**Domain:** pestresource.com

---

## 🎯 Architecture Overview

Your system has **TWO separate components** that need to be deployed:

### 1. **Frontend (Static HTML Files)** → Netlify
- All HTML pages (Admin Panel, Dashboard, Reports, etc.)
- No server-side code
- Pure client-side React (via CDN)
- Communicates with bot API via fetch()

### 2. **Backend (Discord Bot + API)** → Railway
- main.py (Discord bot + Flask API)
- SQLite database (tasks.db)
- Handles Discord commands
- Provides REST API for frontend

```
┌─────────────────┐         HTTPS API Calls        ┌──────────────────┐
│   Netlify       │  ──────────────────────────>   │    Railway       │
│  (Frontend)     │                                  │   (Backend)      │
│                 │  <────────────────────────────  │                  │
│ - Dashboard     │         JSON Responses          │ - main.py        │
│ - Admin Panel   │                                  │ - Flask API      │
│ - Reports       │                                  │ - tasks.db       │
│ - All HTML      │                                  │ - Discord Bot    │
└─────────────────┘                                  └──────────────────┘
         │                                                    │
         │                                                    │
         └────────────── Users ──────────────────────────────┘
                      (Browser)                        (Discord Server)
```

---

## Part 1: Deploy Backend to Railway

### Step 1: Prepare Your Repository

Your bot is **already set up** with all necessary files:

```bash
BottyOttyChatGPT/
├── main.py                          # Discord bot + Flask API
├── requirements.txt                 # Python dependencies
├── tasks.db                         # SQLite database (auto-created)
└── bot_config.json                  # Config from Admin Panel (auto-created)
```

### Step 2: Deploy to Railway

1. **Go to Railway:** https://railway.app/
2. **Login with GitHub**
3. **New Project → Deploy from GitHub repo**
4. **Select:** `paragonpestdfw-blip/BottyOttyChatGPT`
5. **Branch:** `claude/consolidated-all-features-014GifquVpcPXSiZ7QSeYnpe`

### Step 3: Configure Environment Variables

In Railway dashboard, add these environment variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `DISCORD_TOKEN` | `your_bot_token_here` | Get from Discord Developer Portal |
| `PORT` | `8080` | Flask API port (Railway auto-detects) |
| `PYTHON_VERSION` | `3.11` | Python version |

**Get your Discord token:**
1. Go to https://discord.com/developers/applications
2. Click your bot application
3. Go to "Bot" section
4. Copy token (or reset to get new one)

### Step 4: Verify Deployment

Railway will automatically:
1. Install dependencies from `requirements.txt`
2. Run `python main.py`
3. Start Discord bot
4. Start Flask API on port 8080

**Check logs:**
```
✅ Discord bot starting...
✅ Flask server starting on 0.0.0.0:8080
✅ Bot is ready! Logged in as BottyOtty#1234
✅ Flask running on http://0.0.0.0:8080
```

### Step 5: Get Your API URL

Railway will assign you a URL like:
```
https://bottyotty-production.up.railway.app
```

**Test it:**
```bash
curl https://bottyotty-production.up.railway.app/api/health
```

Should return:
```json
{
  "status": "healthy",
  "bot_online": true,
  "database": "connected"
}
```

---

## Part 2: Deploy Frontend to Netlify

### Step 1: Prepare HTML Files

All your HTML files are **already ready** for deployment. They include:

**Main Pages:**
- Admin Panel v18.html (9,887 lines)
- BottyOtty Dashboard v18.html (10,962 lines)
- BottyOtty Reports v18.html (2,473 lines)
- BottyOtty Help & User Guide v18.html (3,729 lines)
- BottyOtty Newsletter v18.html (864 lines)
- Quick Launch v18.html (3,558 lines)

**Widget Pages:**
- Company Calendar v18.html
- Customer Feedback Tracker v18.html
- Inventory Widget v18.html
- Lead Sites Switchboard v18.html
- Office Alerts v18.html
- Pest Move-Up List v18.html
- Safety Management v18.html
- Tech Reminders v18.html
- Vehicle Management v18.html

**Features included in ALL pages:**
✅ Sidebar navigation (collapsible)
✅ Consistent UI/styling
✅ Dark glassmorphic theme
✅ Links between all pages
✅ API connectivity to Railway backend

### Step 2: Update API URLs

**IMPORTANT:** Before deploying, update the API URL in all HTML files.

Find and replace in ALL HTML files:
```javascript
// Change this:
const API_BASE = "http://localhost:8080";

// To this:
const API_BASE = "https://bottyotty-production.up.railway.app";
```

**Files to update:**
- Admin Panel v18.html
- BottyOtty Dashboard v18.html
- BottyOtty Reports v18.html
- All widget HTML files that make API calls

### Step 3: Create index.html

Netlify needs an `index.html` as the entry point. Create one:

**Option 1:** Rename Dashboard as index
```bash
cp "BottyOtty Dashboard v18.html" index.html
```

**Option 2:** Create a landing page that redirects
```html
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="refresh" content="0; url=BottyOtty Dashboard v18.html">
  <title>BottyOtty - Redirecting...</title>
</head>
<body>
  <p>Redirecting to Dashboard...</p>
</body>
</html>
```

### Step 4: Create _redirects File

Create a file named `_redirects` (no extension) in your project root:

```
# Netlify redirects for clean URLs

/dashboard    /BottyOtty Dashboard v18.html    200
/admin        /Admin Panel v18.html             200
/reports      /BottyOtty Reports v18.html       200
/help         /BottyOtty Help & User Guide v18.html    200
/newsletter   /BottyOtty Newsletter v18.html    200
/quick        /Quick Launch v18.html            200

# Widget redirects
/calendar     /Company Calendar v18.html        200
/feedback     /Customer Feedback Tracker v18.html    200
/inventory    /Inventory Widget v18.html        200
/leads        /Lead Sites Switchboard v18.html  200
/alerts       /Office Alerts v18.html           200
/moveup       /Pest Move-Up List v18.html       200
/safety       /Safety Management v18.html       200
/reminders    /Tech Reminders v18.html          200
/vehicles     /Vehicle Management v18.html      200

# Default to dashboard
/             /BottyOtty Dashboard v18.html     200

# 404 - Redirect to dashboard
/*            /BottyOtty Dashboard v18.html     404
```

### Step 5: Deploy to Netlify

**Method 1: Drag & Drop (Easiest)**

1. Go to https://app.netlify.com/
2. Login with GitHub
3. Click "Add new site → Deploy manually"
4. Drag your entire project folder
5. Wait for deployment (1-2 minutes)

**Method 2: GitHub Integration (Recommended)**

1. Go to https://app.netlify.com/
2. Login with GitHub
3. Click "Add new site → Import from Git"
4. Choose GitHub
5. Select repository: `paragonpestdfw-blip/BottyOttyChatGPT`
6. Branch: `claude/consolidated-all-features-014GifquVpcPXSiZ7QSeYnpe`
7. Build settings:
   - **Build command:** (leave empty - no build needed)
   - **Publish directory:** `/` (root)
8. Click "Deploy site"

### Step 6: Configure Custom Domain

1. In Netlify dashboard, go to **Domain settings**
2. Click "Add custom domain"
3. Enter: `pestresource.com`
4. Netlify will provide DNS settings

**Add these records to your domain registrar:**

| Type | Name | Value |
|------|------|-------|
| CNAME | www | `your-site-name.netlify.app` |
| A | @ | `75.2.60.5` |

**Or use Netlify DNS:**
1. Transfer nameservers to Netlify
2. Netlify handles everything automatically

### Step 7: Enable HTTPS

Netlify automatically provisions SSL certificates via Let's Encrypt:
1. Go to **Domain settings → HTTPS**
2. Click "Verify DNS configuration"
3. Wait 5-10 minutes for SSL to activate
4. Enable "Force HTTPS"

---

## Part 3: Connect Frontend to Backend

### Update CORS in main.py

Add Netlify domain to CORS allowed origins:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "https://pestresource.com",
    "https://www.pestresource.com",
    "https://your-site-name.netlify.app",
    "http://localhost:3000"  # For local testing
])
```

Redeploy Railway after this change.

### Test API Connectivity

Open browser console on your Netlify site and test:

```javascript
fetch('https://bottyotty-production.up.railway.app/api/health')
  .then(r => r.json())
  .then(console.log)
```

Should return:
```json
{
  "status": "healthy",
  "bot_online": true
}
```

---

## 🔐 Authentication Status

### Current Authentication: **Simple Name Selection**

Your app currently uses a **basic dropdown login**:

1. User opens Dashboard
2. Modal appears with dropdown of all team members
3. User selects their name
4. Selection stored in `localStorage`
5. No passwords, no Auth0, no verification

**Security Level:** ⚠️ **Low** - Anyone can select any name

### Authentication Flow:

```javascript
// In BottyOtty Dashboard v18.html (line 1782)
function LoginModal({ onLogin }) {
  // User selects name from TEAM_MEMBERS dropdown
  // No password required
  // Stored in localStorage: 'bottyotty-current-user'
}
```

### **Auth0 is NOT implemented**

You mentioned Auth0, but it's **not currently in the codebase**. Your options:

**Option 1: Keep Simple Auth (Current)**
- ✅ Easy for employees
- ✅ No passwords to remember
- ❌ No real security
- ❌ Anyone with URL can access
- **Best for:** Internal company tool on private network

**Option 2: Add Password Protection**
- Add password field to login modal
- Store hashed passwords in localStorage or database
- Still no external auth provider

**Option 3: Implement Auth0 (Requires Development)**
- Would need to add Auth0 SDK
- Configure Auth0 application
- Add login callbacks
- Implement JWT verification
- **Estimated work:** 4-6 hours

**Option 4: Netlify Identity (Easiest Upgrade)**
- Built into Netlify
- No code changes needed
- Email/password or magic links
- Free for up to 1,000 users

### Recommendation for Netlify Deployment:

**Use Netlify Identity** (simplest upgrade):

1. Enable in Netlify dashboard
2. Add this to your HTML `<head>`:
```html
<script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
```

3. Add login button:
```javascript
netlifyIdentity.open(); // Opens login modal
```

4. Check if user is logged in:
```javascript
const user = netlifyIdentity.currentUser();
if (!user) {
  netlifyIdentity.open();
}
```

**Or keep as-is** if this is internal-only and you trust your team.

---

## 📊 Database Information

### Current Setup: **SQLite (tasks.db)**

Your bot uses **SQLite** for data storage:

```python
# Database created automatically on first run
DATABASE = 'tasks.db'

# Tables:
- tasks                 # All tasks/jobs/operations
- pool_channels         # Task pool assignments
- callouts              # Employee callouts
- mentions              # @mentions tracking
- task_updates          # Task status changes
- trainings             # Training sessions
- training_attendance   # Who attended trainings
- important_messages    # Pinned messages
- message_reactions     # Reaction tracking
```

### Database Location:

**On Railway:** Stored in container's filesystem
- ⚠️ **Data persists ONLY while container runs**
- If Railway redeploys, database resets
- **Solution:** Use Railway's Persistent Volumes

### Add Persistent Storage:

1. In Railway dashboard, click your service
2. Go to "Volumes" tab
3. Click "New Volume"
4. Name: `bottyotty-data`
5. Mount path: `/app/data`
6. Update main.py:
```python
DATABASE = '/app/data/tasks.db'
```
7. Redeploy

Now your database persists across deployments!

### Alternative: PostgreSQL

For production, consider PostgreSQL:

1. **Add PostgreSQL plugin in Railway**
2. **Update main.py** to use PostgreSQL instead of SQLite
3. **Install psycopg2:** Add to requirements.txt
4. **Migrate data** from SQLite to PostgreSQL

**Benefits:**
- ✅ Better performance
- ✅ Automatic backups
- ✅ Concurrent access
- ✅ Production-ready

---

## 🚀 Complete Deployment Checklist

### Before Deployment:

- [ ] Discord bot token ready
- [ ] Railway account created
- [ ] Netlify account created
- [ ] Domain DNS access (if using custom domain)
- [ ] All HTML files have updated API URLs

### Railway Backend:

- [ ] Repository connected
- [ ] Branch selected (consolidated-all-features)
- [ ] Environment variables set (DISCORD_TOKEN)
- [ ] Deployment successful
- [ ] Bot shows "Online" in Discord
- [ ] API health check passes
- [ ] Persistent volume added for database
- [ ] CORS configured for Netlify domain

### Netlify Frontend:

- [ ] index.html created (or Dashboard renamed)
- [ ] _redirects file created
- [ ] robots.txt uploaded
- [ ] All HTML files uploaded
- [ ] API URLs updated to Railway URL
- [ ] Site deployed
- [ ] Custom domain configured (if applicable)
- [ ] HTTPS enabled
- [ ] SSL certificate active
- [ ] Test all pages load correctly
- [ ] Test API calls work from frontend

### Post-Deployment:

- [ ] Test login flow
- [ ] Test creating tasks from Dashboard
- [ ] Test Discord bot commands
- [ ] Test Admin Panel config sync
- [ ] Test all widget pages
- [ ] Test automated reports
- [ ] Test Discord panel modals
- [ ] Verify database persistence
- [ ] Check mobile responsiveness
- [ ] Monitor Railway logs for errors

---

## 🛠️ Troubleshooting

### Frontend Issues:

**Pages show 404:**
- Check _redirects file is uploaded
- Verify file names match exactly (case-sensitive)

**API calls fail (CORS errors):**
- Update CORS in main.py to include Netlify domain
- Redeploy Railway
- Hard refresh browser (Ctrl+Shift+R)

**Styles broken:**
- All CSS is inline, so shouldn't happen
- Check browser console for errors

### Backend Issues:

**Bot offline in Discord:**
- Check Railway logs
- Verify DISCORD_TOKEN is correct
- Check bot has all required intents enabled

**API returns 500 errors:**
- Check Railway logs for Python errors
- Verify database is accessible
- Check all environment variables set

**Database resets on deploy:**
- Add persistent volume in Railway
- Mount at /app/data
- Update DATABASE path in main.py

---

## 📈 Monitoring & Maintenance

### Railway Monitoring:

**View logs:**
```bash
# In Railway dashboard
Deployments → Latest → Logs
```

**Check metrics:**
- CPU usage
- Memory usage
- Network traffic
- Database size

### Netlify Monitoring:

**Analytics:**
- Page views
- Unique visitors
- Popular pages
- Traffic sources

**Functions (if added later):**
- Invocations
- Errors
- Run time

---

## 💰 Costs

### Railway:
- **Hobby Plan:** $5/month
- **Pro Plan:** $20/month
- Includes persistent volumes
- Unlimited deployments

### Netlify:
- **Free Starter:** $0/month
  - 100 GB bandwidth
  - 300 build minutes
  - HTTPS included
- **Pro Plan:** $19/month (if needed)

### Total Monthly Cost:
**$5-$25/month** depending on tier

---

## 🔄 Updating Your Site

### Frontend Updates:

**Method 1: Git Push (If using GitHub integration)**
```bash
git add .
git commit -m "Update Admin Panel"
git push origin claude/consolidated-all-features-014GifquVpcPXSiZ7QSeYnpe
# Netlify auto-deploys
```

**Method 2: Manual Upload**
- Drag updated files to Netlify deploy page
- Previous version automatically backed up

### Backend Updates:

```bash
git add main.py
git commit -m "Add new API endpoint"
git push origin claude/consolidated-all-features-014GifquVpcPXSiZ7QSeYnpe
# Railway auto-deploys (if auto-deploy enabled)
```

---

## ✅ Summary

Your **complete deployment** consists of:

### 🌐 **Netlify (Frontend):**
- Domain: `pestresource.com`
- All 15 HTML pages
- Static files only
- No server-side code
- HTTPS enabled

### 🚂 **Railway (Backend):**
- Domain: `bottyotty-production.up.railway.app`
- Discord bot (Python)
- Flask REST API
- SQLite database
- Persistent storage

### 🔗 **Connection:**
- Frontend calls Backend API via HTTPS
- CORS enabled for pestresource.com
- All data flows through API endpoints

### 🔐 **Authentication:**
- Simple dropdown name selection
- Stored in localStorage
- **No Auth0** (not implemented)
- Consider upgrading to Netlify Identity

### 💾 **Database:**
- SQLite (tasks.db)
- Auto-creates on first run
- Needs persistent volume on Railway
- Consider PostgreSQL for production

---

**You're ready to deploy!** 🚀

All your files are properly merged with sidebar navigation on every page, and all features are integrated. Just follow the steps above for Netlify + Railway deployment.
