import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus.reader import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
import sys
import csv

#Set Random seed
np.random.seed(500)

####################################
### INPUT- labeled database file ###
####################################

dataArr = []
with open(r"C:\Users\נועם\Documents\all_text_wth_speaker_50_50_s_j.csv", 'r',encoding='latin-1') as file_name2:
    sheet_laugh = csv.reader(file_name2)
    for row in sheet_laugh:
        if row[0] is not "":
            row = [item.lower() for item in row] # Change all chars to lower case
            dataArr.append(row)
print(len(dataArr))

Corpus = pd.DataFrame(dataArr)



#####################
### Edit the data ###
#####################

# Remove blank rows
Corpus[0].dropna(inplace=True)	

# Tokenization - broke each entry into set of words
Corpus[0]= [entry.split() for entry in Corpus[0]]	

# WordNetLemmatizer:

# Its requires syntactic labeling for each word
tag_map = defaultdict(lambda : wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV

for index,entry in enumerate(Corpus[0]):
    Final_words = []
    word_Lemmatized = WordNetLemmatizer()
    # syntactic labeling
    for word, tag in pos_tag(entry):
        if word not in stopwords.words('english') and word.isalpha():	# check stop words
            word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
            Final_words.append(word_Final)
			
    Corpus.loc[index,2] = str(Final_words)


# Split the database into train and test data sets
Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus[2],Corpus[1],test_size=0.2,shuffle=False)


# Label encode the target variable
Encoder = LabelEncoder()
Train_Y = Encoder.fit_transform(Train_Y)
Test_Y = Encoder.fit_transform(Test_Y)


# Vectorize the words by using TF-IDF Vectorizer
Tfidf_vect = TfidfVectorizer(max_features=5000)
Tfidf_vect.fit(Corpus[2])

Train_X_Tfidf = Tfidf_vect.transform(Train_X)
Test_X_Tfidf = Tfidf_vect.transform(Test_X)


#######################################
### Run machine learning algorithms ###
#######################################

# Naive Bayes
Naive = naive_bayes.MultinomialNB()
Naive.fit(Train_X_Tfidf,Train_Y)
predictions_NB = Naive.predict(Test_X_Tfidf)

print("Naive Bayes Accuracy Score -> ",accuracy_score(predictions_NB, Test_Y)*100)


# SVM
SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
SVM.fit(Train_X_Tfidf,Train_Y)
predictions_SVM = SVM.predict(Test_X_Tfidf)

print("SVM Accuracy Score -> ",accuracy_score(predictions_SVM, Test_Y)*100)



#########################################
### OUTPUT- CSV file with the results ###
#########################################

with open("SVM_results.csv", 'w') as csvfile:
  table_write = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for i in range(len(predictions_SVM)):
    table_write.writerow([predictions_SVM[i]])

# Write the Predictions and the original classifying
with open("check_accuracy_all_text_28_10_2020.csv", 'w') as csvfile:
  table_write = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  table_write.writerow(['predictions_SVM','Test_Y - reality'])
  for i in range(len(predictions_SVM)):
      if (predictions_SVM[i] == Test_Y[i]):
          if (predictions_SVM[i] == 1):
            table_write.writerow([predictions_SVM[i] , Test_Y[i], "1 match"])
          elif (predictions_SVM[i] == 0):
              table_write.writerow([predictions_SVM[i], Test_Y[i], "0 match"])
      else:
          table_write.writerow([predictions_SVM[i], Test_Y[i]])

