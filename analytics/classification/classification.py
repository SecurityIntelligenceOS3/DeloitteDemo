import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier

X_train = np.array(["The most rainy city must be Amsterdam!", 
                    "I visited NY metropolitan museum of art", 
                    "Have the best bitterballen in Amsterdam", 
                    "In Tokyo they really like fish", 
                    "Amsterdam is all for the weed", 
                    "Let's listen to some New York Jazz!", 
                    "Sting is playin in Tokyo this weekend", 
                    "Have you visited Amsterdam During King Day?", 
                    "There are so many people in Tokyo", 
                    "I wanna be a part of it New York New York",
                    "New York then Tokyo then back to Amsterdam!!",
                    "I had a friend from Amsterdam but he now moved to Tokyo",
                    "New York and Tokyo are among the most populus cities",
                    "Amsterdam Light Festival attracted people from New York",
                    "Tokyo is one of the most technologically advanced cities"])
     
y_train = [[0],[1],[0],[2],[0],[1],[2],[0],[2],[1],[0,1,2],[0,2],[1,2],[0,1],[2]]
X_test = np.array(['Where can I find the best bitterballen?',
                    'My mother likes fish',
		    'My gf likes art',
                    'My friend moved',
                    'Light Festival',
		    'Shall I try weed?',
		    'back'])
target_names = ['Amsterdam','New York', 'Tokyo']

classifier = Pipeline([
    ('vectorizer', CountVectorizer(min_df=1)),
    ('tfidf', TfidfTransformer()),
    ('clf', OneVsRestClassifier(LinearSVC()))])
classifier.fit(X_train, y_train)
predicted = classifier.predict(X_test)
print "Training set:"
print X_train
print
print "Test set:"
for item, labels in zip(X_test, predicted):
    print '%s => %s' % (item, ', '.join(target_names[x] for x in labels))


