# TODO
# 1. crawl to "better" urls

#
# web crawler
#
import requests
import pymongo
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Crawler:

    def __init__(self, mongo_client):
        self.collection = mongo_client["search_engine"]["search_results"]  # [db][collection]
        self.text_tags = ['p']  # paragraph
        self.data = []

    def crawl(self, url, depth, visited_urls):
        if url in visited_urls or len(self.data) > 100:
            return
        visited_urls.add(url)  # should be global var??
        try:
            response = requests.get(url)  # get the url web page
            print('crawling url: %s, at depth %d\n' % (url, depth))
        except:
            print('ERROR, failed to preform requests.get(%s)' % url)
            return

        content = BeautifulSoup(response.text, "html.parser")  # parse response

        # try to get title and description
        try:
            title = content.find('title').text
            description = ''
            for tag in content.findAll():
                if tag.name in self.text_tags:
                    description += tag.text.strip().replace('\n', '')
        except:
            return

        result = {
            'url': url,
            'title': title,
            'description': description
        }

        # insets information to database
        self.collection.insert_one(result)
        self.collection.create_index([
            ('url', pymongo.TEXT),
            ('title', pymongo.TEXT),
            ('description', pymongo.TEXT)],
            name='search_results', default_language='english')

        self.data.append(result)
        if depth == 0:
            return

        # extract all links in the current page
        links = content.findAll('a')
        for link in links:
            # try to recursively crawl to those links
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
                self.crawl(href, depth - 1, visited_urls)
            except:
                print("ERROR, couldn't parse url: %s\n" % url)
                pass

        return

    def to_string(self):
        for dat in self.data:
            print(dat['title'], "\n\n", dat['url'], "\n\n", dat['description'], "\n\n")
        print(len(self.data))



