from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return {"???/": "!!!/"}


uvicorn.run(app, host="127.0.0.1", port=8000)

'''

class API:
    app = FastAPI()

    def __init__(self, collection):
        self.collection = collection

    # define root
    @app.get("/")
    def home(self):  # home endpoint
        return {"???/": "!!!/"}

    def run(self):
        uvicorn.run(self.app, host="127.0.0.1", port=8000)



'''
