FROM debian:9.6

WORKDIR /whiteboard_project

RUN apt-get update \
    && apt-get -y install python python-pip python3 python3-pip nginx curl git \
    && curl -sL https://deb.nodesource.com/setup_10.x | bash - \
    && apt-get -y install nodejs \
    && pip install supervisor \
    && npm i -g peer


COPY whiteboard/requirements.txt .
COPY whiteboard/client/package*.json ./client/

COPY whiteboard/config/server_config.default.py instance/config.py
COPY whiteboard/config/client_config.default.json client/src/config.json

RUN pip3 install -r requirements.txt \
    && cd client && npm install

COPY whiteboard .

RUN cd client && npm run-script build

RUN export LC_ALL=C.UTF-8 LANG=C.UTF-8 FLASK_CONFIG=production FLASK_APP=run.py
RUN mkdir /b_data

COPY config/nginx.conf /etc/nginx/nginx.conf
COPY whiteboard/config/supervisord.conf /etc/supervisord.conf

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

STOPSIGNAL SIGTERM

CMD ["/start.sh"]
