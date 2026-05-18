def generate_recommendations(missing_skills):
    if not missing_skills:
        return ["Excellent match! Your resume already includes the major keywords from the job description."]

    missing_list = ", ".join(missing_skills)

    return [
        "Your resume is missing important keywords found in the job description.",
        f"Missing keywords: {missing_list}",
        "If you have experience with these tools, include them in your Skills, Projects, or Experience section.",
        "Add 1–2 bullet points showing where you used these skills in real projects.",
    ]
