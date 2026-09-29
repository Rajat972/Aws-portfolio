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
    Sends an email notification to Rajat when a new visitor contact form submission arrives.
    If SMTP variables are not set in .env, falls back to logging/preview mode cleanly.
    """
    smtp_server = os.getenv("SMTP_SERVER", "").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SENDER_EMAIL", "").strip()
    sender_password = os.getenv("SENDER_PASSWORD", "").strip()
    receiver_email = os.getenv("RECEIVER_EMAIL", "rajatrajput076@gmail.com").strip()

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
            "   [LOCAL PREVIEW MODE - OWNER EMAIL NOTIFICATION]\n"
            "=======================================================\n"
            f"TO: {receiver_email}\n"
            f"FROM: {sender_email if sender_email else 'noreply@portfolio.local'}\n"
            f"SUBJECT: [Portfolio Contact] {subject} from {name}\n"
            f"{email_body}\n"
            "=======================================================\n"
        )
        try:
            print(preview_notice)
        except Exception:
            print(preview_notice.encode("ascii", "ignore").decode("ascii"))
        
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

        logger.info(f"Owner notification email sent to {receiver_email}")
        return {"status": "success", "message": f"Notification email sent to {receiver_email}"}
    except Exception as e:
        error_msg = f"Failed to send email notification: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}


def send_thank_you_email_to_visitor(contact_data: dict) -> dict:
    """
    Sends an automated thank-you / confirmation response email directly to the visitor
    who submitted their details into the contact form box.
    """
    smtp_server = os.getenv("SMTP_SERVER", "").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SENDER_EMAIL", "").strip()
    sender_password = os.getenv("SENDER_PASSWORD", "").strip()

    name = contact_data.get("name", "Valued Visitor")
    email = contact_data.get("email", "").strip()
    subject = contact_data.get("subject", "Portfolio Inquiry")
    message = contact_data.get("message", "")

    if not email:
        return {"status": "skipped", "message": "No visitor email provided"}

    email_body = f"""
Hi {name},

Thank you for reaching out to me through my portfolio website!

I have received your message regarding "{subject}" and I appreciate your inquiry. I am currently reviewing your message and will get back to you as soon as possible.

Here is a copy of your submitted message for your records:
--------------------------------------------------
{message}
--------------------------------------------------

Best regards,
Rajat Bandhral
DevOps Engineer
Email: rajatrajput076@gmail.com
Phone: +91 6006231663
Location: Jammu, India
    """

    if not smtp_server or not sender_email or not sender_password:
        preview_notice = (
            "\n=======================================================\n"
            "   [LOCAL PREVIEW MODE - VISITOR THANK-YOU RESPONDER]\n"
            "=======================================================\n"
            f"TO: {email}\n"
            f"FROM: Rajat Bandhral <{sender_email if sender_email else 'rajatrajput076@gmail.com'}>\n"
            f"SUBJECT: Thank you for contacting Rajat Bandhral!\n"
            f"{email_body}\n"
            "=======================================================\n"
        )
        try:
            print(preview_notice)
        except Exception:
            print(preview_notice.encode("ascii", "ignore").decode("ascii"))
        
        log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "notifications.log")
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(preview_notice)
            
        return {"status": "preview_mode", "message": "Thank-you response logged to preview mode."}

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Thank you for contacting Rajat Bandhral!"
    msg["From"] = f"Rajat Bandhral <{sender_email}>"
    msg["To"] = email

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f6f9; padding: 20px; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #e1e4e8; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
          <div style="background: #2563eb; color: #ffffff; padding: 24px; text-align: center;">
            <h2 style="margin: 0; font-size: 22px;">Thank You for Reaching Out!</h2>
          </div>
          <div style="padding: 28px;">
            <p style="font-size: 16px; color: #0f172a; margin-top: 0;">Hi <strong>{name}</strong>,</p>
            <p style="font-size: 15px; color: #334155; line-height: 1.6;">
              Thank you for contacting me through my portfolio website. I have successfully received your inquiry regarding <strong>"{subject}"</strong>.
            </p>
            <p style="font-size: 15px; color: #334155; line-height: 1.6;">
              I am currently reviewing your details and will get back to you as soon as possible.
            </p>
            
            <div style="background: #f8fafc; border-left: 4px solid #2563eb; padding: 16px; border-radius: 4px; margin: 20px 0;">
              <h4 style="margin: 0 0 8px 0; color: #1e293b;">Your Message Summary:</h4>
              <p style="margin: 0; white-space: pre-wrap; color: #475569; font-size: 14px; line-height: 1.6;">{message}</p>
            </div>
            
            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0;" />
            
            <div style="font-size: 14px; color: #64748b;">
              <p style="margin: 0 0 4px 0; font-weight: bold; color: #0f172a;">Best regards,</p>
              <p style="margin: 0 0 4px 0; font-size: 15px; font-weight: bold; color: #2563eb;">Rajat Bandhral</p>
              <p style="margin: 0 0 2px 0;">DevOps Engineer</p>
              <p style="margin: 0 0 2px 0;">Email: <a href="mailto:rajatrajput076@gmail.com" style="color: #2563eb; text-decoration: none;">rajatrajput076@gmail.com</a></p>
              <p style="margin: 0;">Location: Jammu, India</p>
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

        logger.info(f"Thank-you email sent successfully to visitor: {email}")
        return {"status": "success", "message": f"Thank-you email sent to {email}"}
    except Exception as e:
        error_msg = f"Failed to send thank-you email: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}
