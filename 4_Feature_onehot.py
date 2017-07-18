import os
import numpy as np

# Division of amino acids into seven groups based on the dipoles and volumes of the side chains. 
aaconvert = ['1','0','2','7','7','4','1','5','4','0','6','4','3','5','0','4','5','6','3','3','0','1','5','0','3','0']
            
def aa2index(x):
    return aaconvert[ord(x) - ord('A')]

def aaseq2idxseq(s):
    return map(aa2index,s)

def getOneHot(s,cutoff):
    slist = aaseq2idxseq(s)
    l = len(slist)
    flag = 1
    mat = np.zeros((cutoff,7),dtype = np.float64)
    if l <= cutoff:
        for i in range(l):
            mat[i][ord(slist[i])- ord('1')] = 1
    else:
        flag = 0
    return flag, mat

if __name__ == '__main__':
    Dir = '../data/aaseq/'
    features = []
    hsa = []
    for root, dirs, files in os.walk(Dir):
        for txt in files:
            if txt == '.DS_Store':
                continue
            f = open(Dir+txt,'r')
            aaseq = f.readline()
            f.close()
            (flag, mat) = getOneHot(aaseq,2000)
            if flag == 1:
                features.append(mat)
                hsa.append(txt[:-4])
                
    np.save('../data/OneHotFt.npy',np.array(features))
    np.save('../data/OneHotFt_hsa.npy',np.array(hsa))   

    
        
