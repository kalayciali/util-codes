import requests
from bs4 import BeautifulSoup

class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def __str__(self):
        return "URL: {}\nTITLE: {}\nBODY:\n{}".format(
            self.url, self.title, self.body)

class Website:
    def __init__(self, name, url, title_tag, body_tag):
        # crawling sites through search
        self.name = name
        self.url = url
        self.title_tag = title_tag
        self.body_tag = body_tag

class Crawler:

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

    def parse(self, site, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, site.title_tag)
            body = self.safeGet(bs, site.body_tag)
            body = bs.find('div', {'class': 'post-body'}).text
            if title != '' and body != '':
                content = Content(url, title, body)
                print(content)

crawler = Crawler()
siteData = [
['O\'Reilly Media', 'http://oreilly.com',
'h1', 'section#product-description'],
['Reuters', 'http://reuters.com', 'h1',
'div.StandardArticleBody_body_1gnLA'],
['Brookings', 'http://www.brookings.edu',
'h1', 'div.post-body'],
['New York Times', 'http://nytimes.com',
'h1', 'p.story-content'],
]
websites = []
for row in siteData:
    websites.append(Website(row[0], row[1], row[2], row[3]))

crawler.parse(websites[2], 'https://www.brookings.edu/blog/techtank/2016/03/01/idea-to-retire-old-methods-of-policy-education/')


