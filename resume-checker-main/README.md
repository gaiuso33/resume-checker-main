# 📄 Resume Checker

A Flask-based web app that analyzes PDF resumes and scores them based on matched technical skills. The app extracts text, compares it against a list of target skills, generates a score, displays a visual chart, and even allows exporting the analysis as a downloadable PDF report.

---

## 🚀 Features

- 🧠 Extracts resume content from PDF
- 🛠️ Checks for essential tech skills like Python, Flask, SQL, etc.
- 📊 Visual chart showing matched vs missing skills (Chart.js)
- 🧾 Exports analysis as a clean, professional PDF (ReportLab)
- 🎨 Clean Bootstrap UI

---

## 🛠️ Technologies

- Python, Flask
- PyPDF2 – PDF parsing
- ReportLab – PDF export
- Chart.js – frontend chart
- Bootstrap – UI styling

---

## ⚙️ How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/gaiuso33/resume-checker.git
cd resume-checker

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
````

Then go to: [http://localhost:5000](http://localhost:5000)

---

## 📸 Sample Output

* **Match Score:** 80%
* **Matched Skills:** `python`, `flask`, `sql`, `html`, `data analysis`
* **Chart:** Bar graph showing skill distribution
* **PDF Report:** Downloadable resume analysis

---

## 📁 Folder Structure

```
resume-checker/
│
├── app.py
├── templates/
│   ├── index.html
│   ├── result.html
│   └── upload.html
├── uploads/
├── utils/
│   └── resume_parser.py
├── static/
│   └── (optional CSS/chart)
└── README.md
```

---
```
## 📌 Future Improvements

* User login (admin vs guest)
* Save past uploads & results
* Live skill set customization
* Host app online (Streamlit, Render, etc.)

---

## 👨‍💻 Author

**Oluwole Qwerty**
[GitHub](https://github.com/gaiuso33) | [LinkedIn](https://www.linkedin.com/in/oluwole-qwerty)

---

## ⭐️ Show Your Support
If you find this useful, star ⭐ the repo and share with friends!

