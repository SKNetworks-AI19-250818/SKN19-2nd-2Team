"""
Organize existing images into standardized folders.

Usage (from repo root):
  python scripts/migrate_images.py

Rules:
- Model figures → docs/img/model/
  keywords: ["roc", "pr", "precision_recall", "auc", "confusion", "cm", "metrics", "importance"]
- EDA figures → docs/img/eda/{COLUMN}/
  - COLUMN inferred by matching filename tokens to labels.json keys or discovered column lists
  - If no match → docs/img/eda/_misc/

This script is idempotent (safe to re-run). It prints a manifest at docs/summary/eda/image_manifest.csv
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Dict, List, Set

REPO_ROOT = Path(__file__).resolve().parents[1]
IMG_ROOT = REPO_ROOT / "docs" / "img"
EDA_ROOT = IMG_ROOT / "eda"
MODEL_ROOT = IMG_ROOT / "model"
LABELS_PATH = REPO_ROOT / "docs" / "summary" / "eda" / "labels.json"
MANIFEST_PATH = REPO_ROOT / "docs" / "summary" / "eda" / "image_manifest.csv"
MAPPING_CSV = REPO_ROOT / "docs" / "summary" / "eda" / "image_mapping_template.csv"

MODEL_KEYWORDS = [
    "roc",
    "pr",
    "precision_recall",
    "auc",
    "confusion",
    "cm",
    "metrics",
    "importance",
]


def load_labels() -> Set[str]:
    keys: Set[str] = set()
    if LABELS_PATH.exists():
        try:
            data = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
            keys |= set(map(str, data.keys()))
        except Exception:
            pass

    # Also collect known column files named columns.json across repo (best-effort)
    for path in REPO_ROOT.rglob("columns.json"):
        try:
            j = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(j, dict):
                keys |= set(map(str, j.keys()))
            elif isinstance(j, list):
                keys |= set(map(str, j))
        except Exception:
            continue
    return keys


def is_model_figure(name: str) -> bool:
    low = name.lower()
    return any(k in low for k in MODEL_KEYWORDS)


def guess_column(name: str, known_cols: Set[str]) -> str | None:
    base = Path(name).stem
    tokens = re.split(r"[^A-Za-z0-9_]+", base)
    tokens = [t for t in tokens if t]
    # exact match first
    for t in tokens:
        if t in known_cols:
            return t
        if t.upper() in known_cols:
            return t.upper()
        if t.lower() in known_cols:
            # Keep original case from known_cols if present
            for kc in known_cols:
                if kc.lower() == t.lower():
                    return kc
    # common prefixes
    for t in tokens:
        for kc in known_cols:
            if kc.lower().startswith(t.lower()) and len(t) >= 3:
                return kc
    return None


def ensure_dirs():
    EDA_ROOT.mkdir(parents=True, exist_ok=True)
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)


def move_images() -> List[str]:
    ensure_dirs()
    known_cols = load_labels()
    moved: List[str] = []

    candidates = [p for p in IMG_ROOT.iterdir() if p.is_file()]
    for p in candidates:
        target: Path
        if is_model_figure(p.name):
            target = MODEL_ROOT / p.name
        else:
            col = guess_column(p.name, known_cols) or "_misc"
            target_dir = EDA_ROOT / col
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / p.name

        if target.resolve() == p.resolve():
            continue
        try:
            shutil.move(str(p), str(target))
            moved.append(f"{p.name} -> {target.relative_to(REPO_ROOT)}")
        except Exception as e:
            print(f"Skip {p.name}: {e}")

    return moved


def write_manifest(rows: List[str]):
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", encoding="utf-8") as f:
        f.write("filename,relocated_to\n")
        for r in rows:
            left, right = r.split(" -> ", 1)
            f.write(f"{left},{right}\n")


def apply_mapping() -> List[str]:
    """Apply manual filename->column mapping from MAPPING_CSV.

    Rows with empty column are ignored. Moves files from eda/_misc to eda/{col}.
    """
    if not MAPPING_CSV.exists():
        return []
    moved: List[str] = []
    lines = MAPPING_CSV.read_text(encoding="utf-8").splitlines()
    if not lines:
        return []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 2:
            continue
        fname, col = parts[0], parts[1]
        if not fname or not col:
            continue
        src = EDA_ROOT / "_misc" / fname
        if not src.exists():
            continue
        dest_dir = EDA_ROOT / col
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / fname
        try:
            shutil.move(str(src), str(dest))
            moved.append(f"{fname} -> {dest.relative_to(REPO_ROOT)}")
        except Exception as e:
            print(f"Mapping skip {fname}: {e}")
    return moved


def main():
    moved = move_images()
    moved += apply_mapping()
    write_manifest(moved)
    print(f"Moved {len(moved)} images. Manifest: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()


