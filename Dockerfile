FROM alpine:3.6
MAINTAINER Aurelien PERRIER <a.perrier89@gmail.com>

RUN apk update
RUN apk add nginx