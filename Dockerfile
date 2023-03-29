FROM python:3.10.7-slim

# set work directory
WORKDIR /project

# set environment variables


# install dependencies

COPY ./requirements.txt /project/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . .