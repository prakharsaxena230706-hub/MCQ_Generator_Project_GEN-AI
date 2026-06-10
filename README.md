# 🧠 MCQ Generator — AI-Powered Quiz Engine
### Built with LangChain 🦜🔗 | OpenAI GPT | Streamlit | Deployed on AWS EC2

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/LangChain-Enabled-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/OpenAI-GPT--3.5%2F4-412991?style=for-the-badge&logo=openai" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/AWS-EC2%20Deployed-FF9900?style=for-the-badge&logo=amazonaws" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

---

## 📌 What Is This Project?

**MCQ Generator** is a production-grade, AI-powered web application that automatically generates **Multiple Choice Questions (MCQs)** from any uploaded document — PDF or plain text — using the power of **Large Language Models (LLMs)** via OpenAI's GPT API, orchestrated through **LangChain's Sequential Chain** architecture.

Upload your study material. Set the number of questions, subject, and difficulty. Click a button. Get exam-ready MCQs — instantly.

No manual question writing. No template copying. Just pure AI-generated, context-aware questions tailored to your content.

---

## 🎯 The Problem It Solves

Creating MCQs manually is one of the most **time-consuming, repetitive, and cognitively draining** tasks for educators, trainers, and content creators. Consider:

- A university professor needs 50 MCQs for a mid-semester exam from a 40-page chapter
- A corporate trainer needs assessments from a 30-page policy document
- A student needs 100 practice questions from their entire semester notes
- An EdTech platform needs to auto-generate quizzes from video transcripts

**MCQ Generator eliminates this bottleneck entirely** — what used to take hours now takes seconds.

---

## 🚀 Live Demo

> 🌐 Deployed on **AWS EC2 (Ubuntu 22.04)** via Streamlit

```
https://mcqgeneratorgenai.streamlit.app/
```

---

## 🗂️ Project Structure

```
MCQ_Generator_Project_GEN-AI/
│
├── StreamlitAPP.py                  # Main Streamlit frontend application
├── Response.json                    # MCQ response template/schema for LLM prompting
├── requirements.txt                 # All Python dependencies
├── setup.py                         # Package setup for modular imports
├── .env                             # Environment variables (OpenAI API Key)
│
├── src/
│   └── MCQ_Generator/
│       ├── __init__.py
│       ├── MCQ_Generate.py          # Core LangChain chain logic (LLMChain + SequentialChain)
│       ├── utils.py                 # File reading (PDF/TXT) + table data formatter
│       └── logger.py                # Custom logging configuration
│
├── experiments/
│   └── mcq.ipynb                    # Jupyter notebook for prototyping & testing
│
└── data/                            # Sample input files for testing
```

---

## 🧱 Tech Stack — Deep Dive

### 🐍 Python
The backbone of the entire application. Python's rich NLP and AI ecosystem makes it the ideal language for building LLM-powered pipelines.

### 🦜 LangChain
The **orchestration framework** that manages the LLM pipeline. Key components used:

| Component | Role |
|-----------|------|
| `LLMChain` | Wraps a prompt template + LLM into a single callable chain |
| `SequentialChain` | Chains multiple LLMChains so output of one feeds into the next |
| `PromptTemplate` | Structures dynamic prompts with variable injection |
| `ChatOpenAI` | LangChain's interface to OpenAI's chat models |

**The Two-Chain Architecture:**
```
Chain 1: quiz_chain
  Input  → text, number, subject, tone, response_json
  Output → quiz (raw MCQ JSON string)

Chain 2: review_chain
  Input  → quiz (from Chain 1)
  Output → review (quality evaluation of generated MCQs)

SequentialChain → runs both in order, passing state automatically
```

### 🤖 OpenAI GPT (via API)
The **intelligence engine** powering question generation. GPT understands the context of uploaded content and generates semantically valid, contextually relevant MCQs with correct answers and plausible distractors.

Token tracking is built-in via `get_openai_callback`:
- Total tokens consumed
- Prompt tokens
- Completion tokens
- Estimated API cost per run

### 🎨 Streamlit
Provides the **interactive web UI** without writing a single line of HTML/CSS/JS. Key UI components:
- `st.file_uploader` — drag-and-drop PDF/TXT upload
- `st.number_input` — select MCQ count (3–50)
- `st.text_input` — subject and difficulty inputs
- `st.spinner` — loading state during LLM inference
- `st.table` — renders final MCQs in a clean tabular format
- `st.text_area` — shows GPT's quality review of the quiz

### 📄 PyPDF2
Handles **PDF text extraction** page by page. Accepts Streamlit's `UploadedFile` object directly as a file-like stream without needing disk I/O.

### ☁️ AWS EC2
The application is **deployed on an Ubuntu EC2 instance**, making it accessible as a live web server. The deployment stack:
- Ubuntu 22.04 LTS on EC2
- Python virtual environment (`venv`)
- Streamlit server on port `8501`
- Security Group configured to allow inbound traffic on port `8501`

---

## ⚙️ How It Works — End to End

```
┌─────────────────────────────────────────────────────────────┐
│                     USER UPLOADS FILE                        │
│              (PDF or TXT via Streamlit UI)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    read_file() [utils.py]                    │
│     Detects file type via .name → extracts raw text         │
│     PDF: PyPDF2.PdfReader | TXT: .read().decode('utf-8')    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              generate_evaluate_chain() [MCQ_Generate.py]     │
│                                                              │
│   Inputs: text, number, subject, tone, response_json        │
│                                                              │
│   Chain 1 (quiz_chain):                                      │
│   → PromptTemplate + ChatOpenAI → generates MCQ JSON        │
│                                                              │
│   Chain 2 (review_chain):                                    │
│   → Takes quiz output → GPT evaluates quality/complexity    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                 get_table_data() [utils.py]                  │
│    Parses quiz JSON string → list of dicts                   │
│    Handles markdown fences (```json) + json.loads()         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│               Streamlit renders results                      │
│   pd.DataFrame → st.table (MCQs)                            │
│   st.text_area (GPT review/feedback)                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🌍 Real-World Applications

### 🎓 Education
- **Schools & Universities** — Auto-generate chapter-end tests from textbooks, PDF notes, or lecture slides
- **Competitive Exam Prep** — Create unlimited practice MCQs for UPSC, JEE, NEET, CAT, GRE, GMAT from study material
- **E-Learning Platforms** — Automatically attach assessments to every piece of course content at scale
- **Self-Study Tools** — Students upload their own notes and generate personalized practice tests

### 🏢 Corporate & HR
- **Employee Onboarding** — Generate compliance and policy quizzes from HR documents automatically
- **Skill Assessments** — Upload training manuals and instantly create post-training evaluations
- **L&D Teams** — Scale learning assessment creation without manual effort from instructional designers

### 🏥 Healthcare & Law
- **Medical Training** — Generate MCQs from clinical guidelines, pharmacology notes, or case studies for medical students and residents
- **Legal Certification** — Create bar exam practice questions from case law documents and legal texts

### 🧪 Research & Publishing
- **Academic Publishers** — Attach auto-generated test banks to every textbook chapter
- **Content Quality Assurance** — Use GPT's review chain to evaluate whether generated questions meet complexity standards

### 🌐 EdTech Product Teams
- **Zero-effort quiz generation** at scale for platforms like Coursera, Unacademy, BYJU's, Khan Academy
- Reduces content production cost and time-to-market for new courses dramatically

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.10+
- OpenAI API Key ([get one here](https://platform.openai.com/api-keys))
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/prakharsaxena230706-hub/MCQ_Generator_Project_GEN-AI.git
cd MCQ_Generator_Project_GEN-AI
```

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv env
.\env\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 5. Run the Application
```bash
streamlit run StreamlitAPP.py
```

Open your browser at: `http://localhost:8501`

---

## ☁️ AWS EC2 Deployment Guide

### 1. Launch EC2 Instance
- AMI: **Ubuntu 22.04 LTS**
- Instance type: `t2.micro` (free tier) or `t2.small`
- Security Group: Allow inbound **TCP port 8501** from `0.0.0.0/0`

### 2. SSH Into Instance
```bash
ssh -i your-key.pem ubuntu@<your-ec2-public-ip>
```

### 3. Install Python & Dependencies
```bash
sudo apt update && sudo apt install python3-pip python3-venv git -y
git clone https://github.com/prakharsaxena230706-hub/MCQ_Generator_Project_GEN-AI.git
cd MCQ_Generator_Project_GEN-AI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Set Environment Variables
```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### 5. Run Streamlit on EC2
```bash
streamlit run StreamlitAPP.py --server.port 8501 --server.address 0.0.0.0
```

Access at: `http://<your-ec2-public-ip>:8501`

### 6. Keep App Running After SSH Exit
```bash
nohup streamlit run StreamlitAPP.py --server.port 8501 --server.address 0.0.0.0 &
```

---

## 📦 Key Dependencies

```txt
streamlit
langchain
langchain-openai
langchain-community
openai
python-dotenv
PyPDF2
pandas
```

---

## 🔐 Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key for GPT access |

> ⚠️ Never commit your `.env` file. It is listed in `.gitignore`.

---

## 📊 Token & Cost Tracking

Every API call is tracked automatically:

```
Total Tokens   : 2,847
Prompt Tokens  : 2,104
Completion Tokens: 743
Estimated Cost : $0.0043
```

This helps monitor OpenAI API usage and optimize prompts for cost efficiency.

---

## 🧩 Key Design Decisions

### Why LangChain SequentialChain?
Rather than making two separate API calls manually, SequentialChain passes the output of the quiz generation step directly into the review step — cleaner, faster, and stateful within a single invocation.

### Why JSON Schema Prompting?
`Response.json` acts as a **few-shot template** shown to the LLM, enforcing structured output format so parsing is deterministic and reliable.

### Why Streamlit?
Streamlit converts a Python script into a full-stack web app with zero frontend code — ideal for AI/ML projects where rapid prototyping and deployment speed matter most.

---

## 🐛 Common Issues & Fixes

| Error | Fix |
|-------|-----|
| `ImportError: cannot import ChatOpenAI from langchain.chat_models` | Use `from langchain_openai import ChatOpenAI` |
| `AttributeError: 'UploadedFile' has no attribute 'lower'` | Use `uploaded_file.name.lower()` instead of `file_path.lower()` |
| `AttributeError: _traceback_` | Use `e.__traceback__` (double underscores) |
| `AttributeError: 'TextAccessor' has no attribute 'items'` | Parse quiz string with `json.loads()` before iterating |
| `FileNotFoundError: Response.json` | Use relative path `open('Response.json', 'r')` instead of hardcoded Windows path |

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 👨‍💻 Author

**Prakhar Saxena**

[![GitHub](https://img.shields.io/badge/GitHub-prakharsaxena230706--hub-181717?style=flat&logo=github)](https://github.com/prakharsaxena230706-hub)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## ⭐ Show Your Support

If this project helped you, please consider giving it a **⭐ star** on GitHub — it means a lot and helps others discover it!

---

<p align="center">Built with ❤️ using Python, LangChain, OpenAI & Streamlit</p>
