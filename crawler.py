#
# web scrawler
#

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

start_url = 'https://stackoverflow.com/questions/'


def crawl(url):
    try:
        response = requests.get(url)  # get the url web page
    except (requests.exceptions.ConnectionError, requests.exceptions.SSLError):
        print('ERROR, given url: "%s" is not available' % url)
        return
    content = BeautifulSoup(response.text, "html.parser")  # represents the document as a nested data structure
    links = content.findAll('a', {'class': 's-link'})  # ignore javascript links
    description = content.findAll('div', {'class': 's-post-summary--content-excerpt'})
    for link_ in links:
        link = link_['href']
        url_parse = urlparse(url)
        print(url_parse.path)
        # handling different types of links
        if link[0:1] == '/' and link[0:2] != '//':
            link = url_parse.scheme + "://" + url_parse.netloc + link
        elif link[0:2] == '//':
            link = url_parse.scheme + ":" + link
        elif link[0:2] == './':
            link = url_parse.scheme + "://" + url_parse.netloc + url_parse.path + link[1:]
        elif link[0:1] == '#':
            link = url_parse.scheme + "://" + url_parse.netloc + url_parse.path + link
        elif link[0:3] == '../':
            link = url_parse.scheme + "://" + url_parse.netloc + "/" + link
        elif link[0:11] == 'javascript:':
            continue  # ignore
        print(link)


crawl(start_url)
'''
links = content.findAll('a', {'class': 's-link'}, text=lambda s: s != None)  # ignore javascript links
for index in range(0, len(description)):
question = {
            'title': links[index].text,
            'url': links[index]['href'],
            'description': description[index].text.strip().replace('\n', '')
        }
        print("\n\n" + str(question))
'''
