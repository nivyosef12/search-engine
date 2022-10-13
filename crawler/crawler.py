# TODO
# 1. thoughts about using multi threaded crawler, and have couple of crawlers crawling through the internet
# 2. instead of visited_urls maybe check if 'title' is in the database already
# 3. do not insert "cannot find" and etc web pages
# 4. check if title is in english - reg exp
# 5. implementing a queue that insertrs to database
#
# web crawler
#
import threading

import requests
import pymongo
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


class Crawler:
    def __init__(self, mongo_client):
        self.collection = mongo_client["search_engine"]["search_results"]  # [db][collection]
        self.text_tags = ['p']  # paragraph
        self.visited_urls = set()  # shared resource
        self.lock = threading.Lock()
        self.pattern = "^[a-zA-Z0-9@#&*()—'?|/\:!,.\s-]+$"

    def crawl(self, url, depth):
        if depth < 0:
            return
        try:
            response = requests.get(url)  # get the url web page
            print('crawling url: %s, at depth %d' % (url, depth))
        except:
            print('ERROR, failed to preform requests.get(%s)' % url)
            return
        content = BeautifulSoup(response.text, "html.parser")  # parse response

        # try to get title and description
        try:
            title = content.find('title').text

            self.lock.acquire()
            if title in self.visited_urls:
                print("!!!! VISITED !!!! ", title)
                self.lock.release()  # TODO check if necessary
                return
            self.visited_urls.add(title)
            self.lock.release()

            if title == "404 Not Found" or title == "403 Forbidden" or not re.search(self.pattern, title):
                print("!!!! NOT ENG !!!! ", title)
                return

            description = ''
            for tag in content.findAll():
                if tag.name in self.text_tags:
                    description += tag.text.strip().replace('\n', '')
        except:
            print("Couldn't extract content of ", url)
            return

        result = {
            'url': url,
            'title': title,
            'description': description
        }
        print(title, "\n")
        # TODO need to lock?
        # insets information to database
        self.collection.insert_one(result)
        # create index for efficient search query
        self.collection.create_index([
            ('title', pymongo.TEXT)],
            name='search_results', default_language='english')

        # don't extract links when depth == 0
        if depth == 0:
            return

        for link in self.get_links(content, url):
            try:
                self.crawl(link, depth - 1)
            except:
                print("ERROR, couldn't crawl url: %s\n" % url)
                pass
        return

    # extract all links in the current page
    def get_links(self, content, url):
        for link in content.findAll('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path


'''

SEARCHING BY TITLE and DESCRIPTION

        self.collection.create_index([
            ('title', pymongo.TEXT),
            ('description', pymongo.TEXT)],
            name='search_results', default_language='english')

'''

