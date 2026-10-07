"""
Evaluation and diagnostic metrics for role mining and entitlement recommendations.
"""

from typing import Any, Dict, List, Optional, Set, Tuple


def evaluate_role_mining(
    users: List[Dict[str, Any]],
    archetypes: List[Tuple[str, List[str], int]],
    departmental_recs: Dict[str, List[Tuple[str, float]]],
) -> Dict[str, Any]:
    """
    Computes empirical structural metrics for unsupervised role mining.

    Note: Supervised precision/recall require verified ground-truth role labels.
    """
    total_identities = len(users)
    total_archetypes = len(archetypes)
    departments: Set[str] = {u.get("department", "Unknown") for u in users}
    unique_entitlements: Set[str] = set()
    for u in users:
        unique_entitlements.update(u.get("entitlements", []))

    reduction_ratio = (
        (1.0 - (total_archetypes / total_identities)) * 100.0
        if total_identities > 0
        else 0.0
    )

    avg_archetype_size = (
        (total_identities / total_archetypes) if total_archetypes > 0 else 0.0
    )

    return {
        "dataset_type": "SYNTHETIC_SAMPLE_DATA",
        "total_identities": total_identities,
        "total_departments": len(departments),
        "total_unique_entitlements": len(unique_entitlements),
        "discovered_role_archetypes": total_archetypes,
        "average_identities_per_archetype": round(avg_archetype_size, 2),
        "role_reduction_percentage": round(reduction_ratio, 2),
        "department_coverage_percentage": 100.0 if departmental_recs else 0.0,
        "ground_truth_status": "Ground-truth role labels are currently unavailable for supervised evaluation.",
        "supervised_evaluation": None,
    }


def evaluate_supervised_recommendations(
    predicted_entitlements: Dict[str, List[str]],
    ground_truth_entitlements: Dict[str, List[str]],
) -> Dict[str, float]:
    """
    Evaluation framework for evaluating recommendation precision, recall,
    and F1 when ground-truth labeled roles become available.
    """
    all_precisions = []
    all_recalls = []

    for dept, preds in predicted_entitlements.items():
        truth = set(ground_truth_entitlements.get(dept, []))
        if not truth:
            continue
        pred_set = set(preds)
        true_positives = len(pred_set.intersection(truth))
        precision = true_positives / len(pred_set) if pred_set else 0.0
        recall = true_positives / len(truth) if truth else 0.0
        all_precisions.append(precision)
        all_recalls.append(recall)

    mean_precision = sum(all_precisions) / len(all_precisions) if all_precisions else 0.0
    mean_recall = sum(all_recalls) / len(all_recalls) if all_recalls else 0.0
    f1 = (
        (2 * mean_precision * mean_recall) / (mean_precision + mean_recall)
        if (mean_precision + mean_recall) > 0
        else 0.0
    )

    return {
        "precision": round(mean_precision, 4),
        "recall": round(mean_recall, 4),
        "f1_score": round(f1, 4),
    }
