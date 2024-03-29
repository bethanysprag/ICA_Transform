ARG AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID
ARG AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
FROM ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/ubuntu_focal
MAINTAINER 'Bethany Sprague bethanysprag@gmail.com'
ENV DEBIAN_FRONTEND='noninteractive'
ARG AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID # requires setting twice since setting prior to FROM only makes available up to that point
ARG AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
ENV AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID
ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
WORKDIR /work
RUN apt-get update && \
    apt-get install -qy libwxgtk3.0-gtk3-dev libtiff5-dev libgdal-dev libproj-dev  \
                        libexpat-dev wx-common libogdi-dev unixodbc-dev  && \
    apt-get install -qy g++ make automake libtool git wget                && \
    apt-get install -y python3-pip gdal-bin && \
    apt-get install -y zip nano
COPY requirements.txt /work/requirements.txt
COPY requirements-dev.txt /work/requirements-dev.txt
RUN apt-get install -y awscli
RUN pip3 install --upgrade awscli
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements-dev.txt
COPY . /work
RUN mkdir /work/Data
CMD /bin/bash
