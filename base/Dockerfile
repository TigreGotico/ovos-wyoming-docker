ARG TAG=latest
FROM debian:bookworm-slim

ARG ALPHA=true
ARG USER=ovos

ENV DEBIAN_FRONTEND noninteractive

SHELL ["/bin/bash", "-c"]

RUN apt-get update \
    && apt-get install -y git python3 python3-venv python3-pip \
    && c_rehash \
    && useradd --no-log-init $USER -m -c "Open Voice OS user" \
    && python3 -m venv /home/${USER}/.venv \
    && . /home/${USER}/.venv/bin/activate \
    && mkdir -p /home/${USER}/.config/mycroft /home/${USER}/.cache \
    && chown ${USER}:${USER} -R /home/${USER} \
    && apt-get --purge autoremove -y \
    && apt-get clean \
    && rm -rf ${HOME}/.cache/* /var/lib/apt /var/log/{apt,dpkg.log}


COPY wyoming-ovos-stt /opt/wyoming/wyoming-ovos-stt
COPY wyoming-ovos-tts /opt/wyoming/wyoming-ovos-tts
COPY wyoming-ovos-wakeword /opt/wyoming/wyoming-ovos-ww
RUN chown ${USER}:${USER} -R /opt/wyoming

USER $USER

ENV PATH /home/${USER}/.venv/bin:$PATH
ENV VIRTUAL_ENV /home/${USER}/.venv

WORKDIR /home/${USER}