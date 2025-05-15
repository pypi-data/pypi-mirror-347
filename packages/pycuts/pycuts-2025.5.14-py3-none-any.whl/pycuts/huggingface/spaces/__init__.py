# pycuts - A lightweight Python utility toolkit
# © 2025 Daniel Ialcin Misser Westergaard ([dwancin](https://github.com/dwancin))
# This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

from .core import Spaces
from ...packages.spaces import is_spaces_available, get_spaces_version

is_spaces = Spaces.is_spaces
is_zero_gpu = Spaces.is_zero_gpu
is_canonical = Spaces.is_canonical
get_space_id = Spaces.get_space_id
get_space_host = Spaces.get_space_host
get_space_author = Spaces.get_space_author

__all__ = [
    "Spaces",
    "is_spaces_available",
    "get_spaces_version",
    "is_spaces",
    "is_zero_gpu",
    "is_canonical",
    "get_space_id",
    "get_space_host",
    "get_space_autor"
]
