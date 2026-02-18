# # app/main.py
# from fastapi import FastAPI, Request, Response, status
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from app1.routes import generate, scan

# app = FastAPI()

# # Set up Jinja2 templates
# templates = Jinja2Templates(directory="./templates")

# app.include_router(generate.router, prefix="/ticket")
# app.include_router(scan.router, prefix="/ticket") 

# @app.get("/", response_class=HTMLResponse, tags=["Main"])
# async def read_root(res: Response, request: Request):
#     res.status_code = status.HTTP_200_OK
#     return templates.TemplateResponse("main.html", {"request": request})

# Import required modules
from app1.app import app
import uvicorn

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)