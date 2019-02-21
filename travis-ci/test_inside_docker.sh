#!/bin/sh -xe

OS_VERSION=$1
PACKAGES=$2

ls -l /home

# Clean the yum cache
yum -y clean all
yum -y clean expire-cache

# First, install all the needed packages.
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-${OS_VERSION}.noarch.rpm

yum -y install yum-plugin-priorities
rpm -Uvh https://repo.opensciencegrid.org/osg/3.4/osg-3.4-el${OS_VERSION}-release-latest.rpm
yum -y install make git openssl rpm-build

# Prepare the RPM environment
mkdir -p /tmp/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
cat >> /etc/rpm/macros.dist << EOF
%dist .osg.el${OS_VERSION}
%osg 1
EOF

SPEC="osg-test/rpm/osg-test.spec"
cp $SPEC /tmp/rpmbuild/SPECS
package_version=`grep -m 1 Version $SPEC | awk '{print $2}'`
pushd osg-test
git archive --format=tar --prefix=osg-test-${package_version}/ HEAD  | gzip >/tmp/rpmbuild/SOURCES/osg-test-${package_version}.tar.gz
popd

# Build the RPM
rpmbuild --define '_topdir /tmp/rpmbuild' -ba /tmp/rpmbuild/SPECS/osg-test.spec

# After building the RPM, try to install it
yum localinstall -y /tmp/rpmbuild/RPMS/noarch/osg-test*

rpm -ql osg-test

# HTCondor really, really wants a domain name.  Fake one.
sed /etc/hosts -e "s/`hostname`/`hostname`.unl.edu `hostname`/" > /etc/hosts.new
/bin/cp -f /etc/hosts.new /etc/hosts

# Bind on the right interface and skip hostname checks.
mkdir -p /etc/condor{-ce,}/config.d/
cat << EOF > /etc/condor/config.d/99-local.conf
NETWORK_INTERFACE=eth0
GSI_SKIP_HOST_CHECK=true
SCHEDD_DEBUG=\$(SCHEDD_DEBUG) D_FULLDEBUG
SCHEDD_INTERVAL=1
SCHEDD_MIN_INTERVAL=1
EOF
cp /etc/condor/config.d/99-local.conf /etc/condor-ce/config.d/99-local.conf

# Reduce the trace timeouts
export _condor_CONDOR_CE_TRACE_ATTEMPTS=60

# Ok, do actual testing
INSTALL_STR="--install ${PACKAGES//,/ --install }"
echo "------------ OSG Test --------------"
osg-test --extra-repo osg-testing -vad --hostcert --no-cleanup ${INSTALL_STR}
