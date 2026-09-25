# Architecture and Design Decisions

## Data flow

```text
Local input
   │
   ├── Reference MVP: pasted transcript
   └── Snapdragon build: microphone → Whisper/QNN
   │
   ▼
Sentence segmentation → stable source IDs
   │
   ├── concept extraction
   ├── summary selection / local LLM
   ├── confusion signals
   ├── grounded retrieval
   └── quiz generation
   │
   ▼
Local browser UI → optional user-initiated export
```

## Security and privacy boundaries

- The server binds to `127.0.0.1` by default, not the local network.
- The API rejects request bodies above 1 MB.
- The default workflow keeps content in process and browser memory.
- No analytics, remote fonts, CDN scripts, cloud model API, or account is used.
- Export occurs only after a user action.
- User text is inserted through escaped templates to reduce HTML injection risk.

## Grounding strategy

Transcript sentences receive stable source IDs before any learning material is
created. The reference Q&A engine ranks sentences by query coverage and refuses
low-evidence questions. The LLM adapter should be constrained to return source
IDs, and a post-generation verifier should remove claims that cannot be mapped to
those sources.

## Why a local web interface

A localhost PWA gives a polished cross-platform demo while keeping the inference
process local. The same interface can later be wrapped for Windows without
changing the model contract. It is also easy for judges to inspect and for
students to use with keyboard and screen-reading tools.
