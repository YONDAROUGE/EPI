import smtplib
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
from datetime import datetime, timezone, timedelta

# Load environment variables from .env file
load_dotenv()

def send_test_email():
    sender = os.getenv('EMAIL_USER')
    receiver = os.getenv('TO_EMAIL')

    # Location: University of Buea
    latitude = "4.1449"
    longitude = "9.2886"
    location = f"{latitude},{longitude}"
    maps_link = f"https://maps.google.com/?q={location}"

    # Get current time in UTC+1 (Cameroon local time)
    current_time = datetime.now(timezone(timedelta(hours=1))).strftime("%Y-%m-%d %H:%M:%S")

    # Email content
    subject = '📍 Epilepsy Alert – Test Email'
    body = f"""
🕒 Time: {current_time}
📍 Location: {location}
🌍 View on Map: {maps_link}

⚠️ This is a test alert from the Epilepsy Monitoring Device at the University of Buea.
"""

    # Construct and send email
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, os.getenv('EMAIL_PASS'))
            smtp.send_message(msg)
        print("✅ Test email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Run it
send_test_email()
