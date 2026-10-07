"""
Configuration module for role recommendation engine.
"""

from pathlib import Path
from typing import List

# Standard departmental taxonomy
DEFAULT_DEPARTMENTS: List[str] = [
    "Engineering",
    "Marketing",
    "Sales",
    "Finance",
    "HR",
    "IT",
]

# Standard entitlement catalog
DEFAULT_ENTITLEMENTS: List[str] = [
    "E1",
    "E2",
    "E3",
    "E4",
    "E5",
    "E6",
    "E7",
    "E8",
    "E9",
    "E10",
]

DEFAULT_DATA_FILENAME: str = "user_entitlements_data.json"
DEFAULT_RANDOM_SEED: int = 42
DEFAULT_TOP_K: int = 5


def get_project_root() -> Path:
    """
    Returns the repository root directory resolved portably.
    """
    # src/role_recommendation/config.py -> parents[2] is repository root
    return Path(__file__).resolve().parents[2]


def get_default_data_path() -> Path:
    """
    Returns the absolute path to the default user entitlements JSON file.
    """
    return get_project_root() / DEFAULT_DATA_FILENAME
