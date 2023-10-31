from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from models.models import Base
from database.database import engine, sessionlocal
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import models.models

models.models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

app = FastAPI()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
   db = sessionlocal()
   try:
       yield db
   finally:
       db.close()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add")
async def add(request: Request, marca: str = Form(...), modelo: str = Form(...), cor: str = Form(...), db: Session = Depends(get_db)):
    print(marca)
    print(modelo)
    print(cor)
    veiculos = models.models.Veiculo(marca=marca, modelo=modelo, cor=cor)
    db.add(veiculos)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})
