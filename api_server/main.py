from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from api_server.mail.mail import send_email
from api_server.scraper.boostbot_scraper import run_selenium_scraper
from api_server.search.search import run_search_tool

app = FastAPI()

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class SeleniumRequest(BaseModel):
    category: str

@app.post("/run_selenium")
def run_selenium_endpoint(request: SeleniumRequest):
    print("starting selenium...")
    try:
        result = run_selenium_scraper(request.category)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SearchRequest(BaseModel):
    query: str

@app.post("/run_search")
def run_search_endpoint(request: SearchRequest):
    try:
        result = run_search_tool(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Definition of the email request model
class EmailRequest(BaseModel):
    sender_email: str
    receiver_email: str
    subject: str
    text: str

# Endpoint for sending emails
@app.post("/send_email")
def send_email_endpoint(request: EmailRequest):
    try:
        # Here, you should call your send_email function (or whatever its name is)
        # Make sure the function is defined and performs the required task
        result = send_email(request.sender_email, request.receiver_email, request.subject, request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#python -m uvicorn api_server.main:app --reload --port 8001
