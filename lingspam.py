# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 22:53:50 2017
@author: Abhijeet Singh
"""

import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix


def make_Dictionary(train_dir):
    emails = [os.path.join(train_dir, f) for f in os.listdir(train_dir)]
    all_words = []
    for mail in emails:
        print (mail)
        with open(mail) as m:
            for i, line in enumerate(m):
                if i == 2:
                    words = line.split()
                    all_words += words

    dictionary = Counter(all_words)
    print ("a")
    list_to_remove = list(dictionary)
    for item in list_to_remove:
        if item.isalpha() == False:
            del dictionary[item]
        elif len(item) == 1:
            del dictionary[item]
    dictionary = dictionary.most_common(3000)
    print ("b")
    return dictionary


def extract_features(mail_dir):
    files = [os.path.join(mail_dir, fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.zeros((len(files), 3000))
    docID = 0;
    nb = 0;
    for fil in files:
        print (nb)
        nb = nb +1
        print (fil)
        with open(fil) as fi:
            for i, line in enumerate(fi):
                if i == 2:
                    words = line.split()
                    for word in words:
                        wordID = 0
                        for i, d in enumerate(dictionary):
                            if d[0] == word:
                                wordID = i
                                features_matrix[docID, wordID] = words.count(word)
            docID = docID + 1
    return features_matrix


# Create a dictionary of words with its frequency

train_dir = '/home/mcn/PycharmProjects/bololo/train-mails'
dictionary = make_Dictionary(train_dir)

# Prepare feature vectors per training mail and its labels

train_labels = np.zeros(702)
train_labels[351:701] = 1
#train_matrix = extract_features(train_dir)
train_matrix = np.load('lingspam_train_matrix.npy');

# Training SVM and Naive bayes classifier and its variants

model1 = LinearSVC()
model2 = MultinomialNB()

model1.fit(train_matrix, train_labels)
model2.fit(train_matrix, train_labels)

# Test the unseen mails for Spam

#test_dir = '/home/mcn/PycharmProjects/bololo/test-mails-small'
#test_matrix = extract_features(test_dir)
#test_labels = np.zeros(260)
#test_labels[130:260] = 1

test_dir = '/home/mcn/PycharmProjects/bololo/test-mails-small'
test_matrix = extract_features(test_dir)
test_labels = np.zeros(1)
test_labels[0] = 1


result1 = model1.predict(test_matrix)
result2 = model2.predict(test_matrix)

print
confusion_matrix(test_labels, result1)
print
confusion_matrix(test_labels, result2)