#!/bin/bash
IMGNAME=jointhero/datainsight
IMGVERSION=sz-v1.251030
docker build --no-cache -t $IMGNAME:$IMGVERSION .
