import smtplib
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText

# Load environment variables from .env file
load_dotenv()

def send_test_email():
    if not load_dotenv():
        print("Failed to load .env file")
    sender = os.getenv('EMAIL_USER')
    receiver = os.getenv('TO_EMAIL')
    subject = 'Test Email'
    body = 'This is a test email.'

    print(f"Sender: {sender}")
    print(f"Receiver: {receiver}")
    print(f"Body: {body}")

    from datetime import datetime, timezone, timedelta

    # Get the current time in UTC
    utc_plus_one = timezone(timedelta(hours=1))
    current_time_utc_plus_one = datetime.now(utc_plus_one)
    print(current_time_utc_plus_one)  # Outputs the current time in UTC


    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, os.getenv('EMAIL_PASS'))
            smtp.send_message(msg)
        print("Test email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

send_test_email()
