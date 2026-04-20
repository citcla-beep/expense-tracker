from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas import EntrataCreate, EntrataOut
from typing import List


router = APIRouter(prefix="/api/entrate", tags=["Entrate"])

#Leggiamo tutte le entrate
@router.get("/", response_model=List[EntrataOut])
def get_entrate(db:Session=Depends(get_db)):
    return db.query(models.Entrata).all()


#Leggiamo per fonte
@router.get("/fonte/{fonte}", response_model=List[EntrataOut])
def get_entrate_per_fonte(fonte:str, db:Session=Depends(get_db)):
    entrata = db.query(models.Entrata).filter(models.Entrata.fonte == fonte).all()
    if not entrata:
        raise HTTPException(status_code=404, detail="Entrata non trovata")
    return entrata

#Creiamo una nuova entrata
@router.post("/", response_model=EntrataOut)
def create_entrata( entrata : EntrataCreate, db : Session = Depends(get_db)):
    nuova_entrata = models.Entrata(**entrata.model_dump()) #crea una nuova entrata usando i dati del modello EntrataCreate, model_dump() converte il modello in un dizionario
    db.add(nuova_entrata) #aggiunge la nuova entrata alla sessione del database
    db.commit() #salva le modifiche al database
    db.refresh(nuova_entrata) #aggiorna la nuova entrata con i dati del database, ad esempio l'id generato automaticamente
    return nuova_entrata #restituisce la nuova entrata creata

@router.delete("/{entrata_id}")
def delete_entrata(entrata_id:int, db:Session = Depends(get_db)):
    entrata = db.query(models.Entrata).filter(models.Entrata.id == entrata_id).first() #trova la spesa con l'id specificato
    if not entrata:
        raise HTTPException(status_code=404, detail = "Entrata non trovata") 
    db.delete(entrata) #elimina la spesa trovata
    db.commit() #salva le modifiche al database
    return {"detail": "Entrata eliminata con successo"}