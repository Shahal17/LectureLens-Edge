"""Runtime capability detection without external dependencies."""

from __future__ import annotations

import os
import platform
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RuntimeProfile:
    os: str
    architecture: str
    provider: str
    qnn_available: bool
    snapdragon_candidate: bool
    external_calls: int = 0
    data_retention: str = "Session memory only"

    def to_dict(self) -> dict:
        return asdict(self)


def detect_runtime() -> RuntimeProfile:
    system = platform.system() or "Unknown"
    architecture = platform.machine() or "Unknown"
    qnn_available = False

    try:
        import onnxruntime as ort  # type: ignore

        qnn_available = "QNNExecutionProvider" in ort.get_available_providers()
    except (ImportError, OSError):
        pass

    forced_provider = os.getenv("LECTURELENS_PROVIDER", "").strip()
    if forced_provider:
        provider = forced_provider
    elif qnn_available:
        provider = "QNNExecutionProvider"
    else:
        provider = "Portable reference engine"

    arm_markers = {"arm64", "aarch64", "armv8l"}
    snapdragon_candidate = system == "Windows" and architecture.lower() in arm_markers

    return RuntimeProfile(
        os=system,
        architecture=architecture,
        provider=provider,
        qnn_available=qnn_available,
        snapdragon_candidate=snapdragon_candidate,
    )
