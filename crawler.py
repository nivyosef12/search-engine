#
# web scrawler
#
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

start_url = 'https://stackoverflow.com/questions/'
# start_url = 'https://en.wikipedia.org/wiki/Main_Page'
text_tags = ['p', 'div', 'h']
data = []


def crawl(url, depth, visited_urls):
    if len(data) > 5 or url in visited_urls:  # just t make it stop fast
        return
    visited_urls.add(url)  # should be global var??
    try:
        response = requests.get(url)  # get the url web page
        print('crawling url: %s, at depth %d\n' % (url, depth))
    except (requests.exceptions.ConnectionError, requests.exceptions.SSLError):
        print('ERROR, failed to preform requests.get(%s)' % url)
        return

    content = BeautifulSoup(response.text, "html.parser")  # represents the document as a nested data structure

    try:
        title = content.find('title').text
        description = ''
        for tag in content.findAll():
            if tag.name in text_tags:
                description += tag.text.strip().replace('\n', '')
    except:
        return

    result = {
        'url': url,
        'title': title,
        'description': description
    }
    data.append(result)
    # print('\n\nRETURN\n\n', json.dumps(result, indent=2))
    if depth == 0:
        return

    try:
        links = content.findAll('a')
    except:
        return

    for link in links:
        try:
            href = link['href']
            url_parse = urlparse(url)
            # handling different types of links
            if href[0:1] == '/' and href[0:2] != '//':
                href = url_parse.scheme + "://" + url_parse.netloc + href
            elif href[0:2] == '//':
                href = url_parse.scheme + ":" + href
            elif href[0:2] == './':
                href = url_parse.scheme + "://" + url_parse.netloc + url_parse.path + href[1:]
            elif href[0:1] == '#':
                href = url_parse.scheme + "://" + url_parse.netloc + url_parse.path + href
            elif href[0:3] == '../':
                href = url_parse.scheme + "://" + url_parse.netloc + "/" + href
            elif href[0:11] == 'javascript:':
                continue  # ignore
            crawl(href, depth - 1, visited_urls)
        except:
            print("ERR")
            pass
    return


crawl(start_url, 1, set())
for dat in data:
    print(dat['title'], "\n", dat['url'], "\n", dat['description'], "\n")
print(len(data))
