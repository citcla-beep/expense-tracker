from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from datetime import date
from database import Base

class Categoria(Base):
    __tablename__ = "categorie"
    id   = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)

class Fonti(Base):
    __tablename__ = "fonti"
    id   = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)

# Conto PRIMA di Spesa, Entrata e Trasferimento
class Conto(Base):
    __tablename__ = "conti"
    id             = Column(Integer, primary_key=True, index=True)
    nome           = Column(String, nullable=False)
    saldo_iniziale = Column(Float, default=0.0)

class Spesa(Base):
    __tablename__ = "spese"
    id          = Column(Integer, primary_key=True, index=True)
    importo     = Column(Float, nullable=False)
    categoria   = Column(String, nullable=False)
    descrizione = Column(String, nullable=True)
    data        = Column(Date, default=date.today)
    conto_id    = Column(Integer, ForeignKey("conti.id"), nullable=True)  # "conti.id" non "conto.id"

    @property
    def tipo(self):
        if self.data and self.data > date.today():
            return "futura"
        return "effettiva"

class Entrata(Base):
    __tablename__ = "entrate"  # plurale
    id          = Column(Integer, primary_key=True, index=True)
    importo     = Column(Float, nullable=False)
    fonte       = Column(String, nullable=False)
    descrizione = Column(String, nullable=True)
    data        = Column(Date, default=date.today)
    conto_id    = Column(Integer, ForeignKey("conti.id"), nullable=True)  # "conti.id" non "conto.id"

class Trasferimento(Base):
    __tablename__ = "trasferimenti"
    id                    = Column(Integer, primary_key=True, index=True)
    importo               = Column(Float, nullable=False)
    conto_origine_id      = Column(Integer, ForeignKey("conti.id"), nullable=False)
    conto_destinazione_id = Column(Integer, ForeignKey("conti.id"), nullable=False)
    descrizione           = Column(String, nullable=True)
    data                  = Column(Date, default=date.today)