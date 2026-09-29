from flask import Flask, request, jsonify, send_from_directory
import os
import threading
import re

from app.database import init_db, save_contact_message, get_all_contact_messages, update_email_notified_status
from app.notifier import send_notification_email

static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app = Flask(__name__, static_folder=static_folder)

# Initialize database
init_db()

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

# Admin Secret Key for protecting production database API
ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "").strip()

def async_email_worker(saved_record: dict):
    """Background thread function for sending notification email without blocking response."""
    res = send_notification_email(saved_record)
    if res.get("status") == "success":
        update_email_notified_status(saved_record["id"], True)

@app.route("/", methods=["GET"])
def index():
    """Serve portfolio frontend index.html."""
    return send_from_directory(static_folder, "index.html")

@app.route("/static/<path:filename>", methods=["GET"])
def serve_static(filename):
    """Serve static CSS, JS, and asset files."""
    return send_from_directory(static_folder, filename)

@app.route("/api/contact", methods=["POST"])
def handle_contact_submission():
    """
    Receives visitor details from portfolio contact box, stores in SQLite DB, 
    and triggers background email notification.
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"success": False, "detail": "Invalid or missing JSON payload"}), 400

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    subject = str(data.get("subject", "Portfolio Contact")).strip()
    message = str(data.get("message", "")).strip()

    # Input validation
    if len(name) < 2:
        return jsonify({"success": False, "detail": "Name must be at least 2 characters long."}), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({"success": False, "detail": "Please provide a valid email address."}), 400

    if len(subject) < 2:
        return jsonify({"success": False, "detail": "Subject must be at least 2 characters long."}), 400

    if len(message) < 5:
        return jsonify({"success": False, "detail": "Message must be at least 5 characters long."}), 400

    try:
        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
        user_agent = request.headers.get("User-Agent", "Unknown")

        # 1. Save entry to SQLite DB
        saved_record = save_contact_message(
            name=name,
            email=email,
            subject=subject,
            message=message,
            ip_address=ip_address,
            user_agent=user_agent
        )

        # 2. Trigger asynchronous email notification in background thread
        email_thread = threading.Thread(target=async_email_worker, args=(saved_record,))
        email_thread.daemon = True
        email_thread.start()

        return jsonify({
            "success": True,
            "message": "Thank you! Your details have been received and saved. I will get back to you soon.",
            "data": {
                "id": saved_record["id"],
                "created_at": saved_record["created_at"]
            }
        }), 201

    except Exception as e:
        return jsonify({"success": False, "detail": f"Database error: {str(e)}"}), 500

@app.route("/api/messages", methods=["GET"])
def list_contact_messages():
    """
    Protected API endpoint to view contact messages.
    Requires ADMIN_SECRET_KEY in header or query parameter. 
    Public access without secret is forbidden on production.
    """
    provided_key = request.headers.get("X-Admin-Key") or request.args.get("admin_key")

    if not ADMIN_SECRET_KEY or provided_key != ADMIN_SECRET_KEY:
        return jsonify({"success": False, "detail": "Access forbidden: Admin authentication required."}), 403

    try:
        limit = request.args.get("limit", default=50, type=int)
        messages = get_all_contact_messages(limit=limit)
        return jsonify({
            "success": True,
            "count": len(messages),
            "messages": messages
        }), 200
    except Exception as e:
        return jsonify({"success": False, "detail": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
