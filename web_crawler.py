from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

random.seed(datetime.datetime.now())
def getLinks(articleURL):
    URL = 'http://en.wikipedia.org{}'.format(articleURL)
    html = urlopen(URL)
    bs = BeautifulSoup(html.read(), 'html.parser')
    return bs.find('div', {'id': 'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))


def sixDegreeWiki(links,init, aim, path=[]):
    path.append(init)
    if init == aim:
        return path
    if len(path) > 6:
        raise KeyError
    newArticle = links[random.randint(0, len(links) - 1)].attrs['href']
    links = getLinks(newArticle)
    res = sixDegreeWiki(links, newArticle, aim, path)
    return res


INIT_LINK = '/wiki/Eric_Idle'
AIM_LINK = '/wiki/Kevin_Bacon'
MAX_NUMBER = 6
init_links = getLinks(INIT_LINK)

#res = None
#while res == None:
#    try:
#        res = sixDegreeWiki(init_links, INIT_LINK, AIM_LINK)
#    except KeyError:
#        print("error")
#        res = None
#    else:
#        print(res)

# Crawling Entire Site
# be careful about recursion limit
pages = set()
def getLinks(pageURL):
    global pages
    URL = 'http://en.wikipedia.org{}'.format(pageURL)
    html = urlopen(URL)
    bs = BeautifulSoup(html.read(), 'html.parser')
    try:
        print(bs.h1.get_text())
        print(bs.find(id='mw-content-text').find_all('p')[0])
        print(bs.find(id='ca-edit').find('span').
              find('a').attrs['href'])
    except AttributeError:
        print('this page is missing smt, I am continuing')

    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print('-'*20)
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks('')


