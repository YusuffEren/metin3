#!/usr/bin/env python3
"""Create compact inventories for the fully unpacked asset tree."""

from __future__ import annotations

import csv
from collections import defaultdict
import hashlib
from pathlib import Path


def find_workspace_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "outputs/Metin2Mobil-full-v1791518086").is_dir():
            return candidate
    raise RuntimeError("workspace root with extracted Metin2Mobil outputs was not found")


ROOT = find_workspace_root()
SOURCE = ROOT / "outputs/Metin2Mobil-full-v1791518086/unpacked"
OUT = ROOT / "outputs/Metin2Mobil-reconstruction-kit-v1791518086/assets"


def write_stats(path: Path, rows: list[tuple[str, int, int]], first_name: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([first_name, "files", "bytes"])
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    extensions: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    top_levels: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    all_files = sorted(
        path for path in SOURCE.rglob("*")
        if path.is_file() and path.name != "unpack-report.json"
    )
    for path in all_files:
        size = path.stat().st_size
        ext = path.suffix.lower() or "<none>"
        top = path.relative_to(SOURCE).parts[0]
        extensions[ext][0] += 1
        extensions[ext][1] += size
        top_levels[top][0] += 1
        top_levels[top][1] += size

    write_stats(
        OUT / "by-extension.csv",
        [(name, count, size) for name, (count, size) in sorted(extensions.items(), key=lambda item: (-item[1][0], item[0]))],
        "extension",
    )
    write_stats(
        OUT / "by-top-level.csv",
        [(name, count, size) for name, (count, size) in sorted(top_levels.items(), key=lambda item: (-item[1][1], item[0]))],
        "directory",
    )

    patterns = (
        "item_proto", "mob_proto", "item_list.txt", "skilldesc.txt", "skilltable.txt",
        "atlasinfo.txt", "locale_game.txt", "locale_interface.txt", "serverinfo.py",
        "intrologin.py", "introselect.py", "game.py", "interfacemodule.py",
    )
    critical = [path for path in all_files if path.name.lower() in patterns]
    with (OUT / "critical-files.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["relative_path", "bytes", "sha256"])
        for path in critical:
            writer.writerow([
                path.relative_to(SOURCE).as_posix(), path.stat().st_size,
                hashlib.sha256(path.read_bytes()).hexdigest(),
            ])

    atlas = SOURCE / "locale_tr/locale/tr/atlasinfo.txt"
    with (OUT / "map-atlas.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["map", "base_x", "base_y", "width_sections", "height_sections"])
        for line in atlas.read_text(encoding="cp1254", errors="replace").splitlines():
            fields = line.split()
            if len(fields) == 5:
                writer.writerow(fields)

    summary = OUT / "SUMMARY.txt"
    summary.write_text(
        f"files={len(all_files)}\nbytes={sum(path.stat().st_size for path in all_files)}\n"
        f"extensions={len(extensions)}\ntop_level_directories={len(top_levels)}\n",
        encoding="utf-8",
    )
    print(summary.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
