#!/bin/sh
afsutil ktlogin \
  --realm EXAMPLE.COM \
  --cell example.com \
  --user afsadmin \
  --akimpersonate \
  --keytab /tmp/afsutil/fake.keytab \
  -p aklog=/usr/local/bin/aklog-1.6
