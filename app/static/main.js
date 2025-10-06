async function analyze() {
  const url = document.getElementById('url').value.trim();
  const child = document.getElementById('child').checked;
  const status = document.getElementById('status');
  status.textContent = 'Analyzing…';
  status.classList.remove('hidden');
  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, simplify_for_child: child })
    });
    if (!res.ok) throw new Error('Request failed');
    const data = await res.json();
    status.textContent = '';
    document.getElementById('results').classList.remove('hidden');
    document.getElementById('title').textContent = data.title || 'Untitled';
    const ul = document.getElementById('keypoints');
    ul.innerHTML = '';
    (data.key_points || []).forEach(k => {
      const li = document.createElement('li');
      li.textContent = k;
      ul.appendChild(li);
    });
    document.getElementById('child_explanation').textContent = data.child_explanation || '';
    document.getElementById('excerpt').textContent = data.transcript_excerpt || '';
    document.getElementById('download').onclick = async () => {
      const resp = await fetch('/api/download', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
      const blob = await resp.blob();
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = (data.title || 'notes') + '.txt';
      a.click();
    };
    document.getElementById('quiz').onclick = async () => {
      const resp = await fetch('/api/quiz', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ key_points: data.key_points }) });
      const q = await resp.json();
      document.getElementById('qa').classList.remove('hidden');
      document.getElementById('question').textContent = q.question;
      document.getElementById('submit_answer').onclick = async () => {
        const answer = document.getElementById('answer').value;
        const feedbackResp = await fetch('/api/quiz/grade', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question: q.question, answer, key_points: data.key_points }) });
        const fb = await feedbackResp.json();
        document.getElementById('feedback').textContent = fb.feedback;
      };
    };
  } catch (e) {
    status.textContent = 'Error: ' + (e.message || e);
  }
}

document.getElementById('analyze').addEventListener('click', analyze);
