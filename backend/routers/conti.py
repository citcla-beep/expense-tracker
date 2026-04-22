from typing import List
from database import get_db
from datetime import date
import models
from schemas import ContoCreate, ContoOut
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/conti", tags=["Conti"])



@router.get("/", response_model=List[ContoOut])
def get_conti(db:Session=Depends(get_db)):
    return db.query(models.Conto).all()


@router.post("/", response_model=ContoOut)
def crea_conto(conto:ContoCreate, db:Session =Depends(get_db)):
    nuovo_conto = models.Conto(**conto.model_dump())
    db.add(nuovo_conto)
    db.commit()
    db.refresh(nuovo_conto)
    return nuovo_conto

@router.delete("/{conto_id}")
def delete_conto(conto_id:int, db:Session=Depends(get_db)):
    conto = db.query(models.Conto).filter(models.Conto.id == conto_id).first()
    if not conto:
        raise HTTPException(status_code=404, detail="Conto non trovato")
    db.delete(conto)
    db.commit()
    return {"detail": "Conto eliminato con successo"}

from sqlalchemy import func

from sqlalchemy import func

@router.get("/{conto_id}/saldo")
def get_saldo_conto(conto_id: int, db: Session = Depends(get_db)):
    conto = db.query(models.Conto).filter(models.Conto.id == conto_id).first()
    if not conto:
        raise HTTPException(status_code=404, detail="Conto non trovato")

    totale_entrate = db.query(func.sum(models.Entrata.importo))\
        .filter(models.Entrata.conto_id == conto_id).scalar() or 0

    totale_spese = db.query(func.sum(models.Spesa.importo))\
        .filter(models.Spesa.conto_id == conto_id)\
        .filter(models.Spesa.data <= date.today()).scalar() or 0

    trasferimenti_uscita = db.query(func.sum(models.Trasferimento.importo))\
        .filter(models.Trasferimento.conto_origine_id == conto_id).scalar() or 0

    trasferimenti_entrata = db.query(func.sum(models.Trasferimento.importo))\
        .filter(models.Trasferimento.conto_destinazione_id == conto_id).scalar() or 0

    saldo = conto.saldo_iniziale + totale_entrate - totale_spese \
            + trasferimenti_entrata - trasferimenti_uscita

    return {
        "conto": conto.nome,
        "saldo_iniziale": conto.saldo_iniziale,
        "totale_entrate": totale_entrate,
        "totale_spese": totale_spese,
        "trasferimenti_entrata": trasferimenti_entrata,
        "trasferimenti_uscita": trasferimenti_uscita,
        "saldo": saldo
    }