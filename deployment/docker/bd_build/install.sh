#!/bin/bash
set -e
set -x
apt-get update && DEBIAN_FRONTEND=noninteractive && \
apt -y dist-upgrade && \
apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev python3-dev net-tools libsasl2-dev libsnappy-dev cmake libsnappy-dev zlib1g-dev libbz2-dev libgflags-dev liblz4-dev curl wget procps netcat git libnss3-tools python3-pip && \
pip3 install virtualenv && \
cd /opt && \
git clone https://github.com/zinohome/MACDA-SZ16.git && \
mv MACDA-SZ16 MACDA && \
cd /opt/MACDA && \
git pull && \
mkdir -p /opt/MACDA/log && \
virtualenv venv && \
. venv/bin/activate && \
pip3 install -r requirements.txt && \
pip3 install 'aiokafka[snappy]' && \
cd /opt/MACDA && cp /bd_build/default_env /opt/MACDA/.env && \
cp /bd_build/wait-for /usr/bin/wait-for && chmod 755 /usr/bin/wait-for && \
ls -l /opt/MACDA/.env && cat /opt/MACDA/.env && \
cp /opt/MACDA/deployment/docker/bd_build/50_start_h.sh /etc/my_init.d/50_start_macda.sh && \
chmod 755 /etc/my_init.d/50_start_macda.sh && \
cd /tmp && \
curl -sL rocksdb.tar.gz https://github.com/facebook/rocksdb/archive/refs/tags/v7.8.3.tar.gz > rocksdb.tar.gz && \
tar fvxz rocksdb.tar.gz && \
mv rocksdb-7.8.3 rocksdb && \
cd rocksdb && \
make shared_lib && \
make install-shared && \
rm -r /tmp/*
