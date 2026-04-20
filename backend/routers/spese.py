from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas import SpesaCreate, SpesaOut
from typing import List, Optional
from datetime import date as DateType

router = APIRouter(prefix="/api/spese", tags=["Spese"])


#Leggiamo tutte le spese
@router.get("/", response_model=List[SpesaOut])
def get_spese(
    categoria: Optional[str] = None,
    data_inizio: Optional[DateType] = None,
    data_fine: Optional[DateType] = None,
    descrizione: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Spesa)

    if categoria:
        query = query.filter(models.Spesa.categoria == categoria)
    if data_inizio:
        query = query.filter(models.Spesa.data >= data_inizio)
    if data_fine:
        query = query.filter(models.Spesa.data <= data_fine)
    if descrizione:
        query = query.filter(models.Spesa.descrizione.ilike(f"%{descrizione}%"))

    return query.order_by(models.Spesa.data.desc()).all()



#Leggiamo spesa per categoria
@router.get("/categoria/{categoria}", response_model=List[SpesaOut])
def get_spese_per_categoria(categoria:str, db:Session = Depends(get_db)):
    spesa = db.query(models.Spesa).filter(models.Spesa.categoria == categoria).all()
    if not spesa:
        raise HTTPException(status_code=404, detail="Spesa non trovata")
    return spesa

#Creiamo una nuova spesa
@router.post("/", response_model=SpesaOut)
def create_spesa(spesa: SpesaCreate, db:Session = Depends(get_db)):
    nuova_spesa = models.Spesa(**spesa.model_dump()) #crea una nuova spesa usando i dati del modello SpesaCreate, model_dump() converte il modello in un dizionario
    db.add(nuova_spesa) #aggiunge la nuova spesa alla sessione del database
    db.commit() #salva le modifiche al database
    db.refresh(nuova_spesa) #aggiorna la nuova spesa con i dati del database, ad esempio l'id generato automaticamente
    return nuova_spesa #restituisce la nuova spesa creata


#eliminiamo una spesa
@router.delete("/{spesa_id}")
def delete_spesa(spesa_id:int, db:Session = Depends(get_db)):
    spesa = db.query(models.Spesa).filter(models.Spesa.id == spesa_id).first() #trova la spesa con l'id specificato
    if not spesa:
        raise HTTPException(status_code=404, detail = "Spesa non trovata") 
    db.delete(spesa) #elimina la spesa trovata
    db.commit() #salva le modifiche al database
    return {"detail": "Spesa eliminata con successo"}