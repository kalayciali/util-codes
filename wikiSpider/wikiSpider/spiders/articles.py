from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article

class ArticleSpider(CrawlSpider):
    name = 'articles'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [Rule(LinkExtractor(allow=r'^.*(/wiki/)((?!:).)*$'),
                  callback='parse_items', cb_kwargs={'is_article': True},
                  follow=True),
             # if there is callback func follow is False by default
             Rule(LinkExtractor(allow=r'.*'), callback='parse_items',
                  cb_kwargs={'is_article': False})
             ]

    def parse_items(self, response, is_article):
        # return article object to save as csv
        article = Article()
        title = response.css('h1::text').extract_first()
        article['url'] = response.url
        article['title'] = title
        article['text'] = response.xpath('//div[@id="mw-content-text"]//text()').extract()
        lastUpdated = response.css('li#footer-info-lastmod::text').extract_first()
        article['lastUpdated'] = lastUpdated.replace('this page was last edited on', '')
        return article
