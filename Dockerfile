FROM python:3.12

RUN apt-get update \
    && apt-get install -y \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

COPY .env /app/.env

ENV DJANGO_SETTINGS_MODULE=bugutest.settings
ENV PYTHONUNBUFFERED 1

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "bugutest.wsgi:application"]
