#
# stackoverflow question scrapper
#

import requests
from bs4 import BeautifulSoup

# base url
start_url = 'https://stackoverflow.com/questions/'


def fetch(url_):
    print(url_)
    try:
        response = requests.get(url_)  # get the url web page
    except (requests.exceptions.ConnectionError, requests.exceptions.SSLError):
        print('ERROR, given url: "%s" is not available' % url_)
        return
    content = BeautifulSoup(response.text, "html.parser")  # represents the document as a nested data structure
    num_of_pages = max([int(lst['title'][11:]) for lst in content.findAll('a', {'class': 's-pagination--item '
                                                                                         'js-pagination-item'})])
    # loop over stackoverflow question pages
    for page_num in range(1, num_of_pages):
        if page_num > 10:  # just for simplicity
            break
        url = url_ + "?tab=newest&page=" + str(page_num)
        print(url)

        try:
            response = requests.get(url)  # get the url web page
        except requests.exceptions.SSLError:
            print('ERROR, given url: "%s" is not available' % url)
            break

        # parse content
        content = BeautifulSoup(response.text, "html.parser")

        # extract
        links = content.findAll('a', {'class': 's-link'})
        description = content.findAll('div', {'class': 's-post-summary--content-excerpt'})

        for index in range(0, len(description)):
            question = {
                'title': links[index].text,
                'url': links[index]['href'],
                'description': description[index].text.strip().replace('\n', '')
            }
            print(question)
        print("\n\n\n")


fetch(start_url)

