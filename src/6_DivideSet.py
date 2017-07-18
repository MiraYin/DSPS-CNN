import random
import os

if(os.path.exists('../data/forCaffe')):
    os.mkdir('../data/forCaffe')

def divideSet(dti,preflix = 'e'):
    random.shuffle(dti)
    l = len(dti)
    train = dti[0:int(l*0.8)]
    val = dti[int(l*0.8):int(l*0.9)]
    test = dti[int(l*0.9):]
    f = open('../data/forCaffe/'+preflix+'_train.txt','w')
    f.writelines(train)
    f.close()
    f = open('../data/forCaffe/'+preflix+'_val.txt','w')
    f.writelines(val)
    f.close()
    f = open('../data/forCaffe/'+preflix+'_test.txt','w')
    f.writelines(test)
    f.close()

if __name__ = '__main__':
    #only for enzyme
    f = open('../dti/drug_e_cid_all.txt','r')
    dti = f.readlines()
    f.close()

    divideSet(dti,'e')
