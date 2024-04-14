import os
from graph_ml.utils import config
import pytest


@pytest.fixture()
def os():
    return config.OS

@pytest.fixture()
def platform():
    return config.PLATFORM

@pytest.fixture()
def device_type():
    return config.DEVICE_TYPE

@pytest.fixture()
def device_count():
    return config.DEVICE_COUNT

def test_target_os(os):
    assert os == "posix"


def test_target_platform(platform):
    assert platform in ["linux", "darwin"]


def test_device_type(device_type):
    assert device_type in ["cpu", "cuda", "mps"]


def test_gpu_available(device_type):
    if device_type == "cuda":
        assert config.GPU_AVAILABLE
    elif device_type == "mps":
        assert config.GPU_AVAILABLE
    elif device_type == "cpu":
        assert not config.GPU_AVAILABLE
    else:
        assert False


def test_device_count():
    assert config.DEVICE_COUNT >= 1

def test_seed():
    assert config.SEED == 42

def test_tuning():
    assert not config.TUNING

def explicit_seed():
    os.environ["SEED"] = "123"
    assert config.SEED == 123

def explicit_tuning():
    os.environ["TUNING"] = "True"
    assert config.TUNING


