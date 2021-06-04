from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article

class ArticleSpider(CrawlSpider):
    name = 'articlePipelines'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [Rule(LinkExtractor(allow=r'^.*(/wiki/)((?!:).)*$'),
                  callback='parse_items', follow=True),
             ]

    def parse_items(self, response):
        # do less work as possible
        # return item obj
        article = Article()
        title = response.css('h1::text').extract_first()
        article['url'] = response.url
        article['title'] = title
        article['text'] = response.xpath('//div[@id="mw-content-text"]//text()').extract()
        lastUpdated = response.css('li#footer-info-lastmod::text').extract_first()
        article['lastUpdated'] = lastUpdated
        return article
        

