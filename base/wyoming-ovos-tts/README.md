
# Wyoming OVOS TTS Bridge

expose OVOS TTS plugins via wyoming for usage with the voice pee

![image](https://github.com/user-attachments/assets/67808db8-1c45-4ba7-bae6-4659dfdeac4e)

## Usage

```bash
$ wyoming-ovos-tts --help
usage: wyoming-ovos-tts [-h] --plugin-name PLUGIN_NAME --uri URI [--debug] [--log-format LOG_FORMAT] [--version]

options:
  -h, --help            show this help message and exit
  --plugin-name PLUGIN_NAME
                        OVOS STT plugin to load, corresponds to what you would put under "module" in mycroft.conf
  --uri URI             unix:// or tcp://
  --debug               Log DEBUG messages
  --log-format LOG_FORMAT
                        Format for log messages
  --version             Print version and exit

```

e.g.  to use the ovos public servers

> wyoming-ovos-tts --uri tcp://0.0.0.0:7892 --debug --plugin-name ovos-tts-plugin-server

plugin config is read from mycroft.conf


example logs with public OVOS servers
```bash
DEBUG:root:Namespace(plugin_name='ovos-tts-plugin-server', uri='tcp://0.0.0.0:7892', debug=True)
INFO:root:Ready
2025-04-09 15:14:07.226 - OVOS - ovos_plugin_manager.tts:create:162 - INFO - Found plugin ovos-tts-plugin-server
2025-04-09 15:14:07.227 - OVOS - ovos_plugin_manager.tts:create:166 - INFO - Loaded plugin ovos-tts-plugin-server
DEBUG:root:Client connected: 356048323844881
DEBUG:root:Synthesize(text='Hello. How can I assist?', voice=SynthesizeVoice(name='ovos-tts-plugin-server', language=None, speaker=None))
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): pipertts.ziggyai.online:443
2025-04-09 15:14:11.081 - OVOS - ovos_plugin_manager.utils.tts_cache:load_persistent_cache:263 - INFO - Persistent TTS cache files loaded successfully.
DEBUG:urllib3.connectionpool:https://pipertts.ziggyai.online:443 "GET /v2/synthesize?lang=en-US&utterance=Hello.+How+can+I+assist%3F HTTP/1.1" 200 62508
DEBUG:root:Got 62508 byte(s) of WAV data
DEBUG:root:Client disconnected: 356048323844881
```
