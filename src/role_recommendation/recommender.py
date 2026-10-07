"""
Role mining and least-privilege recommendation engine.
"""

from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Tuple

from tabulate import tabulate


def discover_role_archetypes(
    users: List[Dict[str, Any]],
    departments: Optional[List[str]] = None,
) -> List[Tuple[str, List[str], int]]:
    """
    Identifies natural role archetypes by aggregating identical departmental
    entitlement clusters and counting user membership.

    Returns a list of tuples: (department, list_of_entitlements, user_count).
    """
    user_count_by_department_entitlements = defaultdict(int)
    unique_recommendations = set()

    for user in users:
        department = user.get("department", "Unknown")
        if departments and department not in departments:
            continue
        entitlements = tuple(sorted(user.get("entitlements", [])))
        unique_key = (department, entitlements)

        user_count_by_department_entitlements[unique_key] += 1
        if user_count_by_department_entitlements[unique_key] == 1:
            unique_recommendations.add(unique_key)

    department_recommendations = defaultdict(list)
    for unique_key in unique_recommendations:
        department, entitlements = unique_key
        count = user_count_by_department_entitlements[unique_key]
        department_recommendations[department].append(
            (department, list(entitlements), count)
        )

    # Sort archetypes by department name, then descending by user count
    sorted_recommendations: List[Tuple[str, List[str], int]] = []
    for dept in sorted(department_recommendations.keys()):
        dept_archetypes = sorted(
            department_recommendations[dept],
            key=lambda x: x[2],
            reverse=True,
        )
        sorted_recommendations.extend(dept_archetypes)

    return sorted_recommendations


def format_archetype_table(
    archetypes: List[Tuple[str, List[str], int]],
    tablefmt: str = "pretty",
) -> str:
    """
    Renders discovered role archetypes into a readable ASCII/Unicode table.
    """
    return tabulate(
        archetypes,
        headers=["Department", "Entitlements", "Count"],
        tablefmt=tablefmt,
    )


def recommend_departmental_entitlements(
    users: List[Dict[str, Any]],
    top_k: int = 5,
) -> Dict[str, List[Tuple[str, float]]]:
    """
    Calculates empirical baseline entitlements for each department along
    with confidence / confirmation percentages.

    Returns dict mapping department name to list of (entitlement, confirmation_percentage).
    """
    department_users = defaultdict(list)
    for user in users:
        department = user.get("department", "Unknown")
        department_users[department].append(user)

    department_recommendations: Dict[str, List[Tuple[str, float]]] = {}
    for department in sorted(department_users.keys()):
        users_in_dept = department_users[department]
        total_users = len(users_in_dept)

        all_entitlements = []
        for u in users_in_dept:
            all_entitlements.extend(u.get("entitlements", []))

        entitlement_counts = Counter(all_entitlements)
        recs: List[Tuple[str, float]] = []

        if total_users > 0:
            for ent, count in entitlement_counts.most_common(top_k):
                percentage = (count / total_users) * 100.0
                recs.append((ent, round(percentage, 2)))

        department_recommendations[department] = recs

    return department_recommendations
