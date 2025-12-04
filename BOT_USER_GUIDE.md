# BottyOtty Bot User Guide

Complete guide for using all BottyOtty Discord bot commands and features.

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Slash Commands](#slash-commands)
3. [Panels & Modals](#panels--modals)
4. [Quick Reference](#quick-reference)

---

## 🚀 Getting Started

### How to Use Slash Commands

1. Type `/` in any Discord channel
2. Start typing the command name (e.g., "alert")
3. Select the command from the dropdown
4. Fill in any required options
5. Press Enter to run the command

**Example:**
```
/alert → Select "Time Update" → Fill out modal → Submit
```

### Understanding Ephemeral Messages

Many bot responses are **ephemeral** - only you can see them. Look for this message:
> "Only you can see this"

This keeps channels clean and protects privacy.

---

## 💬 Slash Commands

### 1. `/alert` - Send Alerts to Management

**Purpose:** Notify management about important updates

**Alert Types:**

**⏰ Time Update**
- Clock in/out
- Running late
- Schedule changes
- Example: "Running 15 minutes late due to traffic"

**📸 Customer Evidence**
- Photos of pest activity
- Before/after treatment photos
- Property damage documentation
- Example: Submit termite damage photos with customer info

**📅 Pending Appointment**
- Upcoming job alerts
- Appointment confirmations
- Scheduling issues
- Example: "Customer requested reschedule to Friday 2PM"

**📢 General Alert**
- Questions for management
- Issues or concerns
- Updates
- Requests
- Example: "Need approval for extra materials on Johnson job"

**How to Use:**
```
/alert
→ Choose alert type
→ Fill out modal form
→ Submit
```

**What Happens:**
- Alert posts to #management-alerts channel
- Management gets notified
- You get confirmation message

---

### 2. `/calendar` - View & Manage Calendar Events

**Purpose:** Access company calendar and add events

**Actions:**

**View Upcoming Events**
- Shows next 20 calendar events
- Displays date, type, and description
- Private response (only you see it)

**Add New Event**
- Opens modal to create event
- Posts to channel when created
- Creates Discord scheduled event automatically

**This Month**
- Shows all events for current month
- Grid display with emojis
- Easy month-at-a-glance view

**Event Types:**
- 🎂 Birthday
- 💰 Pay Day
- 📦 Supply Day
- 🎉 Anniversary
- 💍 Wedding
- 💻 Office Night
- 🎮 Game Night
- 🏢 Company Event
- 🎊 Holiday
- 📚 Training
- 👥 Meeting
- 📌 Custom Event

**How to Use:**
```
/calendar add
→ Enter event title
→ Enter date (YYYY-MM-DD)
→ Enter event type
→ Add description (optional)
→ Submit
```

**Result:** Event appears in:
1. Discord database
2. Web calendar dashboard
3. Server's Events tab (with RSVP)
4. #calendar-events channel

---

### 3. `/logs` - View Historical Logs

**Purpose:** Access log entries from specific channels

**Log Types:**
- Damages Log
- Fleet Reporting Log
- Training Log
- Safety Log
- Customer Feedback Log
- Tech Reminders Log
- Inventory Log
- Move-Up Log
- Office Operations Log

**Date Ranges:**
- Last 7 days
- Last 30 days
- Last 90 days
- Custom range (specify start/end dates)

**How to Use:**
```
/logs
→ Choose log type
→ Select date range
→ (If custom) Enter start/end dates
→ Submit
```

**Result:**
- First 10 entries shown in embed
- Full export sent to your DMs
- Formatted with timestamps and details

---

### 4. `/reports` - Generate Statistics

**Purpose:** Create formatted reports with statistics

**Report Types:**

**Damages Report**
- All damage incidents
- Grouped by category
- Shows incident counts
- Date range filtered

**Fleet Reporting**
- Vehicle status reports
- Maintenance issues
- Fleet statistics

**Weekly Reservice Summary**
- Reserves completed this week
- Pending reserves
- Success metrics

**Move-Up Summary**
- Job prioritization stats
- By category (Pest, Rodent, Insulation, Sales, Termite)
- Total move-ups

**Request Statistics**
- Top request categories
- Request volume
- Trending requests

**Date Options:**
- Last 7 days
- Last 30 days
- This Week
- This Month
- Custom range

**How to Use:**
```
/reports
→ Choose report type
→ Select date range
→ (If custom) Enter dates
→ Submit
```

**Result:**
- Beautiful formatted embed
- Statistics and breakdowns
- Private response
- Can be shared if needed

---

### 5. `/policy` - Access Company Policies

**Purpose:** Quick reference for company policies

**Categories:**

**🦺 Safety Policies**
- Personal Protective Equipment (PPE)
- Vehicle Safety
- Chemical Safety
- Incident Reporting

**👥 HR Policies**
- Attendance Policy
- Paid Time Off (PTO)
- Code of Conduct
- Dress Code

**⚙️ Operations**
- Scheduling
- Customer Service
- Quality Standards
- Equipment Care

**💰 Payroll & Compensation**
- Timekeeping
- Pay Schedule
- Expense Reimbursement
- Commission Structure

**💻 Technology Use**
- Company Phone Policy
- Software Access
- Data Privacy
- Social Media Guidelines

**📋 All Policies (Overview)**
- Shows all categories
- Quick reference list

**How to Use:**
```
/policy
→ Choose category
→ View policies
```

**Result:**
- Detailed policy information
- Bullet-point format
- Private response
- Always up-to-date

---

### 6. `/kb` - Knowledge Base & Resources

**Purpose:** Training materials, troubleshooting, FAQs

**Topics:**

**💻 Software & Tools**
- ATS (Appointment Tracking System)
- FieldRoutes
- Discord Bot Commands
- Mobile Apps

**📚 Training & How-To Guides**
- New Tech Onboarding
- Sales Best Practices
- Treatment Procedures
- Customer Service Excellence

**🔧 Troubleshooting**
- Equipment Problems
- Software Issues
- Customer Complaints
- Weather Delays

**🚨 Emergency Procedures**
- Employee Injury
- Chemical Spill
- Vehicle Accident
- Customer Emergency

**❓ FAQs**
- Pay Questions
- Time Off
- Equipment
- Route Assignments

**📋 All Topics (Index)**
- Complete article list
- Organized by topic

**How to Use:**
```
/kb
→ Choose topic
→ Read articles
```

**Result:**
- Step-by-step guides
- Troubleshooting solutions
- Quick answers
- Private response

---

## 🎛️ Panels & Modals

### Request Panel

**Access:** Posted in employee channels (look for pinned message)

**Components:**

**Requests Dropdown (16 types):**
- Extra Pest Route
- Extra Rodent Route
- Extra Insulation Route
- Extra Termite Route
- Extra Sales Route
- Extra Office Day
- Print Materials
- Safety Gear
- Special Inventory
- Vehicle Issue
- Vehicle Maintenance
- Meeting Request
- Manager - Doc Edits
- Manager - Code Requests
- Route Change Request
- Other Request

**Reports Dropdown (8 types):**
- WPI — Injured
- WPI — Witness
- Damage Report
- Car Accident
- Spill / Chemical Incident
- Customer Evidence
- Vehicle Swap
- Hours Correction Needed

**Quick Buttons:**
- 😷 Call-Out
- ⏱ Hours Update
- 💰 Tech Collections

**How to Use:**
1. Click dropdown or button
2. Fill out modal form
3. Submit
4. Confirmation message appears

---

### Office Team Panel

**Access:** Posted in office staff channels

**Options:**
- 💻 ATS IT Issue - Report ATS technical problems
- 🔄 Shift Cover - Request shift coverage
- ⚙️ FR IT Issue - FieldRoutes technical issues
- 👥 Recruitment - Hiring requests
- ⚠️ Pending Cancellation - Log customer cancellations

**How to Use:**
1. Select operation type
2. Fill out modal
3. Submit to office team

---

### Move-Up Panel

**Access:** Posted in operations channels

**Options:**
- 🪲 Pest Job Move-Up
- 🐀 Rodent Job Move-Up
- 💩 Insulation Job Move-Up
- 🤑 Sales Inspection Move-Up
- 🐜 Termite Job Move-Up

**How to Use:**
1. Select job type
2. Enter customer info
3. Provide reason for move-up
4. Set priority level
5. Submit

**Result:**
- Job added to priority list
- Management notified
- Tracked in database

---

### Management Panel

**Access:** Management channels only

**Options:**
- 📊 Weekly Reservice Report
- 🔐 Manager Password Storage (private)
- 📝 Meeting Notes
- 📄 Manager Document
- 🎓 Manager Tutorial

**How to Use:**
1. Select tool
2. Fill out form
3. Submit
4. Stored in database

---

## 📚 Quick Reference

### Common Tasks

**I'm running late:**
```
/alert → Time Update → Fill details
```

**Need to report damage:**
```
Request Panel → Reports → Damage Report
```

**Check company events:**
```
/calendar → View Upcoming Events
```

**Look up a policy:**
```
/policy → Choose category
```

**Troubleshoot equipment:**
```
/kb → Troubleshooting → Equipment Problems
```

**Request supplies:**
```
Request Panel → Requests → Special Inventory
```

**Add to move-up list:**
```
Move-Up Panel → Select job type → Fill form
```

**Generate weekly report:**
```
/reports → Weekly Reservice Summary → This Week
```

---

## 💡 Pro Tips

1. **Use Tab to Autocomplete** - When typing commands, use Tab to quickly complete
2. **Bookmark Panels** - Right-click panel messages → "Copy Message Link" → Save for quick access
3. **Mobile Friendly** - All commands work great on Discord mobile app
4. **Private by Default** - Most responses are ephemeral (only you see them)
5. **Screenshot Evidence** - Take screenshots before submitting customer evidence alerts
6. **Calendar Reminders** - RSVP to events in Server Events for automatic reminders
7. **Search Policies** - Use Ctrl+F in policy responses to find specific keywords
8. **Export Logs** - Log exports go to your DMs for easy downloading

---

## 🆘 Need Help?

**Can't find a command?**
- Type `/` and browse available commands
- Check pinned panel messages

**Modal not submitting?**
- Fill all required fields (marked with asterisk)
- Check date formats (YYYY-MM-DD)
- Try again if timeout occurs

**Don't see your submission?**
- Check the appropriate channel
- Look for confirmation message
- Contact management if issue persists

**Have a question?**
- Use `/kb` for FAQs
- Use `/policy` for policy questions
- Use `/alert` to ask management

---

## 🎯 Best Practices

1. **Be Specific** - Provide detailed information in alerts and requests
2. **Use Correct Type** - Choose the right alert/request type for your situation
3. **Respond Promptly** - Check Discord regularly for updates
4. **RSVP to Events** - Use Discord's RSVP feature for calendar events
5. **Keep It Professional** - All submissions are logged and reviewed
6. **Document Everything** - Use customer evidence alerts for important documentation
7. **Plan Ahead** - Submit requests with advance notice when possible

---

**Last Updated:** December 2025
**Bot Version:** v18+
**Questions?** Ask your manager or use `/alert` to contact management
