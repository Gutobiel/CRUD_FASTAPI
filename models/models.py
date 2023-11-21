from sqlalchemy import Boolean, Column, Integer, String
from database.database import Base

class Veiculo(Base):
    __tablename__ = 'veiculos'
    id = Column(Integer, primary_key=True)
    placa = Column(String(200))
    marca = Column(String(200))
    modelo = Column(String(200))
    cor = Column(String(200))
    favorito = Column(Boolean, default=False)

def __repr__(self):
    return '<Veiculo %r>' % (self.id)
