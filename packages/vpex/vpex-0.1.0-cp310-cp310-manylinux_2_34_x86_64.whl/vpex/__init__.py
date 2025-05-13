import torch
torch.utils.rename_privateuse1_backend("vsi")

import vpex.vtal
torch._register_device_module("vsi", vpex.vtal)
