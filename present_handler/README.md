# PRESENTATION_HANDLER_SERVER

## Installation

### Requirements

* python 3.5


In the root directory of the project check, is directory "instance" there:

If Not:

`mkdir instance`

`touch instance/config.py`

Edit `instance/config.py` and add the following:

```
PRESENT_DIR = "/home/peio_jr/projects/whiteboard_project/whiteboard/static/presentations/"

ALLOWED_EXTENSIONS = set(["ppt", "otp", "odp"])
```


Optionally create virtualenv for the project.

Install backend dependencies with:

`pip install -r requirements.txt`

Set the following environment variables:

`export FLASK_CONFIG=development FLASK_APP=run.py`

And run the backend server with:

`flask run --port=5500`

