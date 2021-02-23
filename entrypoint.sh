#!/bin/bash

/usr/sbin/init &
/usr/sbin/osg-test "$@"
