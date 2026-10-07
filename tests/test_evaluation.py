"""
Unit tests for evaluation metrics.
"""

import unittest

from role_recommendation.evaluation import (
    evaluate_role_mining,
    evaluate_supervised_recommendations,
)


class TestEvaluationModule(unittest.TestCase):
    def test_evaluate_role_mining_structure(self):
        users = [
            {"id": 1, "department": "Sales", "entitlements": ["E1"]},
            {"id": 2, "department": "Sales", "entitlements": ["E1"]},
        ]
        archetypes = [("Sales", ["E1"], 2)]
        departmental_recs = {"Sales": [("E1", 100.0)]}

        metrics = evaluate_role_mining(users, archetypes, departmental_recs)
        self.assertEqual(metrics["total_identities"], 2)
        self.assertEqual(metrics["discovered_role_archetypes"], 1)
        self.assertEqual(metrics["role_reduction_percentage"], 50.0)
        self.assertEqual(metrics["department_coverage_percentage"], 100.0)
        self.assertIn("Ground-truth role labels are currently unavailable", metrics["ground_truth_status"])

    def test_evaluate_supervised_recommendations(self):
        predicted = {"IT": ["E1", "E2"]}
        ground_truth = {"IT": ["E1", "E3"]}

        res = evaluate_supervised_recommendations(predicted, ground_truth)
        # Precision: 1 true pos / 2 predicted = 0.5
        # Recall: 1 true pos / 2 true = 0.5
        # F1: 0.5
        self.assertEqual(res["precision"], 0.5)
        self.assertEqual(res["recall"], 0.5)
        self.assertEqual(res["f1_score"], 0.5)


if __name__ == "__main__":
    unittest.main()
