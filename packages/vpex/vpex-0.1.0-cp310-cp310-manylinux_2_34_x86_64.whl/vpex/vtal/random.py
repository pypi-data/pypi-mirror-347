from typing import Iterable, List, Union
import torch

import vpex
from . import _lazy_init, _lazy_call, _get_device, device_count, current_device


def get_rng_state(
        device: Union[int, str, torch.device] = "vsi") -> torch.Tensor:
    r"""Returns the random number generator state of the specified VSI as a ByteTensor.

    Args:
        device (torch.device or int, optional): The device to return the RNG state of.
            Default: ``"vsi"`` (i.e., ``torch.device("vsi")``, the current VSI device).

    .. warning::
        This function eagerly initializes VSI.
    """
    _lazy_init()
    device = _get_device(device)
    device_index = device.index
    if device_index is None:
        device_index = current_device()
    default_generator = vpex.vtal.default_generators[device_index]
    return default_generator.get_state()


def get_rng_state_all() -> List[torch.Tensor]:
    r"""Returns a list of ByteTensor representing the random number states of all devices."""
    results = [get_rng_state(i) for i in range(device_count())]
    return results


def set_rng_state(new_state: torch.Tensor,
                  device: Union[int, str, torch.device] = "vsi") -> None:
    r"""Sets the random number generator state of the specified VSI.

    Args:
        new_state (torch.ByteTensor): The desired state
        device (torch.device or int, optional): The device to set the RNG state.
            Default: ``"vsi"`` (i.e., ``torch.device("vsi")``, the current VSI device).
    """
    new_state_copy = new_state.clone(memory_format=torch.contiguous_format)
    device = _get_device(device)

    def cb():
        device_index = device.index
        if device_index is None:
            device_index = current_device()
        default_generator = vpex.vtal.default_generators[device_index]
        default_generator.set_state(new_state_copy)

    _lazy_call(cb)


def set_rng_state_all(new_states: Iterable[torch.Tensor]) -> None:
    r"""Sets the random number generator state of all devices.

    Args:
        new_states (Iterable of torch.ByteTensor): The desired state for each device
    """
    for i, state in enumerate(new_states):
        set_rng_state(state, i)


def manual_seed(seed: int) -> None:
    r"""Sets the seed for generating random numbers for the current VSI.
    It's safe to call this function if VSI is not available; in that
    case, it is silently ignored.

    Args:
        seed (int): The desired seed.

    .. warning::
        If you are working with a multi-VSI model, this function is insufficient
        to get determinism.  To seed all VSI devices, use :func:`manual_seed_all`.
    """
    seed = int(seed)

    def cb():
        device_index = current_device()
        default_generator = vpex.vtal.default_generators[device_index]
        default_generator.manual_seed(seed)

    _lazy_call(cb)


def manual_seed_all(seed: int) -> None:
    r"""Sets the seed for generating random numbers on all VSI devices.
    It's safe to call this function if VSI is not available; in that
    case, it is silently ignored.

    Args:
        seed (int): The desired seed.
    """
    seed = int(seed)

    def cb():
        for i in range(device_count()):
            default_generator = vpex.vtal.default_generators[i]
            default_generator.manual_seed(seed)

    _lazy_call(cb)


def seed() -> None:
    r"""Sets the seed for generating random numbers to a random number for the current VSI.
    It's safe to call this function if VSI is not available; in that
    case, it is silently ignored.

    .. warning::
        If you are working with a multi-VSI model, this function will only initialize
        the seed on one VSI.  To initialize all VSI devicess, use :func:`seed_all`.
    """

    def cb():
        device_index = current_device()
        default_generator = vpex.vtal.default_generators[device_index]
        default_generator.seed()

    _lazy_call(cb)


def seed_all() -> None:
    r"""Sets the seed for generating random numbers to a random number on all VSI devices.
    It's safe to call this function if VSI is not available; in that
    case, it is silently ignored.
    """

    def cb():
        random_seed = 0
        seeded = False
        for i in range(device_count()):
            default_generator = vpex.vtal.default_generators[i]
            if not seeded:
                default_generator.seed()
                random_seed = default_generator.initial_seed()
                seeded = True
            else:
                default_generator.manual_seed(random_seed)

    _lazy_call(cb)


def initial_seed() -> int:
    r"""Returns the current random seed of the current VSI.

    .. warning::
        This function eagerly initializes VSI.
    """
    _lazy_init()
    device_index = current_device()
    default_generator = vpex.vtal.default_generators[device_index]
    return default_generator.initial_seed()
