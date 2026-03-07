from flask import Flask, render_template, request, send_file
from io import BytesIO
import os
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume_file = request.files['resume']
        if resume_file and resume_file.filename.endswith('.pdf'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(filepath)

            # Extract PDF text
            reader = PdfReader(filepath)
            text = ''
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"

            text = text.lower()

            # Target skills
            skills = [
                "python", "flask", "sql", "data analysis", "machine learning",
                "html", "css", "javascript", "git", "github"
            ]

            matched = [skill for skill in skills if skill in text]
            score = round(len(matched) / len(skills) * 100)

            return render_template('result.html', text=text, matched=matched, score=score, total=len(skills))

    return render_template('index.html')

@app.route('/export/pdf', methods=['POST'])
def export_pdf():
    text = request.form['text']
    score = request.form['score']
    matched = request.form.getlist('matched')
    total = int(request.form['total'])

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Resume Analysis Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Match Score: {score}%")
    c.drawString(50, height - 120, f"Matched Skills: {', '.join(matched)}")
    c.drawString(50, height - 140, f"Total Skills: {total}")
    c.drawString(50, height - 160, "Extracted Resume Text:")

    text_lines = text.split('\n')
    y = height - 180
    for line in text_lines:
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)
        c.drawString(50, y, line[:90])  # truncate long lines
        y -= 14

    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="resume_analysis.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)

