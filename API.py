# TODO
# 1.wrap API in class

from fastapi import FastAPI, Request, Form, status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
import uvicorn

templates = Jinja2Templates(directory="templates")
app = FastAPI()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.post("/search")
def search(request: Request, title: str = Form(...)):
    print(title)
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)  # changing from post route to get route


uvicorn.run(app, host="127.0.0.1", port=8000)


