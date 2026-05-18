import os
from flask import Blueprint, render_template, request, current_app
from werkzeug.utils import secure_filename

from app.services.pdf_extractor import extract_text_from_pdf
from app.services.skill_matcher import compare_skills
from app.services.scoring import calculate_skill_score, calculate_structure_score, calculate_overall_score
from app.services.recommendations import generate_recommendations
from app.services.resume_optimizer import rewrite_bullets

main_bp = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    resume_file = request.files.get("resume")
    job_description = request.form.get("job_description")

    if not resume_file or resume_file.filename == "":
        return render_template("index.html", error="Please upload a resume PDF.")

    if not job_description or job_description.strip() == "":
        return render_template("index.html", error="Please paste a job description.")

    if not allowed_file(resume_file.filename):
        return render_template("index.html", error="Only PDF resumes are allowed.")

    filename = secure_filename(resume_file.filename)
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    resume_file.save(upload_path)

    resume_text = extract_text_from_pdf(upload_path)

    resume_skills, job_skills, matched, missing, extra = compare_skills(resume_text, job_description)

    skill_score = calculate_skill_score(job_skills, matched)
    structure_score = calculate_structure_score(resume_text)
    overall_score = calculate_overall_score(skill_score, structure_score)

    recommendations = generate_recommendations(missing)
    bullet_suggestions = rewrite_bullets(resume_text)

    return render_template(
        "result.html",
        overall_score=overall_score,
        skill_score=skill_score,
        structure_score=structure_score,
        matched=matched,
        missing=missing,
        extra=extra,
        recommendations=recommendations,
        bullet_suggestions=bullet_suggestions
    )