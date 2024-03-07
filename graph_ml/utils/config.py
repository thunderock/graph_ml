import os, sys
import torch


OS = os.name
DEVICE_TYPE = 'cpu'
if OS == 'posix':
    if torch.cuda.is_available():
        DEVICE_TYPE = 'cuda'
    elif torch.backends.mps.is_available():
        DEVICE_TYPE = 'mps'

DEVICE = torch.device(DEVICE_TYPE)

GPU_AVAILABLE = DEVICE_TYPE in ['cuda', 'mps']

