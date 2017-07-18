#!/usr/bin/env sh
SOLVER_DIR=/Users/yanxin/Documents/DSPS_CNN/CNN
CAFFE_DIR=/Users/yanxin/Documents/caffe
TOOLS=${CAFFE_DIR}/build/tools
LOG="log/train_log.txt.`date +'%Y-%m-%d_%H-%M-%S'`"
$TOOLS/caffe train \
--solver=${SOLVER_DIR}/solver.prototxt 2>&1|tee ${LOG}&