# Caprae Leadgen Scoring Tool

This project was developed as part of Caprae Capital's AI Readiness Pre-Screening Challenge. It is a lead generation and scoring tool designed to evaluate potential SaaS startup leads using a rule-based and optionally ML-augmented scoring pipeline.

---

## 🔧 Features

- 🧠 **ARS Scoring Engine** (AI Readiness Score)
- 📥 Accepts input via `.json` and `.csv` files
- 🎯 Visual & tabular lead prioritization
- 📊 Custom styling and logos for polished dashboard
- 🛠️ Utilities for image handling and scoring logic
- 📂 Modular and scalable backend architecture

---

## 🗂️ Folder Structure

CAPRAE_LEADGEN_PROJECT/
├── .vscode/ # Editor config (optional)
├── backend/
│ └── utils/
│ ├── init.py
│ ├── ars_utils.py # AI scoring logic
│ └── image_utils.py # For logo/image handling
├── data/
│ ├── enriched_company_data.json
│ ├── sample_leads.json
│ └── standardized_company_data.csv
├── env311/ # ⚠️ Virtual environment (should be ignored)
├── static/
│ ├── logo.png
│ ├── logo_horizontal.png
│ └── styles/
│ └── style.css
├── .gitignore
├── .python-version
├── app.py # Streamlit frontend
├── pyproject.toml # Project metadata
├── README.md
└── requirements.txt # Dependencies

## 🚀 Getting Started

1. **Clone the Repository**  
```bash
git clone https://github.com/23f2003521/caprae-leadgen-dashboard.git
cd CAPRAE_LEADGEN_PROJEC


Set Up a Virtual Environment

python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Run the App
streamlit run app.py

📂 Input Data Format
You can use:

sample_leads.json or standardized_company_data.csv

Required fields: Company Name, Industry, Revenue, Growth Rate, Founder Involved, AI Readiness, etc.

🧠 AI Readiness Logic
Points-based scoring based on:

Revenue brackets

Growth signals

Founder involvement

AI and digital maturity

Extendable with ML proxy label generation

📌 Future Improvements
LLM-based company summary generation

API integrations (Clearbit, LinkedIn)

Model-based scoring

User login & project history saving
