#!/usr/bin/env python3
"""
User-Role-Recommendations Legacy Entrypoint.

Maintained for backward compatibility. Imports and executes the modular
role recommendation pipeline from src.role_recommendation without runtime
dependency downloads or state mutation.
"""

import sys
from pathlib import Path

# Ensure src/ is on the Python module search path
REPO_ROOT = Path(__file__).resolve().parent
SRC_PATH = REPO_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from role_recommendation.cli import main

if __name__ == "__main__":
    sys.exit(main())
