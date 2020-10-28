# -*- coding: utf-8 -*-


pip install ernie


#################################
### Function to open CSv file ###
#################################

import csv

def openCSVasList(file_name):
    dataArr = []
    i = 0
    with open(file_name, 'r', encoding='latin-1') as a_file:
        sheet_laugh = csv.reader(a_file)
        for row in sheet_laugh:
            # if (i % 2 == 0):                    # jump on blank rows, if there is any
            #     dataArr.append(row)
            #     # print(row)
            # i += 1
            dataArr.append(row)
    # print("length of", str, "dataframe", len(dataArr))
    print(dataArr[0],dataArr[1])
    return dataArr

	
	
	
###############################################################
### Input- open train & test dataset into panda's DataFrame ###
###############################################################

import pandas as pd
from sklearn import model_selection

train_file_name = '/content/all_text_wth_speaker_50_50_s_j_80.csv'
Corpus_train = pd.DataFrame(openCSVasList(train_file_name))

test_file_name = '/content/all_text_wth_speaker_50_50_s_j_20.csv'
Corpus_test = pd.DataFrame(openCSVasList(test_file_name))




#########################################
### Labelize the data as integers 1,0 ###
#########################################

label1 = Corpus_train.iat[0,1]
# label1 = 'SENTENCE'
i=1
while (Corpus_train.iloc[i,1] == label1): i+=1
label0 = Corpus_train.iloc[i,1] 

Corpus_train[1] = (Corpus_train[1] == label1).astype(int)
Corpus_test[1] = (Corpus_test[1] == label1).astype(int)
print("label1: ", label1, "\tlabel0: ", label0)




###########################################
### From soft decision to hard decision ###
###########################################

def probabilitiesTodecisions(probabilities_list):
  decisions = []
  for i in range(len(probabilities_list)):
    if probabilities_list[i][0] >=0.5:
      decisions.append(0)
    else:
      decisions.append(1)
    # print(probabilities_list[i], "\t", decisions[i])
  return decisions

  
  
  
######################
### check accuracy ###
######################

def checkAccuracy(prediction_labels,Test_labels):
  label_1_counter = 0
  label_1_match = 0
  label_0_counter = 0
  label_0_match = 0
  label_match= 0
  
  for i in range(len(prediction_labels)):
      if_correct = False                        ### add
      if(Test_labels.iloc[i,1] == 1):   # If the original label is '1'
          label_1_counter += 1
          if(prediction_labels[i] == Test_labels.iloc[i,1]):  # And if the prediction label is the same
              label_1_match += 1

              # print(Test_labels.iloc[i,0])    ### add
              if_correct = True                 ### add

      elif(Test_labels.iloc[i,1] == 0): # If the original label is '0'
          label_0_counter += 1
          if(prediction_labels[i] == Test_labels.iloc[i,1]):
              label_0_match += 1

              # print(Test_labels.iloc[i,0])    ### add
              if_correct = True                 ### add

      ### add
      # if (if_correct == True):
      #   print("true: ", Test_labels.iloc[i,1], "prediction: ", prediction_labels[i], "line number: ", i)
      # else:
      #   print("true: ", Test_labels.iloc[i,1], "prediction: ", prediction_labels[i])

  # Printing the results
  print("number of matches \n*label 1* \t",label_1_match ,"/", label_1_counter,
        "\n*label 0* \t",label_0_match ,"/", label_0_counter,)
  label_match = label_0_match + label_1_match
  accuracy = (label_match)*100/(len(prediction_labels))
  print("check accuracy\t", accuracy)
  


  # Save the results as CSV file
  with open("/content/a.csv", 'w') as csvfile:
    table_write = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    table_write.writerow(['','Test_Y - reality', 'predictions_NN'])
    for i in range(len(prediction_labels)):
      if (prediction_labels[i] == Test_labels.iloc[i,1]):
        table_write.writerow([Test_labels.iloc[i,0] ,Test_labels.iloc[i,1], prediction_labels[i], "match"])
      else:
        table_write.writerow([Test_labels.iloc[i,0] ,Test_labels.iloc[i,1], prediction_labels[i]])
          
        # if (prediction_labels[i] == Test_labels.iloc[i,1]):
        #     if (prediction_labels[i] == 1):
        #       table_write.writerow([prediction_labels[i] ,Test_labels.iloc[i,1], "1 match"])
        #     elif (prediction_labels[i] == 0):
        #         table_write.writerow([prediction_labels[i], Test_labels.iloc[i,1], "0 match"])
        # else:
        #     table_write.writerow([prediction_labels[i], Test_labels.iloc[i,1]])

  return accuracy, label_1_match/label_1_counter, label_0_match/label_0_counter

  
  
###########################################
### Save the test output for the graphs ###
###########################################

def append_3_list(model_vs_epochs_,accuracy_, match1_, match0_):
  model_vs_epochs_[0].append(accuracy_)
  model_vs_epochs_[1].append(match1_)
  model_vs_epochs_[2].append(match0_)
  return model_vs_epochs_

model_vs_epochs = [[],[],[]]






###################################################
###################################################
###################################################

### Run the neural network on the train dataset ###

###################################################
###################################################
###################################################

from ernie import SentenceClassifier, Models

# 1 epochs
classifier1 = SentenceClassifier(model_name=Models.BertBaseUncased, max_length=64, labels_no=2) # Initialize the model
classifier1.load_dataset(Corpus_train, validation_split=0.2)  # Load the dataset for a pre-train
classifier1.fine_tune(epochs=1, learning_rate=2e-5, training_batch_size=32, validation_batch_size=64) # learning stage

probabilities1 = list(classifier1.predict(Corpus_test[0]))
decisions1 = probabilitiesTodecisions(probabilities1)
accuracy1, match1_1, match0_1 = checkAccuracy(decisions1, Corpus_test)

model_vs_epochs = append_3_list(model_vs_epochs, accuracy1, match1_1, match0_1)




# 2 epochs
classifier2 = SentenceClassifier(model_name=Models.BertBaseUncased, max_length=64, labels_no=2)
classifier2.load_dataset(Corpus_train, validation_split=0.2)
classifier2.fine_tune(epochs=2, learning_rate=2e-5, training_batch_size=32, validation_batch_size=64)

probabilities2 = list(classifier2.predict(Corpus_test[0]))
decisions2 = probabilitiesTodecisions(probabilities2)
accuracy2, match1_2, match0_2 = checkAccuracy(decisions2, Corpus_test)

model_vs_epochs = append_3_list(model_vs_epochs, accuracy2, match1_2, match0_2)




# 3 epochs
classifier3 = SentenceClassifier(model_name=Models.BertBaseUncased, max_length=64, labels_no=2)
classifier3.load_dataset(Corpus_train, validation_split=0.2)
classifier3.fine_tune(epochs=3, learning_rate=2e-5, training_batch_size=32, validation_batch_size=64)

probabilities3 = list(classifier3.predict(Corpus_test[0]))  
decisions3 = probabilitiesTodecisions(probabilities3)
accuracy3, match1_3, match0_3 = checkAccuracy(decisions3, Corpus_test)

model_vs_epochs = append_3_list(model_vs_epochs, accuracy3, match1_3, match0_3)




# 4 epochs
classifier4 = SentenceClassifier(model_name=Models.BertBaseUncased, max_length=64, labels_no=2)
classifier4.load_dataset(Corpus_train, validation_split=0.2)
classifier4.fine_tune(epochs=4, learning_rate=2e-5, training_batch_size=32, validation_batch_size=64)

probabilities4 = list(classifier4.predict(Corpus_test[0]))
decisions4 = probabilitiesTodecisions(probabilities4)
accuracy4, match1_4, match0_4 = checkAccuracy(decisions4, Corpus_test)

model_vs_epochs = append_3_list(model_vs_epochs, accuracy4, match1_4, match0_4)





# 5 epochs
classifier5 = SentenceClassifier(model_name=Models.BertBaseUncased, max_length=64, labels_no=2)
classifier5.load_dataset(Corpus_train, validation_split=0.2)
classifier5.fine_tune(epochs=5, learning_rate=2e-5, training_batch_size=32, validation_batch_size=64)

probabilities5 = list(classifier5.predict(Corpus_test[0]))
decisions5 = probabilitiesTodecisions(probabilities5)
accuracy5, match1_5, match0_5 = checkAccuracy(decisions5, Corpus_test)

model_vs_epochs = append_3_list(model_vs_epochs, accuracy5, match1_5, match0_5)





for i in range(len(model_vs_epochs[0])):
  model_vs_epochs[0][i] = model_vs_epochs[0][i]/100

import matplotlib.pyplot as plot


# All 3 datas
plot.figure(figsize=(10,10))
plot.subplot(211)
plot.plot(model_vs_epochs[0])   # accuracy
plot.plot(model_vs_epochs[1])   # matches of label 1
plot.plot(model_vs_epochs[2])   # matches of label 0
plot.title('Model fit')
plot.ylabel('Fit')
plot.xlabel('Epoch')
plot.legend(['Accuracy', 'Label 1', 'Label 0'], loc='upper left')

# Only accuracy
plot.subplot(212)
plot.plot(model_vs_epochs[0])   # accuracy
plot.title('Model accuracy')
plot.ylabel('Accuracy')
plot.xlabel('Epoch')

plot.show()







# 10 epochs
classifier10 = SentenceClassifier(model_name=Models.BertBaseUncased, max_length=64, labels_no=2)
classifier10.load_dataset(Corpus_train, validation_split=0.2)
classifier10.fine_tune(epochs=17, learning_rate=2e-5, training_batch_size=32, validation_batch_size=64)

probabilities10 = list(classifier10.predict(Corpus_test[0]))
decisions10 = probabilitiesTodecisions(probabilities10)
accuracy10, match1_10, match0_10 = checkAccuracy(decisions10, Corpus_test)






model_epochs = [[],[],[]]

# testing
classifier_t = SentenceClassifier(model_name=Models.BertBaseUncased, max_length=64, labels_no=2)
classifier_t.load_dataset(Corpus_train, validation_split=0.2)
for i in range(10): 
  print("\n\n", "num of epochs:   ", i+1)
  classifier_t.fine_tune(epochs=1, learning_rate=2e-5, training_batch_size=32, validation_batch_size=64)
  probabilities_t = list(classifier_t.predict(Corpus_test[0]))
  decisions_t = probabilitiesTodecisions(probabilities_t)
  accuracy_t, match1_t, match0_t = checkAccuracy(decisions_t, Corpus_test)
  model_epochs = append_3_list(model_epochs, accuracy_t, match1_t, match0_t)

import matplotlib.pyplot as plot


# All 3 datas
plot.figure(figsize=(10,10))
plot.subplot(211)
plot.plot(model_epochs[0])   # accuracy
plot.plot(model_epochs[1])   # matches of label 1
plot.plot(model_epochs[2])   # matches of label 0
plot.title('Model fit')
plot.ylabel('Fit')
plot.xlabel('Epoch')
plot.legend(['Accuracy', 'Label 1', 'Label 0'], loc='upper left')

# Only accuracy
plot.subplot(212)
plot.plot(model_epochs[0])   # accuracy
plot.title('Model accuracy')
plot.ylabel('Accuracy')
plot.xlabel('Epoch')

plot.show()
