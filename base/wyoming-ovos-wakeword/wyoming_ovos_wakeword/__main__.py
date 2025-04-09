#!/usr/bin/env python3
import argparse
import asyncio
import logging
import time
from functools import partial
from pathlib import Path
from typing import List, Dict, Optional

from ovos_config import Configuration
from ovos_plugin_manager.templates.hotwords import HotWordEngine
from ovos_plugin_manager.wakewords import OVOSWakeWordFactory
from wyoming.audio import AudioChunk, AudioChunkConverter, AudioStart, AudioStop
from wyoming.event import Event
from wyoming.info import Attribution, Describe, Info, WakeModel, WakeProgram
from wyoming.server import AsyncEventHandler, AsyncServer, AsyncTcpServer
from wyoming.wake import Detect, Detection, NotDetected

_LOGGER = logging.getLogger()
_DIR = Path(__file__).parent


async def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri", default="stdio://", help="unix:// or tcp://")
    #
    parser.add_argument(
        "--zeroconf",
        nargs="?",
        const="ovos-ww-plugin",
        help="Enable discovery over zeroconf with optional name (default: ovos-ww-plugin)",
    )
    #
    parser.add_argument("--debug", action="store_true", help="Log DEBUG messages")
    parser.add_argument(
        "--log-format", default=logging.BASIC_FORMAT, help="Format for log messages"
    )
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO, format=args.log_format
    )
    _LOGGER.debug(args)

    default_ww = Configuration().get("listener", {}).get("wake_word", "hey_mycroft")
    models: Dict[str, HotWordEngine] = {default_ww: OVOSWakeWordFactory.create_hotword(default_ww)}

    _LOGGER.info("Ready")

    # Start server
    server = AsyncServer.from_uri(args.uri)

    if args.zeroconf:
        if not isinstance(server, AsyncTcpServer):
            raise ValueError("Zeroconf requires tcp:// uri")

        from wyoming.zeroconf import register_server

        tcp_server: AsyncTcpServer = server
        await register_server(
            name=args.zeroconf, port=tcp_server.port, host=tcp_server.host
        )
        _LOGGER.debug("Zeroconf discovery enabled")

    try:
        await server.run(partial(OVOSWakeWordEventHandler,
                                 args, default_ww, models,))
    except KeyboardInterrupt:
        pass


# -----------------------------------------------------------------------------


class OVOSWakeWordEventHandler(AsyncEventHandler):
    """Event handler for clients."""

    def __init__(
            self,
            cli_args: argparse.Namespace,
            default_ww: str,
            models: Dict[str, HotWordEngine],
            *args,
            **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.cli_args = cli_args
        self.client_id = str(time.monotonic_ns())
        self.converter = AudioChunkConverter(rate=16000, width=2, channels=1)
        self.default_ww = default_ww
        self.models = models

        self.active_detectors: List[str] = [self.default_ww]

        self._detection: bool = False

        _LOGGER.debug("Client connected: %s", self.client_id)

    async def load_wakewords(self, names: Optional[List[str]] = None) -> None:
        names = names or self.active_detectors
        ww_definitions = Configuration().get("hotwords", {})
        for ww_name in names:
            ww_name = ww_name.replace(" ", "_")
            if ww_name in self.models:
                continue
            if ww_name not in ww_definitions:
                raise ValueError(f"Unknown hotword {ww_name}")
            self.models[ww_name] = OVOSWakeWordFactory.create_hotword(ww_name)
            _LOGGER.debug(f"Loaded model: {ww_name}")

    async def handle_event(self, event: Event) -> bool:
        if Describe.is_type(event.type):
            wyoming_info = self._get_info()
            await self.write_event(wyoming_info.event())
            _LOGGER.debug("Sent info to client: %s", self.client_id)
            return True

        if Detect.is_type(event.type):
            detect = Detect.from_event(event)
            if detect.names:
                self.active_detectors = detect.names
                # load requested ww models if needed
                await self.load_wakewords(detect.names)

        elif AudioStart.is_type(event.type):
            # reset states to prepare for new detection
            self._detection = False
            self.active_detectors = self.active_detectors or [self.default_ww]
            await self.load_wakewords()  # if needed
            for name in self.active_detectors:
                self.models[name].reset()

        elif AudioChunk.is_type(event.type):
            chunk = self.converter.convert(AudioChunk.from_event(event))
            for wake_word in self.active_detectors:
                detector = self.models[wake_word]
                detector.update(chunk.audio)
                if detector.found_wake_word(None):  # pass None for legacy reasons before plugins supported streaming
                    _LOGGER.debug(
                        f"Detected {wake_word} from client {self.client_id}"
                    )
                    await self.write_event(
                        Detection(name=wake_word, timestamp=chunk.timestamp).event()
                    )
                    self._detection = True

        elif AudioStop.is_type(event.type):
            # Inform client if not detections occurred
            if not self._detection:
                # No wake word detections
                await self.write_event(NotDetected().event())
                _LOGGER.debug(
                    f"Audio stopped without detection from client: {self.client_id}"
                )
        else:
            _LOGGER.debug(f"Unexpected event: type={event.type}, data={event.data}")

        return True

    async def disconnect(self) -> None:
        _LOGGER.debug("Client disconnected: %s", self.client_id)

    def _get_info(self) -> Info:
        return Info(
            wake=[
                WakeProgram(
                    name="ovos-wakeword-plugins",
                    description="wake word detection via OpenVoiceOS plugins",
                    attribution=Attribution(
                        name="TigreGótico",
                        url="https://github.com/TigreGotico"
                    ),
                    installed=True,
                    version="0.0.1",
                    models=[
                        WakeModel(
                            name=ww_name,
                            description=f"wake-word detection via {ww_cfg['module']}",
                            phrase=ww_name.replace("_", " ").title(),
                            attribution=Attribution(
                                name="OpenVoiceOS",
                                url="https://github.com/OpenVoiceOS/ovos-plugin-manager"
                            ),
                            installed=True,
                            languages=[ww_cfg.get("lang", Configuration().get("lang", "en"))],
                            version="0.0.1",
                        )
                        for ww_name, ww_cfg in Configuration().get("hotwords", {}).items()
                    ],
                )
            ],
        )


# -----------------------------------------------------------------------------


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
