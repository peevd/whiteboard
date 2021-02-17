# Use an official Python runtime as a parent image
FROM python:3.7.3-alpine3.9

# Set the working directory to /app
WORKDIR /present_handler

# Create dir for storing presentations (attached to a volume)
RUN mkdir /static

# Install libreoffice and supervisord

RUN apk add build-base \
    && apk add --no-cache --virtual .build-deps gcc libc-dev musl-dev \
    && apk add libreoffice nginx \
    && pip3 install --upgrade pip supervisor gunicorn eventlet

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Copy supervisord and nginx configs
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisord.conf

# Copy the code last so changes don't rebuild all layers
COPY . .
COPY instance_conf.py /present_handler/instance/config.py

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app when the container launches
ENV export LC_ALL=C.UTF-8 LANG=C.UTF-8 FLASK_CONFIG=development FLASK_APP=run.py
CMD ["supervisord"]
