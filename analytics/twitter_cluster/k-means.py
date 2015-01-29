from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import numpy as np
from pymongo import MongoClient as MC


#connect to mongoDB database
client = MC()
db = client['DeloitteDemo']
collection = db.twitter_cluster


data = collection.find()
dataCount = collection.count()

corpus = []

for document in data:
        #objectID = document['_id']
        bull = document['t']
        str1 = ''.join(bull)
        corpus.append(str1)

cluster_numbers = 20
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(corpus)
model = KMeans(n_clusters=cluster_numbers, init='k-means++', max_iter=20000, n_init=1,verbose=0)
clusters = model.fit_predict(X)
for i in range(cluster_numbers):
        print "Cluster", i, " will contain association with the following documents: ",np.where(clusters == i)
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(cluster_numbers):
    print "Cluster %d:" % i,
    for ind in order_centroids[i, :20]:
        print ' %s' % terms[ind],
    print
