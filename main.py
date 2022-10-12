# TODO
# 1.wait for threads to terminate before closing the db connection
# 2.ranking
# 3.list of links or different threads?

import crawler as cr
import uvicorn
import threading
from database import get_db_client_connection

start_url1 = 'https://en.wikipedia.org/wiki/Sport'
start_url2 = 'https://en.wikipedia.org/wiki/Google'
start_url3 = 'https://www.imdb.com/'

try:
    client = get_db_client_connection()
except ConnectionError:
    print("ERROR, failed to connect to database")
    exit(1)


if __name__ == "__main__":
    crawler = cr.Crawler(client)
    crawler_thread1 = threading.Thread(target=crawler.crawl, args=(start_url1, 5))
    crawler_thread2 = threading.Thread(target=crawler.crawl, args=(start_url2, 5))
    crawler_thread3 = threading.Thread(target=crawler.crawl, args=(start_url3, 5))
    crawler_thread1.start()
    crawler_thread2.start()
    crawler_thread3.start()

    # uvicorn.run("API:app", host="127.0.0.1", port=8000, reload=False)

    crawler_thread1.join()
    crawler_thread2.join()
    crawler_thread3.join()
    # client["search_engine"]["search_results"].delete_many({})
    client.close()
