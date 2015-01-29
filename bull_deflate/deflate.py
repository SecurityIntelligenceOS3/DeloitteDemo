from pymongo import MongoClient as MC
import csv

keywords = {'ddos': 2, 'vulnerability': 1.4, 'exploit': 0.8, 'attack': 0.2, 'bug': 0.5, 'ing':10, 'amro':10, 'deloitte':10, 'apple':10}
count = {}
threshold = 100

client = MC()
db = client['DeloitteDemo']
collection = db.bull
doc = collection.find()

for d in doc:
    inf = []
    for k in keywords:
        count[k] = 0
    sc = 0
    list = []
    for w in d['b'].split():
        if w.lower() in keywords:
            inf.append(w.encode('ascii'))
            if w.lower() in count:
              count[w.lower()] += 1
            else:
                count[w.lower()] = 1
    for w in keywords:
        sc += count[w]*keywords[w]
    for c in count:
        l = [c,count[c]]
        list.append(l)
    
    f = {'doc': d['_id'], 'count': list, 'score': sc}
    if sc>threshold:
	print f
