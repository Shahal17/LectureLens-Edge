const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

const demoTranscript = `Machine learning is a way for computers to learn patterns from examples rather than being programmed with every rule. Supervised learning is the branch in which each training example contains input features and a known target label. The model studies the relationship between those features and labels so that it can make a prediction for a new example. A dataset is normally divided into training data, validation data, and testing data. Training data teaches the model, while validation data helps us choose settings and compare versions. Testing data must remain separate until the end because using it during development gives us an unrealistically optimistic result. This separation is an important safeguard against data leakage.

Classification and regression are the two common supervised learning tasks. Classification predicts a category, such as whether a student is likely to receive an internship. Regression predicts a continuous value, such as the expected salary or the number of days needed to complete a task. A feature is an input measurement used by the model, while a label is the answer that the model is expected to learn. Good features describe the problem without revealing the answer unfairly.

Overfitting happens when a model memorises details and noise in the training data instead of learning a pattern that generalises. An overfit model may score extremely well during training but fail on unseen examples. We can reduce overfitting by collecting more representative data, simplifying the model, using regularisation, or stopping training at the right time. However, a model that is too simple can underfit and miss useful structure. The key is to balance bias and variance.

Accuracy alone is not enough for every problem. In an imbalanced medical screening dataset, a model can achieve high accuracy while missing most positive cases. Precision tells us how many predicted positives were correct, and recall tells us how many real positives the model found. The choice of metric should follow the real cost of each type of mistake. Remember that a useful machine learning system combines a clear problem, trustworthy data, an appropriate model, and evaluation that reflects the people affected by its predictions.`;

const state = { result: null, runtime: null, quizAnswers: new Map() };

function escapeHtml(value = "") {
  return String(value).replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  }[character]));
}

function sourceBadge(source) {
  return `<span class="source-ref" title="Transcript sentence ${source}">S${source}</span>`;
}

async function loadRuntime() {
  try {
    const response = await fetch("/api/health");
    state.runtime = await response.json();
    const runtime = state.runtime.runtime;
    $("#runtimeLabel").textContent = runtime.qnn_available ? "Snapdragon NPU ready" : "Local reference engine";
  } catch {
    $("#runtimeLabel").textContent = "Local app shell";
  }
}

function updateWordCount() {
  const words = $("#transcriptInput").value.trim().split(/\s+/).filter(Boolean).length;
  $("#wordCounter").textContent = `${words.toLocaleString()} words`;
}

function metric(label, value) {
  return `<div class="metric"><b>${escapeHtml(value)}</b><span>${escapeHtml(label)}</span></div>`;
}

function renderResult(result) {
  state.result = result;
  state.quizAnswers.clear();
  $("#resultsSection").classList.remove("hidden");
  $("#resultSubtitle").textContent = `${result.title} • ${result.subject}`;
  $("#metrics").innerHTML = [
    metric("Words processed", result.metrics.words),
    metric("Key concepts", result.metrics.concepts),
    metric("Review flags", result.metrics.review_flags),
    metric("Reading time", `${result.metrics.reading_minutes} min`),
    metric("Cloud calls", result.metrics.external_calls),
  ].join("");

  $("#summaryList").innerHTML = result.summary.map(item =>
    `<div class="summary-item">${escapeHtml(item.text)} ${sourceBadge(item.source)}</div>`
  ).join("");

  $("#conceptList").innerHTML = result.concepts.map(item =>
    `<span class="chip">${escapeHtml(item.term)} · ${item.mentions}</span>`
  ).join("");

  $("#reviewList").innerHTML = result.review_flags.length ? result.review_flags.map(item =>
    `<div class="review-item"><span class="review-time">${escapeHtml(item.time)}</span><div><b>${escapeHtml(item.reason)} ${sourceBadge(item.source)}</b><p>${escapeHtml(item.text)}</p></div></div>`
  ).join("") : `<p class="panel-copy">No unusually dense sections detected.</p>`;

  $("#notesList").innerHTML = result.summary.map((item, index) =>
    `<div class="note"><span class="note-number">0${index + 1}</span><div><p>${escapeHtml(item.text)} ${sourceBadge(item.source)}</p><small>Grounded in transcript sentence ${item.source}</small></div></div>`
  ).join("");

  $("#quizList").innerHTML = result.quiz.length ? result.quiz.map((item, index) => `
    <section class="quiz-card" data-quiz="${index}">
      <p><b>Q${index + 1}.</b> ${escapeHtml(item.question)} ${sourceBadge(item.source)}</p>
      <div class="quiz-options">${item.options.map(option => `<button data-option="${escapeHtml(option)}">${escapeHtml(option)}</button>`).join("")}</div>
    </section>`).join("") : `<p class="panel-copy">Add a longer transcript to generate a quiz.</p>`;
  updateQuizScore();

  $("#glossaryList").innerHTML = result.glossary.length ? result.glossary.map(item =>
    `<div class="glossary-item"><strong>${escapeHtml(item.term)}</strong><span lang="ml">${escapeHtml(item.malayalam)}</span></div>`
  ).join("") : `<p class="panel-copy">No mapped Malayalam terms appeared in this lecture.</p>`;

  $("#sourceList").innerHTML = result.sources.map(item =>
    `<div class="source" id="source-${item.id}"><b>S${item.id}</b><span>${escapeHtml(item.text)}</span></div>`
  ).join("");

  const runtime = state.runtime?.runtime || {};
  $("#runtimeDetails").innerHTML = [
    ["Current engine", result.engine.name],
    ["Provider", runtime.provider || "Portable reference engine"],
    ["Device", `${runtime.os || "Unknown"} / ${runtime.architecture || "Unknown"}`],
    ["QNN detected", runtime.qnn_available ? "Yes" : "Not on this device"],
  ].map(([label, value]) => `<div class="runtime-detail"><span>${escapeHtml(label)}</span><b>${escapeHtml(value)}</b></div>`).join("");

  $("#resultsSection").scrollIntoView({ behavior: "smooth", block: "start" });
}

async function analyse() {
  const transcript = $("#transcriptInput").value.trim();
  const button = $("#analyseButton");
  $("#errorMessage").textContent = "";
  button.disabled = true;
  button.querySelector("span").textContent = "Processing locally…";
  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcript, title: $("#titleInput").value, subject: $("#subjectInput").value })
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Analysis failed.");
    renderResult(result);
  } catch (error) {
    $("#errorMessage").textContent = error.message;
  } finally {
    button.disabled = false;
    button.querySelector("span").textContent = "Analyse privately";
  }
}

async function askLecture() {
  const question = $("#questionInput").value.trim();
  if (!question || !state.result) return;
  $("#answerBox").innerHTML = "Searching only this lecture…";
  const response = await fetch("/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ transcript: $("#transcriptInput").value, question })
  });
  const answer = await response.json();
  $("#answerBox").innerHTML = `<strong>${answer.supported ? "Grounded answer" : "Not enough evidence"}</strong>${escapeHtml(answer.answer)} ${answer.source ? sourceBadge(answer.source) : ""}`;
}

function updateQuizScore() {
  const total = state.result?.quiz.length || 0;
  let correct = 0;
  state.quizAnswers.forEach((isCorrect) => { if (isCorrect) correct += 1; });
  $("#quizScore").textContent = `${correct} / ${total}`;
}

function answerQuiz(button) {
  const card = button.closest(".quiz-card");
  const index = Number(card.dataset.quiz);
  if (state.quizAnswers.has(index)) return;
  const correctAnswer = state.result.quiz[index].answer;
  const selected = button.dataset.option;
  state.quizAnswers.set(index, selected === correctAnswer);
  card.querySelectorAll("button").forEach(option => {
    if (option.dataset.option === correctAnswer) option.classList.add("correct");
    else if (option === button) option.classList.add("wrong");
    option.disabled = true;
  });
  updateQuizScore();
}

function download(name, content, type) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url; anchor.download = name; anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 500);
}

function exportMarkdown() {
  if (!state.result) return;
  const result = state.result;
  const lines = [`# ${result.title}`, ``, `**Subject:** ${result.subject}`, ``, `## Summary`, ""];
  result.summary.forEach(item => lines.push(`- ${item.text} [S${item.source}]`));
  lines.push("", "## Key concepts", "", result.concepts.map(item => `- ${item.term}`).join("\n"), "", "## Review moments", "");
  result.review_flags.forEach(item => lines.push(`- ${item.time} — ${item.reason} [S${item.source}]`));
  lines.push("", "_Generated locally by LectureLens Edge. Verify important details against the source lecture._");
  download("lecturelens-notes.md", lines.join("\n"), "text/markdown");
}

function speakSummary() {
  if (!state.result || !window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(state.result.summary.map(item => item.text).join(" "));
  utterance.rate = 0.92;
  window.speechSynthesis.speak(utterance);
}

function bindEvents() {
  $("#demoButton").addEventListener("click", () => { $("#transcriptInput").value = demoTranscript; updateWordCount(); });
  $("#transcriptInput").addEventListener("input", updateWordCount);
  $("#analyseButton").addEventListener("click", analyse);
  $("#askButton").addEventListener("click", askLecture);
  $("#themeButton").addEventListener("click", () => document.body.classList.toggle("high-contrast"));
  $("#fontUp").addEventListener("click", () => document.body.classList.toggle("large-text"));
  $("#readingMode").addEventListener("click", () => document.body.classList.toggle("reading-mode"));
  $("#speakSummary").addEventListener("click", speakSummary);
  $("#exportMarkdown").addEventListener("click", exportMarkdown);
  $("#exportJson").addEventListener("click", () => state.result && download("lecturelens-session.json", JSON.stringify(state.result, null, 2), "application/json"));
  $("#quizList").addEventListener("click", event => { if (event.target.matches("button[data-option]")) answerQuiz(event.target); });
  $$(".tabs button").forEach(button => button.addEventListener("click", () => {
    $$(".tabs button").forEach(tab => tab.classList.toggle("active", tab === button));
    $$(".tab-panel").forEach(panel => panel.classList.remove("active"));
    $(`#${button.dataset.tab}Panel`).classList.add("active");
  }));
}

bindEvents();
loadRuntime();
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});
