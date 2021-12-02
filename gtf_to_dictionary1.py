#import library 
import pandas as pd 

#supress warning message 
pd.options.mode.chained_assignment = None

#read gtf file and add a header
gtf = pd.read_csv('/Users/ramiyasivakumar/AMP/annotations/gencode.v29.primary_assembly.annotation.gtf.bk', sep ="\t",header = None, names = ["Chr", "Group", "Type", "Start", "End", "Space", "Strand", "Space1", "Meta"])

#filter gtf file for exon,UTR regions 
region = ["exon", "UTR"]
gtf_regions = gtf[gtf['Type'].isin(region)]

#Drop the meta column (this will be added back later on)
gtf_regions = gtf_regions.drop(['Meta'], axis=1)

#reset index 
gtf_regions.reset_index(inplace = True)

#formatting the information present in the final column(splitting by ';' as a delimiter, dropping columns that aren't present in all rows, adding header)
gtf_regions_meta = gtf[gtf['Type'].isin(region)]
gtf_regions_expanded = pd.DataFrame(gtf_regions_meta.Meta.str.split(';').tolist())
gtf_regions_expanded.drop(gtf_regions_expanded.columns[[9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]], axis=1, inplace=True)
gtf_regions_expanded.columns =['gene_id', 'transcript_id', 'gene_type', 'gene_name', 'transcript_type', 'transcript_name', 'exon_number', 'exon_id', 'level']
gtf_regions_expanded

#combine formatted final column with previous dataframe, index again
result = pd.concat([gtf_regions, gtf_regions_expanded], axis=1).reindex(gtf_regions.index)

#drop index column
result = result.drop(['index'], axis=1)

#remove redundant string in rows 
result['gene_id'] = result['gene_id'].str.replace(r'gene_id', '')
result['transcript_id'] = result['transcript_id'].str.replace(r'transcript_id', '')
result['gene_type'] = result['gene_type'].str.replace(r'gene_type', '')
result['gene_name'] = result['gene_name'].str.replace(r'gene_name', '')
result['transcript_type'] = result['transcript_type'].str.replace(r'transcript_type', '')
result['transcript_name'] = result['transcript_name'].str.replace(r'transcript_name', '')
result['exon_number'] = result['exon_number'].str.replace(r'exon_number', '')
result['exon_id'] = result['exon_id'].str.replace(r'exon_id', '')
result['level'] = result['level'].str.replace(r'level', '')

#subset dataframe into 2 dataframes based on strand 
#positive strand 
gtf_pos = result[result['Strand'] == '+']
#rename start and end to donor and acceptor
gtf_pos.rename(columns = {'End':'Donor'}, inplace = True)
gtf_pos.rename(columns = {'Start':'Acceptor'}, inplace = True)

gtf_pos = gtf_pos[['Chr','Type', 'Acceptor', 'Donor','exon_id', 'gene_name', 'transcript_id']]

gtf_pos_plus = gtf_pos
gtf_pos_minus = gtf_pos

gtf_pos_plus = gtf_pos_plus.astype({"Acceptor":'int64', "Donor":'int64'})
gtf_pos_minus = gtf_pos_minus.astype({"Acceptor":'int64', "Donor":'int64'})

gtf_pos_plus['Acceptor'] = gtf_pos_plus['Acceptor'] + 1
gtf_pos_plus['Donor'] = gtf_pos_plus['Donor'] + 1

gtf_pos_minus['Acceptor'] = gtf_pos_minus['Acceptor'] - 1
gtf_pos_minus['Donor'] = gtf_pos_minus['Donor'] - 1


#combine all three dataframes into one 
gtf_pos = gtf_pos.append([gtf_pos_minus, gtf_pos_plus])

#sort
gtf_pos = gtf_pos.astype({"Acceptor":'int64', "Donor":'int64'})
gtf_pos.sort_values(by=['Acceptor'])
gtf_pos = gtf_pos.astype(str)

#add new columns suitable for dictionary creation
gtf_pos["acceptor_pos"] = gtf_pos["Chr"] +'_'+ gtf_pos["Acceptor"]
gtf_pos["donor_pos"] = gtf_pos["Chr"] +'_'+ gtf_pos["Donor"]

#UID
gtf_pos["ID"] = gtf_pos["exon_id"] +'_'+ gtf_pos["gene_name"]+'_'+ gtf_pos["transcript_id"]

gtf_pos.columns = gtf_pos.columns.str.replace(' ', '')

gtf_neg = result[result['Strand'] == '+']
#rename start and end to donor and acceptor
gtf_neg.rename(columns = {'Start':'Donor'}, inplace = True)
gtf_neg.rename(columns = {'End':'Acceptor'}, inplace = True)

gtf_neg = gtf_neg[['Chr','Type', 'Acceptor', 'Donor','exon_id', 'gene_name', 'transcript_id']]

gtf_neg_plus = gtf_neg
gtf_neg_minus = gtf_neg

gtf_neg_plus = gtf_neg_plus.astype({"Acceptor":'int64', "Donor":'int64'})
gtf_neg_minus = gtf_neg_minus.astype({"Acceptor":'int64', "Donor":'int64'})

gtf_neg_plus['Acceptor'] = gtf_neg_plus['Acceptor'] + 1
gtf_neg_plus['Donor'] = gtf_neg_plus['Donor'] + 1

gtf_neg_minus['Acceptor'] = gtf_neg_minus['Acceptor'] - 1
gtf_neg_minus['Donor'] = gtf_neg_minus['Donor'] - 1


#combine all three dataframes into one 
gtf_neg = gtf_neg.append([gtf_neg_minus, gtf_neg_plus])

#sort
gtf_neg = gtf_neg.astype({"Acceptor":'int64', "Donor":'int64'})
gtf_neg.sort_values(by=['Acceptor'])

gtf_neg = gtf_neg.astype(str)

#add new columns suitable for dictionary creation
gtf_neg["acceptor_pos"] = gtf_neg["Chr"] +'_'+ gtf_neg["Acceptor"]
gtf_neg["donor_pos"] = gtf_neg["Chr"] +'_'+ gtf_neg["Donor"]

#UID
gtf_neg["ID"] = gtf_neg["exon_id"] +'_'+ gtf_neg["gene_name"]+'_'+ gtf_neg["transcript_id"]

gtf_neg.columns = gtf_neg.columns.str.replace(' ', '')


gtf_neg = gtf_neg.replace({'\s': ''}, regex=True)
gtf_pos = gtf_pos.replace({'\s': ''}, regex=True)

#combine dataframes pos and neg
frames = [gtf_pos, gtf_neg]
gtf_dictionary = pd.concat(frames)


donor_dictionary = gtf_dictionary[["ID", "donor_pos"]]
acceptor_dictionary = gtf_dictionary[["ID", "acceptor_pos"]]
donor_dictionary.to_csv('/Users/ramiyasivakumar/AMP/donor_dictionary.csv', sep='\t', header=True, index=False)
acceptor_dictionary.to_csv('/Users/ramiyasivakumar/AMP/acceptor_dictionary.csv', sep='\t', header=True, index=False)
