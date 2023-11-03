#Importar automaticamente uma lista fixa de carros

from fastapi import FastAPI, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from utils.dados import veiculos  # Importe os veículos do arquivo dados.py

app = FastAPI(debug=True)

# Modelo Pydantic para validação
class CarCreate(BaseModel):
    marca: str
    modelo: str
    cor: str

# Inicialize a lista de veículos com os dados importados
veiculos = veiculos

# Operação de Create (POST)
@app.post("/add")
async def add_car(car_data: CarCreate):
    veiculos.append(car_data.dict())
    return JSONResponse(content=car_data.dict(), status_code=status.HTTP_201_CREATED)

# ... Outras operações CRUD ...
