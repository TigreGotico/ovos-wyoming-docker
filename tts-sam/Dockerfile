ARG TAG=latest
FROM jarbasai/ovos-wyoming-base:${TAG}

ARG BUILD_DATE=unknown
ARG VERSION=unknown

ARG ALPHA=true
ARG USER=ovos

SHELL ["/bin/bash", "-c"]

WORKDIR /home/${USER}

USER root

RUN apt-get update \
    && apt-get install -y libsdl1.2-dev \
    && rm -rf /var/lib/apt /var/log/{apt,dpkg.log}

USER $USER

ENV PATH /home/${USER}/.venv/bin:$PATH
ENV VIRTUAL_ENV /home/${USER}/.venv

RUN pip3 install /opt/wyoming/wyoming-ovos-tts

RUN pip3 install aiohttp \
  && if [ "${ALPHA}" == "true" ]; then \
  pip3 install SpeechRecognition git+https://github.com/OpenVoiceOS/ovos-tts-plugin-SAM --pre; \
  else \
  pip3 install SpeechRecognition ovos-tts-plugin-SAM; \
  fi \
  && mkdir -p /home/${USER}/.cache/mycroft/SAMTTS \
  && rm -rf /home/${USER}/.cache/pip


ENTRYPOINT wyoming-ovos-tts --uri tcp://0.0.0.0:8080 --plugin-name ovos-tts-plugin-SAM

EXPOSE 8080
