# Submission Proposal — LectureLens Edge

## Applicant

**Mohammed Shahal**  
B.Tech Computer Science and Engineering (Artificial Intelligence & Machine Learning)  
MEA Engineering College, Kerala, India

## One-line pitch

LectureLens Edge is a privacy-first, offline learning copilot that turns classroom
speech into source-grounded notes, review moments, and quizzes on a Snapdragon-
powered PC—especially for students limited by connectivity, language friction,
or hearing accessibility.

## Problem

Many students do not lose marks because they lack effort; they lose the thread of
a lecture in real time. Fast speech, unfamiliar technical English, background
noise, and unreliable internet compound the problem. Existing meeting assistants
often depend on cloud upload, creating three barriers:

1. lecture audio and student questions may leave the device;
2. recurring subscriptions and bandwidth are difficult for low-income students;
3. cloud latency and outages make the tool unreliable inside the classroom.

This problem is especially visible in tier-2 and tier-3 colleges, where a useful
learning tool must work even when the network does not.

## Solution

LectureLens Edge processes a lecture locally and creates a compact learning pack:

- multilingual speech-to-text;
- concise, source-linked notes;
- a “Confusion Radar” highlighting dense explanations, contrasts, and exceptions;
- an active-recall quiz generated only from lecture evidence;
- question answering that cites the supporting transcript sentence and declines
  unsupported questions;
- English–Malayalam technical glossary and accessible reading controls;
- a privacy receipt showing the number of external calls and bytes uploaded.

The portable MVP already implements the end-to-end experience. The Snapdragon
build will use Qualcomm AI Hub's Whisper-Base model for NPU-accelerated speech
recognition and a quantized Llama 3.2 3B Instruct model for structured notes and
quiz generation.

## Why Snapdragon

This is not “AI on a PC” as a branding layer. On-device inference directly solves
the product's constraints:

- **privacy:** raw classroom audio does not need to leave the laptop;
- **reliability:** core features continue without Wi-Fi;
- **latency:** NPU inference can create feedback while the lecture is still useful;
- **efficiency:** dedicated NPU execution is designed for sustained AI workloads;
- **accessibility:** a student can use the same device for capture, notes, review,
  and text-to-speech.

The target implementation uses the ONNX Runtime QNN execution provider demonstrated
by Qualcomm's Whisper Windows sample. The language model is quantized for
on-device deployment on Snapdragon X-series reference devices.

## User journey

1. The student starts a local session and selects the subject.
2. Whisper transcribes the lecture on the Snapdragon NPU.
3. LectureLens segments the transcript and attaches stable source IDs.
4. The local language model produces structured notes and quiz candidates.
5. A grounding layer checks that every output maps to transcript evidence.
6. The student reviews dense moments, asks a question, and exports notes.
7. Closing the session removes temporary data unless the student explicitly saves it.

## Innovation

LectureLens Edge combines four ideas that are usually separated:

1. **Learning, not meeting minutes:** outputs are designed for recall and revision.
2. **Grounding by default:** every summary point, quiz answer, and response retains
   its source sentence.
3. **Confusion Radar:** complexity signals prioritise the parts most likely to need
   replay or teacher clarification.
4. **Verifiable privacy:** the interface presents a plain-language receipt instead
   of asking users to trust a vague “private AI” claim.

## Technical implementation

```text
Microphone / audio file
        │
        ▼
Whisper-Base on Snapdragon NPU (ONNX Runtime + QNN)
        │ timestamped transcript
        ▼
Segmentation + source-ID evidence layer
        │
        ├──► Quantized Llama 3.2 3B: notes, quiz, simplification
        ├──► Confusion Radar: density and contrast signals
        └──► Local retrieval: grounded question answering
        │
        ▼
Offline accessible PWA + Markdown/JSON export
```

The reference MVP has no mandatory Python dependencies and uses a deterministic
extractive engine so the product flow can be reviewed on any laptop. Runtime
detection reports whether QNN is actually available, preventing false NPU claims.

## Deployment and accessibility

- local web application bound to `127.0.0.1`;
- installable offline PWA shell;
- keyboard-accessible controls and semantic labels;
- high-contrast, large-text, reading-spacing, and text-to-speech modes;
- Markdown/JSON export for interoperability;
- no login and no default cloud retention.

## Evaluation plan

Before final judging, test at least five lecture clips across quiet and noisy rooms.
Report only measured values:

- word error rate for transcription;
- end-to-end latency and real-time factor;
- peak memory and battery change during a 30-minute session;
- percentage of generated claims with a valid source sentence;
- quiz-answer correctness;
- student-rated usefulness and clarity (five-person pilot minimum).

## Responsible AI

- The product states when it cannot find supporting evidence.
- Notes are an aid, not an authoritative replacement for the lecturer or textbook.
- Sessions remain local unless the user explicitly exports them.
- The interface never labels heuristic output as NPU inference.
- Medical, legal, or safety-critical lectures display a verification reminder.

## Current status and next milestone

Completed: responsive interface, local API, notes, concepts, grounded Q&A, quiz,
Confusion Radar, Malayalam glossary, exports, privacy receipt, runtime detection,
offline caching, automated tests, and demo material.

Next: connect the official Whisper Windows pipeline, add the quantized LLM adapter,
and collect reproducible Snapdragon profiling results.
