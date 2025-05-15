import smtplib
from email.mime.text import MIMEText
from typing import Dict

from agents_for_all.tools.base_tool import Tool


class Email(Tool):
    """
    A tool that sends emails via SMTP.

    Requires SMTP host, port, and login credentials during initialization.
    """

    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str):
        """
        Initialize the Email tool.

        Args:
            smtp_host (str): SMTP server hostname (e.g., smtp.gmail.com).
            smtp_port (int): SMTP server port (e.g., 587).
            username (str): Email account username.
            password (str): Email account password or app-specific token.

        Returns:
            None
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    @property
    def name(self) -> str:
        """
        Email
        """
        return "Email"

    @property
    def description(self) -> str:
        """
        Sends an email using SMTP.
        """
        return (
            "Sends an email to a recipient. "
            'Input must include: {"to": "...", "subject": "...", "body": "..."}. '
            "Requires SMTP credentials during initialization."
        )

    def execute(self, input_json: Dict) -> str:
        to_email = input_json.get("to")
        subject = input_json.get("subject")
        body = input_json.get("body")

        if not to_email or not subject or not body:
            return "Error: 'to', 'subject', and 'body' are required."

        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self.username
            msg["To"] = to_email

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            return f"Email sent to {to_email}"

        except Exception as e:
            return f"Email error: {str(e)}"
