import math
import pickle

amp = open("ampList.txt")
AmpList = amp.read().split("	")
AmpListF = []
for thing in AmpList:
    parts = thing.split('\n')
    for that in parts:
        AmpListF.append(that)

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

#for num in range(1100, 1901):
 #   try:
  #      print(str(AmpListF[int(AmpListF.index(str(roundup(num))))+1]) + " " + str(num))
   # except:
    #    print(num)

pickle.dump(AmpListF,open("pickledAmpList.p", "wb"))

print(pickle.load(open("pickledAmpList.p", "rb")))
