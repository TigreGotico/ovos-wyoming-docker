import logging

from speech_recognition import AudioData
from wyoming.asr import Transcribe, Transcript
from wyoming.audio import AudioChunk, AudioChunkConverter, AudioStop
from wyoming.event import Event
from wyoming.info import Describe, Info
from wyoming.server import AsyncEventHandler
from ovos_plugin_manager.templates.stt import STT

_LOGGER = logging.getLogger(__name__)


class STTAPIEventHandler(AsyncEventHandler):
    """Event handler for STT"""

    def __init__(
            self,
            wyoming_info: Info,
            stt: STT,
            *args,
            **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.stt = stt
        self.wyoming_info_event = wyoming_info.event()
        self.audio = bytes()
        self.audio_converter = AudioChunkConverter(
            rate=16000,
            width=2,
            channels=1,
        )

    def handle_audio_chunk(self, event: Event) -> None:
        chunk = AudioChunk.from_event(event)
        chunk = self.audio_converter.convert(chunk)
        self.audio += chunk.audio

    async def handle_stt(self, audio: bytes) -> str:
        audio = AudioData(audio, sample_rate=self.audio_converter.rate,
                          sample_width=self.audio_converter.width)
        text = self.stt.execute(audio)
        return text

    async def handle_audio_end(self, text: str) -> None:
        await self.write_event(Transcript(text=text).event())
        _LOGGER.debug("Completed request")
        # Reset
        self.audio = bytes()

    async def handle_event(self, event: Event) -> bool:
        if AudioChunk.is_type(event.type):
            if not self.audio:
                _LOGGER.debug("Receiving audio")
            self.handle_audio_chunk(event)
            return True

        if AudioStop.is_type(event.type):
            text = await self.handle_stt(self.audio)
            _LOGGER.info(text)
            await self.handle_audio_end(text)
            return False

        if Transcribe.is_type(event.type):
            _LOGGER.debug("Transcribe event")
            return True

        if Describe.is_type(event.type):
            await self.write_event(self.wyoming_info_event)
            _LOGGER.debug("Sent info")
            return True

        return True
