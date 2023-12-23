from datetime import datetime

import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, email_login: str = '', email_password: str = '', email_smtp: str = '', smtp_port: int = 0, email_imap: str = ''):
        self.email_login = email_login
        self.email_password = email_password
        self.email_smtp = email_smtp
        self.smtp_port = smtp_port
        self.email_imap = email_imap

    def send_msg(self, email_subject: str = '', recipients_lst: list = [], email_message: str = ''):
        smtp_obj = smtplib.SMTP(self.email_smtp, self.smtp_port)
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.ehlo()
        smtp_obj.login(self.email_login, self.email_password)
        msg = MIMEMultipart()
        msg['From'] = self.email_login
        msg['To'] = ', '.join(recipients_lst)
        msg['Subject'] = email_subject
        msg.attach(MIMEText(email_message))
        smtp_obj.sendmail(self.email_login, msg.as_string())
        smtp_obj.quit()

    def recieve_messages(self, email_headers=None, rfc: str = '(RFC822)'):
        eamil_headers = email_headers
        imap_mail = imaplib.IMAP4_SSL(self.email_imap)
        imap_mail.login(self.email_login, self.email_password)
        imap_mail.list()
        imap_mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % eamil_headers if eamil_headers else 'ALL'
        result, data = imap_mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = imap_mail.uid('fetch', latest_email_uid, rfc)
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        imap_mail.logout()
        return email_message


if __name__ == '__main__':
    print("Let's start")
    print()
    start_time = datetime.now()
    my_email = Email('login', 'password', 'smtp_server', 587,'imap_server')
    my_email.send_msg('subject', ['recipient1', 'recipient2'], 'message')
    my_email.recieve_messages()
    print(f'Done in {datetime.now() - start_time}')
