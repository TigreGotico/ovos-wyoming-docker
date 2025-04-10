# OVOS Wyoming Docker

![image](https://github.com/user-attachments/assets/e8d0a736-372a-47a5-9a11-3a92fbf88810)

## Build

either run `build.sh` or `docker compose build`

## Compose

adjust to your liking

```
services:
  ovos-assist-agent:
    image: ovos-persona/ovos-core
    restart: always
    container_name: ovos_core_persona
    # network_mode: host in order to be able to connect to the bus
    network_mode: host
    #ports:
    #  - 8337:8337
    
  wyoming-ovos-tts-servers:
    build:
      context: ./tts-servers
      dockerfile: Dockerfile
    image: jarbasai/ovos-wyoming-tts-servers:latest
    container_name: wyoming-ovos-tts-servers
    restart: unless-stopped
    volumes:
      - ${CONFIG_BASE_DIR}/mycroft.conf:/etc/mycroft/mycroft.conf
    ports:
      - 10600:8080
  wyoming-ovos-stt-servers:
    build:
      context: ./stt-servers
      dockerfile: Dockerfile
    image: jarbasai/ovos-wyoming-stt-servers:latest
    container_name: wyoming-ovos-stt-servers
    restart: unless-stopped
    volumes:
      - ${CONFIG_BASE_DIR}/mycroft.conf:/etc/mycroft/mycroft.conf
    ports:
      - 10501:8080
  wyoming-ovos-chromium-stt:
    build:
      context: ./stt-chromium
      dockerfile: Dockerfile
    image: jarbasai/ovos-wyoming-chromium:latest
    container_name: wyoming-ovos-chromium-stt
    restart: unless-stopped
    volumes:
      - ${CONFIG_BASE_DIR}/mycroft.conf:/etc/mycroft/mycroft.conf
    ports:
      - 10500:8080
  wyoming-ovos-wakewords:
    build:
      context: ./ww
      dockerfile: Dockerfile
    container_name: wyoming-ovos-wakewords
    image: jarbasai/ovos-wyoming-wakewords:latest
    volumes:
      - ${CONFIG_BASE_DIR}/mycroft.conf:/etc/mycroft/mycroft.conf
    ports:
      - 10900:8080
```
