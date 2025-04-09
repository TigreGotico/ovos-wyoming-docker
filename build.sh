

docker build -f base/Dockerfile -t jarbasai/ovos-wyoming-base:latest ./base

docker build -f stt-chromium/Dockerfile -t jarbasai/ovos-wyoming-chromium:latest ./stt-chromium
docker build -f stt-servers/Dockerfile -t jarbasai/ovos-wyoming-stt-servers:latest ./stt-servers

docker build -f tts-servers/Dockerfile -t jarbasai/ovos-wyoming-tts-servers:latest ./tts-servers
docker build -f tts-matxa/Dockerfile -t jarbasai/ovos-wyoming-tts-matxa:latest ./tts-matxa
docker build -f tts-google-tx/Dockerfile -t jarbasai/ovos-wyoming-tts-google-tx:latest ./tts-google-tx
docker build -f tts-mimic/Dockerfile -t jarbasai/ovos-wyoming-tts-mimic:latest ./tts-mimic
docker build -f tts-nos/Dockerfile -t jarbasai/ovos-wyoming-tts-nos:latest ./tts-nos
docker build -f tts-sam/Dockerfile -t jarbasai/ovos-wyoming-tts-sam:latest ./tts-sam


docker build -f ww/Dockerfile -t jarbasai/ovos-wyoming-wakewords:latest ./ww
