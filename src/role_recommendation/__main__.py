"""
Entrypoint for module execution via python -m role_recommendation.
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
