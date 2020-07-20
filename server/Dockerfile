FROM python:3.7-slim
RUN apt update

WORKDIR /server
ADD ./requirements.txt /server/requirements.txt
RUN pip install -r requirements.txt
ADD . /server/