import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import os
import ssl

# Adding environment variables
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def send_email(subject, body, image_stream=None):
    # Create an SSL context
    context = ssl.create_default_context()
    context.options |= (
        ssl.OP_LEGACY_SERVER_CONNECT
    )  # Enable unsafe legacy renegotiation

    # Connect to the server using the context
    server = smtplib.SMTP_SSL("mail.kurumsaleposta.com", 465, context=context)
    server.login(EMAIL, PASSWORD)

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = "nattotrecrogre-8867@yopmail.com"  # Recipient address
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Attach image if available
    if image_stream:
        image = MIMEImage(image_stream.getvalue())
        image.add_header("Content-Disposition", "attachment", filename="image.png")
        msg.attach(image)

    server.send_message(msg)
    server.quit()


# Example usage
# with open("path_to_image.png", "rb") as img_file:
#     image_stream = io.BytesIO(img_file.read())
# send_email("Anlık Kripto Verileri", "This is the email body", image_stream)
