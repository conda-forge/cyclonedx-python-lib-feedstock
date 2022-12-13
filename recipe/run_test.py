from pathlib import Path
import os
import subprocess
import sys

# test sources
SRC_DIR = Path(os.environ["SRC_DIR"])
TESTS = SRC_DIR / "src/tests"
COV_THRESHOLD = 91

os.environ.update(
    # see https://github.com/CycloneDX/cyclonedx-python-lib/issues/202
    PYTHONHASHSEED="0",
    # expects importable paths
    PYTHONPATH=str(TESTS),
)

PYTEST_ARGS = [
    "pytest",
    "-vv",
    "--cov=cyclonedx",
    f"--cov-fail-under={COV_THRESHOLD}",
    "--cov-report=term-missing:skip-covered",
    "--no-cov-on-fail",
    str(TESTS),
]

print(" ".join(PYTEST_ARGS), flush=True)

sys.exit(subprocess.call(PYTEST_ARGS))
