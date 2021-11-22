%%file filter_junction_file_seperate.py

import pandas as pd 
import sys 
import fileinput 

donor_dictionary = pd.read_csv('/Users/ramiyasivakumar/AMP/donor_dictionary.csv', sep='\t')
donor_dictionary=donor_dictionary.set_index('ID')['donor_pos'].to_dict()

acceptor_dictionary = pd.read_csv('/Users/ramiyasivakumar/AMP/acceptor_dictionary.csv', sep='\t')
acceptor_dictionary=acceptor_dictionary.set_index('ID')['acceptor_pos'].to_dict()

junction_file=sys.argv[1]
junc=fileinput.input(junction_file)

for each_line_junc in junc:
        each_line_junc = each_line_junc.split('\t') 
        junction_donor = each_line_junc[0]+"_"+each_line_junc[1]
        junction_acceptor = each_line_junc[0]+"_"+each_line_junc[2]
        if junction_donor in donor_dictionary and junction_acceptor in acceptor_dictionary: 
             print (each_line_junc)              
