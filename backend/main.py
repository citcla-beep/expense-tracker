from fastapi import FastAPI
from database import engine, SessionLocal
import models
from routers import spese, entrate, riepilogo, categorie, categorieEntrate, grafici
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine) #crea le tabelle nel database se non esistono già, usa il motore per collegarsi al database e creare le tabelle in base ai modelli definiti in models.py

def crea_categorie_default(db):
    categorie_default = [
        "Cibo", "Trasporti", "Casa", "Salute",
        "Svago", "Abbigliamento", "Tecnologia",
        "Sport", "Istruzione", "Altro"
    ]
    for nome in categorie_default:
        esistente = db.query(models.Categoria).filter(
            models.Categoria.nome == nome
        ).first()
        if not esistente:
            db.add(models.Categoria(nome=nome))
    db.commit()

def crea_fonti_default(db):
    fonti_default = [
         "Stipendio","Regalo", "Investimento","Altro"
    ]
    for nome in fonti_default:
        esistente = db.query(models.Fonti).filter(
            models.Fonti.nome == nome
        ).first()
        if not esistente:
            db.add(models.Fonti(nome=nome))
    db.commit()

db = SessionLocal()
crea_categorie_default(db)
crea_fonti_default(db)

db.close()

app = FastAPI(title="Expense Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(spese.router) #include il router delle spese, in questo modo tutte le rotte definite in spese.py saranno disponibili nell'applicazione
app.include_router(entrate.router) #include il router delle entrate, in questo modo tutte le rotte definite in entrate.py saranno disponibili nell'applicazione
app.include_router(riepilogo.router) #include il router del riepilogo, in questo modo tutte le rotte definite in riepilogo.py saranno disponibili nell'applicazione
app.include_router(categorie.router) #include il router delle categorie, in questo modo tutte le rotte definite in categorie.py saranno disponibili nell'applicazione
app.include_router(categorieEntrate.router) #include il router delle categorie entrate, in questo modo tutte le rotte definite in categorieEntrate.py saranno disponibili nell'applicazione
app.include_router(grafici.router) #include il router dei grafici, in questo modo tutte le rotte definite in grafici.py saranno disponibili nell'applicazione


@app.get("/")
def root():
    return {"messaggio": "Expense Tracker funziona!"}