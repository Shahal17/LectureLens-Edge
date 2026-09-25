# Local API Reference

LectureLens Edge exposes a small JSON API from the same local server that serves
the browser interface.

Default base URL:

```text
http://127.0.0.1:8765
```

## Health

`GET /api/health`

```bash
curl http://127.0.0.1:8765/api/health
```

Example response:

```json
{
  "status": "ready",
  "local_only": true,
  "runtime": {
    "os": "Linux",
    "architecture": "x86_64",
    "qnn_available": false
  },
  "engine_version": "0.1.0-local"
}
```

Runtime fields can vary by operating system and installed accelerator support.

## Analyse a transcript

`POST /api/analyze`

Request body:

```json
{
  "title": "Introduction to machine learning",
  "subject": "Machine Learning",
  "transcript": "Machine learning systems learn patterns from examples. Training data teaches the model, while testing data measures final performance. Testing data must remain separate until the end because using it during development can create data leakage."
}
```

Example request:

```bash
curl -X POST http://127.0.0.1:8765/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"title":"Introduction to machine learning","subject":"Machine Learning","transcript":"Machine learning systems learn patterns from examples. Training data teaches the model, while testing data measures final performance. Testing data must remain separate until the end because using it during development can create data leakage."}'
```

The response contains:

- `summary`: selected statements with `source` IDs;
- `concepts`: recurring concepts and their first source;
- `review_flags`: dense or contrast-heavy moments to revisit;
- `quiz`: locally generated active-recall questions;
- `glossary`: matching English-Malayalam technical explanations;
- `sources`: the stable sentence list used for grounding;
- `metrics`: local document statistics and external-call count;
- `engine`: the active engine name, version, and mode.

Validation rules:

- transcript length must be between 80 and 120,000 characters;
- the transcript must contain at least two complete sentences;
- request bodies larger than 1 MB are rejected.

## Ask a grounded question

`POST /api/ask`

```bash
curl -X POST http://127.0.0.1:8765/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Why should testing data remain separate?","transcript":"Training data teaches the model. Testing data must remain separate because using it during development creates an unrealistically optimistic result."}'
```

A supported response includes the answer, the source sentence ID, and a retrieval
score:

```json
{
  "answer": "Testing data must remain separate because using it during development creates an unrealistically optimistic result.",
  "supported": true,
  "source": 2,
  "score": 0.42
}
```

When the transcript lacks enough evidence, `supported` is `false` and
`source` is `null`.

## Errors

Client errors return HTTP `400` with a JSON `error` field. Unknown API routes
return `404`. Unexpected processing failures return a generic `500` response
without an internal traceback.
