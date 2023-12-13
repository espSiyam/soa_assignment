from fastapi import FastAPI, Request, Form
import json
import uvicorn
from rdflib import Graph
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta
import random
import requests
from utils import make_rig, get_rdg_properties
import re

HOST = "127.0.0.2"
PORT = 5000


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.post("/")
async def query(request: Request,
                url: str = Form(...),
                bookedBy: str = Form(...), 
                hasPlaces: str = Form(...),
                hasBedrooms: str = Form(...),
                distanceToLake: str = Form(...),
                city: str = Form(...),
                nearestCity:int = Form(...),
                bookingStartDate: str = Form(...),
                bookingDuration: int = Form(...),
                maxShift: int = Form(...)):
    print(url, bookedBy, hasPlaces, hasBedrooms)
    response = requests.get(url)
    # rdg_file =
    with open('temp_rdg.ttl', 'wb') as file:  # Replace 'filename.ext' with the desired file name
        file.write(response.content)
    properties = get_rdg_properties("temp_rdg.ttl")
    print("Hello Properties",properties)
    dic = {}
    
    return templates.TemplateResponse("index_sswap2.html", {"request": request})


@app.get("/")
async def view_page(request: Request):
    return templates.TemplateResponse("index_sswap2.html", {"request": request})

if __name__ == '__main__':
    uvicorn.run("mediator:app",reload=True, port=PORT, host=HOST)