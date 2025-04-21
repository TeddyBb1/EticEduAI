from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uuid, os

from ai_detector import check_ai_probability
from plagiarism_advanced import check_plagiarism_advanced
from pdf_generator import generate_pdf_report

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/verifica_licenta/")
async def verifica_licenta(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    paragrafe = [p for p in text.split("\n") if len(p.strip()) > 30]

    rezultate = []
    toate_sursele = []

    for paragraf in paragrafe:
        scor_ai = check_ai_probability(paragraf)
        surse = check_plagiarism_advanced(paragraf)
        scor_plagiat = max([s['scor'] for s in surse], default=0)

        rezultate.append({
            "paragraf": paragraf,
            "scor_ai": scor_ai,
            "scor_plagiat": scor_plagiat,
            "surse_similare": [s['link'] for s in surse]
        })

        toate_sursele.extend(surse)

    raport_id = str(uuid.uuid4())
    raport_path = f"rapoarte/raport_{raport_id}.pdf"
    os.makedirs("rapoarte", exist_ok=True)
    generate_pdf_report(raport_path, "Student Necunoscut", rezultate, toate_sursele)

    return {
        "rezultate": rezultate,
        "raport_pdf": f"http://localhost:8000/static/{Path(raport_path).name}"
    }

app.mount("/static", StaticFiles(directory="rapoarte"), name="static")