# Building the image:
# sudo docker build -t ftxcc - < ./Dockerfile
#
# Running:
# sudo docker run -it -v /path/to/src/:/ftxcc -w /ftxcc/bin ftxcc /bin/bash

FROM ubuntu:18.04

# TODO to upgrade to libssl1.1, we need to modify the code
# https://wiki.openssl.org/index.php/OpenSSL_1.1.0_Changes
RUN apt-get -y update && apt-get install -y \
    libssl1.0-dev \
    g++ \
    make \
    pkg-config \
    cmake \
    curl \
    tar \
    less \
    gzip \
    ssh \
    ca-certificates \
    build-essential software-properties-common # required for add-apt-repository

# GCC-8 Installation
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test \
    && apt-get update -y \
    && apt-get install -y gcc-8 g++-8 \
    && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 800 --slave /usr/bin/g++ g++ /usr/bin/g++-8

# Build boost
RUN rm -rf /usr/include/boost; rm -rf /usr/lib/libboost*
ARG BOOST_VERSION=1.71.0
ARG BOOST_CHECKSUM=96b34f7468f26a141f6020efb813f1a2f3dfb9797ecf76a7d7cbd843cc95f5bd
ARG BOOST_DIR=boost
ARG CONCURRENT_PROCESSES=1
ENV BOOST_VERSION ${BOOST_VERSION}
RUN mkdir -p ${BOOST_DIR} \
    && cd ${BOOST_DIR} \
    && curl -L --retry 3 "https://dl.bintray.com/boostorg/release/${BOOST_VERSION}/source/boost_1_71_0.tar.gz" -o boost.tar.gz \
    && echo "${BOOST_CHECKSUM}  boost.tar.gz" | sha256sum -c \
    && tar -xzf boost.tar.gz --strip 1 \
    && cp -r boost /usr/include/boost \
    && cd .. && rm -rf ${BOOST_DIR} \
    && rm -rf /var/cache/*
