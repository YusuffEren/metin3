#!/usr/bin/env python3
"""Build a reconstruction-oriented index from the extracted Metin2 Mobile client.

The generated material is evidence, not the original source code.  It deliberately
keeps automatic inferences separate from manually verified protocol facts.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


def find_workspace_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "outputs/Metin2Mobil-full-v1791518086").is_dir():
            return candidate
    raise RuntimeError("workspace root with extracted Metin2Mobil outputs was not found")


ROOT = find_workspace_root()
PSEUDO = ROOT / "outputs/Metin2Mobil-native-pseudocode-v0.75.0/libsancak2client-selected.c"
UNPACKED = ROOT / "outputs/Metin2Mobil-full-v1791518086/unpacked"
OUT = ROOT / "outputs/Metin2Mobil-reconstruction-kit-v1791518086"


FUNCTION_HEADER = re.compile(
    r"^/\* ={20,}\r?\n \* (?P<name>.*?) @ (?P<address>[0-9a-fA-F]+)\r?\n \* ={20,} \*/",
    re.MULTILINE,
)

CATEGORIES = {
    "network-protocol": re.compile(
        r"Network|Packet|Socket|TCP|UDP|Handshake|HandShake|Crypto|Cipher|Connect|LoginPhase|SelectPhase|LoadingPhase|GamePhase",
        re.I,
    ),
    "python-native-api": re.compile(r"CPython|Python|PyObject|PyCall|PyTuple|PyDict|PyList|PyLong|PyString", re.I),
    "gameplay-actor": re.compile(
        r"Actor|Character|Player|Item|Skill|Guild|Quest|Shop|Mount|Race|Dungeon|Fishing|NonPlayer|Background|EffectInstance",
        re.I,
    ),
    "graphics-resource": re.compile(
        r"Graphic|Render|Texture|Image|Model|Mesh|Resource|EterPack|PackManager|Vfs|BGFX|bgfx|Granny|Camera|Terrain",
        re.I,
    ),
    "android-platform": re.compile(r"Android|JNI|Java_|ANative|AAsset|EGL|OpenSLES|AAudio", re.I),
}

IMPORT_RE = re.compile(r"^\s*(?:from\s+([A-Za-z_][\w.]*)\s+import\s+|import\s+([^#;\r\n]+))", re.MULTILINE)
KNOWN_STDLIB = {
    "abc", "array", "atexit", "base64", "binascii", "calendar", "cmath", "collections", "copy",
    "datetime", "errno", "functools", "gc", "glob", "hashlib", "heapq", "hmac", "io", "itertools",
    "json", "locale", "logging", "marshal", "math", "operator", "os", "pickle", "random", "re",
    "select", "shutil", "socket", "sqlite3", "stat", "string", "struct", "subprocess", "sys", "tempfile",
    "thread", "threading", "time", "traceback", "types", "urllib", "uuid", "weakref", "xml", "zipfile",
}


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def parse_functions(text: str) -> list[dict[str, str]]:
    matches = list(FUNCTION_HEADER.finditer(text))
    functions: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        functions.append(
            {
                "name": match.group("name"),
                "address": match.group("address").lower(),
                "body": text[match.start():end].rstrip() + "\n",
            }
        )
    return functions


def build_native_index(functions: list[dict[str, str]]) -> dict[str, int]:
    native_dir = OUT / "native"
    native_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    membership: dict[tuple[str, str], list[str]] = defaultdict(list)

    for category, pattern in CATEGORIES.items():
        selected = [fn for fn in functions if pattern.search(fn["name"])]
        counts[category] = len(selected)
        for fn in selected:
            membership[(fn["address"], fn["name"])].append(category)
        prelude = (
            "/* Reconstructed by Ghidra from the ARM64 client; not original source.\n"
            f" * Category: {category}; selected functions: {len(selected)}.\n"
            " */\n\n"
        )
        write_text(native_dir / f"{category}.c", prelude + "\n".join(fn["body"] for fn in selected))

    with (native_dir / "function-catalog.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["address", "function", "categories", "decompiled_lines"])
        for fn in functions:
            cats = membership.get((fn["address"], fn["name"]), [])
            writer.writerow([fn["address"], fn["name"], ";".join(cats), fn["body"].count("\n")])

    candidates = []
    for fn in functions:
        if not re.search(r"(?:Send|Recv|Receive).*Packet|Packet.*(?:Send|Recv|Receive)", fn["name"], re.I):
            continue
        send_sizes = sorted(set(re.findall(r"(?:^|::)Send\([^\n]{0,180}?(0x[0-9a-f]+|\d+)", fn["body"], re.I)))
        recv_sizes = sorted(set(re.findall(r"(?:^|::)Recv\([^\n]{0,180}?(0x[0-9a-f]+|\d+)", fn["body"], re.I)))
        byte_assignments = sorted(set(re.findall(r"=\s*(?:'\\x([0-9a-fA-F]{2})'|0x([0-9a-fA-F]{1,2}))\s*;", fn["body"])))
        byte_values = sorted({(a or b).lower().zfill(2) for a, b in byte_assignments})
        candidates.append(
            {
                "address": fn["address"],
                "function": fn["name"],
                "direction": "send" if "send" in fn["name"].lower() else "receive",
                "send_size_candidates": ";".join(send_sizes),
                "recv_size_candidates": ";".join(recv_sizes),
                "byte_constant_candidates": ";".join("0x" + item for item in byte_values),
            }
        )
    protocol_dir = OUT / "protocol"
    protocol_dir.mkdir(parents=True, exist_ok=True)
    with (protocol_dir / "packet-function-candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(candidates[0]) if candidates else ["address"])
        writer.writeheader()
        writer.writerows(candidates)
    return counts


def decode_source(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "cp1254", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass
    return data.decode("utf-8", errors="replace")


def build_python_graph() -> dict[str, object]:
    files = sorted({*UNPACKED.rglob("*.py"), *UNPACKED.rglob("*.py.bak")})
    local_by_name: dict[str, list[str]] = defaultdict(list)
    for path in files:
        stem = path.name.split(".py", 1)[0]
        local_by_name[stem.lower()].append(path.relative_to(UNPACKED).as_posix())

    edges: set[tuple[str, str, str]] = set()
    imported = Counter()
    parse_errors: list[dict[str, str]] = []
    for path in files:
        rel = path.relative_to(UNPACKED).as_posix()
        try:
            source = decode_source(path)
        except OSError as exc:
            parse_errors.append({"file": rel, "error": str(exc)})
            continue
        for match in IMPORT_RE.finditer(source):
            modules: list[str]
            if match.group(1):
                modules = [match.group(1)]
            else:
                modules = []
                for item in match.group(2).split(","):
                    token = item.strip().split()[0] if item.strip() else ""
                    if token:
                        modules.append(token)
            for module in modules:
                root = module.split(".", 1)[0]
                if not root:
                    continue
                imported[root] += 1
                kind = "local-python" if root.lower() in local_by_name else ("stdlib" if root in KNOWN_STDLIB else "native-or-external")
                edges.add((rel, root, kind))

    py_dir = OUT / "python"
    py_dir.mkdir(parents=True, exist_ok=True)
    with (py_dir / "dependency-edges.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "import", "classification"])
        writer.writerows(sorted(edges))

    native_modules = [
        {"module": name, "import_count": count}
        for name, count in imported.most_common()
        if name.lower() not in local_by_name and name not in KNOWN_STDLIB
    ]
    with (py_dir / "native-or-external-modules.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["module", "import_count"])
        writer.writeheader()
        writer.writerows(native_modules)

    # Calls and constants used by the recovered Python layer are a practical
    # specification for the C++ extension modules that a clean-room client needs.
    native_names = {row["module"] for row in native_modules}
    api_calls: dict[tuple[str, str], dict[str, object]] = {}
    api_constants: dict[tuple[str, str], dict[str, object]] = {}
    for path in files:
        rel = path.relative_to(UNPACKED).as_posix()
        source = decode_source(path)
        for module, member in re.findall(r"\b([A-Za-z_]\w*)\.([A-Za-z_]\w*)\s*\(", source):
            if module not in native_names:
                continue
            entry = api_calls.setdefault((module, member), {"module": module, "member": member, "uses": 0, "files": set()})
            entry["uses"] = int(entry["uses"]) + 1
            entry["files"].add(rel)
        for module, member in re.findall(r"\b([A-Za-z_]\w*)\.([A-Z][A-Z0-9_]{2,})\b", source):
            if module not in native_names:
                continue
            entry = api_constants.setdefault((module, member), {"module": module, "member": member, "uses": 0, "files": set()})
            entry["uses"] = int(entry["uses"]) + 1
            entry["files"].add(rel)

    for filename, records in (("native-api-calls.csv", api_calls), ("native-api-constants.csv", api_constants)):
        with (py_dir / filename).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["module", "member", "uses", "source_files"])
            for key in sorted(records):
                entry = records[key]
                writer.writerow([entry["module"], entry["member"], entry["uses"], ";".join(sorted(entry["files"]))])

    dot_lines = ["digraph python_dependencies {", "  rankdir=LR;", "  node [fontsize=9];"]
    for src, dst, kind in sorted(edges):
        src_name = Path(src).name.replace(".bak", "")
        if kind == "local-python":
            dot_lines.append(f'  "{src_name}" -> "{dst}.py";')
    dot_lines.append("}")
    write_text(py_dir / "dependencies.dot", "\n".join(dot_lines) + "\n")
    summary = {
        "python_files": len(files),
        "dependency_edges": len(edges),
        "unique_imports": len(imported),
        "native_or_external_modules": len(native_modules),
        "native_api_calls": len(api_calls),
        "native_api_constants": len(api_constants),
        "parse_errors": parse_errors,
    }
    write_text(py_dir / "dependency-summary.json", json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    return summary


def main() -> None:
    text = PSEUDO.read_text(encoding="utf-8", errors="replace")
    functions = parse_functions(text)
    native_counts = build_native_index(functions)
    python_summary = build_python_graph()
    summary = {
        "input": str(PSEUDO.relative_to(ROOT)).replace("\\", "/"),
        "input_sha256": hashlib.sha256(PSEUDO.read_bytes()).hexdigest(),
        "functions_indexed": len(functions),
        "category_counts": native_counts,
        "python": python_summary,
        "notes": [
            "Native files are reconstructed pseudocode, not the original C++ source.",
            "A function may appear in more than one category.",
            "Packet candidates are automatic leads; verified facts live in packet-catalog.csv.",
        ],
    }
    write_text(OUT / "reconstruction-index.json", json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
