# AI Generated Portfolio from Resume 🌐

This project takes a **resume PDF** as input and automatically generates a **dark-themed professional portfolio website** using AI.  
The generated website includes structured sections such as skills, projects, and experience, built using **HTML, CSS, and JavaScript**.

The goal of this project is to help users quickly create a personal portfolio website without manually writing frontend code.

---

## 📌 Purpose of the Project

- Convert a resume into a professional portfolio website
- Automate frontend generation using AI
- Provide live preview and downloadable website code
- Maintain clean backend-only GitHub repository (no generated frontend files)

---

## 🛠️ Setup Instructions

Follow these steps **exactly**.

---

## 1️⃣ Create Virtual Environment

From the root of the repository:

```bash
python -m venv web


# Windows
web\Scripts\activate

# macOS / Linux
source web/bin/activate

pip install -r web/project/req.txt

AI-GENERATED-PORTFOLIO-FROM-RESUME/
│
├── web/
│   ├── project/
│   │   ├── main.py
│   │   ├── req.txt
│   │
│   ├── .gitignore
│
├── README.md

GOOGLE_API_KEY=your_google_gemini_api_key

streamlit run web/project/main.py
```

🚀 Output

Upload a resume (PDF)

AI generates:

index.html

styles.css

script.js

Live preview inside Streamlit

Downloadable ZIP of portfolio website

Generated frontend files are intentionally ignored in Git.


---


