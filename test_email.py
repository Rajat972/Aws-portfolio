#!/usr/bin/env python3
"""
Diagnostic Script to test real email sending via SMTP.
Usage: python test_email.py [recipient_email]
"""

import sys
import os
from dotenv import load_dotenv
from app.notifier import send_notification_email, send_thank_you_email_to_visitor

load_dotenv()

def main():
    recipient = sys.argv[1] if len(sys.argv) > 1 else "rajatrajput076@gmail.com"

    print("==========================================================================")
    print(" [DIAGNOSTIC SMTP EMAIL TESTER]")
    print("==========================================================================")
    print(f"SMTP_SERVER    : '{os.getenv('SMTP_SERVER')}'")
    print(f"SMTP_PORT      : '{os.getenv('SMTP_PORT')}'")
    print(f"SENDER_EMAIL   : '{os.getenv('SENDER_EMAIL')}'")
    print(f"SENDER_PASSWORD: '{'***** (Configured)' if os.getenv('SENDER_PASSWORD') else 'MISSING / EMPTY (Preview Mode Active)'}'")
    print(f"TEST RECIPIENT : '{recipient}'")
    print("--------------------------------------------------------------------------")

    if not os.getenv('SENDER_PASSWORD'):
        print("\n[!] WARNING: SENDER_PASSWORD is empty in your .env file!")
        print("Because password is missing, the system is in PREVIEW MODE.")
        print("Emails are written to notifications.log instead of sending to real inboxes.")
        print("\nTo send real emails to inboxes:")
        print("1. Get a 16-character App Password from Google: https://myaccount.google.com/apppasswords")
        print("2. Put it in .env: SENDER_PASSWORD=your_16_char_app_password")
        print("==========================================================================")
        return

    print("Attempting to send REAL email via SMTP to:", recipient)

    test_data = {
        "id": 999,
        "name": "Test Visitor",
        "email": recipient,
        "subject": "Testing Portfolio Auto-Responder",
        "message": "This is a test message to verify visitor email delivery.",
        "created_at": "2026-09-30 00:00:00"
    }

    res_owner = send_notification_email(test_data)
    print("\n1. Owner Notification Result:", res_owner)

    res_visitor = send_thank_you_email_to_visitor(test_data)
    print("\n2. Visitor Thank-You Result:", res_visitor)
    print("==========================================================================")

if __name__ == "__main__":
    main()
