"""
Unit tests for data loading, schema validation, and synthetic generation.
"""

import json
import tempfile
import unittest
from pathlib import Path

from role_recommendation.data import (
    generate_synthetic_dataset,
    load_dataset,
    save_dataset,
    validate_user_record,
)


class TestDataModule(unittest.TestCase):
    def test_validate_user_record_valid(self):
        sample = {
            "id": 101,
            "username": "alex",
            "email": "alex@corp.local",
            "department": "Engineering",
            "entitlements": ["E1", "E3"],
        }
        validated = validate_user_record(sample, index=0)
        self.assertEqual(validated["id"], 101)
        self.assertEqual(validated["username"], "alex")
        self.assertEqual(validated["department"], "Engineering")
        self.assertEqual(validated["entitlements"], ["E1", "E3"])

    def test_validate_user_record_invalid_type(self):
        with self.assertRaises(ValueError):
            validate_user_record("not-a-dict", index=0)

    def test_validate_user_record_invalid_entitlements(self):
        with self.assertRaises(ValueError):
            validate_user_record({"id": 1, "entitlements": "not-a-list"}, index=0)

    def test_load_dataset_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            load_dataset("/nonexistent/path/data.json")

    def test_generate_synthetic_dataset_deterministic(self):
        data1 = generate_synthetic_dataset(num_users=20, seed=123)
        data2 = generate_synthetic_dataset(num_users=20, seed=123)
        self.assertEqual(len(data1["users"]), 20)
        self.assertEqual(data1["users"][0], data2["users"][0])
        self.assertEqual(data1["users"][-1], data2["users"][-1])

    def test_save_and_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_data.json"
            sample_data = {
                "users": [
                    {
                        "id": 1,
                        "username": "dev1",
                        "email": "dev1@corp.local",
                        "department": "IT",
                        "entitlements": ["E2", "E4"],
                    }
                ]
            }
            save_dataset(sample_data, filepath)
            loaded = load_dataset(filepath)
            self.assertEqual(len(loaded), 1)
            self.assertEqual(loaded[0]["username"], "dev1")
            self.assertEqual(loaded[0]["department"], "IT")


if __name__ == "__main__":
    unittest.main()
