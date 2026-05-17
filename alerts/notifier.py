# alerts/notifier.py

from alerts.email_alert import send_alert
from utils.logger import get_logger

logger = get_logger("notifier")

class Notifier:
    def __init__(self):
        self.channels = ["email"]  # Extend: slack, webhook, sms

    def notify(self, message):
        logger.info("Triggering alert notification")

        if "email" in self.channels:
            try:
                send_alert(message)
                logger.info("Email alert sent successfully")
            except Exception as e:
                logger.error(f"Email alert failed: {e}")

        # Future integrations
        # if "slack" in self.channels:
        #     send_slack(message)

        # if "webhook" in self.channels:
        #     send_webhook(message)
