from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

def getInternalLinks(bs, includeUrl):
    # scheme = http
    # netloc = www.cwi.com:80
    include_url = '{}://{}'.format(urlparse(includeUrl).scheme,
                                  urlparse(includeUrl).netloc)
    internal_links = []
    for link in bs.find_all('a',
                            href=re.compile('^(/|.*' + includeUrl + ')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internal_links:
                if (link.attrs['href'].startswith('/')):
                    internal_links.append(includeUrl+link.attrs['href'])
                else:
                    internal_links.append(link.attrs['href'])
    return internal_links

def getExternalLinks(bs, excludeUrl):
    external_links = []
    for link in bs.find_all('a',
                            href=re.compile('^(http|www)((?!' + excludeUrl + ').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in external_links:
                external_links.append(link.attrs['href'])
    return external_links

def getRandomExternalLink(start_page):
    html = urlopen(start_page)
    bs = BeautifulSoup(html.read(), 'html.parser')
    external_links = getExternalLinks(bs, urlparse(start_page).netloc)
    if len(external_links) == 0:
        # no external link
        # dig current site deeper
        print('no external links, looking around to find one')
        domain = '{}://{}'.format(urlparse(start_page).scheme, urlparse(start_page).netloc)
        internal_links = getInternalLinks(bs, domain)
        next_link = internal_links[random.randint(0, len(internal_links)-1)]
        return getRandomExternalLink(next_link)
    else:
        return external_links[random.randint(0, len(external_links)-1)]

def followExternalOnly(start_page):
    external_link = getRandomExternalLink(start_page)
    print(f'random external link is {external_link}')
    followExternalOnly(external_link)

# followExternalOnly('http://oreilly.com')

# collect a list of all external urls found on the site
all_ext_links = set()
all_int_links = set()


def getAllExtLinks(site_url):
    html = urlopen(site_url)
    domain = '{}://{}'.format(urlparse(site_url).scheme,
                              urlparse(site_url).netloc)
    bs = BeautifulSoup(html, 'html.parser')
    internal_links = getInternalLinks(bs, domain)
    external_links = getExternalLinks(bs, domain)

    # find all external links for current internal link
    for link in external_links:
        if link not in all_ext_links:
            all_ext_links.add(link)
            print(link)

    # than change internal link 
    for link in internal_links:
        if link not in all_int_links:
            all_int_links.add(link)
            getAllExtLinks(link)

getAllExtLinks('http://oreilly.com')

