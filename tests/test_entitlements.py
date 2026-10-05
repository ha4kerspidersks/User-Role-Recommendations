import os
import json
import unittest

class TestEntitlementsData(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'user_entitlements_data.json')

    def test_json_file_exists(self):
        self.assertTrue(os.path.exists(self.data_path), "user_entitlements_data.json should exist")

    def test_json_structure(self):
        with open(self.data_path, 'r') as fp:
            data = json.load(fp)
        self.assertIn('users', data, "Dataset should contain 'users' root key")
        users = data['users']
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0, "Users list should not be empty")
        sample = users[0]
        self.assertIn('id', sample)
        self.assertIn('username', sample)
        self.assertIn('email', sample)
        self.assertIn('department', sample)
        self.assertIn('entitlements', sample)
        self.assertIsInstance(sample['entitlements'], list)

if __name__ == '__main__':
    unittest.main()
