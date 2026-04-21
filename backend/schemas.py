from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional
from enum import Enum


class SpesaCreate(BaseModel):
    importo: float
    categoria: str  # torna ad essere una stringa libera
    descrizione: Optional[str] = None
    data: date = date.today()

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

    model_config = {"from_attributes": True}


# --- ENTRATE ---
class FonteEntrata(str, Enum):
    stipendio      = "Stipendio"
    regalo         = "Regalo"
    investimento    = "Investimento"
    altro          = "Altro"

class EntrataCreate(BaseModel):
    importo: float
    fonte: FonteEntrata
    descrizione: Optional[str] = None
    data: date = date.today()

    @field_validator("importo")
    @classmethod
    def importo_positivo(cls, v):
        if v <= 0:
            raise ValueError("L'importo deve essere maggiore di zero")
        return abs(v)


class EntrataOut(BaseModel):
    id: int
    importo: float
    fonte: FonteEntrata
    descrizione: Optional[str]
    data: date

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