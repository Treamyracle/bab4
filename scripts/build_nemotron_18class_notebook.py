#!/usr/bin/env python3
"""
Deterministic Builder for:
1. notebooks/nemotron_18class_colab_bundle.zip (Gold + Verified 17,525-sentence Nemotron 18-Class)
2. notebooks/Eksperimen_Nemotron_18Class_Colab.ipynb (Compiled from cell1.py .. cell10.py)
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys
import zipfile

import nbformat as nbf

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CELLS_DIR = ROOT / "notebooks" / "Eksperimen_Nemotron_18Class_cells"
DEFAULT_NOTEBOOK_PATH = ROOT / "notebooks" / "Eksperimen_Nemotron_18Class_Colab.ipynb"
DEFAULT_BUNDLE_PATH = ROOT / "notebooks" / "nemotron_18class_colab_bundle.zip"
DEFAULT_NEMOTRON_JSONL = ROOT / "data" / "distilled_nemotron_verified" / "corrected.jsonl"

GOLD_SOURCE_MAP = {
    "data/train.txt": "gold/train.txt",
    "data/valid.txt": "gold/valid.txt",
    "data/test.txt": "gold/test.txt",
    "data/labels-map.csv": "gold/labels-map.csv",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def count_conll_sentences(raw_bytes: bytes) -> int:
    text = raw_bytes.decode("utf-8-sig")
    count = 0
    buf = []
    for line in text.splitlines() + [""]:
        if not line.strip():
            if buf:
                count += 1
                buf = []
        else:
            buf.append(line)
    return count


def _load_gold_files_bytes(existing_bundle_path: Path | None = None) -> dict[str, bytes]:
    """Load Gold train/valid/test/labels-map bytes from bab4_source_bundle.zip or existing bundle."""
    source_bundle_candidates = [
        ROOT / "notebooks" / "bab4_source_bundle.zip",
        Path(r"C:\Users\tream\OneDrive\Documents\SKRIPSI\skripsi\notebooks\bab4_source_bundle.zip"),
        ROOT.parent / "SKRIPSI" / "skripsi" / "notebooks" / "bab4_source_bundle.zip",
    ]
    for candidate in source_bundle_candidates:
        if candidate.is_file():
            with zipfile.ZipFile(candidate, "r") as zf:
                return {dest_arc: zf.read(src_arc) for src_arc, dest_arc in GOLD_SOURCE_MAP.items()}

    if existing_bundle_path and existing_bundle_path.is_file():
        with zipfile.ZipFile(existing_bundle_path, "r") as zf:
            return {dest_arc: zf.read(dest_arc) for dest_arc in GOLD_SOURCE_MAP.values()}

    raise FileNotFoundError(
        "Could not locate bab4_source_bundle.zip or existing nemotron_18class_colab_bundle.zip for Gold files."
    )


def build_colab_bundle(
    bundle_path: Path = DEFAULT_BUNDLE_PATH,
    nemotron_jsonl_path: Path = DEFAULT_NEMOTRON_JSONL,
) -> dict:
    """Build deterministic notebooks/nemotron_18class_colab_bundle.zip with SHA-256 manifest."""
    bundle_path = Path(bundle_path).resolve()
    nemotron_jsonl_path = Path(nemotron_jsonl_path).resolve()
    if not nemotron_jsonl_path.is_file():
        raise FileNotFoundError(f"Verified Nemotron dataset not found: {nemotron_jsonl_path}")

    gold_bytes_map = _load_gold_files_bytes(existing_bundle_path=bundle_path)
    nemotron_bytes = nemotron_jsonl_path.read_bytes()

    nemotron_lines = [
        json.loads(line)
        for line in nemotron_bytes.decode("utf-8").splitlines()
        if line.strip()
    ]
    if len(nemotron_lines) != 17525:
        raise ValueError(f"Expected 17,525 verified Nemotron sentences, found {len(nemotron_lines)}")

    total_json_entities = sum(len(item.get("entities", [])) for item in nemotron_lines)
    for idx, item in enumerate(nemotron_lines):
        for ent in item.get("entities", []):
            if ent.get("type") in ("REG", "TTL"):
                raise ValueError(f"Forbidden tag in corrected.jsonl#{idx}: {ent}")

    archive_members: dict[str, bytes] = {
        **gold_bytes_map,
        "nemotron_18class/corrected.jsonl": nemotron_bytes,
    }

    sha256_map = {arc: sha256_bytes(content) for arc, content in sorted(archive_members.items())}
    files_info = {
        arc: {"sha256": sha256_bytes(content), "size_bytes": len(content)}
        for arc, content in sorted(archive_members.items())
    }

    manifest = {
        "format": "nemotron-18class-colab-bundle-v1",
        "sha256": sha256_map,
        "files": files_info,
        "record_counts": {
            "gold_train_raw_sentences": count_conll_sentences(gold_bytes_map["gold/train.txt"]),
            "gold_valid_raw_sentences": count_conll_sentences(gold_bytes_map["gold/valid.txt"]),
            "gold_test_raw_sentences": count_conll_sentences(gold_bytes_map["gold/test.txt"]),
            "gold_partitioned_train_sentences": 12465,
            "gold_partitioned_validation_sentences": 2543,
            "gold_partitioned_test_sentences": 2423,
            "gold_partitioned_test_entities": 8890,
            "nemotron_18class_sentences": len(nemotron_lines),
            "nemotron_18class_json_entities": total_json_entities,
            "nemotron_18class_partitioned_train_sentences": 14896,
            "nemotron_18class_partitioned_validation_sentences": 2629,
        },
    }
    manifest_bytes = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")

    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    fixed_dt = (2026, 1, 1, 0, 0, 0)
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for arc_name in sorted(archive_members):
            info = zipfile.ZipInfo(arc_name, date_time=fixed_dt)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, archive_members[arc_name])
        m_info = zipfile.ZipInfo("bundle_manifest.json", date_time=fixed_dt)
        m_info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(m_info, manifest_bytes)

    manifest["bundle_sha256"] = sha256_bytes(bundle_path.read_bytes())
    manifest["bundle_size_bytes"] = bundle_path.stat().st_size
    return manifest


def build_notebook(
    cells_dir: Path = DEFAULT_CELLS_DIR,
    output_path: Path = DEFAULT_NOTEBOOK_PATH,
    bundle_manifest: dict | None = None,
) -> Path:
    """Compile cell1.py .. cell10.py into notebooks/Eksperimen_Nemotron_18Class_Colab.ipynb."""
    cells_dir = Path(cells_dir).resolve()
    output_path = Path(output_path).resolve()
    manifest_path = cells_dir / "cell_manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Cell manifest not found: {manifest_path}")

    cell_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cell_specs = cell_manifest.get("cells", [])
    if len(cell_specs) != 10:
        raise ValueError(f"Expected 10 cells in cell_manifest.json, found {len(cell_specs)}")

    nb_cells = []
    for idx, spec in enumerate(cell_specs, start=1):
        fname = spec["file"]
        ctype = spec["cell_type"]
        fpath = cells_dir / fname
        if not fpath.is_file():
            raise FileNotFoundError(f"Missing cell file: {fpath}")

        raw_source = fpath.read_text(encoding="utf-8").strip()
        if ctype == "markdown":
            parsed_ast = ast.parse(raw_source, filename=fname)
            md_text = ast.get_docstring(parsed_ast, clean=False)
            if not md_text:
                raise ValueError(f"Markdown cell {fname} must contain a top-level docstring.")
            cell = nbf.v4.new_markdown_cell(md_text.strip())
        elif ctype == "code":
            compile(raw_source, fname, "exec")
            cell = nbf.v4.new_code_cell(raw_source)
        else:
            raise ValueError(f"Unsupported cell_type {ctype!r} in {fname}")

        cell["id"] = f"nemotron18c-cell-{idx:02d}-{sha256_bytes((fname + raw_source).encode('utf-8'))[:8]}"
        nb_cells.append(cell)

    notebook = nbf.v4.new_notebook(cells=nb_cells)
    notebook.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    notebook.metadata["language_info"] = {
        "name": "python",
        "version": "3.11",
    }
    notebook.metadata["colab"] = {
        "name": "Eksperimen_Nemotron_18Class_Colab.ipynb",
        "provenance": [],
        "gpuType": "A100",
    }
    notebook.metadata["nemotron_18class_experiment"] = {
        "format": cell_manifest.get("format", "nemotron-18class-colab-cells-v1"),
        "training_seeds": cell_manifest.get("training_seeds", [42]),
        "entity_classes": 18,
        "bio_tags": 37,
        "cells": [spec["file"] for spec in cell_specs],
        "bundle_sha256": bundle_manifest.get("bundle_sha256") if bundle_manifest else None,
    }

    nbf.validate(notebook)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(notebook, output_path)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build nemotron_18class_colab_bundle.zip and Eksperimen_Nemotron_18Class_Colab.ipynb."
    )
    parser.add_argument("--cells-dir", type=Path, default=DEFAULT_CELLS_DIR)
    parser.add_argument("--notebook-out", type=Path, default=DEFAULT_NOTEBOOK_PATH)
    parser.add_argument("--bundle-out", type=Path, default=DEFAULT_BUNDLE_PATH)
    parser.add_argument("--nemotron-jsonl", type=Path, default=DEFAULT_NEMOTRON_JSONL)
    parser.add_argument("--skip-bundle", action="store_true")
    args = parser.parse_args()

    bundle_manifest = None
    if not args.skip_bundle:
        bundle_manifest = build_colab_bundle(
            bundle_path=args.bundle_out,
            nemotron_jsonl_path=args.nemotron_jsonl,
        )
        print(
            f"✅ Built bundle: {args.bundle_out} "
            f"({bundle_manifest['bundle_size_bytes'] / (1024 * 1024):.2f} MB, "
            f"sha256={bundle_manifest['bundle_sha256'][:16]}...)"
        )

    nb_path = build_notebook(
        cells_dir=args.cells_dir,
        output_path=args.notebook_out,
        bundle_manifest=bundle_manifest,
    )
    print(f"✅ Built & validated notebook: {nb_path} (10 cells)")


if __name__ == "__main__":
    main()
