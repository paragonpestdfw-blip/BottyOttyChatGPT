# Dashboard & Bot Integration Guide

Complete guide for how the BottyOtty web dashboard and Discord bot work together.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Shared Features](#shared-features)
3. [Dashboard-Only Features](#dashboard-only-features)
4. [Discord-Only Features](#discord-only-features)
5. [API Integration](#api-integration)
6. [Best Practices](#best-practices)

---

## 🌐 Overview

BottyOtty operates as a **unified system** with two interfaces:

**Web Dashboard** (HTML/React)
- Browser-based interface
- Visual calendar, reports, alerts
- Desktop/laptop optimized
- Direct database access

**Discord Bot** (Python/Discord.py)
- Chat-based interface
- Slash commands and modals
- Mobile-friendly
- Real-time notifications

**Both interfaces share the same database** (tasks.db), ensuring data stays in sync.

---

## 🔄 Shared Features

These features work on BOTH dashboard and Discord with full synchronization:

### 1. Calendar Events

**Dashboard:**
- Visual calendar grid
- Click dates to add events
- Drag-and-drop (if enabled)
- Month notes
- Event type colors

**Discord:**
- `/calendar` command
- Add via modal form
- View upcoming events
- This month view
- Discord scheduled events

**Data Flow:**
```
Dashboard Add Event → API → Database → Discord sees it
Discord Add Event → Database → API → Dashboard sees it
```

**Files:**
- Dashboard: `Company Calendar v18.html`
- Discord: `/calendar` command in main.py
- API: `/api/calendar/events` endpoints

---

### 2. Office Alerts

**Dashboard:**
- Send targeted alerts
- Select recipients
- Set priority (high/medium/low)
- Specify Discord channel

**Discord:**
- Receives alerts in configured channel
- Color-coded by priority
- Formatted embeds
- Timestamp tracking

**Data Flow:**
```
Dashboard → /api/office-alert → Bot → Discord Channel
```

**Files:**
- Dashboard: `Office Alerts v18.html`
- Discord: `/api/office-alert` endpoint in main.py

---

### 3. Task Management

**Dashboard:**
- Task list view
- Status tracking
- Assignee management
- Category filtering

**Discord:**
- Slash commands create tasks
- Modals submit to database
- Reports query task data
- Logs view historical tasks

**Data Flow:**
```
Both → tasks.db → Both can query
```

**Files:**
- Dashboard: `Admin Panel v18.html`, `BottyOtty Dashboard v18.html`
- Discord: All modals and commands in main.py

---

## 🖥️ Dashboard-Only Features

Features currently only available on the web dashboard:

### 1. Visual Interfaces

**BottyOtty Dashboard v18.html**
- Grid layout
- Drag-and-drop widgets
- Live stats
- Quick launch buttons

**Admin Panel v18.html**
- User management
- System settings
- Bulk operations
- Advanced filtering

### 2. Reports & Analytics

**BottyOtty Reports v18.html**
- Visual charts
- Export to Excel/PDF
- Custom date ranges
- Trend analysis

**Note:** Discord has `/reports` command for basic statistics, but dashboard offers richer visualizations.

### 3. Customer Feedback Tracker

**Customer Feedback Tracker v18.html**
- Rating submissions
- Review management
- Response tracking
- Analytics dashboard

### 4. Inventory Management

**Inventory Widget v18.html**
- Stock levels
- Order history
- Low stock alerts
- Supplier management

### 5. Vehicle Fleet

**Vehicle Management v18.html**
- Vehicle roster
- Maintenance schedules
- Inspection records
- Mileage tracking

### 6. Safety Management

**Safety Management v18.html**
- Incident logs
- Training records
- Compliance tracking
- Safety metrics

### 7. Lead Sites Switchboard

**Lead Sites Switchboard v18.html**
- Lead source tracking
- Conversion metrics
- Sales pipeline
- Performance analytics

---

## 💬 Discord-Only Features

Features only available through Discord bot:

### 1. Real-Time Alerts

**Employee → Management Alerts**
- `/alert` command
- Time updates
- Customer evidence
- Pending appointments
- General alerts

**Real-time notification to management channels**

### 2. Policy & Knowledge Base

**Instant Access:**
- `/policy` - 20 company policies
- `/kb` - 20 knowledge articles
- Private responses
- Always up-to-date

### 3. Interactive Panels

**Persistent UI:**
- Request Panel
- Office Team Panel
- Move-Up Panel
- Management Panel

**Available 24/7, survive bot restarts**

### 4. Discord Scheduled Events

**Native Integration:**
- Auto-creates Discord events
- RSVP functionality
- Mobile notifications
- Server Events tab

### 5. Log Viewing

**Historical Access:**
- `/logs` command
- 9 log types
- Date range filtering
- DM exports

---

## 🔌 API Integration

### How Data Syncs

**Database: tasks.db (SQLite)**
```
Web Dashboard ↔️ API Endpoints ↔️ Database ↔️ Discord Bot
```

### API Endpoints

**Calendar:**
- `GET /api/calendar/events` - Fetch all events
- `POST /api/calendar/events` - Create event
- `DELETE /api/calendar/events/<id>` - Delete event
- `GET /api/calendar/notes/<monthKey>` - Get month notes
- `POST /api/calendar/notes/<monthKey>` - Save month notes

**Office Alerts:**
- `POST /api/office-alert` - Send alert to Discord

**Tasks:**
- `GET /api/tasks` - Fetch all tasks
- `POST /api/tasks` - Create task
- `DELETE /api/tasks/<id>` - Delete task
- `PUT /api/tasks/<id>/update` - Update task
- `POST /api/tasks/<id>/complete` - Complete task

**Trainings:**
- `GET /api/trainings` - Fetch trainings
- `POST /api/trainings` - Create training
- `POST /api/trainings/<id>/signin` - Sign in to training

**Important Messages:**
- `GET /api/important-messages` - Fetch messages
- `POST /api/important-messages/<id>/react` - React to message

**Health Check:**
- `GET /api/health` - Bot status

### API Base URL
```
https://bottyotty-production.up.railway.app
```

---

## 📊 Data Flow Examples

### Example 1: Creating a Calendar Event

**From Dashboard:**
```
1. User clicks date in Company Calendar
2. Fills out event form
3. JavaScript calls POST /api/calendar/events
4. API saves to tasks.db with type='calendar-event'
5. Returns success
6. Dashboard updates UI
```

**From Discord:**
```
1. User runs /calendar add
2. Fills out modal
3. Bot saves to tasks.db with type='calendar-event'
4. Bot creates Discord scheduled event
5. Posts confirmation to channel
```

**Result:** Both can now see the event!

---

### Example 2: Sending an Office Alert

**From Dashboard:**
```
1. Manager opens Office Alerts page
2. Writes message, selects recipients, sets priority
3. Optionally specifies Discord channel ID
4. Clicks "Send Alert"
5. JavaScript calls POST /api/office-alert
6. API sends message to Discord bot via asyncio
7. Bot posts to specified channel
8. Returns success to dashboard
```

**Result:** Alert appears in Discord with formatted embed

---

### Example 3: Viewing Calendar Events

**Dashboard Query:**
```javascript
const response = await fetch(`${API_URL}/api/calendar/events`);
const data = await response.json();
// Displays events in calendar grid
```

**Discord Query:**
```python
c.execute('''
    SELECT id, title, description, created_at, category
    FROM tasks
    WHERE task_type = 'calendar-event'
    ORDER BY created_at ASC
''')
# Displays events in embed
```

**Same Database, Different Presentation!**

---

## 🎯 Best Practices

### When to Use Dashboard

**Use dashboard for:**
- ✅ Visual data analysis
- ✅ Bulk operations
- ✅ Report generation with charts
- ✅ Configuration and settings
- ✅ Desktop work sessions
- ✅ Complex filtering and search
- ✅ Historical data review

### When to Use Discord

**Use Discord for:**
- ✅ Quick submissions on the go
- ✅ Real-time notifications
- ✅ Mobile access
- ✅ Team communication
- ✅ Instant policy/KB lookup
- ✅ Quick status checks
- ✅ Field work

### Workflow Tips

**Morning Routine:**
1. Check dashboard for daily metrics
2. Review calendar events
3. Join Discord for real-time updates

**Field Work:**
1. Use Discord `/alert` for time updates
2. Submit requests via Discord panels
3. Check calendar on mobile

**End of Day:**
1. Submit final reports via Discord
2. Review day's activity on dashboard
3. Plan tomorrow's schedule

**Management Tasks:**
1. Send alerts via dashboard
2. Generate reports on dashboard
3. Monitor Discord channels for submissions
4. Use `/reports` for quick stats

---

## 🔄 Synchronization

### What Syncs Automatically

✅ **Calendar Events** - Both directions
✅ **Office Alerts** - Dashboard → Discord
✅ **Tasks** - Both directions
✅ **Trainings** - Both directions

### What Requires Manual Action

❌ **Dashboard visual settings** - Dashboard only
❌ **Discord panel placements** - Discord only
❌ **Discord scheduled events** - Discord creates them
❌ **Report charts** - Dashboard only

### Sync Status

**Check if synced:**
- Dashboard: Look for "Last updated" timestamp
- Discord: Event ID numbers match database IDs
- API: `GET /api/health` shows bot status

**If not syncing:**
1. Check API_URL in HTML files
2. Verify bot is online (`/api/health`)
3. Check Railway logs for errors
4. Ensure database connection is active

---

## 🛠️ Troubleshooting

### Dashboard Can't Reach API

**Symptoms:**
- Events don't save
- "API Error" messages
- Loading spinners don't complete

**Solutions:**
1. Check API_URL in HTML file (should be Railway URL)
2. Verify bot is running on Railway
3. Check browser console for CORS errors
4. Try refreshing the page

### Discord Not Seeing Dashboard Events

**Symptoms:**
- Events created in dashboard don't show in `/calendar`
- Counts don't match

**Solutions:**
1. Verify API endpoints are working (check `/api/health`)
2. Check database connection
3. Ensure both are pointing to same database
4. Review Railway logs

### Dashboard Not Seeing Discord Events

**Symptoms:**
- Events created in Discord don't show in calendar
- Dashboard appears outdated

**Solutions:**
1. Refresh dashboard page
2. Check if API is caching (shouldn't be)
3. Verify database is being written to
4. Check created_at timestamps

---

## 📱 Mobile Considerations

### Dashboard on Mobile

**Works but limited:**
- Some UI elements may be cramped
- Desktop browser required
- Better on tablet than phone

**Recommendation:** Use desktop for dashboard tasks

### Discord on Mobile

**Fully Optimized:**
- All slash commands work
- Modals are mobile-friendly
- Ephemeral messages work great
- Push notifications enabled

**Recommendation:** Primary mobile interface

---

## 🔐 Security Notes

### Dashboard Security

- Served over HTTPS
- No authentication built-in (add if needed)
- Direct database access
- Consider adding login system

### Discord Security

- OAuth2 authentication via Discord
- Permission-based access
- Role-restricted commands
- Ephemeral responses for privacy

### API Security

- CORS enabled for dashboard
- Bot authentication for Discord
- Rate limiting recommended
- HTTPS required

---

## 📚 Summary

**Dashboard = Visual + Desktop + Management**
**Discord = Quick + Mobile + Real-time**
**Database = Single Source of Truth**

Use both together for maximum efficiency!

---

**Last Updated:** December 2025
**Compatible Versions:**
- Dashboard: v18+
- Bot: main.py latest
- API: Flask on Railway
