import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.message import EmailMessage
SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025


def send_email(address, sub, mess, fileName):
    msg = MIMEMultipart()
    body_part = MIMEText(mess, 'plain')
    msg.attach(body_part)
    # msg.set_content(mess)
    msg['Subject'] = sub
    msg['From'] = "chiraggoel172002@gmail.com"
    msg['To'] = address
    path = "./"+fileName
    with open(path, 'rb') as file:
        msg.attach(MIMEApplication(file.read(), Name=fileName))
    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
