# TODO
# 1.wrap crawler and API in threads
# 2.wait for threads to terminate before closing the db connection

import crawler as cr
import API as api
import uvicorn
from database import get_db_client_connection

start_url = 'https://stackoverflow.com/questions/'
# start_url = 'https://en.wikipedia.org/wiki/Main_Page'
try:
    client = get_db_client_connection()
except ConnectionError:
    print("ERROR, failed to connect to database")
    exit(1)


if __name__ == "__main__":
    # crawler = cr.Crawler(client)
    # crawler.crawl(start_url, 1, set())
    # uvicorn.run("API:app", host="127.0.0.1", port=8000, reload=True)
    client["search_engine"]["search_results"].delete_many({})
    client.close()
