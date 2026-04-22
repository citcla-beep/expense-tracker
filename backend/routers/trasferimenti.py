from typing import List
from database import get_db
from datetime import date
import models
from schemas import TrasferimentoCreate, TrasferimentoOut
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/trasferimenti", tags=["Trasferimenti"])

@router.get("/", response_model=List[TrasferimentoOut])
def leggi_trasferimenti(db:Session=Depends(get_db)):
    trasferimenti = db.query(models.Trasferimento).order_by(models.Trasferimento.data.desc()).all()
    return trasferimenti


@router.post("/", response_model=TrasferimentoOut)
def crea_trasferimento(trasferimento:TrasferimentoCreate, db:Session=Depends(get_db)):
    conto_origine = db.query(models.Conto).filter(models.Conto.id == trasferimento.conto_origine_id).first()
    conto_destinazione = db.query(models.Conto).filter(models.Conto.id == trasferimento.conto_destinazione_id).first()

    if not conto_origine or not conto_destinazione:
        raise HTTPException(status_code=404, detail="Conto mittente o destinatario non trovato")

    if trasferimento.conto_origine_id == trasferimento.conto_destinazione_id:
        raise HTTPException(status_code=400, detail="Il conto mittente e destinatario devono essere diversi")
    
    nuovo_trasferimento = models.Trasferimento(**trasferimento.model_dump())
    db.add(nuovo_trasferimento)
    db.commit()
    db.refresh(nuovo_trasferimento)
    return nuovo_trasferimento  


@router.delete("/{trasferimento_id}")
def elimina_trasferimento(trasferimento_id :int, db:Session=Depends(get_db)):
    trasferimento = db.query(models.Trasferimento).filter(models.Trasferimento.id == trasferimento.id).first()
    if not trasferimento:
        raise HTTPException(status_code=404, detail="Trasferimento non trovato")
    db.delete(trasferimento)
    db.commit()
    return {"detail": "Trasferimento eliminato con successo"}