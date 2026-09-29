# Portfolio Website with SQLite DB & Email Notification System

A modern, responsive portfolio application featuring an interactive visitor contact form box. Every submission is:
1. **Saved in a local SQLite database** (`portfolio.db`)
2. **Dispatched as an email notification** to your email inbox (via SMTP or logged in preview mode)
3. **Viewable in real-time** via the built-in "Stored Messages" database drawer

---

## 🛠️ Tech Stack

- **Backend**: Python 3, FastAPI, Uvicorn
- **Database**: SQLite 3 (native, zero extra database server setup required)
- **Email Dispatcher**: Python `smtplib` + `email.mime` (Supports Gmail, Outlook, Yahoo, or custom SMTP)
- **Frontend**: HTML5, CSS3 (Glassmorphism Dark Theme), Modern ES6 JavaScript

---

## 🚀 How to Run the Portfolio Server

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
Run Uvicorn from the project root directory:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 3. Open in Browser
Visit [http://localhost:8000](http://localhost:8000) in your web browser.

---

## 📬 How to Configure Email Notifications (.env)

By default, the application runs in **Local Preview Mode** (messages are saved to SQLite and printed in the terminal + saved to `notifications.log`).

To receive real email notifications whenever a visitor writes in your contact box:

1. Open `.env` (or copy `.env.example` to `.env`)
2. Add your SMTP details (For Gmail):
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=yourname@gmail.com
   SENDER_PASSWORD=your_gmail_app_password
   RECEIVER_EMAIL=yourname@gmail.com
   ```
> 💡 **Tip for Gmail Users**:
> Generate an **App Password** from your [Google Account Security Settings](https://myaccount.google.com/apppasswords) under *2-Step Verification* -> *App Passwords*. Use this 16-character password as `SENDER_PASSWORD`.

---

## 📂 Project Structure

```
portfolio/
├── app/
│   ├── __init__.py
│   ├── database.py       # SQLite connection and CRUD queries
│   ├── notifier.py       # Email notification dispatcher & preview logger
│   └── main.py           # FastAPI routes & static file mounting
├── static/
│   ├── index.html        # Portfolio layout with contact form box
│   ├── styles.css        # Responsive dark glassmorphism styling
│   └── script.js         # Async form handling & DB inbox modal
├── portfolio.db          # Auto-created SQLite database file
├── notifications.log     # Auto-created preview notification log
├── .env                  # Local environment configuration
├── .env.example          # Environment variable template
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
```
