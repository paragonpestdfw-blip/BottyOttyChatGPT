# Automated Reports & Logs System

## Overview
BottyOtty now has automated scheduled reports that can be configured to run daily, weekly, or monthly. Reports are automatically sent to the `#🤖reports` Discord channel.

**Default Schedule:** Weekly on Friday mornings at 9:00 AM

---

## Features

### 📊 Report Types

1. **Task Summary Report**
   - Total tasks created in past 7 days
   - Completed, in progress, pending, and overdue counts
   - Completion rate percentage
   - Top 5 performers (most tasks completed)

2. **Activity Log Summary**
   - Counts of bot-logged entries across all log channels:
     - 🔨 Damage Reports (#damages-log)
     - 🚗 Fleet Issues (#fleet-log)
     - 📚 Training Events (#training-log)
     - ⚠️ Safety Incidents (#safety-and-accident-log)
     - 💬 Customer Feedback (#customer-feedback-log)
     - 🔔 Tech Reminders (#tech-reminders-log)
     - 📦 Inventory Updates (#inventory-log)
     - 🏢 Office Operations (#office-operations-log)

3. **Training Report**
   - Recent trainings from past 30 days
   - Presenter names
   - Attendee counts

4. **Inventory Report**
   - Weekly inventory check reminder
   - Links to #inventory-log for updates

---

## Configuration

### Method 1: Via Admin Panel (Recommended)

The Admin Panel has `reportSchedule` configuration built-in. It syncs to the bot automatically when you click "💾 Save Configuration to Bot".

**Report Schedule Settings:**
```javascript
{
  enabled: false,              // Set to true to enable automated reports
  schedule_type: 'weekly',     // 'daily', 'weekly', or 'monthly'
  day: 'Friday',              // For weekly: 'Monday', 'Tuesday', etc.
  day_of_month: 1,            // For monthly: 1-31
  hour: 9,                    // Hour of day (0-23, 24-hour format)
  report_types: [             // Which reports to generate
    'tasks',
    'logs',
    'training',
    'inventory'
  ]
}
```

**Steps to Configure in Admin Panel:**
1. Open Admin Panel (`Admin Panel v18.html`)
2. Scroll to report configuration section (will be added in future UI update)
3. Or manually edit in browser console:
   ```javascript
   // In browser console on Admin Panel page
   setReportSchedule({
     enabled: true,
     schedule_type: 'weekly',
     day: 'Friday',
     hour: 9,
     report_types: ['tasks', 'logs', 'training', 'inventory']
   })
   ```
4. Click "💾 Save Configuration to Bot"
5. Confirm you see "✅ Configuration synced to bot successfully!"

### Method 2: Direct File Edit

Edit `bot_config.json` directly on your server:

```json
{
  "report_schedule": {
    "enabled": true,
    "schedule_type": "weekly",
    "day": "Friday",
    "hour": 9,
    "report_types": ["tasks", "logs", "training", "inventory"]
  }
}
```

Then restart the bot to load the new configuration.

---

## Schedule Types

### Daily Reports
Runs every day at the specified hour.

```json
{
  "enabled": true,
  "schedule_type": "daily",
  "hour": 9,
  "report_types": ["tasks", "logs"]
}
```

**Example:** Daily reports at 9:00 AM

### Weekly Reports (DEFAULT)
Runs once per week on the specified day at the specified hour.

```json
{
  "enabled": true,
  "schedule_type": "weekly",
  "day": "Friday",
  "hour": 9,
  "report_types": ["tasks", "logs", "training", "inventory"]
}
```

**Example:** Weekly reports every Friday at 9:00 AM

**Valid Days:** Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday

### Monthly Reports
Runs once per month on the specified day of the month.

```json
{
  "enabled": true,
  "schedule_type": "monthly",
  "day_of_month": 1,
  "hour": 9,
  "report_types": ["tasks", "logs", "training"]
}
```

**Example:** Monthly reports on the 1st of each month at 9:00 AM

---

## Report Customization

### Selecting Report Types

You can enable/disable specific report types by modifying the `report_types` array:

```json
{
  "report_types": [
    "tasks",       // Task summary report
    "logs",        // Activity log summary
    "training",    // Training report
    "inventory"    // Inventory reminder
  ]
}
```

**Examples:**

**Tasks and Logs Only:**
```json
"report_types": ["tasks", "logs"]
```

**Just Training Reports:**
```json
"report_types": ["training"]
```

**All Reports:**
```json
"report_types": ["tasks", "logs", "training", "inventory"]
```

---

## How It Works

### 1. Schedule Check Loop
- Bot runs `check_scheduled_reports()` every hour
- Checks if current day/time matches configured schedule
- Prevents duplicate runs using `last_report_run.txt` tracker

### 2. Report Generation
When schedule matches:
- Loads configuration from `bot_config.json`
- Generates selected report types
- Sends formatted embeds to #🤖reports channel

### 3. Duplicate Prevention
- Saves last run timestamp to `last_report_run.txt`
- Format: `YYYY-MM-DD-HH` (e.g., `2025-12-04-09`)
- If already ran this hour, skips execution

---

## Example Reports

### Task Summary Report
```
📋 Task Summary (Past 7 Days)

Total Tasks: 47
✅ Completed: 35
📊 In Progress: 8
⏳ Pending: 4
⚠️ Overdue: 2
Completion Rate: 74.5%

🌟 Top Performers:
Caleb: 12 tasks
Dakota: 10 tasks
Joey: 8 tasks
Preston: 5 tasks
Adam: 4 tasks
```

### Activity Log Summary
```
📝 Activity Log Summary (Past 7 Days)

🔨 Damage Reports: 3 entries
🚗 Fleet Issues: 7 entries
📚 Training Events: 2 entries
⚠️ Safety Incidents: 1 entries
💬 Customer Feedback: 15 entries
📦 Inventory Updates: 4 entries
```

### Training Report
```
📚 Training Report (Past 30 Days)

Safety Protocol Updates
Date: 2025-12-01
Presenter: Dakota
Attendees: 23

New Software Training
Date: 2025-11-28
Presenter: Joey
Attendees: 18
```

---

## Testing & Manual Triggers

### Test the Reporting System

You can manually trigger a report run for testing:

1. **Via Admin Panel API:**
   ```javascript
   // Set schedule to run in next hour
   const now = new Date();
   const config = {
     "report_schedule": {
       "enabled": true,
       "schedule_type": "weekly",
       "day": now.toLocaleDateString('en-US', {weekday: 'long'}),
       "hour": now.getHours() + 1,
       "report_types": ["tasks", "logs"]
     }
   };

   // Save and wait for next hour
   ```

2. **Quick Test (Direct Function Call):**
   Add this slash command to main.py for testing:
   ```python
   @bot.tree.command(name="test_reports")
   async def test_reports(interaction: discord.Interaction):
       """Manually trigger report generation (Owners only)"""
       # Check if user is owner (Megan or Chase)
       if interaction.user.id not in [928725439059464222, 1297804315041333354]:
           await interaction.response.send_message("❌ Owners only", ephemeral=True)
           return

       await interaction.response.send_message("🔄 Generating reports...", ephemeral=True)
       await generate_and_send_reports()
   ```

### Check If Reports Are Running

**Check Bot Logs:**
```bash
# Railway
railway logs | grep "Scheduled reports"

# Heroku
heroku logs --tail | grep "Scheduled reports"

# Local/VPS
# Look for: "✅ Scheduled reports task started"
# And: "✅ Automated reports sent to #🤖reports"
```

**Check last_report_run.txt:**
```bash
cat last_report_run.txt
# Should show: YYYY-MM-DD-HH of last run
```

---

## Troubleshooting

### Reports Not Running

**1. Check if enabled:**
```json
// In bot_config.json
"report_schedule": {
  "enabled": true  // ← Must be true
}
```

**2. Check schedule matches:**
- If `schedule_type: 'weekly'` and `day: 'Friday'`, reports only run on Fridays
- If `hour: 9`, reports only run during the 9:00 AM hour
- Bot checks every hour on the hour

**3. Check reports channel exists:**
- Channel ID must be in `CONFIG['global_logs']['reports']`
- Currently: `1446273562548899901` (#🤖reports)
- Bot must have permission to send messages there

**4. Check bot logs for errors:**
```bash
railway logs | grep "Error in check_scheduled_reports"
# or
railway logs | grep "Error generating reports"
```

**5. Verify task is running:**
```bash
railway logs | grep "Scheduled reports task started"
# Should see on bot startup
```

### Reports Running But Empty

**No task data:**
- Check if tasks exist in database: `SELECT COUNT(*) FROM tasks`
- Ensure tasks have `created_at` timestamps

**No log data:**
- Bot counts messages in log channels from past 7 days
- If log channels are empty, report will show no entries

**No training data:**
- Requires `trainings` and `training_attendance` tables
- If tables don't exist, training report is skipped

### Wrong Schedule Time

**Time Zone Issues:**
- Bot uses server time (likely UTC)
- If server is UTC and you want 9 AM EST, set `hour: 14` (9 AM EST = 2 PM UTC)
- Check server time: `date` command on server

**Daylight Saving Time:**
- May need to adjust `hour` when DST changes
- Consider using UTC-relative times

---

## Advanced Configuration

### Custom Report Timing

**Early Morning Reports (6 AM):**
```json
{
  "enabled": true,
  "schedule_type": "weekly",
  "day": "Monday",
  "hour": 6,
  "report_types": ["tasks"]
}
```

**End of Day Reports (5 PM):**
```json
{
  "enabled": true,
  "schedule_type": "daily",
  "hour": 17,
  "report_types": ["tasks", "logs"]
}
```

**Multiple Weekly Reports:**
You can only have one schedule, but you could modify code to support multiple schedules in the future.

### Customizing Report Content

Edit the report generation functions in `main.py`:

**Change Task Report Time Period (lines 3297-3305):**
```python
# Change from 7 days to 30 days
WHERE created_at >= datetime('now', '-30 days')
```

**Change Top Performers Limit (line 3332):**
```python
LIMIT 10  # Show top 10 instead of top 5
```

**Modify Log Summary Period (line 3374):**
```python
week_ago = datetime.now() - timedelta(days=30)  # 30 days instead of 7
```

---

## API Integration

The Admin Panel sends the report schedule to the bot via `/api/admin-config`:

**Request:**
```json
POST /api/admin-config
Content-Type: application/json

{
  "reportSchedule": {
    "enabled": true,
    "schedule_type": "weekly",
    "day": "Friday",
    "hour": 9,
    "report_types": ["tasks", "logs", "training", "inventory"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Configuration updated successfully",
  "timestamp": "2025-12-04T12:00:00.000Z"
}
```

The bot saves this to `bot_config.json` for persistence across restarts.

---

## Benefits for Owners (Megan & Chase)

✅ **Weekly Overview** - Every Friday morning, get a comprehensive summary
✅ **Performance Tracking** - See top performers and completion rates
✅ **Activity Monitoring** - Track log activity across all categories
✅ **Training Accountability** - Monitor training attendance
✅ **Automated** - No manual work required, reports generate automatically
✅ **Customizable** - Adjust schedule and report types as needed
✅ **Centralized** - All reports in one place (#🤖reports)

---

## Future Enhancements

Potential features to add:

- [ ] UI in Admin Panel for configuring schedules
- [ ] Multiple schedules (e.g., daily tasks + weekly full report)
- [ ] Report delivery to multiple channels
- [ ] Custom report templates
- [ ] Report export to PDF/Excel
- [ ] Email reports to owners
- [ ] Department-specific reports
- [ ] Trend analysis (week-over-week comparison)
- [ ] Alert thresholds (e.g., if completion rate < 70%)

---

## Quick Reference

| Setting | Values | Description |
|---------|--------|-------------|
| `enabled` | `true` / `false` | Enable/disable automated reports |
| `schedule_type` | `'daily'` / `'weekly'` / `'monthly'` | How often to run |
| `day` | `'Monday'` - `'Sunday'` | Day of week (weekly only) |
| `day_of_month` | `1` - `31` | Day of month (monthly only) |
| `hour` | `0` - `23` | Hour of day (24-hour format) |
| `report_types` | Array of strings | Which reports to include |

**Report Type Options:**
- `'tasks'` - Task summary
- `'logs'` - Activity log summary
- `'training'` - Training report
- `'inventory'` - Inventory reminder

---

*Last updated: December 2025*
*Related files: `main.py` (lines 3163-3449), `Admin Panel v18.html`*
