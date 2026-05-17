from twilio.rest import Client

# Replace with your Twilio credentials
ACCOUNT_SID = "AC346e703cf0919e0cf229c8b494c643d3"
AUTH_TOKEN = "16b00e1a6e147606acb2f527b6162ee9"
TWILIO_NUMBER = "+1 727 800 3891"
TARGET_NUMBER = "+917349347948"

def send_sms_alert(message):
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,
            to=TARGET_NUMBER
        )

        print("📱 SMS sent successfully")

    except Exception as e:
        print("❌ SMS failed:", e)
