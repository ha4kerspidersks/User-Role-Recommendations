# Contributing to User-Role-Recommendations

Thank you for contributing to **User-Role-Recommendations**! This project provides enterprise Identity Governance & Administration (IGA) least-privilege role mining and entitlement recommendation tools.

---

## 1. Code of Conduct

All contributors are expected to adhere to our [Code of Conduct](./CODE_OF_CONDUCT.md).

---

## 2. Architecture Overview

The package is organized under `src/role_recommendation/`:
- `data.py`: Schema validation, JSON file loading, dataset persistence.
- `models.py`: Vector space modeling with TF-IDF and Cosine Similarity matrices.
- `recommender.py`: Role archetype clustering, entitlement confirmation percentages, peer nearest neighbors.
- `evaluation.py`: Role reduction ratios, catalog metrics, benchmark harnesses.
- `cli.py`: Unified command-line interface (`role-recommendation`).
- `synthesize.py`: Deterministic synthetic identity generator.

---

## 3. Development Setup

### Prerequisites
- Python `3.10`, `3.11`, or `3.12`
- `venv` or `virtualenv`

### Installation
```bash
# 1. Clone repository
git clone https://github.com/ha4kerspidersks/User-Role-Recommendations.git
cd User-Role-Recommendations

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install package in editable mode with test dependencies
pip install -e ".[dev]"
```

---

## 4. Running Tests

Before submitting any code changes, ensure all tests pass:

```bash
# Run pytest test suite
pytest

# Test CLI smoke test
python3 -m role_recommendation.cli --help
python3 -m role_recommendation.cli stats
```

---

## 5. Coding & Safety Guidelines

- **Reproducibility**: Use fixed random seeds (`random_state=42`) for any stochastic algorithms or synthetic dataset generations.
- **Zero Real Data**: Never commit customer or real corporate identity datasets (names, employee IDs, proprietary entitlement names). All test datasets must use synthetic data.
- **No Runtime Installs**: Do not invoke `pip` or download binaries dynamically within library code. Pre-declare all dependencies in `pyproject.toml`.

---

## 6. Pull Request Process

1. Create a feature branch: `git checkout -b feat/your-feature-name`.
2. Implement your changes following PEP 8 conventions.
3. Add unit and integration tests in `tests/` covering new functions.
4. Verify tests pass with `pytest`.
5. Submit a Pull Request describing the motivation, implementation, and verification steps.
