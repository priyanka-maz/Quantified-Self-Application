import smtplib
from .config import *
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.encoders import encode_base64

def send_email(to_address, subject, message, content, attachment_file=None):
    msg = MIMEMultipart()
    msg["From"] = DevelopmentConfig.SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(message, content))

    if attachment_file:
        # Add file as application/octet-stream
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment_file)
        # Email attachments are sent as base64 encoded
        encode_base64(part)
        #base64.b64encode(part).decode('utf-8')
        part.add_header(
                "Content-Disposition", f"attachment; filename={attachment_file}",
        )
        # Add the attchment to msg
        msg.attach(part)

    s = smtplib.SMTP(host=DevelopmentConfig.SMTP_SERVER_HOST, port=DevelopmentConfig.SMTP_SERVER_PORT)
    s.login(DevelopmentConfig.SENDER_ADDRESS, DevelopmentConfig.SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return True
