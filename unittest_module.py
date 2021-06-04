import unittest
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
from urllib.parse import unquote

#class TestWikipedia(unittest.TestCase):
#    bs = None
#    def setUpClass(self):
#        url = 'http://en.wikipedia.org/wiki/Monty_Python'
#        TestWikipedia.bs = BeautifulSoup(urlopen(url).read(), 'html.parser')
#
#    def test_titleText(self):
#        pageTitle = TestWikipedia.bs.find('h1').get_text()
#        self.assertEqual('Monty Python', pageTitle)
#
#    def test_contentExists(self):
#        content = TestWikipedia.bs.find('div', {'id': 'mw-content-text'})
#        self.assertIsNotNone(content)

class TextWikipedia(unittest.TestCase):

    def test_PageProperties(self):
        self.url = 'http://en.wikipedia.org/wiki/Monty_Python'
        # test the 10 pages we encounter
        for i in range(1, 10):
            self.bs = BeautifulSoup(urlopen(self.url), 'html.parser')
            titles = self.titleMatchesURL()
            self.assertEqual(titles[0], titles[1])
            self.assertTrue(self.contentExists())
            self.url = self.getNextLink()
        print('Done')

    def titleMatchesURL(self):
        pageTitle = self.bs.find('h1').get_text()
        urlTitle = self.url[(self.url.index('/wiki/') + 6):]
        urlTitle = urlTitle.replace('_', ' ')
        urlTitle = unquote(urlTitle)
        return [pageTitle.lower(), urlTitle.lower()]

    def contentExists(self):
        content = self.bs.find('div', {'id': 'mw-content-text'})
        if content is not None:
            return True
        return False

    def getNextLink(self):
        links = self.bs.find('div', {'id':'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))
        randomLink = random.SystemRandom().choice(links)
        return 'https://wikipedia.org{}'.format(randomLink.attrs['href'])

if __name__ == "__main__":
    unittest.main()
