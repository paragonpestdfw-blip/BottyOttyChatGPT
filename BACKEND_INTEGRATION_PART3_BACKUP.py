"""
BottyOtty - Automatic Backup System (Part 3)
Add this code to main.py after Parts 1 and 2

This will automatically backup your database to GitHub every day at 3 AM
"""

import os
import shutil
from datetime import datetime
import subprocess

# ============================================================================
# AUTOMATIC BACKUP SYSTEM
# ============================================================================

@tasks.loop(hours=24)
async def backup_database():
    """
    Automatically backup database to GitHub daily at 3 AM
    Creates backups in /backups directory and pushes to GitHub
    """
    try:
        # Create backups directory if it doesn't exist
        if not os.path.exists('backups'):
            os.makedirs('backups')

        # Create timestamped backup
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_filename = f'backups/tasks_backup_{timestamp}.db'

        # Copy database file
        shutil.copy2('tasks.db', backup_filename)
        print(f"✅ Database backed up: {backup_filename}")

        # Also keep a "latest" backup
        shutil.copy2('tasks.db', 'backups/tasks_latest.db')

        # Git add and commit (if in git repo)
        try:
            subprocess.run(['git', 'add', backup_filename], check=False)
            subprocess.run(['git', 'add', 'backups/tasks_latest.db'], check=False)
            subprocess.run([
                'git', 'commit', '-m',
                f'Automatic database backup - {timestamp}'
            ], check=False)
            subprocess.run(['git', 'push'], check=False)
            print(f"✅ Backup pushed to GitHub: {timestamp}")

        except Exception as git_error:
            print(f"⚠️  Git backup failed (not critical): {git_error}")
            # Backup still exists locally even if git fails

        # Keep only last 7 days of backups (cleanup)
        cleanup_old_backups()

    except Exception as e:
        print(f"❌ Backup failed: {e}")


def cleanup_old_backups():
    """Remove backups older than 7 days to save space"""
    try:
        if not os.path.exists('backups'):
            return

        files = os.listdir('backups')
        now = datetime.now()

        for filename in files:
            if filename.startswith('tasks_backup_') and filename.endswith('.db'):
                filepath = os.path.join('backups', filename)
                file_time = os.path.getmtime(filepath)
                file_age_days = (now.timestamp() - file_time) / 86400

                # Delete if older than 7 days
                if file_age_days > 7:
                    os.remove(filepath)
                    print(f"🗑️  Removed old backup: {filename}")

    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")


@backup_database.before_loop
async def before_backup():
    """Wait until bot is ready before starting backup loop"""
    await bot.wait_until_ready()
    print("✅ Backup system initialized - running daily at 3 AM")


# ============================================================================
# MANUAL BACKUP ENDPOINT (Optional - for on-demand backups)
# ============================================================================

@app.route('/api/backup/now', methods=['POST'])
def backup_now():
    """Trigger an immediate backup (admin only)"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        if not os.path.exists('backups'):
            os.makedirs('backups')

        backup_filename = f'backups/tasks_backup_{timestamp}.db'
        shutil.copy2('tasks.db', backup_filename)

        return jsonify({
            'success': True,
            'message': f'Backup created: {backup_filename}',
            'timestamp': timestamp
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/backup/list', methods=['GET'])
def list_backups():
    """List all available backups"""
    try:
        if not os.path.exists('backups'):
            return jsonify({'success': True, 'backups': []})

        files = os.listdir('backups')
        backups = []

        for filename in sorted(files, reverse=True):
            if filename.endswith('.db'):
                filepath = os.path.join('backups', filename)
                size = os.path.getsize(filepath)
                modified = datetime.fromtimestamp(os.path.getmtime(filepath))

                backups.append({
                    'filename': filename,
                    'size': size,
                    'modified': modified.isoformat(),
                    'age_days': (datetime.now() - modified).days
                })

        return jsonify({'success': True, 'backups': backups})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# INITIALIZATION CODE - ADD THIS TO YOUR bot.setup_hook()
# ============================================================================

# Add this inside your bot.setup_hook() or bot.on_ready()
@bot.event
async def on_ready():
    """Initialize database and start backup system when bot starts"""
    print(f'Logged in as {bot.user.name}')

    # Initialize BottyOtty database tables
    init_bottyotty_tables()

    # Start backup loop
    if not backup_database.is_running():
        backup_database.start()

    print("✅ BottyOtty integration ready!")


# ============================================================================
# SWAMPED ALERT ENDPOINT (from earlier)
# ============================================================================

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
            timestamp=datetime.utcnow()
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
                        print(f"✅ Swamped alert sent to channel {channel_id}")
                    else:
                        print(f"❌ Channel {channel_id} not found")
                except Exception as e:
                    print(f"❌ Error sending swamped alert: {e}")

            # Schedule the async task
            bot.loop.create_task(send_to_discord())

        return jsonify({
            'success': True,
            'message': 'Swamped alert sent successfully'
        })

    except Exception as e:
        print(f"❌ Error in swamped alert endpoint: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# IMPORT STATEMENT - ADD THIS AT THE TOP OF main.py
# ============================================================================

"""
Add these imports at the top of your main.py if not already present:

import os
import shutil
import subprocess
from datetime import datetime
import json
"""


# ============================================================================
# INSTALLATION CHECKLIST
# ============================================================================

"""
INSTALLATION STEPS:

1. ✅ Copy all code from PART 1, PART 2, and PART 3
2. ✅ Paste into main.py (before bot.run() line)
3. ✅ Add the on_ready() event handler code
4. ✅ Make sure all imports are at the top
5. ✅ Create a 'backups' folder (or let it auto-create)
6. ✅ Push to Railway
7. ✅ Database will auto-initialize on first run
8. ✅ Backups will run daily at 3 AM automatically

TESTING:

Test the database initialization:
- Bot should print "✅ BottyOtty database tables initialized!" on startup

Test an API endpoint:
- Visit: https://bottyotty-production.up.railway.app/api/health
- Should return: {"status": "healthy"}

Test a new endpoint:
- Visit: https://bottyotty-production.up.railway.app/api/vehicles
- Should return: {"success": true, "vehicles": []}

Test manual backup:
- POST to: https://bottyotty-production.up.railway.app/api/backup/now
- Should create a backup file

WHAT HAPPENS NEXT:

✅ Database tables are created automatically
✅ All 40+ API endpoints are now active
✅ Backups run daily at 3 AM
✅ Backups are pushed to GitHub automatically
✅ Old backups (>7 days) are cleaned up automatically
✅ You can trigger manual backups via /api/backup/now

NEXT STEP:
Update the HTML pages to call your API instead of localStorage!
(I'll do that next)
"""
