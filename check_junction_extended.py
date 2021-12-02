%%file check_junction_extended.py

#4

import sys 
import fileinput
import pandas as pd

#import the junction file from the command line (for large scale runs, this can be set up through a job array maybe)
junction_file=sys.argv[1]
junc=fileinput.input(junction_file)

#convert the csv dict into a python dictionary
donor_dictionary = pd.read_csv('/Users/ramiyasivakumar/AMP/donor_dictionary.csv', sep='\t')
donor_dictionary = donor_dictionary.set_index('ID')['donor_pos'].to_dict()
#swap keys/values
dd_1 = dict((value,key) for key,value in donor_dictionary.items())

acceptor_dictionary = pd.read_csv('/Users/ramiyasivakumar/AMP/acceptor_dictionary.csv', sep='\t')
acceptor_dictionary = acceptor_dictionary.set_index('ID')['acceptor_pos'].to_dict()
ad_1 = dict((value,key) for key,value in acceptor_dictionary.items())

for each_line_junc in junc:
        each_line_junc = each_line_junc.split('\t') 
        if each_line_junc[5]=='+\n':
            junction_donor = each_line_junc[0]+"_"+each_line_junc[1]
            junction_acceptor = each_line_junc[0]+"_"+each_line_junc[2]
            if junction_donor in dd_1:
                if junction_acceptor in ad_1: 
                    print (each_line_junc,' Known Donor and Acceptor')
                if junction_acceptor not in ad_1: 
                    print (each_line_junc,' Known Donor')
            if junction_donor not in dd_1: 
                if junction_acceptor in ad_1: 
                    print (each_line_junc,' Known Acceptor')
                if junction_acceptor not in ad_1:
                    pass
        #if strand is reverse, then end position becomes donor (value in position 3) and start position becomes acceptor
        if each_line_junc[5]=='-\n':
            junction_donor = each_line_junc[0]+"_"+each_line_junc[2]
            junction_acceptor = each_line_junc[0]+"_"+each_line_junc[1]
            if junction_donor in dd_1:
                if junction_acceptor in ad_1: 
                    print (each_line_junc,' Known Donor and Acceptor')
                if junction_acceptor not in ad_1: 
                    print (each_line_junc,' Known Donor')
            if junction_donor not in dd_1: 
                if junction_acceptor in ad_1: 
                    print (each_line_junc,' Known Acceptor')
                if junction_acceptor not in ad_1:
                    pass
