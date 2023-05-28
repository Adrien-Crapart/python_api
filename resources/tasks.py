import os
from dotenv import load_dotenv
import jinja2

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)


def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)


def send_simple_message(to, subject, body, html):
    # Create the root message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SMTP_EMAIL
    msg['To'] = to

    msgText = MIMEText(body, 'plain')
    msgHtml = MIMEText(html, 'html')
    msg.attach(msgText)
    msg.attach(msgHtml)

    mailserver = smtplib.SMTP(SMTP_SERVER, 587)
    mailserver.starttls()
    mailserver.login(SMTP_EMAIL, SMTP_PASSWORD)
    mailserver.sendmail(SMTP_EMAIL, to, msg.as_string())
    mailserver.quit()

    return {"message": "Mail done successfully."}


def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "Successfully signed up",
        f"<p>Hi {username}! You have successfully signed up to the Stores REST API.</p>",
        render_template("email/action.html", username=username)
    )
