# TODO
# 1.deal with empty str on search bar
# 2.deal with 0 matches from search
# 3.search only by title?

from fastapi import FastAPI, Request, Form, status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from database import get_db_client_connection

templates = Jinja2Templates(directory="templates")
app = FastAPI()

try:
    client = get_db_client_connection()
except ConnectionError:
    print("ERROR, failed to connect to database")
    # client = None
    exit(1)

collection = client["search_engine"]["search_results"]


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.post("/search_results")
def search(request: Request, search_bar: str = Form(...)):
    search_results = []
    for x in collection.find({'$text': {'$search': search_bar}}):
        result = {
            'url': x['url'],
            'title': x['title'],
            'description': x['description']
        }
        search_results.append(result)
    context = {"request": request, "search_results": search_results, "num_of_results": len(search_results)}
    return templates.TemplateResponse("base.html", context)


# uvicorn.run(app, host="127.0.0.1", port=8000)


