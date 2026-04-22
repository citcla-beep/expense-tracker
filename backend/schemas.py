from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional


class SpesaCreate(BaseModel):
    importo: float
    categoria: str  # torna ad essere una stringa libera
    descrizione: Optional[str] = None
    data: date = date.today()
    conto_id :int

    @field_validator("importo")
    @classmethod
    def importo_positivo(cls, v):
        if v <= 0:
            raise ValueError("L'importo deve essere maggiore di zero")
        return abs(v)

# Aggiungi questi due schema
class CategoriaCreate(BaseModel):
    nome: str

class CategoriaOut(BaseModel):
    id: int
    nome: str

    model_config = {"from_attributes": True}

class SpesaOut(BaseModel):
    id: int
    importo: float
    categoria: str
    descrizione: Optional[str]
    data: date
    tipo: str
    conto_id :int


    model_config = {"from_attributes": True}


class EntrataCreate(BaseModel):
    importo: float
    fonte: str
    descrizione: Optional[str] = None
    data: date = date.today()
    conto_id :int


    @field_validator("importo")
    @classmethod
    def importo_positivo(cls, v):
        if v <= 0:
            raise ValueError("L'importo deve essere maggiore di zero")
        return abs(v)
    
class FontiCreate(BaseModel):
    nome: str

class FontiOut(BaseModel):
    id: int
    nome: str

    model_config = {"from_attributes": True}

class EntrataOut(BaseModel):
    id: int
    importo: float
    fonte: str
    descrizione: Optional[str]
    data: date
    conto_id :int

    model_config = {"from_attributes": True}


# --- RIEPILOGO ---
class RiepilogoEntrate(BaseModel):
    mese: int
    anno: int
    totale_entrate: float

class RiepilogoSpese(BaseModel):
    mese: int
    anno: int
    totale_spese: float

class Riepilogo(BaseModel):
    mese: int
    anno: int
    totale_entrate: float
    totale_spese: float
    saldo: float

class RiepilogoSpesePianificate(BaseModel):
    totale_spese_pianificate: float
    numero_spese: int


class MovimentoOut(BaseModel):
    id :int
    importo: float
    descrizione: str
    data: date
    tipo_movimento:str

    model_config={"from_attributes":True}

# --- GRAFICI ---
class SpesePerCategoria(BaseModel):
    categoria: str
    totale: float

class EntrateVsSpese(BaseModel):
    mese : str
    entrate:float
    spese:float

class AndamentoSaldo(BaseModel):
    data:date
    saldo:float

# -- CONTI E GIROCONTI ---
class ContoCreate(BaseModel):
    nome: str
    saldo_iniziale : float = 0.0

class ContoOut(BaseModel):
    id: int
    nome: str
    saldo_iniziale: float

    model_config = {"from_attributes": True}

class TrasferimentoCreate(BaseModel):
    importo: float
    conto_origine_id: int
    conto_destinazione_id: int  # ← era "conto_destinatario_id"
    descrizione: Optional[str] = None
    data: date = date.today()

    @field_validator("importo")
    @classmethod
    def importo_positivo(cls, v):
        if v <= 0:
            raise ValueError("L'importo deve essere maggiore di zero")
        return abs(v)

class TrasferimentoOut(BaseModel):
    id: int
    importo: float
    conto_origine_id: int
    conto_destinazione_id: int  # ← era "conto_destinatario_id"
    descrizione: Optional[str]
    data: date

    model_config = {"from_attributes": True}