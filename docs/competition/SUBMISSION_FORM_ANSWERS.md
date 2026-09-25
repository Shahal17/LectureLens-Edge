# Paste-Ready Submission Answers

Review the official form's character limits before pasting. Do not claim the NPU
milestone until it has been tested on the target laptop.

## Project name

LectureLens Edge

## Tagline

Private, offline lecture intelligence for every classroom.

## Short description

LectureLens Edge transforms classroom speech into source-grounded notes, review
moments, quizzes, and answers directly on a Snapdragon-powered PC. It is designed
for students facing unreliable internet, unfamiliar technical English, or hearing
accessibility barriers. Raw lecture content stays on the laptop, and every learning
item points back to supporting transcript evidence.

## Problem statement

Students often lose important ideas during fast or technically dense lectures.
This challenge is worse in low-connectivity colleges and for learners studying in
a second language. Most existing transcription and meeting tools depend on cloud
upload, bandwidth, and subscriptions, while producing meeting minutes rather than
revision material. Students need a private tool that works in the classroom even
without dependable internet and helps them understand—not merely record—the lesson.

## Proposed solution

LectureLens Edge uses on-device speech recognition to create a timestamped lecture
transcript. It then produces concise source-linked notes, identifies dense sections
through a Confusion Radar, generates an active-recall quiz, and answers questions
only when the transcript provides evidence. Accessibility features include high
contrast, larger reading text, spoken summaries, and an English–Malayalam technical
glossary. A privacy receipt makes zero-cloud processing visible to the learner.

## What makes it innovative?

Unlike a generic meeting assistant, LectureLens is built around how students learn.
Its Confusion Radar prioritises difficult moments, active recall turns passive notes
into revision, and source IDs make every output auditable. The interface also proves
its privacy claim by showing the current runtime, external-call count, and uploaded
bytes. The result is an offline learning workflow rather than another transcript app.

## How does it use Snapdragon?

The target pipeline runs Qualcomm AI Hub's Whisper-Base through ONNX Runtime and
the QNN execution provider for NPU-accelerated speech recognition. A quantized
Llama 3.2 3B Instruct model creates structured notes and quiz candidates locally.
Snapdragon enables the central value proposition: private classroom audio,
low-latency feedback, offline reliability, and efficient sustained inference on one
student laptop.

## Current implementation status

A working portable MVP is complete: responsive offline interface, local API,
transcript analysis, source-grounded notes, concept extraction, Confusion Radar,
grounded question answering, quiz generation, Malayalam glossary, accessibility
controls, privacy receipt, export, runtime detection, and automated tests. The final
hardware milestone is connecting and profiling the official Whisper/QNN path on an
eligible Snapdragon-powered Windows laptop.

## Technology stack

- Python local API and deterministic reference NLP engine
- HTML, CSS, and vanilla JavaScript offline PWA
- ONNX Runtime + QNN Execution Provider (target runtime)
- Qualcomm AI Hub Whisper-Base (target speech model)
- Quantized Llama 3.2 3B Instruct (target language model)
- Local evidence retrieval and source validation

## Target users

College and university students, especially learners in low-connectivity campuses,
students using English as a second language, and students who benefit from captions,
large text, spoken summaries, or structured revision support.

## Expected impact

LectureLens Edge can reduce the gap between attending a lecture and understanding
it. Students gain a private second pass over difficult material, teachers spend less
time repeating missed definitions, and institutions can offer accessibility support
without uploading classroom audio. Initial validation will measure transcription
quality, grounding rate, quiz correctness, and usefulness ratings from a student pilot.

## Repository description

Offline, source-grounded lecture notes, Q&A, quizzes, and accessibility support for
Snapdragon AI PCs.

## Suggested tags

On-device AI, Edge AI, Education, Accessibility, Speech Recognition, Snapdragon,
Privacy, Low Connectivity, Student Innovation
