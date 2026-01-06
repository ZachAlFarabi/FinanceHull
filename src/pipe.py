# src/pipe.py

from db import init_db
import subprocess
import sys

STEPS = [
    "ingest.py",
    "preprocess.py",
    "rolling.py",
]

def run_step(script):
    print(f"\n=== Running {script} ===")
    result = subprocess.run(
        [sys.executable, f"src/{script}"],
        check=True
    )
    return result.returncode


def main():
    for step in STEPS:
        run_step(step)

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
