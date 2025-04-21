from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf_report(filename, student_name, ai_results, plagiarism_results):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Raport EticEduAI")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Nume student: {student_name}")
    c.drawString(50, height - 100, f"Data generării: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y = height - 140
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Analiză AI:")
    y -= 20

    c.setFont("Helvetica", 11)
    for idx, entry in enumerate(ai_results):
        c.drawString(60, y, f"{idx + 1}. Scor AI: {entry['scor_ai']}%")
        y -= 18
        if y < 100:
            c.showPage()
            y = height - 50

    y -= 10
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Analiză Plagiat:")
    y -= 20

    c.setFont("Helvetica", 11)
    for entry in plagiarism_results:
        c.drawString(60, y, f"- Sursa: {entry['sursa']}, Scor: {entry['scor']}%")
        y -= 18
        c.drawString(70, y, f"  Link: {entry['link']}")
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
    return filename