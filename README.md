# 🚀 AI Smart Resume Matcher

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Scikit-Learn](https://img.shields.io/badge/Library-Scikit--Learn-orange)

An intelligent recruiting tool that parses resumes, extracts skills, and ranks candidates based on job descriptions using **NLP (TF-IDF & Cosine Similarity)**. 

Designed to mimic how Applicant Tracking Systems (ATS) filter candidates, providing a visual match score and missing skills report.

## 📸 Interface
![UI interface](image.png)

## ✨ Key Features
- **🧠 AI-Powered Ranking:** Uses TF-IDF vectorization to understand the semantic importance of words.
- **📊 Interactive Dashboard:** Built with **Streamlit** for real-time analysis and easy drag-and-drop.
- **🔍 Skill Extraction:** Automatically detects technical skills (Python, SQL, React, etc.) and compares them against the JD.
- **⚡ Instant Feedback:** Provides a percentage match score and highlights missing keywords.
- **📄 PDF Support:** Robust text extraction from modern PDF resumes.

## 📂 Project Structure
```text
resume-matcher/
├── data/
│   └── job_description.txt  # Default JD for testing
├── src/
│   ├── matcher.py           # Core logic (Cosine Similarity)
│   ├── pdf_reader.py        # PDF text extraction
│   ├── skills.py            # Skill database & extractor
│   └── text_cleaner.py      # NLP preprocessing
├── app_ui.py                # Streamlit Frontend
├── main.py                  # CLI version (optional)
└── requirements.txt         # Dependencies

🛠️ Installation
Clone the repository

Bash

git clone [https://github.com/Umerheree/smart-resume-matcher.git](https://github.com/Umerheree/smart-resume-matcher.git)
cd smart-resume-matcher
Install dependencies

Bash

pip install -r requirements.txt
Run the Application

Bash

streamlit run app_ui.py
🧩 How It Works
Preprocessing: Cleans text by removing special characters and stop words.

Feature Extraction: Converts text into numerical vectors using TF-IDF.

Similarity Calculation: Measures the cosine angle between the JD vector and Resume vector.

Skill Matching: Cross-references text against a curated database of 500+ tech skills.

👨‍💻 Author
Umer Mehboob Aspiring Software Engineer & CS Student 
