from typing import Union
from fastapi import FastAPI
from models.Controller import Controller
from app.service import *

app = FastAPI()

from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"chauffage": "Controleur API "}

@app.post("/etat_chauffage/{etat}")
async def update_etat_chauffage(etat: bool):
    envoieFireBase(etat)
    return {"etatChauffagee : ": etat}