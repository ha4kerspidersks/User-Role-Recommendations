"""
Unit tests for role archetype discovery and departmental recommendations.
"""

import unittest

from role_recommendation.recommender import (
    discover_role_archetypes,
    format_archetype_table,
    recommend_departmental_entitlements,
)


class TestRecommenderModule(unittest.TestCase):
    def setUp(self):
        self.users = [
            {"id": 1, "department": "IT", "entitlements": ["E1", "E2"]},
            {"id": 2, "department": "IT", "entitlements": ["E2", "E1"]},  # Unsorted duplicate
            {"id": 3, "department": "IT", "entitlements": ["E1"]},
            {"id": 4, "department": "HR", "entitlements": ["E5"]},
        ]

    def test_discover_role_archetypes_clusters_duplicates(self):
        archetypes = discover_role_archetypes(self.users)
        # Should cluster users 1 and 2 together: (IT, ['E1', 'E2'], count=2)
        it_clusters = [a for a in archetypes if a[0] == "IT"]
        self.assertEqual(len(it_clusters), 2)
        top_cluster = it_clusters[0]
        self.assertEqual(top_cluster[0], "IT")
        self.assertEqual(top_cluster[1], ["E1", "E2"])
        self.assertEqual(top_cluster[2], 2)

    def test_discover_role_archetypes_department_filter(self):
        archetypes = discover_role_archetypes(self.users, departments=["HR"])
        self.assertEqual(len(archetypes), 1)
        self.assertEqual(archetypes[0][0], "HR")

    def test_recommend_departmental_entitlements(self):
        recs = recommend_departmental_entitlements(self.users, top_k=2)
        self.assertIn("IT", recs)
        self.assertIn("HR", recs)

        # In IT (3 users total): E1 appears 3 times (100%), E2 appears 2 times (66.67%)
        it_recs = recs["IT"]
        self.assertEqual(it_recs[0][0], "E1")
        self.assertEqual(it_recs[0][1], 100.0)
        self.assertEqual(it_recs[1][0], "E2")
        self.assertAlmostEqual(it_recs[1][1], 66.67, places=2)

    def test_format_archetype_table(self):
        archetypes = [("IT", ["E1", "E2"], 5)]
        table = format_archetype_table(archetypes)
        self.assertIn("Department", table)
        self.assertIn("Entitlements", table)
        self.assertIn("Count", table)
        self.assertIn("IT", table)


if __name__ == "__main__":
    unittest.main()
