"""
User Role Recommendations Engine.

Production-grade modular role mining and least-privilege entitlement
recommendations for enterprise identity governance.
"""

from .config import (
    DEFAULT_DATA_FILENAME,
    DEFAULT_DEPARTMENTS,
    DEFAULT_ENTITLEMENTS,
    DEFAULT_RANDOM_SEED,
    get_default_data_path,
)
from .data import (
    generate_synthetic_dataset,
    load_dataset,
    save_dataset,
    validate_user_record,
)
from .models import (
    IdentityVectorizer,
    compute_pairwise_similarity,
)
from .recommender import (
    discover_role_archetypes,
    format_archetype_table,
    recommend_departmental_entitlements,
)
from .evaluation import (
    evaluate_role_mining,
)

__version__ = "1.0.0"

__all__ = [
    "DEFAULT_DATA_FILENAME",
    "DEFAULT_DEPARTMENTS",
    "DEFAULT_ENTITLEMENTS",
    "DEFAULT_RANDOM_SEED",
    "get_default_data_path",
    "load_dataset",
    "generate_synthetic_dataset",
    "save_dataset",
    "validate_user_record",
    "IdentityVectorizer",
    "compute_pairwise_similarity",
    "discover_role_archetypes",
    "format_archetype_table",
    "recommend_departmental_entitlements",
    "evaluate_role_mining",
]
