import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

# if you have running SMTP on localhost

def sendMail(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'ryan@gmail.com'
    msg['To'] = 'kalayciali@gmail.com'

    # if you have running SMTP on localhost
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

bs = BeautifulSoup(urlopen('https://isitchristmas.com/'), 'html.parser')
while (bs.find('a', {'id': 'answer'}).attrs['title'] == 'NO'):
    print("It is not christmas yet")
    time.sleep(3600)
    bs = BeautifulSoup(urlopen('https://isitchristmas.com/'), 'html.parser')

sendMail('It\'s Christmas!', 'According to http://itischristmas.com, it is Christmas!')
