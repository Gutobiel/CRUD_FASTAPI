from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
import models
from database.database import engine, sessionlocal
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import models.models



models.models.Base.metadata.create_all(bind=engine)
 
templates = Jinja2Templates(directory="templates")
 
app = FastAPI()
 
app.mount("/static", StaticFiles(directory="static"), name="static")
 
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    veiculos = db.query(models.models.Veiculo).order_by(models.models.Veiculo.id.desc())
    return templates.TemplateResponse("C:\Users\augusto.santos\OneDrive/-/Dataeasy\Área/de/Trabalho\fastapi_crud\templates", {"request": request, "veiculos": veiculos})

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

@app.get("/edit/{veiculo_id}")
async def edit(request: Request, veiculo_id: int, db: Session = Depends(get_db)):
    veiculos = db.query(models.models.Veiculo).filter(models.models.Veiculo.id == veiculo_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "veiculos": veiculos})

@app.post("/update/{veiculo_id}")
async def update(request: Request, veiculo_id: int, marca: str = Form(...), modelo: str = Form(...), cor: str = Form(...), db: Session = Depends(get_db)):
    veiculos = db.query(models.models.Veiculo).filter(models.models.Veiculo.id == veiculo_id).first()
    veiculos.marca = marca
    veiculos.modelo = modelo
    veiculos.cor = cor
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{veiculo_id}")
async def delete(request: Request, veiculo_id: int, db: Session = Depends(get_db)):
    veiculos = db.query(models.models.Veiculo).filter(models.models.Veiculo.id == veiculo_id).first()
    db.delete(veiculos)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)