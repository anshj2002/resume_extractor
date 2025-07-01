from flask import Flask, render_template, request, jsonify, session
import os
from pypdf import PdfReader
import docx
import requests
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # For session management (Q&A history)

# -- Hugging Face API Setup --
HF_API_URL = "https://api-inference.huggingface.co/models/google/gemma-1.1-2b-it"
HF_TOKEN = "YOUR_HF_TOKEN"  
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def extract_text(file_path):
    """
    Extracts text from a PDF or DOCX file.
    PDF: Extracts text from each page.
    DOCX: Extracts text from all paragraphs.
    """
    if file_path.endswith('.pdf'):
        text = ""
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

def ask_huggingface_api(question, resume_text):
    """
    Asks the Hugging Face model a question based on resume text.
    Returns the generated answer as a string.
    """
    prompt = f"""You are a helpful assistant analyzing job candidate resumes.
Resume:
{resume_text[:3000]}  # Limit to 3000 chars for HF API safety.
Question: {question}
Answer:"""
    data = {"inputs": prompt, "parameters": {"max_new_tokens": 128}}
    response = requests.post(HF_API_URL, headers=HF_HEADERS, json=data, timeout=60)
    if response.status_code == 200:
        result = response.json()
        # For text-generation models, result[0]['generated_text'] contains the answer.
        answer = result[0].get('generated_text', '').replace(prompt, '').strip()
        return answer
    else:
        return f"Error from Hugging Face API: {response.status_code} {response.text}"

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    """
    Handles resume file upload.
    Extracts text, deletes the file, and resets Q&A history.
    """
    file = request.files['resume']
    filename = file.filename
    filepath = os.path.join('uploads', filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(filepath)
    resume_text = extract_text(filepath)
    try:
        os.remove(filepath)  # Delete uploaded file right after extraction!
    except Exception as e:
        print(f"Could not delete uploaded file: {e}")
    session['qa_history'] = []  # Reset history on new upload
    return jsonify({'resume_text': resume_text})

@app.route('/ask', methods=['POST'])
def ask():
    """
    Handles the Q&A request.
    - Gets the question and resume text from the client.
    - Calls the Hugging Face API and returns the answer.
    - Stores up to 10 recent Q&A pairs in the session.
    """
    try:
        data = request.json
        question = data['question']
        resume_text = data['resume_text']
        answer = ask_huggingface_api(question, resume_text)
        # Add to session history
        history = session.get('qa_history', [])
        history.append({'question': question, 'answer': answer})
        session['qa_history'] = history[-10:]  # Keep only last 10 Q&As
        return jsonify({'answer': answer, 'qa_history': session['qa_history']})
    except Exception as e:
        print("Error in /ask:", e)
        return jsonify({'answer': f"Error: {str(e)}", 'qa_history': session.get('qa_history', [])}), 500

if __name__ == '__main__':
    app.run(debug=True)
