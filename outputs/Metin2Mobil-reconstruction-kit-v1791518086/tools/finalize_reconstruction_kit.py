#!/usr/bin/env python3
"""Hash and zip the user-facing reconstruction kit."""

from __future__ import annotations

import hashlib
from pathlib import Path
import zipfile


def find_workspace_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "outputs/Metin2Mobil-reconstruction-kit-v1791518086").is_dir():
            return candidate
    raise RuntimeError("reconstruction kit not found")


ROOT = find_workspace_root()
KIT = ROOT / "outputs/Metin2Mobil-reconstruction-kit-v1791518086"
ZIP = ROOT / "outputs/Metin2Mobil-reconstruction-kit-v1791518086.zip"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    ignored = {"SHA256SUMS.txt"}
    files = sorted(
        path for path in KIT.rglob("*")
        if path.is_file() and path.name not in ignored and "__pycache__" not in path.parts
    )
    manifest = "".join(f"{sha256(path)}  {path.relative_to(KIT).as_posix()}\n" for path in files)
    (KIT / "SHA256SUMS.txt").write_text(manifest, encoding="ascii", newline="\n")
    files.append(KIT / "SHA256SUMS.txt")
    with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(files):
            archive.write(path, (Path(KIT.name) / path.relative_to(KIT)).as_posix())
    print(f"files={len(files)}")
    print(f"zip_bytes={ZIP.stat().st_size}")
    print(f"zip_sha256={sha256(ZIP)}")


if __name__ == "__main__":
    main()
