#!/usr/bin/env python3
"""Repeatable latency check for the portable reference engine."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from engine.lecture_engine import LectureEngine


DEFAULT_TRANSCRIPT = (
    "Machine learning systems learn patterns from examples rather than receiving every rule explicitly. "
    "Supervised learning uses input features and known labels to learn a predictive relationship. "
    "Training data teaches the model, validation data supports model selection, and testing data measures final performance. "
    "Testing data must remain separate because repeated access can leak information into development decisions. "
    "Classification predicts categories and regression predicts continuous values. "
    "Overfitting occurs when a model memorises training noise and fails to generalise to unseen examples. "
    "Representative data, regularisation, and careful validation can reduce overfitting. "
    "Evaluation metrics must match the real cost of errors because accuracy can be misleading on imbalanced data."
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=50)
    parser.add_argument("--transcript", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    transcript = args.transcript.read_text(encoding="utf-8") if args.transcript else DEFAULT_TRANSCRIPT
    engine = LectureEngine()
    timings = []
    for _ in range(max(1, args.runs)):
        start = time.perf_counter()
        engine.analyze(transcript, "Benchmark", "Machine Learning")
        timings.append((time.perf_counter() - start) * 1000)
    report = {
        "engine": engine.version,
        "runs": len(timings),
        "median_ms": round(statistics.median(timings), 3),
        "min_ms": round(min(timings), 3),
        "max_ms": round(max(timings), 3),
        "characters": len(transcript),
        "note": "Reference-engine latency only; this is not an NPU or speech-model benchmark.",
    }
    print(json.dumps(report, indent=2) if args.json else "\n".join(f"{k}: {v}" for k, v in report.items()))


if __name__ == "__main__":
    main()
