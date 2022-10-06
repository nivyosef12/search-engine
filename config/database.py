import os
import pymongo

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
conn_str = "mongodb+srv://" + str(db_user) + ":" + str(
    db_password) + "@cluster0.xb6fgqb.mongodb.net/?retryWrites=true&w=majority"
try:
    client = pymongo.MongoClient(conn_str)
    # db = client["search_engine"]
    # collection = db["search_results"]
except:
    print("ERROR, failed to connect to database")
    exit(1)
