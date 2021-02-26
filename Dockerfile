# Default to EL7 builds
ARG IMAGE_BASE_TAG=centos7

FROM centos:$IMAGE_BASE_TAG

# Previous arg hsa gone out of scope
ARG IMAGE_BASE_TAG=centos7
ARG OSG_RELEASE=3.6

RUN yum install -y epel-release && \
    yum -y install http://repo.opensciencegrid.org/osg/${OSG_RELEASE}/osg-${OSG_RELEASE}-el${IMAGE_BASE_TAG#centos}-release-latest.rpm && \
    yum update -y && \
    yum install -y \
        # pre-install audit to avoid pre-un bug in the packaging
        audit \
        # required for SELinux
        policycoreutils \
        libselinux-utils \
        make \
        openssl \
        python36-rpm

WORKDIR /src

COPY osg-ca-generator /src/osg-ca-generator
COPY osg-test         /src/osg-test

RUN make -C osg-test install && make -C osg-ca-generator install

