"""
Data ingestion, validation, and synthetic generation module.
"""

import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import faker

from .config import (
    DEFAULT_DEPARTMENTS,
    DEFAULT_ENTITLEMENTS,
    DEFAULT_RANDOM_SEED,
    get_default_data_path,
)


def validate_user_record(user: Dict[str, Any], index: int = 0) -> Dict[str, Any]:
    """
    Validates and normalizes an individual identity record.
    """
    if not isinstance(user, dict):
        raise ValueError(f"User record at index {index} must be a dictionary.")

    user_id = user.get("id", index + 1)
    username = user.get("username", f"user_{user_id}")
    email = user.get("email", f"{username}@example.com")
    department = user.get("department", "Unknown")
    entitlements = user.get("entitlements", [])

    if not isinstance(entitlements, list):
        raise ValueError(
            f"User '{username}' (ID: {user_id}) entitlements must be a list of strings."
        )

    # Clean and stringify entitlement identifiers
    normalized_entitlements = [str(e).strip() for e in entitlements if e]

    return {
        "id": user_id,
        "username": str(username),
        "email": str(email),
        "created_at": user.get("created_at", "1970-01-01T00:00:00"),
        "department": str(department).strip(),
        "entitlements": normalized_entitlements,
    }


def load_dataset(filepath: Optional[Union[str, Path]] = None) -> List[Dict[str, Any]]:
    """
    Loads identity entitlement records from a JSON file.
    """
    path = Path(filepath) if filepath else get_default_data_path()
    if not path.exists():
        raise FileNotFoundError(
            f"Entitlements dataset not found at '{path}'. "
            "Please generate sample data or specify a valid file path."
        )

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict) or "users" not in data:
        raise ValueError("Invalid dataset structure: JSON must contain a root 'users' key.")

    raw_users = data["users"]
    if not isinstance(raw_users, list):
        raise ValueError("Invalid dataset structure: 'users' must be a list.")

    return [validate_user_record(user, idx) for idx, user in enumerate(raw_users)]


def generate_synthetic_dataset(
    num_users: int = 1999,
    departments: Optional[List[str]] = None,
    entitlements: Optional[List[str]] = None,
    seed: Optional[int] = DEFAULT_RANDOM_SEED,
) -> Dict[str, Any]:
    """
    Generates reproducible synthetic enterprise identity records using Faker.
    """
    dept_list = departments if departments is not None else DEFAULT_DEPARTMENTS
    ent_list = entitlements if entitlements is not None else DEFAULT_ENTITLEMENTS

    if seed is not None:
        random.seed(seed)
        fake = faker.Faker()
        faker.Faker.seed(seed)
    else:
        fake = faker.Faker()

    users = []
    for user_id in range(1, num_users + 1):
        num_sample = random.randint(1, len(ent_list))
        user_entitlements = random.sample(ent_list, num_sample)
        user = {
            "id": user_id,
            "username": fake.user_name(),
            "email": fake.email(),
            "created_at": fake.date_time_this_decade().isoformat(),
            "entitlements": user_entitlements,
            "department": random.choice(dept_list),
        }
        users.append(user)

    return {"users": users}


def save_dataset(data: Dict[str, Any], filepath: Union[str, Path]) -> None:
    """
    Atomically writes dataset dictionary to a JSON file.
    """
    target_path = Path(filepath)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
