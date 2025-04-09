ARG TAG=latest
FROM jarbasai/ovos-wyoming-base:${TAG}

ARG BUILD_DATE=unknown
ARG VERSION=unknown

ARG ALPHA=true
ARG USER=ovos

SHELL ["/bin/bash", "-c"]

WORKDIR /home/${USER}

USER root

RUN apt-get update && apt-get install -y curl  \
    && curl -sS https://forslund.github.io/mycroft-desktop-repo/mycroft-desktop.gpg.key | gpg --dearmor -o /etc/apt/trusted.gpg.d/mimic.gpg \
    && echo "deb http://forslund.github.io/mycroft-desktop-repo bionic main" | tee -a /etc/apt/sources.list.d/mimic.list \
    && apt-get update \
    && apt-get install -y mimic \
    && mkdir -p /home/${USER}/.cache/mycroft/MimicTTSPlugin \
    && chown ${USER}:${USER} -R /home/${USER} \
    && apt-get --purge autoremove -y \
    && apt-get clean \
    && rm -rf /home/${USER}/.cache/pip /var/lib/apt /var/log/{apt,dpkg.log}

USER $USER

ENV PATH /home/${USER}/.venv/bin:$PATH
ENV VIRTUAL_ENV /home/${USER}/.venv

RUN pip3 install /opt/wyoming/wyoming-ovos-tts

RUN pip3 install aiohttp \
  && if [ "${ALPHA}" == "true" ]; then \
  pip3 install SpeechRecognition git+https://github.com/OpenVoiceOS/ovos-tts-plugin-mimic --pre; \
  else \
  pip3 install SpeechRecognition ovos-tts-plugin-mimic; \
  fi \
  && rm -rf ${HOME}/.cache


ENTRYPOINT wyoming-ovos-tts --uri tcp://0.0.0.0:8080 --plugin-name ovos-tts-plugin-mimic

EXPOSE 8080
