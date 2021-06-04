import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

conn = pymysql.connect(host='localhost', user='phymat',
                       password='asd-123ASD', db='mysql', charset='utf8')
# send all info as utf-8
cur = conn.cursor()
cur.execute("USE scraping")

random.seed(datetime.datetime.now())

def store(title, content):
    cur.execute('INSERT INTO pages (title, content) VALUES ' +
                '("%s", "%s")', (title, content))
    # commit by cursors connection
    cur.connection.commit()

def getLinks(article_url):
    html = urlopen('http://en.wikipedia.org' + article_url)
    bs = BeautifulSoup(html, 'html.parser')
    title = bs.find('h1').get_text()
    content = bs.find('div', {'id': 'mw-content-text'}).find('p').get_text()
    store(title, content)
    return bs.find('div', {'id': 'bodyContent'}).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))

links = getLinks('/wiki/Kevin_Bacon')
try:
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links)-1)].attrs['href']
        print(newArticle)
        links = getLinks(newArticle)
finally:
    cur.close()
    conn.close()
