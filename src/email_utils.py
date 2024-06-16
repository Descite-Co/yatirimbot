import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import os

# Adding environment variables
load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

def send_email(subject, body, image_stream=None):
    server = smtplib.SMTP_SSL('mail.kurumsaleposta.com', 465)
    server.login(EMAIL, PASSWORD)

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = 'me@omerduran.dev'  # Recipient address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach image if available
    if image_stream:
        image = MIMEImage(image_stream.getvalue())
        image.add_header('Content-Disposition', 'attachment', filename='image.png')
        msg.attach(image)

    server.send_message(msg)
    server.quit()

