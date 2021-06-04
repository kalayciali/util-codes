import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

csvFile = open('test.csv', 'w+')
try:
    writer = csv.writer(csvFile)
    writer.writerow(('number', 'number plus 2', 'number times 2'))
    for i in range(10):
        writer.writerow((i, i + 2, i * 2))
finally:
    csvFile.close()

# wikipedia table parsing
URL = 'http://en.wikipedia.org/wiki/Comparison_of_text_editors'
html = urlopen(URL)
bs = BeautifulSoup(html, 'html.parser')
table = bs.findAll('table', {'class': 'wikitable'})[0]
rows = table.findAll('tr')
csvFile = open('editors.csv', 'wt+')
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)
finally:
    csvFile.close()
