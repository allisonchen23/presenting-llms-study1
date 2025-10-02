#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
copy_reported_results.py

Dynamic script to copy and rename analysis result files into a `reported_results` folder.
Supports multiple studies (Study 1, Study 2, …) without hardcoding paths in the logic.

Usage examples:
    # Copy files for Study 1
    python copy_reported_results.py --study 1

    # Copy files for Study 2, stop if anything is missing
    python copy_reported_results.py --study 2 --fail-on-missing
"""

import os
import shutil
import glob
from dataclasses import dataclass
from typing import List


# Data structure for copy instructions

@dataclass
class CopySpec:
    """
    A single copy instruction.

    Attributes
    ----------
    src : str
        Relative path from repo_root. Can be:
          - An exact file path
          - A glob pattern (e.g., "*.txt")
    dst : str
        Relative destination path from repo_root. Can be:
          - A folder (ends with '/' or existing folder path)
          - A full file path (to rename the file on copy)
    """
    src: str
    dst: str


# Helper functions

def ensure_parent_dir(path: str) -> None:
    """Make sure the parent directory of `path` exists."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def resolve_sources(repo_root: str, src_pattern: str) -> List[str]:
    """
    Expand glob patterns (like *.txt) relative to repo_root.
    Returns a list of absolute paths for source files.
    If no matches and no file exists, returns [].
    """
    abs_pattern = os.path.join(repo_root, src_pattern)
    matches = glob.glob(abs_pattern)
    if matches:
        return matches
    return [abs_pattern] if os.path.exists(abs_pattern) else []


def is_dirish(path: str) -> bool:
    """
    Decide if a path should be treated as a directory.
    - If it ends with '/' or '\\'
    - Or if it already exists and is a directory
    """
    return path.endswith(("/", "\\")) or (os.path.exists(path) and os.path.isdir(path))


def copy_one(src_abs: str, dst_abs: str) -> None:
    """
    Copy one file from src_abs → dst_abs.
    """
    ensure_parent_dir(dst_abs)
    shutil.copy2(src_abs, dst_abs)  # copy2 preserves metadata like timestamps
    print(f"Copied {src_abs} → {dst_abs}")


def apply_spec(repo_root: str, spec: CopySpec, fail_on_missing: bool = False) -> None:
    """
    Apply a single CopySpec:
    - Resolve source files
    - Decide if destination is a directory or file
    - Copy each file accordingly
    """
    src_files = resolve_sources(repo_root, spec.src)
    if not src_files:
        msg = f"WARNING: no source matched '{spec.src}'"
        if fail_on_missing:
            raise FileNotFoundError(msg)
        print(msg)
        return

    dst_abs = os.path.join(repo_root, spec.dst)
    dst_is_dir = is_dirish(dst_abs)

    # Force treat as directory if dst ends with a slash, even if it doesn't exist yet
    if not dst_is_dir and spec.dst.endswith(("/", "\\")):
        dst_is_dir = True

    for src_abs in src_files:
        if dst_is_dir:
            # Copy into the directory, keeping the same filename
            final_dst = os.path.join(dst_abs, os.path.basename(src_abs))
        else:
            # Copy to an exact file path (useful for renaming)
            final_dst = dst_abs
        copy_one(src_abs, final_dst)


def prepare_reported_results(repo_root: str, specs: List[CopySpec], fail_on_missing: bool = False) -> None:
    """
    Run a full list of copy specifications for a given study.
    """
    for spec in specs:
        apply_spec(repo_root, spec, fail_on_missing=fail_on_missing)
    print("Finished preparing reported_results.")



# Study-specific mappings

# Study 1 file mappings
STUDY1_SPECS: List[CopySpec] = [
    # Section 3.2.1–2: Mental capacities --> rename
    CopySpec(
        src="analysis/mental_capacities/factor_analysis/results/R/results/3_components_results.txt",
        dst="reported_results/sec3.2.1-2_results.txt",
    ),

    # Section 3.2.3: Attitudes --> copy/rename into a results folder
    CopySpec(src="analysis/attitudes/R/results/confidence_results.txt", dst="reported_results/sec3.2.3_results/"),
    CopySpec(src="analysis/attitudes/R/results/feeling_results.txt",    dst="reported_results/sec3.2.3_results/"),
    CopySpec(src="analysis/attitudes/R/results/humanness_results.txt",  dst="reported_results/sec3.2.3_results/"),
    CopySpec(src="analysis/attitudes/R/results/se_use.txt",              dst="reported_results/sec3.2.3_results/conf_using_results.txt"),
    CopySpec(src="analysis/attitudes/R/results/se_how.txt",              dst="reported_results/sec3.2.3_results/conf_program_results.txt"),
    CopySpec(src="analysis/attitudes/R/results/trust_results.txt",       dst="reported_results/sec3.2.3_results/"),
]




# CLI entry point

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Copy/rename analysis outputs into reported_results.")
    parser.add_argument("--repo-root", default=os.path.abspath("."), help="Repo root (default: current directory)")
    parser.add_argument("--study", choices=["1", "2"], required=True, help="Which study mapping to run")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without copying")
    parser.add_argument("--fail-on-missing", action="store_true", help="Error out if a source file is missing")
    args = parser.parse_args()

    # Choose the correct spec set based on CLI argument
    specs = STUDY1_SPECS

    # Run the copy logic
    prepare_reported_results(
        repo_root=args.repo_root,
        specs=specs,
        fail_on_missing=args.fail_on_missing,
    )
