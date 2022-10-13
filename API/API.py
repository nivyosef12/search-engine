# TODO
# 1.deal with empty str on search bar

from fastapi import FastAPI, Request, Form, status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from database.database import get_db_client_connection

templates = Jinja2Templates(directory="../templates")
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
    return templates.TemplateResponse("search_results.html", context)

# if len(search_results) == 0 or search_bar == '':
#    url = app.url_path_for("home")
#    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)  # changing from post route to get route
