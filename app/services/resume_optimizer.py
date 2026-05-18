WEAK_VERBS = {
    "helped": "assisted",
    "worked": "developed",
    "did": "implemented",
    "made": "built",
    "used": "utilized",
    "responsible": "managed"
}

def rewrite_bullets(resume_text):
    suggestions = []
    lines = resume_text.split("\n")

    for line in lines:
        lower_line = line.lower()
        for weak, strong in WEAK_VERBS.items():
            if weak in lower_line:
                suggestions.append(f"Replace '{weak}' with '{strong}' in: {line.strip()}")

    return suggestions[:10]