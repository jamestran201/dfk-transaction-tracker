FROM python:3.8-buster as common_build

WORKDIR /dfk_transaction_tracker/

COPY ./docker_build/requirements.txt ./requirements.txt

RUN pip install --requirement requirements.txt

COPY . .

FROM common_build as celery_build

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENTRYPOINT ["scripts/start-celery.sh"]

FROM common_build as app_build

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENTRYPOINT ["scripts/start-django-prod.sh"]
