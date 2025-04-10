ARG IMAGE=python:3-slim-bookworm
FROM ${IMAGE}
ARG IMAGE

COPY ./requirements.txt/ requirements.txt
RUN pip install -r requirements.txt

COPY ./persona.json/ persona.json

CMD ["ovos-persona-server", "--persona", "persona.json"]
