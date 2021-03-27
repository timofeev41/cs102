FROM python:3.9.2-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8080

# Run with: docker run  -ti --rm --net=host --privileged --name hw06 hw06 sh