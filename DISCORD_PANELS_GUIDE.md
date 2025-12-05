# Discord Panels Integration Guide

Complete guide for the Discord panel modal system integrated into the Admin Panel.

---

## Overview

The Admin Panel now includes web-based forms for all Discord panel commands, allowing admins to trigger Discord modal submissions directly from the web interface without needing to be in Discord.

### What's Included:

1. **🏢 Office Team Panel** - 5 operations for office staff coordination
2. **📋 Move-Up Panel** - 5 job types for prioritizing customer appointments
3. **📊 Management Panel** - 5 management tools for internal operations
4. **🚨 Alert System** - 4 alert types for employee notifications
5. **🆘 Swamped Alert** - Emergency alert system for office assistance

---

## 1. 🏢 Office Team Panel

**Discord Command:** `@officepanel`
**Admin Panel Section:** "Office Team Panel"
**API Endpoint:** `POST /api/office-team`

### Operations:

#### 1. ATS IT Issue
Report issues with the ATS (Applicant Tracking System).

**Fields:**
- Operation Type: "ATS IT Issue"
- Title: Brief issue description
- Description: Detailed problem description
- Urgency: Low / Medium / High
- Issue Type: Login, Data, Performance, Other
- Affected Module: Which part of ATS
- Error Message: Any error messages seen

**Routes to:** IT channel
**Saves to DB:** Yes (task_type: 'office-team', category: 'ATS IT Issue')

#### 2. Shift Cover
Request shift coverage for office staff.

**Fields:**
- Operation Type: "Shift Cover"
- Title: Shift needing coverage
- Description: Details about the shift
- Urgency: Low / Medium / High
- Date: Date needing coverage
- Shift: Morning / Afternoon / Evening / Full Day
- Reason: Why coverage is needed
- Preferred Replacement: Suggested person

**Routes to:** Operations channel
**Saves to DB:** Yes (task_type: 'office-team', category: 'Shift Cover')

#### 3. FR IT Issue
Report issues with Field Routes software.

**Fields:**
- Operation Type: "FR IT Issue"
- Title: Brief issue description
- Description: Detailed problem
- Urgency: Low / Medium / High
- Module: Scheduling / Routing / Reporting / Billing / Other
- Error Code: Any error codes
- Impact: How many users affected

**Routes to:** IT channel
**Saves to DB:** Yes (task_type: 'office-team', category: 'FR IT Issue')

#### 4. Recruitment
Submit recruitment requests for new positions.

**Fields:**
- Operation Type: "Recruitment"
- Title: Position title
- Description: Position details
- Urgency: Low / Medium / High
- Position: Technician / Office / Management
- Headcount: Number needed
- Requirements: Required qualifications
- Start Date: Desired start date

**Routes to:** HR channel
**Saves to DB:** Yes (task_type: 'office-team', category: 'Recruitment')

#### 5. Pending Cancellation
Log customers attempting to cancel service.

**Fields:**
- Operation Type: "Pending Cancellation"
- Title: Customer name
- Description: Cancellation details
- Urgency: Low / Medium / High
- Customer: Full customer name
- Reason: Why they want to cancel
- Attempted Save: What offers were made
- Follow-up: Recommended next steps

**Routes to:** Customer service channel
**Saves to DB:** Yes (task_type: 'office-team', category: 'Pending Cancellation')

### Example API Call:

```javascript
fetch('https://bottyotty-production.up.railway.app/api/office-team', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    operationType: 'ATS IT Issue',
    title: 'Login system not working',
    description: 'Users unable to log in to ATS portal',
    urgency: 'high',
    details: {
      issue_type: 'Login',
      affected_module: 'Authentication',
      error_message: 'Invalid credentials (but they are correct)'
    }
  })
})
```

---

## 2. 📋 Move-Up Panel

**Discord Command:** `@moveuppanel`
**Admin Panel Section:** "Move-Up Panel"
**API Endpoint:** `POST /api/move-up`

### Job Types:

#### 1. 🪲 Pest Job
Prioritize a general pest control appointment.

#### 2. 🐀 Rodent Job
Prioritize a rodent control appointment.

#### 3. 💩 Insulation Job
Prioritize an insulation inspection/installation.

#### 4. 🤑 Sales Inspection
Prioritize a sales inspection appointment.

#### 5. 🐜 Termite Job
Prioritize a termite inspection/treatment.

### Common Fields (All Job Types):

- **Job Type:** Pest / Rodent / Insulation / Sales / Termite
- **Customer:** Full customer name
- **Phone:** Customer phone number
- **Address:** Service address
- **Reason:** Why job needs to move up (Cancellation / Reschedule / Urgent / Callback)
- **Priority:** Low / Medium / High
- **Notes:** Additional details

**Routes to:** #move-up-log channel + Operations channel
**Saves to DB:** Yes (task_type: 'move-up', category: job type)

### Example API Call:

```javascript
fetch('https://bottyotty-production.up.railway.app/api/move-up', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jobType: 'Pest',
    customer: 'John Smith',
    phone: '555-1234',
    address: '123 Main St, Dallas, TX',
    reason: 'Customer called with urgent pest issue - roaches in kitchen',
    priority: 'high',
    notes: 'Customer is elderly and needs help ASAP'
  })
})
```

---

## 3. 📊 Management Panel

**Discord Command:** `@managementpanel`
**Admin Panel Section:** "Management Panel"
**API Endpoint:** `POST /api/management-panel`

### Tools:

#### 1. 📊 Weekly Reservice
Track weekly reservice statistics.

**Fields:**
- Tool Type: "Weekly Reservice"
- Title: Week identifier (e.g., "Week of Dec 1-7")
- Content: Summary
- Week Of: Date
- Total: Total reservices
- Resolved: Number resolved
- Pending: Number pending
- Notes: Additional notes

**Privacy:** Public (posts to management channel)

#### 2. 🔐 Manager Password
Securely store manager passwords for company systems.

**Fields:**
- Tool Type: "Manager Password"
- Title: System name
- Content: Username
- System: Which system/platform
- Password: The password
- Notes: Access instructions

**Privacy:** **Ephemeral** (does NOT post to Discord, only saved to DB)

#### 3. 📝 Meeting Notes
Document meeting notes for management.

**Fields:**
- Tool Type: "Meeting Notes"
- Title: Meeting title
- Content: Meeting notes
- Date: Meeting date
- Attendees: Who attended
- Action Items: Follow-up tasks

**Privacy:** Public (posts to management channel)

#### 4. 📄 Manager Document
Share important documents with management.

**Fields:**
- Tool Type: "Manager Document"
- Title: Document name
- Content: Description
- Category: Policy / Procedure / Form / Report / Other
- Link: Document URL
- Tags: Search tags

**Privacy:** Public (posts to management channel)

#### 5. 🎓 Manager Tutorial
Create tutorials for company software/procedures.

**Fields:**
- Tool Type: "Manager Tutorial"
- Title: Tutorial name
- Content: Tutorial content
- Software: Which software/system
- Steps: Step-by-step instructions
- Difficulty: Beginner / Intermediate / Advanced

**Privacy:** Public (posts to management channel)

### Example API Call:

```javascript
fetch('https://bottyotty-production.up.railway.app/api/management-panel', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    toolType: 'Weekly Reservice',
    title: 'Week of December 1-7, 2025',
    content: 'Weekly reservice summary for first week of December',
    details: {
      week_of: '2025-12-01',
      total: 45,
      resolved: 38,
      pending: 7,
      notes: 'Great week! 84% resolution rate'
    }
  })
})
```

---

## 4. 🚨 Alert System

**Discord Command:** `/alert`
**Admin Panel Section:** "Alert System"
**API Endpoint:** `POST /api/alert`

### Alert Types:

#### 1. ⏰ Time Update
Notify management of time changes or delays.

**Fields:**
- Alert Type: "Time Update"
- Title: Brief description
- Message: Update details
- Urgency: Low / Medium / High
- Update Type: Running Late / Running Early / Schedule Change
- Estimated Time: New ETA
- Reason: Why the change

#### 2. 📸 Customer Evidence
Submit customer evidence (photos, videos, documents).

**Fields:**
- Alert Type: "Customer Evidence"
- Title: Customer name
- Message: Evidence description
- Urgency: Low / Medium / High
- Evidence Type: Photo / Video / Document / Other
- Link: URL to evidence
- Context: What it shows

#### 3. 📅 Pending Appointment
Alert about appointments needing action.

**Fields:**
- Alert Type: "Pending Appointment"
- Title: Customer name
- Message: Appointment details
- Urgency: Low / Medium / High
- Date: Appointment date
- Status: Needs Confirmation / Needs Reschedule / Other
- Notes: Additional info

#### 4. 📢 General Alert
Send general alerts to management.

**Fields:**
- Alert Type: "General Alert"
- Title: Alert title
- Message: Alert message
- Urgency: Low / Medium / High
- Category: Operational / Customer / Employee / Other

**Routes to:** #management-alerts channel
**Saves to DB:** No (alerts are ephemeral)

### Example API Call:

```javascript
fetch('https://bottyotty-production.up.railway.app/api/alert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    alertType: 'Time Update',
    title: 'Running late to appointment',
    message: 'Truck broke down, will be 30 minutes late to 2pm appointment',
    urgency: 'high',
    details: {
      update_type: 'Running Late',
      estimated_time: '2:30 PM',
      reason: 'Vehicle breakdown - tire blowout on highway'
    }
  })
})
```

---

## 5. 🆘 Swamped Alert

**Admin Panel Section:** "Swamped Alert"
**API Endpoint:** `POST /api/swamped-alert`

### Purpose:
Emergency alert system for when the office is overwhelmed and needs immediate help from available staff.

### Fields:
- **Message:** Alert message describing the situation
- **Recipients:** All Team Members / Managers Only / Specific Users
- **Channel ID:** (Optional) Discord channel to post to

### Behavior:
- Posts red alert embed to Discord with @everyone mention (if "All" selected)
- Displays in BottyOtty Dashboard as red banner for all users
- Stored in localStorage (`bottyotty-swamped-alert`)
- Can be cleared from Admin Panel or Dashboard

### Example API Call:

```javascript
fetch('https://bottyotty-production.up.railway.app/api/swamped-alert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Office is extremely busy! Phones ringing non-stop. Need help ASAP!',
    recipients: 'all',
    channelId: '1445619376832254054'  // office-alerts channel
  })
})
```

### Frontend Integration:
The Dashboard checks for active swamped alerts every 30 seconds:

```javascript
// In BottyOtty Dashboard v18.html
useEffect(() => {
  const checkSwampedAlert = () => {
    const alert = JSON.parse(localStorage.getItem('bottyotty-swamped-alert') || 'null');
    if (alert && alert.active) {
      // Show red pulsing banner at top
    }
  };

  checkSwampedAlert();
  const interval = setInterval(checkSwampedAlert, 30000);
  return () => clearInterval(interval);
}, []);
```

---

## Database Schema

All Discord panel submissions (except Alerts and Swamped Alerts) are saved to `tasks.db`:

### Office Team Operations:
```sql
INSERT INTO tasks (
  title, description, created_by, task_type, category, status, created_at
) VALUES (
  'ATS IT Issue: Login system not working',
  'Users unable to log in...',
  'Admin Panel',
  'office-team',
  'ATS IT Issue',
  'open',
  '2025-12-05T10:30:00'
);
```

### Move-Up Jobs:
```sql
INSERT INTO tasks (
  title, description, created_by, task_type, category, status, created_at
) VALUES (
  'Pest Move-Up: John Smith',
  'Phone: 555-1234\nAddress: 123 Main St...',
  'Admin Panel',
  'move-up',
  'Pest',
  'open',
  '2025-12-05T11:00:00'
);
```

### Management Tools:
```sql
INSERT INTO tasks (
  title, description, created_by, task_type, category, status, created_at
) VALUES (
  'Weekly Reservice: Week of Dec 1-7',
  'Weekly reservice summary...',
  'Admin Panel',
  'management',
  'Weekly Reservice',
  'open',
  '2025-12-05T09:00:00'
);
```

---

## Channel Routing

Each Discord panel posts to specific channels configured in `CONFIG`:

| Panel | Channel Key | Default Channel |
|-------|------------|----------------|
| Office Team | `global_logs.office_operations` | #office-operations-log |
| Move-Up | `global_logs.move_up` | #move-up-log |
| Management | `special_channels.management_alerts` | #🚨alerts (management) |
| Alert System | `special_channels.management_alerts` | #🚨alerts (management) |
| Swamped Alert | Custom (user provides channel ID) | Any channel |

### Configuring Channels:

Update `CONFIG` in `main.py`:

```python
CONFIG = {
    "global_logs": {
        "office_operations": 1234567890123456789,
        "move_up": 1234567890123456789,
    },
    "special_channels": {
        "management_alerts": 1445630201223450778,
    }
}
```

Or configure via Admin Panel → Discord Config section.

---

## Admin Panel Usage

### Accessing Discord Panels:

1. Open **Admin Panel v18.html**
2. Use sidebar navigation or search bar
3. Click on desired panel section:
   - 🏢 Office Team Panel
   - 📋 Move-Up Panel
   - 📊 Management Panel
   - 🚨 Alert System
   - 🆘 Swamped Alert

### Submitting Forms:

1. Fill out all required fields (marked with *)
2. Select appropriate urgency/priority
3. Click "Submit" button
4. Notification appears confirming submission
5. Form auto-clears for next submission

### Viewing Submissions:

- Check Discord channels for embeds
- View in **BottyOtty Reports** for database queries
- Filter by `task_type` and `category` in reports

---

## Troubleshooting

### Form not submitting:
- Check all required fields are filled
- Check browser console for errors
- Verify API endpoint is accessible (check Network tab)

### Discord embed not appearing:
- Verify bot is online (`/api/health` endpoint)
- Check channel IDs in CONFIG are correct
- Verify bot has permissions in target channels
- Check Railway logs for errors

### Database not saving:
- Verify `tasks.db` exists and is writable
- Check `add_task()` function in main.py
- Review Flask logs for SQL errors

### Wrong channel:
- Update channel IDs in CONFIG
- Push updated config via Admin Panel
- Restart bot if necessary

---

## API Response Format

### Success:
```json
{
  "success": true,
  "message": "Operation type operation submitted"
}
```

### Error:
```json
{
  "success": false,
  "error": "Operation type and title required"
}
```

---

## Security Considerations

1. **Manager Passwords:** Not posted to Discord, only saved to database
2. **Swamped Alerts:** Can mention @everyone - use sparingly
3. **API Authentication:** Currently open - consider adding auth tokens
4. **Input Validation:** All inputs sanitized before Discord posting
5. **Channel Permissions:** Ensure bot has proper channel access

---

## Future Enhancements

- [ ] Add user authentication to API endpoints
- [ ] Implement rate limiting on alert endpoints
- [ ] Add file upload support for evidence
- [ ] Create approval workflow for move-ups
- [ ] Add email notifications for high-urgency items
- [ ] Create analytics dashboard for panel usage
- [ ] Add mobile app integration
- [ ] Implement webhook notifications

---

**Last Updated:** December 5, 2025
**Admin Panel Version:** v18 (9,887 lines)
**main.py Version:** 5,895 lines
**Total Discord Panels:** 5 (20+ operations total)
