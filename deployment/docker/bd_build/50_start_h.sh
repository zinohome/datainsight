#!/bin/bash
cd /opt/datainsight && \
sleep 30 && \
nohup /opt/datainsight/venv/bin/gunicorn -w 4 -b 0.0.0.0:8050 app:server >> /tmp/datainsight.log 2>&1 &