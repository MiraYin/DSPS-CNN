import numpy as np
import random
import os
import scipy.io as sio
import caffe
import lmdb
from PIL import Image

proteinFt = np.load('../data/OneHotFt.npy')
hsa = np.load('../data/OneHotFt_hsa.npy')
Dir1 = '../data/fingerprint/'

f = open('../data/forCaffe/e_train.txt','r')
train = f.readlines()
f.close()

f = open('../data/forCaffe/e_val.txt','r')
val = f.readlines()
f.close()

#fingerprint: 327~881
chem = np.zeros((len(train),554,1,1))
chem = np.uint8(chem)

in_db = lmdb.open('protein-train-lmdb', map_size=int(1e12))
with in_db.begin(write=True) as in_txn:
    for in_idx, in_ in enumerate(train):
        pair = in_.split(',')
        lb = int(pair[0])
        hsa_id = pair[1].split('hsa:')[1]
        cid = pair[2].strip()
        f = open(Dir1 + cid + '.txt','r')
        chemdat = f.readline()
        f.close()
        chemdat = map(int,list(chemdat))
        chemdat = chemdat[327:]
        chemdat = np.uint8(np.asarray(chemdat))
    	chem[in_idx] = chemdat.reshape((554,1,1))
        onehotdat = proteinFt[np.argwhere(hsa==hsa_id)[0][0]]
        cutoff = 
        onehotdat = np.uint8(onehotdat.reshape((1,onehotdat.shape[0],onehotdat.shape[1])))
	im_dat = caffe.io.array_to_datum(onehotdat)
	im_dat.label = lb
        in_txn.put('{:0>10d}'.format(in_idx), im_dat.SerializeToString())
in_db.close()

np.save('chem-train',chem)
in_db = lmdb.open('chem-train-lmdb', map_size=int(1e12))
with in_db.begin(write=True) as in_txn:
    for in_idx, in_ in enumerate(train):
	im_dat = caffe.io.array_to_datum(chem[in_idx])
        in_txn.put('{:0>10d}'.format(in_idx), im_dat.SerializeToString())
in_db.close()

chem = np.zeros((len(val),554,1,1))
chem = np.uint8(chem)

in_db = lmdb.open('protein-val-lmdb', map_size=int(1e12))
with in_db.begin(write=True) as in_txn:
    for in_idx, in_ in enumerate(val):
        pair = in_.split(',')
        lb = int(pair[0])
        hsa_id = pair[1].split('hsa:')[1]
        cid = pair[2].strip()
        f = open(Dir1 + cid + '.txt','r')
        chemdat = f.readline()
        f.close()
        chemdat = map(int,list(chemdat))
        chemdat = chemdat[327:]
    	chemdat = np.uint8(np.asarray(chemdat))
    	chem[in_idx] = chemdat.reshape((554,1,1))
        onehotdat = proteinFt[np.argwhere(hsa==hsa_id)[0][0]]
        onehotdat = np.uint8(onehotdat.reshape((1,onehotdat.shape[0],onehotdat.shape[1])))
	im_dat = caffe.io.array_to_datum(onehotdat)
	im_dat.label = lb
        in_txn.put('{:0>10d}'.format(in_idx), im_dat.SerializeToString())
in_db.close()

np.save('chem-val',chem)
in_db = lmdb.open('chem-val-lmdb', map_size=int(1e12))
with in_db.begin(write=True) as in_txn:
    for in_idx, in_ in enumerate(val):
	im_dat = caffe.io.array_to_datum(chem[in_idx])
        in_txn.put('{:0>10d}'.format(in_idx), im_dat.SerializeToString())
in_db.close()
