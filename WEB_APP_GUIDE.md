# Quick Start Guide - Web App

## Running Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask app:**
   ```bash
   python app.py
   ```

3. **Open in browser:**
   ```
   http://localhost:5000
   ```

## Usage

1. Enter a course ID (e.g., `61954`)
2. Click "הוסף" (Add)
3. Watch the schedule populate automatically!
4. Add more courses to build your complete schedule
5. Remove courses by clicking "הסר" (Remove)

## Features

- ✅ Real-time schedule updates
- ✅ Color-coded courses
- ✅ Responsive design (works on mobile)
- ✅ No page refresh needed
- ✅ Session-based (each user gets their own schedule)

## Deployment to Render.com (Free)

1. **Create account** at [render.com](https://render.com)

2. **Create new Web Service**
   - Connect your GitHub repository
   - Or upload code directly

3. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Add to requirements.txt: `gunicorn==21.2.0`

4. **Deploy!**
   - Your app will be live at `https://your-app-name.onrender.com`

## Troubleshooting

**Port already in use:**
```bash
# Change port in app.py:
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Module not found:**
```bash
pip install -r requirements.txt
```

**CORS errors:**
- Already handled with flask-cors ✅
