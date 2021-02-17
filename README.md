### Docker Build

#### Create configuration files

`cd config`

##### Create backend config file:

`cp server_config.default.py server_config.py`

Fill in the missing spots and save the file.

##### Create client config file:

`cp client_config.default.json client_config.json`

Fill in the missing spots and save the file.

#### Build docker image

`docker-compose build`

#### Deploy a container

`docker-compose up -d`

#### On first run

If the container is ran for the first time the database must be initialised
using the following commands:

```
docker exec -e LC_ALL=C.UTF-8 -e LANG=C.UTF-8 -e FLASK_CONFIG=production -e FLASK_APP=run.py -it whiteboard_app /bin/bash

$ flask db upgrade
$ exit
```
