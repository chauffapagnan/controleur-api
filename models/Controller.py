from pydantic import BaseModel

class Controller(BaseModel):
    etat: bool
    temperature: float
    vitesseVentilateur: float

