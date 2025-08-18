#!/bin/bash
cd /opt/MACDA && \
sleep 30 && \
nohup /opt/MACDA/venv/bin/faust --datadir=/tmp/worker1 -A app worker -l info --web-port=6166 >> /tmp/macda.log 2>&1 &