
from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import smtplib
from email.mime.text import MIMEText
import os
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('health_logs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            g_force REAL,
            temperature REAL,
            gsr INTEGER,
            heart_rate INTEGER,
            location TEXT
        )
    ''')
    conn.commit()
    conn.close()

def send_email_alert(data):
    sender = os.getenv('EMAIL_USER')
    receiver = os.getenv('TO_EMAIL')
    subject = 'Epilepsy Alert – Patient Health Update'
    
    # Small code to get time in UTC+1
    utc_plus_one = timezone(timedelta(hours=1))
    # current_time_utc_plus_one = datetime.now(utc_plus_one)

    body = f"""📅 Time: {datetime.now(utc_plus_one).isoformat()}
📍 Location: {data['location']}
⚠️ ALERT: Seizure Detected
- G-Force: {data['g_force']}
- Temp: {data['temperature']}°C
- GSR: {data['gsr']}
- Heart Rate: {data['heart_rate']} bpm
"""

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, os.getenv('EMAIL_PASS'))
        smtp.send_message(msg)

@app.route('/api/log', methods=['POST'])
def log_data():
    data = request.get_json()
    required = ['g_force', 'temperature', 'gsr', 'heart_rate', 'location']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing fields in request'}), 400

    conn = sqlite3.connect('health_logs.db')
    c = conn.cursor()
    c.execute('''INSERT INTO logs (timestamp, g_force, temperature, gsr, heart_rate, location)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (datetime.utcnow().isoformat(),
               data['g_force'],
               data['temperature'],
               data['gsr'],
               data['heart_rate'],
               data['location']))
    conn.commit()
    conn.close()

    send_email_alert(data)
    return jsonify({'status': 'logged and emailed'}), 200

@app.route('/api/logs', methods=['GET'])
def get_logs():
    conn = sqlite3.connect('health_logs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM logs ORDER BY timestamp DESC')
    logs = c.fetchall()
    conn.close()
    return jsonify(logs)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
