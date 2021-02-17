#!/bin/sh

# todo: set up database if not already

env LC_ALL=C.UTF-8 LANG=C.UTF-8 FLASK_CONFIG=production FLASK_APP=run.py flask db upgrade

exec supervisord
