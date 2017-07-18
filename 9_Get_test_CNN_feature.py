import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import caffe
import matlab.engine
import scipy.io

Dir1 = '../data/fingerprint/'
deploy_path = '../CNN/deploy.prototxt'
model_path = '../CNN/iter_90000.caffemodel'
if os.path.isfile(deploy_path):
    print 'caffemodel found.'
else:
    print 'caffemodel not found'

def getFingerPt(cid):
    f = open(Dir1 + cid + '.txt','r')
    chemdat = f.readline()
    f.close()
    chemdat = map(int,list(chemdat))
    chemdat = chemdat[327:]
    return chemdat
 
#caffe.set_device(0)
#caffe.set_mode_gpu()
caffe.set_mode_cpu()

net = caffe.Net(deploy_path, model_path, caffe.TEST) 

f = open('../data/forCaffe/test.txt','r')
dti = f.readlines()
f.close()

proteinFt = np.load('../data/OneHotFt.npy')
hsa = np.load('../data/OneHotFt_hsa.npy')
pscore = []
ptruth = []
cnnft = []
out = []

for idx, in_ in enumerate(dti):
    pair = in_.split(',')
    ptruth.append(int(pair[0]))
    hsa_id = pair[1].split('hsa:')[1]
    cid = pair[2].strip()
    chemdat = np.uint8(np.asarray(getFingerPt(cid)))
    chemdat = chemdat.reshape((554,1,1))
    try:
        onehotdat = proteinFt[np.argwhere(hsa==hsa_id)[0][0]]
    except:
        continue
    else:
        cutoff = onehotdat.shape[0]
        onehotdat = np.uint8(onehotdat.reshape((1,cutoff,7)))
        out.append(in_)

    net.blobs['data'].reshape(1, 1, cutoff, 7)
    net.blobs['data'].data[...] = onehotdat
    net.blobs['chem'].reshape(1, 554, 1, 1)
    net.blobs['chem'].data[...] = chemdat
    output = net.forward()
    pscore.append(net.blobs['prob'].data[0].copy())
    cnnft.append(net.blobs['fc2'].data[0].copy())
    
scipy.io.savemat('result_cnn_test.mat', {'ptruth':ptruth,'pscore':pscore,'cnnft_test':cnnft,'dti':out})
