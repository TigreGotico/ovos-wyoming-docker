# 🐳 OVOS Wyoming Docker

A collection of Docker images for running [OVOS](https://openvoiceos.org) services using the [Wyoming Protocol](https://github.com/Rhasspy/wyoming).

> Easily spin up TTS, STT, and Wake Word services using Docker and Docker Compose.

![OVOS Wyoming](https://github.com/user-attachments/assets/cc5e69ae-7549-45a9-a48f-94d57d07129c)

---

## 🚀 Getting Started

### 🔧 Build the Images

You can build all images manually:

```bash
./build.sh
```

Or use Docker Compose to build:

```bash
docker compose build
```

---

## 🧩 Compose Setup

Customize your `docker-compose.yml` to fit your needs. Below is an example with multiple TTS, STT, and Wake Word services.

> **Note:** Update `${CONFIG_BASE_DIR}` to the path containing your `mycroft.conf`.

```yaml
services:
  ovos-assist-agent:
    image: ovos-persona/ovos-core
    restart: always
    container_name: ovos_core_persona
    # network_mode: host in order to be able to connect to the bus
    network_mode: host
    #ports:
    #  - 8337:8337
    
  wyoming-ovos-tts-sam:
    image: jarbasai/ovos-wyoming-tts-sam:latest
    container_name: wyoming-ovos-tts-sam
    restart: unless-stopped
    volumes:
      - ${CONFIG_BASE_DIR}/mycroft.conf:/etc/mycroft/mycroft.conf
    ports:
      - 10605:8080

  wyoming-ovos-tts-nos:
    image: jarbasai/ovos-wyoming-tts-nos:latest
    container_name: wyoming-ovos-tts-nos
    restart: unless-stopped
    volumes:
      - ${CONFIG_BASE_DIR}/mycroft.conf:/etc/mycroft/mycroft.conf
    ports:
      - 10604:8080

  wyoming-ovos-tts-mimic:
    image: jarbasai/ovos-wyoming-tts-mimic:latest
    container_name: wyoming-ovos-tts-mimic
    restart: unless-stopped
    volumes:
      - ${CONFIG_BASE_DIR}/mycroft.conf:/etc/mycroft/mycroft.conf
    ports:
      - 10603:8080

  wyoming-ovos-tts-google-tx:
    image: jarbasai/ovos-wyoming-tts-google-tx:latest
    container_name: wyoming-ovos-tts-google-tx
    restart: unless-stopped
    volumes:
      - ${CONFIG_BASE_DIR}/mycroft/mycroft.conf:/etc/mycroft/mycroft.conf
    ports:
      - 10602:8080

  wyoming-ovos-tts-matxa:
    image: jarbasai/ovos-wyoming-tts-matxa:latest
    container_name: wyoming-ovos-tts-matxa
    restart: unless-stopped
    volumes:
      - ${CONFIG_BASE_DIR}/mycroft/mycroft.conf:/etc/mycroft/mycroft.conf
    ports:
      - 10601:8080

  wyoming-ovos-tts-servers:
    image: jarbasai/ovos-wyoming-tts-servers:latest
    container_name: wyoming-ovos-tts-servers
    restart: unless-stopped
    volumes:
      - ${CONFIG_BASE_DIR}/mycroft/mycroft.conf:/etc/mycroft/mycroft.conf
    ports:
      - 10600:8080

  wyoming-ovos-stt-servers:
    image: jarbasai/ovos-wyoming-stt-servers:latest
    container_name: wyoming-ovos-stt-servers
    restart: unless-stopped
    volumes:
      - ${CONFIG_BASE_DIR}/mycroft/mycroft.conf:/etc/mycroft/mycroft.conf
    ports:
      - 10501:8080

  wyoming-ovos-chromium-stt:
    image: jarbasai/ovos-wyoming-chromium:latest
    container_name: wyoming-ovos-chromium-stt
    restart: unless-stopped
    volumes:
      - ${CONFIG_BASE_DIR}/mycroft/mycroft.conf:/etc/mycroft/mycroft.conf
    ports:
      - 10500:8080

  wyoming-ovos-wakewords:
    image: jarbasai/ovos-wyoming-wakewords:latest
    container_name: wyoming-ovos-wakewords
    restart: unless-stopped
    volumes:
      - ${CONFIG_BASE_DIR}/mycroft/mycroft.conf:/etc/mycroft/mycroft.conf
    ports:
      - 10900:8080
```

---

## 📁 Configuration

All services rely on a shared `mycroft.conf` file, typically located at:

```
/etc/mycroft/mycroft.conf
```

Set `${CONFIG_BASE_DIR}` to the base directory where your config is stored, for example:

```bash
export CONFIG_BASE_DIR=$HOME/.config/mycroft
```

---

## 🧪 Testing

Once all services are up, you can test them using a Wyoming-compatible client.

---

## 💬 Feedback & Contributions

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.
