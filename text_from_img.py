import time
from urllib.request import urlretrieve
from PIL import Image
import pytesseract
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess

def getImgText(imgURL):
    urlretrieve(img, 'page.jpg')
    p = subprocess.Popen(['tesseract', 'page.jpg', 'page'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()
    f = open('page.txt', 'r')
    print(f.read())

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome('./chromedriver', options=chrome_options)
driver.get('https://www.amazon.com/Am-Strange-Loop-Douglas-Hofstadter/dp/0465030793/ref=sr_1_1?crid=1FBIHUVC5PULO&dchild=1&keywords=douglas+hofstadter&qid=1607834002&sprefix=douglas+hofs%2Caps%2C301&sr=8-1')
time.sleep(2)
driver.find_element_by_id('imgBlkFront').click()
imgList= []
time.sleep(5)

while 'pointer' in driver.find_element_by_id('sitbReaderRightPageTurner').get_attribute('style'):
    driver.find_element_by_id('sitbReaderRightPageTurner').click()
    time.sleep(2)
    pages = driver.find_elements_by_xpath('//div[@class=\'pageImage\']/div/img')
    if not len(pages):
        print("no pages found")
    for page in pages:
        img = page.get_attribute('src')
        print('found img: {}'.format(img))
        if img not in imgList:
            imgList.append(img)
            getImgText(img)

driver.quit()


