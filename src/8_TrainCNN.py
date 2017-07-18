import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import caffe
import matlab.engine
import scipy.io

'''
this script is for training DSPS-CNN using pycaffe.
However training using shell is recommended, since it has easy access to log file
which is useful for further loss plot.
Shell is also given: /src/runTrain.sh
'''
Dir1 = '../data/fingerprint/'

caffe_root = '../CNN/'
solver_path = caffe_root+'solver.prototxt'
# for CPU only
caffe.set_mode_cpu()
## if use GPU, use below instead 
#caffe.set_device(0)
#caffe.set_mode_gpu()

solver = caffe.SGDSolver(solver_path)
