import requests
from bs4 import BeautifulSoup
import re

class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def __str__(self):
        return "URL: {}\nTITLE: {}\nBODY:\n{}".format(self.url, self.title, self.body)

class Website:
    def __init__(self, name, url, target_pattern,
                 abs_url, title_tag, body_tag):
        # crawling sites through links 
        self.name = name
        self.url = url
        self.target_pattern = target_pattern
        self.abs_url = abs_url
        self.title_tag = title_tag
        self.body_tag = body_tag

class Crawler:

    def __init__(self, site):
        self.site = site
        self.visited = []

    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, page_obj, selector):
        selected_elems = page_obj.select(selector)
        if selected_elems is not None and len(selected_elems) > 0:
            return '\n'.join([elem.get_text() for elem in selected_elems])
        return ''

    def parse(self, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, self.site.title_tag)
            body = self.safeGet(bs, self.site.body_tag)
            if title != '' and body != '':
                content = Content(url, title, body)
                print(content)

    def crawl(self):
        # get pages from website home page
        bs = self.getPage(self.site.url)
        target_pages = bs.findAll('a', 
                                  href=re.compile(self.site.target_pattern))
        for target in target_pages:
            target = target.attrs['href']
            if target not in self.visited:
                self.visited.append(target)
                if not self.site.abs_url:
                    target = '{}{}'.format(self.site.url, target)
                self.parse(target)

reuters = Website('Reuters', 'https://www.reuters.com', '^(/article/)', False, 'h1', 'div.StandardArticleBody_body_1gnLA')
crawler  = Crawler(reuters)
crawler.crawl()
