FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8000

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT 