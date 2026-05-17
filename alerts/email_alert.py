import os
import logging
from dotenv import load_dotenv

load_dotenv()  # ✅ THIS LINE IS REQUIRED

logger = logging.getLogger("notifier")

def send_alert(message):

    email = os.getenv("ALERT_EMAIL")
    password = os.getenv("ALERT_PASSWORD")

    if not email or not password:
        logger.info("🚨 ALERT (EMAIL DISABLED OR MISSING ENV)")
        logger.info(message)
        return

    try:
        import smtplib
        from email.mime.text import MIMEText

        msg = MIMEText(message)
        msg["Subject"] = "Dark Web Monitoring Alert"
        msg["From"] = email
        msg["To"] = email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(email, password)
        server.sendmail(email, email, msg.as_string())
        server.quit()

        logger.info("✅ Email alert sent successfully")

    except Exception as e:
        logger.error(f"Email alert failed: {e}")
