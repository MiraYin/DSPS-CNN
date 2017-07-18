import urllib2
import numpy as np

def get_aaseq(hsa):
    url = 'http://rest.kegg.jp/get/hsa:' + str(hsa) + '/aaseq'
    try:
        response = urllib2.urlopen(url)
    except urllib2.URLError, e:    
        print e.reason
        return
    else:
        html = response.read()
        aaseq = html.split('(A)\n')
        aaseq = aaseq[1].replace('\n','')
        return aaseq

if __name__ = "__main__":
    os.mkdir("../data/aaseq")
    f = open("../data/unique_protein.txt",'r')
    lines = f.readlines()
    f.close()
    errList_protein = []
    for line in lines:
        hsa = line.strip()
        try:
            aaseq = get_aaseq(hsa)
        except:
            print hsa + ": not found!"
            errList_protein.append(hsa)
        else:
            f = open("../data/aaseq/"+hsa+".txt")
            f.write(aaseq)
            f.close()
            
    f = open("../data/errorList_protein_hsa.txt",'w')
    for in_ in errList_protein:
        f.write(in_+'\n')
    f.close()
