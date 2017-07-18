import numpy as np
import random

def generate_nega(drug, protein):
    dti_l = len(drug)
    nega = []   
    for i in range(2*dti_l):
        if len(nega)>dti_l:
            break
        rdi = random.randint(0,dti_l-1)
        rpi = random.randint(0,dti_l-1)
        while rdi==rpi:
            rdi = random.randint(0,dti_l-1)
            rpi = random.randint(0,dti_l-1)
        temp = 'hsa:'+ protein[rpi]+ '\t'+ drug[rdi]+'\n'
        if temp not in dti:
            nega.append(temp)
    return nega

if __name__ = '__main__':
    pkind = ['e','gpcr','ic','nr']
    for pk in pkind:
        f = open('../dti/drug_'+pk+'_cid.txt','r')
        dti = f.readlines()
        f.close()
        drug = []
        protein = []
        for in_ in dti:
            temp = in_.split()
            protein.append(temp[0].split('hsa:')[1])
            drug.append(temp[1].strip())
        nega = generate_nega(drug,protein)
        out = ''
        for in_ in dti:
            out += '1,'+in_
        for in_ in nega:
            out += '0,'+in_
        f = open('../dti/drug_'+pk+'_cid_all.txt','w')
        f.write(out)
        f.close()
