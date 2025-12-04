import discord
from discord.ext import commands, tasks
from discord import app_commands, ui
import sqlite3
import json
from datetime import datetime, timedelta
import re
import asyncio
from typing import Optional, Dict, List, Any
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from threading import Thread
import os

DATE_FORMAT = "%Y-%m-%d"


def parse_date_str(date_str: str) -> Optional[datetime]:
    """Parse YYYY-MM-DD into a datetime (UTC-naive)."""
    try:
        return datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        return None

# Flask app for API
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get port from environment variable (Railway sets this automatically)
PORT = int(os.environ.get('PORT', 8080))

# Centralized configuration for employees and logging channels
CONFIG: Dict[str, Any] = {
    # Special/Alert Channels
    "special_channels": {
        "management_alerts": 1445630201223450778,  # #🚨alerts
        "office_alerts": 1445619376832254054,  # #📅important-alerts
        "kb_updates": 1446269836404719737,  # #🛟resources🛟
        "calendar_events": 1445482076693332030,  # #💥company-alerts💥
        "policy_updates_thread": 1446270910125310092,  # 📒 Policy Updates thread
        "company_chat": 1445075784309145705,  # #general-company-chat
        "watercooler": 1445482123778588733,  # #watercooler
        "field_photos": 1445482038390947982,  # #📸field-photos📸
        "music": 1445482157026840596,  # #🎵music🎵
        "resources": 1446269836404719737,  # #🛟resources🛟
    },

    # Global Log Channels
    "global_logs": {
        "damages": 1446272676141334638,  # #damages-log
        "fleet": 1446273032967426088,  # #fleet-log
        "training": 1446273088655200416,  # #training-log
        "safety_and_accident": 1446273177620578305,  # #safety-and-accident-log
        "customer_feedback": 1446273287293501561,  # #customer-feedback-log
        "tech_reminders": 1446273372001407148,  # #tech-reminders-log
        "inventory": 1446273416708751551,  # #inventory-log
        "office_operations": 1446273519901216889,  # #office-operations-log
        "reports": 1446273562548899901,  # #🤖reports
    },

    # Team Channels (non-personal)
    "team_channels": {
        "pest_team": 1445612175161819277,
        "pest_training": 1445613523047813211,
        "pest_inventory": 1445613211700301915,
        "rodent_team": 1445613873033121984,
        "rodent_training": 1445613936945795112,
        "rodent_inventory": 1445614073705271337,
        "insulation_team": 1445612683813457992,
        "insulation_photos": 1445615997754019970,
        "sales_team": 1445615036822196287,
        "sales_training": 1445615276640047114,
        "sales_resources": 1445615319455498341,
        "tech_to_inspect": 1445614391016816681,
    },

    # Office to Tech Channels
    "office_to_tech": {
        "chat": 1445482310941016124,
        "customer_feedback": 1445507404312740031,
        "availability_calendar": 1445505875979796542,
        "inspector_scheduling": 1445609902314750044,
        "insulation_consult": 1445608742040240128,
        "marketing_consult": 1445609185437028495,
        "pest_consult": 1445609221730209947,
        "rodent_consult": 1445609271185379386,
        "sales_consult": 1445609305960218634,
    },

    # Office Team Channels
    "office_team": {
        "cubicle_chat": 1445619027580944424,  # #cubicle-loves-bryan
        "chimkin": 1445624254837035038,
        "afk": 1445624532948881530,
        "office_tools": 1445624845818662932,
        "support_resources": 1445619705883918409,
        "important_alerts": 1445619376832254054,
        "scheduling": 1445619506847285268,
        # Office tools threads
        "billing_thread": 1445651200983826493,
        "customer_care_thread": 1445651337290322003,
        "cube_pool_thread": 1445651386023936071,
        "switchboard_thread": 1445651576470372432,
        "call_log_thread": 1445651625233350747,
    },

    # Office Management Channels
    "office_management": {
        "manager_chat": 1445633249777946674,
        "om_pool_thread": 1445633750430912553,
        "smot": 1445633544948027402,
        "think_tank": 1445633871176536217,
        "payroll_prep": 1445635472369123328,
        "document_sharing": 1445634481053765652,
        "account_logins": 1445635985034448906,
    },

    # Management Team Channels
    "management": {
        "manager_chat": 1445511267166060616,
        "manager_resources": 1445630429439852766,
        "alerts": 1445630201223450778,
        "tuesday_meeting_notes": 1445629877297614978,
    },

    # Employee Personal Channels (Round Table channels + Campfire)
    "employees": {
        # Technicians
        "caleb_lee": {
            "rt_channel_id": 1445468249318883471,
            "rt_thread_id": 1445471138338574628,
            "campfire_channel_id": 1445477280112705617,
        },
        "charles_swanier": {
            "rt_channel_id": 1445468304113139754,
            "rt_thread_id": 1445471186057302117,
            "campfire_channel_id": 1445477492159938641,
        },
        "cole_heflin": {
            "rt_channel_id": 1445468381976465571,
            "rt_thread_id": 1445475061073973429,
            "campfire_channel_id": 1445477529543643330,
        },
        "dahyla_luna": {
            "rt_channel_id": 1445468429787070647,
            "rt_thread_id": 1445475094276083712,
            "campfire_channel_id": 1445477555972083762,
        },
        "devin_williams": {
            "rt_channel_id": 1445468507713179851,
            "rt_thread_id": 1445475146797289565,
            "campfire_channel_id": 1445477612402118806,
        },
        "dylan_weeks": {
            "rt_channel_id": 1445468910353776650,
            "rt_thread_id": 1445475175410962432,
            "campfire_channel_id": 1445477636020244680,
        },
        "edward_leija": {
            "rt_channel_id": 1445468935527993555,
            "rt_thread_id": 1445475216665870346,
            "campfire_channel_id": 1445477661861482526,
        },
        "fernando_chairez": {
            "rt_channel_id": 1445468981371863194,
            "rt_thread_id": 1445475247452192992,
            "campfire_channel_id": 1445477702827114660,
        },
        "hector_bermudez": {
            "rt_channel_id": 1445469026389069926,
            "rt_thread_id": 1445475276409540691,
            "campfire_channel_id": 1445477732153688245,
        },
        "isiac_ramirez": {
            "rt_channel_id": 1445469063957450783,
            "rt_thread_id": 1445475303471321118,
            "campfire_channel_id": 1445477769252180029,
        },
        "jose_flores": {
            "rt_channel_id": 1445469181947547768,
            "rt_thread_id": 1445475390821896252,
            "campfire_channel_id": 1445477875787628706,
        },
        "logan_bean": {
            "rt_channel_id": 1445469216781373662,
            "rt_thread_id": 1445475414444212225,
            "campfire_channel_id": 1445477946818170993,
        },
        "matt_kiger": {
            "rt_channel_id": 1445469256161431663,
            "rt_thread_id": 1445475436531421349,
            "campfire_channel_id": 1445477982750769232,
        },
        "nathaniel_de_leon": {
            "rt_channel_id": 1445469288923271320,
            "rt_thread_id": 1445475465572651028,
            "campfire_channel_id": 1445478014879272981,
        },
        "rafael_flores": {
            "rt_channel_id": 1445469367948021830,
            "rt_thread_id": 1445475516428587109,
            "campfire_channel_id": 1445478175185305814,
        },
        "raymond_flores": {
            "rt_channel_id": 1445469419781357598,
            "rt_thread_id": 1445475546296357028,
            "campfire_channel_id": 1445478212120481974,
        },
        "ric_brown": {
            "rt_channel_id": 1445469464207294524,
            "rt_thread_id": 1445475577199853579,
            "campfire_channel_id": 1445478254034161787,
        },
        "ryan_mcguire": {
            "rt_channel_id": 1445469505881899092,
            "rt_thread_id": 1445475604945440799,
            "campfire_channel_id": 1445478292961493142,
        },
        "ryan_poole": {
            "rt_channel_id": 1445469540304683028,
            "rt_thread_id": 1445475625908306073,
            "campfire_channel_id": 1445478329623908578,
        },
        "sam_hancock": {
            "rt_channel_id": 1445469574672683251,
            "rt_thread_id": 1445475652169105619,
            "campfire_channel_id": 1445478370459779092,
        },
        "tony_rodriguez": {
            "rt_channel_id": 1445469608311259269,
            "rt_thread_id": 1445475674197459126,
            "campfire_channel_id": 1445478571652026562,
        },
        "trevor_bell": {
            "rt_channel_id": 1445469642905882736,
            "rt_thread_id": 1445475702336917576,
            "campfire_channel_id": 1445478600324284416,
        },
        "tyler_brown": {
            "rt_channel_id": 1445469676929945700,
            "rt_thread_id": 1445475736562569410,
            "campfire_channel_id": 1445478632381218877,
        },

        # Office Staff
        "araceli_lee": {
            "rt_channel_id": 1445469725709828278,
            "rt_thread_id": 1445473275365822496,
            "office_notes_thread": 1445473873008267404,
            "campfire_channel_id": 1445477103666729112,
        },
        "amanda_stevenson": {
            "rt_channel_id": 1445469774837715067,
            "rt_thread_id": 1445473374401855659,
            "office_notes_thread": 1445473948010807326,
            "campfire_channel_id": 1445477158054138027,
        },
        "rachel_sweet": {
            "rt_channel_id": 1445469889933479947,
            "rt_thread_id": 1445473519604596787,
            "office_notes_thread": 1445474268589850654,
            "campfire_channel_id": 1445478136300179588,
        },
        "sean_richter": {
            "rt_channel_id": 1445469919750918295,
            "rt_thread_id": 1445473549136433245,
            "office_notes_thread": 1445474401788362895,
            "campfire_channel_id": 1445478399236768008,
        },
        "summer_geer": {
            "rt_channel_id": 1445469946753581168,
            "rt_thread_id": 1445473579335680061,
            "office_notes_thread": 1445474502887735407,
            "campfire_channel_id": 1445478435668496414,
        },
        "terry_sabin": {
            "rt_channel_id": 1445469973039288342,
            "rt_thread_id": 1445473611833016350,
            "office_notes_thread": 1445474552636244131,
            "campfire_channel_id": 1445478534200950865,
        },

        # Managers
        "adam_wilmes": {
            "rt_channel_id": 1445468158189109279,
            "rt_thread_id": 1445470890811719811,
            "todo_thread_id": 1445629515656204318,
            "campfire_channel_id": 1445477055633424415,
        },
        "dakota_colburn": {
            "rt_channel_id": 1445468473286463609,
            "rt_thread_id": 1445475119224062114,
            "todo_thread_id": 1445629457976135744,
            "campfire_channel_id": 1445477586716328028,
        },
        "jeff_kirkham": {
            "rt_channel_id": 1445469096194998282,
            "rt_thread_id": 1445475333032771666,
            "todo_thread_id": 1445629333782925362,
            "campfire_channel_id": 1445477805562400919,
        },
        "joey_heminger": {
            "rt_channel_id": 1445469136246276097,
            "rt_thread_id": 1445475366788530389,
            "todo_thread_id": 1445629280267538552,
            "campfire_channel_id": 1445477838344949883,
        },
        "preston_wagner": {
            "rt_channel_id": 1445469323765223474,
            "rt_thread_id": 1445475490017181780,
            "todo_thread_id": 1445629238173765744,
            "campfire_channel_id": 1445478097397874932,
        },
        "ash_streeter": {
            "rt_channel_id": 1445469803551916083,
            "rt_thread_id": 1445473413861871688,
            "office_notes_thread": 1445474037965783110,
            "todo_thread_id": 1445629184096337981,
            "campfire_channel_id": 1445477206930358442,
        },
        "lauren_ledyard": {
            "rt_channel_id": 1445469830848184320,
            "rt_thread_id": 1445473438578774088,
            "office_notes_thread": 1445545433651744828,
            "todo_thread_id": 1445629050918928404,
            "campfire_channel_id": 1445477908666908845,
        },
        "presley_mcentee": {
            "rt_channel_id": 1445469860422357044,
            "rt_thread_id": 1445473486188449959,
            "office_notes_thread": 1445474204345438420,
            "todo_thread_id": 1445629114953367565,
            "campfire_channel_id": 1445478048513134804,
        },
    },
}


def get_employee_by_rt_channel(channel_id: int) -> Optional[str]:
    """Get employee key by their Round Table channel ID"""
    for key, data in CONFIG.get("employees", {}).items():
        if data.get("rt_channel_id") == channel_id:
            return key
    return None


def get_employee_by_rt_thread(thread_id: int) -> Optional[str]:
    """Get employee key by their Round Table thread ID"""
    for key, data in CONFIG.get("employees", {}).items():
        if data.get("rt_thread_id") == thread_id:
            return key
    return None


def get_employee_by_campfire(channel_id: int) -> Optional[str]:
    """Get employee key by their Campfire channel ID"""
    for key, data in CONFIG.get("employees", {}).items():
        if data.get("campfire_channel_id") == channel_id:
            return key
    return None


def get_employee_by_user_id(user_id: int) -> Optional[str]:
    """Get employee key by their Discord user ID (requires discord_user_id in CONFIG)"""
    for key, data in CONFIG.get("employees", {}).items():
        if data.get("discord_user_id") == user_id:
            return key
    return None


async def log_event(
    bot: commands.Bot,
    employee_key: str,
    event_type: str,
    title: str,
    fields: Dict[str, str],
    global_log_key: str,
):
    """Send a structured embed to the global log channel and optionally to employee's RT channel."""

    employee_info = CONFIG.get("employees", {}).get(employee_key)
    if not employee_info:
        return

    global_channel_id = CONFIG.get("global_logs", {}).get(global_log_key)
    rt_channel_id = employee_info.get("rt_channel_id")
    user_id = employee_info.get("discord_user_id")

    employee_mention = f"<@{user_id}>" if user_id else employee_key.replace("_", " ").title()
    rt_channel_ref = f"<#{rt_channel_id}>" if rt_channel_id else "Round Table"

    # Global embed
    if global_channel_id:
        channel = bot.get_channel(int(global_channel_id))
        if channel:
            embed = discord.Embed(title=title, color=discord.Color.blue())
            embed.add_field(name="Employee", value=employee_mention, inline=True)
            embed.add_field(name="Type", value=event_type, inline=True)
            embed.add_field(name="Employee Channel", value=rt_channel_ref, inline=True)
            for field_name, value in fields.items():
                embed.add_field(name=field_name, value=value or "N/A", inline=False)
            embed.add_field(name="Status", value="Pending", inline=True)
            embed.timestamp = discord.utils.utcnow()
            await channel.send(embed=embed)

    # Optional: Send marker to employee's Round Table channel
    if rt_channel_id:
        marker_channel = bot.get_channel(int(rt_channel_id))
        if marker_channel:
            marker_parts = [f"📌 {title}"]
            detail_parts = [f"{k}: {v}" for k, v in fields.items() if v]
            if detail_parts:
                marker_parts.append(" — ".join(detail_parts))
            marker_parts.append("Status: Pending")
            await marker_channel.send(" | ".join(marker_parts))


def detect_hey_event(content: str) -> Optional[str]:
    lowered = content.lower()
    if any(keyword in lowered for keyword in ["sick", "ill", "fever", "can't come", "call out", "calling out"]):
        return "call_out"
    if any(keyword in lowered for keyword in ["vehicle", "unsafe", "flat tire", "engine", "brake", "car accident"]):
        return "vehicle_issue"
    return None

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks for HTML sync"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        # Include all tasks except deleted ones (deleted tasks have their own endpoint)
        c.execute("SELECT * FROM tasks WHERE status != 'deleted' ORDER BY created_at DESC")
        columns = [description[0] for description in c.description]
        rows = c.fetchall()
        conn.close()

        tasks = []
        for row in rows:
            task_dict = dict(zip(columns, row))
            # Convert to HTML-compatible format
            html_task = {
                'id': task_dict['task_number'],
                'name': task_dict['title'],
                'assignee': task_dict.get('assigned_to') or task_dict.get('created_by', 'Unassigned'),
                'link': task_dict.get('reference_message_link'),
                'category': task_dict.get('category', 'General'),
                'priority': task_dict.get('priority', 'medium'),
                'startDate': None,
                'endDate': task_dict.get('due_date'),
                'notes': task_dict.get('description'),
                'status': 'completed' if task_dict['status'] == 'completed' else 'active',
                'starred': False,
                'isIncoming': task_dict['task_type'] == 'request',  # @hey commands
                'isAssignedOut': task_dict['task_type'] == 'assigned',
                'assignedTo': task_dict.get('assigned_to'),
                'isTeamRequest': task_dict['task_type'] == 'pool' or task_dict['task_type'] == 'form-request',  # Pool tasks + Form submissions
                'isCampfire': task_dict['task_type'] == 'campfire' or task_dict.get('is_campfire', 0) == 1,
                'isRecurring': False,
                'createdAt': task_dict.get('created_at'),
                'discordTaskNumber': task_dict['task_number'],
                'claimedBy': task_dict.get('claimed_by'),
                'claimedById': task_dict.get('claimed_by_id'),
                'completedBy': task_dict.get('completed_by')
            }
            tasks.append(html_task)

        return jsonify(tasks)
    except Exception as e:
        print(f"ERROR in /api/tasks: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/trash', methods=['GET'])
def get_trash():
    """Get all deleted tasks"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE status = 'deleted' ORDER BY completed_at DESC")
        columns = [description[0] for description in c.description]
        rows = c.fetchall()
        conn.close()

        trash = []
        for row in rows:
            task_dict = dict(zip(columns, row))
            trash_task = {
                'id': task_dict['task_number'],
                'name': task_dict['title'],
                'assignee': task_dict.get('assigned_to') or task_dict.get('created_by', 'Unassigned'),
                'link': task_dict.get('reference_message_link'),
                'category': task_dict.get('category', 'General'),
                'priority': task_dict.get('priority', 'medium'),
                'endDate': task_dict.get('due_date'),
                'notes': task_dict.get('description'),
                'trashedAt': task_dict.get('completed_at'),  # Reuse completed_at for deleted timestamp
                'isIncoming': task_dict['task_type'] == 'request',
                'isAssignedOut': task_dict['task_type'] == 'assigned',
                'isTeamRequest': task_dict['task_type'] == 'pool',
                'isCampfire': task_dict.get('is_campfire', 0) == 1,
                'discordTaskNumber': task_dict['task_number']
            }
            trash.append(trash_task)

        return jsonify(trash)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Move task to trash (soft delete)"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''UPDATE tasks
                     SET status = 'deleted', completed_at = CURRENT_TIMESTAMP
                     WHERE task_number = ?''',
                  (task_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Task {task_id} moved to trash'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trash/<int:task_id>/restore', methods=['POST'])
def restore_task(task_id):
    """Restore task from trash"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''UPDATE tasks
                     SET status = 'pending', completed_at = NULL
                     WHERE task_number = ? AND status = 'deleted' ''',
                  (task_id,))
        rows_affected = c.rowcount
        conn.commit()
        conn.close()

        if rows_affected > 0:
            return jsonify({'success': True, 'message': f'Task {task_id} restored'})
        else:
            return jsonify({'error': 'Task not found in trash'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_number>/assign', methods=['POST'])
def assign_task(task_number):
    """Assign task to someone and notify in Discord"""
    try:
        data = request.json
        assigned_to = data.get('assignedTo')
        assigned_to_id = data.get('assignedToId')
        assignee_channel_id = data.get('assigneeChannelId')

        if not assigned_to or not assigned_to_id:
            return jsonify({'error': 'assignedTo and assignedToId are required'}), 400

        # If no channel ID provided, try to get from PERSONAL_CHANNELS
        if not assignee_channel_id:
            assignee_channel_id = PERSONAL_CHANNELS.get(assigned_to)

        # Update task in database
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''UPDATE tasks
                     SET assigned_to = ?, assigned_to_id = ?, task_type = 'assigned'
                     WHERE task_number = ?''',
                  (assigned_to, int(assigned_to_id), task_number))
        rows_affected = c.rowcount

        # Get task details for Discord notification
        c.execute('SELECT * FROM tasks WHERE task_number = ?', (task_number,))
        columns = [description[0] for description in c.description]
        row = c.fetchone()
        conn.commit()
        conn.close()

        if rows_affected == 0:
            return jsonify({'error': f'Task {task_number} not found'}), 404

        task = dict(zip(columns, row)) if row else None

        # Send Discord notification (async, don't wait for it)
        if task and assignee_channel_id:
            asyncio.run_coroutine_threadsafe(
                send_assignment_notification(task, assigned_to, int(assigned_to_id), assignee_channel_id),
                bot.loop
            )

        # Update the original Discord message with assignment info
        if task and task.get('bot_message_id') and task.get('channel_id'):
            asyncio.run_coroutine_threadsafe(
                update_discord_message(task),
                bot.loop
            )

        return jsonify({
            'success': True,
            'message': f'Task {task_number} assigned to {assigned_to}',
            'task_number': task_number,
            'assigned_to': assigned_to
        })
    except Exception as e:
        print(f"ERROR in assign_task: {e}")
        return jsonify({'error': str(e)}), 500

async def send_assignment_notification(task, assigned_to, assigned_to_id, assignee_channel_id):
    """Send Discord notification about task assignment to assignee's personal channel"""
    try:
        # Send to assignee's personal channel (To-Do or RoundTable)
        channel = bot.get_channel(int(assignee_channel_id))
        if not channel:
            print(f"Assignee channel {assignee_channel_id} not found for {assigned_to}")
            return

        assignee_mention = f"<@{assigned_to_id}>"

        embed = discord.Embed(
            title=f"📋 New Task Assigned #{task['task_number']}",
            description=task['title'],
            color=discord.Color.purple()
        )
        embed.add_field(name="Priority", value=task.get('priority', 'medium').upper(), inline=True)
        if task.get('due_date'):
            embed.add_field(name="Due Date", value=task['due_date'], inline=True)
        if task.get('reference_message_link'):
            embed.add_field(name="Original Request", value=f"[View Message]({task['reference_message_link']})", inline=False)
        embed.set_footer(text="React with ✋ to claim or ✅ to complete")

        message = await channel.send(f"{assignee_mention}", embed=embed)

        # Add reaction buttons
        await message.add_reaction('✋')
        await message.add_reaction('✅')

        # Save bot message ID to database for tracking
        update_bot_message_id(task['task_number'], message.id)

        # Also update the channel_id if not set
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''UPDATE tasks SET channel_id = ? WHERE task_number = ?''',
                  (assignee_channel_id, task['task_number']))
        conn.commit()
        conn.close()

        print(f"✅ Sent assignment notification to {assigned_to}'s channel for task #{task['task_number']}")
    except Exception as e:
        print(f"Error sending assignment notification: {e}")

@app.route('/api/tasks/<int:task_number>/update', methods=['PUT'])
def update_task(task_number):
    """Update task details and sync to Discord"""
    try:
        data = request.json

        # Update task in database
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        # Build update query dynamically based on provided fields
        update_fields = []
        update_values = []

        if 'name' in data:
            update_fields.append('title = ?')
            update_values.append(data['name'])
        if 'notes' in data:
            update_fields.append('description = ?')
            update_values.append(data['notes'])
        if 'category' in data:
            update_fields.append('category = ?')
            update_values.append(data['category'])
        if 'priority' in data:
            update_fields.append('priority = ?')
            update_values.append(data['priority'])
        if 'endDate' in data:
            update_fields.append('due_date = ?')
            update_values.append(data['endDate'])
        if 'assignedTo' in data:
            update_fields.append('assigned_to = ?')
            update_values.append(data['assignedTo'])
        if 'status' in data:
            update_fields.append('status = ?')
            update_values.append(data['status'])

        if not update_fields:
            return jsonify({'error': 'No fields to update'}), 400

        # Add task_number to values
        update_values.append(task_number)

        # Execute update
        query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE task_number = ?"
        c.execute(query, update_values)
        rows_affected = c.rowcount

        # Get updated task for Discord sync
        c.execute('SELECT * FROM tasks WHERE task_number = ?', (task_number,))
        columns = [description[0] for description in c.description]
        row = c.fetchone()
        conn.commit()
        conn.close()

        if rows_affected == 0:
            return jsonify({'error': f'Task {task_number} not found'}), 404

        task = dict(zip(columns, row)) if row else None

        # Update Discord message if bot_message_id exists
        if task and task.get('bot_message_id') and task.get('channel_id'):
            asyncio.run_coroutine_threadsafe(
                update_discord_message(task),
                bot.loop
            )

        return jsonify({
            'success': True,
            'message': f'Task {task_number} updated',
            'task_number': task_number
        })
    except Exception as e:
        print(f"ERROR in update_task: {e}")
        return jsonify({'error': str(e)}), 500

async def update_discord_message(task):
    """Update the Discord embed message with new task details"""
    try:
        channel = bot.get_channel(int(task['channel_id']))
        if not channel:
            print(f"Channel {task['channel_id']} not found for task #{task['task_number']}")
            return

        try:
            message = await channel.fetch_message(int(task['bot_message_id']))
        except discord.NotFound:
            print(f"Message {task['bot_message_id']} not found in channel {task['channel_id']}")
            return

        # Create updated embed
        priority_colors = {
            'low': discord.Color.green(),
            'medium': discord.Color.blue(),
            'high': discord.Color.orange(),
            'urgent': discord.Color.red()
        }
        color = priority_colors.get(task.get('priority', 'medium'), discord.Color.blue())

        embed = discord.Embed(
            title=f"📋 Task #{task['task_number']}: {task['title']}",
            description=task.get('description') or 'No description',
            color=color
        )

        # Add fields
        embed.add_field(name="Priority", value=task.get('priority', 'medium').upper(), inline=True)
        embed.add_field(name="Category", value=task.get('category', 'General'), inline=True)
        if task.get('assigned_to'):
            embed.add_field(name="Assigned To", value=task['assigned_to'], inline=True)
        if task.get('due_date'):
            embed.add_field(name="Due Date", value=task['due_date'], inline=True)
        if task.get('status'):
            status_emoji = {'pending': '⏳', 'active': '🔄', 'completed': '✅', 'deleted': '🗑️'}
            embed.add_field(name="Status", value=f"{status_emoji.get(task['status'], '📋')} {task['status'].title()}", inline=True)

        # Get latest update
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''SELECT update_text, updated_by, updated_at FROM task_updates
                     WHERE task_number = ?
                     ORDER BY updated_at DESC LIMIT 1''', (task['task_number'],))
        latest_update = c.fetchone()
        conn.close()

        if latest_update:
            update_text, updated_by, updated_at = latest_update
            embed.add_field(
                name="📝 Latest Update",
                value=f"{update_text}\n*- {updated_by}*",
                inline=False
            )

        # Update the message
        await message.edit(embed=embed)
        print(f"✅ Updated Discord message for task #{task['task_number']}")
    except Exception as e:
        print(f"Error updating Discord message: {e}")

async def update_discord_message_with_latest_update(task, update_text, updated_by):
    """Update Discord message to show the latest update"""
    await update_discord_message(task)

@app.route('/api/tasks', methods=['POST'])
def add_task_from_html():
    """Add task from HTML interface"""
    try:
        data = request.json
        task_number = get_next_task_number()
        
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''INSERT INTO tasks 
                     (task_number, title, created_by, created_by_id, task_type, status, 
                      priority, due_date, category, description)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (task_number, data.get('name'), 'HTML User', 0,
                   'request', 'pending', data.get('priority', 'medium'),
                   data.get('endDate'), data.get('category', 'General'),
                   data.get('notes')))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'task_number': task_number})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assignees', methods=['GET'])
def get_assignees():
    """Get list of unique assignees from tasks"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        # Get unique assignees from both assigned_to and created_by
        c.execute('''SELECT DISTINCT assigned_to FROM tasks 
                     WHERE assigned_to IS NOT NULL AND assigned_to != ''
                     UNION
                     SELECT DISTINCT created_by FROM tasks 
                     WHERE created_by IS NOT NULL AND created_by != ''
                     ORDER BY 1''')
        assignees = [row[0] for row in c.fetchall()]
        conn.close()
        return jsonify(assignees)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get list of unique categories from tasks"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''SELECT DISTINCT category FROM tasks
                     WHERE category IS NOT NULL AND category != ''
                     ORDER BY category''')
        categories = [row[0] for row in c.fetchall()]
        conn.close()
        # Return default categories if none exist yet
        if not categories:
            categories = ['Design', 'Development', 'Bug Fix', 'Feature', 'Documentation', 'Meeting', 'General']
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/permissions', methods=['GET'])
def get_permissions():
    """Get user permissions configuration"""
    try:
        # Try to read from file first
        if os.path.exists('permissions.json'):
            with open('permissions.json', 'r') as f:
                permissions = json.load(f)
                return jsonify(permissions)

        # If no file exists, return empty config (will use defaults on frontend)
        return jsonify({})
    except Exception as e:
        print(f"ERROR in /api/permissions GET: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/permissions', methods=['POST'])
def save_permissions():
    """Save user permissions configuration"""
    try:
        permissions = request.get_json()

        # Save to file
        with open('permissions.json', 'w') as f:
            json.dump(permissions, f, indent=2)

        print(f"✅ Saved permissions for {len(permissions)} users")
        return jsonify({'success': True, 'message': 'Permissions saved'})
    except Exception as e:
        print(f"ERROR in /api/permissions POST: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mentions/<int:user_id>', methods=['GET'])
def get_mentions(user_id):
    """Get mentions for a specific user"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM mentions
                     WHERE user_id = ?
                     ORDER BY created_at DESC
                     LIMIT 100''', (user_id,))
        columns = [description[0] for description in c.description]
        rows = c.fetchall()
        conn.close()

        mentions = []
        for row in rows:
            mention_dict = dict(zip(columns, row))
            mentions.append(mention_dict)

        return jsonify(mentions)
    except Exception as e:
        print(f"ERROR in /api/mentions GET: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mentions/<int:mention_id>/read', methods=['POST'])
def mark_mention_read(mention_id):
    """Mark a mention as read"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('UPDATE mentions SET is_read = 1 WHERE id = ?', (mention_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        print(f"ERROR in /api/mentions mark read: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_number>/complete', methods=['POST'])
def complete_task_api(task_number):
    """Mark a task as completed from HTML"""
    try:
        data = request.get_json() or {}
        completed_by = data.get('completedBy', 'Unknown')

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        # Check if task exists and isn't already completed
        c.execute('SELECT status FROM tasks WHERE task_number = ?', (task_number,)).fetchone()
        task_status = c.execute('SELECT status FROM tasks WHERE task_number = ?', (task_number,)).fetchone()

        if not task_status:
            conn.close()
            return jsonify({'error': 'Task not found'}), 404

        if task_status[0] == 'completed':
            conn.close()
            return jsonify({'message': 'Task already completed'}), 200

        # Update task status
        c.execute('''UPDATE tasks
                     SET status = ?, completed_at = CURRENT_TIMESTAMP, completed_by = ?
                     WHERE task_number = ?''',
                  ('completed', completed_by, task_number))

        # Fetch updated task data for Discord update
        c.execute('SELECT * FROM tasks WHERE task_number = ?', (task_number,))
        columns = [description[0] for description in c.description]
        row = c.fetchone()
        task = dict(zip(columns, row)) if row else None

        conn.commit()
        conn.close()

        # Update the original Discord message
        if task and task.get('bot_message_id') and task.get('channel_id'):
            asyncio.run_coroutine_threadsafe(
                update_discord_message(task),
                bot.loop
            )

        print(f"✅ Task #{task_number} marked as completed by {completed_by} (from HTML)")
        return jsonify({'success': True, 'message': f'Task #{task_number} completed'})
    except Exception as e:
        print(f"ERROR in /api/tasks/complete: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_number>/updates', methods=['GET'])
def get_task_updates(task_number):
    """Get all updates for a task"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM task_updates
                     WHERE task_number = ?
                     ORDER BY updated_at DESC''', (task_number,))
        columns = [description[0] for description in c.description]
        rows = c.fetchall()
        conn.close()

        updates = []
        for row in rows:
            update_dict = dict(zip(columns, row))
            updates.append(update_dict)

        return jsonify(updates)
    except Exception as e:
        print(f"ERROR in /api/tasks/updates: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_number>/updates', methods=['POST'])
def add_task_update(task_number):
    """Add an update to a task"""
    try:
        data = request.get_json() or {}
        update_text = data.get('updateText', '')
        updated_by = data.get('updatedBy', 'Unknown')
        updated_by_id = data.get('updatedById', 0)

        if not update_text:
            return jsonify({'error': 'Update text is required'}), 400

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        # Check if task exists
        c.execute('SELECT * FROM tasks WHERE task_number = ?', (task_number,))
        task_row = c.fetchone()
        if not task_row:
            conn.close()
            return jsonify({'error': 'Task not found'}), 404

        # Insert update
        c.execute('''INSERT INTO task_updates
                     (task_number, update_text, updated_by, updated_by_id)
                     VALUES (?, ?, ?, ?)''',
                  (task_number, update_text, updated_by, updated_by_id))

        update_id = c.lastrowid

        # Get the task details for Discord update
        columns = [description[0] for description in c.description]
        task = dict(zip(columns, task_row))

        conn.commit()
        conn.close()

        # Update Discord message to show latest update
        if task and task.get('bot_message_id') and task.get('channel_id'):
            asyncio.run_coroutine_threadsafe(
                update_discord_message_with_latest_update(task, update_text, updated_by),
                bot.loop
            )

        return jsonify({
            'success': True,
            'update_id': update_id,
            'message': 'Update added successfully'
        })
    except Exception as e:
        print(f"ERROR in /api/tasks/updates POST: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_number>/release-to-pool', methods=['POST'])
def release_to_pool_api(task_number):
    """Release a task back to the pool (unclaim it)"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        # Check if task exists
        c.execute('SELECT task_type FROM tasks WHERE task_number = ?', (task_number,))
        task = c.fetchone()

        if not task:
            conn.close()
            return jsonify({'error': 'Task not found'}), 404

        # Reset claimed status
        c.execute('''UPDATE tasks
                     SET claimed_by = NULL, claimed_by_id = NULL, claimed_at = NULL
                     WHERE task_number = ?''',
                  (task_number,))
        conn.commit()
        conn.close()

        print(f"🔄 Task #{task_number} released back to pool (from HTML)")
        return jsonify({'success': True, 'message': f'Task #{task_number} released to pool'})
    except Exception as e:
        print(f"ERROR in /api/tasks/release-to-pool: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/trainings', methods=['GET'])
def get_trainings():
    """Get all trainings with attendance"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM trainings ORDER BY date DESC')
        columns = [description[0] for description in c.description]
        rows = c.fetchall()

        trainings = []
        for row in rows:
            training_dict = dict(zip(columns, row))

            # Get attendance for this training
            c.execute('''SELECT attendee_name, attendee_id, signed_in_at
                         FROM training_attendance
                         WHERE training_id = ?''', (training_dict['id'],))
            attendance = c.fetchall()
            training_dict['attendees'] = [
                {'name': a[0], 'id': a[1], 'signed_in_at': a[2]}
                for a in attendance
            ]

            trainings.append(training_dict)

        conn.close()
        return jsonify(trainings)
    except Exception as e:
        print(f"ERROR in /api/trainings: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/trainings', methods=['POST'])
def create_training():
    """Create a new training"""
    try:
        data = request.get_json() or {}
        title = data.get('title', '')
        date = data.get('date', '')
        presenter = data.get('presenter', '')
        presenter_id = data.get('presenterId', 0)
        notes = data.get('notes', '')
        category = data.get('category', '')
        created_by = data.get('createdBy', 'Unknown')
        created_by_id = data.get('createdById', 0)

        if not title or not date:
            return jsonify({'error': 'Title and date are required'}), 400

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''INSERT INTO trainings
                     (title, date, presenter, presenter_id, notes, category, created_by, created_by_id)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (title, date, presenter, presenter_id, notes, category, created_by, created_by_id))

        training_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'training_id': training_id})
    except Exception as e:
        print(f"ERROR in /api/trainings POST: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/trainings/<int:training_id>/signin', methods=['POST'])
def training_signin(training_id):
    """Sign in to a training"""
    try:
        data = request.get_json() or {}
        attendee_name = data.get('attendeeName', '')
        attendee_id = data.get('attendeeId', 0)

        if not attendee_name:
            return jsonify({'error': 'Attendee name is required'}), 400

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        # Check if already signed in
        c.execute('''SELECT id FROM training_attendance
                     WHERE training_id = ? AND attendee_id = ?''',
                  (training_id, attendee_id))
        if c.fetchone():
            conn.close()
            return jsonify({'message': 'Already signed in'}), 200

        c.execute('''INSERT INTO training_attendance (training_id, attendee_name, attendee_id)
                     VALUES (?, ?, ?)''',
                  (training_id, attendee_name, attendee_id))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Signed in successfully'})
    except Exception as e:
        print(f"ERROR in training signin: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/important-messages', methods=['GET'])
def get_important_messages():
    """Get all important messages with reaction tracking"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM important_messages ORDER BY posted_at DESC')
        columns = [description[0] for description in c.description]
        rows = c.fetchall()

        messages = []
        for row in rows:
            msg_dict = dict(zip(columns, row))

            # Get reactions for this message
            c.execute('''SELECT user_name, user_id, reacted_at, reminder_count, manager_notified
                         FROM message_reactions
                         WHERE message_id = ?''', (msg_dict['message_id'],))
            reactions = c.fetchall()
            msg_dict['reactions'] = [
                {
                    'user_name': r[0],
                    'user_id': r[1],
                    'reacted_at': r[2],
                    'reminder_count': r[3],
                    'manager_notified': r[4]
                }
                for r in reactions
            ]

            messages.append(msg_dict)

        conn.close()
        return jsonify(messages)
    except Exception as e:
        print(f"ERROR in /api/important-messages: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/important-messages/<int:message_id>/react', methods=['POST'])
def mark_message_read(message_id):
    """Mark an important message as read"""
    try:
        data = request.get_json() or {}
        user_name = data.get('userName', '')
        user_id = data.get('userId', 0)

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        # Check if already reacted
        c.execute('''SELECT id FROM message_reactions
                     WHERE message_id = ? AND user_id = ?''',
                  (message_id, user_id))
        if c.fetchone():
            conn.close()
            return jsonify({'message': 'Already marked as read'}), 200

        c.execute('''INSERT INTO message_reactions (message_id, user_name, user_id)
                     VALUES (?, ?, ?)''',
                  (message_id, user_name, user_id))
        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        print(f"ERROR in mark message read: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'bot': bot.user.name if bot.user else 'starting',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/admin-config', methods=['POST'])
def update_admin_config():
    """
    Receive configuration updates from Admin Panel
    Updates the bot's CONFIG dictionary with Discord channels, users, and other settings
    """
    try:
        data = request.get_json() or {}

        # Update Discord configuration if provided
        if 'discordConfig' in data:
            discord_config = data['discordConfig']

            # Map discord config to employee CONFIG structure
            # The admin panel sends: {channels: {name: id}, users: {name: id}, threads: {name: id}}
            # We need to update CONFIG['employees'] and CONFIG['global_logs']

            # Store discord config for reference (can be used by bot commands)
            CONFIG['discord_channels'] = discord_config.get('channels', {})
            CONFIG['discord_users'] = discord_config.get('users', {})
            CONFIG['discord_threads'] = discord_config.get('threads', {})

        # Update channels configuration
        if 'channels' in data:
            CONFIG['channels'] = data['channels']

        # Update users configuration
        if 'users' in data:
            CONFIG['users'] = data['users']

        # Update reactions
        if 'reactions' in data:
            CONFIG['reactions'] = data['reactions']

        # Update bot messages
        if 'botConfig' in data and 'messages' in data['botConfig']:
            CONFIG['bot_messages'] = data['botConfig']['messages']

        # Update categories
        if 'categories' in data:
            CONFIG['categories'] = data['categories']

        # Update departments and roles
        if 'departments' in data:
            CONFIG['departments'] = data['departments']
        if 'roles' in data:
            CONFIG['roles'] = data['roles']

        # Save config to file for persistence across restarts
        try:
            with open('bot_config.json', 'w') as f:
                json.dump(CONFIG, f, indent=2)
            print("✅ Admin config saved to bot_config.json")
        except Exception as e:
            print(f"⚠️ Failed to save config to file: {e}")

        print(f"✅ Admin config updated from Admin Panel")
        return jsonify({
            'success': True,
            'message': 'Configuration updated successfully',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"ERROR in /api/admin-config: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    """Root endpoint"""
    return jsonify({
        'message': 'BottyOtty Task Manager API',
        'status': 'running',
        'endpoints': ['/api/tasks', '/api/health']
    })

def run_flask():
    """Run Flask API server"""
    print(f"✅ Flask server starting on 0.0.0.0:{PORT}")
    try:
        app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False, threaded=True)
    except Exception as e:
        print(f"❌ Flask failed to start: {e}")

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='@', intents=intents)

# Load saved config from Admin Panel if it exists
try:
    if os.path.exists('bot_config.json'):
        with open('bot_config.json', 'r') as f:
            saved_config = json.load(f)
            # Update CONFIG with saved values
            if 'discord_channels' in saved_config:
                CONFIG['discord_channels'] = saved_config['discord_channels']
            if 'discord_users' in saved_config:
                CONFIG['discord_users'] = saved_config['discord_users']
            if 'discord_threads' in saved_config:
                CONFIG['discord_threads'] = saved_config['discord_threads']
            if 'channels' in saved_config:
                CONFIG['channels'] = saved_config['channels']
            if 'users' in saved_config:
                CONFIG['users'] = saved_config['users']
            if 'reactions' in saved_config:
                CONFIG['reactions'] = saved_config['reactions']
            if 'categories' in saved_config:
                CONFIG['categories'] = saved_config['categories']
            if 'departments' in saved_config:
                CONFIG['departments'] = saved_config['departments']
            if 'roles' in saved_config:
                CONFIG['roles'] = saved_config['roles']
            print("✅ Loaded configuration from bot_config.json")
except Exception as e:
    print(f"⚠️ Could not load bot_config.json: {e}")

# Authorized users who can use 📌 reaction to add tasks (Managers)
AUTHORIZED_USERS = [
    1228184859772588042,  # Joey
    1189283572100645005,  # Presley
    931331954220101632,   # Lauren
    289212918615244801,   # Ash
    353922166250799106,   # Adam
    1297804315041333354,  # Chase
    928725439059464222,   # Megan
    220326831524544513,   # Dakota
    1060679174945259520   # Preston
]

# Authorized users who can use 🔥 reaction for Campfire tasks
CAMPFIRE_AUTHORIZED_USERS = [
    931331954220101632,   # Lauren
    928725439059464222    # Megan
]

# User authorized for extra custom reaction (set EXTRA_REACT_EMOJI below)
EXTRA_REACT_USER = 289212918615244801  # Ash
EXTRA_REACT_EMOJI = '⭐'  # Change this to your custom emoji

# Pool Channel IDs
POOL_CHANNELS = {
    'SMOT Pool': 1440575030118449152,
    'OM Pool': 1440575273778286684,
    'Cube Pool': 1440575543358525555
}

# Personal assignment channels (To-Dos and RoundTables)
PERSONAL_CHANNELS = {
    # To-Dos
    'Ash': 1392524881723392040,
    'Preston': 1378435914375757865,
    'Presley': 1378435889507733655,
    'Joey': 1378435818745499781,
    'Jeff': 1378435776823562473,
    'Dakota': 1378435732338643066,
    'Adam': 1378435680555765841,
    # RoundTables
    'Dahlya': 1364145512344981515,
    'Araceli': 1364145395956977705,
    'Terry': 1364146225959403520,
    'Cole': 1427801942327038002,
    'Devin': 1364145559119597638,
    'Amanda': 1425968878848311326,
    'Caleb': 1364145445017882634,
    'Charles': 1437224826703056996,
    'Dylan': 1364145584524759121,
    'Edward': 1425939780025192498,
    'Fernando': 1437224785632428062,
    'Hector': 1364145633333739590,
    'Isiac': 1364145675700273274,
    'Jose': 1364145746693324830,
    'Matt Kiger': 1364145899839815690,
    'Logan': 1387470240988008551,
    'Nathaniel': 1364145942231519262,
    'Rachel': 1364146051338211388,
    'Rafael': 1364146128861528186,
    'Raymond': 1387465577035202661,
    'Ric': 1399765599542050816,
    'Ryan M': 1364146186658910259,
    'Ryan P': 1425941108889751712,
    'Sam': 1364317982985031711,
    'Sean': 1387465649772826664,
    'Summer': 1364146209895223337,
    'Tony': 1364146256292610110,
    'Trevor': 1364146273191460934,
    'Tyler': 1364146301805269063,
    'Chase': 0,  # TODO: Add Chase's channel
    'Lauren': 0,  # TODO: Add Lauren's channel
    'Megan': 0   # TODO: Add Megan's channel
}

# Custom Reaction Auto-Assignment (for high-volume users)
# Maps emoji -> (user_name, user_id, channel_id)
REACTION_ASSIGNMENTS = {
    '👍': ('Ash', 289212918615244801, 1392524881723392040),  # Thumbs up → Ash
    # Add more as needed:
    # '👋': ('Ryan M', user_id, channel_id),
    # '💪': ('Lauren', user_id, channel_id),
}

@bot.tree.command(
    name="exportimages",
    description="Export image attachment links from a channel within a date range and DM them to you (NDJSON).",
)
@app_commands.describe(
    channel="Channel to scan (default: the channel where you run this).",
    mode="Timeframe preset or custom range.",
    start="For custom mode: start date (YYYY-MM-DD).",
    end="For custom mode: end date (YYYY-MM-DD, optional).",
    max_messages="Max messages to scan (default 5000).",
)
@app_commands.choices(
    mode=[
        app_commands.Choice(name="Last 30 days", value="last_30"),
        app_commands.Choice(name="Last 90 days", value="last_90"),
        app_commands.Choice(name="Custom range", value="custom"),
    ]
)
async def exportimages(
    interaction: discord.Interaction,
    channel: Optional[discord.TextChannel] = None,
    mode: app_commands.Choice[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    max_messages: int = 5000,
):
    """Export image attachment metadata as NDJSON via DM."""

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ You need administrator permissions to use this command.",
            ephemeral=True,
        )
        return

    mode_value = mode.value if mode is not None else "last_30"
    now = datetime.utcnow()
    after_dt: Optional[datetime] = None
    before_dt: Optional[datetime] = None
    range_text = ""

    if mode_value == "last_30":
        after_dt = now - timedelta(days=30)
        range_text = f"from {after_dt.date()} to now (last 30 days)"
    elif mode_value == "last_90":
        after_dt = now - timedelta(days=90)
        range_text = f"from {after_dt.date()} to now (last 90 days)"
    else:
        if not start:
            await interaction.response.send_message(
                "⚠️ In custom mode you must provide a start date (YYYY-MM-DD).",
                ephemeral=True,
            )
            return
        after_dt = parse_date_str(start)
        if after_dt is None:
            await interaction.response.send_message(
                "⚠️ Could not parse start date. Use format YYYY-MM-DD.",
                ephemeral=True,
            )
            return
        if end:
            before_dt = parse_date_str(end)
            if before_dt is None:
                await interaction.response.send_message(
                    "⚠️ Could not parse end date. Use format YYYY-MM-DD.",
                    ephemeral=True,
                )
                return
            range_text = f"from {after_dt.date()} to {before_dt.date()}"
        else:
            range_text = f"from {after_dt.date()} onward"

    await interaction.response.defer(ephemeral=True)

    target_channel = channel or interaction.channel
    total_scanned = 0
    image_count = 0
    lines: list[str] = []

    async for msg in target_channel.history(
        limit=max_messages,
        oldest_first=True,
        after=after_dt,
        before=before_dt,
    ):
        total_scanned += 1
        for attachment in msg.attachments:
            content_type = attachment.content_type or ""
            if not content_type.startswith("image"):
                continue
            image_count += 1
            record = {
                "url": attachment.url,
                "filename": attachment.filename,
                "content_type": content_type or None,
                "size": attachment.size,
                "kind": "image",
                "author": msg.author.display_name,
                "message_id": msg.id,
                "timestamp": msg.created_at.isoformat(),
                "channel_id": msg.channel.id,
                "channel_name": msg.channel.name,
                "guild_id": msg.guild.id if msg.guild else None,
                "guild_name": msg.guild.name if msg.guild else None,
            }
            lines.append(json.dumps(record, ensure_ascii=False))

    if image_count == 0:
        await interaction.followup.send(
            f"ℹ️ I didn't find any **image** attachments in {target_channel.mention} "
            f"({range_text}, scanned {total_scanned} messages).",
            ephemeral=True,
        )
        return

    full_report = "\n".join(lines)
    chunks = []
    remaining = full_report
    while remaining:
        chunk = remaining[:1900]
        last_nl = chunk.rfind("\n")
        if last_nl != -1:
            chunk, remaining = remaining[:last_nl], remaining[last_nl + 1 :]
        else:
            remaining = remaining[1900:]
        chunks.append(chunk)

    for chunk in chunks:
        await interaction.user.send(f"```{chunk}```")

    await interaction.followup.send(
        f"✅ Found {image_count} **image** attachment(s) in "
        f"{target_channel.mention} ({range_text}, scanned {total_scanned} messages). "
        f"I’ve DM’d you the NDJSON export.",
        ephemeral=True,
    )


@bot.tree.command(
    name="exportfiles",
    description="Export non-image file attachment links from a channel within a date range and DM them to you (NDJSON).",
)
@app_commands.describe(
    channel="Channel to scan (default: the channel where you run this).",
    mode="Timeframe preset or custom range.",
    start="For custom mode: start date (YYYY-MM-DD).",
    end="For custom mode: end date (YYYY-MM-DD, optional).",
    max_messages="Max messages to scan (default 5000).",
)
@app_commands.choices(
    mode=[
        app_commands.Choice(name="Last 30 days", value="last_30"),
        app_commands.Choice(name="Last 90 days", value="last_90"),
        app_commands.Choice(name="Custom range", value="custom"),
    ]
)
async def exportfiles(
    interaction: discord.Interaction,
    channel: Optional[discord.TextChannel] = None,
    mode: app_commands.Choice[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    max_messages: int = 5000,
):
    """Export non-image file attachment metadata as NDJSON via DM."""

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ You need administrator permissions to use this command.",
            ephemeral=True,
        )
        return

    mode_value = mode.value if mode is not None else "last_30"
    now = datetime.utcnow()
    after_dt: Optional[datetime] = None
    before_dt: Optional[datetime] = None
    range_text = ""

    if mode_value == "last_30":
        after_dt = now - timedelta(days=30)
        range_text = f"from {after_dt.date()} to now (last 30 days)"
    elif mode_value == "last_90":
        after_dt = now - timedelta(days=90)
        range_text = f"from {after_dt.date()} to now (last 90 days)"
    else:
        if not start:
            await interaction.response.send_message(
                "⚠️ In custom mode you must provide a start date (YYYY-MM-DD).",
                ephemeral=True,
            )
            return
        after_dt = parse_date_str(start)
        if after_dt is None:
            await interaction.response.send_message(
                "⚠️ Could not parse start date. Use format YYYY-MM-DD.",
                ephemeral=True,
            )
            return
        if end:
            before_dt = parse_date_str(end)
            if before_dt is None:
                await interaction.response.send_message(
                    "⚠️ Could not parse end date. Use format YYYY-MM-DD.",
                    ephemeral=True,
                )
                return
            range_text = f"from {after_dt.date()} to {before_dt.date()}"
        else:
            range_text = f"from {after_dt.date()} onward"

    await interaction.response.defer(ephemeral=True)

    target_channel = channel or interaction.channel
    total_scanned = 0
    file_count = 0
    lines: list[str] = []

    async for msg in target_channel.history(
        limit=max_messages,
        oldest_first=True,
        after=after_dt,
        before=before_dt,
    ):
        total_scanned += 1
        for attachment in msg.attachments:
            content_type = attachment.content_type or ""
            if content_type.startswith("image"):
                continue
            file_count += 1
            record = {
                "url": attachment.url,
                "filename": attachment.filename,
                "content_type": content_type or None,
                "size": attachment.size,
                "kind": "file",
                "author": msg.author.display_name,
                "message_id": msg.id,
                "timestamp": msg.created_at.isoformat(),
                "channel_id": msg.channel.id,
                "channel_name": msg.channel.name,
                "guild_id": msg.guild.id if msg.guild else None,
                "guild_name": msg.guild.name if msg.guild else None,
            }
            lines.append(json.dumps(record, ensure_ascii=False))

    if file_count == 0:
        await interaction.followup.send(
            f"ℹ️ I didn't find any **file** attachments (non-images) in {target_channel.mention} "
            f"({range_text}, scanned {total_scanned} messages).",
            ephemeral=True,
        )
        return

    full_report = "\n".join(lines)
    chunks = []
    remaining = full_report
    while remaining:
        chunk = remaining[:1900]
        last_nl = chunk.rfind("\n")
        if last_nl != -1:
            chunk, remaining = remaining[:last_nl], remaining[last_nl + 1 :]
        else:
            remaining = remaining[1900:]
        chunks.append(chunk)

    for chunk in chunks:
        await interaction.user.send(f"```{chunk}```")

    await interaction.followup.send(
        f"✅ Found {file_count} **file** attachment(s) (non-images) in "
        f"{target_channel.mention} ({range_text}, scanned {total_scanned} messages). "
        f"I’ve DM’d you the NDJSON export.",
        ephemeral=True,
    )


# ============================================================
# REQUEST PANEL MODALS & BUTTON VIEW
# (inlined from discord_request_buttons.py)
# ============================================================

class UniformModal(ui.Modal, title="Uniform Request"):
    item = ui.TextInput(
        label="What do you need?",
        placeholder="polo, hat, jacket, pants...",
        required=True
    )
    size = ui.TextInput(
        label="Size",
        placeholder="S / M / L / XL / XXL",
        required=True
    )
    quantity = ui.TextInput(
        label="Quantity",
        placeholder="1",
        default="1",
        required=True
    )
    notes = ui.TextInput(
        label="Notes (optional)",
        placeholder="Any special instructions?",
        required=False,
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Build title and description
        title = f"Uniform: {self.item.value} (Size {self.size.value})"
        description = f"Item: {self.item.value}\nSize: {self.size.value}\nQuantity: {self.quantity.value}"
        if self.notes.value:
            description += f"\nNotes: {self.notes.value}"

        # Add to database
        task_number = add_task(
            title=title,
            description=description,
            created_by=interaction.user.display_name,
            created_by_id=interaction.user.id,
            task_type='form-request',
            category='Uniform',
            channel_id=interaction.channel_id
        )

        embed = discord.Embed(
            title=f"✅ Uniform Request #{task_number}",
            color=0xFFAA00
        )
        embed.add_field(name="Item", value=self.item.value, inline=True)
        embed.add_field(name="Size", value=self.size.value, inline=True)
        embed.add_field(name="Quantity", value=self.quantity.value, inline=True)
        if self.notes.value:
            embed.add_field(name="Notes", value=self.notes.value, inline=False)
        embed.add_field(name="Status", value="⏳ Pending", inline=True)
        embed.set_footer(text=f"Submitted by {interaction.user.display_name}")
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(
            "✅ Request submitted! Tracking below:",
            embed=embed
        )

        # Get the message and update the bot_message_id in database
        bot_msg = await interaction.original_response()
        update_bot_message_id(task_number, bot_msg.id)


class VehicleModal(ui.Modal, title="Vehicle Issue Report"):
    vehicle_number = ui.TextInput(
        label="Vehicle Number",
        placeholder="e.g., 12, 47, 103...",
        required=True
    )
    issue = ui.TextInput(
        label="What's wrong?",
        placeholder="Describe the issue...",
        required=True,
        style=discord.TextStyle.paragraph
    )
    urgency = ui.TextInput(
        label="Urgency",
        placeholder="Can wait / Soon / URGENT - Safety Issue",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Build title and description
        title = f"Vehicle #{self.vehicle_number.value} Issue"
        description = f"Vehicle: #{self.vehicle_number.value}\nUrgency: {self.urgency.value}\nIssue: {self.issue.value}"

        # Add to database
        task_number = add_task(
            title=title,
            description=description,
            created_by=interaction.user.display_name,
            created_by_id=interaction.user.id,
            task_type='form-request',
            category='Vehicle',
            channel_id=interaction.channel_id
        )

        embed = discord.Embed(
            title=f"✅ Vehicle Issue #{task_number}",
            color=0xFFAA00
        )
        embed.add_field(name="Vehicle #", value=self.vehicle_number.value, inline=True)
        embed.add_field(name="Urgency", value=self.urgency.value, inline=True)
        embed.add_field(name="Issue", value=self.issue.value, inline=False)
        embed.add_field(name="Status", value="⏳ Pending", inline=True)
        embed.set_footer(text=f"Submitted by {interaction.user.display_name}")
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(
            "✅ Request submitted! Tracking below:",
            embed=embed
        )

        # Get the message and update the bot_message_id in database
        bot_msg = await interaction.original_response()
        update_bot_message_id(task_number, bot_msg.id)


class PrintModal(ui.Modal, title="Print Materials Request"):
    item = ui.TextInput(
        label="What do you need printed?",
        placeholder="door hangers, business cards, flyers...",
        required=True
    )
    quantity = ui.TextInput(
        label="Quantity",
        placeholder="50",
        required=True
    )
    instructions = ui.TextInput(
        label="Special Instructions (optional)",
        placeholder="Any specific details?",
        required=False,
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Build title and description
        title = f"Print: {self.item.value} (Qty: {self.quantity.value})"
        description = f"Item: {self.item.value}\nQuantity: {self.quantity.value}"
        if self.instructions.value:
            description += f"\nInstructions: {self.instructions.value}"

        # Add to database
        task_number = add_task(
            title=title,
            description=description,
            created_by=interaction.user.display_name,
            created_by_id=interaction.user.id,
            task_type='form-request',
            category='Print',
            channel_id=interaction.channel_id
        )

        embed = discord.Embed(
            title=f"✅ Print Request #{task_number}",
            color=0xFFAA00
        )
        embed.add_field(name="Item", value=self.item.value, inline=True)
        embed.add_field(name="Quantity", value=self.quantity.value, inline=True)
        if self.instructions.value:
            embed.add_field(name="Instructions", value=self.instructions.value, inline=False)
        embed.add_field(name="Status", value="⏳ Pending", inline=True)
        embed.set_footer(text=f"Submitted by {interaction.user.display_name}")
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(
            "✅ Request submitted! Tracking below:",
            embed=embed
        )

        # Get the message and update the bot_message_id in database
        bot_msg = await interaction.original_response()
        update_bot_message_id(task_number, bot_msg.id)


class IDCardModal(ui.Modal, title="ID Card Request"):
    reason = ui.TextInput(
        label="Reason",
        placeholder="Lost, damaged, name change, new hire...",
        required=True
    )
    notes = ui.TextInput(
        label="Additional Notes (optional)",
        placeholder="Any other details?",
        required=False,
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Build title and description
        title = f"ID Card: {self.reason.value}"
        description = f"Reason: {self.reason.value}"
        if self.notes.value:
            description += f"\nNotes: {self.notes.value}"

        # Add to database
        task_number = add_task(
            title=title,
            description=description,
            created_by=interaction.user.display_name,
            created_by_id=interaction.user.id,
            task_type='form-request',
            category='ID Card',
            channel_id=interaction.channel_id
        )

        embed = discord.Embed(
            title=f"✅ ID Card Request #{task_number}",
            color=0xFFAA00
        )
        embed.add_field(name="Reason", value=self.reason.value, inline=True)
        if self.notes.value:
            embed.add_field(name="Notes", value=self.notes.value, inline=False)
        embed.add_field(name="Status", value="⏳ Pending", inline=True)
        embed.set_footer(text=f"Submitted by {interaction.user.display_name}")
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(
            "✅ Request submitted! Tracking below:",
            embed=embed
        )

        # Get the message and update the bot_message_id in database
        bot_msg = await interaction.original_response()
        update_bot_message_id(task_number, bot_msg.id)


class ReimbursementModal(ui.Modal, title="Reimbursement Request"):
    amount = ui.TextInput(
        label="Amount ($)",
        placeholder="e.g., 45.99",
        required=True
    )
    description = ui.TextInput(
        label="What was it for?",
        placeholder="Describe the purchase...",
        required=True,
        style=discord.TextStyle.paragraph
    )
    receipt_note = ui.TextInput(
        label="Receipt",
        placeholder="Attach photo to this channel after submitting OR note where it is",
        required=True,
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Build title and description
        title = f"Reimbursement: ${self.amount.value}"
        description = f"Amount: ${self.amount.value}\nFor: {self.description.value}\nReceipt: {self.receipt_note.value}"

        # Add to database
        task_number = add_task(
            title=title,
            description=description,
            created_by=interaction.user.display_name,
            created_by_id=interaction.user.id,
            task_type='form-request',
            category='Reimbursement',
            channel_id=interaction.channel_id
        )

        embed = discord.Embed(
            title=f"✅ Reimbursement Request #{task_number}",
            color=0xFFAA00
        )
        embed.add_field(name="Amount", value=f"${self.amount.value}", inline=True)
        embed.add_field(name="For", value=self.description.value, inline=False)
        embed.add_field(name="Receipt", value=self.receipt_note.value, inline=False)
        embed.add_field(name="Status", value="⏳ Pending", inline=True)
        embed.set_footer(text=f"Submitted by {interaction.user.display_name}")
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(
            "✅ Request submitted! Tracking below:",
            embed=embed
        )

        # Get the message and update the bot_message_id in database
        bot_msg = await interaction.original_response()
        update_bot_message_id(task_number, bot_msg.id)


class MeetingModal(ui.Modal, title="Meeting Request"):
    meeting_type = ui.TextInput(
        label="Meeting Type",
        placeholder="Owner Meeting or General Meeting",
        required=True
    )
    topic = ui.TextInput(
        label="What's it about?",
        placeholder="Brief description of what you want to discuss...",
        required=True,
        style=discord.TextStyle.paragraph
    )
    preferred_time = ui.TextInput(
        label="Preferred Time (optional)",
        placeholder="e.g., 'This week' or 'Tuesday afternoon'",
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Build title and description
        title = f"Meeting: {self.meeting_type.value}"
        description = f"Type: {self.meeting_type.value}\nTopic: {self.topic.value}"
        if self.preferred_time.value:
            description += f"\nPreferred Time: {self.preferred_time.value}"

        # Add to database
        task_number = add_task(
            title=title,
            description=description,
            created_by=interaction.user.display_name,
            created_by_id=interaction.user.id,
            task_type='form-request',
            category='Meeting',
            channel_id=interaction.channel_id
        )

        embed = discord.Embed(
            title=f"✅ Meeting Request #{task_number}",
            color=0xFFAA00
        )
        embed.add_field(name="Type", value=self.meeting_type.value, inline=True)
        embed.add_field(name="Topic", value=self.topic.value, inline=False)
        if self.preferred_time.value:
            embed.add_field(name="Preferred Time", value=self.preferred_time.value, inline=True)
        embed.add_field(name="Status", value="⏳ Pending", inline=True)
        embed.set_footer(text=f"Submitted by {interaction.user.display_name}")
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(
            "✅ Request submitted! Tracking below:",
            embed=embed
        )

        # Get the message and update the bot_message_id in database
        bot_msg = await interaction.original_response()
        update_bot_message_id(task_number, bot_msg.id)


class SafetyGearModal(ui.Modal, title="Safety Gear Request"):
    item = ui.TextInput(
        label="What do you need?",
        placeholder="gloves, safety glasses, respirator, etc...",
        required=True
    )
    size = ui.TextInput(
        label="Size (if applicable)",
        placeholder="S / M / L / XL or N/A",
        required=True
    )
    quantity = ui.TextInput(
        label="Quantity",
        placeholder="1",
        default="1",
        required=True
    )
    reason = ui.TextInput(
        label="Reason",
        placeholder="Replacement, new, damaged...",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Build title and description
        title = f"Safety Gear: {self.item.value}"
        description = f"Item: {self.item.value}\nSize: {self.size.value}\nQuantity: {self.quantity.value}\nReason: {self.reason.value}"

        # Add to database
        task_number = add_task(
            title=title,
            description=description,
            created_by=interaction.user.display_name,
            created_by_id=interaction.user.id,
            task_type='form-request',
            category='Safety Gear',
            channel_id=interaction.channel_id
        )

        embed = discord.Embed(
            title=f"✅ Safety Gear Request #{task_number}",
            color=0xFFAA00
        )
        embed.add_field(name="Item", value=self.item.value, inline=True)
        embed.add_field(name="Size", value=self.size.value, inline=True)
        embed.add_field(name="Quantity", value=self.quantity.value, inline=True)
        embed.add_field(name="Reason", value=self.reason.value, inline=False)
        embed.add_field(name="Status", value="⏳ Pending", inline=True)
        embed.set_footer(text=f"Submitted by {interaction.user.display_name}")
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(
            "✅ Request submitted! Tracking below:",
            embed=embed
        )

        # Get the message and update the bot_message_id in database
        bot_msg = await interaction.original_response()
        update_bot_message_id(task_number, bot_msg.id)


class OtherRequestModal(ui.Modal, title="Other Request"):
    category = ui.TextInput(
        label="What type of request is this?",
        placeholder="Describe the category...",
        required=True
    )
    details = ui.TextInput(
        label="Details",
        placeholder="Explain what you need...",
        required=True,
        style=discord.TextStyle.paragraph
    )
    urgency = ui.TextInput(
        label="Urgency",
        placeholder="Can wait / Soon / Urgent",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Build title and description
        title = f"Other: {self.category.value}"
        description = f"Category: {self.category.value}\nUrgency: {self.urgency.value}\nDetails: {self.details.value}"

        # Add to database
        task_number = add_task(
            title=title,
            description=description,
            created_by=interaction.user.display_name,
            created_by_id=interaction.user.id,
            task_type='form-request',
            category='Other',
            channel_id=interaction.channel_id
        )

        embed = discord.Embed(
            title=f"✅ Other Request #{task_number}",
            color=0xFFAA00
        )
        embed.add_field(name="Category", value=self.category.value, inline=True)
        embed.add_field(name="Urgency", value=self.urgency.value, inline=True)
        embed.add_field(name="Details", value=self.details.value, inline=False)
        embed.add_field(name="Status", value="⏳ Pending", inline=True)
        embed.set_footer(text=f"Submitted by {interaction.user.display_name}")
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(
            "✅ Request submitted! Tracking below:",
            embed=embed
        )

        # Get the message and update the bot_message_id in database
        bot_msg = await interaction.original_response()
        update_bot_message_id(task_number, bot_msg.id)


class CallOutModal(ui.Modal, title="Call-Out"):
    date = ui.TextInput(label="Date", placeholder="YYYY-MM-DD", required=True)
    reason = ui.TextInput(label="Reason", required=True)
    notes = ui.TextInput(label="Notes", style=discord.TextStyle.paragraph, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        employee_key = get_employee_by_log_channel(interaction.channel_id)
        if not employee_key:
            await interaction.response.send_message("This channel is not linked to an employee log.", ephemeral=True)
            return

        fields = {
            "Date": self.date.value,
            "Reason": self.reason.value,
            "Notes": self.notes.value,
            "Submitted by": interaction.user.mention,
        }
        await log_event(bot, employee_key, "call_out", "Call-Out Logged", fields, "call_outs")
        await interaction.response.send_message("Your call-out has been logged.", ephemeral=True)


class HoursUpdateModal(ui.Modal, title="Hours Update"):
    date = ui.TextInput(label="Date", placeholder="YYYY-MM-DD", required=True)
    update = ui.TextInput(label="Update", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        employee_key = get_employee_by_log_channel(interaction.channel_id)
        if not employee_key:
            await interaction.response.send_message("This channel is not linked to an employee log.", ephemeral=True)
            return

        fields = {
            "Date": self.date.value,
            "Update": self.update.value,
            "Submitted by": interaction.user.mention,
        }
        await log_event(bot, employee_key, "hours_update", "Hours Update Logged", fields, "hours_updates")
        await interaction.response.send_message("Your hours update has been logged.", ephemeral=True)


class TechCollectionsModal(ui.Modal, title="Tech Collections"):
    amount = ui.TextInput(label="Amount", placeholder="$0.00", required=True)
    customer = ui.TextInput(label="Customer / Account", required=True)
    notes = ui.TextInput(label="Notes", style=discord.TextStyle.paragraph, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        employee_key = get_employee_by_log_channel(interaction.channel_id)
        if not employee_key:
            await interaction.response.send_message("This channel is not linked to an employee log.", ephemeral=True)
            return

        fields = {
            "Amount": self.amount.value,
            "Customer": self.customer.value,
            "Notes": self.notes.value,
            "Submitted by": interaction.user.mention,
        }
        await log_event(bot, employee_key, "tech_collection", "Tech Collection Logged", fields, "tech_collections")
        await interaction.response.send_message("Your tech collection has been logged.", ephemeral=True)


class PanelReimbursementModal(ui.Modal, title="Reimbursement"):
    item = ui.TextInput(label="What for?", required=True)
    amount = ui.TextInput(label="Amount", placeholder="$0.00", required=False)
    notes = ui.TextInput(label="Notes", style=discord.TextStyle.paragraph, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        employee_key = get_employee_by_log_channel(interaction.channel_id)
        if not employee_key:
            await interaction.response.send_message("This channel is not linked to an employee log.", ephemeral=True)
            return

        fields = {
            "Item": self.item.value,
            "Amount": self.amount.value,
            "Notes": self.notes.value,
            "Submitted by": interaction.user.mention,
        }
        await log_event(bot, employee_key, "reimbursement", "Reimbursement Logged", fields, "requests")
        await interaction.response.send_message("Your reimbursement request has been logged.", ephemeral=True)


class PanelUniformModal(ui.Modal, title="Uniform Request"):
    item = ui.TextInput(label="Item", placeholder="Shirt, pants, etc.", required=True)
    size = ui.TextInput(label="Size", required=True)
    quantity = ui.TextInput(label="Quantity", required=False, default="1")
    notes = ui.TextInput(label="Notes", style=discord.TextStyle.paragraph, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        employee_key = get_employee_by_log_channel(interaction.channel_id)
        if not employee_key:
            await interaction.response.send_message("This channel is not linked to an employee log.", ephemeral=True)
            return

        fields = {
            "Item": self.item.value,
            "Size": self.size.value,
            "Quantity": self.quantity.value,
            "Notes": self.notes.value,
            "Submitted by": interaction.user.mention,
        }
        await log_event(bot, employee_key, "uniform", "Uniform Request Logged", fields, "requests")
        await interaction.response.send_message("Your uniform request has been logged.", ephemeral=True)


class PanelIDCardModal(ui.Modal, title="ID Card Request"):
    name = ui.TextInput(label="Name on Card", required=True)
    reason = ui.TextInput(label="Reason", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        employee_key = get_employee_by_log_channel(interaction.channel_id)
        if not employee_key:
            await interaction.response.send_message("This channel is not linked to an employee log.", ephemeral=True)
            return

        fields = {
            "Name": self.name.value,
            "Reason": self.reason.value,
            "Submitted by": interaction.user.mention,
        }
        await log_event(bot, employee_key, "id_card", "ID Card Request Logged", fields, "requests")
        await interaction.response.send_message("Your ID card request has been logged.", ephemeral=True)


class PanelCompanyCardModal(ui.Modal, title="Company Card Request"):
    reason = ui.TextInput(label="Reason for Card", required=True)
    notes = ui.TextInput(label="Notes", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        employee_key = get_employee_by_log_channel(interaction.channel_id)
        if not employee_key:
            await interaction.response.send_message("This channel is not linked to an employee log.", ephemeral=True)
            return

        fields = {
            "Reason": self.reason.value,
            "Notes": self.notes.value,
            "Submitted by": interaction.user.mention,
        }
        await log_event(bot, employee_key, "company_card", "Company Card Request Logged", fields, "requests")
        await interaction.response.send_message("Your company card request has been logged.", ephemeral=True)


class VehicleIssueModal(ui.Modal, title="Vehicle Issue"):
    vehicle = ui.TextInput(label="Vehicle", placeholder="Truck/Van number", required=True)
    issue = ui.TextInput(label="Issue", style=discord.TextStyle.paragraph, required=True)
    safe_to_drive = ui.TextInput(label="Is it safe to drive?", placeholder="Yes/No/Unsure", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        employee_key = get_employee_by_log_channel(interaction.channel_id)
        if not employee_key:
            await interaction.response.send_message("This channel is not linked to an employee log.", ephemeral=True)
            return

        fields = {
            "Vehicle": self.vehicle.value,
            "Issue": self.issue.value,
            "Safe to drive": self.safe_to_drive.value,
            "Submitted by": interaction.user.mention,
        }
        await log_event(bot, employee_key, "vehicle_issue", "Vehicle Issue Logged", fields, "vehicle_issues")
        await interaction.response.send_message("Your vehicle issue has been logged.", ephemeral=True)


class GenericRequestModal(ui.Modal):
    def __init__(self, title: str, request_type: str):
        super().__init__(title=title)
        self.request_type = request_type
        self.what_needed = ui.TextInput(label="What do you need?", style=discord.TextStyle.paragraph, required=True)
        self.needed_by = ui.TextInput(label="Needed by (optional)", required=False)
        self.add_item(self.what_needed)
        self.add_item(self.needed_by)

    async def on_submit(self, interaction: discord.Interaction):
        employee_key = get_employee_by_log_channel(interaction.channel_id)
        if not employee_key:
            await interaction.response.send_message("This channel is not linked to an employee log.", ephemeral=True)
            return

        fields = {
            "Request": self.what_needed.value,
            "Needed by": self.needed_by.value,
            "Submitted by": interaction.user.mention,
        }
        await log_event(bot, employee_key, self.request_type, f"{self.request_type.replace('_', ' ').title()} Logged", fields, "requests")
        await interaction.response.send_message("Your request has been logged.", ephemeral=True)


class IncidentModal(ui.Modal):
    def __init__(self, title: str, incident_type: str):
        super().__init__(title=title)
        self.incident_type = incident_type
        self.when_where = ui.TextInput(label="When & where?", required=True)
        self.what_happened = ui.TextInput(label="What happened?", style=discord.TextStyle.paragraph, required=True)
        self.injuries = ui.TextInput(label="Injuries/damage?", style=discord.TextStyle.paragraph, required=False)
        self.add_item(self.when_where)
        self.add_item(self.what_happened)
        self.add_item(self.injuries)

    async def on_submit(self, interaction: discord.Interaction):
        employee_key = get_employee_by_log_channel(interaction.channel_id)
        if not employee_key:
            await interaction.response.send_message("This channel is not linked to an employee log.", ephemeral=True)
            return

        fields = {
            "When & where": self.when_where.value,
            "What happened": self.what_happened.value,
            "Injuries/damage": self.injuries.value,
            "Submitted by": interaction.user.mention,
        }
        await log_event(bot, employee_key, self.incident_type, f"{self.incident_type.replace('_', ' ').title()} Logged", fields, "wpi_reports")
        await interaction.response.send_message("Your report has been logged.", ephemeral=True)


class CampfireEscalationModal(ui.Modal, title="Escalate to Campfire"):
    subject = ui.TextInput(label="Subject", required=True)
    description = ui.TextInput(label="Description / Why escalate", style=discord.TextStyle.paragraph, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        employee_key = get_employee_by_log_channel(interaction.channel_id)
        if not employee_key:
            await interaction.response.send_message("This channel is not linked to an employee log.", ephemeral=True)
            return

        employee_info = CONFIG.get("employees", {}).get(employee_key, {})
        campfire_channel_id = employee_info.get("campfire_channel_id")
        log_channel_id = employee_info.get("log_channel_id")

        fields = {
            "Subject": self.subject.value,
            "Description": self.description.value,
            "Submitted by": interaction.user.mention,
        }

        if campfire_channel_id:
            campfire_channel = bot.get_channel(int(campfire_channel_id))
            if campfire_channel:
                summary = (
                    f"🔥 Campfire Escalation for {employee_key.title()}\n"
                    f"Subject: {self.subject.value}\n"
                    f"Description: {self.description.value}\n"
                )
                links = []
                if log_channel_id:
                    links.append(f"Employee Log: <#{log_channel_id}>")
                global_log_id = CONFIG.get("global_logs", {}).get("requests")
                if global_log_id:
                    links.append(f"Global Log: <#{global_log_id}>")
                if links:
                    summary += "\n" + " | ".join(links)
                await campfire_channel.send(summary)

        await log_event(bot, employee_key, "campfire", "Campfire Escalation", fields, "requests")
        await interaction.response.send_message("Escalation sent to Campfire.", ephemeral=True)


class RequestsSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Print Materials"),
            discord.SelectOption(label="Safety Gear"),
            discord.SelectOption(label="Vehicle Issue"),
            discord.SelectOption(label="Route Change Request"),
            discord.SelectOption(label="Extra Pest Route"),
            discord.SelectOption(label="Extra Insulation Route"),
            discord.SelectOption(label="Meeting Request"),
            discord.SelectOption(label="Special Inventory"),
            discord.SelectOption(label="Other Request"),
        ]
        super().__init__(
            placeholder="Requests",
            options=options,
            min_values=1,
            max_values=1,
            custom_id="request_panel_requests_select",
        )

    async def callback(self, interaction: discord.Interaction):
        selection = self.values[0]
        if selection == "Vehicle Issue":
            await interaction.response.send_modal(VehicleIssueModal())
            return

        modal_title = f"{selection} Request"
        request_type = selection.lower().replace(" ", "_")
        await interaction.response.send_modal(GenericRequestModal(modal_title, request_type))


class ReportsSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="WPI — Injured"),
            discord.SelectOption(label="WPI — Witness"),
            discord.SelectOption(label="Damage Report"),
            discord.SelectOption(label="Car Accident"),
            discord.SelectOption(label="Spill / Chemical Incident"),
            discord.SelectOption(label="Customer Evidence"),
            discord.SelectOption(label="Vehicle Swap"),
            discord.SelectOption(label="Hours Correction Needed"),
        ]
        super().__init__(
            placeholder="Reports",
            options=options,
            min_values=1,
            max_values=1,
            custom_id="request_panel_reports_select",
        )

    async def callback(self, interaction: discord.Interaction):
        selection = self.values[0]
        if selection == "Hours Correction Needed":
            await interaction.response.send_modal(HoursUpdateModal())
            return

        incident_type = selection.lower().replace(" ", "_")
        await interaction.response.send_modal(IncidentModal(selection, incident_type))


class RequestPanelView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RequestsSelect())
        self.add_item(ReportsSelect())

    @ui.button(
        label="Call-Out",
        emoji="😷",
        style=discord.ButtonStyle.primary,
        row=0,
        custom_id="request_panel_call_out",
    )
    async def call_out(
        self, interaction: discord.Interaction, button: ui.Button
    ):
        await interaction.response.send_modal(CallOutModal())

    @ui.button(
        label="Hours Update",
        emoji="⏱",
        style=discord.ButtonStyle.primary,
        row=0,
        custom_id="request_panel_hours_update",
    )
    async def hours_update(
        self, interaction: discord.Interaction, button: ui.Button
    ):
        await interaction.response.send_modal(HoursUpdateModal())

    @ui.button(
        label="Tech Collections",
        emoji="💰",
        style=discord.ButtonStyle.primary,
        row=0,
        custom_id="request_panel_tech_collections",
    )
    async def tech_collections(
        self, interaction: discord.Interaction, button: ui.Button
    ):
        await interaction.response.send_modal(TechCollectionsModal())

    @ui.button(
        label="Reimbursement",
        emoji="🫰",
        style=discord.ButtonStyle.primary,
        row=1,
        custom_id="request_panel_reimbursement",
    )
    async def reimbursement(
        self, interaction: discord.Interaction, button: ui.Button
    ):
        await interaction.response.send_modal(PanelReimbursementModal())

    @ui.button(
        label="Uniform Request",
        emoji="👕",
        style=discord.ButtonStyle.secondary,
        row=1,
        custom_id="request_panel_uniform",
    )
    async def uniform_request(
        self, interaction: discord.Interaction, button: ui.Button
    ):
        await interaction.response.send_modal(PanelUniformModal())

    @ui.button(
        label="ID Card Request",
        emoji="🪪",
        style=discord.ButtonStyle.secondary,
        row=1,
        custom_id="request_panel_id_card",
    )
    async def id_card(
        self, interaction: discord.Interaction, button: ui.Button
    ):
        await interaction.response.send_modal(PanelIDCardModal())

    @ui.button(
        label="Company Card Request",
        emoji="💳",
        style=discord.ButtonStyle.secondary,
        row=2,
        custom_id="request_panel_company_card",
    )
    async def company_card(
        self, interaction: discord.Interaction, button: ui.Button
    ):
        await interaction.response.send_modal(PanelCompanyCardModal())

    @ui.button(
        label="Escalate to Campfire",
        emoji="🔥",
        style=discord.ButtonStyle.danger,
        row=2,
        custom_id="request_panel_escalate_campfire",
    )
    async def escalate(
        self, interaction: discord.Interaction, button: ui.Button
    ):
        await interaction.response.send_modal(CampfireEscalationModal())


class RequestButtonsView(ui.View):
    def __init__(self):
        # timeout=None keeps the buttons working after restart
        super().__init__(timeout=None)

    @ui.button(
        label="Uniform",
        emoji="👕",
        style=discord.ButtonStyle.primary,
        row=0
    )
    async def uniform_button(
        self,
        interaction: discord.Interaction,
        button: ui.Button
    ):
        await interaction.response.send_modal(UniformModal())

    @ui.button(
        label="Vehicle",
        emoji="🚗",
        style=discord.ButtonStyle.primary,
        row=0
    )
    async def vehicle_button(
        self,
        interaction: discord.Interaction,
        button: ui.Button
    ):
        await interaction.response.send_modal(VehicleModal())

    @ui.button(
        label="Print",
        emoji="🖨️",
        style=discord.ButtonStyle.primary,
        row=0
    )
    async def print_button(
        self,
        interaction: discord.Interaction,
        button: ui.Button
    ):
        await interaction.response.send_modal(PrintModal())

    @ui.button(
        label="ID Card",
        emoji="🪪",
        style=discord.ButtonStyle.secondary,
        row=1
    )
    async def idcard_button(
        self,
        interaction: discord.Interaction,
        button: ui.Button
    ):
        await interaction.response.send_modal(IDCardModal())

    @ui.button(
        label="Reimburse",
        emoji="💰",
        style=discord.ButtonStyle.secondary,
        row=1
    )
    async def reimburse_button(
        self,
        interaction: discord.Interaction,
        button: ui.Button
    ):
        await interaction.response.send_modal(ReimbursementModal())

    @ui.button(
        label="Meeting",
        emoji="📅",
        style=discord.ButtonStyle.secondary,
        row=1
    )
    async def meeting_button(
        self,
        interaction: discord.Interaction,
        button: ui.Button
    ):
        await interaction.response.send_modal(MeetingModal())

    @ui.button(
        label="Safety Gear",
        emoji="🦺",
        style=discord.ButtonStyle.success,
        row=2
    )
    async def safety_button(
        self,
        interaction: discord.Interaction,
        button: ui.Button
    ):
        await interaction.response.send_modal(SafetyGearModal())

    @ui.button(
        label="Other",
        emoji="📦",
        style=discord.ButtonStyle.success,
        row=2
    )
    async def other_button(
        self,
        interaction: discord.Interaction,
        button: ui.Button
    ):
        await interaction.response.send_modal(OtherRequestModal())


# Database initialization
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (task_number INTEGER PRIMARY KEY,
                  title TEXT NOT NULL,
                  description TEXT,
                  created_by TEXT,
                  created_by_id INTEGER,
                  assigned_to TEXT,
                  assigned_to_id INTEGER,
                  task_type TEXT,
                  status TEXT DEFAULT 'pending',
                  priority TEXT DEFAULT 'medium',
                  due_date TEXT,
                  category TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  completed_at TIMESTAMP,
                  pool_role TEXT,
                  claimed_by TEXT,
                  claimed_by_id INTEGER,
                  claimed_at TIMESTAMP,
                  reference_message_link TEXT,
                  reference_message_id INTEGER,
                  channel_id INTEGER,
                  bot_message_id INTEGER,
                  is_campfire BOOLEAN DEFAULT 0)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS pool_channels
                 (role_name TEXT PRIMARY KEY,
                  channel_id INTEGER NOT NULL,
                  role_id INTEGER NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS callouts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  person_name TEXT NOT NULL,
                  person_id INTEGER,
                  callout_date TEXT NOT NULL,
                  reason TEXT,
                  logged_by TEXT,
                  logged_by_id INTEGER,
                  logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    c.execute('''CREATE TABLE IF NOT EXISTS mentions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_name TEXT NOT NULL,
                  user_id INTEGER NOT NULL,
                  message_content TEXT,
                  message_link TEXT,
                  message_id INTEGER,
                  channel_id INTEGER,
                  channel_name TEXT,
                  author_name TEXT,
                  author_id INTEGER,
                  mention_type TEXT,
                  is_read BOOLEAN DEFAULT 0,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    c.execute('''CREATE TABLE IF NOT EXISTS task_updates
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task_number INTEGER NOT NULL,
                  update_text TEXT NOT NULL,
                  updated_by TEXT,
                  updated_by_id INTEGER,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (task_number) REFERENCES tasks(task_number))''')

    c.execute('''CREATE TABLE IF NOT EXISTS trainings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  date TEXT NOT NULL,
                  presenter TEXT,
                  presenter_id INTEGER,
                  notes TEXT,
                  attachments TEXT,
                  category TEXT,
                  created_by TEXT,
                  created_by_id INTEGER,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    c.execute('''CREATE TABLE IF NOT EXISTS training_attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  training_id INTEGER NOT NULL,
                  attendee_name TEXT NOT NULL,
                  attendee_id INTEGER NOT NULL,
                  signed_in_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (training_id) REFERENCES trainings(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS important_messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  message_id INTEGER UNIQUE NOT NULL,
                  channel_id INTEGER NOT NULL,
                  channel_name TEXT,
                  author_name TEXT,
                  author_id INTEGER,
                  content_preview TEXT,
                  posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  required_users TEXT,
                  auto_track BOOLEAN DEFAULT 1)''')

    c.execute('''CREATE TABLE IF NOT EXISTS message_reactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  message_id INTEGER NOT NULL,
                  user_name TEXT NOT NULL,
                  user_id INTEGER NOT NULL,
                  reacted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  reminder_count INTEGER DEFAULT 0,
                  manager_notified BOOLEAN DEFAULT 0,
                  FOREIGN KEY (message_id) REFERENCES important_messages(message_id))''')

    # Add completed_by column if it doesn't exist
    try:
        c.execute('ALTER TABLE tasks ADD COLUMN completed_by TEXT')
        print("✅ Added completed_by column to tasks table")
    except sqlite3.OperationalError:
        pass  # Column already exists

    conn.commit()
    conn.close()

def get_next_task_number():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT MAX(task_number) FROM tasks')
    result = c.fetchone()[0]
    conn.close()
    return (result or 0) + 1

def add_task(title: str, description: str = None, created_by: str = None,
             created_by_id: int = None, task_type: str = 'request',
             assigned_to: str = None, assigned_to_id: int = None,
             priority: str = 'medium', due_date: str = None,
             category: str = None, pool_role: str = None,
             reference_message_link: str = None, reference_message_id: int = None,
             channel_id: int = None, bot_message_id: int = None, is_campfire: bool = False):

    task_number = get_next_task_number()
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute('''INSERT INTO tasks
                 (task_number, title, description, created_by, created_by_id,
                  assigned_to, assigned_to_id, task_type, priority, due_date,
                  category, pool_role, reference_message_link, reference_message_id, channel_id,
                  bot_message_id, is_campfire)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (task_number, title, description, created_by, created_by_id,
               assigned_to, assigned_to_id, task_type, priority, due_date,
               category, pool_role, reference_message_link, reference_message_id, channel_id,
               bot_message_id, is_campfire))

    conn.commit()
    conn.close()
    return task_number

def get_task(task_number: int):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE task_number = ?', (task_number,))
    columns = [description[0] for description in c.description]
    row = c.fetchone()
    conn.close()
    
    if row:
        return dict(zip(columns, row))
    return None

def update_task_status(task_number: int, status: str, completed_by: str = None):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    if status == 'completed':
        c.execute('''UPDATE tasks
                     SET status = ?, completed_at = CURRENT_TIMESTAMP, completed_by = ?
                     WHERE task_number = ?''',
                  (status, completed_by, task_number))
    else:
        c.execute('UPDATE tasks SET status = ? WHERE task_number = ?',
                  (status, task_number))

    conn.commit()
    conn.close()

def update_bot_message_id(task_number: int, bot_message_id: int):
    """Update the bot message ID for a task"""
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET bot_message_id = ? WHERE task_number = ?',
              (bot_message_id, task_number))
    conn.commit()
    conn.close()

def claim_pool_task(task_number: int, claimed_by: str, claimed_by_id: int):
    """Claim a task (pool, request, or assigned) and set the claimer as assignee"""
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''UPDATE tasks
                 SET claimed_by = ?, claimed_by_id = ?, claimed_at = CURRENT_TIMESTAMP,
                     status = 'in_progress', assigned_to = ?, assigned_to_id = ?
                 WHERE task_number = ? AND status IN ('pending', 'active')''',
              (claimed_by, claimed_by_id, claimed_by, claimed_by_id, task_number))

    rows_affected = c.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def unclaim_pool_task(task_number: int):
    """Unclaim a pool task and return it to pending status"""
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''UPDATE tasks 
                 SET claimed_by = NULL, claimed_by_id = NULL, claimed_at = NULL, status = 'pending'
                 WHERE task_number = ? AND task_type = 'pool' AND status = 'in_progress' ''',
              (task_number,))
    
    rows_affected = c.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def get_task_by_message_id(message_id: int):
    """Check if a message already has a task created from it"""
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT task_number FROM tasks WHERE reference_message_id = ?', (message_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def delete_task_by_message_id(message_id: int):
    """Delete tasks associated with a deleted message"""
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE reference_message_id = ?', (message_id,))
    rows_affected = c.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def get_pool_channel(role_name: str):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT channel_id, role_id FROM pool_channels WHERE role_name = ?', (role_name,))
    result = c.fetchone()
    conn.close()
    return result

def register_pool_channel(role_name: str, channel_id: int, role_id: int):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO pool_channels (role_name, channel_id, role_id)
                 VALUES (?, ?, ?)''', (role_name, channel_id, role_id))
    conn.commit()
    conn.close()

def parse_task_metadata(content: str):
    """Extract priority, due date, and category from task content"""
    metadata = {
        'priority': 'medium',
        'due_date': None,
        'category': None
    }
    
    # Extract priority
    priority_match = re.search(r'\[priority:(low|medium|high)\]', content, re.IGNORECASE)
    if priority_match:
        metadata['priority'] = priority_match.group(1).lower()
        content = content.replace(priority_match.group(0), '').strip()
    
    # Extract due date
    due_match = re.search(r'\[due:(\d{4}-\d{2}-\d{2}|\w+\d+)\]', content, re.IGNORECASE)
    if due_match:
        metadata['due_date'] = due_match.group(1)
        content = content.replace(due_match.group(0), '').strip()
    
    # Extract category
    category_match = re.search(r'\[category:([^\]]+)\]', content, re.IGNORECASE)
    if category_match:
        metadata['category'] = category_match.group(1)
        content = content.replace(category_match.group(0), '').strip()
    
    return content.strip(), metadata

@tasks.loop(minutes=30)
async def check_important_message_reminders():
    """Check for users who haven't reacted to important messages and send reminders"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        # Get important messages from last 2 days
        c.execute('''SELECT message_id, channel_id, content_preview, author_name
                     FROM important_messages
                     WHERE posted_at >= datetime('now', '-2 days')''')
        important_messages = c.fetchall()

        for msg_id, channel_id, content_preview, author_name in important_messages:
            # Get the message age in hours
            c.execute('SELECT (julianday("now") - julianday(posted_at)) * 24 as hours_ago FROM important_messages WHERE message_id = ?', (msg_id,))
            hours_ago = c.fetchone()[0]

            # Get all guild members (excluding bots)
            guild = bot.guilds[0] if bot.guilds else None
            if not guild:
                continue

            all_members = [m for m in guild.members if not m.bot]

            # Get who has already reacted
            c.execute('SELECT user_id FROM message_reactions WHERE message_id = ?', (msg_id,))
            reacted_user_ids = {row[0] for row in c.fetchall()}

            # Find who hasn't reacted
            not_reacted = [m for m in all_members if m.id not in reacted_user_ids]

            for member in not_reacted:
                # Get reminder count for this user and message
                c.execute('''SELECT id, reminder_count, manager_notified FROM message_reactions
                             WHERE message_id = ? AND user_id = ?''', (msg_id, member.id))
                reaction_record = c.fetchone()

                if not reaction_record:
                    # Create record if doesn't exist
                    c.execute('''INSERT INTO message_reactions (message_id, user_name, user_id, reminder_count, manager_notified)
                                 VALUES (?, ?, ?, 0, 0)''', (msg_id, member.display_name, member.id))
                    conn.commit()
                    reminder_count = 0
                    manager_notified = False
                else:
                    _, reminder_count, manager_notified = reaction_record

                # Send reminder at 5 hours (4pm same day) and 17 hours (9am next day)
                should_send_first = 4.5 <= hours_ago < 5.5 and reminder_count == 0
                should_send_second = 16.5 <= hours_ago < 17.5 and reminder_count == 1

                if should_send_first or should_send_second:
                    try:
                        await member.send(
                            f"⚠️ **Important Message Reminder**\n\n"
                            f"You haven't acknowledged this important message from {author_name}:\n"
                            f"```{content_preview[:200]}...```\n"
                            f"Please react with 👁️ to acknowledge you've read it."
                        )

                        # Update reminder count
                        c.execute('''UPDATE message_reactions SET reminder_count = reminder_count + 1
                                     WHERE message_id = ? AND user_id = ?''', (msg_id, member.id))
                        conn.commit()
                        print(f"📨 Sent reminder #{reminder_count + 1} to {member.display_name} for message {msg_id}")
                    except discord.Forbidden:
                        print(f"❌ Couldn't DM {member.display_name} - DMs disabled")
                    except Exception as e:
                        print(f"Error sending reminder to {member.display_name}: {e}")

                # Notify managers after 2 failed reminders (after 9am next day reminder)
                if hours_ago >= 17.5 and reminder_count >= 2 and not manager_notified:
                    # Find RoundTable channel
                    roundtable_channel = discord.utils.get(guild.text_channels, name='roundtable')
                    if roundtable_channel:
                        try:
                            await roundtable_channel.send(
                                f"⚠️ **Unacknowledged Important Message**\n\n"
                                f"{member.mention} has not acknowledged an important message from {author_name} "
                                f"despite 2 reminders.\n"
                                f"Message preview: ```{content_preview[:200]}...```"
                            )

                            # Mark manager as notified
                            c.execute('''UPDATE message_reactions SET manager_notified = 1
                                         WHERE message_id = ? AND user_id = ?''', (msg_id, member.id))
                            conn.commit()
                            print(f"📢 Notified managers about {member.display_name} not acknowledging message {msg_id}")
                        except Exception as e:
                            print(f"Error notifying managers: {e}")

        conn.close()
    except Exception as e:
        print(f"Error in check_important_message_reminders: {e}")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    init_db()

    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    print(f'Flask API started on port {PORT}')

    # Start background task for important message reminders
    if not check_important_message_reminders.is_running():
        check_important_message_reminders.start()
        print('✅ Important message reminder task started')

    # Persistent views
    bot.add_view(RequestPanelView())

    try:
        await bot.tree.sync()
        print("✅ Slash commands synced.")
    except Exception as e:
        print(f"❌ Error syncing slash commands: {e}")


def build_request_panel_embed() -> discord.Embed:
    return discord.Embed(
        title="Request & Reports",
        description=(
            "Use the buttons and dropdowns below to submit requests, reports, or escalations. "
            "Entries will be logged to leadership channels automatically."
        ),
        color=discord.Color.blurple(),
    )


@bot.command(name="setup_panel")
@commands.has_permissions(administrator=True)
async def setup_panel(ctx: commands.Context, employee_key: Optional[str] = None):
    """Post and pin the request panel in an employee log channel."""

    target_employee_key = None
    target_channel = None

    if employee_key:
        candidate_key = employee_key.lower()
        employee_info = CONFIG.get("employees", {}).get(candidate_key)
        log_channel_id = employee_info.get("log_channel_id") if employee_info else None
        if not employee_info or not log_channel_id:
            await ctx.send(
                "Unknown employee key or missing log channel in config. "
                "Double-check CONFIG['employees'].")
            return

        channel_obj = bot.get_channel(int(log_channel_id))
        if not channel_obj:
            await ctx.send("I couldn't find that employee log channel. Is the ID correct?")
            return

        target_employee_key = candidate_key
        target_channel = channel_obj
    else:
        target_employee_key = get_employee_by_log_channel(ctx.channel.id)
        target_channel = ctx.channel if target_employee_key else None

    if not target_employee_key or not target_channel:
        await ctx.send(
            "Provide an employee key or run this in a mapped log channel.\n"
            "Usage: `@setup_panel <employee_key>`"
        )
        return

    message = await target_channel.send(embed=build_request_panel_embed(), view=RequestPanelView())
    try:
        await message.pin()
    except discord.Forbidden:
        await ctx.send("Panel posted but I could not pin it. Please pin manually.")
    else:
        await ctx.send(
            f"Panel posted and pinned in {target_channel.mention} for {target_employee_key.title()}.",
            delete_after=10,
        )

@bot.event
async def on_message(message):
    # Ignore the bot's own messages
    if message.author == bot.user:
        return

    # Handle @requestpanel command (admin only)
    if message.content.strip().lower().startswith('@requestpanel'):
        # Check if user is an admin
        if not message.author.guild_permissions.administrator:
            await message.channel.send("❌ You need administrator permissions to use this command.")
            return

        await message.channel.send(embed=build_request_panel_embed(), view=RequestPanelView())

        # Try to delete the command message to keep the channel clean
        try:
            await message.delete()
        except discord.Forbidden:
            pass

        return

    # 🔹 Handle @exportstructure command (owner/admin only)
    if message.content.strip().lower().startswith('@exportstructure'):
        # You can tighten this to owners only if you want
        if not message.author.guild_permissions.administrator:
            await message.channel.send("❌ You need administrator permissions to use this command.")
            return

        guild = message.guild
        if guild is None:
            await message.channel.send("This command must be run in a server, not in DMs.")
            return

        lines = []
        lines.append(f"Server: {guild.name} (id: {guild.id})")
        lines.append("")

        # Categories with their channels + threads
        for category in guild.categories:
            lines.append(f"📁 {category.name} (id: {category.id})")
            for channel in category.text_channels:
                lines.append(f"  # {channel.name} (id: {channel.id})")
                # Active threads in this channel
                for thread in channel.threads:
                    lines.append(f"    🧵 {thread.name} (id: {thread.id})")
            lines.append("")

        # Channels without a category
        no_cat_channels = [ch for ch in guild.text_channels if ch.category is None]
        if no_cat_channels:
            lines.append("📁 (No Category)")
            for channel in no_cat_channels:
                lines.append(f"  # {channel.name} (id: {channel.id})")
                for thread in channel.threads:
                    lines.append(f"    🧵 {thread.name} (id: {thread.id})")
            lines.append("")

        full_report = "\n".join(lines)

        # DM it to the person who ran the command, chunked so we don't hit the 2000-char limit
        chunks = []
        remaining = full_report
        while remaining:
            chunk = remaining[:1900]
            last_nl = chunk.rfind("\n")
            if last_nl != -1:
                chunk, remaining = remaining[:last_nl], remaining[last_nl+1:]
            else:
                remaining = remaining[1900:]
            chunks.append(chunk)

        for chunk in chunks:
            await message.author.send(f"```{chunk}```")

        await message.channel.send("✅ I’ve DM’d you the server structure.")
        return
    
    # Handle @hey command
    if message.content.startswith('@hey '):
        task_content = message.content[len('@hey '):].strip()
        rt_employee = get_employee_by_rt_channel(message.channel.id)

        if rt_employee:
            event_type = detect_hey_event(task_content)
            await message.channel.send(f"Hey there, {message.author.mention}! I’m on it.")

            if event_type:
                fields = {
                    "Summary": task_content,
                    "Submitted by": message.author.mention,
                }
                global_log_key = "call_outs" if event_type == "call_out" else "vehicle_issues"
                title = "Call-Out Logged" if event_type == "call_out" else "Vehicle Issue Logged"
                await log_event(bot, rt_employee, event_type, title, fields, global_log_key)

                global_channel_id = CONFIG.get("global_logs", {}).get(global_log_key)
                receipt_target = f"<#{global_channel_id}>" if global_channel_id else "the log channel"
                await message.channel.send(f"(Bot) Logged this as {title} in {receipt_target}.")
            return

        # Fallback to legacy behavior for non-RT channels
        cleaned_content, metadata = parse_task_metadata(task_content)

        task_number = add_task(
            title=cleaned_content,
            created_by=message.author.display_name,
            created_by_id=message.author.id,
            task_type='request',
            priority=metadata['priority'],
            due_date=metadata['due_date'],
            category=metadata['category'],
            reference_message_link=message.jump_url,
            reference_message_id=message.id,
            channel_id=message.channel.id
        )

        embed = discord.Embed(
            title=f"✅ Task Request #{task_number} Created",
            description=cleaned_content,
            color=discord.Color.blue()
        )
        embed.add_field(name="Requested by", value=message.author.mention, inline=True)
        embed.add_field(name="Priority", value=metadata['priority'].upper(), inline=True)
        if metadata['due_date']:
            embed.add_field(name="Due Date", value=metadata['due_date'], inline=True)
        if metadata['category']:
            embed.add_field(name="Category", value=metadata['category'], inline=True)
        embed.add_field(name="Status", value="⏳ Pending", inline=True)

        bot_msg = await message.channel.send(embed=embed)
        update_bot_message_id(task_number, bot_msg.id)
        await message.add_reaction('✅')
        return
    
    # Handle @assign command
    if message.content.startswith('@assign '):
        if not message.mentions:
            await message.channel.send("❌ Please mention a user to assign the task to!")
            return

        assigned_user = message.mentions[0]
        task_content = message.content.split(assigned_user.mention, 1)[1].strip()
        cleaned_content, metadata = parse_task_metadata(task_content)

        task_number = add_task(
            title=cleaned_content,
            created_by=message.author.display_name,
            created_by_id=message.author.id,
            assigned_to=assigned_user.display_name,
            assigned_to_id=assigned_user.id,
            task_type='assigned',
            priority=metadata['priority'],
            due_date=metadata['due_date'],
            category=metadata['category'],
            reference_message_link=message.jump_url,
            reference_message_id=message.id,
            channel_id=message.channel.id
        )

        embed = discord.Embed(
            title=f"📋 Task #{task_number} Assigned",
            description=cleaned_content,
            color=discord.Color.green()
        )
        embed.add_field(name="Assigned by", value=message.author.mention, inline=True)
        embed.add_field(name="Assigned to", value=assigned_user.mention, inline=True)
        embed.add_field(name="Priority", value=metadata['priority'].upper(), inline=True)
        if metadata['due_date']:
            embed.add_field(name="Due Date", value=metadata['due_date'], inline=True)
        if metadata['category']:
            embed.add_field(name="Category", value=metadata['category'], inline=True)
        embed.add_field(name="Status", value="⏳ Pending", inline=True)

        bot_msg = await message.channel.send(embed=embed)
        update_bot_message_id(task_number, bot_msg.id)
        await message.add_reaction('✅')
        return
    
    # Handle @pool command
    if message.content.startswith('@pool '):
        parts = message.content.split()
        
        # Check for status subcommands
        if len(parts) >= 2 and parts[1] in ['status', 'available', 'my']:
            subcommand = parts[1]
            
            if subcommand == 'status':
                # Show overall pool status
                conn = sqlite3.connect('tasks.db')
                c = conn.cursor()
                c.execute('''SELECT pool_role, status, COUNT(*) as count
                            FROM tasks 
                            WHERE task_type = 'pool'
                            GROUP BY pool_role, status''')
                results = c.fetchall()
                conn.close()
                
                embed = discord.Embed(
                    title="📊 Pool Task Status",
                    color=discord.Color.purple()
                )
                
                pool_stats = {}
                for role, status, count in results:
                    if role not in pool_stats:
                        pool_stats[role] = {}
                    pool_stats[role][status] = count
                
                for role, stats in pool_stats.items():
                    status_text = "\n".join([f"{status.capitalize()}: {count}" for status, count in stats.items()])
                    embed.add_field(name=f"@{role}", value=status_text, inline=True)
                
                await message.channel.send(embed=embed)
                return
            
            elif subcommand == 'available':
                # Show unclaimed tasks
                conn = sqlite3.connect('tasks.db')
                c = conn.cursor()
                c.execute('''SELECT task_number, title, pool_role, priority, due_date
                            FROM tasks 
                            WHERE task_type = 'pool' AND status = 'pending'
                            ORDER BY priority DESC, due_date ASC''')
                results = c.fetchall()
                conn.close()
                
                if not results:
                    await message.channel.send("✨ No available pool tasks!")
                    return
                
                embed = discord.Embed(
                    title="🎯 Available Pool Tasks",
                    description="React with ✋ to claim a task",
                    color=discord.Color.gold()
                )
                
                for task_number, title, role, priority, due_date in results:
                    field_value = f"**Priority:** {priority.upper()}\n**Role:** @{role}"
                    if due_date:
                        field_value += f"\n**Due:** {due_date}"
                    embed.add_field(name=f"Task #{task_number}: {title}", value=field_value, inline=False)
                
                await message.channel.send(embed=embed)
                return
            
            elif subcommand == 'my':
                # Show user's claimed tasks
                conn = sqlite3.connect('tasks.db')
                c = conn.cursor()
                c.execute('''SELECT task_number, title, status, priority, due_date
                            FROM tasks 
                            WHERE task_type = 'pool' AND claimed_by_id = ?
                            ORDER BY status, due_date ASC''',
                          (message.author.id,))
                results = c.fetchall()
                conn.close()
                
                if not results:
                    await message.channel.send("You haven't claimed any pool tasks yet!")
                    return
                
                embed = discord.Embed(
                    title=f"📝 {message.author.display_name}'s Pool Tasks",
                    color=discord.Color.blue()
                )
                
                for task_number, title, status, priority, due_date in results:
                    field_value = f"**Status:** {status}\n**Priority:** {priority.upper()}"
                    if due_date:
                        field_value += f"\n**Due:** {due_date}"
                    embed.add_field(name=f"Task #{task_number}: {title}", value=field_value, inline=False)
                
                await message.channel.send(embed=embed)
                return
        
        # Original @pool creation logic
        if not message.role_mentions:
            await message.channel.send("❌ Please mention a role to assign the pool task to!")
            return
        
        role = message.role_mentions[0]
        task_content = message.content.split(role.mention, 1)[1].strip()
        cleaned_content, metadata = parse_task_metadata(task_content)
        
        # Check if we have a pool channel for this role
        pool_info = get_pool_channel(role.name)
        
        if not pool_info:
            # Try to find or create a pool channel
            pool_channel_name = f"{role.name.lower()}-pool"
            pool_channel = discord.utils.get(message.guild.text_channels, name=pool_channel_name)
            
            if not pool_channel:
                await message.channel.send(f"❌ No pool channel found for role {role.mention}. Please create #{pool_channel_name} first!")
                return
            
            # Register the channel
            register_pool_channel(role.name, pool_channel.id, role.id)
            pool_info = (pool_channel.id, role.id)
        
        pool_channel_id, role_id = pool_info
        pool_channel = bot.get_channel(pool_channel_id)
        
        if not pool_channel:
            await message.channel.send(f"❌ Could not find pool channel for {role.mention}")
            return
        
        task_number = add_task(
            title=cleaned_content,
            created_by=message.author.display_name,
            created_by_id=message.author.id,
            task_type='pool',
            pool_role=role.name,
            priority=metadata['priority'],
            due_date=metadata['due_date'],
            category=metadata['category'],
            reference_message_link=message.jump_url,
            reference_message_id=message.id,
            channel_id=message.channel.id
        )
        
        # Post to pool channel
        embed = discord.Embed(
            title=f"🎯 New Pool Task #{task_number}",
            description=cleaned_content,
            color=discord.Color.purple()
        )
        embed.add_field(name="Posted by", value=message.author.mention, inline=True)
        embed.add_field(name="For Role", value=role.mention, inline=True)
        embed.add_field(name="Priority", value=metadata['priority'].upper(), inline=True)
        if metadata['due_date']:
            embed.add_field(name="Due Date", value=metadata['due_date'], inline=True)
        if metadata['category']:
            embed.add_field(name="Category", value=metadata['category'], inline=True)
        embed.set_footer(text="React with ✋ to claim this task")
        
        pool_message = await pool_channel.send(f"{role.mention}", embed=embed)
        await pool_message.add_reaction('✋')

        # Store the pool message ID and channel so we can edit it later
        update_bot_message_id(task_number, pool_message.id)
        # Update channel_id to the pool channel (not the original command channel)
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('UPDATE tasks SET channel_id = ? WHERE task_number = ?',
                  (pool_channel.id, task_number))
        conn.commit()
        conn.close()

        # Confirm in original channel
        await message.channel.send(f"✅ Pool task #{task_number} posted to {pool_channel.mention}")
        await message.add_reaction('✅')
        return
    
    # Handle @complete command
    if message.content.startswith('@complete '):
        try:
            task_number = int(message.content.split()[1])
            task = get_task(task_number)

            if not task:
                await message.channel.send(f"❌ Task #{task_number} not found!")
                return

            if task['status'] == 'completed':
                await message.channel.send(f"ℹ️ Task #{task_number} is already completed!")
                return

            update_task_status(task_number, 'completed', message.author.display_name)

            # Try to edit the original bot message if it exists
            if task.get('bot_message_id') and task.get('channel_id'):
                try:
                    channel = bot.get_channel(task['channel_id'])
                    if channel:
                        bot_message = await channel.fetch_message(task['bot_message_id'])
                        if bot_message and bot_message.embeds:
                            # Edit the existing embed
                            old_embed = bot_message.embeds[0]
                            # Handle different title formats
                            new_title = old_embed.title
                            if "Created" in new_title:
                                new_title = new_title.replace("Created", "✅ COMPLETED")
                            elif "Assigned" in new_title:
                                new_title = new_title.replace("Assigned", "✅ COMPLETED")
                            elif "Claimed" in new_title or "Pool Task" in new_title:
                                # For pool tasks, extract task number and create completion title
                                try:
                                    task_num = int(new_title.split('#')[1].split()[0])
                                    new_title = f"✅ Task #{task_num} Completed"
                                except:
                                    new_title = "✅ Task Completed"
                            else:
                                new_title = "✅ Task Completed"

                            new_embed = discord.Embed(
                                title=new_title,
                                description=old_embed.description,
                                color=discord.Color.green()
                            )

                            # Copy existing fields but update status
                            for field in old_embed.fields:
                                if field.name != "Status":
                                    new_embed.add_field(name=field.name, value=field.value, inline=field.inline)

                            new_embed.add_field(name="Status", value=f"✅ Completed by {message.author.mention}", inline=False)
                            new_embed.timestamp = datetime.now()

                            await bot_message.edit(embed=new_embed)
                            await message.add_reaction('✅')
                            return
                except Exception as e:
                    print(f"Could not edit original message: {e}")

            # Fallback: send new message if editing fails
            embed = discord.Embed(
                title=f"✅ Task #{task_number} Completed",
                description=task['title'],
                color=discord.Color.green()
            )
            embed.add_field(name="Completed by", value=message.author.mention, inline=True)

            await message.channel.send(embed=embed)
            await message.add_reaction('✅')

        except (ValueError, IndexError):
            await message.channel.send("❌ Please provide a valid task number: `@complete 47`")
        return

    # Handle @report command
    if message.content.startswith('@report'):
        parts = message.content.split()

        # Show help if no subcommand
        if len(parts) == 1:
            help_embed = discord.Embed(
                title="📊 Report Commands",
                description="Generate various task reports",
                color=discord.Color.blue()
            )
            help_embed.add_field(
                name="@report summary",
                value="Overall task statistics and breakdown by status/type",
                inline=False
            )
            help_embed.add_field(
                name="@report my",
                value="Your personal tasks (assigned to you or created by you)",
                inline=False
            )
            help_embed.add_field(
                name="@report assignee @user",
                value="Tasks for a specific user",
                inline=False
            )
            help_embed.add_field(
                name="@report overdue",
                value="Tasks past their due date",
                inline=False
            )
            help_embed.add_field(
                name="@report recent",
                value="Recently completed tasks (last 7 days)",
                inline=False
            )
            help_embed.add_field(
                name="@report pending",
                value="All pending (unassigned) tasks",
                inline=False
            )
            help_embed.add_field(
                name="@report callouts <start-date> <end-date>",
                value="Call outs within date range (format: MM/DD/YY or MM/DD/YYYY)",
                inline=False
            )
            await message.channel.send(embed=help_embed)
            return

        subcommand = parts[1]

        # Report: Summary
        if subcommand == 'summary':
            conn = sqlite3.connect('tasks.db')
            c = conn.cursor()

            # Overall counts
            c.execute("SELECT COUNT(*) FROM tasks WHERE status != 'deleted'")
            total_tasks = c.fetchone()[0]

            c.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending' AND status != 'deleted'")
            pending_count = c.fetchone()[0]

            c.execute("SELECT COUNT(*) FROM tasks WHERE status = 'in_progress' AND status != 'deleted'")
            in_progress_count = c.fetchone()[0]

            c.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
            completed_count = c.fetchone()[0]

            # By type
            c.execute('''SELECT task_type, COUNT(*) as count
                        FROM tasks
                        WHERE status != 'deleted' AND status != 'completed'
                        GROUP BY task_type''')
            type_counts = c.fetchall()

            # By priority
            c.execute('''SELECT priority, COUNT(*) as count
                        FROM tasks
                        WHERE status != 'deleted' AND status != 'completed'
                        GROUP BY priority''')
            priority_counts = c.fetchall()

            conn.close()

            embed = discord.Embed(
                title="📊 Task Summary Report",
                color=discord.Color.blue()
            )

            # Overall stats
            embed.add_field(
                name="📈 Overall Statistics",
                value=f"**Total Tasks:** {total_tasks}\n"
                      f"⏳ Pending: {pending_count}\n"
                      f"🔨 In Progress: {in_progress_count}\n"
                      f"✅ Completed: {completed_count}",
                inline=True
            )

            # Completion rate
            if total_tasks > 0:
                completion_rate = (completed_count / total_tasks) * 100
                embed.add_field(
                    name="📊 Completion Rate",
                    value=f"{completion_rate:.1f}%",
                    inline=True
                )

            # By type
            if type_counts:
                type_text = "\n".join([f"**{t_type or 'None'}:** {count}" for t_type, count in type_counts])
                embed.add_field(name="📋 Active by Type", value=type_text, inline=False)

            # By priority
            if priority_counts:
                priority_text = "\n".join([f"**{priority.upper()}:** {count}" for priority, count in priority_counts])
                embed.add_field(name="🎯 Active by Priority", value=priority_text, inline=False)

            embed.timestamp = datetime.now()
            await message.channel.send(embed=embed)
            return

        # Report: My tasks
        elif subcommand == 'my':
            conn = sqlite3.connect('tasks.db')
            c = conn.cursor()

            # Tasks assigned to user
            c.execute('''SELECT task_number, title, status, priority, due_date, task_type
                        FROM tasks
                        WHERE assigned_to_id = ? AND status != 'deleted'
                        ORDER BY
                            CASE status
                                WHEN 'pending' THEN 1
                                WHEN 'in_progress' THEN 2
                                WHEN 'completed' THEN 3
                            END,
                            CASE priority
                                WHEN 'high' THEN 1
                                WHEN 'medium' THEN 2
                                WHEN 'low' THEN 3
                            END''',
                      (message.author.id,))
            assigned_tasks = c.fetchall()

            # Tasks created by user
            c.execute('''SELECT task_number, title, status, priority, due_date, task_type
                        FROM tasks
                        WHERE created_by_id = ? AND assigned_to_id != ? AND status != 'deleted'
                        ORDER BY status, priority DESC''',
                      (message.author.id, message.author.id))
            created_tasks = c.fetchall()

            conn.close()

            embed = discord.Embed(
                title=f"📝 Tasks for {message.author.display_name}",
                color=discord.Color.blue()
            )

            # Assigned tasks
            if assigned_tasks:
                assigned_text = ""
                for task_number, title, status, priority, due_date, task_type in assigned_tasks[:10]:
                    status_emoji = {"pending": "⏳", "in_progress": "🔨", "completed": "✅"}.get(status, "❓")
                    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                    title_short = title[:40] + "..." if len(title) > 40 else title
                    assigned_text += f"{status_emoji} {priority_emoji} **#{task_number}** {title_short}\n"

                if len(assigned_tasks) > 10:
                    assigned_text += f"\n_...and {len(assigned_tasks) - 10} more_"

                embed.add_field(name=f"📥 Assigned to You ({len(assigned_tasks)})", value=assigned_text, inline=False)
            else:
                embed.add_field(name="📥 Assigned to You", value="No tasks assigned", inline=False)

            # Created tasks
            if created_tasks:
                created_text = ""
                for task_number, title, status, priority, due_date, task_type in created_tasks[:5]:
                    status_emoji = {"pending": "⏳", "in_progress": "🔨", "completed": "✅"}.get(status, "❓")
                    title_short = title[:40] + "..." if len(title) > 40 else title
                    created_text += f"{status_emoji} **#{task_number}** {title_short}\n"

                if len(created_tasks) > 5:
                    created_text += f"\n_...and {len(created_tasks) - 5} more_"

                embed.add_field(name=f"📤 Created by You ({len(created_tasks)})", value=created_text, inline=False)

            embed.timestamp = datetime.now()
            await message.channel.send(embed=embed)
            return

        # Report: Assignee
        elif subcommand == 'assignee':
            if not message.mentions:
                await message.channel.send("❌ Please mention a user: `@report assignee @username`")
                return

            target_user = message.mentions[0]

            conn = sqlite3.connect('tasks.db')
            c = conn.cursor()

            c.execute('''SELECT task_number, title, status, priority, due_date, task_type
                        FROM tasks
                        WHERE assigned_to_id = ? AND status != 'deleted'
                        ORDER BY
                            CASE status
                                WHEN 'pending' THEN 1
                                WHEN 'in_progress' THEN 2
                                WHEN 'completed' THEN 3
                            END,
                            CASE priority
                                WHEN 'high' THEN 1
                                WHEN 'medium' THEN 2
                                WHEN 'low' THEN 3
                            END''',
                      (target_user.id,))
            tasks = c.fetchall()
            conn.close()

            if not tasks:
                await message.channel.send(f"No tasks found for {target_user.mention}")
                return

            embed = discord.Embed(
                title=f"📝 Tasks for {target_user.display_name}",
                description=f"Total: {len(tasks)} tasks",
                color=discord.Color.blue()
            )

            tasks_text = ""
            for task_number, title, status, priority, due_date, task_type in tasks[:15]:
                status_emoji = {"pending": "⏳", "in_progress": "🔨", "completed": "✅"}.get(status, "❓")
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                title_short = title[:40] + "..." if len(title) > 40 else title
                tasks_text += f"{status_emoji} {priority_emoji} **#{task_number}** {title_short}\n"

            if len(tasks) > 15:
                tasks_text += f"\n_...and {len(tasks) - 15} more tasks_"

            embed.add_field(name="Tasks", value=tasks_text, inline=False)
            embed.timestamp = datetime.now()
            await message.channel.send(embed=embed)
            return

        # Report: Overdue
        elif subcommand == 'overdue':
            conn = sqlite3.connect('tasks.db')
            c = conn.cursor()

            today = datetime.now().date().isoformat()

            c.execute('''SELECT task_number, title, assigned_to, due_date, priority, task_type
                        FROM tasks
                        WHERE due_date IS NOT NULL
                        AND due_date < ?
                        AND status != 'completed'
                        AND status != 'deleted'
                        ORDER BY due_date ASC''',
                      (today,))
            overdue_tasks = c.fetchall()
            conn.close()

            if not overdue_tasks:
                await message.channel.send("✨ No overdue tasks!")
                return

            embed = discord.Embed(
                title="⚠️ Overdue Tasks",
                description=f"Found {len(overdue_tasks)} overdue tasks",
                color=discord.Color.red()
            )

            overdue_text = ""
            for task_number, title, assigned_to, due_date, priority, task_type in overdue_tasks[:15]:
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                title_short = title[:35] + "..." if len(title) > 35 else title
                assignee = assigned_to or "Unassigned"
                overdue_text += f"{priority_emoji} **#{task_number}** {title_short}\n   📅 Due: {due_date} | Assigned: {assignee}\n"

            if len(overdue_tasks) > 15:
                overdue_text += f"\n_...and {len(overdue_tasks) - 15} more overdue tasks_"

            embed.add_field(name="Overdue Tasks", value=overdue_text, inline=False)
            embed.timestamp = datetime.now()
            await message.channel.send(embed=embed)
            return

        # Report: Recent completions
        elif subcommand == 'recent':
            conn = sqlite3.connect('tasks.db')
            c = conn.cursor()

            seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()

            c.execute('''SELECT task_number, title, assigned_to, completed_at, priority
                        FROM tasks
                        WHERE status = 'completed'
                        AND completed_at >= ?
                        ORDER BY completed_at DESC''',
                      (seven_days_ago,))
            recent_tasks = c.fetchall()
            conn.close()

            if not recent_tasks:
                await message.channel.send("No tasks completed in the last 7 days.")
                return

            embed = discord.Embed(
                title="✅ Recently Completed Tasks",
                description=f"{len(recent_tasks)} tasks completed in the last 7 days",
                color=discord.Color.green()
            )

            recent_text = ""
            for task_number, title, assigned_to, completed_at, priority in recent_tasks[:15]:
                title_short = title[:40] + "..." if len(title) > 40 else title
                assignee = assigned_to or "Unknown"
                # Format completed_at date
                try:
                    completed_date = datetime.fromisoformat(completed_at).strftime("%b %d")
                except:
                    completed_date = "Recently"
                recent_text += f"✅ **#{task_number}** {title_short}\n   👤 {assignee} | 📅 {completed_date}\n"

            if len(recent_tasks) > 15:
                recent_text += f"\n_...and {len(recent_tasks) - 15} more_"

            embed.add_field(name="Completed Tasks", value=recent_text, inline=False)
            embed.timestamp = datetime.now()
            await message.channel.send(embed=embed)
            return

        # Report: Pending
        elif subcommand == 'pending':
            conn = sqlite3.connect('tasks.db')
            c = conn.cursor()

            c.execute('''SELECT task_number, title, created_by, priority, due_date, task_type
                        FROM tasks
                        WHERE status = 'pending'
                        AND (assigned_to IS NULL OR assigned_to = 'Unassigned')
                        AND status != 'deleted'
                        ORDER BY
                            CASE priority
                                WHEN 'high' THEN 1
                                WHEN 'medium' THEN 2
                                WHEN 'low' THEN 3
                            END,
                            created_at ASC''')
            pending_tasks = c.fetchall()
            conn.close()

            if not pending_tasks:
                await message.channel.send("✨ No pending tasks!")
                return

            embed = discord.Embed(
                title="⏳ Pending Tasks",
                description=f"{len(pending_tasks)} unassigned tasks waiting for action",
                color=discord.Color.gold()
            )

            pending_text = ""
            for task_number, title, created_by, priority, due_date, task_type in pending_tasks[:15]:
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                type_emoji = {"request": "📥", "pool": "🎯", "campfire": "🔥", "assigned": "📋"}.get(task_type, "📝")
                title_short = title[:35] + "..." if len(title) > 35 else title
                due_info = f"📅 {due_date}" if due_date else ""
                pending_text += f"{priority_emoji} {type_emoji} **#{task_number}** {title_short}\n   👤 {created_by} {due_info}\n"

            if len(pending_tasks) > 15:
                pending_text += f"\n_...and {len(pending_tasks) - 15} more pending tasks_"

            embed.add_field(name="Unassigned Tasks", value=pending_text, inline=False)
            embed.timestamp = datetime.now()
            await message.channel.send(embed=embed)
            return

        # Report: Call outs by date range
        elif subcommand == 'callouts':
            if len(parts) < 4:
                await message.channel.send("❌ Please provide date range: `@report callouts MM/DD/YY MM/DD/YY`")
                return

            start_date_str = parts[2]
            end_date_str = parts[3]

            # Parse dates (support MM/DD/YY or MM/DD/YYYY)
            try:
                # Try MM/DD/YYYY first
                try:
                    start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date()
                except ValueError:
                    # Try MM/DD/YY
                    start_date = datetime.strptime(start_date_str, '%m/%d/%y').date()

                try:
                    end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date()
                except ValueError:
                    end_date = datetime.strptime(end_date_str, '%m/%d/%y').date()

            except ValueError:
                await message.channel.send("❌ Invalid date format. Use MM/DD/YY or MM/DD/YYYY")
                return

            # Convert to ISO format for SQL query
            start_iso = start_date.isoformat()
            end_iso = end_date.isoformat()

            conn = sqlite3.connect('tasks.db')
            c = conn.cursor()

            c.execute('''SELECT person_name, callout_date, reason, logged_by, logged_at
                        FROM callouts
                        WHERE callout_date >= ? AND callout_date <= ?
                        ORDER BY callout_date ASC''',
                      (start_iso, end_iso))
            callouts = c.fetchall()
            conn.close()

            if not callouts:
                await message.channel.send(f"✨ No call outs found between {start_date_str} and {end_date_str}")
                return

            embed = discord.Embed(
                title=f"🏠 Call Out Report",
                description=f"{len(callouts)} call out(s) from {start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}",
                color=discord.Color.orange()
            )

            callouts_text = ""
            for person_name, callout_date, reason, logged_by, logged_at in callouts[:20]:
                # Format date
                try:
                    date_obj = datetime.fromisoformat(callout_date)
                    formatted_date = date_obj.strftime("%m/%d/%y")
                except:
                    formatted_date = callout_date

                reason_text = reason if reason else "No reason provided"
                callouts_text += f"📅 **{formatted_date}** - {person_name}\n   💬 {reason_text}\n"

            if len(callouts) > 20:
                callouts_text += f"\n_...and {len(callouts) - 20} more call outs_"

            embed.add_field(name="Call Outs", value=callouts_text, inline=False)
            embed.timestamp = datetime.now()
            await message.channel.send(embed=embed)
            return

        else:
            await message.channel.send(f"❌ Unknown report type: `{subcommand}`\nUse `@report` to see available options.")
            return

    # Handle @callout command
    if message.content.startswith('@callout '):
        # Parse: @callout Name MM/DD/YY Reason text here
        # or: @callout @User MM/DD/YY Reason text here
        content_parts = message.content[9:].strip()  # Remove '@callout '

        # Check if user is mentioned
        if message.mentions:
            person = message.mentions[0]
            person_name = person.display_name
            person_id = person.id
            # Remove mention from content
            content_parts = content_parts.replace(person.mention, '').strip()
        else:
            # Parse name from text
            parts = content_parts.split(maxsplit=2)
            if len(parts) < 2:
                await message.channel.send("❌ Usage: `@callout Name MM/DD/YY Reason` or `@callout @User MM/DD/YY Reason`")
                return
            person_name = parts[0]
            person_id = None
            content_parts = ' '.join(parts[1:])

        # Parse date and reason
        parts = content_parts.split(maxsplit=1)
        if len(parts) < 1:
            await message.channel.send("❌ Please provide a date: `@callout Name MM/DD/YY Reason`")
            return

        date_str = parts[0]
        reason = parts[1] if len(parts) > 1 else "No reason provided"

        # Parse date
        try:
            # Try MM/DD/YYYY first
            try:
                callout_date = datetime.strptime(date_str, '%m/%d/%Y').date()
            except ValueError:
                # Try MM/DD/YY
                callout_date = datetime.strptime(date_str, '%m/%d/%y').date()
        except ValueError:
            await message.channel.send(f"❌ Invalid date format: `{date_str}`. Use MM/DD/YY or MM/DD/YYYY")
            return

        # Save to database
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''INSERT INTO callouts (person_name, person_id, callout_date, reason, logged_by, logged_by_id)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (person_name, person_id, callout_date.isoformat(), reason,
                   message.author.display_name, message.author.id))
        conn.commit()
        conn.close()

        # Confirm
        embed = discord.Embed(
            title="🏠 Call Out Logged",
            description=f"**{person_name}** called out on **{callout_date.strftime('%m/%d/%y')}**",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Logged by", value=message.author.mention, inline=True)
        embed.timestamp = datetime.now()

        await message.channel.send(embed=embed)
        await message.add_reaction('✅')
        return

    # Handle @update command
    if message.content.startswith('@update '):
        parts = message.content[8:].strip().split(maxsplit=1)
        if len(parts) < 2:
            await message.channel.send("❌ Usage: `@update <task#> <update text>`")
            return

        try:
            task_number = int(parts[0].replace('#', ''))
            update_text = parts[1]
        except ValueError:
            await message.channel.send("❌ Invalid task number")
            return

        # Add update to database
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        # Check if task exists
        c.execute('SELECT * FROM tasks WHERE task_number = ?', (task_number,))
        task_row = c.fetchone()
        if not task_row:
            conn.close()
            await message.channel.send(f"❌ Task #{task_number} not found")
            return

        # Insert update
        c.execute('''INSERT INTO task_updates
                     (task_number, update_text, updated_by, updated_by_id)
                     VALUES (?, ?, ?, ?)''',
                  (task_number, update_text, message.author.display_name, message.author.id))
        conn.commit()

        # Get task details
        columns = [description[0] for description in c.description]
        task = dict(zip(columns, task_row))
        conn.close()

        # Update Discord message
        if task.get('bot_message_id') and task.get('channel_id'):
            await update_discord_message(task)

        await message.add_reaction('✅')
        await message.channel.send(f"📝 Update added to Task #{task_number}")
        return

    # Handle @training-create command
    if message.content.startswith('@training-create '):
        parts = message.content[17:].strip().split('|')
        if len(parts) < 2:
            await message.channel.send("❌ Usage: `@training-create Title | MM/DD/YYYY | Notes (optional)`")
            return

        title = parts[0].strip()
        date_str = parts[1].strip()
        notes = parts[2].strip() if len(parts) > 2 else ""

        # Parse date
        try:
            training_date = datetime.strptime(date_str, '%m/%d/%Y').date()
        except ValueError:
            await message.channel.send(f"❌ Invalid date format: `{date_str}`. Use MM/DD/YYYY")
            return

        # Save to database
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''INSERT INTO trainings
                     (title, date, presenter, presenter_id, notes, created_by, created_by_id)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (title, training_date.isoformat(), message.author.display_name,
                   message.author.id, notes, message.author.display_name, message.author.id))
        training_id = c.lastrowid
        conn.commit()
        conn.close()

        embed = discord.Embed(
            title="🎓 Training Created",
            description=f"**{title}**",
            color=discord.Color.blue()
        )
        embed.add_field(name="Date", value=training_date.strftime('%B %d, %Y'), inline=True)
        embed.add_field(name="Training ID", value=f"#{training_id}", inline=True)
        if notes:
            embed.add_field(name="Notes", value=notes, inline=False)
        embed.add_field(name="Sign In", value=f"Use `@training-signin {training_id}` to sign in", inline=False)
        embed.set_footer(text=f"Created by {message.author.display_name}")

        await message.channel.send(embed=embed)
        await message.add_reaction('✅')
        return

    # Handle @training-signin command
    if message.content.startswith('@training-signin '):
        try:
            training_id = int(message.content[17:].strip())
        except ValueError:
            await message.channel.send("❌ Usage: `@training-signin <training_id>`")
            return

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        # Check if training exists
        c.execute('SELECT title, date FROM trainings WHERE id = ?', (training_id,))
        training = c.fetchone()
        if not training:
            conn.close()
            await message.channel.send(f"❌ Training #{training_id} not found")
            return

        # Check if already signed in
        c.execute('''SELECT id FROM training_attendance
                     WHERE training_id = ? AND attendee_id = ?''',
                  (training_id, message.author.id))
        if c.fetchone():
            conn.close()
            await message.channel.send(f"✅ You're already signed in for this training!")
            return

        # Sign in
        c.execute('''INSERT INTO training_attendance (training_id, attendee_name, attendee_id)
                     VALUES (?, ?, ?)''',
                  (training_id, message.author.display_name, message.author.id))
        conn.commit()

        # Get attendance count
        c.execute('SELECT COUNT(*) FROM training_attendance WHERE training_id = ?', (training_id,))
        attendance_count = c.fetchone()[0]
        conn.close()

        await message.add_reaction('✅')
        await message.channel.send(
            f"🎓 {message.author.mention} signed in for **{training[0]}** ({attendance_count} attendees)"
        )
        return

    # Handle @important command
    if message.content.startswith('@important '):
        important_content = message.content[11:].strip()
        if not important_content:
            await message.channel.send("❌ Usage: `@important <message>`")
            return

        # Post the important message
        embed = discord.Embed(
            title="📢 IMPORTANT INFORMATION",
            description=important_content,
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Posted by {message.author.display_name}")
        embed.timestamp = datetime.now()

        important_msg = await message.channel.send(embed=embed)
        await important_msg.add_reaction('👁️')

        # Save to database
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''INSERT INTO important_messages
                     (message_id, channel_id, channel_name, author_name, author_id, content_preview, posted_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (important_msg.id, message.channel.id, message.channel.name,
                   message.author.display_name, message.author.id, important_content[:200],
                   datetime.now().isoformat()))
        conn.commit()
        conn.close()

        # Delete original command message
        try:
            await message.delete()
        except:
            pass

        return

    # Handle @sync command
    if message.content.startswith('@sync'):
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        columns = [description[0] for description in c.description]
        rows = c.fetchall()
        conn.close()

        tasks = []
        for row in rows:
            tasks.append(dict(zip(columns, row)))

        # Create JSON file
        with open('tasks_export.json', 'w') as f:
            json.dump(tasks, f, indent=2, default=str)

        await message.channel.send(
            "📊 Task database exported!",
            file=discord.File('tasks_export.json')
        )
        return

    # Handle @reset_numbering command (admin only)
    if message.content.startswith('@reset_numbering'):
        # Check if user is authorized
        if message.author.id not in AUTHORIZED_USERS:
            await message.channel.send(f"❌ {message.author.mention}, you're not authorized to reset task numbering.")
            return

        # Add confirmation to prevent accidental resets
        if not message.content.endswith(' CONFIRM'):
            await message.channel.send(
                "⚠️ **Warning:** This will reset task numbering to start from 1.\n"
                "All existing tasks will be kept in the database.\n"
                "To confirm, use: `@reset_numbering CONFIRM`"
            )
            return

        try:
            conn = sqlite3.connect('tasks.db')
            c = conn.cursor()

            # Get all existing tasks
            c.execute('SELECT COUNT(*) FROM tasks')
            task_count = c.fetchone()[0]

            # Delete and recreate table to reset auto-increment
            # First, back up all tasks
            c.execute('SELECT * FROM tasks')
            columns = [description[0] for description in c.description]
            all_tasks = c.fetchall()

            # Drop and recreate table
            c.execute('DROP TABLE tasks')
            c.execute('''CREATE TABLE tasks
                         (task_number INTEGER PRIMARY KEY,
                          title TEXT NOT NULL,
                          description TEXT,
                          created_by TEXT,
                          created_by_id INTEGER,
                          assigned_to TEXT,
                          assigned_to_id INTEGER,
                          task_type TEXT,
                          status TEXT DEFAULT 'pending',
                          priority TEXT DEFAULT 'medium',
                          due_date TEXT,
                          category TEXT,
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                          completed_at TIMESTAMP,
                          pool_role TEXT,
                          claimed_by TEXT,
                          claimed_by_id INTEGER,
                          claimed_at TIMESTAMP,
                          reference_message_link TEXT,
                          reference_message_id INTEGER,
                          channel_id INTEGER,
                          bot_message_id INTEGER,
                          is_campfire BOOLEAN DEFAULT 0)''')

            # Restore tasks with new numbering (1, 2, 3, ...)
            for idx, row in enumerate(all_tasks, start=1):
                task_dict = dict(zip(columns, row))
                # Insert with new task_number
                c.execute('''INSERT INTO tasks
                             (task_number, title, description, created_by, created_by_id,
                              assigned_to, assigned_to_id, task_type, status, priority, due_date,
                              category, created_at, completed_at, pool_role, claimed_by, claimed_by_id,
                              claimed_at, reference_message_link, reference_message_id, channel_id,
                              bot_message_id, is_campfire)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (idx, task_dict['title'], task_dict['description'], task_dict['created_by'],
                           task_dict['created_by_id'], task_dict['assigned_to'], task_dict['assigned_to_id'],
                           task_dict['task_type'], task_dict['status'], task_dict['priority'],
                           task_dict['due_date'], task_dict['category'], task_dict['created_at'],
                           task_dict['completed_at'], task_dict['pool_role'], task_dict['claimed_by'],
                           task_dict['claimed_by_id'], task_dict['claimed_at'], task_dict['reference_message_link'],
                           task_dict['reference_message_id'], task_dict['channel_id'], task_dict['bot_message_id'],
                           task_dict['is_campfire']))

            conn.commit()
            conn.close()

            embed = discord.Embed(
                title="🔄 Task Numbering Reset Complete",
                description=f"All {task_count} tasks have been renumbered starting from 1.",
                color=discord.Color.blue()
            )
            embed.add_field(name="Next Task Number", value=str(task_count + 1), inline=True)
            embed.set_footer(text="All task data preserved - only numbers changed")

            await message.channel.send(embed=embed)
            await message.add_reaction('✅')

        except Exception as e:
            await message.channel.send(f"❌ Error resetting numbering: {str(e)}")
            print(f"Reset numbering error: {e}")
        return

    # Track mentions for all team members
    try:
        # Dictionary mapping Discord IDs to names (from TEAM_MEMBERS)
        team_members_map = {
            928725439059464222: 'Megan',
            1364146121313034291: 'Ash',
            928725621253812285: 'Preston',
            1364146180448383027: 'Dakota',
            1364146215722803240: 'Jason',
            1364146251902844948: 'Trevor',
            1364146301805269063: 'Tyler'
        }

        mentioned_users = set()

        # Track direct user mentions
        for user in message.mentions:
            if user.id in team_members_map:
                mentioned_users.add((user.id, team_members_map[user.id], 'direct_mention'))

        # Track replies
        if message.reference and message.reference.resolved:
            replied_to = message.reference.resolved.author
            if replied_to.id in team_members_map:
                mentioned_users.add((replied_to.id, team_members_map[replied_to.id], 'reply'))

        # Track role mentions
        if message.role_mentions:
            for role in message.role_mentions:
                # Get members of this role
                if hasattr(message.guild, 'get_role'):
                    role_obj = message.guild.get_role(role.id)
                    if role_obj:
                        for member in role_obj.members:
                            if member.id in team_members_map:
                                mentioned_users.add((member.id, team_members_map[member.id], 'role_mention'))

        # Track @everyone and @here
        if message.mention_everyone:
            for user_id, user_name in team_members_map.items():
                mentioned_users.add((user_id, user_name, 'everyone'))

        # Save mentions to database
        if mentioned_users:
            conn = sqlite3.connect('tasks.db')
            c = conn.cursor()
            for user_id, user_name, mention_type in mentioned_users:
                # Don't save self-mentions
                if user_id == message.author.id:
                    continue

                c.execute('''INSERT INTO mentions
                            (user_name, user_id, message_content, message_link, message_id,
                             channel_id, channel_name, author_name, author_id, mention_type)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (user_name, user_id, message.content[:500], message.jump_url,
                          message.id, message.channel.id, message.channel.name,
                          message.author.display_name, message.author.id, mention_type))
            conn.commit()
            conn.close()
    except Exception as e:
        print(f"Error tracking mentions: {e}")

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    print(f"🔔 Reaction detected: {reaction.emoji} by {user.name} (ID: {user.id})")

    if user == bot.user:
        print("  ↳ Ignoring bot's own reaction")
        return

    # Handle 👁️ reaction for important messages
    if str(reaction.emoji) == '👁️':
        message = reaction.message
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT id FROM important_messages WHERE message_id = ?', (message.id,))
        important_msg = c.fetchone()
        if important_msg:
            c.execute('''SELECT id FROM message_reactions WHERE message_id = ? AND user_id = ?''',
                      (message.id, user.id))
            if not c.fetchone():
                c.execute('''INSERT INTO message_reactions (message_id, user_name, user_id)
                             VALUES (?, ?, ?)''', (message.id, user.display_name, user.id))
                conn.commit()
                print(f"✅ {user.display_name} marked important message {message.id} as read")
        conn.close()

    # Handle 📌 reaction to add any message as a task
    if str(reaction.emoji) == '📌':
        print(f"  ↳ Pin reaction detected!")
        print(f"  ↳ User ID: {user.id}")
        print(f"  ↳ Authorized users: {AUTHORIZED_USERS}")
        print(f"  ↳ Is authorized: {user.id in AUTHORIZED_USERS}")

        # Check if user is authorized
        if user.id not in AUTHORIZED_USERS:
            print(f"  ↳ User {user.id} NOT authorized")
            await reaction.message.channel.send(f"❌ {user.mention}, you're not authorized to use 📌 to create tasks.")
            return

        message = reaction.message

        # Check if this message already has a task
        existing_task = get_task_by_message_id(message.id)
        if existing_task:
            print(f"  ↳ Message already has task #{existing_task}, skipping")
            await message.channel.send(f"✅ Already got it! Task #{existing_task} was created from this message.")
            return

        print(f"  ↳ User IS authorized, creating task...")
        task_content = message.content or message.system_content or "Task from message"

        # Truncate if too long
        if len(task_content) > 200:
            task_content = task_content[:197] + "..."

        cleaned_content, metadata = parse_task_metadata(task_content)

        task_number = add_task(
            title=cleaned_content,
            description=f"Created from message by {message.author.display_name}",
            created_by=user.display_name,
            created_by_id=user.id,
            task_type='request',
            priority=metadata['priority'],
            due_date=metadata['due_date'],
            category=metadata['category'],
            reference_message_link=message.jump_url,
            reference_message_id=message.id,
            channel_id=message.channel.id
        )

        print(f"  ↳ Task #{task_number} created successfully!")

        # Send a proper embed with reactions for claiming/completing
        embed = discord.Embed(
            title=f"📋 New Task #{task_number}",
            description=cleaned_content,
            color=discord.Color.blue()
        )
        embed.add_field(name="Priority", value=metadata['priority'].upper(), inline=True)
        if metadata['category']:
            embed.add_field(name="Category", value=metadata['category'], inline=True)
        if metadata['due_date']:
            embed.add_field(name="Due Date", value=metadata['due_date'], inline=True)
        embed.add_field(name="Created by", value=user.mention, inline=True)
        embed.add_field(name="Original Message", value=f"[View Message]({message.jump_url})", inline=False)
        embed.set_footer(text="React with ✋ to claim or ✅ to complete")

        task_message = await message.channel.send(f"📌 New task created!", embed=embed)

        # Add reaction buttons
        await task_message.add_reaction('✋')
        await task_message.add_reaction('✅')

        # Save the bot message ID
        update_bot_message_id(task_number, task_message.id)

        return

    # Handle 🔥 reaction for campfire (private) tasks
    if str(reaction.emoji) == '🔥':
        print(f"  ↳ Campfire reaction detected!")
        print(f"  ↳ User ID: {user.id}")
        print(f"  ↳ Campfire authorized users: {CAMPFIRE_AUTHORIZED_USERS}")
        print(f"  ↳ Is authorized: {user.id in CAMPFIRE_AUTHORIZED_USERS}")

        # Check if user is authorized for campfire tasks
        if user.id not in CAMPFIRE_AUTHORIZED_USERS:
            print(f"  ↳ User {user.id} NOT authorized for campfire tasks")
            try:
                await user.send(f"❌ You're not authorized to create Campfire tasks. Only Lauren and Megan can use 🔥 reactions.")
            except:
                pass
            return

        message = reaction.message

        # Check if this message already has a task
        existing_task = get_task_by_message_id(message.id)
        if existing_task:
            print(f"  ↳ Message already has task #{existing_task}, skipping")
            # Send DM instead of channel message for campfire
            try:
                await user.send(f"✅ Already got it! Task #{existing_task} was created from this message (Campfire).")
            except:
                pass
            return

        print(f"  ↳ User IS authorized, creating campfire task...")
        task_content = message.content or message.system_content or "Campfire task from message"

        # Truncate if too long
        if len(task_content) > 200:
            task_content = task_content[:197] + "..."

        cleaned_content, metadata = parse_task_metadata(task_content)

        task_number = add_task(
            title=cleaned_content,
            description=f"Campfire task created from message by {message.author.display_name}",
            created_by=user.display_name,
            created_by_id=user.id,
            task_type='campfire',
            priority=metadata['priority'],
            due_date=metadata['due_date'],
            category=metadata['category'],
            reference_message_link=message.jump_url,
            reference_message_id=message.id,
            channel_id=message.channel.id,
            is_campfire=True
        )

        print(f"  ↳ Campfire task #{task_number} created successfully!")

        # Send confirmation as DM to keep it private
        try:
            embed = discord.Embed(
                title=f"🔥 Campfire Task #{task_number} Created",
                description=cleaned_content,
                color=discord.Color.orange()
            )
            embed.add_field(name="Priority", value=metadata['priority'].upper(), inline=True)
            if metadata['due_date']:
                embed.add_field(name="Due Date", value=metadata['due_date'], inline=True)
            embed.add_field(name="Original Message", value=f"[Jump to message]({message.jump_url})", inline=False)
            embed.set_footer(text="This is a private campfire task - only you can see it")

            await user.send(embed=embed)
        except discord.Forbidden:
            # If DM fails, send ephemeral message (can't do in reaction, so just skip)
            print(f"  ↳ Could not DM user {user.id}")
        return

    # Handle extra custom reaction (for Ash)
    if str(reaction.emoji) == EXTRA_REACT_EMOJI:
        print(f"  ↳ Extra custom reaction ({EXTRA_REACT_EMOJI}) detected!")
        print(f"  ↳ User ID: {user.id}")
        print(f"  ↳ Extra react user: {EXTRA_REACT_USER}")
        print(f"  ↳ Is authorized: {user.id == EXTRA_REACT_USER}")

        # Check if user is authorized for this custom reaction
        if user.id != EXTRA_REACT_USER:
            print(f"  ↳ User {user.id} NOT authorized for extra reaction")
            try:
                await user.send(f"❌ You're not authorized to use the {EXTRA_REACT_EMOJI} reaction. Only Ash can use this.")
            except:
                pass
            return

        message = reaction.message

        # Check if this message already has a task
        existing_task = get_task_by_message_id(message.id)
        if existing_task:
            print(f"  ↳ Message already has task #{existing_task}, skipping")
            await message.channel.send(f"📌 Already got it! Task #{existing_task} was created from this message.")
            return

        print(f"  ↳ User IS authorized, creating task with custom reaction...")
        task_content = message.content or message.system_content or "Custom task from message"

        # Truncate if too long
        if len(task_content) > 200:
            task_content = task_content[:197] + "..."

        cleaned_content, metadata = parse_task_metadata(task_content)

        task_number = add_task(
            title=cleaned_content,
            description=f"Task created via {EXTRA_REACT_EMOJI} reaction by {message.author.display_name}",
            created_by=user.display_name,
            created_by_id=user.id,
            task_type='request',
            priority=metadata['priority'],
            due_date=metadata['due_date'],
            category=metadata['category'],
            reference_message_link=message.jump_url,
            reference_message_id=message.id,
            channel_id=message.channel.id
        )

        print(f"  ↳ Task #{task_number} created successfully via custom reaction!")

        # Simple response with link
        await message.channel.send(f"{EXTRA_REACT_EMOJI} Got it! Task #{task_number} created → [View original message]({message.jump_url})")
        return

    # Handle custom reaction auto-assignments (👍 → Ash, etc.)
    if str(reaction.emoji) in REACTION_ASSIGNMENTS:
        message = reaction.message

        # Check if this is a task message
        if not message.embeds:
            return

        embed = message.embeds[0]
        if not embed.title:
            return

        # Check if it's a task that can be assigned
        is_pool_task = embed.title.startswith('🎯 New Pool Task #')
        is_assigned_task = embed.title.startswith('📋 New Task Assigned #')
        is_request_task = embed.title.startswith('📋 New Task #')

        if not (is_pool_task or is_assigned_task or is_request_task):
            return

        # Extract task number
        try:
            task_number = int(embed.title.split('#')[1].split()[0])
        except:
            return

        task = get_task(task_number)
        if not task:
            return

        # Get assignee info from config
        assignee_name, assignee_id, assignee_channel = REACTION_ASSIGNMENTS[str(reaction.emoji)]

        # Assign the task
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''UPDATE tasks
                     SET assigned_to = ?, assigned_to_id = ?, task_type = 'assigned',
                         claimed_by = ?, claimed_by_id = ?, claimed_at = CURRENT_TIMESTAMP,
                         status = 'in_progress'
                     WHERE task_number = ?''',
                  (assignee_name, assignee_id, assignee_name, assignee_id, task_number))
        conn.commit()
        conn.close()

        # Edit the original message
        try:
            old_embed = message.embeds[0]
            assigned_embed = discord.Embed(
                title=f"✅ Task #{task_number} Auto-Assigned to {assignee_name}",
                description=old_embed.description,
                color=discord.Color.purple()
            )

            # Copy original fields
            for field in old_embed.fields:
                assigned_embed.add_field(name=field.name, value=field.value, inline=field.inline)

            # Add assignment info
            assigned_embed.add_field(name="👤 Assigned to", value=f"<@{assignee_id}>", inline=True)
            assigned_embed.add_field(name="Status", value="📋 Assigned", inline=True)
            assigned_embed.set_footer(text=f"Auto-assigned via {reaction.emoji} reaction")
            assigned_embed.timestamp = datetime.now()

            await message.edit(embed=assigned_embed)
        except Exception as e:
            print(f"Could not edit task message: {e}")

        # Send to assignee's personal channel
        if assignee_channel and assignee_channel != 0:
            try:
                personal_channel = bot.get_channel(int(assignee_channel))
                if personal_channel:
                    task = get_task(task_number)  # Refresh task data
                    personal_embed = discord.Embed(
                        title=f"📋 Task #{task_number} - ASSIGNED TO YOU!",
                        description=task['title'],
                        color=discord.Color.purple()
                    )
                    personal_embed.add_field(name="Priority", value=task.get('priority', 'medium').upper(), inline=True)
                    if task.get('category'):
                        personal_embed.add_field(name="Category", value=task['category'], inline=True)
                    if task.get('due_date'):
                        personal_embed.add_field(name="Due Date", value=task['due_date'], inline=True)
                    if task.get('description'):
                        personal_embed.add_field(name="Description", value=task['description'], inline=False)
                    if task.get('reference_message_link'):
                        personal_embed.add_field(name="Original Request", value=f"[View Message]({task['reference_message_link']})", inline=False)

                    personal_embed.set_footer(text="React with ✅ when you complete it!")

                    sent_message = await personal_channel.send(f"📋 <@{assignee_id}> New task assigned to you!", embed=personal_embed)
                    await sent_message.add_reaction('✅')

                    # Update bot message tracking
                    update_bot_message_id(task_number, sent_message.id)
                    conn = sqlite3.connect('tasks.db')
                    c = conn.cursor()
                    c.execute('UPDATE tasks SET channel_id = ? WHERE task_number = ?',
                            (assignee_channel, task_number))
                    conn.commit()
                    conn.close()

                    print(f"✅ Auto-assigned task #{task_number} to {assignee_name} via {reaction.emoji}")
            except Exception as e:
                print(f"Error sending assignment to personal channel: {e}")

        return

    # Handle ✋ reaction to claim pool or assigned tasks
    if str(reaction.emoji) == '✋':
        message = reaction.message

        # Check if this is a task message (pool or assigned)
        if not message.embeds:
            return

        embed = message.embeds[0]
        if not embed.title:
            return

        # Check if it's a pool task, assigned task, or general request task
        is_pool_task = embed.title.startswith('🎯 New Pool Task #')
        is_assigned_task = embed.title.startswith('📋 New Task Assigned #')
        is_request_task = embed.title.startswith('📋 New Task #')

        if not (is_pool_task or is_assigned_task or is_request_task):
            return

        # Extract task number from title
        try:
            task_number = int(embed.title.split('#')[1].split()[0])
        except:
            return

        task = get_task(task_number)
        if not task:
            return

        # For pool tasks, check task type; for assigned tasks, allow claiming
        if is_pool_task and task['task_type'] != 'pool':
            return

        if task['status'] not in ['pending', 'active']:
            await message.channel.send(f"❌ {user.mention}, this task has already been claimed or completed!")
            return

        # Claim the task
        if claim_pool_task(task_number, user.display_name, user.id):
            # Get updated task info
            task = get_task(task_number)

            # Edit the original message to show it was claimed
            try:
                old_embed = message.embeds[0]
                claim_embed = discord.Embed(
                    title=f"✋ Task #{task_number} Claimed by {user.display_name}",
                    description=old_embed.description,
                    color=discord.Color.gold()
                )

                # Copy original fields
                for field in old_embed.fields:
                    claim_embed.add_field(name=field.name, value=field.value, inline=field.inline)

                # Add claimed by field
                claim_embed.add_field(name="👤 Claimed by", value=user.mention, inline=True)
                claim_embed.add_field(name="Status", value="🔨 In Progress", inline=True)
                claim_embed.set_footer(text="React with ✅ when completed")
                claim_embed.timestamp = datetime.now()

                await message.edit(embed=claim_embed)
            except Exception as e:
                print(f"Could not edit task message: {e}")

            # Send task to claimer's personal channel
            personal_channel_id = PERSONAL_CHANNELS.get(user.display_name)
            if personal_channel_id and personal_channel_id != 0:
                try:
                    personal_channel = bot.get_channel(int(personal_channel_id))
                    if personal_channel:
                        # Create a detailed task embed for their personal channel
                        personal_embed = discord.Embed(
                            title=f"📋 Task #{task_number} - YOU CLAIMED THIS!",
                            description=task['title'],
                            color=discord.Color.gold()
                        )
                        personal_embed.add_field(name="Priority", value=task.get('priority', 'medium').upper(), inline=True)
                        if task.get('category'):
                            personal_embed.add_field(name="Category", value=task['category'], inline=True)
                        if task.get('due_date'):
                            personal_embed.add_field(name="Due Date", value=task['due_date'], inline=True)
                        if task.get('description'):
                            personal_embed.add_field(name="Description", value=task['description'], inline=False)
                        if task.get('reference_message_link'):
                            personal_embed.add_field(name="Original Request", value=f"[View Message]({task['reference_message_link']})", inline=False)

                        personal_embed.set_footer(text="React with ✅ when you complete it!")

                        sent_message = await personal_channel.send(f"🎯 {user.mention} You claimed a task!", embed=personal_embed)

                        # Add reactions for quick actions
                        await sent_message.add_reaction('✅')

                        # Update the task to point to the new message
                        update_bot_message_id(task_number, sent_message.id)
                        conn = sqlite3.connect('tasks.db')
                        c = conn.cursor()
                        c.execute('UPDATE tasks SET channel_id = ?, task_type = ? WHERE task_number = ?',
                                (personal_channel_id, 'assigned', task_number))
                        conn.commit()
                        conn.close()

                        print(f"✅ Sent claimed task #{task_number} to {user.display_name}'s personal channel")
                except Exception as e:
                    print(f"Error sending claimed task to personal channel: {e}")
    
    # Handle ✅ reaction to complete tasks (pool or assigned)
    if str(reaction.emoji) == '✅':
        message = reaction.message

        if not message.embeds:
            return

        embed = message.embeds[0]
        if not embed.title:
            return

        # Check for claimed task, new assigned task, new pool task, or general request task
        is_claimed_task = embed.title.startswith('✋ Task #')
        is_assigned_task = embed.title.startswith('📋 New Task Assigned #')
        is_pool_task = embed.title.startswith('🎯 New Pool Task #')
        is_request_task = embed.title.startswith('📋 New Task #')

        if not (is_claimed_task or is_assigned_task or is_pool_task or is_request_task):
            return

        try:
            task_number = int(embed.title.split('#')[1].split()[0])
        except:
            return

        task = get_task(task_number)
        if not task:
            return

        # For claimed tasks, check if user is the one who claimed it
        if is_claimed_task and task.get('claimed_by_id'):
            if task['claimed_by_id'] != user.id:
                await message.channel.send(f"❌ {user.mention}, you can only complete tasks you've claimed!")
                return

        # For assigned tasks, allow the assignee to complete directly
        if is_assigned_task and task.get('assigned_to_id'):
            if task['assigned_to_id'] != user.id:
                await message.channel.send(f"❌ {user.mention}, only the assignee can complete this task!")
                return

        if task['status'] == 'completed':
            await message.channel.send(f"ℹ️ Task #{task_number} is already completed!")
            return

        update_task_status(task_number, 'completed', user.display_name)

        # Edit the original message to show completion
        try:
            old_embed = message.embeds[0]
            complete_embed = discord.Embed(
                title=f"✅ Task #{task_number} Completed",
                description=old_embed.description,
                color=discord.Color.green()
            )

            # Copy original fields except Status
            for field in old_embed.fields:
                if field.name != "Status":
                    complete_embed.add_field(name=field.name, value=field.value, inline=field.inline)

            # Add completion status
            complete_embed.add_field(name="Status", value=f"✅ Completed", inline=True)
            complete_embed.timestamp = datetime.now()
            complete_embed.set_footer(text=f"Completed by {user.display_name}")

            await message.edit(embed=complete_embed)
        except Exception as e:
            print(f"Could not edit completion message: {e}")
            # Fallback: send new message
            complete_embed = discord.Embed(
                title=f"✅ Task #{task_number} Completed",
                description=task['title'],
                color=discord.Color.green()
            )
            complete_embed.add_field(name="Completed by", value=user.mention, inline=True)

            await message.channel.send(embed=complete_embed)

    # Handle ❌ reaction to release task back to pool
    if str(reaction.emoji) == '❌':
        message = reaction.message

        if not message.embeds:
            return

        embed = message.embeds[0]
        if not embed.title:
            return

        # Check for claimed task or assigned task
        is_claimed_task = embed.title.startswith('✋ Task #')
        is_assigned_task = embed.title.startswith('📋 New Task Assigned #')
        is_pool_task = embed.title.startswith('🎯 New Pool Task #')

        if not (is_claimed_task or is_assigned_task or is_pool_task):
            return

        try:
            task_number = int(embed.title.split('#')[1].split()[0])
        except:
            return

        task = get_task(task_number)
        if not task:
            return

        # Release the task back to pool
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('''UPDATE tasks
                     SET claimed_by = NULL, claimed_by_id = NULL, claimed_at = NULL
                     WHERE task_number = ?''',
                  (task_number,))
        conn.commit()
        conn.close()

        print(f"🔄 Task #{task_number} released back to pool by {user.display_name}")

        # Notify
        release_embed = discord.Embed(
            title=f"🔄 Task #{task_number} Released to Pool",
            description=task['title'],
            color=discord.Color.blue()
        )
        release_embed.add_field(name="Released by", value=user.mention, inline=True)
        release_embed.set_footer(text="Task is now available for others to claim")

        await message.channel.send(embed=release_embed)

    # Handle 📷 reaction to send to photo tasks channel
    if str(reaction.emoji) == '📷':
        print(f"  ↳ Camera reaction detected!")
        message = reaction.message

        # Check if this message already has a task
        existing_task = get_task_by_message_id(message.id)
        if existing_task:
            print(f"  ↳ Message already has task #{existing_task}, skipping")
            await message.channel.send(f"📷 Already got it! Task #{existing_task} was created from this message.")
            return

        print(f"  ↳ Creating photo task...")
        task_content = message.content or message.system_content or "Photo task from message"

        # Truncate if too long
        if len(task_content) > 200:
            task_content = task_content[:197] + "..."

        cleaned_content, metadata = parse_task_metadata(task_content)

        task_number = add_task(
            title=cleaned_content,
            description=f"Photo task created from message by {message.author.display_name}",
            created_by=user.display_name,
            created_by_id=user.id,
            task_type='request',  # Shows as incoming request
            priority=metadata['priority'],
            due_date=metadata['due_date'],
            category='Photo',
            reference_message_link=message.jump_url,
            reference_message_id=message.id,
            channel_id=message.channel.id
        )

        print(f"  ↳ Photo task #{task_number} created successfully!")

        # Send to the user's photo tasks channel if configured
        # For now, sends to the channel where reaction was added
        embed = discord.Embed(
            title=f"📷 Photo Task #{task_number} Created",
            description=cleaned_content,
            color=discord.Color.purple()
        )
        embed.add_field(name="Created by", value=user.mention, inline=True)
        embed.add_field(name="Priority", value=metadata['priority'].upper(), inline=True)
        if metadata['due_date']:
            embed.add_field(name="Due Date", value=metadata['due_date'], inline=True)
        embed.add_field(name="Category", value="Photo", inline=True)
        embed.add_field(name="Original Message", value=f"[Jump to message]({message.jump_url})", inline=False)
        embed.set_footer(text="React with ✋ to claim or ✅ to complete")

        await message.channel.send(embed=embed)

@bot.event
async def on_reaction_remove(reaction, user):
    """Handle reaction removal"""
    if user == bot.user:
        return
    
    # Handle ✋ removal to unclaim pool tasks
    if str(reaction.emoji) == '✋':
        message = reaction.message

        if not message.embeds:
            return

        embed = message.embeds[0]
        # Check for either new pool task or claimed task
        if not embed.title or not (embed.title.startswith('🎯 New Pool Task #') or embed.title.startswith('✋ Task #')):
            return

        try:
            task_number = int(embed.title.split('#')[1].split()[0])
        except:
            return

        task = get_task(task_number)
        if not task or task['task_type'] != 'pool':
            return

        # Check if user was the one who claimed it
        if task['claimed_by_id'] == user.id and task['status'] == 'in_progress':
            if unclaim_pool_task(task_number):
                # Edit the message back to original pool task state
                try:
                    old_embed = message.embeds[0]
                    unclaim_embed = discord.Embed(
                        title=f"🎯 New Pool Task #{task_number}",
                        description=old_embed.description,
                        color=discord.Color.purple()
                    )

                    # Copy original fields, excluding Claimed by and Status
                    for field in old_embed.fields:
                        if field.name not in ["Claimed by", "Status"]:
                            unclaim_embed.add_field(name=field.name, value=field.value, inline=field.inline)

                    unclaim_embed.set_footer(text="React with ✋ to claim this task")

                    await message.edit(embed=unclaim_embed)
                except Exception as e:
                    print(f"Could not edit unclaim message: {e}")
                    # Fallback: send notification
                    await message.channel.send(f"🔄 Task #{task_number} unclaimed by {user.mention} - back in the pool!")

@bot.event
async def on_message_delete(message):
    """Clean up tasks when the original message is deleted"""
    # Check if this message had a task created from it
    task_number = get_task_by_message_id(message.id)
    if task_number:
        if delete_task_by_message_id(message.id):
            print(f"🗑️ Deleted task #{task_number} - original message was deleted")

# Get Discord token from environment variable
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

if not DISCORD_TOKEN:
    print("ERROR: DISCORD_TOKEN environment variable not set!")
    print("Please set your Discord bot token in Railway environment variables")
    exit(1)

# Initialize database
init_db()

# Start Flask in a separate thread
print(f"🚀 Starting Flask API on port {PORT}...")
flask_thread = Thread(target=run_flask, daemon=False)
flask_thread.start()

# Give Flask time to start
print("⏳ Waiting for Flask to start...")
import time
time.sleep(2)

print("🤖 Starting Discord bot...")
bot.run(DISCORD_TOKEN)
