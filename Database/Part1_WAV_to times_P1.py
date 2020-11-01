from scipy.io import wavfile  # scipy library to read wav files
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import sys

# path = ""
# cmd = "ffmb %s nkndk v%s ,mlfml " % (path, mfnk)
# os.system(cmd)
# open the wav file + view
AudioName = sys.argv[1] #r"C:\Users\נועם\Desktop\S06E02_only_laugh10min.wav"  # Audio File source and name

#print(AudioName)

fs, AudiodataX = wavfile.read(AudioName)
n = len(AudiodataX)

Audiodata = []
for i in range(n):
    Audiodata.append(AudiodataX[i][0])

#plt.plot(Audiodata)
#plt.title('Audiodata', size=16)

#21*60+30=n/48000
# Audiodata[47000:49000]
# find the laugh parts in the audio, by subtracting the left column  from the right one
#luaghGraph = []
#for i in range(0,n):
 #   luaghGraph.append(Audiodata[i][1] - Audiodata[i][0])

#print(Audiodata[1][1] , " " , Audiodata[1][0])
#plt.figure()
#plt.plot(Audiodata)
#plt.show()

# output the beginning and ending times
#
# calculate the average amplitude of every 10,000 samples
#   In order to get the indexes

start=[]
end=[]
last_print = 0  # checks the last time we printed
count=0 # counter to calculate the average
last_laugh = 0 # check if we in the laugh
for i in range(0,n-10000,1000): # run over the graph in jumps of 1,000
    for j in range (0,10000): # calculate the average amplitude of every 10,000 samples
        count+=abs(Audiodata[i+j])
        if(last_laugh == 1 and i>last_print+60000 and (count/10000 <=35 or count/10000 >=500)and j==9999):    # we are in the end of the laugh
                 #print("stop", i/fs)
                 #print(count/10000)
                 RESULT= i/fs #+600
                 end.append(RESULT)
                 last_laugh = 0
                 last_print=i
        elif(last_laugh == 0 and (count/10000 >=100 ) and j==9999 and (i>last_print+60000 or last_print==0)):     # we are in the beginning of the laugh
                                                    # and count/10000 <=200
             print("start",i/fs)
             #print(count / 10000)
             RESULT = i / fs #+600
             start.append(RESULT)
             last_laugh = 1
             last_print = i
    #print(i, count / 10000,"last_laugh:",last_laugh,i>last_print+30000)
    count=0

# export the table to a CSV file
i=0
size=len(start)
with open(sys.argv[2], 'w') as csvfile:
  table_write = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  table_write.writerow(['Start','End'])
  for line in range(0,size):
        table_write.writerow([start[i] , end[i]])
        i = i+1


