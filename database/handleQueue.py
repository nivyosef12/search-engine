# TODO list
# 1.handle visited websites
# 2.do not insert "cannot find" and etc web pages (404, 403, ...)
# 3.thoughts about creating a 'description' index and searching there to while considering the ranking

from queue import Queue
import pymongo
import re


class handleQueue:
    def __init__(self, mongo_client):
        self.queue = Queue(0)  # infinite size
        self.collection = mongo_client["search_engine"]["search_results"]  # [db][collection]
        self.pattern = "^[a-zA-Z0-9@#&*()—'?|/\:!,.\s-]+$"

    def add(self, result):
        print("Added ", result['title'])
        self.queue.put(result)

    def insert_to_database(self):
        # create index for efficient search query
        self.collection.create_index([
            ('title', pymongo.TEXT)],
            name='search_results', default_language='english')

        while True:
            result = self.queue.get()  # if queue is empty, wait until an item is available
            # ignore non English web pages
            if not re.search(self.pattern, result['title']):
                print("!!!! NOT ENG !!!! ", result['title'])
                continue

            # visited web page
            # TODO find better way to do that - something like cursor.size()
            # if len(list(self.collection.find({'$text': {'$search': result['title']}}))) != 0:
            #    continue

            # insets information to database
            self.collection.insert_one(result)
            print("Inserted: ", result['title'])


