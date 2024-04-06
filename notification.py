import smtplib
from email.mime.text import MIMEText
from config import Config
import requests
from market_watch_logger import root_logger


def send_mail_bin(from_addr, to_addr, subject, content):
    from email.mime.text import MIMEText
    from subprocess import Popen, PIPE

    msg = MIMEText(content)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
    p.communicate(msg.as_bytes())


def send_mailgun_email(receiver, email_subject, msg):
    r = requests.post(
        "%s/messages" % Config.MailGunBaseURL,
        auth=("api", Config.MailGunAPIKey),
        data={"from": "%s <%s>" % (Config.MailSenderName, Config.MailGunSenderAddr),
              "to": [receiver],
              "subject": email_subject,
              "text": msg})
    r.encoding = "utf8"
    msg = r.text
    root_logger.info(msg)


def send_email(email_server, acc, pwd, from_addr, to_addr, subject, content):

    msg = MIMEText(content)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr

    smtp = smtplib.SMTP(timeout=Config.EmailTimeOut)
    smtp.connect(email_server)  # example: "smtp.qq.com"
    smtp.login(acc, pwd)
    smtp.sendmail(from_addr, to_addr, msg.as_string())
    smtp.close()
    return 0


def send_signal_notification(msg, stock_ticker):
    content = r"%s: %s" % (msg, stock_ticker)
    email_subject = "Trading Signal"
    receiver = Config.Receiver

    send_mailgun_email(receiver, email_subject, content)


def send_notification(msg):
    email_subject = "Trading Signal"
    receiver = Config.Receiver

    send_mailgun_email(receiver, email_subject, msg)


def send_news_notification(source, msg, subject_body="Market News"):
    email_subject = "%s - %s" % (subject_body, source)
    receiver = Config.Receiver

    send_mailgun_email(receiver, email_subject, msg)


def send_news_notification_general(receiver, source, msg, subject_body="Market News"):
    email_subject = "%s - %s" % (subject_body, source)
    send_mailgun_email(receiver, email_subject, msg)


class EmailMsg(object):
    def __init__(self):
        self.msg_list = []
        self.level = None

    def add(self, msg):
        self.msg_list.append(msg)

    def clear(self):
        self.msg_list.clear()
        self.level = None

    def msg(self):
        tmp = "\n\n".join(self.msg_list)
        return tmp

    def set_importance_level(self, level):
        self.level = level


if __name__ == "__main__":
    email_subject = "News Watch"
    receiver = Config.Receiver
    msg = "This is a test from myself"
    #send_mailgun_email(receiver, email_subject, msg)
    send_news_notification("RR", msg)