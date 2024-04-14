import os
import sys
import torch
from ..utils import utils


OS = os.name
PLATFORM = sys.platform
SEED = utils.get_formatted_environ_variable("SEED", int, 42)
TUNING = utils.get_formatted_environ_variable("TUNING", bool, False)

DEVICE_TYPE = "cpu"
if OS == "posix":
    if torch.cuda.is_available():
        DEVICE_TYPE = "cuda"
    elif torch.backends.mps.is_available():
        DEVICE_TYPE = "mps"

DEVICE = torch.device(DEVICE_TYPE)
DEVICE_COUNT = torch.cuda.device_count() if DEVICE_TYPE == "cuda" else 1

GPU_AVAILABLE = DEVICE_TYPE in ["cuda", "mps"]

try:
    import pyg_lib  # noqa

    WITH_PYG_LIB = True
except Exception:
    WITH_PYG_LIB = False

try:
    import torch_cluster  # noqa

    WITH_TORCH_CLUSTER = True
except Exception:
    WITH_TORCH_CLUSTER = False


def get_formatted_os():
    if PLATFORM == "linux":
        return "Linux"
    if PLATFORM == "darwin":
        return "MacOS"
    assert False, f"Unsupported platform: {PLATFORM}"
    return None


variables = dir()


def print_variables():
    for var in variables:
        if var.isupper():
            print(f"{var}: {eval(var)}")


if __name__ == "__main__":
    # probably should be moved to logger module
    print_variables()
