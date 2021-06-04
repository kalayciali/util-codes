from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import string
import math
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import random
import re


def getLinks(article_url):
    html = urlopen('http://en.wikipedia.org' + article_url)
    bs = BeautifulSoup(html, 'html.parser')
    title = bs.find('h1').get_text()
    content = bs.find('div', {'id': 'bodyContent'}).find('p').get_text()
    return (content, bs.find('div', {'id': 'bodyContent'}).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$')))

def getBody(article_url):
    html = requests.get('http://en.wikipedia.org' + article_url)
    return html.text


def read_file(filename):
    """ 
    we need to analyse line by line
    """
    try:
        f = open(filename, 'r')
        return f.read()
    except IOError:
        print("error")
        sys.exit()


# stop_words = list(stopwords.words('english'))

def cleanDoc(doc):
    sentence_list = sent_tokenize(doc)
    trigrams = {}
    stop_words = set(stopwords.words('english'))

    for line in sentence_list:
        translation = line.maketrans(string.punctuation+string.ascii_uppercase," " *len(string.punctuation)+string.ascii_lowercase)
        line = line.translate(translation)
        tokens = word_tokenize(line)
        tokens = [ w for w in tokens if not w in stop_words ]
        for i in range(len(tokens)-2):
            t = ( tokens[i], tokens[i+1], tokens[i+2] )
            if t in trigrams:
                trigrams[t] += 1
            else:
                trigrams[t] = 1
    print(trigrams)
    return trigrams


#def compareTrigramsFromSite(D1, D2):
#    # I will add angle calc method also
#    # I will do it now
#    same_occur = 0
#
#    for key in D1:
#        if key in D2:
#            same_occur += 1
#
#    all_size = 0
#    for val in D1.values():
#        all_size += val
#
#    for val in D2.values():
#        all_size += val
#
#    return same_occur / all_size

def inner_product(D1,D2):

    summed = 0.0
    for key in D1:
        if key in D2:
            summed += D1[key] * D2[key]
    return summed

def vector_angle(D1,D2):

    numerator = inner_product(D1,D2)
    denominator = math.sqrt(inner_product(D2,D1)*inner_product(D2,D2))
    print(denominator)
    return math.acos(numerator/denominator)

def main():
    content1, links = getLinks('/wiki/Nihilism')
    content2, links = getLinks('wiki/Philosopy')
    vector_angles = []
    try:
        while len(links) > 0:
            newArticle1 = links[random.randint(0, len(links)-1)].attrs['href']
            print(newArticle1)
            newArticle2 = links[random.randint(0, len(links)-1)].attrs['href']
            print(newArticle2)
            content1, links = getLinks(newArticle1)
            content2, links = getLinks(newArticle2)
            content1 = getBody(newArticle1)
            content2 = getBody(newArticle2)
            print(content1)
            print(content2)
            D1 = cleanDoc(content1)
            D2 = cleanDoc(content2)
            vector_angles.append(vector_angle(D1, D2))
    finally:
        print(vector_angles)

    #line_list = read_file(doc1)
    #D1 = cleanDoc(line_list)
    #line_list = read_file(doc2)
    #D2 = cleanDoc(line_list)
    #print(vector_angle(D1, D2))

if __name__ == "__main__":
    main()



