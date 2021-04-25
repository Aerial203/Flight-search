from twilio.rest import Client
import smtplib

ACCOUNT_SID = "AC6bb15efee13b8d1810f53b9e80f95eb0"
AUTH_TOKEN = "2d9e9d1aa4a6c37cc323b19766822709"
SENDER_ADDRESS = "YourEmail"
PASSWORD = "YourPassword"


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_="FromNumber",
            to="PhoneNumber",
        )
        print(message.sid)

    def send_email(self, message, receiver_email, link):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.login(SENDER_ADDRESS, PASSWORD)
            for r_email in receiver_email:
                connection.sendmail(from_addr=SENDER_ADDRESS,
                                    to_addrs=r_email,
                                    msg=f"Subject: Low price alert!\n\n{link}\n{message}".encode('utf-8'))
