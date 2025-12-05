# 🤖 Bot Integration Plan - Complete Analysis

## 📊 **What You Already Have (AMAZING!)**

### **Database: SQLite** ✅
- **File:** `tasks.db`
- **Type:** SQLite3 (perfect for your needs)
- **Location:** Same directory as main.py

### **Flask API Server** ✅
- **Port:** 8080 (Railway deploys automatically)
- **CORS Enabled:** All routes accessible from web pages
- **Base URL:** `https://bottyotty-production.up.railway.app`

### **Existing API Endpoints** ✅
Your bot ALREADY has these working endpoints:

#### Task Management:
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<id>/update` - Update task
- `DELETE /api/tasks/<id>` - Delete task
- `POST /api/tasks/<id>/assign` - Assign task
- `POST /api/tasks/<id>/complete` - Complete task
- `POST /api/tasks/<id>/release-to-pool` - Release to pool
- `GET /api/tasks/<id>/updates` - Get task updates
- `POST /api/tasks/<id>/updates` - Add task update

#### User Management:
- `GET /api/assignees` - Get all assignees
- `GET /api/permissions` - Get user permissions
- `POST /api/permissions` - Save permissions
- `GET /api/mentions/<user_id>` - Get user mentions
- `POST /api/mentions/<id>/read` - Mark mention as read

#### Training System:
- `GET /api/trainings` - Get trainings
- `POST /api/trainings` - Create training
- `POST /api/trainings/<id>/signin` - Sign in to training

#### Important Messages:
- `GET /api/important-messages` - Get messages
- `POST /api/important-messages/<id>/react` - React to message

#### Utilities:
- `GET /api/categories` - Get task categories
- `GET /api/trash` - Get deleted tasks
- `POST /api/trash/<id>/restore` - Restore from trash
- `GET /api/health` - Health check

### **Discord Bot Commands & Modals** ✅
You have TONS of Discord modals already set up:

#### Request Forms:
- **Uniform Request Modal** - Request uniforms
- **Vehicle Issue Modal** - Report vehicle problems
- **Print Materials Modal** - Request printing
- **ID Card Modal** - Request ID cards
- **Reimbursement Modal** - Submit reimbursements
- **Meeting Modal** - Schedule meetings
- **Safety Gear Modal** - Request PPE
- **Other Request Modal** - General requests

#### Logging Modals:
- **Call-Out Modal** - Report absences
- **Hours Update Modal** - Update work hours
- **Tech Collections Modal** - Log collections
- **Incident Modal** - Report incidents
- **Campfire Escalation Modal** - Escalate issues

#### Panel Modals (Admin):
- Panel Reimbursement
- Panel Uniform Request
- Panel ID Card
- Panel Company Card
- Generic Request Modal

### **Team Structure** ✅
You have **30+ employees** configured:

**Management/Office:**
- Ash, Preston, Presley, Joey, Jeff, Dakota, Adam

**Field Technicians:**
- Dahlya, Araceli, Terry, Cole, Devin, Amanda, Caleb, Charles, Dylan, Edward, Fernando, Hector, Isiac, Jose, Matt Kiger, Logan, Nathaniel, Rachel, Rafael, Raymond, Ric, Ryan M, Ryan P, Sam, Sean, Summer, Tony, Trevor, Tyler, Chase, Lauren

### **Channel Organization** ✅

#### Pool Channels (Shared task queues):
- SMOT Pool
- OM Pool
- Cube Pool

#### Personal Channels (Each employee has):
- **To-Do Channel:** Personal task list
- **RoundTable Channel:** Individual workspace
- **Log Channel:** Activity logging
- **Campfire Channel:** Team discussions

#### Global Log Channels:
- Call-outs log
- Requests log
- Hours updates log
- Pending appointments log
- Tech collections log
- Vehicle issues log
- WPI reports log

---

## 🎯 **What We Need to Add**

I'll create **NEW database tables** and **API endpoints** for your 9 new tools:

### **New Database Tables Needed:**

```sql
-- 1. Calendar Events
CREATE TABLE calendar_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    type TEXT NOT NULL,  -- birthday, payday, supplyday, etc.
    mode TEXT NOT NULL,  -- virtual, inperson, general
    date TEXT NOT NULL,  -- YYYY-MM-DD format
    created_at TEXT NOT NULL
);

-- 2. Calendar Notes (month-specific notes)
CREATE TABLE calendar_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month_key TEXT NOT NULL UNIQUE,  -- YYYY-MM format
    notes TEXT
);

-- 3. Lead Sites
CREATE TABLE lead_sites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT,
    status TEXT NOT NULL,  -- active, paused, inactive
    channel_id TEXT,
    webhook_url TEXT,
    api_key TEXT,
    notes TEXT,
    created_at TEXT NOT NULL
);

-- 4. Vehicles
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    plate TEXT NOT NULL,
    vin TEXT,
    year TEXT,
    make TEXT,
    model TEXT,
    mileage TEXT,
    last_service TEXT,
    next_service TEXT,
    assigned_to TEXT,
    status TEXT NOT NULL,  -- active, maintenance, inactive
    notes TEXT
);

-- 5. Safety Incidents
CREATE TABLE safety_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,  -- injury, near-miss, property-damage, chemical-spill, other
    severity TEXT NOT NULL,  -- low, medium, high
    description TEXT NOT NULL,
    location TEXT,
    reported_by TEXT,
    date TEXT NOT NULL
);

-- 6. Safety Inspections
CREATE TABLE safety_inspections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area TEXT NOT NULL,
    inspector TEXT,
    passed INTEGER NOT NULL,  -- 0 or 1 (boolean)
    notes TEXT,
    date TEXT NOT NULL
);

-- 7. Customer Feedback
CREATE TABLE customer_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer TEXT NOT NULL,
    rating INTEGER NOT NULL,  -- 1-5
    category TEXT NOT NULL,  -- service, communication, timeliness, etc.
    comment TEXT,
    technician TEXT,
    date TEXT NOT NULL,
    follow_up_needed INTEGER NOT NULL  -- 0 or 1
);

-- 8. Tech Reminders
CREATE TABLE tech_reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    tech TEXT NOT NULL,
    due_date TEXT,
    priority TEXT NOT NULL,  -- low, medium, high
    category TEXT NOT NULL,  -- general, maintenance, training, etc.
    completed INTEGER NOT NULL,  -- 0 or 1
    created_at TEXT NOT NULL
);

-- 9. Inventory
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    min_quantity INTEGER NOT NULL,
    category TEXT NOT NULL,  -- chemicals, equipment, supplies, tools, ppe
    location TEXT,
    notes TEXT
);

-- 10. Pest Move-Up List
CREATE TABLE pest_moveup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT,
    reason TEXT NOT NULL,  -- cancellation, reschedule, urgent, callback
    priority TEXT NOT NULL,  -- low, medium, high
    notes TEXT,
    date_added TEXT NOT NULL,
    contacted INTEGER NOT NULL,  -- 0 or 1
    position INTEGER  -- For ordering
);

-- 11. Office Alerts
CREATE TABLE office_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    recipients TEXT NOT NULL,  -- JSON array of recipient IDs
    priority TEXT NOT NULL,  -- low, medium, high
    channel_id TEXT,
    timestamp TEXT NOT NULL,
    sent INTEGER NOT NULL  -- 0 or 1
);

-- 12. Alert People (recipients list)
CREATE TABLE alert_people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    discord_id TEXT,
    role TEXT
);
```

### **New API Endpoints Needed:**

I'll create Flask routes for each tool:

#### Calendar API:
- `GET /api/calendar/events` - Get all events
- `POST /api/calendar/events` - Add event
- `DELETE /api/calendar/events/<id>` - Delete event
- `GET /api/calendar/notes/<month>` - Get month notes
- `PUT /api/calendar/notes/<month>` - Update month notes

#### Lead Sites API:
- `GET /api/lead-sites` - Get all sites
- `POST /api/lead-sites` - Add site
- `PUT /api/lead-sites/<id>` - Update site
- `DELETE /api/lead-sites/<id>` - Delete site
- `POST /api/lead-sites/<id>/test` - Test connection

#### Vehicles API:
- `GET /api/vehicles` - Get all vehicles
- `POST /api/vehicles` - Add vehicle
- `PUT /api/vehicles/<id>` - Update vehicle
- `DELETE /api/vehicles/<id>` - Delete vehicle

#### Safety API:
- `GET /api/safety/incidents` - Get incidents
- `POST /api/safety/incidents` - Report incident
- `GET /api/safety/inspections` - Get inspections
- `POST /api/safety/inspections` - Log inspection

#### Feedback API:
- `GET /api/feedback` - Get all feedback
- `POST /api/feedback` - Add feedback

#### Tech Reminders API:
- `GET /api/tech-reminders` - Get all reminders
- `POST /api/tech-reminders` - Add reminder
- `PUT /api/tech-reminders/<id>` - Update reminder
- `DELETE /api/tech-reminders/<id>` - Delete reminder

#### Inventory API:
- `GET /api/inventory` - Get all items
- `POST /api/inventory` - Add item
- `PUT /api/inventory/<id>` - Update item (quantity, etc.)
- `DELETE /api/inventory/<id>` - Delete item

#### Pest Move-Up API:
- `GET /api/pest-moveup` - Get queue
- `POST /api/pest-moveup` - Add customer
- `PUT /api/pest-moveup/<id>` - Update customer
- `DELETE /api/pest-moveup/<id>` - Remove customer
- `PUT /api/pest-moveup/<id>/reorder` - Change position

#### Office Alerts API:
- `GET /api/office-alerts` - Get alerts
- `POST /api/office-alerts` - Send alert
- `GET /api/alert-people` - Get people list
- `POST /api/alert-people` - Add person
- `DELETE /api/alert-people/<id>` - Remove person

---

## 🚀 **Implementation Strategy**

### **Phase 1: Database Setup** (I'll provide SQL)
1. Create all new tables
2. Add indexes for performance
3. Test with sample data

### **Phase 2: API Endpoints** (I'll write Python code)
1. Create helper functions for database operations
2. Write Flask routes for each tool
3. Add error handling
4. Test endpoints

### **Phase 3: Update HTML Pages** (I'll modify existing files)
1. Replace localStorage calls with API calls
2. Add loading states
3. Add error handling
4. Test data flow

### **Phase 4: Discord Integration** (Optional but cool!)
1. Post calendar events to Discord
2. Alert when inventory is low
3. Notify on safety incidents
4. Send customer feedback summaries
5. Post vehicle maintenance reminders

---

## 💡 **Key Design Decisions**

### **Why SQLite is PERFECT for you:**
✅ **Simple:** No separate database server needed
✅ **Fast:** Great for your team size
✅ **Reliable:** Battle-tested, used by millions
✅ **Portable:** Single file, easy backups
✅ **Free:** No database hosting costs

### **Data Persistence Strategy:**
1. **HTML pages** → Send data to Flask API
2. **Flask API** → Save to SQLite database
3. **Database** → Shared across all users
4. **Optional:** Sync to Discord for announcements

### **Backward Compatibility:**
- All existing bot features stay 100% intact
- New tools are completely separate
- No risk of breaking current functionality

---

## 📋 **Next Steps**

Ready to implement? I can:

1. ✍️ **Write the database initialization code** (SQL)
2. ✍️ **Write all Flask API endpoints** (Python)
3. ✍️ **Update all 9 HTML pages** to use your API
4. ✍️ **Add Discord notifications** (optional)
5. ✍️ **Create backup/restore system** (bonus!)

Just say "GO" and I'll start building! 🚀

---

## 🎯 **What You'll Get**

After integration, your system will:
- ✅ **Share data** across all users
- ✅ **Persist forever** in database
- ✅ **Work offline** (with sync button)
- ✅ **Post to Discord** (optional)
- ✅ **Keep all existing features** intact
- ✅ **Be production ready** for Netlify

Sound good? Let's do this! 💪
