FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /web
COPY requirements.txt /web/
RUN apt-get update
RUN apt-get -y install libev-dev
RUN pip install -r requirements.txt
COPY . /web/
