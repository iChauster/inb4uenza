from array import array
import pandas as pd
from random import seed
from random import randint
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

#open FASTA file
with open('./FASTA (9).fa','r') as f:
	unformatted = f.readlines()

#find start points in FASTA
starts = []
for i in range(len(unformatted)):
	if(unformatted[i][0]==">"):
		starts.append(i+1)


#open and cut down csv file with labels
labels = pd.read_csv('./flu (1).txt', delimiter = ",")
abbrev = labels[['length','accession','date']]

#finding possible
possible_end = []
temp = abbrev['length'][0]
for i in range(len(abbrev['length'])):
	if i!=0:
		if(abbrev['length'][i]!=temp):
			possible_end.append(i-1)
			temp = labels['length'][i]

#date ranges for lengths
date_ranges = []
for i in range(len(possible_end)):
	if i!=0:
		x = possible_end[i-1]
		y = possible_end[i] - 1
		date_ranges.append([int(abbrev['date'][x][0:4]),
			int(abbrev['date'][y][0:4]),
			labels['length'][y],
			randint(x+1,y+1)])


#order date ranges by initial start date
date_ranges.sort(key = lambda x: x[0])


#alignment function
def alignment(i,j):
	i_seq = ""
	j_seq = ""

	for val in range(starts[i],starts[i+1]-1):
		i_seq = i_seq + unformatted[val].replace('\n','')

	#appending one sequence for output
	for checker in range(len(date_ranges)):
		if(len(date_ranges[checker])==4 & len(i_seq)==date_ranges[checker][2]):
			date_ranges[checker].append(i_seq)

	for val in range(starts[j],starts[j+1]-1):
		j_seq = j_seq + unformatted[val].replace('\n','')

	#appending one sequence for output
	for checker in range(len(date_ranges)):
		if(len(date_ranges[checker])==4 & len(j_seq)==date_ranges[checker][2]-1):
			date_ranges[checker].append(j_seq)

	alignments = pairwise2.align.globalxx(i_seq,j_seq, one_alignment_only=True)
	print(pairwise2.format_alignment(*alignments[0]))
	shorter_length = labels['length'][i]
	return processing(alignments,shorter_length)


#alignment processing
def processing(alignments,length):
	output = [0]*(length+1)
	pos = 1
	print(alignments[0][0][3])
	for i in range(len(alignments[0][0])):
		if(alignments[0][1][i]=="-"):
			output[pos]= output[pos]+1
		elif(alignments[0][0][i]=="-"):
			output[pos] += 1
			pos = pos +1
		else:
			pos = pos +1
	pos =1
	output.remove(0)
	return output



#scaling distribution vertically
def vertical(distribution):
	total = 0
	for i in distribution:
		total = total + i
	new_output = []
	for i in distribution:
		new_output.append(i/total)
	return new_output

#scaling distribution horizontally
def horizontal(distribution):
	newest_length = date_ranges[len(date_ranges)-1][2]
	current = len(distribution)
	new_output = []
	factor = newest_length / current
	for i in range(len(distribution)):
		new_output.append([(i+1)*factor,distribution[i]])
	return new_output

data = []
for i in range(len(date_ranges)-1):
	line = []
	s = str(date_ranges[i][0]) + str('-') + str(date_ranges[i][1])
	line.append(s)
	line.append("")
	data_set = horizontal(vertical(alignment(date_ranges[i][3],date_ranges[i+1][3])))
	#print(date_ranges)
	#line.append(date_ranges[i][4])
	line.append("")
	data.append(line)

df = pd.DataFrame(data, columns=['year_range','sequence','intervals'])
print(df)
#name = labels[1][4]+"_"+labels[1][3][0:1]+"_"+labels[1][5]+".csv"
#df.to_csv(name)