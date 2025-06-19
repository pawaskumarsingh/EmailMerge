import csv
import smtplib
from email.message import EmailMessage
from .models import SMTPSetting

def send_bulk_emails_from_csv(csv_path):
    # Load the latest SMTP settings
    smtp_setting = SMTPSetting.objects.latest('created_at')

    # Open and read the CSV file
    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        contacts = list(reader)

    # Setup SMTP connection
    with smtplib.SMTP(smtp_setting.smtp_host, smtp_setting.smtp_port) as smtp:
        if smtp_setting.use_tls:
            smtp.starttls()
        smtp.login(smtp_setting.email_address, smtp_setting.email_password)

        for contact in contacts:
            msg = EmailMessage()
            msg['Subject'] = 'Personalized Greeting'
            msg['From'] = smtp_setting.email_address
            msg['To'] = contact['email']

            msg.set_content(f"""\
                        Hi {contact['first_name']} {contact['last_name']},ss
                        This is a personalized message from Django using your SMTP settings.
                        Thanks!
""")

            smtp.send_message(msg)
            print(f"Sent email to {contact['email']}")