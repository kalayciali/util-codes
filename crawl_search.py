import requests
from bs4 import BeautifulSoup

class Content:
    def __init__(self, topic, url, title, body):
        self.topic = topic # query parameter
        self.url = url
        self.title = title
        self.body = body

    def __str__(self):
        return "New article for topic {}\nURL: {}\nTITLE: {}\nBODY:\n{}".format(self.topic, self.url, self.title, self.body)

class Website:
    def __init__(self, name, url, search_url, res_listing,
                 res_url, abs_url, title_tag, body_tag):
        # crawling sites through search
        self.name = name
        self.url = url
        self.search_url = search_url
        self.res_listing = res_listing
        self.res_url = res_url
        self.abs_url = abs_url
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
        child_obj = page_obj.select(selector)
        if child_obj is not None and len(child_obj) > 0:
            # to get title and body
            return child_obj[0].get_text()
        return ''

    def search(self, topic, site):
        # searches given website for given topic and records all pages found
        bs = self.getPage(site.search_url + topic)
        search_res = bs.select(site.res_listing)
        for res in search_res:
            # result url
            url = res.select(site.res_url)[0].attrs['href']
            if site.abs_url:
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print("something went wrong")
                return
            # get search result url
            title = self.safeGet(bs, site.title_tag)
            body = self.safeGet(bs, site.body_tag)
            if title != '' and body != '':
                content = Content(topic, url, title, body)
                print(content)

crawler = Crawler()
siteData = [
['O\'Reilly Media', 'http://oreilly.com',
'https://ssearch.oreilly.com/?q=','article.product-result',
'p.title a', True, 'h1', 'section#product-description'],
['Reuters', 'http://reuters.com',
'http://www.reuters.com/search/news?blob=',
'div.search-result-content','h3.search-result-title a',
False, 'h1', 'div.StandardArticleBody_body_1gnLA'],
['Brookings', 'http://www.brookings.edu',
'https://www.brookings.edu/search/?s=',
'div.list-content article', 'h4.title a', True, 'h1','div.post-body']
]
websites = []
for row in siteData:
    websites.append(Website(row[0], row[1], row[2], row[3],
                            row[4], row[5], row[6], row[7]))

topics = ['python', 'data science']
for topic in topics:
    print("getting info about: " + topic)
    for target in websites:
        crawler.search(topic, target)

