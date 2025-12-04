# Discord Setup Guide

Complete guide for setting up your Discord server to work with BottyOtty.

---

## 📋 Table of Contents

1. [Required Channels](#required-channels)
2. [Optional Channels](#optional-channels)
3. [Panel Setup](#panel-setup)
4. [Permissions](#permissions)
5. [Testing](#testing)

---

## 🎯 Required Channels

### 1. Management & Alerts
Create these channels for core bot functionality:

**#management-alerts**
- Purpose: Employee → Management alerts via `/alert` command
- Who posts: Employees using time updates, customer evidence, appointments, general alerts
- Who monitors: Management team
- Permissions: @everyone can view, bot can post

**#office-alerts**
- Purpose: Management → Team alerts from Office Alerts web interface
- Who posts: Management via web dashboard
- Who monitors: All staff
- Permissions: @everyone can view, bot can post

**#calendar-events**
- Purpose: Calendar event announcements
- Who posts: Bot when events are created
- Who monitors: All staff
- Permissions: @everyone can view, bot can post

### 2. Employee Log Channels (Per Employee)
Create individual log channels for each employee (optional but recommended):

Format: `#employee-{name}-log`

Examples:
- `#employee-joey-log`
- `#employee-presley-log`
- `#employee-lauren-log`

These channels receive:
- Personal request submissions
- Task assignments
- Individual activity tracking

---

## 🔧 Optional Channels

### Log Channels (9 Types)
If you want the `/logs` command to post log entries, create these:

1. **#damages-log** - Equipment/property damage reports
2. **#fleet-reporting-log** - Vehicle status and maintenance
3. **#training-log** - Training sessions and certifications
4. **#safety-log** - Safety incidents and observations
5. **#customer-feedback-log** - Customer reviews and feedback
6. **#tech-reminders-log** - Technical reminders and followups
7. **#inventory-log** - Inventory changes and orders
8. **#move-up-log** - Job prioritization entries
9. **#office-operations-log** - Office team activities

**Note:** Logs will still work without dedicated channels - they'll just post to the channel where the command was run.

### Additional Channels

**#reports**
- Purpose: Generated reports from `/reports` command
- Optional: Reports can be sent as ephemeral (private) messages instead

**#policy-updates**
- Purpose: Announcements when policies change
- Manual posting by management

**#kb-updates**
- Purpose: Notifications about new knowledge base articles
- Manual posting by management

---

## 🎛️ Panel Setup

Panels are interactive message interfaces that give users access to modals and forms.

### Request Panel
Post in employee log channels or a general requests channel:

```
@requestpanel
```

Provides access to:
- 16 request types (extra routes, print materials, safety gear, vehicles, etc.)
- 8 report types (WPI, damage reports, car accidents, spills, etc.)
- Quick buttons for call-outs, hours updates, tech collections

### Office Team Panel
Post in management or office staff channel:

```
@officepanel
```

Provides access to:
- ATS IT Issues
- Shift Cover Requests
- FieldRoutes IT Issues
- Recruitment Requests
- Pending Cancellations

### Move-Up Panel
Post in operations or management channel:

```
@moveuppanel
```

Provides access to:
- Pest Job Move-Ups
- Rodent Job Move-Ups
- Insulation Job Move-Ups
- Sales Inspection Move-Ups
- Termite Job Move-Ups

### Management Panel
Post in management-only channel:

```
@managementpanel
```

Provides access to:
- Weekly Reservice Reports
- Manager Password Storage
- Meeting Notes
- Manager Documents
- Manager Tutorials

**Important:**
- Pin these panels so they're always accessible
- Only administrators can post panels
- Panels are persistent - they work even after bot restarts

---

## 🔐 Permissions

### Bot Permissions Required

The bot needs these permissions in ALL channels:
- ✅ View Channels
- ✅ Send Messages
- ✅ Send Messages in Threads
- ✅ Embed Links
- ✅ Attach Files
- ✅ Read Message History
- ✅ Add Reactions
- ✅ Use External Emojis
- ✅ Manage Events (for Discord scheduled events)

### Administrator Commands

These commands require Administrator permission:
- `@requestpanel` - Post request panel
- `@officepanel` - Post office team panel
- `@moveuppanel` - Post move-up panel
- `@managementpanel` - Post management panel
- `@exportstructure` - Export server structure

### Channel Permissions

**Management Channels:**
- Only management roles can view
- Bot must have access

**Employee Log Channels:**
- Individual employee + management can view
- Bot must have access

**Public Channels:**
- @everyone can view
- Bot must have access

---

## ✅ Testing

After setup, test each system:

### 1. Test Alert System
```
/alert
```
- Choose "Time Update"
- Fill out modal
- Verify message appears in #management-alerts

### 2. Test Calendar
```
/calendar add
```
- Create a test event
- Check it appears in `/calendar view`
- Verify Discord scheduled event created in Server Events

### 3. Test Request Panel
- Post `@requestpanel` in a test channel
- Click a request type
- Fill out modal
- Verify submission posts correctly

### 4. Test Reports
```
/reports
```
- Choose "Request Statistics"
- Select date range
- Verify report generates

### 5. Test Policies
```
/policy
```
- Choose "Safety Policies"
- Verify policies display correctly

### 6. Test Knowledge Base
```
/kb
```
- Choose "Troubleshooting"
- Verify articles display

### 7. Test Logs
```
/logs
```
- Choose a log type
- Select date range
- Verify logs display

---

## 🚀 Quick Start Checklist

- [ ] Create #management-alerts channel
- [ ] Create #office-alerts channel
- [ ] Create #calendar-events channel
- [ ] Create employee log channels (optional)
- [ ] Post @requestpanel in employee channels
- [ ] Post @officepanel in office channel
- [ ] Post @moveuppanel in operations channel
- [ ] Post @managementpanel in management channel
- [ ] Pin all panels
- [ ] Test each slash command
- [ ] Configure bot permissions
- [ ] Train team on slash commands

---

## 💡 Pro Tips

1. **Use Threads** - Create threads under panel messages for specific discussions
2. **Pin Panels** - Always pin panels so they're easy to find
3. **Channel Categories** - Organize channels in categories like "Management", "Logs", "Employees"
4. **Roles** - Create roles for different access levels (Management, Office Staff, Field Techs)
5. **Mobile** - All commands work on Discord mobile app
6. **Ephemeral** - Most slash commands send private responses - only you can see them

---

## 🆘 Troubleshooting

**Panel not responding:**
- Check bot permissions
- Re-post the panel
- Verify bot is online

**Commands not showing:**
- Bot may still be syncing commands
- Wait a few minutes
- Try `/` to see available commands

**Events not creating:**
- Verify bot has "Manage Events" permission
- Check event is in the future
- Date must be YYYY-MM-DD format

**Need Help?**
- Use `/kb` for troubleshooting guides
- Check bot status with web dashboard
- Contact development team

---

**Last Updated:** December 2025
**Bot Version:** v18+
**Compatible with:** Discord.py 2.0+
