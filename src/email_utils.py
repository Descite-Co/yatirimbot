
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import os
import ssl
import io

# Adding environment variables
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def send_email(subject, body, image_stream=None):
    # Create an SSL context
    context = ssl.create_default_context()
    # context.options |= ssl.OP_LEGACY_SERVER_CONNECT  # Commented out

    # Connect to the server using the context
    server = smtplib.SMTP_SSL("mail.kurumsaleposta.com", 465, context=context)
    server.login(EMAIL, PASSWORD)

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = "logrissoitottu-2990@yopmail.com"  # Recipient address
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Attach image if available
    if image_stream:
        image = MIMEImage(image_stream.getvalue())
        image.add_header("Content-Disposition", "attachment", filename="image.png")
        msg.attach(image)

    server.send_message(msg)
    server.quit()
