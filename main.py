# TODO
# 1.wait for threads to terminate before closing the db connection
# 2.ranking
# 3.list of links or different threads?

from database.database import get_db_client_connection

try:
    client = get_db_client_connection()
except ConnectionError:
    print("ERROR, failed to connect to database")
    exit(1)


if __name__ == "__main__":
    client["search_engine"]["search_results"].delete_many({})
    client.close()



