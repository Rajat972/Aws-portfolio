#!/usr/bin/env python3
"""
Secure CLI Tool to view stored portfolio messages directly on your server.
Usage: python view_db.py
"""

from app.database import get_all_contact_messages

def main():
    messages = get_all_contact_messages(limit=100)
    print("==========================================================================")
    print(f" 🗄️  PORTFOLIO SQLITE DATABASE INBOX (Total Entries: {len(messages)})")
    print("==========================================================================")

    if not messages:
        print("No messages found in database yet.")
        print("==========================================================================")
        return

    for msg in messages:
        print(f"\n[ID #{msg['id']}]  Received At: {msg['created_at']}")
        print(f"Sender Name : {msg['name']}")
        print(f"Sender Email: {msg['email']}")
        print(f"Subject     : {msg['subject']}")
        print(f"IP Address  : {msg['ip_address'] or 'N/A'}")
        print(f"Status      : {'Emailed' if msg['notified_via_email'] else 'Stored in DB'}")
        print("--------------------------------------------------------------------------")
        print(f"Message:\n{msg['message']}")
        print("==========================================================================")

if __name__ == "__main__":
    main()
