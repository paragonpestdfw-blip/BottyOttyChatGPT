# BottyOtty Backend Integration - Installation Guide

## 🎯 What This Does

This guide will help you integrate all 9 new BottyOtty management tools with your Discord bot's database, replacing localStorage with persistent cloud storage.

**After installation:**
- ✅ All data persists across users and devices
- ✅ Automatic daily backups to GitHub at 3 AM
- ✅ 40+ new API endpoints for your tools
- ✅ Data syncs between web pages and Discord bot
- ✅ Old backups (>7 days) automatically cleaned up

---

## 📋 Pre-Installation Checklist

**What you need:**
- [ ] Access to your Railway deployment
- [ ] Your main.py file (already has Flask and SQLite)
- [ ] The 3 backend integration files (PART1, PART2, PART3)

**What's already in your main.py:**
- ✅ Flask app running on port 8080
- ✅ SQLite database (tasks.db)
- ✅ Discord bot with discord.py
- ✅ Existing API endpoints and modals

---

## 🚀 Installation Steps

### Step 1: Add Required Imports

Open your `main.py` and check if these imports exist at the **top of the file**. Add any missing ones:

```python
import os
import shutil
import subprocess
from datetime import datetime
import sqlite3
from flask import Flask, jsonify, request
from discord.ext import tasks
import discord
```

**Note:** Most of these should already exist. Only add what's missing.

---

### Step 2: Add Database Initialization Function

Find a good spot in your `main.py` (I recommend after your Flask app is defined but before your routes).

Copy and paste the **entire `init_bottyotty_tables()` function** from `BACKEND_INTEGRATION_PART1.py` (lines 23-194).

This creates all 12 database tables:
1. calendar_events
2. calendar_notes
3. lead_sites
4. vehicles
5. safety_incidents
6. safety_inspections
7. customer_feedback
8. tech_reminders
9. inventory
10. pest_moveup
11. office_alerts
12. alert_people

---

### Step 3: Add API Endpoints

#### 3a. Calendar, Lead Sites, and Vehicles APIs

Copy all the API endpoints from `BACKEND_INTEGRATION_PART1.py` (lines 196-545) and paste them after the database initialization function.

This adds:
- `/api/calendar/events` (GET, POST, DELETE)
- `/api/calendar/notes/<month_key>` (GET, PUT)
- `/api/lead-sites` (GET, POST, PUT, DELETE)
- `/api/vehicles` (GET, POST, PUT, DELETE)

#### 3b. Remaining APIs

Copy all the API endpoints from `BACKEND_INTEGRATION_PART2.py` and paste them after the previous endpoints.

This adds:
- `/api/safety/incidents` (GET, POST, DELETE)
- `/api/safety/inspections` (GET, POST, DELETE)
- `/api/feedback` (GET, POST, DELETE)
- `/api/tech-reminders` (GET, POST, PUT, DELETE)
- `/api/inventory` (GET, POST, PUT, DELETE)
- `/api/pest-moveup` (GET, POST, PUT, DELETE)
- `/api/office-alerts` (GET, POST)
- `/api/alert-people` (GET, POST, DELETE)

---

### Step 4: Add Backup System

Copy the following sections from `BACKEND_INTEGRATION_PART3_BACKUP.py`:

**4a. Backup Functions** (lines 17-92)
- `backup_database()` - Main backup loop
- `cleanup_old_backups()` - Removes old backups
- `before_backup()` - Initialization

**4b. Manual Backup Endpoints** (lines 96-142)
- `/api/backup/now` - Trigger manual backup
- `/api/backup/list` - List all backups

**4c. Swamped Alert Endpoint** (lines 169-225)
- `/api/swamped-alert` - Handle swamped alerts from Admin Panel

---

### Step 5: Initialize on Bot Startup

Find your bot's `on_ready()` event handler in `main.py`. If it doesn't exist, add it:

```python
@bot.event
async def on_ready():
    """Initialize database and start backup system when bot starts"""
    print(f'Logged in as {bot.user.name}')

    # Initialize BottyOtty database tables
    init_bottyotty_tables()

    # Start backup loop
    if not backup_database.is_running():
        backup_database.start()

    print("✅ BottyOtty integration ready!")
```

**Important:** If you already have an `on_ready()` function, just add the 3 new lines inside it (init_bottyotty_tables, backup check, start backup).

---

## 🧪 Testing Your Installation

### Test 1: Database Initialization

After deploying, check your Railway logs. You should see:
```
✅ BottyOtty database tables initialized!
✅ Backup system initialized - running daily at 3 AM
✅ BottyOtty integration ready!
```

### Test 2: API Health Check

Visit: `https://YOUR-RAILWAY-URL.railway.app/api/health`

Should return:
```json
{"status": "healthy"}
```

### Test 3: Test an Endpoint

Visit: `https://YOUR-RAILWAY-URL.railway.app/api/vehicles`

Should return:
```json
{"success": true, "vehicles": []}
```

### Test 4: Manual Backup

**Using curl:**
```bash
curl -X POST https://YOUR-RAILWAY-URL.railway.app/api/backup/now
```

**Should return:**
```json
{
  "success": true,
  "message": "Backup created: backups/tasks_backup_2025-12-04_15-30-45.db",
  "timestamp": "2025-12-04_15-30-45"
}
```

**Check your Railway logs** for:
```
✅ Database backed up: backups/tasks_backup_2025-12-04_15-30-45.db
```

---

## 📁 File Structure After Installation

```
BottyOttyChatGPT/
├── main.py                           # Your bot (now with 40+ new endpoints!)
├── tasks.db                          # Main database
├── backups/                          # Auto-created backup folder
│   ├── tasks_backup_2025-12-04_03-00-00.db
│   ├── tasks_backup_2025-12-05_03-00-00.db
│   └── tasks_latest.db              # Always the most recent backup
├── Company Calendar v18.html
├── Lead Sites Switchboard v18.html
├── Vehicle Management v18.html
├── Safety Management v18.html
├── Customer Feedback Tracker v18.html
├── Tech Reminders v18.html
├── Inventory Widget v18.html
├── Pest Move-Up List v18.html
└── Office Alerts v18.html
```

---

## 🔄 Automatic Backup System

### How it works:

1. **Daily at 3 AM** (server time):
   - Creates timestamped backup: `tasks_backup_2025-12-04_03-00-00.db`
   - Updates `tasks_latest.db` (always most recent)
   - Commits to git
   - Pushes to GitHub
   - Cleans up backups older than 7 days

2. **Manual backups anytime:**
   - POST to `/api/backup/now`
   - Creates immediate backup with current timestamp

3. **List all backups:**
   - GET `/api/backup/list`
   - Returns JSON with all backups, sizes, ages

### Backup location:

- **Local:** `/backups/` directory in your Railway deployment
- **GitHub:** Pushed to your repository (visible in commits)
- **Retention:** Last 7 days kept automatically

---

## 🌐 Next Step: Connect HTML Pages to API

Right now your HTML pages still use `localStorage`. To connect them to the database:

1. Replace `localStorage.getItem()` with `fetch('/api/...')`
2. Replace `localStorage.setItem()` with `fetch('/api/...', { method: 'POST' })`

**Example for Calendar:**

**Before (localStorage):**
```javascript
const events = JSON.parse(localStorage.getItem('bottyotty-calendar-events') || '[]');
```

**After (API):**
```javascript
const response = await fetch('https://YOUR-RAILWAY-URL.railway.app/api/calendar/events');
const data = await response.json();
const events = data.events;
```

I can help update all 9 HTML pages once you confirm the backend is working!

---

## 🐛 Troubleshooting

### Issue: "Module 'discord.ext.tasks' not found"

**Fix:** Update your requirements.txt:
```
discord.py>=2.0.0
```

### Issue: "Database is locked"

**Cause:** SQLite doesn't handle concurrent writes well

**Fix:** This is normal for low-frequency operations. The code already handles this gracefully.

### Issue: Backups not pushing to GitHub

**Possible causes:**
1. Git credentials not configured on Railway
2. Branch protection rules
3. Network issues

**Fix:** Check Railway environment variables:
```
GIT_USER=your-username
GIT_TOKEN=your-github-token
```

### Issue: "Port 8080 already in use"

**Cause:** Your Flask app is already running

**Fix:** This is correct! Your existing Flask app just has more endpoints now.

---

## ✅ Verification Checklist

After installation, verify:

- [ ] Bot starts without errors
- [ ] Database tables created (check Railway logs)
- [ ] Backup system initialized
- [ ] API endpoints respond (test /api/vehicles)
- [ ] Manual backup works (/api/backup/now)
- [ ] Automatic backup runs at 3 AM (check next morning)
- [ ] Old backups cleaned up after 7 days

---

## 🎉 Success!

Once you see these logs on Railway:

```
✅ BottyOtty database tables initialized!
✅ Backup system initialized - running daily at 3 AM
✅ BottyOtty integration ready!
```

**Your backend is fully operational!**

All 9 management tools now have:
- ✅ Persistent database storage
- ✅ RESTful API endpoints
- ✅ Automatic daily backups
- ✅ GitHub version control
- ✅ Multi-user support

---

## 📞 Need Help?

If something doesn't work:

1. Check Railway logs for error messages
2. Test each endpoint individually
3. Verify database file exists: `tasks.db`
4. Confirm backup folder created: `backups/`
5. Check git status for backup commits

**Common first-time issues:**
- Missing imports (add them to top of main.py)
- `on_ready()` not calling initialization
- CORS not enabled (should already be in your Flask app)
