from array import array
import pandas as pd
import random
from random import randint
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

for file in range(19,20):
	string_1 = "../FASTA ("+str(file)+").fa"
	string_2 = "../flu ("+str(file)+").txt"

	#open FASTA file
	with open(string_1,'r') as f:
		unformatted = f.readlines()


	#find start points in FASTA (each value marks index of sequence start, not label, in unformatted array)
	starts = []
	for i in range(len(unformatted)):
		if(unformatted[i][0]==">"):
			starts.append(i+1)

	#open and cut down csv file with labels
	labels = pd.read_csv(string_2, delimiter = ",")

	#finding possible
	possible_end = [0]
	for i in range(len(labels['length'])-1):
		if(labels['length'][i]!=labels['length'][i+1]):
			possible_end.append(i)
	possible_end.append(len(labels['length'])-1)

	#date ranges for lengths
	date_ranges = []
	for i in range(len(possible_end)):
		if i!=0:
			x = possible_end[i-1]
			y = possible_end[i]
			date_ranges.append([int(labels['date'][x+1][0:4]),int(labels['date'][y][0:4]),labels['length'][y],x+1])

	#order date ranges by initial start date
	date_ranges.sort(key = lambda x: x[0])

	#alignment function -output: pairwise alignment with dashes
	def alignment(i,j):
		i_seq = ""
		j_seq = ""

		if(i>=len(starts)-1):
			initial = starts[i-1]
			while(initial<len(unformatted)-1):
				i_seq = i_seq + unformatted[initial].replace('\n','')
				initial = initial +1
		else: 
			for val in range(starts[i],starts[i+1]-1):
				i_seq = i_seq + unformatted[val].replace('\n','')

		#appending one sequence for output
		for checker in range(len(date_ranges)):
			if(len(date_ranges[checker])==4 and len(i_seq)==date_ranges[checker][2]):
				date_ranges[checker].append(i_seq)

		if(j>=len(starts)-1):
			initial = starts[j-1]
			while(initial<len(unformatted)-1):
				j_seq = j_seq + unformatted[initial].replace('\n','')
				initial = initial +1
		else: 
			for val in range(starts[j],starts[j+1]-1):
				j_seq = j_seq + unformatted[val].replace('\n','')

		alignments = pairwise2.align.globalxx(i_seq,j_seq, one_alignment_only=True)
		shorter_length = int(labels['length'][i])
		return processing(alignments,shorter_length)


	#alignment processing to get frequency distribution from pairwise format
	def processing(alignments,length):
		output = [0]*(length+1)
		pos = 1
		for i in range(len(alignments[0][0])):
			if(pos >= length):
				output[pos] = output[pos] + 1
			else:
				if(alignments[0][0][i]=="-"):
					output[pos]= output[pos]+1
				elif(alignments[0][1][i]=="-"):
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

	#for predictive model
	def vertical_2(distribution):
		total = 0
		for i in distribution:
			total = total + i
		new_output = []
		for i in distribution:
			new_output.append(i/total)
		return new_output

	#scaling distribution horizontally
	def horizontal(distribution,newest_length):
		current = len(distribution)
		new_output = [0]*newest_length
		factor = newest_length / current
		for i in range(newest_length):
			new_output[i] += distribution[int(float(i)/factor)]
		return new_output

	#finding intervals in distribution
	def intervals(distribution):
		intervals = []
		i=0
		while i<len(distribution):
			if(distribution[i]>0.000001):
				intervals.append([i,0])
				i=i+1
				while(i<len(distribution) and distribution[i]>0.000001):
					i=i+1
				intervals[len(intervals)-1][1]=i-1
			else:
				i=i+1
		return intervals

	def add(dis1, dis2):
		temp = dis1
		for i in range(len(dis1)):
			temp[i] = temp[i] + dis2[i]
		return temp

	data = []
	for i in range(len(date_ranges)-1):
		line = []
		s = str(date_ranges[i][0]) + str('-') + str(date_ranges[i][1])
		line.append(s)
		data_set = horizontal(vertical(alignment(date_ranges[i][3],date_ranges[i+1][3])),date_ranges[i][2])
		line.append(intervals(data_set))
		data.append(line)

	prob_dis = horizontal(vertical(alignment(date_ranges[0][3],date_ranges[1][3])),date_ranges[len(date_ranges)-1][2])

	for i in range(len(date_ranges)-1):
		if i!= 0:
			prob_dis = add(prob_dis, horizontal(vertical(alignment(date_ranges[i][3],date_ranges[i+1][3])),date_ranges[len(date_ranges)-1][2]))
	prob_dis = vertical_2(prob_dis)
	prob_dis_tuple = []
	for i in range(len(prob_dis)):
		prob_dis_tuple.append([i+1,prob_dis[i]])
	data.append([str(date_ranges[len(date_ranges)-1][0]) + str('-') + str(date_ranges[len(date_ranges)-1][1]),prob_dis_tuple])
		

	for l in range(len(data)):
		if(len(date_ranges[l])==5):
			data[l].append(date_ranges[l][4])

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
			i_seq = ''
			for val in range(starts[l],starts[l+1]-1):
				i_seq = i_seq + unformatted[val].replace('\n','')
			data[l].append(i_seq)


	df = pd.DataFrame(data, columns=['year_range','intervals','sequences'])
	name = labels['serotype'][1]+"_"+labels['segment'][1][0:1]+"_"+labels['country'][1]
	df.to_csv(name)
	print(df)
	print(file)