# Django URL Shortener
#
# VERSION               1.0

FROM python:3.8-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache python3-dev build-base linux-headers pcre-dev
WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py migrate

EXPOSE 8080
CMD ["uwsgi", "--ini", "uwsgi.ini"]
#CMD    ["x11vnc", "-forever", "-usepw", "-create"]