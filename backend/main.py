from fastapi import FastAPI
from database import engine
import models
from routers import spese, entrate, riepilogo
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine) #crea le tabelle nel database se non esistono già, usa il motore per collegarsi al database e creare le tabelle in base ai modelli definiti in models.py
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


@app.get("/")
def root():
    return {"messaggio": "Expense Tracker funziona!"}