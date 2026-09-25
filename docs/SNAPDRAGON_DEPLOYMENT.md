# Snapdragon Deployment and Validation Plan

This document separates implemented work from hardware-dependent work.

## Target pipeline

### Speech recognition

- Model: Qualcomm AI Hub **Whisper-Base**
- OS: Windows 11+
- Runtime: ONNX Runtime
- Acceleration: QNN Execution Provider on Snapdragon NPU
- Reference: <https://aihub.qualcomm.com/apps/whisper_windows_py>

Qualcomm's published sample specifically demonstrates on-device speech-to-text
with this runtime path. Use its current instructions rather than copying stale
installation commands into the submission.

### Learning-material generation

- Model: Qualcomm AI Hub **Llama-v3.2-3B-Instruct**
- Quantisation: w4a16 with selected w8a16 layers, as described by the model card
- Role: summary, quiz candidates, and simplified explanations
- Reference: <https://aihub.qualcomm.com/compute/models/llama_v3_2_3b_instruct>

Keep the existing evidence layer after adding the LLM. Generation must not bypass
source validation.

## Adapter contract

The model adapter should produce the same keys as the reference engine:

```json
{
  "summary": [{"text": "...", "source": 3, "relevance": 0.91}],
  "concepts": [{"term": "...", "mentions": 4, "first_source": 2}],
  "quiz": [{"question": "...", "options": ["..."], "answer": "...", "source": 6}]
}
```

This lets the UI remain unchanged while the reference engine is replaced.

## Device checklist

1. Confirm Windows reports a Qualcomm Snapdragon processor.
2. Update Windows and the OEM NPU drivers.
3. Follow the current Qualcomm Whisper Windows sample instructions.
4. Confirm ONNX Runtime lists `QNNExecutionProvider`.
5. Run the sample audio and save the console output.
6. Connect the transcript string to the LectureLens local endpoint.
7. Add the LLM only after speech recognition is stable.

## Metrics to collect

Use a fixed 5-minute clip for every run and repeat each test three times.

| Metric | How to report |
|---|---|
| Real-time factor | processing seconds / audio seconds; lower is better |
| First transcript latency | seconds until first visible segment |
| Peak working set | MB from Task Manager or profiler |
| Battery change | percentage points during a controlled 30-minute run |
| Word error rate | substitutions + deletions + insertions divided by reference words |
| Grounding rate | supported output statements / all output statements |

Record the laptop model, processor, RAM, Windows build, model version, runtime
version, and power mode beside every result.

## Claims that require evidence

Do not use “real-time,” “NPU-accelerated,” “battery efficient,” or an accuracy
percentage in the final submission until the corresponding test is recorded.
The current portable engine should be described as a functional reference MVP.
