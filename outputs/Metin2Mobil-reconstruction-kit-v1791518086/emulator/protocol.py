"""Small, dependency-free subset of the reconstructed wire protocol.

Only facts verified in the decompiled client are encoded here.  The production
client's optional key-agreement/cipher and sequence layer is intentionally not
implemented yet; see ../protocol/PROTOCOL-NOTES.md.
"""

from __future__ import annotations

from dataclasses import dataclass
import struct
from typing import Iterator


PHASE_OFFLINE = 0
PHASE_HANDSHAKE = 1
PHASE_LOGIN = 2
PHASE_SELECT = 3
PHASE_LOADING = 4
PHASE_GAME = 5


@dataclass(frozen=True)
class PacketSpec:
    phase: int | None
    header: int
    size: int
    name: str


# Client-to-server fixed-length packets used by the emulator/observer.
C2S_SPECS = (
    PacketSpec(PHASE_HANDSHAKE, 0xFF, 13, "HANDSHAKE"),
    PacketSpec(None, 0xFE, 1, "PONG"),
    PacketSpec(PHASE_HANDSHAKE, 0xFB, 261, "KEY_AGREEMENT"),
    PacketSpec(PHASE_LOGIN, 0x01, 49, "LOGIN"),
    PacketSpec(PHASE_LOGIN, 0x6D, 52, "LOGIN_NEW"),
    PacketSpec(PHASE_LOGIN, 0x09, 50, "DIRECT_ENTER"),
    PacketSpec(PHASE_LOGIN, 0xC9, 6, "RUNUP_MATRIX_ANSWER"),
    PacketSpec(PHASE_LOGIN, 0xCA, 10, "PASSPOD_ANSWER"),
    PacketSpec(PHASE_LOGIN, 0x6C, 10, "CHINA_MATRIX_CARD"),
    PacketSpec(PHASE_SELECT, 0x5A, 2, "SELECT_EMPIRE"),
    PacketSpec(PHASE_SELECT, 0x06, 2, "SELECT_CHARACTER"),
    PacketSpec(PHASE_SELECT, 0x05, 10, "DESTROY_CHARACTER"),
    PacketSpec(PHASE_SELECT, 0x04, 34, "CREATE_CHARACTER"),
    PacketSpec(PHASE_SELECT, 0x6A, 27, "CHANGE_NAME"),
    PacketSpec(PHASE_LOADING, 0x0A, 1, "ENTER_GAME"),
    PacketSpec(PHASE_GAME, 0x02, 8, "ATTACK"),
    PacketSpec(PHASE_GAME, 0x0F, 5, "ITEM_PICKUP"),
    PacketSpec(PHASE_GAME, 0x3C, 7, "ITEM_USE_TO_ITEM"),
    PacketSpec(PHASE_GAME, 0x0C, 8, "ITEM_DROP"),
    PacketSpec(PHASE_GAME, 0x14, 10, "ITEM_DROP_NEW"),
    PacketSpec(PHASE_GAME, 0x15, 4, "ITEM_DELETE"),
    PacketSpec(PHASE_GAME, 0x16, 4, "ITEM_SELL"),
    PacketSpec(PHASE_GAME, 0x0D, 9, "ITEM_MOVE"),
)


def _cstring(data: bytes) -> str:
    return data.split(b"\0", 1)[0].decode("utf-8", errors="replace")


def find_spec(phase: int, header: int) -> PacketSpec | None:
    exact = next((item for item in C2S_SPECS if item.phase == phase and item.header == header), None)
    if exact:
        return exact
    return next((item for item in C2S_SPECS if item.phase is None and item.header == header), None)


def describe(packet: bytes, phase: int) -> dict[str, object]:
    if not packet:
        raise ValueError("empty packet")
    spec = find_spec(phase, packet[0])
    result: dict[str, object] = {
        "header": f"0x{packet[0]:02X}",
        "size": len(packet),
        "name": spec.name if spec else "UNKNOWN",
        "raw_hex": packet.hex(" "),
    }
    if packet[0] == 0xFF and len(packet) == 13:
        _, token, time_ms, delta = struct.unpack("<BIIi", packet)
        result.update(handshake=token, time_ms=time_ms, delta=delta)
    elif packet[0] == 0x01 and len(packet) == 49:
        result.update(login=_cstring(packet[1:32]), password=_cstring(packet[32:49]))
    elif packet[0] == 0x6D and len(packet) == 52:
        result.update(login=_cstring(packet[1:32]), login_key=struct.unpack_from("<I", packet, 32)[0])
    elif packet[0] == 0x09 and len(packet) == 50:
        result.update(login=_cstring(packet[1:32]), password=_cstring(packet[32:49]), slot=packet[49])
    elif packet[0] in (0x5A, 0x06) and len(packet) == 2:
        result["value"] = packet[1]
    elif packet[0] in (0x0F,) and len(packet) == 5:
        result["vid"] = struct.unpack_from("<I", packet, 1)[0]
    elif packet[0] == 0x02 and len(packet) == 8:
        result.update(attack_type=packet[1], victim_vid=struct.unpack_from("<I", packet, 2)[0])
    return result


class StreamDecoder:
    """Incremental fixed-length packet decoder scoped to the current phase."""

    def __init__(self, phase: int = PHASE_HANDSHAKE):
        self.phase = phase
        self.buffer = bytearray()

    def set_phase(self, phase: int) -> None:
        self.phase = phase

    def feed(self, data: bytes) -> Iterator[tuple[PacketSpec, bytes]]:
        self.buffer.extend(data)
        while self.buffer:
            spec = find_spec(self.phase, self.buffer[0])
            if spec is None:
                # Unknown framing cannot be recovered safely without the full
                # phase-specific length table.  Let the caller log the tail.
                return
            if len(self.buffer) < spec.size:
                return
            packet = bytes(self.buffer[:spec.size])
            del self.buffer[:spec.size]
            yield spec, packet


def handshake_packet(token: int, time_ms: int, delta: int = 0) -> bytes:
    return struct.pack("<BIIi", 0xFF, token & 0xFFFFFFFF, time_ms & 0xFFFFFFFF, delta)


def phase_packet(phase: int) -> bytes:
    if not 0 <= phase <= 5:
        raise ValueError("phase must be 0..5")
    return bytes((0xFD, phase))


def ping_packet() -> bytes:
    return b"\x2c"


def login_failure_packet(status: str = "WRONGPWD") -> bytes:
    payload = status.encode("ascii", errors="replace")[:8].ljust(9, b"\0")
    return b"\x07" + payload
