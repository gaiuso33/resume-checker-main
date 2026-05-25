# Resume Checker

Resume Checker Pro is a Flask-based ATS resume analyzer that allows users to upload a resume (PDF) and compare it against a job description. It generates a match score, identifies missing skills, and provides recommendations to improve the resume.

## Live demo
[[Github pages][(https://resume-checker-main-2.onrender.com/)]
## Features
- Upload PDF resume and extract text
- Paste job description for comparison
- Skill match scoring (Matched, Missing, Extra skills)
- Resume structure scoring
- Bullet improvement suggestions
- Charts (Pie chart + Score breakdown)
- Export professional PDF report

## Tech Stack
- Python (Flask)
- TailwindCSS (UI)
- Chart.js (Charts)
- PyPDF2 (PDF extraction)
- ReportLab (PDF export)

## Setup Instructions
Clone the repo and install dependencies:

```bash
pip install -r requirements.txt
python run.py
