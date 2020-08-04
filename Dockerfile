FROM python:3

LABEL maintainer="uicode.fr"

ENV APPLICATION_ROOT /
ENV FLASK_SECRET_KEY flask_secret_key
ENV DEMO_WEATHER_API_KEY demo_weather_api_key

RUN pip install gunicorn pydantic && \
  mkdir /log && mkdir /db

VOLUME /log
VOLUME /db

EXPOSE 8000

COPY pyscriptdeck pyscriptdeck
COPY pyscriptdemo pyscriptdemo
COPY logging.conf logging.conf
COPY config.yml config.yml
COPY requirements.txt requirements.txt
COPY setup.py setup.py
COPY conf/entrypoint.sh entrypoint.sh

RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
