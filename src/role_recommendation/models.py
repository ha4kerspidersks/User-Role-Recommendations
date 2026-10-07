"""
Machine Learning models and Vector Space Modeling for identities.
"""

from typing import Any, Dict, List, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class IdentityVectorizer:
    """
    Transforms identity department and entitlement tokens into a TF-IDF vector space.
    """

    def __init__(self, **tfidf_kwargs):
        self.vectorizer = TfidfVectorizer(**tfidf_kwargs)
        self.is_fitted = False

    @staticmethod
    def format_identity_document(user: Dict[str, Any]) -> str:
        """
        Creates a space-delimited document of department and entitlement tokens.
        """
        department = user.get("department", "Unknown")
        entitlements = user.get("entitlements", [])
        return f"{department} {' '.join(entitlements)}".strip()

    def fit_transform(self, users: List[Dict[str, Any]]) -> Any:
        """
        Fits TF-IDF on user documents and returns the sparse feature matrix.
        """
        documents = [self.format_identity_document(user) for user in users]
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        self.is_fitted = True
        return tfidf_matrix

    def transform(self, users: List[Dict[str, Any]]) -> Any:
        """
        Transforms user documents into existing TF-IDF feature space.
        """
        if not self.is_fitted:
            raise RuntimeError("Vectorizer must be fitted before calling transform.")
        documents = [self.format_identity_document(user) for user in users]
        return self.vectorizer.transform(documents)

    @property
    def feature_names(self) -> List[str]:
        """
        Returns vocabulary feature names.
        """
        return self.vectorizer.get_feature_names_out().tolist()


def compute_pairwise_similarity(tfidf_matrix: Any) -> np.ndarray:
    """
    Computes pairwise cosine similarity between identity feature vectors
    using scikit-learn's linear_kernel.
    """
    return linear_kernel(tfidf_matrix, tfidf_matrix)


def find_most_similar_peers(
    user_idx: int,
    cosine_sim: np.ndarray,
    top_k: int = 5,
) -> List[Tuple[int, float]]:
    """
    Finds top_k most similar peer identities given a user index in the matrix.
    Excludes the user themselves (similarity 1.0 at diagonal).
    """
    if user_idx < 0 or user_idx >= cosine_sim.shape[0]:
        raise IndexError(f"User index {user_idx} out of bounds for matrix of size {cosine_sim.shape[0]}.")

    sim_scores = list(enumerate(cosine_sim[user_idx]))
    # Sort descending by similarity score, excluding self
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    peers = [peer for peer in sim_scores if peer[0] != user_idx]
    return peers[:top_k]
