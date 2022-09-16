import requests
from bs4 import BeautifulSoup

start_url = 'https://stackoverflow.com/questions?tab=newest&page=1'  # starts crawling from


def crawl(url):
    try:
        response = requests.get(url)  # get the start_url web page
    except requests.exceptions.SSLError:
        print('ERROR, given url: "%s" is not available' % url)
        return
    content = BeautifulSoup(response.text, "html.parser")  # represents the document as a nested data structure
    links = content.findAll('a', {'class': 's-link'})

    for link in links:
        if 'https://' not in link['href'] and link['href'] != "javascript:void(0)":
            print(link['href'])


crawl(start_url)
