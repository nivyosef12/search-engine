import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Crawler:
    def __init__(self, handle_queue):
        self.handle_queue = handle_queue
        self.text_tags = ['p']  # paragraph

    def crawl(self, url, depth):
        if depth < 0:
            return
        try:
            response = requests.get(url)  # get the url web page
            print(f"crawling url: {url}, at depth {depth}\n")
        except:
            print(f"ERROR, failed to preform requests.get({url})\n")
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
            print(f"Couldn't extract content of {url}")
            return

        result = {
            'url': url,
            'title': title,
            'description': description
        }
        self.handle_queue.add(result)

        # don't extract links when depth == 0
        if depth == 0:
            return

        # crawl recursively
        for link in self.get_links(content, url):
            self.crawl(link, depth - 1)

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

