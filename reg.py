from pymongo import MongoClient
import heapq
from sklearn.linear_model import LogisticRegression
import numpy as np

client = MongoClient("mongodb://savan:isrobot1@ds241278.mlab.com:41278/hackpton2019")

ratings = {
	'USA': 3,
	'United_Kingdom': 3,
	'Norway': 1,
	'Sweden': 1,
	'Belgium': 1,
	'Italy': 1,
	'Poland': 1,
	'Greece': 1,
	'Thailand': 2,
	'Colombia': 2,
	'Dominican_Republic' : 2,
	'Argentina': 3,
	'Bolivia': 3,
	'Brazil': 3,
	'Canada': 3,
	'Ecuador': 3,
	'Mexico': 3,
	'Nicaragua': 3,
	'Peru': 3
}
db = client.hackpton2019
strains = db['strains']

documents = strains.find({"strain": "H1N1", "strainType" :"N", "last":True})

train = []
target = []

for doc in documents:
	
	r = ratings[doc["country"]]
	probDistro = doc["probabilityIntervals"]
	l = len(probDistro)

	firstThird = doc["probabilityIntervals"][0:l//3].copy()
	secondThird = doc["probabilityIntervals"][l//3:2*l//3].copy()
	thirdThird = doc["probabilityIntervals"][2*l//3:l].copy()

	firstThird.sort()
	secondThird.sort()
	thirdThird.sort()

	top3 = [firstThird.pop(), secondThird.pop(), thirdThird.pop()]
	
	train.append(top3)
	target.append(r)


model = LogisticRegression()

train = np.reshape(train, (np.shape(train)[0], -1))

model.fit(train, target)

print(model.get_params())
print(model.score(train,target))

print(model.coef_)





