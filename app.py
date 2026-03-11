from flask import Flask, render_template, request, send_file
from io import BytesIO
import os
import re
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
    "django",
    "fastapi",

    "sql",
    "postgresql",
    "mysql",

    "machine learning",
    "deep learning",
    "nlp",
    "tensorflow",
    "pytorch",

    "data analysis",
    "pandas",
    "numpy",

    "html",
    "css",
    "javascript",
    "react",

    "git",
    "github",
    "docker",
    "api",
]


def clean_text(text):
    if not text:
        return ""
    text = text.encode("utf-8", "ignore").decode("utf-8")
    text = text.replace("\x00", "")
    return text.strip()

def normalize_text(text):
    text = clean_text(text).lower()
    text = re.sub(r"[-_/]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def skill_in_text(skill, text):
    normalized_skill = normalize_text(skill)
    normalized_text = normalize_text(text)

    if " " in normalized_skill:
        return normalized_skill in normalized_text

    pattern = rf"\b{re.escape(normalized_skill)}\b"
    return re.search(pattern, normalized_text) is not None

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


def extract_resume_sections(text):
    text_lower = text.lower()

    return {
        "summary": any(word in text_lower for word in ["summary", "profile", "objective"]),
        "projects": "project" in text_lower or "projects" in text_lower,
        "experience": "experience" in text_lower or "work experience" in text_lower,
        "education": "education" in text_lower,
        "skills": "skills" in text_lower,
    }


def get_stronger_action_verbs():
    return {
        "built": "developed",
        "made": "designed and implemented",
        "helped": "collaborated on",
        "worked on": "contributed to",
        "did": "executed",
        "created": "engineered",
        "used": "leveraged",
        "fixed": "resolved",
        "led": "spearheaded",
        "managed": "coordinated"
    }


def generate_recommendations(score, missing):
    recommendations = []

    if missing:
        recommendations.append(
            "Highlight the most relevant skills from the job description in your resume summary."
        )
        recommendations.append(
            "Add or emphasize missing skills only if you truly have experience with them."
        )
        recommendations.append(
            "Include projects that clearly demonstrate the required technologies."
        )
        recommendations.append(
            "Use stronger keywords from the job description to improve alignment."
        )
    else:
        recommendations.append("Your resume matches this role well.")
        recommendations.append("Focus on measurable achievements and clear project outcomes.")
        recommendations.append("Keep the layout clean and make your strongest work easy to find.")

    if score < 50:
        recommendations.append(
            "Consider tailoring your resume specifically for this role before applying."
        )
    elif score >= 75:
        recommendations.append(
            "You are in a strong position—now improve clarity, impact, and presentation."
        )

    return list(dict.fromkeys(recommendations))


def generate_optimizer_feedback(extracted_text, job_description, matched, missing, required_skills):
    feedback = []
    action_verbs = get_stronger_action_verbs()
    sections = extract_resume_sections(extracted_text)

    if missing:
        feedback.append(
            "Tailor your resume to this role by emphasizing the missing skills only where you have real experience."
        )
        feedback.append(
            "Add more role-specific keywords from the job description to improve alignment and visibility."
        )
        feedback.append(
            "Include projects, coursework, or achievements that demonstrate the required technologies."
        )

    if required_skills and len(matched) >= 1:
        feedback.append(
            "Your resume already aligns with some core requirements. Strengthen it further by making those experiences more visible."
        )

    if not sections["summary"]:
        feedback.append(
            "Consider adding a short professional summary at the top of your resume tailored to the role."
        )

    if not sections["projects"]:
        feedback.append(
            "Add a projects section to showcase practical work related to the job requirements."
        )

    if not sections["skills"]:
        feedback.append(
            "Include a dedicated skills section so recruiters can quickly identify your technical strengths."
        )

    if not sections["experience"]:
        feedback.append(
            "If you have relevant internship, volunteer, freelance, or leadership experience, include it clearly under an experience section."
        )

    keywords_to_add = list(dict.fromkeys(missing))

    verb_suggestions = [
        f"{weak.title()} → {strong}"
        for weak, strong in action_verbs.items()
        if weak in extracted_text.lower()
    ]

    if not verb_suggestions:
        verb_suggestions = [
            "Built → Developed",
            "Helped → Collaborated on",
            "Made → Designed and implemented"
        ]

    feedback = list(dict.fromkeys(feedback))
    verb_suggestions = list(dict.fromkeys(verb_suggestions))

    return {
        "feedback": feedback,
        "keywords_to_add": keywords_to_add,
        "verb_suggestions": verb_suggestions,
        "sections": sections
    }


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
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

        if not extracted_text:
            return render_template("index.html", error="No readable text was found in the PDF.")

        required_skills = [skill for skill in SKILLS if skill_in_text(skill, job_description)]

        if not required_skills:
            required_skills = SKILLS.copy()

        matched = [skill for skill in required_skills if skill_in_text(skill, extracted_text)]
        missing = [skill for skill in required_skills if not skill_in_text(skill, extracted_text)]
        extra_resume_skills = [
            skill for skill in SKILLS
            if skill_in_text(skill, extracted_text) and skill not in required_skills
        ]

        score = round((len(matched) / len(required_skills)) * 100) if required_skills else 0
        recommendations = generate_recommendations(score, missing)
        optimizer = generate_optimizer_feedback(
            extracted_text,
            job_description,
            matched,
            missing,
            required_skills
        )

        return render_template(
            "result.html",
            text=extracted_text,
            job_description=job_description,
            required_skills=required_skills,
            matched=matched,
            missing=missing,
            extra_resume_skills=extra_resume_skills,
            score=score,
            total=len(required_skills),
            recommendations=recommendations,
            optimizer=optimizer
        )

    return render_template("index.html")


@app.route("/export/pdf", methods=["POST"])
def export_pdf():
    optimizer_feedback = request.form.getlist("optimizer_feedback")
    optimizer_keywords = request.form.getlist("optimizer_keywords")
    optimizer_verbs = request.form.getlist("optimizer_verbs")
    recommendations = request.form.getlist("recommendations")

    text = clean_text(request.form["text"])
    score = request.form["score"]
    total = int(request.form["total"])
    job_description = clean_text(request.form.get("job_description", ""))
    matched = request.form.getlist("matched")
    missing = request.form.getlist("missing")
    required_skills = request.form.getlist("required_skills")
    extra_resume_skills = request.form.getlist("extra_resume_skills")

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    _, height = letter
    y = height - 50

    def write_line(line, font="Helvetica", size=10, step=14):
        nonlocal y
        if y < 50:
            pdf.showPage()
            y = height - 50
        pdf.setFont(font, size)
        pdf.drawString(50, y, clean_text(line)[:95])
        y -= step

    write_line("Resume Analysis Report", font="Helvetica-Bold", size=16, step=24)
    write_line(f"Match Score: {score}%", size=12, step=18)
    write_line(f"Required Skills: {', '.join(required_skills) if required_skills else 'None'}")
    write_line(f"Matched Skills: {', '.join(matched) if matched else 'None'}")
    write_line(f"Missing Skills: {', '.join(missing) if missing else 'None'}")
    write_line(
        f"Additional Resume Skills: {', '.join(extra_resume_skills) if extra_resume_skills else 'None'}"
    )
    write_line(f"Total Skills Checked: {total}", step=20)

    if recommendations:
        write_line("Recommendations:", font="Helvetica-Bold", size=12, step=18)
        for item in recommendations:
            write_line(f"- {item}")
        y -= 10

    if optimizer_feedback or optimizer_keywords or optimizer_verbs:
        write_line("AI Resume Optimization Suggestions:", font="Helvetica-Bold", size=12, step=18)

        if optimizer_feedback:
            write_line("Improvement Suggestions:", font="Helvetica-Bold", size=10, step=16)
            for item in optimizer_feedback:
                write_line(f"- {item}")

        if optimizer_keywords:
            write_line("Suggested Keywords to Add:", font="Helvetica-Bold", size=10, step=16)
            write_line(", ".join(optimizer_keywords))

        if optimizer_verbs:
            write_line("Stronger Action Verbs:", font="Helvetica-Bold", size=10, step=16)
            for item in optimizer_verbs:
                write_line(f"- {item}")

        y -= 10

    write_line("Job Description:", font="Helvetica-Bold", size=12, step=18)
    for line in job_description.split("\n"):
        write_line(line)

    y -= 10
    write_line("Extracted Resume Text:", font="Helvetica-Bold", size=12, step=18)
    for line in text.split("\n"):
        write_line(line)

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