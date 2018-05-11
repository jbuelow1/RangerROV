import math
#num = float(input())
for num in range(101):
    print("The input num was: " + str(num))
    bigNum = math.floor((3113*(num/100))+(2458*(1-(num/100))))
    print("The postive way would be: " + str(bigNum))
    littleNum = math.floor((1802*(num/100)) + (2458*(1-(num/100))))
    print("The negitve num would be: " + str(littleNum))
def test():
    return 1, 2
one,two = test()
print(one)
print(two)
