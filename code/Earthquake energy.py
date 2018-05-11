def findUrgs(richter):
    urgs = 11.8 + (1.5*(richter))
    urgs = 2.71828**urgs
    return urgs
while 1:
    try:
        richter = float(input("Please inpute the richter scale meserment\n"))
        break
    except:
        print("1-10")    

urgs = findUrgs(richter)

