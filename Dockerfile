FROM python:3.7
COPY ./ app
# copy from my current directory to a location called app
# base image contains app folder containing our files
WORKDIR /app
RUN pip install -r requirements.txt
#this is to install dependencies
EXPOSE $PORT
#port for accessing the url
# $PORT is a placeholder i.em automatically port assignment
CMD gunicorn --workers=1 --bind 0.0.0.0:$PORT app:app --timeout 600
# workers will divide work based on no of request instances
# binding the port to local host of render and port placeholder
# app.py is the app to be run app:app


