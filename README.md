# DSPS-CNN
DSPS- CNN, short for Drug Substructural Protein Sequence - CNN, is used for predict drug-target interaction using target amino acid sequences and drug substructural fingerprint based on convolutional neural network. 

## Guide
### 0_Generate_Unique_ID.py
used for generating unique drug and target identifier. Drug: PubChem CID; Target: KEGG hsa

### 1_Get_DecodeFingerprint.py
used for get and decode PubChem fingerprint (881 bits). API takes CID as input

### 2_Get_aaseq.py
used for get the amino acid sequence of targets

### 3_Feature_3aa.py
used for generate 3aa feature of targets. 

### 4_Feature_onehot.py
used for generate onehot representation of targets

### 5_Generate_Nega.py
used for generate negative samples

### 6_DivideSet.py
used for divide train/val/test set

### 7_Generate_lmdb.py
used for generate lmdb for Caffe

### 8_TrainCNN.py
used for train CNN via pyCaffe

### 9_Get_test_CNN_feature.py
used for extract CNN feature of test set

### runTrain.sh
shell for train CNN via terminal

### DIR: CNN
prototxts for DSPS-CNN: trainval, solver and deploy

### DIR: dti
original drug-target interaction pairs after ID convert (Drug to PubChem CID, target to KEGG hsa)

### DIR: data/fingerprint
dir built for storing drug fingerprint

### DIR: data/aaseq
dir built for storing target a.a. sequence

### DIR: data/forCaffe
dir build for storing train/val/test set divided for CNN

