import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

comp_name = socket.gethostname()

user = 'greti.lab.updates@gmail.com'
password = 'greti2019'
to = 'mchimento@ab.mpg.de'
subject = 'Daily data {}'.format(comp_name)
data_attachment_path = "/home/pi/Desktop/puzzle_code_pi/data/{}_RFID.csv".format(comp_name)

msg = MIMEMultipart()
msg['Subject'] = subject
msg['From'] = user
msg['To'] = ', '.join(to)

part = MIMEBase('application', "octet-stream")
part.set_payload(open(data_attachment_path, "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename={}'.format(data_attachment_path))
msg.attach(part)

try:
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login(user,password)
    server.sendmail(user, to, msg.as_string())
    server.close()
    print("Email Sent!")
    
except:
    print("no worky worky")