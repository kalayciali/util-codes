from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import subprocess
import requests
from PIL import Image
from PIL import ImageOps

def cleanImage(imgPath):
    img = Image.open(imgPath)
    img = img.point(lambda x: 0 if x<143 else 255)
    borderImg = ImageOps.expand(img, border=20, fill='white')
    borderImg.save(imgPath)

html = urlopen('http://www.pythonscraping.com/humans-only')
bs = BeautifulSoup(html, 'html.parser')
imgLoc = bs.find('img', {'title': 'Image CAPTCHA'})['src']
formId = bs.find('input', {'name': 'form_build_id'})['value']
captchaSid = bs.find('input', {'name': 'captcha_sid'})['value']
captchaToken = bs.find('input', {'name': 'captcha_token'})['value']

captchaUrl = 'http://pythonscraping.com' + imgLoc
urlretrieve(captchaUrl, 'captcha.jpg')
cleanImage('captcha.jpg')
p = subprocess.Popen(['tesseract', 'captcha.jpg', 'captcha'],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.wait()
f = open('captcha.txt', 'r')

captchaResp = f.readline().replace(' ', '').replace('\n', '')
print('soln found is "' + captchaResp + '" this much')
print(len(captchaResp))

if len(captchaResp) == 5:
    params = {'captcha_token': captchaToken, 'captcha_sid': captchaSid,
              'form_id': 'comment_node_page_form', 'form_build_id': formId,
              'captcha_response':captchaResp, 'name':'Ryan Mitchell',
              'subject': 'I come to seek the Grail',
              'comment_body[und][0][value]':'...and I am definitely not a bot'}
    r = requests.post('http://www.pythonscraping.com/comment/reply/10',
                     data=params)
    resp = BeautifulSoup(r.text, 'html.parser')
    if resp.find('div', {'class': 'messages'}) is not None:
        print(resp.find('div', {'class': 'messages'}).get_text())

else:
    print('hellow don\'t dupe me')
    print('there is a problem with CAPTCHA')

