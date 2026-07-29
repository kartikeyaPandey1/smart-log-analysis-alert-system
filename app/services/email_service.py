import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv


load_dotenv()


EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ALERT_RECEIVER = os.getenv("ALERT_RECEIVER")


def send_alert_email(
    service,
    severity,
    error_count
):

    subject = "Smart Log Alert"

    body = f"""
    Alert Generated

    Service: {service}

    Severity: {severity}

    Error Count: {error_count}

    Message: High error rate detected
    """


    message = MIMEMultipart()

    message["From"] = EMAIL_USER
    message["To"] = ALERT_RECEIVER
    message["Subject"] = subject

    message.attach(
        MIMEText(body, "plain")
    )


    try:

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            EMAIL_USER,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_USER,
            ALERT_RECEIVER,
            message.as_string()
        )

        server.quit()

        return True


    except Exception as e:

        print(
            "Email error:",
            e
        )

        return False