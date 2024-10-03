"""Utility module for sending emails with optional image attachments."""

import os
import ssl
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from dotenv import load_dotenv

# Adding environment variables
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
RECEIVER = os.getenv("RECEIVER")


def send_email(subject: str, body: str, image_stream=None):
    """
    Send an email with an optional image attachment.

    Args:
        subject (str): The subject of the email.
        body (str): The body content of the email.
        image_stream (BytesIO, optional): A BytesIO stream containing the image data.

    Raises:
        smtplib.SMTPException: If there's an error sending the email.
    """
    # Create an SSL context
    context = ssl.create_default_context()

    # Connect to the server using the context
    with smtplib.SMTP_SSL("mail.kurumsaleposta.com", 465, context=context) as server:
        server.login(EMAIL, PASSWORD)

        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = RECEIVER
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # Attach image if available
        if image_stream:
            image = MIMEImage(image_stream.getvalue())
            image.add_header("Content-Disposition", "attachment", filename="image.png")
            msg.attach(image)

        server.send_message(msg)

# Example usage
# send_email("Anlık Kripto Verileri", "This is the email body", image_stream)
