

docker build -f base/Dockerfile -t jarbasai/ovos-wyoming-base:latest ./base

docker build -f stt-chromium/Dockerfile -t jarbasai/ovos-wyoming-chromium:latest ./stt-chromium
docker build -f stt-servers/Dockerfile -t jarbasai/ovos-wyoming-stt-servers:latest ./stt-servers

docker build -f tts-servers/Dockerfile -t jarbasai/ovos-wyoming-tts-servers:latest ./tts-servers

docker build -f ww/Dockerfile -t jarbasai/ovos-wyoming-wakewords:latest ./ww
