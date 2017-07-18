import os
import numpy as np
import matplotlib.pyplot as plt

dkind = ["e","gpcr","ic","nr"]
drug = []
protein = []
for in_ in dkind:
    f = open("../dti/drug_" + in_ + "_cid.txt")
    lines = f.readlines();
    f.close()

    for line in lines:
        temp = line.split()
        protein.append(temp[0].split('hsa:')[1])
        drug.append(temp[1].strip())

drug = list(set(drug))
protein = list(set(protein))

f = open("../data/unique_drug.txt",'w')
for in_ in drug:
    f.write(in_+'\n')
f.close()

f = open("../data/unique_protein.txt",'w')
for in_ in protein:
    f.write(in_+'\n')
f.close()
        
    
