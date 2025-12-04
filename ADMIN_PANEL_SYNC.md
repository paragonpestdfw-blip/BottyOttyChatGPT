# Admin Panel ↔️ Bot Sync Feature

## Overview
The Admin Panel can now push configuration changes directly to the Discord bot in real-time through the `/api/admin-config` endpoint.

## How It Works

### 1. Admin Panel Configuration
The Admin Panel provides UI sections to manage:

- **🧵 Thread IDs** - Named Discord thread references
- **📺 Channel IDs** - Named Discord channel references
- **👤 User IDs** - Discord user ID mappings
- **🎯 Reactions** - Custom reaction assignments for auto-task-assignment
- **👥 Team Members** - Team member Discord ID associations
- **📂 Categories** - Task categories
- **🏢 Departments** - Team departments
- **👔 Roles** - User roles and permissions

### 2. Saving Configuration
When you click **"💾 Save Configuration to Bot"** in the Admin Panel:

1. Admin Panel collects all configuration data
2. Sends POST request to `/api/admin-config` endpoint
3. Bot receives and updates its `CONFIG` dictionary
4. Configuration saves to `bot_config.json` for persistence
5. Success notification appears: "✅ Configuration synced to bot successfully!"

### 3. Auto-Sync Feature
The Admin Panel has an **Auto-Sync** toggle:
- When enabled, configuration automatically pushes to bot at regular intervals
- Default sync interval: 30 seconds (configurable)
- Find in: Admin Panel → Bot Configuration section

## Configuration Structure

### Discord Config
```javascript
{
  "discordConfig": {
    "threads": {
      "Sales Thread": "1234567890123456",
      "Support Thread": "2345678901234567"
    },
    "channels": {
      "General": "3456789012345678",
      "Logs": "4567890123456789"
    },
    "users": {
      "John": "5678901234567890",
      "Jane": "6789012345678901"
    }
  }
}
```

### Channels
```javascript
{
  "channels": {
    "pools": [
      { "name": "SMOT Pool", "id": "1440575030118449152" }
    ],
    "personal": [
      { "user": "Caleb", "id": "1234567890123456" }
    ]
  }
}
```

### Users
```javascript
{
  "users": {
    "authorized": [1228184859772588042, 1189283572100645005],
    "campfire": [931331954220101632, 928725439059464222]
  }
}
```

### Reactions
```javascript
{
  "reactions": [
    {
      "emoji": "⭐",
      "user": "Ash",
      "userId": 289212918615244801,
      "channelId": "1234567890123456"
    }
  ]
}
```

## Using Discord Configuration in Bot

### Accessing Stored IDs
```python
# In your bot commands, access the stored Discord IDs:

# Get a channel ID by name
channel_id = CONFIG.get('discord_channels', {}).get('General')
if channel_id:
    channel = bot.get_channel(int(channel_id))

# Get a user ID by name
user_id = CONFIG.get('discord_users', {}).get('John')
if user_id:
    user = await bot.fetch_user(int(user_id))

# Get a thread ID by name
thread_id = CONFIG.get('discord_threads', {}).get('Sales Thread')
if thread_id:
    thread = bot.get_channel(int(thread_id))
```

### Example Bot Command Using Config
```python
@bot.command()
async def notify_general(ctx, *, message):
    """Send a notification to the General channel"""
    channel_id = CONFIG.get('discord_channels', {}).get('General')

    if not channel_id:
        await ctx.send("❌ General channel not configured in Admin Panel")
        return

    channel = bot.get_channel(int(channel_id))
    if channel:
        await channel.send(f"📢 {message}")
        await ctx.send("✅ Notification sent!")
    else:
        await ctx.send("❌ Channel not found")
```

## File Persistence

### bot_config.json
- Created automatically when you save from Admin Panel
- Stores complete configuration for bot restart
- Location: `/path/to/BottyOttyChatGPT/bot_config.json`
- Format: JSON

### Loading on Startup
The bot automatically loads `bot_config.json` on startup (if it exists):
```python
# In main.py around line 1059
if os.path.exists('bot_config.json'):
    with open('bot_config.json', 'r') as f:
        saved_config = json.load(f)
        # Update CONFIG with saved values
```

## Troubleshooting

### "Failed to sync to bot"
**Cause:** API URL not configured or bot is offline

**Solution:**
1. Check Admin Panel → Bot Configuration → API URL
2. Verify bot is running: `railway logs` or check hosting platform
3. Ensure API URL matches your deployment (e.g., `https://bottyotty-production.up.railway.app`)

### Configuration not persisting
**Cause:** bot_config.json write permissions issue

**Solution:**
1. Check file permissions in deployment directory
2. On Railway/Heroku, ensure persistent storage is configured
3. Check bot logs for: "⚠️ Failed to save config to file"

### Changes not reflecting in bot
**Cause:** Bot needs restart or API endpoint not called

**Solution:**
1. Verify "✅ Configuration synced to bot successfully!" message appears
2. Check Network tab in browser DevTools for successful POST to `/api/admin-config`
3. Restart bot if needed: `railway restart` or equivalent

## API Endpoint Reference

### POST /api/admin-config

**Description:** Receive and update bot configuration from Admin Panel

**Request Body:**
```json
{
  "appearance": { ... },
  "botConfig": {
    "autoSync": true,
    "syncInterval": 30,
    "apiUrl": "https://...",
    "messages": { ... }
  },
  "users": {
    "authorized": [...],
    "campfire": [...]
  },
  "channels": {
    "pools": [...],
    "personal": [...]
  },
  "reactions": [...],
  "categories": [...],
  "departments": [...],
  "roles": [...],
  "discordConfig": {
    "threads": { ... },
    "channels": { ... },
    "users": { ... }
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Configuration updated successfully",
  "timestamp": "2025-12-04T12:00:00.000Z"
}
```

**Error Response:**
```json
{
  "error": "Error message"
}
```

## Best Practices

1. **Test Before Saving**
   - Verify Discord IDs are correct before saving to bot
   - Use Discord Developer Mode to copy IDs (Settings → Advanced → Developer Mode)

2. **Regular Backups**
   - Download `bot_config.json` periodically
   - Export Admin Panel localStorage as backup

3. **Gradual Updates**
   - Update one section at a time
   - Test each change before moving to next section

4. **Monitor Sync Status**
   - Watch for success/error notifications
   - Check bot logs after major config changes

5. **Document Custom Mappings**
   - Keep a reference of what each Discord ID represents
   - Document special reaction assignments

## Admin Panel UI Locations

### Discord Configuration Section
Navigate to: **Admin Panel** → Scroll to **"Discord ID Configuration"** section

This section contains:
- **🧵 Thread IDs** accordion
- **📺 Channel IDs** accordion
- **👤 User IDs** accordion (if implemented)

### Bot Configuration Section
Navigate to: **Admin Panel** → **"Bot Configuration"** section

Settings:
- ✅ Automatically sync with Discord bot (toggle)
- ⏱️ Sync Interval (seconds slider)
- 🔗 API URL (text input)

### Save Button
Located at: **Bottom of Admin Panel** → **"💾 Save Configuration to Bot"** button

## Security Considerations

1. **API Security**
   - Consider adding API key authentication
   - Restrict API access to trusted IPs if possible
   - Use HTTPS only (never HTTP)

2. **Discord Token Protection**
   - Never store bot token in Admin Panel
   - Keep `DISCORD_BOT_TOKEN` in environment variables only

3. **Access Control**
   - Restrict Admin Panel access to authorized personnel
   - Use IP whitelisting if hosting publicly

## Future Enhancements

Potential additions to consider:
- [ ] API key authentication for `/api/admin-config`
- [ ] Config versioning and rollback
- [ ] Validation of Discord IDs before saving
- [ ] Live preview of config changes
- [ ] Import/Export config files
- [ ] Audit log of config changes

---

*Last updated: December 2025*
*Related files: `main.py`, `Admin Panel v18.html`*
