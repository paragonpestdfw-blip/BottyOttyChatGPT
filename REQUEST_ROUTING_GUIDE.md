# Request Routing Guide

Complete breakdown of all requests, modals, and where they route in the BottyOtty system.

---

## 📋 Table of Contents

1. [Request Panel](#request-panel)
2. [Office Team Panel](#office-team-panel)
3. [Move-Up Panel](#move-up-panel)
4. [Management Panel](#management-panel)
5. [Alert System](#alert-system)
6. [Database Structure](#database-structure)
7. [Channel Routing](#channel-routing)

---

## 🎛️ Request Panel

**Command:** `@requestpanel`
**Access:** All employees
**Location:** Employee log channels, general request channels

### Requests Dropdown (16 Types)

#### Extra Routes (6)

| Request Type | Modal | Database Fields | Routing |
|-------------|-------|-----------------|---------|
| Extra Pest Route | GenericRequestModal | task_type: 'form-request'<br>category: 'extra_pest_route' | Employee log channel + Management |
| Extra Rodent Route | GenericRequestModal | task_type: 'form-request'<br>category: 'extra_rodent_route' | Employee log channel + Management |
| Extra Insulation Route | GenericRequestModal | task_type: 'form-request'<br>category: 'extra_insulation_route' | Employee log channel + Management |
| Extra Termite Route | GenericRequestModal | task_type: 'form-request'<br>category: 'extra_termite_route' | Employee log channel + Management |
| Extra Sales Route | GenericRequestModal | task_type: 'form-request'<br>category: 'extra_sales_route' | Employee log channel + Management |
| Extra Office Day | GenericRequestModal | task_type: 'form-request'<br>category: 'extra_office_day' | Employee log channel + Management |

#### General Requests (3)

| Request Type | Modal | Database Fields | Routing |
|-------------|-------|-----------------|---------|
| Print Materials | GenericRequestModal | task_type: 'form-request'<br>category: 'print_materials' | Office team channel |
| Safety Gear | GenericRequestModal | task_type: 'form-request'<br>category: 'safety_gear' | Safety/inventory channel |
| Special Inventory | GenericRequestModal | task_type: 'form-request'<br>category: 'special_inventory' | Inventory channel |

#### Vehicle Requests (2)

| Request Type | Modal | Database Fields | Routing |
|-------------|-------|-----------------|---------|
| Vehicle Issue | VehicleIssueModal | task_type: 'form-request'<br>category: 'Vehicle Issue' | Fleet management channel |
| Vehicle Maintenance | GenericRequestModal | task_type: 'form-request'<br>category: 'vehicle_maintenance' | Fleet management channel |

#### Other Requests (5)

| Request Type | Modal | Database Fields | Routing |
|-------------|-------|-----------------|---------|
| Meeting Request | GenericRequestModal | task_type: 'form-request'<br>category: 'meeting_request' | Management channel |
| Manager - Doc Edits | GenericRequestModal | task_type: 'form-request'<br>category: 'manager_doc_edits' | Management channel |
| Manager - Code Requests | GenericRequestModal | task_type: 'form-request'<br>category: 'manager_code_requests' | Management/IT channel |
| Route Change Request | GenericRequestModal | task_type: 'form-request'<br>category: 'route_change_request' | Operations channel |
| Other Request | GenericRequestModal | task_type: 'form-request'<br>category: 'other_request' | General management |

---

### Reports Dropdown (8 Types)

| Report Type | Modal | Database Fields | Routing |
|------------|-------|-----------------|---------|
| WPI — Injured | IncidentModal | task_type: 'incident'<br>category: 'wpi_injured' | Safety channel + HR |
| WPI — Witness | IncidentModal | task_type: 'incident'<br>category: 'wpi_witness' | Safety channel + HR |
| Damage Report | IncidentModal | task_type: 'incident'<br>category: 'damage_report' | #damages-log |
| Car Accident | IncidentModal | task_type: 'incident'<br>category: 'car_accident' | Fleet + Safety + HR |
| Spill / Chemical Incident | IncidentModal | task_type: 'incident'<br>category: 'spill_chemical_incident' | Safety channel (urgent) |
| Customer Evidence | IncidentModal | task_type: 'incident'<br>category: 'customer_evidence' | Customer service |
| Vehicle Swap | IncidentModal | task_type: 'incident'<br>category: 'vehicle_swap' | Fleet management |
| Hours Correction Needed | HoursUpdateModal | task_type: 'hours-update'<br>category: 'Hours Update' | Payroll channel |

---

### Quick Buttons (3)

| Button | Modal | Database Fields | Routing |
|--------|-------|-----------------|---------|
| 😷 Call-Out | CallOutModal | task_type: 'call-out'<br>fields: reason, expected_return | Management + Operations |
| ⏱ Hours Update | HoursUpdateModal | task_type: 'hours-update'<br>fields: date, clock_in, clock_out | Payroll channel |
| 💰 Tech Collections | TechCollectionsModal | task_type: 'tech-collections'<br>fields: amount, payment_type, customer | Accounting channel |

---

## 🏢 Office Team Panel

**Command:** `@officepanel`
**Access:** Office staff, management
**Location:** Office team channel

### 5 Office Operations

| Operation | Modal | Database Fields | Routing |
|-----------|-------|-----------------|---------|
| ATS IT Issue | ATSITIssueModal | task_type: 'office-team'<br>category: 'ATS IT'<br>fields: issue_type, description, urgency | IT channel |
| Shift Cover | ShiftCoverModal | task_type: 'office-team'<br>category: 'Shift Cover'<br>fields: date, shift, reason | Operations channel |
| FR IT Issue | FRITIssueModal | task_type: 'office-team'<br>category: 'FR IT'<br>fields: module, error, impact | IT channel |
| Recruitment | RecruitmentModal | task_type: 'office-team'<br>category: 'Recruitment'<br>fields: position, urgency, requirements | HR channel |
| Pending Cancellation | PendingCancellationModal | task_type: 'office-team'<br>category: 'Cancellation'<br>fields: customer, reason, attempted_save | Customer service |

---

## 📋 Move-Up Panel

**Command:** `@moveuppanel`
**Access:** All employees, operations
**Location:** Operations channel

### 5 Job Prioritization Types

| Move-Up Type | Modal | Database Fields | Routing |
|--------------|-------|-----------------|---------|
| 🪲 Pest Job | PestMoveUpModal | task_type: 'move-up'<br>category: 'Pest'<br>fields: customer, phone, address, reason, priority | #move-up-log + Operations |
| 🐀 Rodent Job | RodentMoveUpModal | task_type: 'move-up'<br>category: 'Rodent'<br>fields: customer, phone, address, reason, priority | #move-up-log + Operations |
| 💩 Insulation Job | InsulationMoveUpModal | task_type: 'move-up'<br>category: 'Insulation'<br>fields: customer, phone, address, reason, priority | #move-up-log + Operations |
| 🤑 Sales Inspection | SalesMoveUpModal | task_type: 'move-up'<br>category: 'Sales'<br>fields: customer, phone, address, reason, priority | #move-up-log + Sales |
| 🐜 Termite Job | TermiteMoveUpModal | task_type: 'move-up'<br>category: 'Termite'<br>fields: customer, phone, address, reason, priority | #move-up-log + Operations |

---

## 📊 Management Panel

**Command:** `@managementpanel`
**Access:** Management only
**Location:** Management channel

### 5 Management Tools

| Tool | Modal | Database Fields | Routing | Privacy |
|------|-------|-----------------|---------|---------|
| 📊 Weekly Reservice | WeeklyReserviceModal | task_type: 'management'<br>category: 'Weekly Reserves'<br>fields: week_of, total, resolved, pending, notes | Management channel | Public |
| 🔐 Manager Password | ManagerPasswordModal | task_type: 'management'<br>category: 'Passwords'<br>fields: system, username, password, notes | Management channel | **Ephemeral** |
| 📝 Meeting Notes | MeetingNotesModal | task_type: 'management'<br>category: 'Meeting Notes'<br>fields: title, date, attendees, notes | Management channel | Public |
| 📄 Manager Document | ManagerDocModal | task_type: 'management'<br>category: 'Manager Docs'<br>fields: title, category, link, tags | Management channel | Public |
| 🎓 Manager Tutorial | ManagerTutorialModal | task_type: 'management'<br>category: 'Tutorials'<br>fields: title, software, steps, difficulty | Management channel | Public |

---

## 🚨 Alert System

**Command:** `/alert`
**Access:** All employees
**Location:** Any channel

### 4 Alert Types

| Alert Type | Modal | Database Fields | Routing |
|-----------|-------|-----------------|---------|
| ⏰ Time Update | TimeUpdateModal | Posted to channel<br>fields: update_type, details, estimated_time | #management-alerts |
| 📸 Customer Evidence | CustomerEvidenceModal | Posted to channel<br>fields: customer, evidence_type, description, link | #management-alerts |
| 📅 Pending Appointment | PendingAppointmentModal | Posted to channel<br>fields: customer, date, status, notes | #management-alerts |
| 📢 General Alert | GeneralEmployeeAlertModal | Posted to channel<br>fields: title, category, message, urgency | #management-alerts |

**Note:** Alerts don't save to database, they post directly to Discord channels as embeds.

---

## 💾 Database Structure

### Task Types

All requests/modals save to `tasks.db` with these task_types:

| task_type | Source | Count |
|-----------|--------|-------|
| `form-request` | Request Panel → Requests dropdown | 16 |
| `incident` | Request Panel → Reports dropdown | 8 |
| `call-out` | Request Panel → Call-Out button | 1 |
| `hours-update` | Request Panel → Hours Update button | 1 |
| `tech-collections` | Request Panel → Tech Collections button | 1 |
| `office-team` | Office Team Panel | 5 |
| `move-up` | Move-Up Panel | 5 |
| `management` | Management Panel | 5 |
| `calendar-event` | /calendar command | ∞ |
| `month-notes` | Calendar API | ∞ |

**Total Modal Types:** 42+

### Database Schema

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    created_by TEXT,
    created_by_id INTEGER,
    task_type TEXT,
    category TEXT,
    status TEXT DEFAULT 'open',
    assigned_to TEXT,
    assigned_to_id INTEGER,
    channel_id INTEGER,
    created_at TEXT,
    updated_at TEXT,
    completed_at TEXT,
    deleted_at TEXT
);
```

### Field Usage by Type

**form-request:**
- title: Request title
- description: Request details
- category: Specific request type (lowercased, underscored)

**incident:**
- title: Incident type
- description: Incident details
- category: Specific incident type (lowercased, underscored)

**office-team:**
- title: Operation title
- description: Operation details
- category: Operation type (e.g., "ATS IT", "Shift Cover")

**move-up:**
- title: "X Move-Up: Customer Name"
- description: Customer info + reason + priority
- category: Job type (Pest, Rodent, Insulation, Sales, Termite)

**management:**
- title: Tool-specific title
- description: Tool-specific data
- category: Tool type (Weekly Reserves, Passwords, Meeting Notes, etc.)

**calendar-event:**
- title: "📅 Event Title"
- description: "Date: YYYY-MM-DD\nType: type\nDescription"
- category: Event type

---

## 🎯 Channel Routing Matrix

### Recommended Channel Setup

| Channel Name | Receives | Purpose |
|-------------|----------|---------|
| #management-alerts | Alerts via `/alert` | Employee → Management communication |
| #office-alerts | Office Alerts web interface | Management → Team announcements |
| #calendar-events | Calendar events | Event announcements |
| #damages-log | Damage reports | Damage tracking |
| #fleet-reporting-log | Fleet reports, vehicle issues | Vehicle management |
| #training-log | Training submissions | Training tracking |
| #safety-log | Safety incidents, WPI reports | Safety compliance |
| #customer-feedback-log | Customer evidence | Customer service |
| #tech-reminders-log | Tech reminders | Technical followups |
| #inventory-log | Inventory requests, special orders | Inventory management |
| #move-up-log | All move-up submissions | Job prioritization |
| #office-operations-log | Office team operations | Office staff coordination |
| #employee-{name}-log | Individual employee submissions | Personal tracking |

### By Task Type

| Task Type | Primary Channel | Secondary Channel |
|-----------|----------------|-------------------|
| form-request | Employee log | Management |
| incident | Specific log channel | Safety/HR |
| call-out | Management-alerts | Operations |
| hours-update | Payroll channel | Employee log |
| tech-collections | Accounting | Employee log |
| office-team | Office-operations-log | IT/HR/Operations |
| move-up | Move-up-log | Operations |
| management | Management channel | - |
| calendar-event | Calendar-events | - |

---

## 🔀 Routing Flow Diagrams

### Request Panel Flow

```
User clicks Requests dropdown
    ↓
Selects request type
    ↓
Opens appropriate modal
    ↓
User fills out form
    ↓
Submits modal
    ↓
Saves to tasks.db with task_type='form-request'
    ↓
Posts to employee log channel
    ↓
Notifies management
```

### Alert System Flow

```
User runs /alert command
    ↓
Selects alert type
    ↓
Opens appropriate modal
    ↓
User fills out form
    ↓
Submits modal
    ↓
Creates embed (NOT saved to database)
    ↓
Posts to current channel
    ↓
Also posts to #management-alerts
```

### Move-Up Flow

```
User clicks Move-Up dropdown
    ↓
Selects job type
    ↓
Opens appropriate modal
    ↓
Enters customer info + priority
    ↓
Submits modal
    ↓
Saves to tasks.db with task_type='move-up'
    ↓
Posts to #move-up-log
    ↓
Posts to operations channel
    ↓
Operations team reviews and schedules
```

---

## 📊 Usage Statistics

Track these metrics for each routing destination:

**Per Channel:**
- Total submissions
- Submissions by type
- Average response time
- Completion rate

**Per Modal:**
- Usage frequency
- Completion rate (submitted vs abandoned)
- Average fill time
- Field validation errors

**Per User:**
- Requests submitted
- Alerts sent
- Move-ups created
- Response rate

**Query Example:**
```sql
-- Request breakdown by category
SELECT category, COUNT(*) as count
FROM tasks
WHERE task_type = 'form-request'
GROUP BY category
ORDER BY count DESC;

-- Move-ups by priority
SELECT category,
       SUM(CASE WHEN description LIKE '%High%' THEN 1 ELSE 0 END) as high,
       SUM(CASE WHEN description LIKE '%Medium%' THEN 1 ELSE 0 END) as medium,
       SUM(CASE WHEN description LIKE '%Low%' THEN 1 ELSE 0 END) as low
FROM tasks
WHERE task_type = 'move-up'
GROUP BY category;
```

---

## 🎯 Best Practices

### For Users

1. **Choose correct type** - Use the most specific request/alert type available
2. **Provide details** - Fill all fields thoroughly
3. **Check channel** - Verify your submission posted to the right place
4. **Follow up** - Monitor channel for responses

### For Admins

1. **Monitor channels** - Check routing destinations regularly
2. **Respond promptly** - Acknowledge submissions quickly
3. **Update status** - Mark tasks as complete when done
4. **Clean up** - Archive old channels periodically

### For Developers

1. **Consistent naming** - Use standardized task_type and category values
2. **Database queries** - Always filter by task_type AND category
3. **Channel IDs** - Store channel_id for audit trails
4. **Error handling** - Gracefully handle missing channels

---

## 🆘 Troubleshooting

**Submission not appearing in expected channel:**
- Check channel permissions
- Verify channel still exists
- Check bot role permissions
- Review channel_id in database

**Wrong modal opening:**
- Check custom_id values match
- Verify routing logic in callback
- Clear cache and restart bot

**Database not saving:**
- Check add_task() function
- Verify database connection
- Review error logs
- Check field requirements

---

**Last Updated:** December 2025
**Total Modals:** 42+
**Total Routes:** 50+
**Database:** tasks.db (SQLite)
