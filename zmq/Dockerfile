FROM python:3.7-slim
RUN apt update

WORKDIR /zmq
ADD ./requirements.txt /zmq/requirements.txt
RUN pip install -r requirements.txt
ADD . /zmq/