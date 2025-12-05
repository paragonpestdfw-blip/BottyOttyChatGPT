"""
BottyOtty - Database Integration Code (Part 2)
Continue adding this code to main.py after Part 1
"""

# ============================================================================
# SAFETY API ENDPOINTS
# ============================================================================

@app.route('/api/safety/incidents', methods=['GET'])
def get_safety_incidents():
    """Get all safety incidents"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM safety_incidents ORDER BY date DESC')
        rows = c.fetchall()
        conn.close()

        incidents = []
        for row in rows:
            incidents.append({
                'id': row[0],
                'type': row[1],
                'severity': row[2],
                'description': row[3],
                'location': row[4],
                'reportedBy': row[5],
                'date': row[6]
            })

        return jsonify({'success': True, 'incidents': incidents})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/safety/incidents', methods=['POST'])
def add_safety_incident():
    """Report a new safety incident"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO safety_incidents (type, severity, description, location, reported_by, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['type'],
            data['severity'],
            data['description'],
            data.get('location', ''),
            data.get('reportedBy', ''),
            data['date']
        ))

        incident_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'id': incident_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/safety/inspections', methods=['GET'])
def get_safety_inspections():
    """Get all safety inspections"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM safety_inspections ORDER BY date DESC')
        rows = c.fetchall()
        conn.close()

        inspections = []
        for row in rows:
            inspections.append({
                'id': row[0],
                'area': row[1],
                'inspector': row[2],
                'passed': bool(row[3]),
                'notes': row[4],
                'date': row[5]
            })

        return jsonify({'success': True, 'inspections': inspections})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/safety/inspections', methods=['POST'])
def add_safety_inspection():
    """Log a new safety inspection"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO safety_inspections (area, inspector, passed, notes, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['area'],
            data.get('inspector', ''),
            1 if data['passed'] else 0,
            data.get('notes', ''),
            data['date']
        ))

        inspection_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'id': inspection_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# CUSTOMER FEEDBACK API ENDPOINTS
# ============================================================================

@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    """Get all customer feedback"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM customer_feedback ORDER BY date DESC')
        rows = c.fetchall()
        conn.close()

        feedback = []
        for row in rows:
            feedback.append({
                'id': row[0],
                'customer': row[1],
                'rating': row[2],
                'category': row[3],
                'comment': row[4],
                'technician': row[5],
                'date': row[6],
                'followUpNeeded': bool(row[7])
            })

        return jsonify({'success': True, 'feedback': feedback})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/feedback', methods=['POST'])
def add_feedback():
    """Add new customer feedback"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO customer_feedback (customer, rating, category, comment, technician, date, follow_up_needed)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['customer'],
            data['rating'],
            data['category'],
            data.get('comment', ''),
            data.get('technician', ''),
            data['date'],
            1 if data.get('followUpNeeded', False) else 0
        ))

        feedback_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'id': feedback_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# TECH REMINDERS API ENDPOINTS
# ============================================================================

@app.route('/api/tech-reminders', methods=['GET'])
def get_tech_reminders():
    """Get all tech reminders"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM tech_reminders ORDER BY created_at DESC')
        rows = c.fetchall()
        conn.close()

        reminders = []
        for row in rows:
            reminders.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'tech': row[3],
                'dueDate': row[4],
                'priority': row[5],
                'category': row[6],
                'completed': bool(row[7]),
                'createdAt': row[8]
            })

        return jsonify({'success': True, 'reminders': reminders})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/tech-reminders', methods=['POST'])
def add_tech_reminder():
    """Add a new tech reminder"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO tech_reminders (title, description, tech, due_date, priority, category, completed, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['title'],
            data.get('description', ''),
            data['tech'],
            data.get('dueDate', ''),
            data['priority'],
            data['category'],
            0,
            datetime.now().isoformat()
        ))

        reminder_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'id': reminder_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/tech-reminders/<int:reminder_id>', methods=['PUT'])
def update_tech_reminder(reminder_id):
    """Update a tech reminder"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            UPDATE tech_reminders
            SET title=?, description=?, tech=?, due_date=?, priority=?, category=?, completed=?
            WHERE id=?
        ''', (
            data['title'],
            data.get('description', ''),
            data['tech'],
            data.get('dueDate', ''),
            data['priority'],
            data['category'],
            1 if data.get('completed', False) else 0,
            reminder_id
        ))

        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/tech-reminders/<int:reminder_id>', methods=['DELETE'])
def delete_tech_reminder(reminder_id):
    """Delete a tech reminder"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('DELETE FROM tech_reminders WHERE id = ?', (reminder_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# INVENTORY API ENDPOINTS
# ============================================================================

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    """Get all inventory items"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM inventory ORDER BY name')
        rows = c.fetchall()
        conn.close()

        items = []
        for row in rows:
            items.append({
                'id': row[0],
                'name': row[1],
                'quantity': row[2],
                'minQuantity': row[3],
                'category': row[4],
                'location': row[5],
                'notes': row[6]
            })

        return jsonify({'success': True, 'items': items})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/inventory', methods=['POST'])
def add_inventory_item():
    """Add a new inventory item"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO inventory (name, quantity, min_quantity, category, location, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['quantity'],
            data['minQuantity'],
            data['category'],
            data.get('location', ''),
            data.get('notes', '')
        ))

        item_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'id': item_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/inventory/<int:item_id>', methods=['PUT'])
def update_inventory_item(item_id):
    """Update an inventory item"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            UPDATE inventory
            SET name=?, quantity=?, min_quantity=?, category=?, location=?, notes=?
            WHERE id=?
        ''', (
            data['name'],
            data['quantity'],
            data['minQuantity'],
            data['category'],
            data.get('location', ''),
            data.get('notes', ''),
            item_id
        ))

        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    """Delete an inventory item"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# PEST MOVE-UP LIST API ENDPOINTS
# ============================================================================

@app.route('/api/pest-moveup', methods=['GET'])
def get_pest_moveup():
    """Get pest move-up queue"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM pest_moveup ORDER BY position, id')
        rows = c.fetchall()
        conn.close()

        customers = []
        for row in rows:
            customers.append({
                'id': row[0],
                'name': row[1],
                'phone': row[2],
                'address': row[3],
                'reason': row[4],
                'priority': row[5],
                'notes': row[6],
                'dateAdded': row[7],
                'contacted': bool(row[8]),
                'position': row[9]
            })

        return jsonify({'success': True, 'customers': customers})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/pest-moveup', methods=['POST'])
def add_pest_moveup_customer():
    """Add customer to move-up list"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        # Get max position
        c.execute('SELECT MAX(position) FROM pest_moveup')
        max_pos = c.fetchone()[0]
        new_pos = (max_pos or 0) + 1

        c.execute('''
            INSERT INTO pest_moveup (name, phone, address, reason, priority, notes, date_added, contacted, position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['phone'],
            data.get('address', ''),
            data['reason'],
            data['priority'],
            data.get('notes', ''),
            data['dateAdded'],
            0,
            new_pos
        ))

        customer_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'id': customer_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/pest-moveup/<int:customer_id>', methods=['PUT'])
def update_pest_moveup_customer(customer_id):
    """Update customer in move-up list"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            UPDATE pest_moveup
            SET name=?, phone=?, address=?, reason=?, priority=?, notes=?, contacted=?
            WHERE id=?
        ''', (
            data['name'],
            data['phone'],
            data.get('address', ''),
            data['reason'],
            data['priority'],
            data.get('notes', ''),
            1 if data.get('contacted', False) else 0,
            customer_id
        ))

        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/pest-moveup/<int:customer_id>', methods=['DELETE'])
def delete_pest_moveup_customer(customer_id):
    """Remove customer from move-up list"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('DELETE FROM pest_moveup WHERE id = ?', (customer_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# OFFICE ALERTS API ENDPOINTS
# ============================================================================

@app.route('/api/office-alerts', methods=['GET'])
def get_office_alerts():
    """Get all office alerts"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM office_alerts ORDER BY timestamp DESC')
        rows = c.fetchall()
        conn.close()

        alerts = []
        for row in rows:
            alerts.append({
                'id': row[0],
                'message': row[1],
                'recipients': json.loads(row[2]),
                'priority': row[3],
                'channelId': row[4],
                'timestamp': row[5],
                'sent': bool(row[6])
            })

        return jsonify({'success': True, 'alerts': alerts})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/office-alerts', methods=['POST'])
def send_office_alert():
    """Send a new office alert"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO office_alerts (message, recipients, priority, channel_id, timestamp, sent)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['message'],
            json.dumps(data['recipients']),
            data['priority'],
            data.get('channelId', ''),
            datetime.now().isoformat(),
            1
        ))

        alert_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'id': alert_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/alert-people', methods=['GET'])
def get_alert_people():
    """Get list of people for alerts"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM alert_people ORDER BY name')
        rows = c.fetchall()
        conn.close()

        people = []
        for row in rows:
            people.append({
                'id': row[0],
                'name': row[1],
                'discordId': row[2],
                'role': row[3]
            })

        return jsonify({'success': True, 'people': people})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/alert-people', methods=['POST'])
def add_alert_person():
    """Add person to alert list"""
    try:
        data = request.json
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO alert_people (name, discord_id, role)
            VALUES (?, ?, ?)
        ''', (
            data['name'],
            data.get('discordId', ''),
            data.get('role', '')
        ))

        person_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'id': person_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/alert-people/<int:person_id>', methods=['DELETE'])
def delete_alert_person(person_id):
    """Remove person from alert list"""
    try:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('DELETE FROM alert_people WHERE id = ?', (person_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Continue in next file for backup system...
