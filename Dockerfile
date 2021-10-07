FROM ubuntu:16.04
ARG PACKAGE_NAME

# Install dependencies
RUN apt-get update && \
 apt-get -y install ${PACKAGE_NAME}

EXPOSE 80