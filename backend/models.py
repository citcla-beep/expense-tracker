from sqlalchemy import Column, Integer, String, Float, Date
from datetime import date
from database import Base

#con sqlalchemy definiamo i modelli del database come classi che ereditano da Base, ogni classe rappresenta una tabella del database e ogni attributo rappresenta una colonna della tabella

class Spesa(Base):
    __tablename__ = "spese" #nome della tabella nel database

    id = Column(Integer, primary_key=True, index=True) #colonna id, chiave primaria, indice
    importo = Column(Float, nullable=False) #colonna importo, non può essere null
    categoria = Column(String, nullable=False) #colonna categoria, non può essere null
    descrizione = Column(String, nullable=True) #colonna descrizione, può essere null
    data = Column(Date, default=date.today) #colonna data, default è la data odierna

    # questa caratteristica è utile per distinguere le spese future da quelle effettive, se la data è maggiore di oggi allora è una spesa futura, altrimenti è una spesa effettiva
    @property
    def tipo(self):
        if self.data and self.data>date.today():
            return "futura"
        return "effettiva"

class Entrata(Base):
    __tablename__ = "entrata"

    id = Column(Integer, primary_key=True, index=True) #colonna id, chiave primaria, indice
    importo = Column(Float, nullable=False) #colonna importo, non può essere null
    fonte = Column(String, nullable=False) #colonna categoria, non può essere null
    descrizione = Column(String, nullable=True) #colonna descrizione, può essere null
    data = Column(Date, default=date.today) #colonna data, default è la data odierna