import os
import pymongo

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
print(f"{db_user} : {db_password}")
conn_str = "mongodb+srv://" + str(db_user) + ":" + str(
    db_password) + "@cluster0.xb6fgqb.mongodb.net/?retryWrites=true&w=majority"
try:
    client = pymongo.MongoClient(conn_str)
    db = client["search_engine"]
    collection = db["search_results"]
except:
    client = None


def get_db_client_connection():
    if client is None:
        raise ConnectionError
    return client
