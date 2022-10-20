import uvicorn
from database.database import get_db_client_connection


def main():
    try:
        # different connection from crawler?
        client = get_db_client_connection()
    except ConnectionError:
        print("ERROR, failed to connect to database")
        exit(1)

    uvicorn.run("API:app", host="127.0.0.1", port=8000, reload=False)
    client.close()


if __name__ == "__main__":
    main()
