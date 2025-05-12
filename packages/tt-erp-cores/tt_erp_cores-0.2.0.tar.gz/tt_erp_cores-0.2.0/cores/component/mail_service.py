from email.mime.text import MIMEText
from smtplib import SMTP

from decouple import config
from fastapi import HTTPException

from cores.logger.logging import ApiLogger

MAIL_DRIVER = config("MAIL_DRIVER")
MAIL_HOST = config("MAIL_HOST")
MAIL_PORT = config("MAIL_PORT")
MAIL_USERNAME = config("MAIL_USERNAME")
MAIL_PASSWORD = config("MAIL_PASSWORD")
MAIL_ENCRYPTION = config("MAIL_ENCRYPTION")
MAIL_FROM_ADDRESS = config("MAIL_FROM_ADDRESS")
MAIL_FROM_NAME = config("MAIL_FROM_NAME")

# typical values for text_subtype are plain, html, xml
# text_subtype = 'plain'
# content = """\
# Test SMTTP Python script
# """

# subject = "Sent from vinasupport.com"


def send_mail(
    subject,
    receiver_emails,
    content,
    text_subtype="plain",
    mail_username: str = None,
    mail_password: str = None,
):
    try:
        msg = MIMEText(content, text_subtype)
        msg["Subject"] = subject
        # some SMTP servers will do this automatically, not all
        if not mail_username:
            mail_from_address = MAIL_FROM_ADDRESS
            mail_username = MAIL_USERNAME
        else:
            mail_from_address = mail_username
        if not mail_password:
            mail_password = MAIL_PASSWORD
        msg["From"] = mail_from_address
        msg["To"] = ", ".join(receiver_emails)
        conn = SMTP(MAIL_HOST, MAIL_PORT)
        conn.login(mail_username, mail_password)
        conn.sendmail(mail_from_address, receiver_emails, msg.as_string())
        conn.quit()
        return True

    except Exception:
        import traceback

        ApiLogger.logging_email(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error sending email: {traceback.format_exc()}",
        )
