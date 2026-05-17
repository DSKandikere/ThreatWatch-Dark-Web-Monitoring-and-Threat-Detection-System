from alerts.email_alert import send_email_alert
from alerts.sms_alert import send_sms_alert
from alerts.push_alert import send_push_alert

def send_alert(text):
    message = f"🚨 Dark Web Leak Detected:\n\n{text}"

    print("\n🚨 ALERT TRIGGERED")

    # Send all alerts
    send_email_alert(message)
    send_sms_alert(message)
    send_push_alert(message)
