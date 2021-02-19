ARG BASE_YUM_REPO=release
ARG DVER=7

FROM opensciencegrid/software-base:3.5-el$DVER-$BASE_YUM_REPO

RUN yum install -y \
        make \
        openssl \
        python36-rpm

WORKDIR /src

COPY osg-ca-generator /src/osg-ca-generator
COPY osg-test         /src/osg-test

RUN make -C osg-test install && make -C osg-ca-generator install

ENTRYPOINT ["/usr/sbin/osg-test"]
