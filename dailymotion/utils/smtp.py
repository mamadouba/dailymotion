import smtplib
from email.mime.text import MIMEText

from dailymotion.utils.logger import logger


class SMTPClient:
    def __init__(self, host, port, sender) -> None:
        self.sender = sender
        self._client = smtplib.SMTP(host=host, port=port)

    def sendmail(
        self,
        recipient: str,
        subject: str,
        content: str,
    ):
        try:
            print(content)
            msg = MIMEText(content)
            msg["Subject"] = subject
            msg["From"] = self.sender
            msg["To"] = recipient
            logger.info(f"Send email to {recipient}")
            self._client.sendmail(self.sender, recipient, msg.as_string())
            logger.info("Successfully sent email")
        except Exception as exc:
            logger.error(f"Fail to send email to {recipient}: {str(exc)}")

    def close(self):
        self._client.close()


if __name__ == "__main__":
    client = smtplib.SMTP(host="localhost", port=1025)
    client.sendmail("test@example.com", "barry@example.com", "hello!")
