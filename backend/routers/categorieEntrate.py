from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas import FontiCreate, FontiOut
from typing import List

router = APIRouter(prefix="/api/fonti", tags=["Fonti"])


@router.get("/", response_model=List[FontiOut])
def get_fonti(db: Session = Depends(get_db)):
    return db.query(models.Fonti).order_by(models.Fonti.nome).all()


@router.post("/", response_model=FontiOut)
def create_fonte(fonte: FontiCreate, db: Session = Depends(get_db)):
    # Controlla se esiste già
    esistente = db.query(models.Fonti).filter(
        models.Fonti.nome == fonte.nome
    ).first()
    if esistente:
        raise HTTPException(status_code=400, detail="Fonte già esistente")

    nuova = models.Fonti(nome=fonte.nome)
    db.add(nuova)
    db.commit()
    db.refresh(nuova)
    return nuova


@router.delete("/{fonte_id}")
def delete_fonte(fonte_id: int, db: Session = Depends(get_db)):
    fonte = db.query(models.Fonti).filter(
        models.Fonti.id == fonte_id
    ).first()
    if not fonte:
        raise HTTPException(status_code=404, detail="Fonte non trovata")
    db.delete(fonte)
    db.commit()
    return {"messaggio": "Fonte eliminata"}