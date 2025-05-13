"""
This package introduces support for the VSI backend.

This package is lazily initialized, so you can always import it,
and use `is_available()` to determine if your system supports VSI device.
"""

import threading
import traceback
from functools import lru_cache
from typing import Any, Optional, Tuple, Union, List, Dict, Callable

import torch
from torch import device as _device
from torch._utils import _get_device_index, _LazySeedTracker

import vpex._C
from .streams import Stream, Event

_initialized = False
_tls = threading.local()
_initialization_lock = threading.Lock()
_queued_calls: List[Tuple[Callable[[], None], List[str]]] = []
_device_t = Union[_device, str, int, None]
_lazy_seed_tracker = _LazySeedTracker()

# fmt: off
_is_in_bad_fork: Callable[[], bool] = getattr(vpex._C, "_is_in_bad_fork", lambda: False)
_get_raw_context: Callable[[], int] = getattr(vpex._C, "_get_raw_context")
_get_raw_device: Callable[[int], int] = getattr(vpex._C, "_get_raw_device")
_get_current_raw_stream: Callable[[int], int] = getattr(vpex._C, "_get_current_raw_stream")
# fmt:on

default_generators: Tuple[torch._C.Generator] = ()  # type: ignore[assignment]

_VSIDeviceProperties = vpex._C._VSIDeviceProperties


def is_initialized() -> bool:
    return _initialized and not _is_in_bad_fork()


def _lazy_call(cb: Callable, **kwargs) -> Any:
    if is_initialized():
        cb()
    else:
        global _lazy_seed_tracker
        if kwargs.get("seed_all", False):
            _lazy_seed_tracker.queue_seed_all(cb, traceback.format_stack())
        elif kwargs.get("seed", False):
            _lazy_seed_tracker.queue_seed(cb, traceback.format_stack())
        else:
            # Don't store the actual traceback to avoid memory cycle
            _queued_calls.append((cb, traceback.format_stack()))


def init():
    r"""Initialize PyTorch's VSI state.
    Lazily initialize VSI backend until the first time it is used.
    Does nothing if the VSI state is already initialized.
    """
    _lazy_init()


def _lazy_init():
    global _initialized, _queued_calls
    if is_initialized() or hasattr(_tls, "is_initializing"):
        return
    with _initialization_lock:
        # This test was protected via GIL. Double-check whether VSI has already been initialized.
        if is_initialized():
            return
        # Stop promptly upon encountering a bad fork error.
        if _is_in_bad_fork():
            raise RuntimeError(
                "Cannot re-initialize VSI in forked subprocess. To use VSI with "
                "multiprocessing, you must use the 'spawn' start method")

        # This function inits VSI backend and detects bad fork processing.
        vpex._C._init()
        # Some of the queued calls may reentrantly call _lazy_init();
        # We need to just return without initializing in that case.
        _tls.is_initializing = True

        _queued_calls.extend(calls for calls in _lazy_seed_tracker.get_calls()
                             if calls)

        try:
            for queued_call, orig_traceback in _queued_calls:
                try:
                    queued_call()
                except Exception as e:
                    msg = (
                        f"VSI call failed lazily at initialization with error: {e}\n\n"
                        f"VSI call was originally invoked at:\n\n{''.join(orig_traceback)}"
                    )
                    raise Exception(msg) from e
        finally:
            delattr(_tls, "is_initializing")

        _initialized = True


class _DeviceGuard:

    def __init__(self, index: int):
        self.index = index
        self.prev_index = -1

    def __enter__(self):
        self.prev_index = vpex._C._exchange_device(self.index)

    def __exit__(self, type: Any, value: Any, traceback: Any):
        if self.prev_index != self.index:
            vpex._C._set_device(self.prev_index)
        return False


class device(object):
    r"""Context-manager that changes the selected device.

    Args:
        device (torch.device or int): device index to select. It's a no-op if
            this argument is a negative integer or ``None``.
    """

    def __init__(self, device: _device_t):
        self.index = _get_device_index(device, optional=True)
        self.prev_index = -1

    def __enter__(self):
        self.prev_index = vpex._C._exchange_device(self.index)

    def __exit__(self, type: Any, value: Any, traceback: Any):
        if self.prev_index != self.index:
            vpex._C._set_device(self.prev_index)
        return False


@lru_cache(maxsize=1)
def device_count() -> int:
    return vpex._C._get_device_count()


def is_available() -> bool:
    if not hasattr(vpex._C, "_set_device"):
        return False
    return device_count() > 0


def current_device() -> int:
    _lazy_init()
    return vpex._C._get_current_device()


def set_device(device: _device_t) -> None:
    _lazy_init()
    device_index = _get_device_index(device, optional=True)
    if device_index >= 0:
        vpex._C._set_device(device_index)


def get_device_properties(
        device: Optional[_device_t] = None) -> _VSIDeviceProperties:
    _lazy_init()
    device_index = _get_device_index(device, optional=True)
    return vpex._C._get_device_properties(device_index)


def get_device_name(device: Optional[_device_t] = None) -> str:
    return get_device_properties(device).name


def get_compute_capability(
        device: Optional[_device_t] = None) -> Dict[str, Any]:
    # TODO: impl.
    return {}


def _get_device(device: Union[int, str, torch.device]) -> torch.device:
    if isinstance(device, str):
        device = torch.device(device)
    elif isinstance(device, int):
        device = torch.device("vsi", index=device)
    return device


class StreamContext:
    current_stream: Optional["torch.vsi.Stream"]

    def __init__(self, stream: Optional["torch.vsi.Stream"]):
        self.stream = stream
        self.index = -1

    def __enter__(self):
        current_stream = self.stream
        if current_stream is None or self.index == -1:
            return
        self.src_prev_stream = vpex._C._get_current_stream(-1)

        # If the stream is not on the current device,
        # then set the current stream on the device.
        if self.src_prev_stream.device != current_stream.device:
            with device(current_stream.device):
                device_index = _get_device_index(current_stream.device)
                self.dst_prev_stream = vpex._C._get_current_stream(
                    device_index)
        vpex._C._set_stream(current_stream)

    def __exit__(self, type: Any, value: Any, traceback: Any):
        current_stream = self.stream
        if current_stream is None or self.index == -1:
            return

        # Reset the stream on the original device and destination device.
        if self.src_prev_stream.device != current_stream.device:
            vpex._C._set_stream(self.dst_prev_stream)
        vpex._C._set_stream(self.src_prev_stream)


def stream(stream: Optional["torch.vsi.Stream"]) -> StreamContext:
    return StreamContext(stream)


def set_stream(stream: Stream) -> None:
    r"""Sets the current stream.This is a wrapper API to set the stream.
        Usage of this function is discouraged in favor of the ``stream``
        context manager.
    Args:
        stream (Stream): selected stream. This function is a no-op
            if this argument is ``None``.
    """
    if stream is None:
        return

    _lazy_init()
    vpex._C._set_stream(stream_id=stream.stream_id,
                        device_index=stream.device_index,
                        device_type=stream.device_type)


def current_stream(device: Optional[_device_t] = None) -> Stream:
    r"""Returns the currently selected :class:`Stream` for a given device.

    Args:
        device (torch.device or int, optional): selected device. Returns
            the currently selected :class:`Stream` for the current device, given
            by :func:`~vpex.vtal.current_device`, if :attr:`device` is ``None``
            (default).
    """
    _lazy_init()
    device_index = _get_device_index(device, optional=True)
    stream_data = vpex._C._get_current_stream(device_index)
    return Stream(stream_id=stream_data[0],
                  device_index=stream_data[1],
                  device_type=stream_data[2])


def synchronize(device: Optional[_device_t] = None) -> None:
    r"""Waits for all kernels in all streams on a VSI device to complete.

    Arguments:
        device (torch.device or int, optional): device for which to synchronize.
            It uses the current device, given by :func:`~vpex.vtal.current_device`,
            if :attr:`device` is ``None`` (default).
    """
    _lazy_init()
    device_index = _get_device_index(device, optional=True)
    return vpex._C._synchronize(device_index)


def _get_generator(device: torch.device) -> torch._C.Generator:
    r"""Return the VSI Generator object for the given device.

    Args:
        device (torch.device): selected device.
    """

    index = device.index
    if index is None:
        index = current_device()
    return default_generators[index]


def _set_rng_state_offset(offset: int,
                          device: Union[int, str,
                                        torch.device] = "vsi") -> None:
    r"""Sets the random number generator state offset of the specified VSI.

    Args:
        offset (int): The desired offset
        device (torch.device or int, optional): The device to set the RNG state.
            Default: ``"vsi"`` (i.e., ``torch.device("vsi")``, the current VSI device).
    """
    final_device = _get_device(device)

    def cb():
        default_generator = _get_generator(final_device)
        default_generator.set_offset(offset)

    _lazy_call(cb)


def _get_rng_state_offset(
        device: Union[int, str, torch.device] = "vsi") -> int:
    r"""Returns the random number generator state offset of the specified VSI.

    Args:
        device (torch.device or int, optional): The device to return the RNG state offset of.
            Default: ``"vsi"`` (i.e., ``torch.device("vsi")``, the current VSI device).

    .. warning::
        This function eagerly initializes VSI.
    """
    _lazy_init()
    final_device = _get_device(device)
    default_generator = _get_generator(final_device)
    return default_generator.get_offset()


# Import here to avoid circular import.
from .random import (
    get_rng_state,
    get_rng_state_all,
    initial_seed,
    manual_seed,
    manual_seed_all,
    seed,
    seed_all,
    set_rng_state,
    set_rng_state_all,
)


# HACK for FlagGems.
_hijacked_op_names = [
    "diag",
    "where.ScalarSelf",
    "where.ScalarOther",
    "isclose",
    "repeat_interleave.self_Tensor",
    "pad",
    "hstack",
    "vstack"
]
_original_impl = torch.library.Library.impl

def _hijacked_impl(
    self,
    op_name: str,
    func: Callable,
    dispatch_key: str="",
    *,
    with_keyset=False
):
    if dispatch_key == "PrivateUse1" and op_name in _hijacked_op_names:
        def autograd_wrapper(*args, **kwargs):
            with torch.inference_mode():
                return func(*args, **kwargs)
        _original_impl(self, op_name, autograd_wrapper, "AutogradPrivateUse1")
    else:
        _original_impl(self, op_name, func, dispatch_key, with_keyset=with_keyset)

torch.library.Library.impl = _hijacked_impl
