#!/usr/bin/env python3
"""Decrypt and export the demo's MIPX/MMPT proto tables.

The outer table layouts come from the client decompilation (item stride 156,
mob stride 255).  XTEA keys are the conventional client proto keys and are
validated by the decrypted MCOZ magic and exact decompressed size.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
import struct
import sys


def find_workspace_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "outputs/Metin2Mobil-full-v1791518086").is_dir():
            return candidate
    raise RuntimeError("workspace root with extracted Metin2Mobil outputs was not found")


ROOT = find_workspace_root()
sys.path.insert(0, str(Path(__file__).resolve().parent / "vendor"))
sys.path.insert(0, str(ROOT / "work/native-analysis/vendor"))
import lzo  # type: ignore  # bundled wheel in work/native-analysis/vendor


SOURCE = ROOT / "outputs/Metin2Mobil-full-v1791518086/unpacked/locale_tr/locale/tr"
OUT = ROOT / "outputs/Metin2Mobil-reconstruction-kit-v1791518086/game-data"

ITEM_KEY = bytes.fromhex("A1 A4 02 00 AA 15 54 04 E7 8B 5A 18 AB D6 AA 01")
MOB_KEY = bytes.fromhex("46 74 49 00 0B 4A 00 00 B7 6E 08 00 9D 18 68 00")


def xtea_decrypt(data: bytes, key_bytes: bytes) -> bytes:
    if len(data) % 8:
        raise ValueError("XTEA buffer is not an 8-byte multiple")
    key = struct.unpack("<4I", key_bytes)
    out = bytearray(len(data))
    delta = 0x9E3779B9
    for offset in range(0, len(data), 8):
        v0, v1 = struct.unpack_from("<2I", data, offset)
        total = (delta * 32) & 0xFFFFFFFF
        for _ in range(32):
            term = ((((v0 << 4) & 0xFFFFFFFF) ^ (v0 >> 5)) + v0) & 0xFFFFFFFF
            v1 = (v1 - (term ^ ((total + key[(total >> 11) & 3]) & 0xFFFFFFFF))) & 0xFFFFFFFF
            total = (total - delta) & 0xFFFFFFFF
            term = ((((v1 << 4) & 0xFFFFFFFF) ^ (v1 >> 5)) + v1) & 0xFFFFFFFF
            v0 = (v0 - (term ^ ((total + key[total & 3]) & 0xFFFFFFFF))) & 0xFFFFFFFF
        struct.pack_into("<2I", out, offset, v0, v1)
    return bytes(out)


def unpack_crypted_object(blob: bytes, key: bytes) -> tuple[bytes, dict[str, int | str]]:
    magic, encrypted_size, compressed_size, real_size = struct.unpack_from("<4sIII", blob)
    if magic != b"MCOZ":
        raise ValueError(f"unsupported crypted-object magic {magic!r}")
    encrypted = blob[16:16 + encrypted_size]
    decrypted = xtea_decrypt(encrypted, key)
    if decrypted[:4] != b"MCOZ":
        raise ValueError("XTEA key validation failed: decrypted MCOZ magic missing")
    compressed = decrypted[4:compressed_size]
    try:
        raw = lzo.decompress(compressed, False, real_size)
    except Exception:
        # Some writers record the compressed payload length excluding magic.
        raw = lzo.decompress(decrypted[4:4 + compressed_size], False, real_size)
    if len(raw) != real_size:
        raise ValueError(f"decompressed size mismatch: {len(raw)} != {real_size}")
    return raw, {
        "magic": magic.decode("ascii"),
        "encrypted_size": encrypted_size,
        "compressed_size": compressed_size,
        "decompressed_size": real_size,
    }


def text(raw: bytes, encodings: tuple[str, ...] = ("cp1254", "utf-8", "latin-1")) -> str:
    chunk = raw.split(b"\0", 1)[0]
    for encoding in encodings:
        try:
            return chunk.decode(encoding)
        except UnicodeDecodeError:
            continue
    return chunk.decode("latin-1", errors="replace")


def u8(record: bytes, offset: int) -> int:
    return record[offset]


def u16(record: bytes, offset: int) -> int:
    return struct.unpack_from("<H", record, offset)[0]


def u32(record: bytes, offset: int) -> int:
    return struct.unpack_from("<I", record, offset)[0]


def i32(record: bytes, offset: int) -> int:
    return struct.unpack_from("<i", record, offset)[0]


def parse_item(record: bytes) -> dict[str, object]:
    row: dict[str, object] = {
        "vnum": u32(record, 0), "vnum_range": u32(record, 4),
        "name": text(record[8:33], ("cp949", "cp1254", "latin-1")), "locale_name": text(record[33:58]),
        "type": u8(record, 58), "subtype": u8(record, 59), "weight": u8(record, 60), "size": u8(record, 61),
        "anti_flags": u32(record, 62), "flags": u32(record, 66), "wear_flags": u32(record, 70),
        "immune_flags": u32(record, 74), "buy_price": u32(record, 78), "sell_price": u32(record, 82),
    }
    offset = 86
    for index in range(2):
        row[f"limit_type_{index}"] = u8(record, offset)
        row[f"limit_value_{index}"] = i32(record, offset + 1)
        offset += 5
    for index in range(3):
        row[f"apply_type_{index}"] = u8(record, offset)
        row[f"apply_value_{index}"] = i32(record, offset + 1)
        offset += 5
    for index in range(6):
        row[f"value_{index}"] = i32(record, offset)
        offset += 4
    for index in range(3):
        row[f"socket_{index}"] = i32(record, offset)
        offset += 4
    row.update(
        refined_vnum=u32(record, 147), refine_set=u16(record, 151),
        alter_to_magic_pct=u8(record, 153), specular=u8(record, 154), gain_socket_pct=u8(record, 155),
    )
    return row


def parse_mob(record: bytes) -> dict[str, object]:
    row: dict[str, object] = {
        "vnum": u32(record, 0),
        "name": text(record[4:29], ("cp949", "cp1254", "latin-1")),
        "locale_name": text(record[29:54]),
        "type": u8(record, 54),
        "rank": u8(record, 55),
        "battle_type": u8(record, 56),
        "level": u8(record, 57),
        "size": u8(record, 58),
        "gold_min": u32(record, 59), "gold_max": u32(record, 63), "exp": u32(record, 67),
        "max_hp": u32(record, 71), "regen_cycle": u8(record, 75), "regen_percent": u8(record, 76),
        "defense": u16(record, 77), "ai_flags": u32(record, 79), "race_flags": u32(record, 83),
        "immune_flags": u32(record, 87), "str": u8(record, 91), "dex": u8(record, 92),
        "con": u8(record, 93), "int": u8(record, 94), "damage_min": u32(record, 95),
        "damage_max": u32(record, 99), "attack_speed": struct.unpack_from("<h", record, 103)[0],
        "move_speed": struct.unpack_from("<h", record, 105)[0], "aggressive_hp_pct": u8(record, 107),
        "aggressive_sight": u16(record, 108), "attack_range": u16(record, 110),
    }
    for index, name in enumerate(("curse", "slow", "poison", "stun", "critical", "penetrate")):
        row[f"enchant_{name}"] = struct.unpack_from("<b", record, 112 + index)[0]
    resist_names = ("sword", "twohand", "dagger", "bell", "fan", "bow", "fire", "elect", "magic", "wind", "poison")
    for index, name in enumerate(resist_names):
        row[f"resist_{name}"] = struct.unpack_from("<b", record, 118 + index)[0]
    row.update(
        resurrection_vnum=u32(record, 129), drop_item_vnum=u32(record, 133), mount_capacity=u8(record, 137),
        on_click_type=u8(record, 138), empire=u8(record, 139), folder=text(record[140:205]),
        damage_multiply=struct.unpack_from("<f", record, 205)[0], summon_vnum=u32(record, 209),
        drain_sp=u32(record, 213), monster_color=u32(record, 217), polymorph_item_vnum=u32(record, 221),
    )
    for index in range(5):
        offset = 225 + index * 5
        row[f"skill_vnum_{index}"] = u32(record, offset)
        row[f"skill_level_{index}"] = u8(record, offset + 4)
    for offset, name in enumerate(("berserk", "stone_skin", "god_speed", "death_blow", "revive"), start=250):
        row[f"special_{name}"] = u8(record, offset)
    return row


def export_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {}

    item_file = (SOURCE / "item_proto").read_bytes()
    magic, version, stride, count, object_size = struct.unpack_from("<4sIIII", item_file)
    if magic != b"MIPX" or version != 1 or stride != 156:
        raise ValueError(f"unexpected item header: {magic!r}, version={version}, stride={stride}")
    item_raw, item_object = unpack_crypted_object(item_file[20:20 + object_size], ITEM_KEY)
    if len(item_raw) != count * stride:
        raise ValueError("item record count mismatch")
    (OUT / "item_proto-records.bin").write_bytes(item_raw)
    item_rows = [parse_item(item_raw[i:i + stride]) for i in range(0, len(item_raw), stride)]
    export_csv(OUT / "item_proto.csv", item_rows)
    report["item_proto"] = {"version": version, "stride": stride, "records": count, **item_object}

    mob_file = (SOURCE / "mob_proto").read_bytes()
    magic, count, object_size = struct.unpack_from("<4sII", mob_file)
    if magic != b"MMPT":
        raise ValueError(f"unexpected mob header: {magic!r}")
    mob_raw, mob_object = unpack_crypted_object(mob_file[12:12 + object_size], MOB_KEY)
    stride = len(mob_raw) // count
    if stride != 255 or len(mob_raw) != count * stride:
        raise ValueError(f"unexpected mob stride {stride}")
    (OUT / "mob_proto-records.bin").write_bytes(mob_raw)
    mob_rows = [parse_mob(mob_raw[i:i + stride]) for i in range(0, len(mob_raw), stride)]
    export_csv(OUT / "mob_proto.csv", mob_rows)
    report["mob_proto"] = {"stride": stride, "records": count, **mob_object, "parsed_fields": "full 255-byte client layout"}

    (OUT / "proto-extraction-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
