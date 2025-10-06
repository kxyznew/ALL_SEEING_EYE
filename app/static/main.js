let lastData = null;
let currentUtterance = null;

function getAquaVoice() {
  const voices = window.speechSynthesis ? speechSynthesis.getVoices() : [];
  if (!voices || voices.length === 0) return null;
  // Prefer a voice literally named 'Aqua' if available
  let v = voices.find(v => /aqua/i.test(v.name));
  if (v) return v;
  // Otherwise prefer an English female-sounding voice
  const english = voices.filter(v => /en[-_]/i.test(v.lang) || /English/i.test(v.name));
  v = english.find(v => /female|woman|girl|sara|jenny|emma|lucy|amy|salli|aria|zoe|linda/i.test(v.name)) || english[0];
  return v || voices[0];
}

function speakAqua(text) {
  if (!('speechSynthesis' in window)) {
    alert('Text-to-speech is not supported in this browser.');
    return;
  }
  if (currentUtterance) {
    speechSynthesis.cancel();
    currentUtterance = null;
  }
  const utter = new SpeechSynthesisUtterance(text);
  const voice = getAquaVoice();
  if (voice) utter.voice = voice;
  // Aqua vibe: calm, clear, slightly higher pitch, steady pace
  utter.rate = 0.95;
  utter.pitch = 1.15;
  utter.volume = 1.0;
  currentUtterance = utter;
  utter.onend = () => {
    currentUtterance = null;
    document.getElementById('stop_read').classList.add('hidden');
  };
  speechSynthesis.speak(utter);
}

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
    lastData = data;
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

    const readBtn = document.getElementById('read');
    const stopBtn = document.getElementById('stop_read');
    readBtn.onclick = () => {
      const parts = [];
      if (data.title) parts.push(`Title: ${data.title}.`);
      if (data.key_points?.length) {
        parts.push('Key points:');
        data.key_points.forEach((kp, i) => parts.push(`${i + 1}. ${kp}`));
      }
      if (data.child_explanation) {
        parts.push('Explanation for kids:');
        parts.push(data.child_explanation);
      }
      const text = parts.join('\n');
      document.getElementById('stop_read').classList.remove('hidden');
      speakAqua(text);
    };
    stopBtn.onclick = () => {
      if (currentUtterance) {
        speechSynthesis.cancel();
        currentUtterance = null;
      }
      stopBtn.classList.add('hidden');
    };
  } catch (e) {
    status.textContent = 'Error: ' + (e.message || e);
  }
}

document.getElementById('analyze').addEventListener('click', analyze);

// Ensure voices are loaded
if ('speechSynthesis' in window) {
  speechSynthesis.onvoiceschanged = () => {
    // cache voices by calling getter once
    speechSynthesis.getVoices();
  };
}
