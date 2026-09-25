# Judging Matrix

| Criterion | Evidence already in the project | What to add before submission |
|---|---|---|
| Technical implementation | Local API, deterministic NLP engine, grounded Q&A, quiz generator, runtime detection, PWA cache, unit tests | Connect Whisper Windows/QNN; capture profiler screenshot and reproducible command |
| Use case and innovation | Low-connectivity student persona, Confusion Radar, source IDs, privacy receipt, Malayalam glossary | Interview five students and add two short quotes plus one quantified pain point |
| Deployment and accessibility | One-command local run, zero mandatory packages, responsive UI, keyboard labels, high contrast, large text, speech output, exports | Test on the exact Snapdragon HP model; add installer if time permits |
| Presentation and documentation | Two-minute pitch, 90-second demo flow, architecture and responsible-AI notes | Replace placeholders with measured results; record clean demo video |

## Highest-impact remaining work

1. Verify that the applicant satisfies the Snapdragon laptop eligibility condition.
2. Run the official Qualcomm Whisper Windows sample on that device.
3. Connect its transcript output to `POST /api/analyze`.
4. Measure latency, memory, and at least a small transcription-quality sample.
5. Test the demo with five real students and record concise feedback.
6. Submit only after checking that every form field and uploaded file is final;
   the competition page says a submitted entry cannot be changed.
