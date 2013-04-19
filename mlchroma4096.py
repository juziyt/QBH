import numpy
import line
import math
import mlpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import tkSnack, Tkinter
import os

execfile('chroma.py')

def most_common(ls):
        return max(set(ls), key=ls.count)

def smooth(a):
        for i in range(len(a)-2):
                if (a[i]-a[i+1])>2 and (a[i+2]-a[i+1])>2:
                        a[i+1] = a[i]
                if (a[i+1]-a[i])>2 and (a[i+1]-a[i+2])>2:
                        a[i+1] = a[i]
        return a

path="./audio4096/"
song_list=[]
chromaset=[]
i=0
for chroma_name in os.listdir(path):
        if chroma_name[-4:]!='.txt':
                continue
        chroma_path = path+chroma_name
        song_list.append(chroma_name[:-4])
        f = open(chroma_path,'r')
        temp = []
        for fline in f:
                temp.append(float(fline.replace('\n','')))
        chromaset.append(temp)

hum_chroma = []
f = open('qchroma.txt','r')
for fline in f:
        hum_chroma.append(float(fline.replace('\n','')))

#means=[]
#for i in range(len(chromaset)):
#       means.append(median(chromaset[i]))

#hum_mean = median(hum_chroma)

#humming_chroma = [[] for index in range(len(chromaset))]
#for i in range(len(chromaset)):
#        for j in range(len(hum_chroma)):
#                humming_chroma[i].append(hum_chroma[j] + means[i] - hum_mean)

def dtw(a, b):
        alen = len(a)
        blen = len(b)
        inf = 1000
        mline = [0]*(alen+1)
        mGamma = []
        for i in range(blen+1):
                mGamma.append(mline)
        for i in range(blen+1):
                mGamma[i][0] = inf
        for i in range(alen+1):
                mGamma[0][i] = inf
        mGamma[0][0] = 0
        for i in range(blen):
                for j in range(alen):
                        cost = 1-numpy.corrcoef(a[j], b[i])[0,1]
                        mGamma[i+1][j+1] = cost + min(mGamma[i][j], mGamma[i+1][j], mGamma[i][j+1])
        return mGamma[blen][alen]


dist = [[] for index in range(len(chromaset))]
for i in range(len(chromaset)):
        tempdist = []
        for j in range(12):
                tem, cost, p = mlpy.dtw_std(chromaset[i], hum_chroma, dist_only=False)
                tempdist.append(tem)
                hum_chroma = mod(hum_chroma+ones(len(hum_chroma)), 12)
        dist[i] = min(tempdist)

print song_list
print dist

match = song_list[dist.index(min(dist))]
for i in range(3):
        out1=min(dist)
        print song_list[dist.index(out1)]
        song_list.remove(song_list[dist.index(out1)])
        dist.remove(out1)

execfile('all.py')
root = Tkinter.Tk()
tkSnack.initializeSnack(root)
song = ConstructTags()
song_name = match+'.wav'
song_path = "./QBH_songs/"
song_path = song_path+song_name
song.read(song_path)
song.play()
root.mainloop()

song.stop()
song.destroy()
