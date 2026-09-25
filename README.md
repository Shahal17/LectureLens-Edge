# LectureLens Edge

**Private, offline lecture intelligence for low-connectivity classrooms.**

LectureLens Edge turns a lecture transcript into concise notes, key concepts,
review flags, source-grounded answers, and a self-test quiz. The reference MVP
runs entirely on the user's laptop with no account, cloud API, or external
network call. The target Snapdragon build replaces the reference transcript
input and extractive engine with Qualcomm AI Hub models accelerated on the NPU.

> Competition status: the portable reference MVP is implemented and tested.
> Final Whisper/QNN profiling must be completed on an eligible Snapdragon-
> powered Windows laptop before claiming NPU performance.

## Why this can stand out

- **A specific underserved user:** students in Indian colleges with unreliable
  connectivity, English-as-a-second-language friction, or hearing-access needs.
- **A real reason to run at the edge:** lecture audio is sensitive, latency
  matters, and classrooms cannot assume reliable broadband.
- **A visible, judgeable demo:** one click produces notes, a quiz, cited answers,
  a complexity map, a bilingual glossary, and a privacy receipt.
- **A credible Snapdragon path:** Qualcomm publishes a Windows Whisper sample
  using ONNX Runtime and the Snapdragon NPU, plus quantized LLMs for Snapdragon
  X-series devices.

## 60-second quick start

Requirements: Python 3.10 or newer. No packages are required for the reference
MVP.

### Windows

```powershell
py run.py
```

Or double-click `run_windows.bat`.

### macOS / Linux

```bash
python3 run.py
```

Then open <http://127.0.0.1:8765>. Select **Load demo lecture** and then
**Analyse privately**.

## Demo flow

1. Load the sample machine-learning lecture.
2. Analyse it and show the privacy receipt (`0 cloud calls`).
3. Open **Smart notes** and **Quiz**.
4. Ask: `Why should we keep test data separate?`
5. Turn on high contrast or reading mode in **Accessibility**.
6. Export the notes as Markdown.

## What is genuinely working now

| Capability | Reference MVP | Snapdragon target |
|---|---|---|
| Transcript input | Paste/sample transcript | Whisper-Base on NPU |
| Notes and concepts | Local extractive engine | Quantized Llama 3.2 3B |
| Grounded Q&A | Local sentence retrieval with source | LLM response constrained to transcript |
| Quiz | Local concept/cloze generator | LLM generation + grounding check |
| Malayalam support | Local technical glossary | Multilingual model/translation adapter |
| Privacy receipt | Working | Working + NPU telemetry |
| Offline app shell | Working | Working |

The reference engine is intentionally transparent. It demonstrates the complete
product flow without pretending that a CPU heuristic is an NPU model.

## Project structure

```text
LectureLens-Edge/
├── app/                    # Offline, accessible web interface
├── engine/                 # Local analysis API and runtime detection
├── tests/                  # Standard-library unit tests
├── config/                 # Target model registry
├── docs/                   # Proposal, pitch, demo, architecture, judging map
├── run.py                  # Cross-platform launcher
├── run_windows.bat         # Windows one-click launcher
└── LICENSE
```

## Test

```bash
python3 -m unittest discover -s tests -v
python3 tools/benchmark.py --runs 50 --json
```

Competition materials are in `docs/`, including paste-ready form answers, a
two-minute pitch, a 90-second demo script, a five-student validation sheet, and
an editable 16:9 SVG submission cover.

## Snapdragon implementation path

The production design uses:

1. **Whisper-Base** through Qualcomm's Whisper Windows reference application
   and the ONNX Runtime QNN execution provider for multilingual speech-to-text.
2. **Llama 3.2 3B Instruct**, quantized for on-device deployment, for structured
   notes, quizzes, and answer generation.
3. A local evidence layer that stores source sentence IDs and refuses to answer
   when the transcript does not support a response.

Official references:

- [Qualcomm AI Hub – Whisper Windows](https://aihub.qualcomm.com/apps/whisper_windows_py)
- [Qualcomm AI Hub – Whisper-Base](https://aihub.qualcomm.com/models/whisper_base)
- [Qualcomm AI Hub – Llama 3.2 3B Instruct](https://aihub.qualcomm.com/compute/models/llama_v3_2_3b_instruct)
- [Qualcomm AI Hub model catalogue](https://aihub.qualcomm.com/models)

See [`docs/SNAPDRAGON_DEPLOYMENT.md`](docs/SNAPDRAGON_DEPLOYMENT.md) for the
integration and validation checklist.

## Submission honesty checklist

- Do not claim measured NPU speed, battery savings, or Malayalam accuracy until
  those numbers are collected on the target laptop.
- Do not upload a team-owned project as a solely owned individual entry.
- Replace sample metrics with results from at least five real lecture clips.
- Review the competition's official rules immediately before submission.

## Author

Mohammed Shahal — B.Tech CSE (AI & ML), MEA Engineering College, Kerala.

## License

MIT. Model weights and third-party runtimes retain their own licences.
