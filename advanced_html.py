from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

URL = 'http://www.pythonscraping.com/pages/warandpeace.html'
html = urlopen(URL)
bs = BeautifulSoup(html.read(), 'html.parser')
name_list = bs.findAll('span', {'class': 'green'})
for name in name_list:
    print(name.get_text())
print('the prince')
name_list = bs.find_all(text='the prince')
print(len(name_list))

# navigating trees
URL = 'http://www.pythonscraping.com/pages/page3.html'
html = urlopen(URL)
bs = BeautifulSoup(html.read(), 'html.parser')

for child in bs.find('table', {'id': 'giftList'}).children:
    print(child)

for sibling in bs.find('table', {'id': 'giftList'}).tr.next_siblings:
    # it will print table rows without heading
    print(sibling)

print(bs.find('img', 
              {'src':'../img/gifts/img1.jpg'})
      .parent.previous_sibling.get_text())

# find with regex
images = bs.find_all('img',
                     {'src':re.compile('\.\.\/img\/gifts\/img.*\.jpg')})
for image in images:
    print(image['src'])

# lambda func 
tags = bs.find_all(lambda tag: len(tag.attrs) == 2)
for tag in tags:
    print(tag.get_text())

tags = bs.find_all(lambda tag: tag.get_text() == 
                   'Or maybe he\'s only resting?')



