from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract
from typing import List
from database import get_db
from datetime import date
import models
from schemas import RiepilogoEntrate, RiepilogoSpese, Riepilogo, RiepilogoSpesePianificate, MovimentoOut

router = APIRouter(prefix="/api/riepilogo", tags=["Riepilogo"]) 

#Riepilogo entrate per mese e anno
@router.get("/entrate", response_model=RiepilogoEntrate)
def riepilogo_entrate(anno:int=date.today().year, mese:int=date.today().month, db:Session = Depends(get_db)):
    entrate = db.query(models.Entrata).filter(extract("year", models.Entrata.data) == anno).filter(extract("month", models.Entrata.data) == mese).all()
    totale_entrate = sum(entrata.importo for entrata in entrate)
    return RiepilogoEntrate(mese=mese, anno=anno, totale_entrate=totale_entrate)

#Riepilogo spese per mese e anno
@router.get("/spese", response_model=RiepilogoSpese)
def riepilogo_spese(anno:int=date.today().year, mese:int=date.today().month, db:Session = Depends(get_db)):
    spese = db.query(models.Spesa).filter(extract("year", models.Spesa.data)==anno).filter(extract("month", models.Spesa.data)==mese).all()
    totale_spese = sum(spesa.importo for spesa in spese)
    return RiepilogoSpese(mese=mese, anno=anno, totale_spese=totale_spese)

#Riepilogo generale per mese e anno
@router.get("/", response_model=Riepilogo)
def riepilogo(anno:int=date.today().year, mese:int=date.today().month, db:Session = Depends(get_db)):
    entrate = db.query(models.Entrata).filter(extract("year", models.Entrata.data) == anno).filter(extract("month", models.Entrata.data) == mese).all()
    spese = db.query(models.Spesa).filter(extract("year", models.Spesa.data)==anno).filter(extract("month", models.Spesa.data)==mese).all()
    totale_entrate = sum(entrata.importo for entrata in entrate)
    totale_spese = sum(spesa.importo for spesa in spese)
    saldo = totale_entrate - totale_spese
    return Riepilogo(mese=mese, anno=anno, totale_entrate=totale_entrate, totale_spese=totale_spese, saldo=saldo)

@router.get("/spese-pianificate", response_model=   RiepilogoSpesePianificate)
def spese_pianificate(db:Session = Depends(get_db)):
    spese_pianificate = db.query(models.Spesa).filter(models.Spesa.data > date.today()).all()
    totale_spese_pianificate = sum(spesa.importo for spesa in spese_pianificate)
    return RiepilogoSpesePianificate(totale_spese_pianificate=totale_spese_pianificate, numero_spese=len(spese_pianificate))


@router.get("/ultimi-movimenti", response_model=List[MovimentoOut])
def ultimi_movimenti(limite:int=20, db:Session=Depends(get_db)):
    spese = db.query(models.Spesa).order_by(models.Spesa.data.desc()).limit(limite)
    entrate = db.query(models.Entrata).order_by(models.Entrata.data.desc()).limit(limite)

    movimenti = []
    for s in spese:
        movimenti.append(
            {
                "id" : s.id,
                "importo" : s.importo,
                "descrizione" : s.descrizione,
                "data" : s.data,
                "tipo_movimento":"spesa"
            }
        )
    for e in entrate:
        movimenti.append(
            {
                "id" : e.id,
                "importo" : e.importo,
                "descrizione" : e.descrizione,
                "data" : e.data,
                "tipo_movimento":"entrata"

            }
        )
    movimenti.sort(key=lambda x:x["data"], reverse=True)
    return movimenti[:limite]