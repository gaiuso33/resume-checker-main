import os
from flask import Blueprint, request, send_file, current_app
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

export_bp = Blueprint("export", __name__, url_prefix="/export")

@export_bp.route("/pdf", methods=["POST"])
def export_pdf():
    data = request.json

    filename = f"resume_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join(current_app.config["REPORT_FOLDER"], filename)

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Resume Checker Report")

    y -= 40
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Overall Score: {data.get('overall_score')}%")

    y -= 20
    c.drawString(50, y, f"Skill Score: {data.get('skill_score')}%")
    y -= 20
    c.drawString(50, y, f"Structure Score: {data.get('structure_score')}%")

    y -= 40
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Matched Skills:")
    y -= 20
    c.setFont("Helvetica", 11)

    for skill in data.get("matched", []):
        c.drawString(70, y, f"- {skill}")
        y -= 15
        if y < 80:
            c.showPage()
            y = height - 50

    y -= 20
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Missing Skills:")
    y -= 20
    c.setFont("Helvetica", 11)

    for skill in data.get("missing", []):
        c.drawString(70, y, f"- {skill}")
        y -= 15
        if y < 80:
            c.showPage()
            y = height - 50

    y -= 20
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Recommendations:")
    y -= 20
    c.setFont("Helvetica", 11)

    for rec in data.get("recommendations", []):
        c.drawString(70, y, f"- {rec}")
        y -= 15
        if y < 80:
            c.showPage()
            y = height - 50

    c.save()

    return send_file(file_path, as_attachment=True)