import os, sys, smtplib
from email.mime.text import MIMEText

from ats.ats import BrokerPlatform

# configs
from config import email_settings

class Emailer:
    def __init__(self, settings):
        self.settings = settings
        self.logged_in = False

    def login(self):
        if (self.logged_in):
            return

        self.smtp = smtplib.SMTP(self.settings.server, self.settings.port)
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login(email_settings.user, email_settings.password)        
        self.logged_in = True

    def send(self, to, subject, msg_body):
        if (not self.logged_in):
            self.login()

        msg = MIMEText(msg_body)
        msg['Subject'] = subject
        msg['From'] = self.settings.user
        msg['To'] = to
        self.smtp.sendmail(self.settings.user, [to], msg.as_string())

    def logout(self):
        if (not self.logged_in):
            return

        self.smtp.quit()

if __name__ == "__main__":
   e = Emailer(email_settings)
   target_email_address = "fill in"
   e.send(target_email_address, "test1", "something")
   e.send(target_email_address, "test2", "something else ")
   e.logout()
   