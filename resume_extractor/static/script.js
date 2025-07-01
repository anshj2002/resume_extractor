// Prevent duplicate submits during processing
let processing = false;

// Show or hide the loader, disable/enable inputs and buttons, focus loader
function showLoader(show) {
  const loader = document.getElementById('loader');
  const questionBox = document.getElementById('question');
  const submitBtn = document.querySelector('#qaForm button[type=submit]');
  if (show) {
    loader.classList.remove('d-none');
    loader.scrollIntoView({ behavior: 'smooth', block: 'center' });
    questionBox.setAttribute('disabled', 'disabled');
    submitBtn.setAttribute('disabled', 'disabled');
  } else {
    loader.classList.add('d-none');
    questionBox.removeAttribute('disabled');
    submitBtn.removeAttribute('disabled');
    questionBox.focus();
  }
}

// Handle the Ask/Enter Q&A
async function handleQA(e) {
  e.preventDefault();
  if (processing) return; // Block if already processing
  const question = document.getElementById('question').value.trim();
  if (!question) return;

  processing = true;
  showLoader(true);

  try {
    const resume_text = document.getElementById('resumeText').value;
    const response = await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, resume_text })
    });
    const data = await response.json();
    displayAnswer(data.answer, data.qa_history);
  } catch (err) {
    displayAnswer("An error occurred. Please try again.");
  } finally {
    showLoader(false);
    processing = false;
  }
}

// Main form submit
document.getElementById('qaForm').onsubmit = handleQA;

// Allow Enter key in the input
document.getElementById('question').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') {
    e.preventDefault();
    if (!processing) handleQA(e);
  }
});

// Show answer and history
function displayAnswer(answer, qa_history=[]) {
  const answerDiv = document.getElementById('answer');
  answerDiv.textContent = answer;
  answerDiv.classList.remove('d-none');
  displayHistory(qa_history);
}

// Show the Q&A history
function displayHistory(history) {
  const historyDiv = document.getElementById('qa-history');
  if (!history || history.length === 0) {
    historyDiv.innerHTML = "";
    return;
  }
  let html = "<h6>Recent Q&A History:</h6><ul class='list-group'>";
  history.slice().reverse().forEach(pair => {
    html += `<li class="list-group-item"><b>Q:</b> ${pair.question}<br><b>A:</b> ${pair.answer}</li>`;
  });
  html += "</ul>";
  historyDiv.innerHTML = html;
}

// Resume upload handler
document.getElementById('uploadForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  const response = await fetch('/upload', { method: 'POST', body: formData });
  const data = await response.json();
  document.getElementById('resumeText').value = data.resume_text;
  document.getElementById('resume-section').classList.remove('d-none');
  // Clear answer and history
  document.getElementById('answer').classList.add('d-none');
  displayHistory([]);
});
