# TODO
# 1.check for concurrency between crawler(insert to db) and API(get from db)
# 2.wait for threads to terminate before closing the db connection
# 3.indexing

import crawler as cr
import API as api
import uvicorn
import threading
from database import get_db_client_connection

# start_url = 'https://stackoverflow.com/questions/'
start_url = 'https://en.wikipedia.org/wiki/Web_crawler'
try:
    client = get_db_client_connection()
except ConnectionError:
    print("ERROR, failed to connect to database")
    exit(1)


if __name__ == "__main__":
    # crawler = cr.Crawler(client)
    # crawler_thread = threading.Thread(target=crawler.crawl, args=(start_url, 3, set()))
    # crawler.crawl(start_url, 1, set())
    # crawler_thread.start()
    # uvicorn.run("API:app", host="127.0.0.1", port=8000, reload=False)
    # crawler_thread.join()
    # client["search_engine"]["search_results"].delete_many({})
    client.close()
