"""Local-only educational protocol observer and minimal login-failure emulator."""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import dataclass
import json
import logging
import secrets
import time

from protocol import (
    PHASE_HANDSHAKE,
    PHASE_LOGIN,
    StreamDecoder,
    describe,
    handshake_packet,
    login_failure_packet,
    phase_packet,
)


LOG = logging.getLogger("metin2mobile-emulator")


@dataclass
class ServerConfig:
    host: str = "127.0.0.1"
    auth_port: int = 11002
    game_port: int = 12002
    mode: str = "observe"


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, role: str, config: ServerConfig) -> None:
    peer = writer.get_extra_info("peername")
    decoder = StreamDecoder(PHASE_HANDSHAKE)
    LOG.info("connection role=%s peer=%s", role, peer)

    if config.mode == "login-failure" and role == "auth":
        token = secrets.randbits(32)
        now_ms = int(time.time() * 1000) & 0xFFFFFFFF
        writer.write(handshake_packet(token, now_ms))
        await writer.drain()
        LOG.info("sent HANDSHAKE token=%08x", token)

    try:
        while data := await reader.read(8192):
            parsed_any = False
            for spec, packet in decoder.feed(data):
                parsed_any = True
                event = describe(packet, decoder.phase)
                # Avoid printing recovered credentials unless explicitly debugging.
                if "password" in event:
                    event["password"] = "<redacted>"
                LOG.info("packet %s", json.dumps(event, ensure_ascii=False))

                if config.mode == "login-failure" and role == "auth":
                    if spec.name == "HANDSHAKE":
                        writer.write(phase_packet(PHASE_LOGIN))
                        await writer.drain()
                        decoder.set_phase(PHASE_LOGIN)
                        LOG.info("sent PHASE_LOGIN")
                    elif spec.name in {"LOGIN", "LOGIN_NEW", "DIRECT_ENTER"}:
                        writer.write(login_failure_packet())
                        await writer.drain()
                        LOG.info("sent LOGIN_FAILURE status=WRONGPWD")

            if not parsed_any and decoder.buffer and decoder.buffer[0] not in {0xFF, 0xFE, 0xFB}:
                LOG.warning("unframed phase=%d bytes=%s", decoder.phase, bytes(decoder.buffer).hex(" "))
                decoder.buffer.clear()
    except (ConnectionError, asyncio.CancelledError):
        pass
    finally:
        writer.close()
        await writer.wait_closed()
        LOG.info("disconnected role=%s peer=%s", role, peer)


async def run(config: ServerConfig) -> None:
    async def auth_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        await handle_client(reader, writer, "auth", config)

    async def game_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        await handle_client(reader, writer, "game", config)

    auth = await asyncio.start_server(auth_handler, config.host, config.auth_port)
    game = await asyncio.start_server(game_handler, config.host, config.game_port)
    sockets = [sock.getsockname() for sock in (*auth.sockets, *game.sockets)]
    LOG.info("listening %s mode=%s", sockets, config.mode)
    async with auth, game:
        await asyncio.gather(auth.serve_forever(), game.serve_forever())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="bind address; localhost is the safe default")
    parser.add_argument("--auth-port", type=int, default=11002)
    parser.add_argument("--game-port", type=int, default=12002)
    parser.add_argument("--mode", choices=("observe", "login-failure"), default="observe")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        asyncio.run(run(ServerConfig(args.host, args.auth_port, args.game_port, args.mode)))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
