# Resume Checker

A simple **Flask web application** that analyzes a PDF resume and compares it against a job description to determine how well the resume matches the job requirements.

The app extracts text from a resume, identifies relevant technical skills, and calculates a **match score** based on how many required skills appear in the resume.

---

## Features

* Upload a **PDF resume**
* Paste a **job description**
* Automatic **skill detection**
* Calculates **resume-job match score**
* Displays:

  * Required skills
  * Matched skills
  * Missing skills
  * Additional skills found in resume
* **Visual chart** showing skill breakdown
* **Downloadable PDF report** of the analysis

---
## Live Demo

Try the app here:

[https://resume-checker-main-1.onrender.com]


## Demo Workflow
1. Upload your resume (PDF)
2. Paste the job description
3. Click **Analyze Resume**
4. View the analysis results:

   * Match Score
   * Skills breakdown
   * Resume text extraction
5. Download a **PDF report**

---

## Tech Stack

**Backend**

* Python
* Flask

**Libraries**

* PyPDF2 – PDF text extraction
* ReportLab – PDF report generation

**Frontend**

* HTML
* Bootstrap 5
* Chart.js

---

## Project Structure

```
resume-checker/
│
├── app.py
├── uploads/
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── static/
│   └── style.css
│
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/resume-checker.git
cd resume-checker
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

**Mac / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install flask PyPDF2 reportlab
```

---

## Running the App

Start the Flask server:

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

---

## Example Skills Detected

The application currently checks for the following skills:

* Python
* Flask
* SQL
* Data Analysis
* Machine Learning
* HTML
* CSS
* JavaScript
* Git
* GitHub

These can easily be expanded in `app.py`.

---

## Future Improvements

Possible upgrades:

* NLP-based skill extraction
* Automatic job description parsing
* Resume keyword recommendations
* User accounts and saved analyses
* Support for **DOCX resumes**
* Deploy the app online

---

## License

This project is open source and available under the **MIT License**.

---

## Author

Built by **Oluwole** as part of a portfolio project exploring Python, 
Flask, and resume analysis tools.
