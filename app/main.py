from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Imports aus den direkt unter app/ liegenden Modulen
from app.database import Base, engine
from app import router # Importiert das gesamte models-Modul für Base.metadata.create_all

# Datenbanktabellen erstellen (falls noch nicht vorhanden)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kraftwerte Manager",
    description="Eine modulare Webanwendung zum Verwalten von Kraftwerten mit FastAPI und SQLAlchemy.",
    version="2.1.0" # Version anpassen
)

# Statische Dateien mounten
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root-Endpunkt für das Frontend
@app.get("/", response_class=FileResponse)
async def read_root_frontend():
    return FileResponse(os.path.join("static", "index.html"))

# Router einbinden
app.include_router(router.router)