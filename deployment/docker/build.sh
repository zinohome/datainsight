#!/bin/bash
IMGNAME=jointhero/datainsight
IMGVERSION=sz-v1.250820
docker build --no-cache -t $IMGNAME:$IMGVERSION .
