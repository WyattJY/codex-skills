#!/usr/bin/env python3
"""
Install and verify required packages for research-workflow.
Run with the Python interpreter you intend to use for the workflow.

  python scripts/setup.py          # install + verify
  python scripts/setup.py --check  # verify only (no install)
"""
import os
import sys
import subprocess
import shutil

PIP = [sys.executable, "-m", "pip", "install", "--no-input", "--progress-bar", "off"]

REQUIRED = [
    ("torch",        "torch",        ["torch", "torchvision", "--index-url", "https://download.pytorch.org/whl/cpu"]),
    ("docling",      "docling",      ["docling>=2.0", "docling-core>=2.0"]),
]


def check_imports() -> list[str]:
    """Return list of missing package names."""
    missing = []
    for name, import_name, _ in REQUIRED:
        try:
            __import__(import_name)
        except ImportError:
            missing.append(name)
    return missing


def install(packages: list[str]) -> None:
    subprocess.run(PIP + packages, check=True)


def ensure_pandoc() -> None:
    env_pandoc = os.environ.get("RESEARCH_PANDOC") or os.environ.get("PANDOC_EXE")
    if env_pandoc and shutil.which(env_pandoc):
        result = subprocess.run([env_pandoc, "--version"], capture_output=True, text=True)
        print(f"pandoc: {result.stdout.splitlines()[0]}")
        return
    if shutil.which("pandoc"):
        result = subprocess.run(["pandoc", "--version"], capture_output=True, text=True)
        print(f"pandoc: {result.stdout.splitlines()[0]}")
        return
    print("Installing pandoc ...")
    conda = shutil.which("conda")
    if conda:
        subprocess.run([conda, "install", "-c", "conda-forge", "pandoc", "-y", "--quiet"], check=False)
    elif sys.platform == "darwin" and shutil.which("brew"):
        subprocess.run(["brew", "install", "pandoc"], check=False)
    elif shutil.which("winget"):
        subprocess.run(["winget", "install", "--id", "JohnMacFarlane.Pandoc",
                        "--accept-source-agreements", "--accept-package-agreements", "-e"], check=False)
    if shutil.which("pandoc"):
        result = subprocess.run(["pandoc", "--version"], capture_output=True, text=True)
        print(f"pandoc installed: {result.stdout.splitlines()[0]}")
    else:
        print("WARNING: pandoc not installed. Word export will fail.")
        print("  Manual install: https://pandoc.org/installing.html")


def main() -> None:
    check_only = "--check" in sys.argv

    missing = check_imports()
    if not missing:
        print(f"OK — all packages importable (Python: {sys.executable})")
    elif check_only:
        print(f"MISSING: {', '.join(missing)}")
        sys.exit(1)
    else:
        for name, _, pip_args in REQUIRED:
            if name in missing:
                print(f"Installing {name} ...")
                install(pip_args)

    # Re-verify
    still_missing = check_imports()
    if still_missing:
        print(f"ERROR: still missing after install: {', '.join(still_missing)}")
        sys.exit(1)

    print(f"Verification passed — Python: {sys.executable}")
    ensure_pandoc()


if __name__ == "__main__":
    main()
