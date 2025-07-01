<p align="center">
  <img src="https://img.shields.io/github/license/anshj2002/resume_extractor?color=brightgreen" alt="License">
  <img src="https://img.shields.io/github/languages/top/anshj2002/resume_extractor" alt="Main Language">
  <img src="https://img.shields.io/badge/LLM-HuggingFace%20API-blue" alt="LLM Backend">
  <img src="https://img.shields.io/badge/UI-Bootstrap%205-green" alt="Bootstrap">
</p>

<h1 align="center">📄 Resume Q&A Extractor (LLM-powered)</h1>


<p align="center">
  <b>Upload any resume, ask questions using AI!</b><br>
  Powered by <a href="https://huggingface.co/inference-api">Hugging Face Inference API</a> and LLMs. No local GPU required.
</p>

---

## ✨ Features

- **🔍 Upload PDF or DOCX resume**
- **💬 Ask questions** in natural language about the resume (skills, experience, education, etc.)
- **🤖 Powered by LLM** (Zephyr-7b-beta / Hugging Face, runs on free API tier)
- **⚡ Shows Q&A History** for each resume
- **📋 Auto-deletes resumes for privacy**
- **🎉 Modern UI** (Bootstrap 5, mobile-first, loader animation)
- **🛡️ 100% free & open source**

---

## 🚀 Quick Demo

<video src="01.07.2025_16.44.34_REC.mp4" controls width="600"></video>
> _Upload resume → Ask "What is the candidate's latest experience?" → Instantly get the answer!_

---


## 🛠️ Installation & Local Setup

**1. Clone this repository**

```bash
git clone https://github.com/anshj2002/resume_extractor.git
cd resume_extractor
```

**2. Create a virtual environment & activate**

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

**3. Install requirements**

```bash
pip install -r requirements.txt
```

**4. Create a `.env` file**

```env
HF_TOKEN=hf_YourHuggingFaceTokenHere
```

> Get a **free HF token** here: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

**5. Run the app**

```bash
python app.py
```

**6. Open your browser at** [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧑‍💻 Project Structure

```
resume_extractor/
│
├── app.py               # Flask backend, API calls
├── requirements.txt
├── .env                 # (keep your HF_TOKEN here)
├── /templates/
│    └── index.html      # Main UI
├── /static/
│    ├── script.js       # Frontend logic
│    └── styles.css      # Custom styles
└── /uploads/            # (temp, auto-deleted files)
```

---

## 🧠 How it Works

1. **User uploads a resume (.pdf or .docx)**
2. **Flask extracts the text** (auto-deletes file after)
3. **User asks questions**; frontend disables input and shows animation while waiting
4. **Backend sends question + resume text** to Hugging Face LLM API (Zephyr-7b)
5. **AI-generated answer is returned** and shown, along with Q&A history

---

## 💡 Example Questions

* "What is the candidate's latest job?"
* "List all technical skills."
* "Which university did the candidate attend?"
* "What is the candidate's email address?"
* "Summarize this candidate in 2 lines."

---

## 🛡️ Security & Privacy

* All resumes are **auto-deleted** after upload/extraction
* **Q&A history is session-only** (not saved after browser close)
* **Your Hugging Face token** is kept private in `.env`

---


<p align="center">
  <b>Made with ❤️ by anshj2002</b>
</p>
