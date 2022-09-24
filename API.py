from fastapi import FastAPI, Request
from starlette.templating import Jinja2Templates
import uvicorn

templates = Jinja2Templates(directory="templates")
app = FastAPI()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


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
