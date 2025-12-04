# Discord Channel Mapping for BottyOtty Bot

## Overview
This document explains where each Discord channel/thread is mapped in the bot's CONFIG and what functionality uses each channel.

---

## 📋 Table of Contents
1. [Special/Alert Channels](#specialalert-channels)
2. [Global Log Channels](#global-log-channels)
3. [Team Channels](#team-channels)
4. [Office to Tech Channels](#office-to-tech-channels)
5. [Office Team Channels](#office-team-channels)
6. [Office Management Channels](#office-management-channels)
7. [Management Team Channels](#management-team-channels)
8. [Employee Personal Channels](#employee-personal-channels)
9. [How to Access Channels in Bot Code](#how-to-access-channels-in-bot-code)

---

## Special/Alert Channels
**Location in CONFIG:** `CONFIG['special_channels']`

| Channel Name | Discord ID | CONFIG Key | Purpose |
|-------------|------------|------------|---------|
| #🚨alerts | 1445630201223450778 | `management_alerts` | Management alerts (employee alerts → managers) |
| #📅important-alerts | 1445619376832254054 | `office_alerts` | Office alerts web interface → Discord |
| #🛟resources🛟 | 1446269836404719737 | `kb_updates` | Knowledge base updates |
| #💥company-alerts💥 | 1445482076693332030 | `calendar_events` | Calendar announcements |
| 📒 Policy Updates (thread) | 1446270910125310092 | `policy_updates_thread` | Policy change announcements |
| #general-company-chat | 1445075784309145705 | `company_chat` | General company discussions |
| #watercooler | 1445482123778588733 | `watercooler` | Casual chat |
| #📸field-photos📸 | 1445482038390947982 | `field_photos` | Field work photos |
| #🎵music🎵 | 1445482157026840596 | `music` | Music sharing |

### Usage Example:
```python
# Send management alert
channel_id = CONFIG['special_channels']['management_alerts']
channel = bot.get_channel(channel_id)
await channel.send("🚨 Alert message here")

# Post to KB updates
kb_channel_id = CONFIG['special_channels']['kb_updates']
kb_channel = bot.get_channel(kb_channel_id)
await kb_channel.send("📚 New knowledge base article: ...")
```

---

## Global Log Channels
**Location in CONFIG:** `CONFIG['global_logs']`

These channels receive centralized logs from all employees for specific event types.

| Channel Name | Discord ID | CONFIG Key | What Gets Logged |
|-------------|------------|------------|------------------|
| #damages-log | 1446272676141334638 | `damages` | Damage reports |
| #fleet-log | 1446273032967426088 | `fleet` | Vehicle/fleet issues |
| #training-log | 1446273088655200416 | `training` | Training events |
| #safety-and-accident-log | 1446273177620578305 | `safety_and_accident` | Safety incidents, accidents |
| #customer-feedback-log | 1446273287293501561 | `customer_feedback` | Customer feedback/complaints |
| #tech-reminders-log | 1446273372001407148 | `tech_reminders` | Tech reminders |
| #inventory-log | 1446273416708751551 | `inventory` | Inventory updates |
| #office-operations-log | 1446273519901216889 | `office_operations` | Office operations |
| #🤖reports | 1446273562548899901 | `reports` | Automated reports |

### Usage Example:
```python
# Log a damage event
await log_event(
    bot=bot,
    employee_key="caleb_lee",
    event_type="Damage",
    title="Equipment Damage Report",
    fields={"Item": "Ladder", "Cost": "$150"},
    global_log_key="damages"  # Uses CONFIG['global_logs']['damages']
)
```

---

## Team Channels
**Location in CONFIG:** `CONFIG['team_channels']`

Team-wide channels for specific departments/functions.

| Channel Name | Discord ID | CONFIG Key | Team |
|-------------|------------|------------|------|
| #🪲pest-team | 1445612175161819277 | `pest_team` | Pest control team |
| #🪲pest-training | 1445613523047813211 | `pest_training` | Pest team training |
| #🪲weekly-inventory | 1445613211700301915 | `pest_inventory` | Pest inventory |
| #🪤rodent-team | 1445613873033121984 | `rodent_team` | Rodent control team |
| #🪤rodent-training | 1445613936945795112 | `rodent_training` | Rodent team training |
| #🪤rodent-inventory | 1445614073705271337 | `rodent_inventory` | Rodent inventory |
| #🏚️insulation-team | 1445612683813457992 | `insulation_team` | Insulation team |
| #🏚️insulation-photos | 1445615997754019970 | `insulation_photos` | Insulation work photos |
| #🧮sales-team | 1445615036822196287 | `sales_team` | Sales team |
| #🧮sales-training | 1445615276640047114 | `sales_training` | Sales training |
| #🧮sales-resources | 1445615319455498341 | `sales_resources` | Sales resources |
| #✌tech-to-inspect | 1445614391016816681 | `tech_to_inspect` | Tech → Inspector handoff |

### Usage Example:
```python
# Notify pest team
pest_channel_id = CONFIG['team_channels']['pest_team']
pest_channel = bot.get_channel(pest_channel_id)
await pest_channel.send("🪲 Team announcement: ...")
```

---

## Office to Tech Channels
**Location in CONFIG:** `CONFIG['office_to_tech']`

Channels for communication between office staff and technicians.

| Channel Name | Discord ID | CONFIG Key |
|-------------|------------|------------|
| #office-to-tech-chat | 1445482310941016124 | `chat` |
| #customer-feedback | 1445507404312740031 | `customer_feedback` |
| #availability-calendar | 1445505875979796542 | `availability_calendar` |
| #inspector-scheduling | 1445609902314750044 | `inspector_scheduling` |
| #🤔insulation-consult | 1445608742040240128 | `insulation_consult` |
| #🤔marketing-consult | 1445609185437028495 | `marketing_consult` |
| #🤔pest-consult | 1445609221730209947 | `pest_consult` |
| #🤔rodent-consult | 1445609271185379386 | `rodent_consult` |
| #🤔sales-consult | 1445609305960218634 | `sales_consult` |

---

## Office Team Channels
**Location in CONFIG:** `CONFIG['office_team']`

Channels used by office staff.

| Channel/Thread Name | Discord ID | CONFIG Key |
|--------------------|------------|------------|
| #cubicle-loves-bryan | 1445619027580944424 | `cubicle_chat` |
| #🍗chimkin | 1445624254837035038 | `chimkin` |
| #🚽afk | 1445624532948881530 | `afk` |
| #office-tools | 1445624845818662932 | `office_tools` |
| #support-and-resources | 1445619705883918409 | `support_resources` |
| #📅important-alerts | 1445619376832254054 | `important_alerts` |
| #scheduling | 1445619506847285268 | `scheduling` |
| 🧵 🫰 Billing | 1445651200983826493 | `billing_thread` |
| 🧵 🫗 Customer Care | 1445651337290322003 | `customer_care_thread` |
| 🧵 🧊 Cube Pool 🏊 | 1445651386023936071 | `cube_pool_thread` |
| 🧵 🎛️ Switchboard | 1445651576470372432 | `switchboard_thread` |
| 🧵 ☎️ Call Log | 1445651625233350747 | `call_log_thread` |

---

## Office Management Channels
**Location in CONFIG:** `CONFIG['office_management']`

Channels for office managers.

| Channel/Thread Name | Discord ID | CONFIG Key |
|--------------------|------------|------------|
| #office-manager-chat | 1445633249777946674 | `manager_chat` |
| 🧵 OM Pool 🏊‍♀️ | 1445633750430912553 | `om_pool_thread` |
| #smot | 1445633544948027402 | `smot` |
| #🌟think-tank🌟 | 1445633871176536217 | `think_tank` |
| #💸payroll-prep💸 | 1445635472369123328 | `payroll_prep` |
| #document-sharing | 1445634481053765652 | `document_sharing` |
| #account-logins🤫 | 1445635985034448906 | `account_logins` |

---

## Management Team Channels
**Location in CONFIG:** `CONFIG['management']`

Channels for company managers.

| Channel Name | Discord ID | CONFIG Key |
|-------------|------------|------------|
| #manager-chat | 1445511267166060616 | `manager_chat` |
| #manager-resources | 1445630429439852766 | `manager_resources` |
| #🚨alerts | 1445630201223450778 | `alerts` |
| #tuesday-meeting-notes | 1445629877297614978 | `tuesday_meeting_notes` |

---

## Employee Personal Channels
**Location in CONFIG:** `CONFIG['employees'][employee_key]`

Each employee has personal channels for direct communication with the bot and managers.

### Channel Types Per Employee:
- **rt_channel_id** - Round Table channel (main personal channel)
- **rt_thread_id** - 🤖Requests + Resources thread (bot interactions)
- **campfire_channel_id** - Campfire chat (1-on-1 with managers)
- **office_notes_thread** (office staff only) - Office notes thread
- **todo_thread_id** (managers only) - Manager to-do thread

### Technicians (23 total)

| Employee Key | RT Channel | RT Thread | Campfire |
|-------------|-----------|-----------|----------|
| `caleb_lee` | 1445468249318883471 | 1445471138338574628 | 1445477280112705617 |
| `charles_swanier` | 1445468304113139754 | 1445471186057302117 | 1445477492159938641 |
| `cole_heflin` | 1445468381976465571 | 1445475061073973429 | 1445477529543643330 |
| `dahyla_luna` | 1445468429787070647 | 1445475094276083712 | 1445477555972083762 |
| `devin_williams` | 1445468507713179851 | 1445475146797289565 | 1445477612402118806 |
| `dylan_weeks` | 1445468910353776650 | 1445475175410962432 | 1445477636020244680 |
| `edward_leija` | 1445468935527993555 | 1445475216665870346 | 1445477661861482526 |
| `fernando_chairez` | 1445468981371863194 | 1445475247452192992 | 1445477702827114660 |
| `hector_bermudez` | 1445469026389069926 | 1445475276409540691 | 1445477732153688245 |
| `isiac_ramirez` | 1445469063957450783 | 1445475303471321118 | 1445477769252180029 |
| `jose_flores` | 1445469181947547768 | 1445475390821896252 | 1445477875787628706 |
| `logan_bean` | 1445469216781373662 | 1445475414444212225 | 1445477946818170993 |
| `matt_kiger` | 1445469256161431663 | 1445475436531421349 | 1445477982750769232 |
| `nathaniel_de_leon` | 1445469288923271320 | 1445475465572651028 | 1445478014879272981 |
| `rafael_flores` | 1445469367948021830 | 1445475516428587109 | 1445478175185305814 |
| `raymond_flores` | 1445469419781357598 | 1445475546296357028 | 1445478212120481974 |
| `ric_brown` | 1445469464207294524 | 1445475577199853579 | 1445478254034161787 |
| `ryan_mcguire` | 1445469505881899092 | 1445475604945440799 | 1445478292961493142 |
| `ryan_poole` | 1445469540304683028 | 1445475625908306073 | 1445478329623908578 |
| `sam_hancock` | 1445469574672683251 | 1445475652169105619 | 1445478370459779092 |
| `tony_rodriguez` | 1445469608311259269 | 1445475674197459126 | 1445478571652026562 |
| `trevor_bell` | 1445469642905882736 | 1445475702336917576 | 1445478600324284416 |
| `tyler_brown` | 1445469676929945700 | 1445475736562569410 | 1445478632381218877 |

### Office Staff (6 total)

| Employee Key | RT Channel | RT Thread | Office Notes Thread | Campfire |
|-------------|-----------|-----------|-------------------|----------|
| `araceli_lee` | 1445469725709828278 | 1445473275365822496 | 1445473873008267404 | 1445477103666729112 |
| `amanda_stevenson` | 1445469774837715067 | 1445473374401855659 | 1445473948010807326 | 1445477158054138027 |
| `rachel_sweet` | 1445469889933479947 | 1445473519604596787 | 1445474268589850654 | 1445478136300179588 |
| `sean_richter` | 1445469919750918295 | 1445473549136433245 | 1445474401788362895 | 1445478399236768008 |
| `summer_geer` | 1445469946753581168 | 1445473579335680061 | 1445474502887735407 | 1445478435668496414 |
| `terry_sabin` | 1445469973039288342 | 1445473611833016350 | 1445474552636244131 | 1445478534200950865 |

### Managers (8 total)

| Employee Key | RT Channel | RT Thread | Office Notes | To-Do Thread | Campfire |
|-------------|-----------|-----------|--------------|--------------|----------|
| `adam_wilmes` | 1445468158189109279 | 1445470890811719811 | - | 1445629515656204318 | 1445477055633424415 |
| `dakota_colburn` | 1445468473286463609 | 1445475119224062114 | - | 1445629457976135744 | 1445477586716328028 |
| `jeff_kirkham` | 1445469096194998282 | 1445475333032771666 | - | 1445629333782925362 | 1445477805562400919 |
| `joey_heminger` | 1445469136246276097 | 1445475366788530389 | - | 1445629280267538552 | 1445477838344949883 |
| `preston_wagner` | 1445469323765223474 | 1445475490017181780 | - | 1445629238173765744 | 1445478097397874932 |
| `ash_streeter` | 1445469803551916083 | 1445473413861871688 | 1445474037965783110 | 1445629184096337981 | 1445477206930358442 |
| `lauren_ledyard` | 1445469830848184320 | 1445473438578774088 | 1445545433651744828 | 1445629050918928404 | 1445477908666908845 |
| `presley_mcentee` | 1445469860422357044 | 1445473486188449959 | 1445474204345438420 | 1445629114953367565 | 1445478048513134804 |

### Usage Examples:

```python
# Get employee's Round Table channel
emp_info = CONFIG['employees']['caleb_lee']
rt_channel_id = emp_info['rt_channel_id']
channel = bot.get_channel(rt_channel_id)
await channel.send("Message to Caleb's RT channel")

# Get employee's bot thread
rt_thread_id = emp_info['rt_thread_id']
thread = bot.get_channel(rt_thread_id)
await thread.send("🤖 Bot request response")

# Get employee's Campfire channel
campfire_id = emp_info['campfire_channel_id']
campfire = bot.get_channel(campfire_id)
await campfire.send("🔥 Manager message")

# Find employee by their RT channel
employee_key = get_employee_by_rt_channel(1445468249318883471)
# Returns: "caleb_lee"

# Find employee by Campfire channel
employee_key = get_employee_by_campfire(1445477280112705617)
# Returns: "caleb_lee"
```

---

## How to Access Channels in Bot Code

### 1. Special/Alert Channels
```python
# Access special channels
alerts_channel = bot.get_channel(CONFIG['special_channels']['management_alerts'])
kb_channel = bot.get_channel(CONFIG['special_channels']['kb_updates'])
calendar_channel = bot.get_channel(CONFIG['special_channels']['calendar_events'])

# Access policy updates thread
policy_thread = bot.get_channel(CONFIG['special_channels']['policy_updates_thread'])
```

### 2. Global Log Channels
```python
# Access log channels directly
damages_log = bot.get_channel(CONFIG['global_logs']['damages'])
fleet_log = bot.get_channel(CONFIG['global_logs']['fleet'])

# Or use the log_event helper function
await log_event(
    bot=bot,
    employee_key="caleb_lee",
    event_type="Fleet Issue",
    title="Vehicle Maintenance Required",
    fields={"Vehicle": "Truck #5", "Issue": "Oil change needed"},
    global_log_key="fleet"
)
```

### 3. Team Channels
```python
# Notify specific teams
pest_team = bot.get_channel(CONFIG['team_channels']['pest_team'])
await pest_team.send("🪲 Team update")

sales_team = bot.get_channel(CONFIG['team_channels']['sales_team'])
await sales_team.send("🧮 Sales target update")
```

### 4. Employee Channels
```python
# Access employee channels
emp = CONFIG['employees']['caleb_lee']

# Round Table channel (main)
rt_channel = bot.get_channel(emp['rt_channel_id'])

# Bot requests thread
bot_thread = bot.get_channel(emp['rt_thread_id'])

# Campfire (manager 1-on-1)
campfire = bot.get_channel(emp['campfire_channel_id'])

# Office notes (if employee has it)
if 'office_notes_thread' in emp:
    notes_thread = bot.get_channel(emp['office_notes_thread'])

# To-do thread (if manager)
if 'todo_thread_id' in emp:
    todo_thread = bot.get_channel(emp['todo_thread_id'])
```

### 5. Helper Functions
```python
# Find employee by channel/thread ID
employee = get_employee_by_rt_channel(1445468249318883471)  # "caleb_lee"
employee = get_employee_by_rt_thread(1445471138338574628)   # "caleb_lee"
employee = get_employee_by_campfire(1445477280112705617)    # "caleb_lee"
```

---

## Quick Reference: What Goes Where

| Event Type | Where It Goes | CONFIG Path |
|-----------|---------------|-------------|
| Management alert | #🚨alerts | `special_channels.management_alerts` |
| Office alert | #📅important-alerts | `special_channels.office_alerts` |
| KB update | #🛟resources🛟 | `special_channels.kb_updates` |
| Calendar event | #💥company-alerts💥 | `special_channels.calendar_events` |
| Policy update | 📒 Policy Updates thread | `special_channels.policy_updates_thread` |
| Damage report | #damages-log | `global_logs.damages` |
| Fleet issue | #fleet-log | `global_logs.fleet` |
| Training event | #training-log | `global_logs.training` |
| Safety incident | #safety-and-accident-log | `global_logs.safety_and_accident` |
| Customer feedback | #customer-feedback-log | `global_logs.customer_feedback` |
| Tech reminder | #tech-reminders-log | `global_logs.tech_reminders` |
| Inventory update | #inventory-log | `global_logs.inventory` |
| Office ops | #office-operations-log | `global_logs.office_operations` |
| Bot report | #🤖reports | `global_logs.reports` |
| Employee request | Employee's RT thread | `employees[key].rt_thread_id` |
| Manager 1-on-1 | Employee's Campfire | `employees[key].campfire_channel_id` |

---

## Notes

- **User IDs**: Employee Discord user IDs are NOT yet populated in CONFIG. You'll need to add `discord_user_id` to each employee entry.
- **Backward Compatibility**: The old `log_channel_id` field no longer exists. Individual employee log channels have been replaced with global log channels.
- **Helper Functions**: Use `get_employee_by_rt_channel()`, `get_employee_by_rt_thread()`, or `get_employee_by_campfire()` to look up employees.

---

*Last updated: December 2025*
*Related files: `main.py` (lines 32-336)*
