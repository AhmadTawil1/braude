# Tanzim Braude - Deployment Guide

This guide covers deploying your Flask web application to the cloud so anyone can access it online.

## 🚀 Recommended: Deploy to Render.com (Free)

Render.com offers free hosting for web applications with automatic HTTPS.

### Prerequisites
- GitHub account
- Render.com account (free)

### Step 1: Prepare Your Repository

1. **Create `requirements.txt` in the root directory:**
   ```bash
   cd c:\Users\tawil\Python\braude-scheduler
   pip freeze > requirements.txt
   ```

2. **Create `render.yaml` in the root directory:**
   ```yaml
   services:
     - type: web
       name: tanzim-braude
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn app:app
       envVars:
         - key: PYTHON_VERSION
           value: 3.11.0
   ```

3. **Add `gunicorn` to requirements.txt:**
   ```bash
   echo gunicorn >> requirements.txt
   ```

4. **Update `app.secret_key` in `app.py`:**
   ```python
   import os
   app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
   ```

### Step 2: Push to GitHub

```bash
cd c:\Users\tawil\Python\braude-scheduler
git init
git add .
git commit -m "Initial commit - Tanzim Braude"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 3: Deploy on Render

1. Go to [render.com](https://render.com) and sign in with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `tanzim-braude`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Add environment variable:
   - **Key:** `SECRET_KEY`
   - **Value:** Generate a random string (e.g., `python -c "import secrets; print(secrets.token_hex(32))"`)
6. Click **"Create Web Service"**

### Step 4: Access Your App

- Your app will be live at: `https://tanzim-braude.onrender.com`
- First deployment takes 5-10 minutes
- Free tier sleeps after 15 minutes of inactivity (wakes up automatically when accessed)

---

## Alternative: Deploy to Heroku

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. **Create `Procfile` in root:**
   ```
   web: gunicorn app:app
   ```

2. **Login and create app:**
   ```bash
   heroku login
   heroku create tanzim-braude
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set SECRET_KEY=<your-secret-key>
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

5. **Open app:**
   ```bash
   heroku open
   ```

---

## Alternative: Deploy to PythonAnywhere

### Steps

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Go to **Web** tab → **Add a new web app**
3. Choose **Flask** framework
4. Upload your code via **Files** tab or use Git
5. Configure WSGI file to point to your `app.py`
6. Reload the web app

**Free tier:** `<username>.pythonanywhere.com`

---

## Local Network Deployment (For Testing)

Run the app on your local network so others can access it:

```bash
python app.py
```

Then access from other devices on the same network:
- Find your IP: `ipconfig` (look for IPv4 Address)
- Access at: `http://<your-ip>:5000`

**Note:** Only works while your computer is running and on the same network.

---

## Production Checklist

Before deploying to production:

- [ ] Change `app.secret_key` to a secure random value
- [ ] Set `debug=False` in `app.run()`
- [ ] Add error handling for failed course fetches
- [ ] Consider adding rate limiting
- [ ] Add analytics (optional)
- [ ] Test on mobile devices
- [ ] Add favicon
- [ ] Set up custom domain (optional)

---

## Monitoring & Maintenance

### Render.com
- View logs in Render dashboard
- Automatic HTTPS
- Auto-deploys on git push

### Heroku
- View logs: `heroku logs --tail`
- Monitor dyno usage in dashboard

---

## Cost Comparison

| Platform | Free Tier | Limitations | Best For |
|----------|-----------|-------------|----------|
| **Render** | ✅ Yes | Sleeps after 15min inactivity | Recommended |
| **Heroku** | ✅ Yes (550 hours/month) | Sleeps after 30min inactivity | Good alternative |
| **PythonAnywhere** | ✅ Yes | Limited CPU/bandwidth | Simple apps |
| **Railway** | ✅ $5 credit/month | Pay after credit | Flexible |

---

## Need Help?

- **Render Docs:** https://render.com/docs
- **Flask Deployment:** https://flask.palletsprojects.com/en/latest/deploying/
- **Gunicorn Docs:** https://gunicorn.org/

**Ready to deploy? Start with Render.com - it's the easiest!**
