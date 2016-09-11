import pprint

class CLSVAR():
    pass

'''
6개의 숫자를 modular으로 분류를 했을 때, modular별로 나올수 있는 경우의 조합을 print
 예) Module=3일 때,
format = Mod0, Mod1, Mod2 에 해당하는 조합
[0, 0, 6]
[0, 1, 5]
[0, 2, 4]
[0, 3, 3]
[0, 4, 2]
[0, 5, 1]
[0, 6, 0]
[1, 0, 5]
[1, 1, 4]
[1, 2, 3]
[1, 3, 2]
[1, 4, 1]
[1, 5, 0]
[2, 0, 4]
[2, 1, 3]
[2, 2, 2]
[2, 3, 1]
[2, 4, 0]
[3, 0, 3]
[3, 1, 2]
[3, 2, 1]
[3, 3, 0]
[4, 0, 2]
[4, 1, 1]
[4, 2, 0]
[5, 0, 1]
[5, 1, 0]
[6, 0, 0]
'''
def printModulationCombination(clsvar,currDepth,remainedValue) :
    #check if this is last
    if clsvar.Mod == currDepth + 1 :
        clsvar.listvalue[currDepth] = remainedValue
        # print( clsvar.listvalue)
        clsvar.listlistcombination.append(clsvar.listvalue.copy() )

        return

    # call next function
    for i in range(remainedValue+1):
        clsvar.listvalue[currDepth] = i
        printModulationCombination(clsvar, currDepth + 1 ,remainedValue - i )


if __name__ == "__main__":
    clsvar = CLSVAR()
    clsvar.Mod = 15
    clsvar.listvalue = [0] * clsvar.Mod
    clsvar.listlistcombination = []

    currDepth = 0
    remainedValue = 6
    printModulationCombination(clsvar, currDepth, remainedValue)
    pprint.pprint(clsvar.listlistcombination)