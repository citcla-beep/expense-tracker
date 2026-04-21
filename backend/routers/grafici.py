from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas import SpesePerCategoria, EntrateVsSpese, AndamentoSaldo
from typing import List
from datetime import date, timedelta
from sqlalchemy import func

router = APIRouter(prefix="/api/grafici", tags=["Grafici"])


@router.get("/spese-per-categoria", response_model=List[SpesePerCategoria])
def spese_per_categoria(
    data_inizio: date = date.today() - timedelta(days=30),
    data_fine: date = date.today(),
    db: Session = Depends(get_db)
):
    risultato = db.query(
        models.Spesa.categoria,
        func.sum(models.Spesa.importo).label("totale")
    ).filter(
        models.Spesa.data >= data_inizio,
        models.Spesa.data <= data_fine
    ).group_by(models.Spesa.categoria).all()

    return [SpesePerCategoria(categoria=categoria, totale=totale) for categoria, totale in risultato]


@router.get("/entrate-vs-spese", response_model=List[EntrateVsSpese])
def entrate_vs_spese(
    data_inizio: date = date.today() - timedelta(days=30),
    data_fine: date = date.today(),
    db: Session = Depends(get_db)
):
    entrate_sub = db.query(
        func.strftime("%Y-%m", models.Entrata.data).label("mese"),
        func.sum(models.Entrata.importo).label("totale_entrate")
    ).filter(
        models.Entrata.data >= data_inizio,
        models.Entrata.data <= data_fine
    ).group_by("mese").subquery()

    spese_sub = db.query(
        func.strftime("%Y-%m", models.Spesa.data).label("mese"),
        func.sum(models.Spesa.importo).label("totale_spese")
    ).filter(
        models.Spesa.data >= data_inizio,
        models.Spesa.data <= data_fine
    ).group_by("mese").subquery()

    risultato = db.query(
        entrate_sub.c.mese,
        entrate_sub.c.totale_entrate,
        spese_sub.c.totale_spese
    ).outerjoin(spese_sub, entrate_sub.c.mese == spese_sub.c.mese).all()

    return [
        EntrateVsSpese(
            mese=mese,
            entrate=totale_entrate or 0,
            spese=totale_spese or 0
        )
        for mese, totale_entrate, totale_spese in risultato
    ]


@router.get("/andamento-saldo", response_model=List[AndamentoSaldo])
def andamento_saldo(
    data_inizio: date = date.today() - timedelta(days=30),
    data_fine: date = date.today(),
    db: Session = Depends(get_db)
):
    entrate_sub = db.query(
        models.Entrata.data.label("data"),
        func.sum(models.Entrata.importo).label("totale_entrate")
    ).filter(
        models.Entrata.data >= data_inizio,
        models.Entrata.data <= data_fine
    ).group_by(models.Entrata.data).subquery()

    spese_sub = db.query(
        models.Spesa.data.label("data"),
        func.sum(models.Spesa.importo).label("totale_spese")
    ).filter(
        models.Spesa.data >= data_inizio,
        models.Spesa.data <= data_fine
    ).group_by(models.Spesa.data).subquery()

    risultato = db.query(
        entrate_sub.c.data,
        entrate_sub.c.totale_entrate,
        spese_sub.c.totale_spese
    ).outerjoin(spese_sub, entrate_sub.c.data == spese_sub.c.data).all()

    return [
        AndamentoSaldo(
            data=data,
            saldo=(totale_entrate or 0) - (totale_spese or 0)
        )
        for data, totale_entrate, totale_spese in risultato
    ]