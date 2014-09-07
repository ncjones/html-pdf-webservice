FROM openlabs/docker-wkhtmltopdf:latest
MAINTAINER Sharoon Thomas <sharoon.thomas@openlabs.co.in>

# Install dependencies for running web service
RUN apt-get install -y python-pip
RUN pip install werkzeug executor gunicorn

ADD app.py /app.py
ADD config.py /config.py

EXPOSE 80

ENTRYPOINT ["usr/local/bin/gunicorn"]

# Show the extended help
CMD ["-c", "/config.py", "app:application"]
