import os
import numpy as np

# Division of amino acids into seven groups based on the dipoles and volumes of the side chains. 
aaconvert = ['1','0','2','7','7','4','1','5','4','0','6','4','3','5','0','4','5','6','3','3','0','1','5','0','3','0']
aa = ['1','2','3','4','5','6','7']
aa2 = []
aa3 = []

for i in range(len(aa)):
    for j in range(len(aa)):
        aa2.append(aa[i]+aa[j])
        for k in range(len(aa)):
            aa3.append(aa[i]+aa[j]+aa[k])
            
def aa2index(x):
    return aaconvert[ord(x) - ord('A')]

def aaseq2idxseq(s):
    return map(aa2index,s)

def getCD(slist):
    l = float(len(slist))
    c1 = slist.count('1')
    c2 = slist.count('2')
    c3 = slist.count('3')
    c4 = slist.count('4')
    c5 = slist.count('5')
    c6 = slist.count('6')
    c7 = slist.count('7')
    C = [c1,c2,c3,c4,c5,c6,c7]
    return C           

def getT(s):
    slist = aaseq2idxseq(s)
    l = len(slist)
    results = [0.0]*343
    #343=7*7*7
    for i in range(l-2):
        in_ = slist[i]+slist[i+1]+slist[i+2]
        try:
            idx = aa3.index(in_)
        except:
            continue
        else:
            results[idx] += 1
    return [x/(l-2) for x in results]

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
            features.append(getT(aaseq))
            hsa.append(txt[:-4])

    np.save('../data/Ft_3aa.npy',np.array(features))
    np.save('../data/Ft_3aa_hsa.npy',np.array(hsa))
