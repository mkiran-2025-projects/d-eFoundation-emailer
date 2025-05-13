import os
import csv
import time
import smtplib
import schedule
from dotenv import load_dotenv
from email.message import EmailMessage

# 1) load .env
load_dotenv()  
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER   = os.getenv('SMTP_SERVER')
SMTP_PORT     = int(os.getenv('SMTP_PORT', 465))
SEND_TIME     = os.getenv('SEND_TIME', '22:53')
DELAY         = int(os.getenv('DELAY_SECONDS', 5))

# 2) your cold‐email subject & body template
SUBJECT = "Quick Question About Your Work"
BODY_TEMPLATE = """\
Hello {name},

I hope you’re doing well. I wanted to reach out about [YOUR PITCH HERE]—

• bullet 1  
• bullet 2  

Would love 10 min on your calendar next week!

Best,  
Your Name
"""

def send_email(recipient: str, name: str):
    msg = EmailMessage()
    msg['Subject'] = SUBJECT
    msg['From']    = EMAIL_ADDRESS
    msg['To']      = recipient
    # personalize if name exists, else just email
    body = BODY_TEMPLATE.format(name=name or recipient)
    msg.set_content(body)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print(f"✅ Sent to {recipient}")

def job():
    print(f"Starting send job… ({time.strftime('%Y-%m-%d %H:%M:%S')})")
    with open('emails.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                send_email(row['email'], row.get('name', ''))
            except Exception as e:
                print(f"❌ Failed {row['email']}: {e}")
            time.sleep(DELAY)
    print("Job complete.")

if __name__ == "__main__":
    # schedule once per day
    schedule.every().day.at(SEND_TIME).do(job)
    print(f"Scheduled daily sends at {SEND_TIME}. Press Ctrl+C to quit.")
    while True:
        schedule.run_pending()
        time.sleep(1)
