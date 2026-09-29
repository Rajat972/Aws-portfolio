import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Setup logging for notifications
logger = logging.getLogger("portfolio_notifier")
logger.setLevel(logging.INFO)

def send_notification_email(contact_data: dict) -> dict:
    """
    Sends an email notification to the portfolio owner when a new contact form submission arrives.
    If SMTP variables are not set in .env, falls back to logging/preview mode cleanly.
    """
    smtp_server = os.getenv("SMTP_SERVER", "").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SENDER_EMAIL", "").strip()
    sender_password = os.getenv("SENDER_PASSWORD", "").strip()
    receiver_email = os.getenv("RECEIVER_EMAIL", sender_email).strip()

    name = contact_data.get("name", "N/A")
    email = contact_data.get("email", "N/A")
    subject = contact_data.get("subject", "New Portfolio Inquiry")
    message = contact_data.get("message", "")
    created_at = contact_data.get("created_at", "")

    email_body = f"""
NEW CONTACT INQUIRY FROM YOUR PORTFOLIO WEBSITE
------------------------------------------------
Received At : {created_at}
Sender Name : {name}
Sender Email: {email}
Subject     : {subject}

Message:
------------------------------------------------
{message}
------------------------------------------------
    """

    # Check if SMTP credentials are provided
    if not smtp_server or not sender_email or not sender_password:
        preview_notice = (
            "\n=======================================================\n"
            "   [LOCAL PREVIEW MODE - EMAIL NOTIFICATION TRIGGERED]\n"
            "=======================================================\n"
            f"TO: {receiver_email if receiver_email else '[Owner Email Not Configured]'}\n"
            f"FROM: {sender_email if sender_email else 'noreply@portfolio.local'}\n"
            f"SUBJECT: [Portfolio Contact] {subject} from {name}\n"
            f"{email_body}\n"
            "NOTE: To send real emails, set SMTP_SERVER, SENDER_EMAIL, and SENDER_PASSWORD in your .env file.\n"
            "=======================================================\n"
        )
        try:
            print(preview_notice)
        except Exception:
            print(preview_notice.encode("ascii", "ignore").decode("ascii"))
        
        # Save to local log file as well
        log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "notifications.log")
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(preview_notice)
            
        return {
            "status": "preview_mode",
            "message": "Notification logged to server output & notifications.log (SMTP credentials not configured in .env)."
        }

    # Prepare HTML & Text MIME Message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📬 Portfolio Contact: {subject} from {name}"
    msg["From"] = f"{name} via Portfolio <{sender_email}>"
    msg["To"] = receiver_email
    msg["Reply-To"] = email

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f6f9; padding: 20px; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #e1e4e8; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
          <div style="background: #2563eb; color: #ffffff; padding: 20px; text-align: center;">
            <h2 style="margin: 0; font-size: 20px;">New Portfolio Inquiry</h2>
          </div>
          <div style="padding: 24px;">
            <p style="margin-top: 0; color: #64748b; font-size: 14px;">You received a new message via your portfolio contact form on <strong>{created_at}</strong>.</p>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
              <tr>
                <td style="padding: 8px 0; font-weight: bold; color: #475569; width: 120px;">Visitor Name:</td>
                <td style="padding: 8px 0; color: #0f172a;">{name}</td>
              </tr>
              <tr>
                <td style="padding: 8px 0; font-weight: bold; color: #475569;">Email Address:</td>
                <td style="padding: 8px 0;"><a href="mailto:{email}" style="color: #2563eb; text-decoration: none;">{email}</a></td>
              </tr>
              <tr>
                <td style="padding: 8px 0; font-weight: bold; color: #475569;">Subject:</td>
                <td style="padding: 8px 0; color: #0f172a;">{subject}</td>
              </tr>
            </table>
            
            <div style="background: #f8fafc; border-left: 4px solid #2563eb; padding: 16px; border-radius: 4px; margin-top: 16px;">
              <h4 style="margin: 0 0 8px 0; color: #1e293b;">Message Content:</h4>
              <p style="margin: 0; white-space: pre-wrap; color: #334155; line-height: 1.6;">{message}</p>
            </div>
            
            <div style="margin-top: 24px; text-align: center;">
              <a href="mailto:{email}?subject=Re: {subject}" style="display: inline-block; background-color: #2563eb; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: bold;">Reply to Visitor</a>
            </div>
          </div>
        </div>
      </body>
    </html>
    """

    msg.attach(MIMEText(email_body, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

        logger.info(f"Email sent successfully to {receiver_email} for submission ID {contact_data.get('id')}")
        return {"status": "success", "message": f"Notification email sent to {receiver_email}"}
    except Exception as e:
        error_msg = f"Failed to send email notification: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}
