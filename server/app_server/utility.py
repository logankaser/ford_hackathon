
from secrets import randbelow
import requests
from flask import current_app


def random_hash256():
    """Random 256bithash."""
    hex_string = "0123456789abcdef"
    output = ""
    for _ in range(64):
        output += hex_string[randbelow(16)]
    return output


def send_email(to, subject, message):
    """Sends an email.
    :param to: email address of reciever
    :param subject: subject of email
    :param message: body of email
    """
    res = requests.post(
        "https://api.mailgun.net/v3/" +
        current_app.config.get("MAILGUN_DOMAIN") +
        "/messages",
        auth=("api", current_app.config.get("MAILGUN_KEY")),
        data={
            "from": "No Reply <" +
                    "noreply@" +
                    current_app.config.get("MAILGUN_DOMAIN") +
                    ">",
            "to": [to],
            "subject": subject,
            "html": message
        })
