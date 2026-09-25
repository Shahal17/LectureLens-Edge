# Product Roadmap

This roadmap describes product work, not a promise of release dates. Priorities
should change when user research or technical evidence points to a better order.

## Current foundation

The repository already provides:

- a usable local browser interface;
- deterministic transcript analysis;
- stable source IDs and grounded retrieval;
- summaries, concepts, review flags, quizzes, and a technical glossary;
- accessibility controls and user-initiated export;
- local runtime detection, tests, and a repeatable benchmark.

## Milestone 1: strengthen the local MVP

- Define explicit engine and transcription adapter interfaces.
- Add API contract tests and malformed-request coverage.
- Improve quiz distractors and duplicate-concept filtering.
- Add import and export fixtures for regression testing.
- Publish a small set of synthetic evaluation transcripts.

Acceptance criteria:

- all output items retain valid source IDs;
- unsupported questions continue to be declined;
- the app passes automated tests on Python 3.10 through 3.13;
- no network service is required for the default workflow.

## Milestone 2: real audio input

- Add microphone and audio-file controls.
- Connect an offline speech-recognition adapter.
- Preserve timestamps and map them to source IDs.
- Add permission, recording-state, and deletion controls.
- Measure word error rate on consented or openly licensed samples.

Acceptance criteria:

- the user can stop and delete a recording at any time;
- raw audio is not uploaded by default;
- transcription quality and latency are reported from reproducible tests;
- the interface clearly identifies the active transcription engine.

## Milestone 3: grounded local generation

- Add a local language-model adapter for summaries, explanations, and quizzes.
- Require structured output containing source IDs.
- Reject or remove claims that cannot be mapped to transcript evidence.
- Add model-size, memory, and licence information to the runtime screen.

Acceptance criteria:

- every generated learning item passes the evidence check;
- the fallback extractive engine remains available;
- model failures do not erase the user's transcript or session;
- unsupported answers are still refused.

## Milestone 4: student-ready desktop experience

- Add explicit local save, reopen, rename, and delete operations.
- Encrypt saved sessions or integrate with operating-system storage protection.
- Package a signed desktop build.
- Improve onboarding and subject-specific glossary packs.
- Complete accessibility testing with keyboard and screen-reader users.

## Milestone 5: validated hardware acceleration

- Profile supported NPU or GPU adapters on named devices.
- Record latency, memory, battery, model version, runtime version, and power mode.
- Compare accelerated and CPU paths using the same input.
- Publish only reproducible measurements.

The Snapdragon-specific checklist is in
[SNAPDRAGON_DEPLOYMENT.md](SNAPDRAGON_DEPLOYMENT.md).

## Product research

The [user pilot guide](USER_PILOT.md) should be used throughout development, not
only at the end. Useful product signals include:

- whether source markers increase trust;
- whether review flags help students find difficult moments;
- whether quizzes reveal misunderstandings;
- whether students return to the tool each week;
- which accessibility controls are actually used.

## Out of scope for the current project

- replacing teachers, textbooks, or official course material;
- cloud surveillance or institution-level student monitoring;
- silently recording lectures;
- publishing performance or accuracy claims without a reproducible evaluation.
