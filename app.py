from flask import Flask, render_template, request, send_file
from io import BytesIO
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

SKILLS = [
    "python",
    "flask",
    "sql",
    "data analysis",
    "machine learning",
    "html",
    "css",
    "javascript",
    "git",
    "github"
]
def clean_text(text):
    if not text:
        return ""
    return text.encode("utf-8", "ignore").decode("utf-8")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_pdf_text(filepath):
    text = ""
    reader = PdfReader(filepath)

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text.strip()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "resume" not in request.files:
            return render_template("index.html", error="No file was uploaded.")

        resume_file = request.files["resume"]
        job_description = request.form.get("job_description", "").strip()

        if resume_file.filename == "":
            return render_template("index.html", error="Please select a PDF file.")

        if not allowed_file(resume_file.filename):
            return render_template("index.html", error="Only PDF files are allowed.")

        if not job_description:
            return render_template("index.html", error="Please paste a job description.")

        filename = secure_filename(resume_file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        resume_file.save(filepath)

        try:
            extracted_text = clean_text(extract_pdf_text(filepath))
            job_description = clean_text(job_description)
        except Exception:
            return render_template("index.html", error="Could not read the PDF file.")

        if not extracted_text:
            return render_template("index.html", error="No readable text was found in the PDF.")

        resume_text_lower = extracted_text.lower()
        jd_text_lower = job_description.lower()

        required_skills = [skill for skill in SKILLS if skill in jd_text_lower]

        if not required_skills:
            required_skills = SKILLS.copy()

        matched = [skill for skill in required_skills if skill in resume_text_lower]
        missing = [skill for skill in required_skills if skill not in resume_text_lower]
        extra_resume_skills = [
            skill for skill in SKILLS
            if skill in resume_text_lower and skill not in required_skills
        ]

        score = round((len(matched) / len(required_skills)) * 100) if required_skills else 0

        return render_template(
            "result.html",
            text=extracted_text,
            job_description=job_description,
            required_skills=required_skills,
            matched=matched,
            missing=missing,
            extra_resume_skills=extra_resume_skills,
            score=score,
            total=len(required_skills)
        )

    return render_template("index.html")


@app.route("/export/pdf", methods=["POST"])
def export_pdf():
    text = request.form["text"]
    score = request.form["score"]
    total = int(request.form["total"])
    job_description = request.form.get("job_description", "")
    matched = request.form.getlist("matched")
    missing = request.form.getlist("missing")
    required_skills = request.form.getlist("required_skills")
    extra_resume_skills = request.form.getlist("extra_resume_skills")

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50

    def write_line(line, font="Helvetica", size=10, step=14):
        nonlocal y
        if y < 50:
            pdf.showPage()
            y = height - 50
        pdf.setFont(font, size)
        pdf.drawString(50, y, line[:95])
        y -= step

    write_line("Resume Analysis Report", font="Helvetica-Bold", size=16, step=24)
    write_line(f"Match Score: {score}%", size=12, step=18)
    write_line(f"Required Skills: {', '.join(required_skills) if required_skills else 'None'}", size=10)
    write_line(f"Matched Skills: {', '.join(matched) if matched else 'None'}", size=10)
    write_line(f"Missing Skills: {', '.join(missing) if missing else 'None'}", size=10)
    write_line(
        f"Additional Resume Skills: {', '.join(extra_resume_skills) if extra_resume_skills else 'None'}",
        size=10
    )
    write_line(f"Total Skills Checked: {total}", size=10, step=20)

    write_line("Job Description:", font="Helvetica-Bold", size=12, step=18)
    for line in job_description.split("\n"):
        write_line(line, size=10)

    y -= 10
    write_line("Extracted Resume Text:", font="Helvetica-Bold", size=12, step=18)
    for line in text.split("\n"):
        write_line(line, size=10)

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="resume_analysis.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)