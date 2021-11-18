import pandas as pd 
import sys 
import fileinput 


gtf_dictionary = pd.read_csv('/Users/ramiyasivakumar/AMP/gtf_dict.csv', sep='\t')

#convert dataframe to dictionary 
gtf_dictionary_file = gtf_dictionary.to_dict('index')
gtf_dictionary_file

junction_file=sys.argv[1]
junc=fileinput.input(junction_file)

for each_line_junc in junc:
        each_line_junc = each_line_junc.split('\t') 
        chr_num_junc = each_line_junc[0]
        start_pos_junc_mod = int(each_line_junc[1]) 
        end_pos_junc_mod = int(each_line_junc[2])
        if start_pos_junc_mod in gtf_dictionary_file and end_pos_junc_mod in gtf_dictionary_file: 
             print (each_line_junc)
