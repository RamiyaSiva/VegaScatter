#import library 
import pandas as pd 

#supress warning message 
pd.options.mode.chained_assignment = None

#read gtf file and add a header
gtf = pd.read_csv('/Users/ramiyasivakumar/AMP/annotations/gencode.v29.primary_assembly.annotation.gtf.back', sep ="\t",header = None, names = ["Chr", "Group", "Type", "Start", "End", "Space", "Strand", "Space1", "Meta"])

#filter gtf file for exon,UTR regions 
region = ["exon", "UTR"]
gtf_regions = gtf[gtf['Type'].isin(region)]

#Drop the meta column, this will be added back later on
gtf_regions = gtf_regions.drop(['Meta'], axis=1)

#reset index 
gtf_regions.reset_index(inplace = True)

#formatting the information present in the final column(splitting by ';' as a delimiter, dropping columns that aren't present in all rows, adding header)
gtf_regions_meta = gtf[gtf['Type'].isin(region)]
gtf_regions_expanded = pd.DataFrame(gtf_regions_meta.Meta.str.split(';').tolist())
gtf_regions_expanded.drop(gtf_regions_expanded.columns[[9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]], axis=1, inplace=True)
gtf_regions_expanded.columns =['gene_id', 'transcript_id', 'gene_type', 'gene_name', 'transcript_type', 'transcript_name', 'exon_number', 'exon_id', 'level']

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

#create unique id - index 
#result.duplicated(subset=['brand'])
#cols = ['gene_name', 'exon_id']
#result['UID'] = result[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

#subset dataframe into 2 dataframes based on strand 

#positive strand 
gtf_pos = result[result['Strand'] == '+']
#rename start and end to donor and acceptor
gtf_pos.rename(columns = {'End':'Donor'}, inplace = True)
gtf_pos.rename(columns = {'Start':'Acceptor'}, inplace = True)

gtf_pos = gtf_pos[['Chr','Type', 'Acceptor', 'Donor','exon_id', 'gene_name', 'transcript_id']]

#negative strand
gtf_neg = result[result['Strand'] == '-']

#rename donor and acceptor
gtf_neg.rename(columns = {'Start':'Donor'}, inplace = True)
gtf_neg.rename(columns = {'End':'Acceptor'}, inplace = True)

#subsetting columns that will be kept in dictionary and reordering to match gtf_pos
gtf_neg = gtf_neg[['Chr','Type', 'Acceptor', 'Donor','exon_id', 'gene_name', 'transcript_id']]

#combine dataframes pos and neg
frames = [gtf_pos, gtf_neg]
gtf_dictionary = pd.concat(frames)


gtf_dictionary.to_csv('/Users/ramiyasivakumar/AMP/gtf_dict.csv', sep='\t', header=True, index=False)

