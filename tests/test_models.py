"""
Unit tests for Vector Space Model and similarity calculation.
"""

import unittest
import numpy as np

from role_recommendation.models import (
    IdentityVectorizer,
    compute_pairwise_similarity,
    find_most_similar_peers,
)


class TestModelsModule(unittest.TestCase):
    def setUp(self):
        self.users = [
            {"id": 1, "department": "Engineering", "entitlements": ["E1", "E2"]},
            {"id": 2, "department": "Engineering", "entitlements": ["E1", "E2"]},
            {"id": 3, "department": "Finance", "entitlements": ["E5", "E6"]},
            {"id": 4, "department": "Engineering", "entitlements": ["E1", "E3"]},
        ]

    def test_vectorizer_fit_transform(self):
        vectorizer = IdentityVectorizer()
        matrix = vectorizer.fit_transform(self.users)
        self.assertEqual(matrix.shape[0], len(self.users))
        self.assertGreater(matrix.shape[1], 0)
        self.assertTrue(vectorizer.is_fitted)

    def test_vectorizer_transform_unfitted_raises(self):
        vectorizer = IdentityVectorizer()
        with self.assertRaises(RuntimeError):
            vectorizer.transform(self.users)

    def test_compute_pairwise_similarity(self):
        vectorizer = IdentityVectorizer()
        matrix = vectorizer.fit_transform(self.users)
        sim = compute_pairwise_similarity(matrix)

        self.assertEqual(sim.shape, (len(self.users), len(self.users)))
        # Identical users (0 and 1) should have cosine similarity approx 1.0
        self.assertAlmostEqual(sim[0, 1], 1.0, places=4)
        # Disjoint users (0 and 2) should have low / zero similarity
        self.assertLess(sim[0, 2], 0.1)

    def test_find_most_similar_peers(self):
        vectorizer = IdentityVectorizer()
        matrix = vectorizer.fit_transform(self.users)
        sim = compute_pairwise_similarity(matrix)

        peers = find_most_similar_peers(0, sim, top_k=2)
        self.assertEqual(len(peers), 2)
        # Peer 1 is identical to user 0
        top_peer_idx, top_score = peers[0]
        self.assertEqual(top_peer_idx, 1)
        self.assertAlmostEqual(top_score, 1.0, places=4)


if __name__ == "__main__":
    unittest.main()
