from __future__ import annotations
import os


from graph_ml.utils import config

OS = os.name


def test_target_os():
    assert OS == "posix"


def test_target_platform():
    assert config.PLATFORM in ["linux", "darwin"]


def test_device_type():
    assert config.DEVICE_TYPE in ["cpu", "cuda", "mps"]


def test_gpu_available():
    if config.DEVICE_TYPE == "cuda":
        assert config.GPU_AVAILABLE
    elif config.DEVICE_TYPE == "mps":
        assert config.GPU_AVAILABLE
    elif config.DEVICE_TYPE == "cpu":
        assert not config.GPU_AVAILABLE
    else:
        assert False


def test_device_count():
    assert config.DEVICE_COUNT >= 1
