# Import required modules
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app1.routes import generate, scan
from fastapi.middleware.cors import CORSMiddleware
from app1.routes.scan import router as scan_router

# Initialize the FastAPI application
app = FastAPI()

# CORS configuration
# Specifying allowed origins for cross-origin requests, including common local development URLs.
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8001",
    "http://127.0.0.1:5500"
]

# Adding CORS middleware
# Allowing all origins, credentials, methods, and headers for handling cross-origin requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Including routers for the application modules
app.include_router(generate.router, prefix="/ticket")
app.include_router(scan.router, prefix="/ticket") 
app.include_router(scan_router)

# Welcome Endpoint
@app.get("/greating", tags=["Welcome & Health"])
def greating(): 
    return "Welcome in Ticket Scanning System."

# Health Check Endpoint
@app.get("/health", tags=["Welcome & Health"])
async def health_check(): # Add a lightweight check for the database or other services
    try:
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# Set up Jinja2 templates
templates = Jinja2Templates(directory="./templates")

# Main page endpoint rendering the main.html template
@app.get("/", response_class=HTMLResponse, tags=["Welcome & Health"])
async def read_root(res: Response, request: Request):
    res.status_code = status.HTTP_200_OK
    return templates.TemplateResponse("main.html", {"request": request})