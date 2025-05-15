# pycuts - A lightweight Python utility toolkit
# © 2025 Daniel Ialcin Misser Westergaard ([dwancin](https://github.com/dwancin))
# This project is licensed under the MIT License.

import torch
from typing import Optional, Union
from warnings import warn

class Torch:
    """
    Utility class providing static methods for simplified interaction with PyTorch devices.
    Supports CUDA, Metal (MPS), and CPU environments.
    """

    @staticmethod
    def device() -> str:
        """
        Detects and returns the best available PyTorch device as a string.
        """
        return (
            "cuda" if torch.cuda.is_available()
            else "mps" if torch.backends.mps.is_available()
            else "cpu"
        )

    @staticmethod
    def _resolve_device(device: Optional[Union[str, torch.device]]) -> torch.device:
        """
        Internal helper to normalize device input.
        """
        return torch.device(device) if device else torch.device(Torch.device())

    @staticmethod
    def is_gpu(device: Optional[Union[str, torch.device]] = None) -> bool:
        """
        Checks if the given or current device is a GPU (CUDA or MPS).
        """
        resolved = Torch._resolve_device(device)
        if resolved.type in ("cuda", "mps"):
            return True
        if resolved.type == "cpu":
            return False

        warn(f"`is_gpu` only supports 'cuda', 'mps', and 'cpu'. Received unsupported device type '{resolved}'.")
        return False

    @staticmethod
    def empty_cache(device: Optional[Union[str, torch.device]] = None) -> None:
        """
        Clears the unused GPU memory cache for the given or current device.
        """
        resolved = Torch._resolve_device(device)

        if resolved.type == "cuda":
            with torch.cuda.device(resolved):
                torch.cuda.empty_cache()
        elif resolved.type == "mps":
            try:
                torch.mps.empty_cache()
            except AttributeError:
                warn("`torch.mps.empty_cache()` not available in this PyTorch version.")
        else:
            warn(f"Cache clearing is only supported for 'cuda' and 'mps' devices. Received '{resolved}', no cache was cleared.")

    @staticmethod
    def recommended_max_memory(device: Optional[Union[str, torch.device]] = None) -> Optional[int]:
        """
        Returns a recommended maximum working memory size in bytes for the given or current device.
        Intended for limiting memory usage during large operations or model inference.
        """
        resolved = Torch._resolve_device(device)

        if resolved.type == "cuda":
            with torch.cuda.device(resolved):
                _, total = torch.cuda.mem_get_info()
                return int(total * 0.9)
        elif resolved.type == "mps":
            try:
                return torch.mps.recommended_max_memory()
            except AttributeError:
                warn("`torch.mps.recommended_max_memory()` not available in this PyTorch version.")
                return None

        warn(f"`recommended_max_memory` only supports 'cuda' and 'mps' devices. Received '{resolved}', returning None.")
        return None