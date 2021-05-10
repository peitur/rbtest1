FROM python:latest

RUN mkdir -p /application
COPY . /application
RUN  pip install -r /application/requirements.txt

# VOLUME ["/application¨"]

RUN pip install flask jinja2 uwsgi

## docker run -p 5000:5000
EXPOSE 5000/tcp

CMD python /application/server.py
