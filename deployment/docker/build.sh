#!/bin/bash
IMGNAME=jointhero/datainsight
IMGVERSION=sz-v1.2508
docker build --no-cache -t $IMGNAME:$IMGVERSION .
