import crawler
import os
import pymongo

start_url = 'https://stackoverflow.com/questions/'
# start_url = 'https://en.wikipedia.org/wiki/Main_Page'


db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
conn_str = "mongodb+srv://" + str(db_user) + ":" + str(db_password) + "@cluster0.xb6fgqb.mongodb.net/?retryWrites=true&w=majority"
try:
    client = pymongo.MongoClient(conn_str)
except:
    print("ERROR, failed to connect to database")
db = client["search_engine"]
collection = db["search_results"]

crawler = crawler.Crawler(collection)
crawler.crawl(start_url, 1, set())
crawler.to_string()

client.close()
