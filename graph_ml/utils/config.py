import os
import sys
import torch


OS = os.name
PLATFORM = sys.platform

DEVICE_TYPE = "cpu"
if OS == "posix":
    if torch.cuda.is_available():
        DEVICE_TYPE = "cuda"
    elif torch.backends.mps.is_available():
        DEVICE_TYPE = "mps"

DEVICE = torch.device(DEVICE_TYPE)
DEVICE_COUNT = torch.cuda.device_count() if DEVICE_TYPE == "cuda" else 1

GPU_AVAILABLE = DEVICE_TYPE in ["cuda", "mps"]


def get_formatted_os():
    if PLATFORM == "linux":
        return "Linux"
    if PLATFORM == "darwin":
        return "MacOS"
    assert False, f"Unsupported platform: {PLATFORM}"
