from pymongo import MongoClient
import heapq
from sklearn.linear_model import LogisticRegression

client = MongoClient("mongodb://savan:isrobot1@ds241278.mlab.com:41278/hackpton2019")

db = client.hackpton2019
strains = db['strains']

documents = strains.find({"last":True})

train = []
target = []

for doc in documents:

	rating = 1
	probDistro = doc.probabilityIntervals
	length = len(probDistro)

	firstThird = doc.probabilityIntervals[:length/3].copy()
	secondThird = doc.probabilityIntervals[length/3:2*length/3].copy()
	thirdThird = doc.probabilityIntervals[2*length/3:length].copy()

	top3 = [firstThird.pop(), secondThird.pop(), thirdThird.pop()]
	train.append(top3)
	target.append(rating)


model = LogisticRegression()

model.fit(train, target)

print(model.get_params())




