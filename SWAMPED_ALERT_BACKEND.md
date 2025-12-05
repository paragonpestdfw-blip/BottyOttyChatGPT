# Swamped Alert System - Backend Integration

## Overview
This document contains the Python code snippets to add to your `main.py` file to enable the Swamped Alert system's Discord integration.

## What it does
- Receives swamped alert requests from the Admin Panel
- Posts alerts to a specified Discord channel
- Stores active alerts in memory for retrieval

---

## Step 1: Add the endpoint to your Flask routes

Add this endpoint to your Flask app in `main.py`:

```python
@app.route('/api/swamped-alert', methods=['POST'])
def swamped_alert():
    """
    Handle swamped alert broadcasts from Admin Panel.
    Posts to Discord and stores alert state.
    """
    try:
        data = request.json
        message = data.get('message', '')
        recipients = data.get('recipients', 'all')
        channel_id = data.get('channelId', '')

        if not message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400

        # Build alert embed
        embed = discord.Embed(
            title="🆘 SWAMPED ALERT",
            description=message,
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Recipients", value=recipients.upper(), inline=False)
        embed.add_field(
            name="Action Required",
            value="⚠️ Office needs immediate assistance!",
            inline=False
        )
        embed.set_footer(text="Swamped Alert System")

        # Post to Discord channel
        if channel_id:
            async def send_to_discord():
                try:
                    channel = bot.get_channel(int(channel_id))
                    if channel:
                        await channel.send(embed=embed)
                        # Optionally mention @everyone or specific role
                        if recipients == 'all':
                            await channel.send("@everyone")
                        logger.info(f"✅ Swamped alert sent to channel {channel_id}")
                    else:
                        logger.error(f"❌ Channel {channel_id} not found")
                except Exception as e:
                    logger.error(f"❌ Error sending swamped alert: {e}")

            # Schedule the async task
            bot.loop.create_task(send_to_discord())

        # Store alert in global state (optional - for tracking active alerts)
        ACTIVE_SWAMPED_ALERT = {
            'message': message,
            'recipients': recipients,
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'channel_id': channel_id,
            'active': True
        }

        return jsonify({
            'success': True,
            'message': 'Swamped alert sent successfully',
            'alert': ACTIVE_SWAMPED_ALERT
        })

    except Exception as e:
        logger.error(f"❌ Error in swamped alert endpoint: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
```

---

## Step 2: Add global variable for tracking active alerts (optional)

Add this near the top of your `main.py` with other global variables:

```python
# Global state for swamped alerts
ACTIVE_SWAMPED_ALERT = None
```

---

## Step 3: Add endpoint to check active swamped alert (optional)

This allows the dashboard to fetch the current alert status from the backend:

```python
@app.route('/api/swamped-alert', methods=['GET'])
def get_swamped_alert():
    """
    Retrieve the current active swamped alert.
    """
    global ACTIVE_SWAMPED_ALERT

    if ACTIVE_SWAMPED_ALERT and ACTIVE_SWAMPED_ALERT.get('active'):
        return jsonify({
            'success': True,
            'alert': ACTIVE_SWAMPED_ALERT
        })
    else:
        return jsonify({
            'success': True,
            'alert': None
        })
```

---

## Step 4: Add endpoint to clear swamped alert (optional)

This allows clearing the alert from the backend:

```python
@app.route('/api/swamped-alert/clear', methods=['POST'])
def clear_swamped_alert():
    """
    Clear the active swamped alert.
    """
    global ACTIVE_SWAMPED_ALERT

    if ACTIVE_SWAMPED_ALERT:
        ACTIVE_SWAMPED_ALERT['active'] = False
        return jsonify({
            'success': True,
            'message': 'Alert cleared successfully'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'No active alert to clear'
        })
```

---

## Step 5: Update CONFIG for default swamped alert channel (optional)

Add a default channel ID to your CONFIG dict:

```python
CONFIG = {
    # ... existing config ...
    'CHANNELS': {
        # ... existing channels ...
        'swamped_alerts': 1234567890123456789,  # Replace with your channel ID
    }
}
```

Then update the endpoint to use this default if no channel is provided:

```python
# In the swamped_alert endpoint, replace:
channel_id = data.get('channelId', '')

# With:
channel_id = data.get('channelId', '') or CONFIG['CHANNELS'].get('swamped_alerts', '')
```

---

## Testing

1. **Test from Admin Panel:**
   - Open Admin Panel v18.html
   - Navigate to "🆘 Swamped Alert" section
   - Enter a test message: "Testing swamped alert system"
   - Add a Discord channel ID (or leave blank for dashboard-only)
   - Click "🆘 Send Swamped Alert"

2. **Verify on Dashboard:**
   - Open BottyOtty Dashboard v18.html
   - You should see a red banner at the top with your message
   - Banner should pulse/animate
   - Click "✅ Dismiss Alert" to clear it

3. **Verify on Discord (if channel ID provided):**
   - Check the specified Discord channel
   - You should see the red embed with your message
   - If recipients='all', @everyone should be mentioned

---

## Notes

- The frontend (Admin Panel + Dashboard) works **without** the backend
- Alerts are stored in localStorage and will show on the dashboard
- Backend integration adds Discord posting functionality
- All Discord operations are async to avoid blocking the Flask server
- Add error handling as needed for your specific setup

---

## Channel ID Examples

Common channels you might want to use:
- Office alerts channel: Get ID from Discord (right-click channel → Copy ID)
- Manager-only channel: For manager-specific alerts
- General channel: For company-wide announcements

Enable Developer Mode in Discord to see channel IDs:
Settings → Advanced → Developer Mode

---

## Frontend Flow (Already Implemented)

1. **Admin Panel** → User composes alert → Saves to localStorage → Calls `/api/swamped-alert`
2. **Dashboard** → Checks localStorage every 30 seconds → Shows banner if active
3. **Clear Alert** → Updates localStorage → Optionally calls `/api/swamped-alert/clear`

All frontend code is already in place! Just add the backend when ready.
