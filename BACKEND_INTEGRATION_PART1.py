"""
BottyOtty - Database Integration Code
Add this code to your main.py file

INSTALLATION INSTRUCTIONS:
1. Copy all the code below
2. Paste it at the END of your main.py file (before the bot.run() line)
3. The database will auto-initialize on first run
4. Backups will run daily at 3 AM automatically
"""

import os
import shutil
from datetime import datetime
import sqlite3
from flask import Flask, jsonify, request
from discord.ext import tasks

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_bottyotty_tables():
    """Initialize all database tables for BottyOtty tools"""
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    # 1. Calendar Events
    c.execute('''
        CREATE TABLE IF NOT EXISTS calendar_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            mode TEXT NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    # 2. Calendar Notes (month-specific)
    c.execute('''
        CREATE TABLE IF NOT EXISTS calendar_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month_key TEXT NOT NULL UNIQUE,
            notes TEXT
        )
    ''')

    # 3. Lead Sites
    c.execute('''
        CREATE TABLE IF NOT EXISTS lead_sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT,
            status TEXT NOT NULL,
            channel_id TEXT,
            webhook_url TEXT,
            api_key TEXT,
            notes TEXT,
            created_at TEXT NOT NULL
        )
    ''')

    # 4. Vehicles
    c.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
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
            status TEXT NOT NULL,
            notes TEXT
        )
    ''')

    # 5. Safety Incidents
    c.execute('''
        CREATE TABLE IF NOT EXISTS safety_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT,
            reported_by TEXT,
            date TEXT NOT NULL
        )
    ''')

    # 6. Safety Inspections
    c.execute('''
        CREATE TABLE IF NOT EXISTS safety_inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area TEXT NOT NULL,
            inspector TEXT,
            passed INTEGER NOT NULL,
            notes TEXT,
            date TEXT NOT NULL
        )
    ''')

    # 7. Customer Feedback
    c.execute('''
        CREATE TABLE IF NOT EXISTS customer_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            rating INTEGER NOT NULL,
            category TEXT NOT NULL,
            comment TEXT,
            technician TEXT,
            date TEXT NOT NULL,
            follow_up_needed INTEGER NOT NULL
        )
    ''')

    # 8. Tech Reminders
    c.execute('''
        CREATE TABLE IF NOT EXISTS tech_reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            tech TEXT NOT NULL,
            due_date TEXT,
            priority TEXT NOT NULL,
            category TEXT NOT NULL,
            completed INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    # 9. Inventory
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            min_quantity INTEGER NOT NULL,
            category TEXT NOT NULL,
            location TEXT,
            notes TEXT
        )
    ''')

    # 10. Pest Move-Up List
    c.execute('''
        CREATE TABLE IF NOT EXISTS pest_moveup (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT,
            reason TEXT NOT NULL,
            priority TEXT NOT NULL,
            notes TEXT,
            date_added TEXT NOT NULL,
            contacted INTEGER NOT NULL,
            position INTEGER
        )
    ''')

    # 11. Office Alerts
    c.execute('''
        CREATE TABLE IF NOT EXISTS office_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            recipients TEXT NOT NULL,
            priority TEXT NOT NULL,
            channel_id TEXT,
            timestamp TEXT NOT NULL,
            sent INTEGER NOT NULL
        )
    ''')

    # 12. Alert People
    c.execute('''
        CREATE TABLE IF NOT EXISTS alert_people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            discord_id TEXT,
            role TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ BottyOtty database tables initialized!")


# ============================================================================
# CALENDAR API ENDPOINTS
# ============================================================================

@app.route('/api/calendar/events', methods=['GET'])
def get_calendar_events():
    """Get all calendar events"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM calendar_events ORDER BY year, month, day')
        rows = c.fetchall()
        conn.close()

        events = []
        for row in rows:
            events.append({
                'id': row[0],
                'title': row[1],
                'type': row[2],
                'mode': row[3],
                'year': row[4],
                'month': row[5],
                'day': row[6],
                'created_at': row[7]
            })

        return jsonify({'success': True, 'events': events})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/calendar/events', methods=['POST'])
def add_calendar_event():
    """Add a new calendar event"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO calendar_events (title, type, mode, year, month, day, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['title'],
            data['type'],
            data['mode'],
            data['year'],
            data['month'],
            data['day'],
            datetime.now().isoformat()
        ))

        event_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'id': event_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/calendar/events/<int:event_id>', methods=['DELETE'])
def delete_calendar_event(event_id):
    """Delete a calendar event"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('DELETE FROM calendar_events WHERE id = ?', (event_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/calendar/notes/<month_key>', methods=['GET'])
def get_calendar_notes(month_key):
    """Get notes for a specific month"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT notes FROM calendar_notes WHERE month_key = ?', (month_key,))
        row = c.fetchone()
        conn.close()

        notes = row[0] if row else ""
        return jsonify({'success': True, 'notes': notes})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/calendar/notes/<month_key>', methods=['PUT'])
def update_calendar_notes(month_key):
    """Update notes for a specific month"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            INSERT OR REPLACE INTO calendar_notes (month_key, notes)
            VALUES (?, ?)
        ''', (month_key, data['notes']))

        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# LEAD SITES API ENDPOINTS
# ============================================================================

@app.route('/api/lead-sites', methods=['GET'])
def get_lead_sites():
    """Get all lead sites"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM lead_sites ORDER BY created_at DESC')
        rows = c.fetchall()
        conn.close()

        sites = []
        for row in rows:
            sites.append({
                'id': row[0],
                'name': row[1],
                'url': row[2],
                'status': row[3],
                'channelId': row[4],
                'webhookUrl': row[5],
                'apiKey': row[6],
                'notes': row[7],
                'createdAt': row[8]
            })

        return jsonify({'success': True, 'sites': sites})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/lead-sites', methods=['POST'])
def add_lead_site():
    """Add a new lead site"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO lead_sites (name, url, status, channel_id, webhook_url, api_key, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data.get('url', ''),
            data['status'],
            data.get('channelId', ''),
            data.get('webhookUrl', ''),
            data.get('apiKey', ''),
            data.get('notes', ''),
            datetime.now().isoformat()
        ))

        site_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'id': site_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/lead-sites/<int:site_id>', methods=['PUT'])
def update_lead_site(site_id):
    """Update a lead site"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            UPDATE lead_sites
            SET name=?, url=?, status=?, channel_id=?, webhook_url=?, api_key=?, notes=?
            WHERE id=?
        ''', (
            data['name'],
            data.get('url', ''),
            data['status'],
            data.get('channelId', ''),
            data.get('webhookUrl', ''),
            data.get('apiKey', ''),
            data.get('notes', ''),
            site_id
        ))

        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/lead-sites/<int:site_id>', methods=['DELETE'])
def delete_lead_site(site_id):
    """Delete a lead site"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('DELETE FROM lead_sites WHERE id = ?', (site_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# VEHICLES API ENDPOINTS
# ============================================================================

@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    """Get all vehicles"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM vehicles ORDER BY name')
        rows = c.fetchall()
        conn.close()

        vehicles = []
        for row in rows:
            vehicles.append({
                'id': row[0],
                'name': row[1],
                'plate': row[2],
                'vin': row[3],
                'year': row[4],
                'make': row[5],
                'model': row[6],
                'mileage': row[7],
                'lastService': row[8],
                'nextService': row[9],
                'assignedTo': row[10],
                'status': row[11],
                'notes': row[12]
            })

        return jsonify({'success': True, 'vehicles': vehicles})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/vehicles', methods=['POST'])
def add_vehicle():
    """Add a new vehicle"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO vehicles
            (name, plate, vin, year, make, model, mileage, last_service, next_service, assigned_to, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['plate'],
            data.get('vin', ''),
            data.get('year', ''),
            data.get('make', ''),
            data.get('model', ''),
            data.get('mileage', ''),
            data.get('lastService', ''),
            data.get('nextService', ''),
            data.get('assignedTo', ''),
            data['status'],
            data.get('notes', '')
        ))

        vehicle_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'id': vehicle_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    """Update a vehicle"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            UPDATE vehicles
            SET name=?, plate=?, vin=?, year=?, make=?, model=?, mileage=?,
                last_service=?, next_service=?, assigned_to=?, status=?, notes=?
            WHERE id=?
        ''', (
            data['name'],
            data['plate'],
            data.get('vin', ''),
            data.get('year', ''),
            data.get('make', ''),
            data.get('model', ''),
            data.get('mileage', ''),
            data.get('lastService', ''),
            data.get('nextService', ''),
            data.get('assignedTo', ''),
            data['status'],
            data.get('notes', ''),
            vehicle_id
        ))

        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    """Delete a vehicle"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('DELETE FROM vehicles WHERE id = ?', (vehicle_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Continue in next file...
