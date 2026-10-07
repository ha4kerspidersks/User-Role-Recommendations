"""
Command-line interface for the role recommendation engine.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .config import DEFAULT_DATA_FILENAME, DEFAULT_RANDOM_SEED, DEFAULT_TOP_K, get_default_data_path
from .data import generate_synthetic_dataset, load_dataset, save_dataset
from .evaluation import evaluate_role_mining
from .models import IdentityVectorizer, compute_pairwise_similarity
from .recommender import (
    discover_role_archetypes,
    format_archetype_table,
    recommend_departmental_entitlements,
)


def build_parser() -> argparse.ArgumentParser:
    """
    Constructs the CLI argument parser.
    """
    parser = argparse.ArgumentParser(
        prog="role-recommendation",
        description="Enterprise IAM Least-Privilege Role Mining & Recommendation Engine",
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default=None,
        help=f"Path to user entitlements JSON file (default: {DEFAULT_DATA_FILENAME})",
    )
    parser.add_argument(
        "--top-k",
        "-k",
        type=int,
        default=DEFAULT_TOP_K,
        help=f"Number of top departmental entitlements to recommend (default: {DEFAULT_TOP_K})",
    )
    parser.add_argument(
        "--generate-synthetic",
        action="store_true",
        help="Generate a reproducible synthetic entitlements dataset and save to file",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Target output path when generating synthetic data",
    )
    parser.add_argument(
        "--num-users",
        type=int,
        default=1999,
        help="Number of users to generate when --generate-synthetic is specified (default: 1999)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_RANDOM_SEED,
        help=f"Random seed for reproducibility (default: {DEFAULT_RANDOM_SEED})",
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Compute and display evaluation metrics for role discovery",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output presentation format (default: text)",
    )
    return parser


def run_pipeline(
    input_path: Optional[str] = None,
    top_k: int = DEFAULT_TOP_K,
    evaluate: bool = False,
    output_format: str = "text",
) -> int:
    """
    Executes the role recommendation analysis pipeline.
    """
    try:
        data_path = Path(input_path) if input_path else get_default_data_path()
        users = load_dataset(data_path)
    except Exception as exc:
        print(f"Error loading dataset: {exc}", file=sys.stderr)
        return 1

    # 1. Feature extraction and vector space model
    vectorizer = IdentityVectorizer()
    tfidf_matrix = vectorizer.fit_transform(users)
    cosine_sim = compute_pairwise_similarity(tfidf_matrix)

    # 2. Discover role archetypes
    archetypes = discover_role_archetypes(users)

    # 3. Departmental entitlement confidence scores
    department_recs = recommend_departmental_entitlements(users, top_k=top_k)

    # 4. Optional Evaluation
    metrics = evaluate_role_mining(users, archetypes, department_recs) if evaluate else None

    if output_format == "json":
        payload = {
            "metadata": {
                "input_file": str(data_path),
                "total_users": len(users),
                "feature_dimensions": tfidf_matrix.shape[1],
            },
            "archetypes": [
                {"department": d, "entitlements": e, "user_count": c}
                for d, e, c in archetypes
            ],
            "department_recommendations": {
                dept: [{"entitlement": ent, "confirmation_percentage": pct} for ent, pct in recs]
                for dept, recs in department_recs.items()
            },
        }
        if metrics:
            payload["evaluation"] = metrics
        print(json.dumps(payload, indent=2))
        return 0

    # Default text presentation (preserving original visual fidelity)
    print("User data loaded from", data_path)
    print(f"Constructed TF-IDF Vector Space with {tfidf_matrix.shape[0]} identities and {tfidf_matrix.shape[1]} features.")
    print("Recommended Roles for User:")
    print(format_archetype_table(archetypes))
    print()

    for department, recommendations in department_recs.items():
        print(f"Recommendations for Department '{department}':")
        for i, (entitlement, percentage) in enumerate(recommendations, start=1):
            print(f"{i}. {entitlement}: {percentage:.2f}% confirmation")
        print()

    if evaluate and metrics:
        print("============================================================")
        print("ROLE MINING EVALUATION METRICS")
        print("============================================================")
        for k, v in metrics.items():
            print(f"  {k}: {v}")
        print()

    return 0


def main(argv: Optional[list] = None) -> int:
    """
    Main CLI entry point.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.generate_synthetic:
        target_path = Path(args.output) if args.output else get_default_data_path()
        print(f"Generating synthetic dataset with {args.num_users} users (seed={args.seed})...")
        data = generate_synthetic_dataset(
            num_users=args.num_users,
            seed=args.seed,
        )
        save_dataset(data, target_path)
        print(f"Synthetic dataset saved to {target_path}")
        return 0

    return run_pipeline(
        input_path=args.input,
        top_k=args.top_k,
        evaluate=args.evaluate,
        output_format=args.format,
    )


if __name__ == "__main__":
    sys.exit(main())
