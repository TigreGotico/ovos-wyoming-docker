ARG TAG=latest
FROM jarbasai/ovos-wyoming-base:${TAG}

ARG BUILD_DATE=unknown
ARG VERSION=unknown

ARG ALPHA=true
ARG USER=ovos

SHELL ["/bin/bash", "-c"]

WORKDIR /home/${USER}

USER $USER

ENV PATH /home/${USER}/.venv/bin:$PATH
ENV VIRTUAL_ENV /home/${USER}/.venv

RUN pip3 install /opt/wyoming/wyoming-ovos-tts

RUN pip3 install aiohttp \
  && if [ "${ALPHA}" == "true" ]; then \
  pip3 install SpeechRecognition ovos-tts-plugin-google-tx --pre; \
  else \
  pip3 install SpeechRecognition ovos-tts-plugin-google-tx; \
  fi \
  && rm -rf ${HOME}/.cache

ENTRYPOINT wyoming-ovos-tts --uri tcp://0.0.0.0:8080 --plugin-name ovos-tts-plugin-google-tx

EXPOSE 8080
