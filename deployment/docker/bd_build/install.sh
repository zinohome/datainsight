#!/bin/bash
set -e
set -x
apt-get update && DEBIAN_FRONTEND=noninteractive && \
apt -y dist-upgrade && \
apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev python3-dev net-tools libsasl2-dev libsnappy-dev cmake libsnappy-dev zlib1g-dev libbz2-dev libgflags-dev liblz4-dev curl wget procps netcat git libnss3-tools python3-pip && \
pip3 install virtualenv && \
cd /opt && \
git clone https://github.com/zinohome/datainsight.git && \
cd /opt/datainsight && \
git pull && \
mkdir -p /opt/datainsight/log && \
virtualenv venv && \
. venv/bin/activate && \
pip3 install -r requirements.txt && \
cp /bd_build/wait-for /usr/bin/wait-for && chmod 755 /usr/bin/wait-for && \
cp /opt/datainsight/deployment/docker/bd_build/50_start_h.sh /etc/my_init.d/50_start_datainsight.sh && \
chmod 755 /etc/my_init.d/50_start_datainsight.sh
