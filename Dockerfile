# Default to EL7 builds
ARG IMAGE_BASE_TAG=centos7

FROM centos:$IMAGE_BASE_TAG

# Previous arg hsa gone out of scope
ARG IMAGE_BASE_TAG=centos7
ARG OSG_RELEASE=3.5

RUN yum install -y epel-release && \
    yum install -y yum -y install http://repo.opensciencegrid.org/osg/${OSG_RELEASE}/osg-${OSG_RELEASE}-el${IMAGE_BASE_TAG#centos}-release-latest.rpm && \
    yum install -y \
        make \
        openssl \
        python36-rpm

WORKDIR /src

COPY osg-ca-generator /src/osg-ca-generator
COPY osg-test         /src/osg-test

RUN make -C osg-test install && make -C osg-ca-generator install

