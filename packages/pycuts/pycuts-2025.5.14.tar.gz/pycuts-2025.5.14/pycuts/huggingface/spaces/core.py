# pycuts - A lightweight Python utility toolkit
# © 2025 Daniel Ialcin Misser Westergaard ([dwancin](https://github.com/dwancin))
# This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

import os
from huggingface_hub import space_info

class Spaces:
    """
    Utilities and environment info for Hugging Face Spaces.
    """

    @staticmethod
    def is_spaces() -> bool:
        """
        Returns:
            bool: `True` if running inside a Hugging Face Space.
        """
        return os.getenv("SYSTEM") == "spaces"


    @staticmethod
    def is_zero_gpu() -> bool:
        """
        Returns:
            bool: `True` if the current space supports dynamic GPU allocation.
        """
        return os.getenv("SPACES_ZERO_GPU") == "true"


    @staticmethod
    def is_canonical(repo_id: str) -> bool:
        """
        Args:
            repo_id (str): A namespace (user or an organization) and a repo name separated by a `/`.
        Returns:
            bool: `True` if the given `repo_id` matches with the current space.
        """
        return os.getenv("SPACE_ID") == repo_id


    @staticmethod
    def get_space_id() -> str:
        """
        Returns:
            str: `repo id` of the current space.
        """
        return os.getenv("SPACE_ID", "")


    @staticmethod
    def get_space_host() -> str:
        """
        Returns: 
            str: Host name of the current space.
        """
        return os.getenv("SPACE_HOST", "")


    @staticmethod
    def get_space_author() -> str:
        """
        Returns:
            str: A namespace (user or an organization) that owns the current Space.
        """
        return os.getenv("SPACE_AUTHOR_NAME", "")
