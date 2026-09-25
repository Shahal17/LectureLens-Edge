# Architecture and Design Decisions

LectureLens Edge is separated into a browser interface, a local HTTP boundary,
and a replaceable learning engine. The separation keeps the current application
useful while speech and language-model adapters are developed independently.

## Data flow

```text
Transcript input
      │
      ▼
Sentence segmentation and stable source IDs
      │
      ├── summary selection
      ├── concept extraction
      ├── confusion signals
      ├── grounded retrieval
      └── quiz generation
      │
      ▼
Local browser interface and user-initiated export
```

Planned audio flow:

```text
Microphone or audio file
      │
      ▼
Offline speech adapter
      │ timestamped transcript
      ▼
Existing source and learning pipeline
```

## Components

### Browser interface

The `app/` directory contains a dependency-free interface for transcript input,
results, accessibility controls, question answering, and export. The app talks
only to the local API by default.

### Local HTTP server

`engine/server.py` serves the static app and JSON endpoints. It binds to
`127.0.0.1` by default, limits request size, disables response caching for API
data, and returns generic internal-error messages.

### Reference learning engine

`engine/lecture_engine.py` provides deterministic analysis with no model
download. It establishes the product's output contract and fallback behaviour:

- source-indexed summaries;
- concept metadata;
- review flags;
- grounded question answering;
- quiz items with answer sources;
- session metrics and engine identity.

### Runtime detection

`engine/runtime.py` reports the operating system, architecture, and whether an
optional QNN provider can be discovered. Detection does not mean the current
analysis request used that provider. The interface keeps active-engine identity
separate from available runtime capability.

## Grounding strategy

Transcript sentences receive stable source IDs before any learning material is
created. The current question-answering engine ranks sentences by query coverage
and refuses low-evidence questions.

A future language-model adapter must:

1. return source IDs with every generated learning item;
2. use only IDs from the active transcript;
3. pass a post-generation evidence check;
4. remove unsupported claims or return a refusal;
5. preserve the deterministic engine as a fallback.

## Security and privacy boundaries

- The default server is reachable only from the current computer.
- API request bodies larger than 1 MB are rejected.
- The current workflow keeps content in process and browser memory.
- No analytics, remote fonts, CDN scripts, cloud model API, or account is used.
- Export occurs only after a user action.
- User text is rendered through HTML escaping helpers.

The application is not designed as a public multi-user server. Binding it to a
non-loopback address requires a separate authentication and threat-model review.

## Why a local web interface

A local web interface provides a cross-platform, accessible product surface while
keeping processing on the user's computer. It can later be wrapped as a desktop
application without changing the engine contract.

## Extension points

Planned adapters should remain behind explicit interfaces:

- `TranscriptionAdapter.transcribe(audio) -> transcript segments`
- `LearningAdapter.analyze(sources) -> structured learning pack`
- `StorageAdapter.save(session) -> local session reference`

Adapters must declare whether they use the network, where data is retained, the
model and runtime versions, and which acceleration provider was actually used.
