import math

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10
currentText = open("Current.txt")
lmao = currentText.read().split("	")
bestList = []
for element in lmao:
    parts = element.split('\n')
    for l in parts:
        bestList.append(l)
    #print (parts)
#for line in currentText:
#    print(line)
for l in bestList:
    try:
        if float(l) > 14 and float(l) < 1000:
            bestList.remove(l)
    except:
        bestList.remove(l)
for kys in bestList:
    kys = float(kys)
print(bestList)
#print(roundup(41))
#element = '1100'
#if element in bestList:
#    print (bestList.index(element))
#print(bestList.index(13.33))
for num in range(1100, 1900):
    num2 = roundup(num)
    placeHolder = bestList.index(str(num2))
    print(str(bestList[placeHolder+1])+ " " + str(num))
