# 🚀 Deployment Guide - PythonAnywhere

Step-by-step instructions to deploy SEO AIditor on PythonAnywhere (free hosting).

**Time needed:** 15-20 minutes
**Cost:** $0/month (free tier)
**Result:** Live at `https://yourusername.pythonanywhere.com`

---

## 📋 Prerequisites

- [x] GitHub account with this repository
- [x] Email address for PythonAnywhere registration

That's it! No credit card needed for free tier.

---

## Step 1: Create PythonAnywhere Account (3 min)

1. Go to https://www.pythonanywhere.com

2. Click **"Start running Python online in less than a minute!"**

3. Fill out registration form:
   - **Username:** Choose carefully - this becomes your URL (`username.pythonanywhere.com`)
   - **Email:** Your email
   - **Password:** Strong password

   **Username suggestions:**
   - `seoaiditor` → https://seoaiditor.pythonanywhere.com
   - `yourname-seo` → https://yourname-seo.pythonanywhere.com
   - `nitolic` → https://nitolic.pythonanywhere.com

4. **Verify email** (check inbox/spam)

5. **Log in** to PythonAnywhere dashboard

---

## Step 2: Clone Repository from GitHub (5 min)

### 2.1 Open Bash Console

1. In PythonAnywhere dashboard, click **"Consoles"** tab
2. Click **"Bash"** (under "Start a new console")
3. You'll see a terminal window

### 2.2 Clone the Repository

In the Bash console, type:

```bash
git clone https://github.com/maciusman/seo-aiditor.git
cd seo-aiditor
```

**Output should show:**
```
Cloning into 'seo-aiditor'...
remote: Enumerating objects...
```

### 2.3 Install Python Dependencies

```bash
pip3.10 install --user -r requirements.txt
```

**This will take 2-3 minutes.** You'll see:
```
Collecting Flask>=3.0.0
Collecting flask-cors>=4.0.0
...
Successfully installed ...
```

---

## Step 3: Create Web App (5 min)

### 3.1 Start Web App Creation

1. Click **"Web"** tab (top of dashboard)
2. Click **"Add a new web app"** button
3. Click **"Next"** on domain confirmation (`username.pythonanywhere.com`)
4. Select **"Manual configuration"** (NOT Flask wizard!)
5. Choose **Python 3.10**
6. Click **"Next"**

### 3.2 Configure Source Code

In the **"Code"** section:

1. **Source code:**
   ```
   /home/yourusername/seo-aiditor
   ```
   *(Replace `yourusername` with YOUR username!)*

2. **Working directory:**
   ```
   /home/yourusername/seo-aiditor
   ```

### 3.3 Configure WSGI File

1. In **"Code"** section, find **"WSGI configuration file"**
2. Click the link (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. **Delete ALL existing content**
4. **Paste this code:**

```python
import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/seo-aiditor'  # ← CHANGE yourusername!
if path not in sys.path:
    sys.path.append(path)

# Set environment variable for production mode
os.environ['PRODUCTION'] = 'true'

# Import Flask app
from app import app as application
```

5. **IMPORTANT:** Replace `yourusername` with your actual PythonAnywhere username!
6. Click **"Save"** (top right)

---

## Step 4: Configure Static Files (2 min)

In the **"Static files"** section:

**Add these three mappings:**

### Mapping 1: Logo
- **URL:** `/logo.png`
- **Directory:** `/home/yourusername/seo-aiditor/logo.png`

### Mapping 2: Static folder (if exists)
- **URL:** `/static/`
- **Directory:** `/home/yourusername/seo-aiditor/static`

### Mapping 3: Frontend (index.html)
- **URL:** `/`
- **Directory:** `/home/yourusername/seo-aiditor/index.html`

Click **checkmark ✓** to save each mapping.

---

## Step 5: Reload Web App (1 min)

1. Scroll to the **top** of the Web tab
2. Click the big green **"Reload"** button
3. Wait 5-10 seconds for reload to complete

---

## Step 6: Test Your Deployment! 🎉

1. Click the link at the top: `https://yourusername.pythonanywhere.com`
2. You should see the SEO AIditor interface!

### First Use:

1. **Modal will appear:** "🔑 API Keys Required"
2. You'll need:
   - **Gemini API key** (required) → [Get it here](https://aistudio.google.com/apikey)
   - **PageSpeed key** (optional) → [Get it here](https://console.cloud.google.com/apis/library/pagespeedonline.googleapis.com)

3. See **[GETTING_API_KEYS.md](GETTING_API_KEYS.md)** for detailed instructions

4. Enter keys, check "Remember keys", click "Start Analysis"

5. **Run your first audit!** 🚀

---

## 🔄 How to Update Your App (Future Changes)

When you pull new updates from GitHub:

### Method 1: Bash Console (Recommended)

```bash
cd ~/seo-aiditor
git pull origin master
```

Then: **Web tab → Reload button**

### Method 2: Files Tab

1. Navigate to `/home/yourusername/seo-aiditor`
2. Manually upload changed files
3. **Web tab → Reload button**

**Always reload** after changes!

---

## ⚠️ Troubleshooting

### Error: "Something went wrong"

**Solution:**
1. Web tab → Click **"Error log"** link
2. Read the error message
3. Common issues:
   - Wrong path in WSGI file (check `/home/yourusername/...`)
   - Missing dependencies (re-run `pip install`)
   - Python version mismatch (use 3.10)

### Error: "ImportError: No module named 'app'"

**Problem:** Wrong path in WSGI file

**Solution:**
1. Open WSGI configuration file
2. Check `path = '/home/yourusername/seo-aiditor'`
3. Make sure `yourusername` is YOUR actual username
4. Save → Reload

### Static files (logo, CSS) not loading

**Problem:** Static files not configured

**Solution:**
1. Web tab → "Static files" section
2. Add all three mappings (see Step 4)
3. Reload

### "App not loading" / Blank page

**Check:**
1. Is `index.html` in the root directory?
2. Is static files mapping `/` → `/home/yourusername/seo-aiditor/index.html` correct?
3. Check error log for details

### API keys modal not appearing

**This is normal for production mode!**

- Online version requires user to provide keys
- Your local version uses `config_local.py` (no modal)

### Free tier limitations

**PythonAnywhere free tier:**
- ⚠️ **HTTP only** (no HTTPS without upgrade)
- ⚠️ **App sleeps** after 3 months of no login (easy restart)
- ⚠️ **Limited CPU** (sufficient for SEO audits)

**Upgrade ($5/month) for:**
- ✅ HTTPS (secure SSL)
- ✅ Custom domain
- ✅ More CPU time
- ✅ Always-on (no sleep)

---

## 🔐 Security Best Practices

### On PythonAnywhere:

1. **No API keys needed on server**
   - Users provide their own keys
   - Keys never stored server-side

2. **Keep GitHub repo private** if you add:
   - Database credentials
   - Payment processing
   - User authentication

3. **HTTPS recommended**
   - Free tier = HTTP only
   - $5/month upgrade = HTTPS
   - Important for API key security

### For Users:

1. **Educate users:**
   - Link to [GETTING_API_KEYS.md](GETTING_API_KEYS.md)
   - Explain keys are client-side only
   - Recommend sessionStorage (default)

2. **Monitor usage:**
   - PythonAnywhere dashboard shows traffic
   - Gemini API console shows quota usage

---

## 📊 Monitoring & Maintenance

### Check App Health:

1. **Access logs:** Web tab → "Access log"
   - See who's visiting
   - Track popular pages

2. **Error logs:** Web tab → "Error log"
   - Python exceptions
   - Flask errors
   - Import problems

3. **Bash console:**
   ```bash
   cd ~/seo-aiditor
   python app.py  # Test locally on PA
   ```

### Maintenance Schedule:

**Monthly:**
- [ ] Log in to PythonAnywhere (prevent sleep)
- [ ] Check error logs
- [ ] `git pull` for updates

**Quarterly:**
- [ ] Review Gemini API pricing
- [ ] Check PythonAnywhere limits
- [ ] Update dependencies if needed

---

## 🚀 Going Further

### Custom Domain (Requires Paid Plan)

1. Upgrade to PythonAnywhere paid plan ($5/month)
2. Web tab → "Set up custom domain"
3. Point your domain's CNAME to PA servers
4. Enable HTTPS (automatic Let's Encrypt)

### Add User Analytics

```html
<!-- In index.html, before </head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Add Rate Limiting (Future)

If abuse becomes a problem:
- Flask-Limiter extension
- Limit audits per IP
- Captcha for excessive use

---

## 📞 Support

### PythonAnywhere Help:

- **Forum:** https://www.pythonanywhere.com/forums/
- **Help pages:** https://help.pythonanywhere.com/
- **Email:** support@pythonanywhere.com

### SEO AIditor Issues:

- **GitHub Issues:** https://github.com/maciusman/seo-aiditor/issues
- **Documentation:** See README.md

---

## ✅ Deployment Checklist

- [ ] Created PythonAnywhere account
- [ ] Cloned repository via Bash
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Created web app (Manual config, Python 3.10)
- [ ] Configured source code path
- [ ] Edited WSGI file with correct path
- [ ] Set `PRODUCTION=true` in WSGI
- [ ] Added static files mappings
- [ ] Reloaded web app
- [ ] Tested app at `yourusername.pythonanywhere.com`
- [ ] Got Gemini API key
- [ ] Ran first successful audit 🎉

---

**Congratulations!** 🎊 Your SEO AIditor is now live and accessible to anyone with the link!

Share it: `https://yourusername.pythonanywhere.com`
