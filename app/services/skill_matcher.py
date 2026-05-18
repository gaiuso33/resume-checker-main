import re

SKILLS_DB = [
    "python", "java", "javascript", "react", "node", "express",
    "html", "css", "tailwind", "mongodb", "sql", "flask", "django",
    "git", "github", "docker", "linux", "postman",
    "machine learning", "deep learning", "numpy", "pandas", "matplotlib",
    "rest api", "api", "cybersecurity", "networking"
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\+\#\.\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_skills(text):
    cleaned = clean_text(text)
    found = set()

    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, cleaned):
            found.add(skill)

    return sorted(found)

def compare_skills(resume_text, job_text):
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_text))

    matched = sorted(resume_skills.intersection(job_skills))
    missing = sorted(job_skills - resume_skills)
    extra = sorted(resume_skills - job_skills)

    return resume_skills, job_skills, matched, missing, extra