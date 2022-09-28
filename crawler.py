# TODO
# 1. crawl to "better" urls
# 2. thoughts about using multi threaded concepts, and have couple of crawlers crawling through the internet
# 3. exclude class=image links ??

#
# web crawler
#
import requests
import pymongo
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Crawler:

    def __init__(self, mongo_client):
        self.collection = mongo_client["search_engine"]["search_results"]  # [db][collection]
        self.text_tags = ['p']  # paragraph
        self.data = []

    def crawl(self, url, depth, visited_urls):
        if depth < 0 or url in visited_urls:
            return
        visited_urls.add(url)
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
            if title == "404 Not Found" or title == "403 Forbidden":
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

        # insets information to database
        self.collection.insert_one(result)
        self.collection.create_index([
            ('url', pymongo.TEXT),
            ('title', pymongo.TEXT),
            ('description', pymongo.TEXT)],
            name='search_results', default_language='english')

        # don't extract links when depth == 0
        if depth == 0:
            return

        for link in self.get_links(content, url):
            try:
                self.crawl(link, depth - 1, visited_urls)
            except Exception as e:
                print("exception is")
                print(e)
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

    def to_string(self):
        for dat in self.data:
            print(dat['title'], "\n\n", dat['url'], "\n\n", dat['description'], "\n\n")
        print(len(self.data))


# self.data.append(result) -  or len(self.data) > 100

