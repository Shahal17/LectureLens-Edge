# Two-Minute Pitch Script

## 0:00–0:20 — Problem

“A student can sit through an entire lecture and still lose the key idea. This is
common when the lecturer speaks quickly, the subject uses unfamiliar English, or
the classroom internet is unreliable. Cloud meeting assistants are not designed
for this student: they upload sensitive audio, consume bandwidth, and produce
minutes rather than learning.”

## 0:20–0:42 — Solution

“LectureLens Edge is an offline learning copilot for Snapdragon-powered PCs. It
turns classroom speech into source-grounded notes, highlights the moments most
likely to cause confusion, creates an active-recall quiz, and answers questions
using only evidence from that lecture.”

## 0:42–1:15 — Demo

“I will load a short machine-learning lecture. Notice the privacy indicator: no
account and zero cloud calls. In one local pass, LectureLens creates a summary,
key concepts, and a Confusion Radar. Every learning item has a source marker.
When I ask why test data must remain separate, the answer points to the exact
sentence. If I ask something absent from the lecture, it refuses instead of
inventing an answer. The student can then take a quiz, use large-text or spoken
summary mode, and export revision notes.”

## 1:15–1:42 — Snapdragon advantage

“The target build uses Qualcomm AI Hub's Whisper-Base through ONNX Runtime and
the QNN execution provider for speech recognition on the NPU. A quantized Llama
3.2 3B model creates structured learning material locally. Snapdragon is the
reason the product can be private, responsive, and available without Wi-Fi—not
just the device on which the interface is displayed.”

## 1:42–2:00 — Impact and close

“I am building for students like those in low-connectivity colleges across India:
capable students who need a second chance to understand the lecture, not another
subscription. LectureLens Edge turns the AI PC into a private learning equaliser:
hear less noise, keep more knowledge.”

## Likely judge questions

**Is the NPU integration complete?**  
“The cross-platform reference MVP and output contract are complete. The official
Whisper/QNN adapter and profiling are the next hardware-dependent milestone. I
will present measured performance only after testing on the target laptop.”

**How is this different from a meeting assistant?**  
“The unit of value is learning: source-grounded notes, confusion prioritisation,
active recall, bilingual technical support, and offline classroom reliability.”

**How do you reduce hallucinations?**  
“Every answer must retrieve supporting transcript sentences. Unsupported
questions are declined, and the interface exposes the source to the student.”

**What is the business path?**  
“A free student edition can establish trust. Institutions can pay for managed
deployment, subject packs, accessibility administration, and aggregate opt-in
learning analytics without collecting raw audio.”
