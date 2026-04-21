from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas import CategoriaCreate, CategoriaOut
from typing import List

router = APIRouter(prefix="/api/categorie", tags=["Categorie"])


@router.get("/", response_model=List[CategoriaOut])
def get_categorie(db: Session = Depends(get_db)):
    return db.query(models.Categoria).order_by(models.Categoria.nome).all()


@router.post("/", response_model=CategoriaOut)
def create_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    # Controlla se esiste già
    esistente = db.query(models.Categoria).filter(
        models.Categoria.nome == categoria.nome
    ).first()
    if esistente:
        raise HTTPException(status_code=400, detail="Categoria già esistente")

    nuova = models.Categoria(nome=categoria.nome)
    db.add(nuova)
    db.commit()
    db.refresh(nuova)
    return nuova


@router.delete("/{categoria_id}")
def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(models.Categoria).filter(
        models.Categoria.id == categoria_id
    ).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria non trovata")
    db.delete(categoria)
    db.commit()
    return {"messaggio": "Categoria eliminata"}