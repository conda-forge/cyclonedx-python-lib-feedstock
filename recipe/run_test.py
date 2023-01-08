from pathlib import Path
import os
import json
import subprocess
import sys

# test sources
PKG_VERSION = os.environ["PKG_VERSION"]
SRC_DIR = Path(os.environ["SRC_DIR"])
TESTS = SRC_DIR / "src/tests"
COV_THRESHOLD = 91
JSON_FIXTURES = sorted((TESTS / "fixtures/json").rglob("*.json"))
XML_FIXTURES = sorted((TESTS / "fixtures/xml").rglob("*.xml"))
OLD_VERSION = json.loads(JSON_FIXTURES[0].read_text(encoding="utf-8"))["metadata"]["tools"][0]["version"]
REPLACEMENTS = {
    (
        f'''"version": "{OLD_VERSION}"''',
        f'''"version": "{PKG_VERSION}"''',
    ): JSON_FIXTURES,
    (
        f'''<version>{OLD_VERSION}</version>''',
        f'''<version>{PKG_VERSION}</version>''',
    ):XML_FIXTURES
}

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


if __name__ == "__main__":
    print("updating fixture versions...", flush=True)

    for from_to_version, fixtures in REPLACEMENTS.items():
        from_version, to_version = from_to_version
        print(f"... handling {len(fixtures)} fixtures", flush=True)
        print(f"    {from_version}   --->   {to_version}", flush=True)
        for fixture in fixtures:
            old_text = fixture.read_text(encoding="utf-8")
            if from_version in old_text:
                fixture.write_text(
                    old_text.replace(from_version, to_version),
                    encoding="utf-8"
                )
                print("  ... updated", fixture.relative_to(TESTS), flush=True)
            else:
                print("  --- skipped", fixture.relative_to(TESTS), flush=True)

    print(" ".join(PYTEST_ARGS), flush=True)

    sys.exit(subprocess.call(PYTEST_ARGS))
