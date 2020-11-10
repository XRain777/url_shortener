# Django URL shortener

## Installation

Run:
```
docker build -f Dockerfile -t url_shortener_uwsgi url_shortener/
docker run --name url_shortener -d -p 8080:8080 url_shortener_uwsgi
```

In NGINX config use:
```
uwsgi_pass 127.0.0.1:8080;
```

## Demo

See at http://s.xrain.ru/
