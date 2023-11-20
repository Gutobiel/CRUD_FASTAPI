from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
import uvicorn
import models.models
from database.database import engine, sessionlocal
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from utils.dados import veiculos


models.models.Base.metadata.create_all(bind=engine)
 
templates = Jinja2Templates(directory="templates")
 
app = FastAPI(debug=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
 
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Tela Inicial"])
async def home(request: Request, db: Session = Depends(get_db)):
    veiculos = db.query(models.models.Veiculo).order_by(models.models.Veiculo.id.desc())
    totalVeiculos = db.query(func.count(models.models.Veiculo.id)).scalar()
    
    return templates.TemplateResponse("index.html", {"request": request, "veiculos": veiculos, "totalVeiculos": totalVeiculos})

@app.get("/addnew", tags=["Tela de criar"])
async def home(request: Request, db: Session = Depends(get_db)):
    veiculo = (...) # Obtenha o veículo apropriado aqui
    totalVeiculos = db.query(func.count(models.models.Veiculo.id)).scalar()
    return templates.TemplateResponse("addnew.html", {"request": request, "veiculo": veiculo, "totalVeiculos": totalVeiculos})

@app.post("/add", tags=["Criar"])
async def add(request: Request, marca: str = Form(...), modelo: str = Form(...), cor: str = Form(), db: Session = Depends(get_db)):
    # Obtém as 3 primeiras letras da marca em maiúsculas
    marca_inicial = marca[:3].upper()

    # Obtém o próximo ID
    veiculos = db.query(models.models.Veiculo).order_by(models.models.Veiculo.id.desc()).first()
    if veiculos:
        proximo_id = veiculos.id + 1
    else:
        proximo_id = 1

    # Formata o ID com um mínimo de 3 dígitos e cria a placa
    id_formatado = f"{proximo_id:03d}"
    placa = f"{marca_inicial}-{id_formatado}"

    # Crie um novo registro no banco de dados
    veiculo = models.models.Veiculo(placa=placa, marca=marca, modelo=modelo, cor=cor)
    db.add(veiculo)
    db.commit()

    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/edit/{veiculo_id}", tags=["Tela de editar"])
async def edit(request: Request, veiculo_id: int, db: Session = Depends(get_db)):
    veiculos = db.query(models.models.Veiculo).filter(models.models.Veiculo.id == veiculo_id).first()
    totalVeiculos = db.query(func.count(models.models.Veiculo.id)).scalar()
    return templates.TemplateResponse("edit.html", {"request": request, "veiculos": veiculos, "totalVeiculos": totalVeiculos})

@app.post("/update/{veiculo_id}", tags=["Atualizar"])
async def update(request: Request, veiculo_id: int, marca: str = Form(...), modelo: str = Form(...), cor: str = Form(), db: Session = Depends(get_db)):
    veiculo = db.query(models.models.Veiculo).filter(models.models.Veiculo.id == veiculo_id).first()
    
    # Obtém as 3 primeiras letras da marca em maiúsculas
    marca_inicial = marca[:3].upper()
    
    # Cria a placa com base na marca e no ID existente
    id_formatado = f"{veiculo.id:03d}"
    placa = f"{marca_inicial}-{id_formatado}"

    # Atualiza os campos do veículo
    veiculo.marca = marca
    veiculo.modelo = modelo
    veiculo.cor = cor
    veiculo.placa = placa
    
    db.commit()
    
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

#Deletar carro da tabela
@app.get("/delete/{veiculo_id}", tags=["Deletar"])
async def delete(request: Request, veiculo_id: int, db: Session = Depends(get_db)):
    veiculos = db.query(models.models.Veiculo).filter(models.models.Veiculo.id == veiculo_id).first()
    db.delete(veiculos)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/ver/{veiculo_id}", tags=["Tela informações do carro"])
async def delete(request: Request, veiculo_id: int, db: Session = Depends(get_db)):
    veiculo = db.query(models.models.Veiculo).filter(models.models.Veiculo.id == veiculo_id).first()
    totalVeiculos = db.query(func.count(models.models.Veiculo.id)).scalar()
    return templates.TemplateResponse("ver.html", {"request": request, "veiculos": veiculos, "totalVeiculos": totalVeiculos})

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=7777)