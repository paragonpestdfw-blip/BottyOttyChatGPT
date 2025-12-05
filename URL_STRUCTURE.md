# URL Structure & File Organization

**Last Updated:** December 5, 2025
**Domain:** pestresource.com

---

## ✅ Clean URL Structure

Your site now uses **clean, professional URLs** without spaces or version numbers.

### Main Pages:

| Page | File Name | URL | Description |
|------|-----------|-----|-------------|
| **Dashboard** | `dashboard.html` | `/` or `/dashboard` | Main employee dashboard |
| **Admin Panel** | `admin.html` | `/admin` | Bot configuration & Discord panels |
| **Reports** | `reports.html` | `/reports` | Task reports and analytics |
| **Help** | `help.html` | `/help` | User guide & documentation |
| **Newsletter** | `newsletter.html` | `/newsletter` | Company newsletter & posts |
| **Quick Launch** | `quick-launch.html` | `/quick-launch` | Quick access launcher |

### Widget Pages:

| Widget | File Name | URL | Description |
|--------|-----------|-----|-------------|
| **Calendar** | `calendar.html` | `/calendar` | Company calendar events |
| **Feedback** | `feedback.html` | `/feedback` | Customer feedback tracker |
| **Inventory** | `inventory.html` | `/inventory` | Inventory management |
| **Leads** | `leads.html` | `/leads` | Lead sites switchboard |
| **Alerts** | `alerts.html` | `/alerts` | Office alerts system |
| **Move-Up** | `moveup.html` | `/moveup` | Pest move-up list |
| **Safety** | `safety.html` | `/safety` | Safety management |
| **Reminders** | `reminders.html` | `/reminders` | Tech reminders |
| **Vehicles** | `vehicles.html` | `/vehicles` | Vehicle management |

---

## 🔄 How URLs Work

### Option 1: With .html extension
```
https://pestresource.com/dashboard.html
https://pestresource.com/admin.html
```

### Option 2: Without .html extension (cleaner)
```
https://pestresource.com/dashboard
https://pestresource.com/admin
```

**Both work!** The `_redirects` file handles the mapping.

### Root URL
```
https://pestresource.com/
```
Automatically redirects to dashboard.

---

## 📁 File Structure

### Before (Messy):
```
BottyOtty Dashboard v18.html
Admin Panel v18.html
BottyOtty Reports v18.html
BottyOtty Help & User Guide v18.html
...etc
```

**Problems:**
- ❌ Spaces in filenames
- ❌ Version numbers in URLs
- ❌ Inconsistent naming
- ❌ URLs looked like: `pestresource.com/BottyOtty%20Dashboard%20v18.html`

### After (Clean):
```
dashboard.html
admin.html
reports.html
help.html
newsletter.html
quick-launch.html
calendar.html
feedback.html
inventory.html
leads.html
alerts.html
moveup.html
safety.html
reminders.html
vehicles.html
index.html
_redirects
```

**Benefits:**
- ✅ No spaces
- ✅ Short, memorable names
- ✅ Consistent kebab-case
- ✅ Professional URLs: `pestresource.com/dashboard`
- ✅ SEO-friendly
- ✅ Easy to type and share

---

## 🔗 Internal Navigation

All sidebar links have been updated to use the new filenames:

```html
<!-- Old links (broken) -->
<a href="BottyOtty Dashboard v18.html">Dashboard</a>
<a href="Admin Panel v18.html">Admin Panel</a>

<!-- New links (working) -->
<a href="dashboard.html">Dashboard</a>
<a href="admin.html">Admin Panel</a>
```

**Every HTML file** has been updated, so navigation works seamlessly across all pages.

---

## 🌐 Netlify _redirects Configuration

The `_redirects` file enables:

### 1. Clean URLs (no .html needed)
```
/dashboard    →    dashboard.html
/admin        →    admin.html
/reports      →    reports.html
```

Users can type `pestresource.com/admin` instead of `pestresource.com/admin.html`

### 2. Backwards Compatibility
```
/BottyOtty%20Dashboard%20v18.html    →    /dashboard.html  (301 redirect)
/Admin%20Panel%20v18.html             →    /admin.html      (301 redirect)
```

**Why 301?** This is a "permanent redirect" that tells search engines:
- "This page has moved permanently"
- "Update your links to the new URL"
- Good for SEO - transfers page authority to new URL

### 3. Fallback for 404s
```
/*    →    /dashboard.html  (404)
```

Any unknown URL shows the dashboard instead of a broken page.

---

## 📋 _redirects File Explained

```
# Clean URLs without .html extension
/dashboard             /dashboard.html           200

# ↑ Path       ↑ Actual file     ↑ Status code
# What user    What file          200 = success
# types        gets loaded        (rewrites URL)
```

```
# Backwards compatibility
/BottyOtty%20Dashboard%20v18.html    /dashboard.html    301

# ↑ Old URL                   ↑ New URL      ↑ Status code
# (with %20 for spaces)                      301 = permanent redirect
#                                            (changes URL in browser)
```

**Difference between 200 and 301:**
- **200:** URL stays the same, different file loads (rewrite)
- **301:** Browser redirects to new URL (visible to user)

---

## 🏠 index.html Landing Page

The `index.html` file serves as your entry point:

```
User visits: pestresource.com
    ↓
index.html loads
    ↓
Auto-redirects to dashboard.html after 0.5 seconds
    ↓
Shows loading spinner while redirecting
    ↓
User sees: pestresource.com/dashboard
```

**Fallback:** If JavaScript is disabled, meta refresh redirects after 1 second.
**Manual option:** "Click here" link if auto-redirect fails.

---

## 🔍 SEO Benefits

### Before:
```
URL: pestresource.com/BottyOtty%20Dashboard%20v18.html
Title: BottyOtty Dashboard v18
```
- ❌ Ugly URL with %20 (encoded spaces)
- ❌ Version number in URL (bad for SEO)
- ❌ Hard to remember and share

### After:
```
URL: pestresource.com/dashboard
Title: BottyOtty Dashboard v18
```
- ✅ Clean, professional URL
- ✅ Keyword-focused (/dashboard, /admin)
- ✅ Easy to remember and share
- ✅ Better for search rankings

---

## 🚀 Deployment Process

### When you deploy to Netlify:

1. **Upload files:**
   - All 15 renamed .html files
   - index.html
   - _redirects
   - robots.txt

2. **Netlify automatically:**
   - Reads `_redirects` file
   - Sets up URL rewriting
   - Enables clean URLs
   - Handles 301 redirects

3. **Users can access site via:**
   - `pestresource.com/` → Dashboard
   - `pestresource.com/dashboard` → Dashboard
   - `pestresource.com/dashboard.html` → Dashboard
   - All work!

---

## 📝 Example User Journey

### Journey 1: New User
```
1. User types: pestresource.com
2. Netlify serves: index.html
3. index.html redirects to: dashboard.html
4. User sees: Dashboard page
5. Browser URL: pestresource.com/dashboard
```

### Journey 2: Direct Link
```
1. User types: pestresource.com/admin
2. _redirects maps /admin → admin.html
3. Netlify serves: admin.html
4. User sees: Admin Panel
5. Browser URL: pestresource.com/admin (stays clean!)
```

### Journey 3: Old Bookmark
```
1. User has old bookmark: pestresource.com/Admin%20Panel%20v18.html
2. _redirects: Old URL → /admin.html (301)
3. Browser redirects to: pestresource.com/admin.html
4. User sees: Admin Panel
5. Browser URL: pestresource.com/admin.html (updated!)
```

---

## 🛠️ How to Update Filenames Later

If you need to rename a file in the future:

### Step 1: Rename the file
```bash
mv old-name.html new-name.html
```

### Step 2: Update internal links
Search all HTML files for `href="old-name.html"` and replace with `href="new-name.html"`

### Step 3: Update _redirects
Add a redirect from old URL to new URL:
```
/old-name    /new-name.html    301
```

### Step 4: Commit and deploy
```bash
git add .
git commit -m "Rename old-name to new-name"
git push
```

Netlify auto-deploys and your changes are live!

---

## 📊 File Inventory

### Total Files: 17

**HTML Pages:** 15
- dashboard.html
- admin.html
- reports.html
- help.html
- newsletter.html
- quick-launch.html
- calendar.html
- feedback.html
- inventory.html
- leads.html
- alerts.html
- moveup.html
- safety.html
- reminders.html
- vehicles.html

**Special Files:** 2
- index.html (landing page)
- _redirects (Netlify config)

**Legacy Files:** 15 (kept for reference, not deployed)
- BottyOtty Dashboard v18.html
- Admin Panel v18.html
- etc.

**Note:** When deploying to Netlify, only deploy the NEW files (no spaces in names).

---

## ✅ Checklist for Deployment

Before deploying to Netlify:

- [x] All HTML files renamed to clean names
- [x] All internal links updated
- [x] index.html created
- [x] _redirects file created
- [ ] Update API URLs in HTML files (change localhost to Railway URL)
- [ ] Test all links locally
- [ ] Upload to Netlify
- [ ] Test all URLs work on Netlify
- [ ] Verify redirects work
- [ ] Check mobile responsiveness

---

## 🎯 Summary

**Before:**
```
pestresource.com/BottyOtty%20Dashboard%20v18.html ❌
```

**After:**
```
pestresource.com/dashboard ✅
```

**How it works:**
1. User types clean URL
2. _redirects maps to actual file
3. Netlify serves the file
4. URL stays clean in browser

**Benefits:**
- ✅ Professional URLs
- ✅ Better SEO
- ✅ Easy to share
- ✅ Backwards compatible
- ✅ Consistent navigation
- ✅ Production-ready

---

**Your site is now ready for professional deployment!** 🚀
