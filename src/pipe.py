# src/pipe.py

from .db import init_db
import subprocess
import sys

STEPS = [
    "ingest.py",
    "preprocess.py",
    "rolling.py",
    "visProt1.py"
]

def run_step(script):
    # Remove 'src/' from the path, just use module name
    module_name = script.replace(".py", "")
    subprocess.run(
        [sys.executable, "-m", f"src.{module_name}"],
        check=True
    )

def main():
    for step in STEPS:
        run_step(step)

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
