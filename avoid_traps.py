import requests
from bs4 import BeautifulSoup

# User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53
# it is more easy to scrape sites with mobile user agent

session = requests.Session()
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
url = 'https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending'
req = session.get(url, headers=headers)
bs = BeautifulSoup(req.text, 'html.parser')
print(bs.find('table', {'class': 'table-striped'}).get_text)

# getting cookies 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome('./chromedriver', options=chrome_options)
driver.get('http://pythonscraping.com')
driver.implicitly_wait(1)
cookies = driver.get_cookies()
print(cookies)

driver2 = webdriver.Chrome('./chromedriver', options=chrome_options)
driver2.get('http://pythonscraping.com')
driver2.delete_all_cookies()
for cookie in cookies:
    driver2.add_cookie(cookie)

driver2.get('http://pythonscraping.com')
driver.implicitly_wait(1)
print(driver2.get_cookies())

# honeypots
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.Chrome('./chromedriver', options=chrome_options)
driver.get('http://pythonscraping.com/pages/itsatrap.html')
links = driver.find_elements_by_tag_name('a')
print(links)
for link in links:
    if not link.is_displayed():
        print('the trap link is {}'.format(link.get_attribute('href')))

fields = driver.find_elements_by_tag_name('input')
for field in fields:
    if not field.is_displayed():
        print('hidden fields {}'.format(field.get_attribute('name')))

