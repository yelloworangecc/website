import smtplib
from email.mime.text import MIMEText
from email.header import Header

class EmailMe:
    def __init__(self, domain, port):
        self._domain = domain
        self._port = port
        
    def login(self, email, passcode):
        self._smtp = smtplib.SMTP_SSL(_domain, _port)
        self._email = email
        self._smtp.login(email, passcode)
    def quit(self):
        self._smtp.quit()
    def send(self,to,who,msg):
        content = MIMEText(who + ': ' + msg, 'plain', 'utf-8')
        content['Subject'] = Header("WT Message", 'utf-8')
        content['From'] = Header(self._email, 'utf-8')
        content['To'] =  Header(to, 'utf-8')
        to_list = []
        to_list.append(to)
        self._smtp.sendmail(self._email, to_list, content.as_string())
