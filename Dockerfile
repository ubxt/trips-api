FROM python:3.9.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /tripsApi
WORKDIR /tripsApi
ADD . /tripsApi/
RUN pip install -r requirements.txt