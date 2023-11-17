from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from api_server.scraper.scraper import run_selenium_scraper

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
    try:
        result = run_selenium_scraper(request.category)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#python -m uvicorn api_server.main:app --reload --port 8001

