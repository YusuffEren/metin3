from __future__ import annotations

import struct
import unittest

from protocol import (
    PHASE_HANDSHAKE,
    PHASE_LOGIN,
    StreamDecoder,
    describe,
    handshake_packet,
    login_failure_packet,
    phase_packet,
)


class ProtocolTests(unittest.TestCase):
    def test_handshake_layout(self) -> None:
        packet = handshake_packet(0x11223344, 0x55667788, -7)
        self.assertEqual(13, len(packet))
        self.assertEqual((0xFF, 0x11223344, 0x55667788, -7), struct.unpack("<BIIi", packet))

    def test_phase_layout(self) -> None:
        self.assertEqual(b"\xfd\x02", phase_packet(PHASE_LOGIN))

    def test_login_failure_layout(self) -> None:
        packet = login_failure_packet("WRONGPWD")
        self.assertEqual(10, len(packet))
        self.assertEqual(b"\x07WRONGPWD\x00", packet)

    def test_fragmented_login_decode(self) -> None:
        raw = b"\x01" + b"demo\x00".ljust(31, b"\x00") + b"secret\x00".ljust(17, b"\x00")
        self.assertEqual(49, len(raw))
        decoder = StreamDecoder(PHASE_LOGIN)
        self.assertEqual([], list(decoder.feed(raw[:9])))
        packets = list(decoder.feed(raw[9:]))
        self.assertEqual(1, len(packets))
        spec, packet = packets[0]
        self.assertEqual("LOGIN", spec.name)
        parsed = describe(packet, PHASE_LOGIN)
        self.assertEqual("demo", parsed["login"])
        self.assertEqual("secret", parsed["password"])

    def test_two_packets_in_one_read(self) -> None:
        packet = handshake_packet(1, 2)
        decoder = StreamDecoder(PHASE_HANDSHAKE)
        decoded = list(decoder.feed(packet + packet))
        self.assertEqual(2, len(decoded))


if __name__ == "__main__":
    unittest.main()
