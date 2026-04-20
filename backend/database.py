from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = "sqlite:///./test.db" #segue il formato tipo_db://utente:password@host:porta/nome_db

#il motoro è il collegamento con il database, è un oggetto che gestisce le connessioni al database
engine = create_engine(db_url, connect_args={"check_same_thread": False}) #per SQLite, per altri DB non serve

#la sessione è cioè che usiamo per fare le query al database, è un oggetto che gestisce le transazioni e le operazioni sul database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() #è la classe base per i modelli del database, è una classe che contiene tutte le informazioni sui modelli e le tabelle del database

def get_db():
    db = SessionLocal() #crea una nuova sessione
    try:
        yield db #restituisce la sessione, è un generatore che permette di usare la sessione in modo efficiente
    finally:
        db.close() #chiude la sessione dopo l'uso