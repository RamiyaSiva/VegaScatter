import os
import sys
import fileinput


#create empty dictionary
dictionary = {} 

os.chdir('/Users/ramiyasivakumar/AMP/junction')
dir = "/Users/ramiyasivakumar/AMP/junction"

for junc in os.listdir(dir): 
    with open(junc, 'r') as f: 
        for line in f: 
            count = 1
            line = line.split('\t') 
            chr_num_junc = line[0]
            start_pos_junc_mod = line[1]
            end_pos_junc_mod = line[2]
            strand = line[5]
            UID = chr_num_junc + "_" + start_pos_junc_mod + "_" + end_pos_junc_mod
            if UID in dictionary:
                count = count+1
                dictionary[UID] = count
            if UID not in dictionary: 
                dictionary[UID] = count
print (dictionary) 
