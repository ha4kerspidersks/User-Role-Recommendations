"""
Unit and integration tests for CLI interface.
"""

import tempfile
import unittest
from pathlib import Path

from role_recommendation.cli import build_parser, main


class TestCLIModule(unittest.TestCase):
    def test_build_parser_defaults(self):
        parser = build_parser()
        args = parser.parse_args([])
        self.assertIsNone(args.input)
        self.assertEqual(args.top_k, 5)
        self.assertEqual(args.format, "text")

    def test_cli_smoke_run(self):
        exit_code = main(["--top-k", "1"])
        self.assertEqual(exit_code, 0)

    def test_cli_json_format(self):
        exit_code = main(["--top-k", "1", "--format", "json"])
        self.assertEqual(exit_code, 0)

    def test_cli_evaluate_flag(self):
        exit_code = main(["--evaluate"])
        self.assertEqual(exit_code, 0)

    def test_cli_generate_synthetic(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = str(Path(tmpdir) / "synthetic.json")
            exit_code = main(["--generate-synthetic", "--output", out_file, "--num-users", "10", "--seed", "99"])
            self.assertEqual(exit_code, 0)
            self.assertTrue(Path(out_file).exists())


if __name__ == "__main__":
    unittest.main()
