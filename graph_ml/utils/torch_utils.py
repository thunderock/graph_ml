import numpy as np
import torch


# TODO (ashutosh): move these assert statements once we have a stable code
def convert_to_tensor(data):
    if isinstance(data, np.ndarray):
        return torch.from_numpy(data)
    assert isinstance(data, torch.Tensor)
    return data


def convert_to_numpy(data):
    if isinstance(data, torch.Tensor):
        return data.cpu().numpy()
    assert isinstance(data, np.ndarray)
    return data


def move_to_device(data, device):
    if isinstance(data, np.ndarray):
        return convert_to_tensor(data).to(device)
    assert isinstance(data, torch.Tensor)
    return data.to(device)