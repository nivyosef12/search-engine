# TODO
# 1.wrap crawler and API in threads
# 2.wait for threads to terminate before closing the db connection

import crawler as cr
import API as api
import os
import pymongo
# import dnspython

start_url = 'https://stackoverflow.com/questions/'


# start_url = 'https://en.wikipedia.org/wiki/Main_Page'

def main():
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    conn_str = "mongodb+srv://" + str(db_user) + ":" + str(db_password) + "@cluster0.xb6fgqb.mongodb.net/?retryWrites=true&w=majority"
    try:
        client = pymongo.MongoClient(conn_str)
        db = client["search_engine"]
        collection = db["search_results"]
    except:
        print("ERROR, failed to connect to database")
        return

    # crawler = cr.Crawler(collection)
    # crawler.crawl(start_url, 1, set())
    # crawler.to_string()
    # app_interface = api.API(collection)
    # app_interface.run()
    client.close()


main()