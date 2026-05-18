def calculate_skill_score(job_skills, matched_skills):
    if not job_skills:
        return 50

    return int((len(matched_skills) / len(job_skills)) * 100)

def calculate_structure_score(resume_text):
    required_sections = ["experience", "education", "skills", "projects"]
    score = 0

    for section in required_sections:
        if section.lower() in resume_text.lower():
            score += 25

    return score

def calculate_overall_score(skill_score, structure_score):
    return int((skill_score * 0.7) + (structure_score * 0.3))