
from pydantic import Base

class Veiculos(Base):
    id: int
    marca: str
    modelo: str
    cor: str
    placa: str

