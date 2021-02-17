# WHITEBOARD

POC for the online whiteboard project

## Installation

### Requirements

* MariaDB server
* nodejs
* python 3.5


#### MariaDB

Open mysql console and run the following:

`CREATE DATABASE whiteboard_db;`

`CREATE USER 'whiteboard'@'localhost' IDENTIFIED BY 'wh!t3b0@rd';`

`GRANT ALL PRIVILEGES ON whiteboard_db . * TO 'whiteboard'@'localhost';`

`FLUSH privileges;`

#### Backend

In the root directory of the project:

`mkdir instance`

`touch instance/config.py`

Edit `instance/config.py` and add the following:

```
SECRET_KEY = 'asdasd'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://whiteboard:wh!t3b0@rd@localhost/whiteboard_db'

GOOGLE_ID = ''
GOOGLE_SECRET = ''

TOKEN_SECRET = 'asdasd'

HOST = "http://lvh.me:8081/"

B_DATA_FILES_DIR = '/home/peio/src/whiteboard/b_data'

BASIC_AUTH_USERNAME = 'john'
BASIC_AUTH_PASSWORD = '1'

####  Email settings   ####

FROM_ADDR = "whiteboard.me.team@gmail.com"
EMAIL_PASS = "wh1tebo@rd"
SMTP_SERVER = "smtp.gmail.com"
SMTP_SERVER_PORT = 587
```

Set GOOGLE_ID and GOOGLE_SECRET with valid ones

Optionally create virtualenv for the project.

Install backend dependencies with:

`pip install -r requirements.txt`

Set the following environment variables:

`export FLASK_CONFIG=development FLASK_APP=run.py`

Create dabase tables:

`flask db upgrade`

And run the backend server with:

`flask run --host=lvh.me`

#### Client

Go into `client` directory

`touch src/config.json`

In `src/config.json` add the following:
```
{
  "apiHost": "http://lvh.me:5000",
  "google": {
    "clientId": ""
  }
}
```

And set a valid `clientId`

Install the client dependecies with:

`npm install`

Run the client server with:

`env HOST=lvh.me npm run dev`

Open `http://lvh.me:8081` in a browser
