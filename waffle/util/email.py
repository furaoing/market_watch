# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:57:35 2015

@author: Taikor
"""

import smtplib
from email.mime.text import MIMEText


def send_email(email_server, acc, pwd, from_addr, to_addr, subject, content):

    msg = MIMEText(content)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr

    smtp = smtplib.SMTP()
    smtp.connect(email_server)  # example: "smtp.qq.com"
    smtp.login(acc, pwd)
    smtp.sendmail(from_addr, to_addr, msg.as_string())
    smtp.close()
    return 0

