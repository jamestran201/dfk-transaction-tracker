FROM python:3.8-buster as common_build

WORKDIR /dfk_transaction_tracker/

COPY ./docker_build/requirements.txt ./requirements.txt

RUN pip install --requirement requirements.txt

FROM common_build as celery_build

COPY . .

ENTRYPOINT ["scripts/celery-start.sh"]
