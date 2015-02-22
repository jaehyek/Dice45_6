# -*- coding: utf-8 -*-
from operator import itemgetter
MAXNO = 45
SELNO = 6
MAXDIFFINNING = 60

class TableInningNum():
    def __init__(self, filecsv):
        listlistInningNos = []
        for line in open(filecsv):
            liststr = line.split(",")
            listno = []
            for no in liststr :
                listno.append(int(no))
            listlistInningNos.append( listno )
        self.listlistInningNos = listlistInningNos

    def getweekno(self):
        return self.listlistInningNos


    def calNumFreq(self):
        dictNumFreq = {}
        for i in range(1,MAXNO+1 ):
            dictNumFreq[i] = 0

        for listno in self.listlistInningNos:
            for no in listno[1:]:
                dictNumFreq[int(no)] += 1

        return dictNumFreq.items()

class Closeness():
    def __init__(self):
        dictdictcloseness = {}
        for no in range(1, MAXNO+1) :
            dictcloseness = {}
            for no_greater in range(no+1, MAXNO+1):
                dictcloseness[no_greater] = 0
            dictdictcloseness[no] = dictcloseness
        self.dictdictcloseness = dictdictcloseness

    def __str__(self):
        outstring = ""
        for no in range(1, MAXNO+1) :
            outstring += str(no) + ":"
            dictcloseness = self.dictdictcloseness[no]
            for no_greater in range(no+1, MAXNO+1):
                outstring += str((no_greater,dictcloseness[no_greater] )) + ","
            outstring += "\n"
        return outstring

    def putcloseness(self, no1, no2):
        if no1 > no2:
            no1, no2 = no2, no1

        self.dictdictcloseness[no1][no2] += 1

    def getcloseness(self, no1, no2):
        if no1 > no2:
            no1, no2 = no2, no1

        return self.dictdictcloseness[no1][no2]


    def makeCloseness(self, listlistInningNos) :
        for listweekno in listlistInningNos :
            for no1 in range(1, SELNO + 1 ):
                for no2 in range(no1+1, SELNO+1):
                    self.putcloseness(listweekno[no1], listweekno[no2])

    def getmostcloseness(self, no1):
        dictcloseness = self.dictdictcloseness[no1]
        return  sorted(dictcloseness.items, key=lambda closeness : closeness[1], reverse= True)

    def cal6MemberCloseness( self, listcandidate6No ):
        size6No = len(listcandidate6No)
        totalcloseness = 0
        for i in range(size6No):
            for j in range(size6No-1):
                listnos = [a for a in listcandidate6No]
                no1 = listnos.pop(i)
                no2 = listnos.pop(j)
                totalcloseness += self.getcloseness(no1, no2)


        return totalcloseness




class   calNextSelectionStat():
    def __init__(self):
        dictdictdiffInning = {}
        for no in range(1,MAXNO+1 ):
            dictdiffinning = {}
            for diffinning in range(1, MAXDIFFINNING + 1 ) :
                dictdiffinning[diffinning] = 0
            dictdictdiffInning[no] = dictdiffinning

        self.dictdictdiffInning = dictdictdiffInning

    def __str__(self):
        outstring = ""
        for no in range(1,MAXNO+1 ):
            dictdiffinning = self.dictdictdiffInning[no]
            listRankingNumDiffinning = sorted( dictdiffinning.items(), key=lambda freq: freq[1], reverse=True)
            outstring += str(no)+":"+ str(listRankingNumDiffinning) + "\n"

        return outstring



    def makenextInning(self,listlistInningNos ):
        # 주어진 입력으로, 각 번호별 회차차이에 대한 발생회수더하고, 저장.

        dictIntervalInning = {}
        for no in range(1, MAXNO+1):
            dictIntervalInning[no] = 0

        dictdictdiffInning = self.dictdictdiffInning

        for listno in listlistInningNos :
            currinning = listno[0]
            for no in listno[1:] :
                previnning = dictIntervalInning[no]
                dictIntervalInning[no] = currinning
                diffinning = currinning - previnning
                dictdictdiffInning[no][diffinning] += 1

        self.dictdictdiffInning = dictdictdiffInning

    def makeListTurpleNumInningOccurs(self):
        #마지막 회차 기준으로 다음 회차에 나올 가능성을  listturple형태로 계산
        listturpleNumInningOccurs = []
        for no in range(1, MAXNO+1) :
            for diffinning in range(1, MAXDIFFINNING + 1) :
                listturpleNumInningOccurs.append((no, diffinning,self.dictdictdiffInning[no][diffinning] ))
        return listturpleNumInningOccurs

def getNextCandidate6BasedOnInningNos(CandidateMax, listlistInningNos):
    # 각 번호별 다음회차에 나올 확률구하기
    nextsel = calNextSelectionStat()
    nextsel.makenextInning(listlistInningNos)
    # print ( "calculation of number next occurance : ")
    # print ( nextsel)

    #마지막 회차 기준으로 다음 회차에 나올 가능성을  listturple형태로 계산하고 sorting.( 번호, diffinning, 발생횟수)
    listturpleNumInningOccurs = nextsel.makeListTurpleNumInningOccurs()
    listturpleNumInningOccurs = sorted(listturpleNumInningOccurs, key= lambda tripair: tripair[2], reverse=True)
    # print ("Based on the last Inning, possibility of listturpleNumInningOccurs")
    # print (listturpleNumInningOccurs)

    listturplecandidateNoInningOccurs = []

    occursprev = 10000

    for turpleNumInningOccurs in listturpleNumInningOccurs :
        no, diffinning, occurs = turpleNumInningOccurs
        if len(listturplecandidateNoInningOccurs) >= CandidateMax  and occursprev > occurs :
            break

        # no가 이전의 -diffinning에서 존재했는지 조사.
        if no in listlistInningNos[-diffinning][1:] :
            # listturplecandidateNoInningOccurs에 이미 같은 번호가 있는지 조사한다.
            if not no in [ NoInningOccurs[0] for NoInningOccurs in listturplecandidateNoInningOccurs  ]:
                listturplecandidateNoInningOccurs.append(turpleNumInningOccurs)
                occursprev = occurs


    # 마지막 회차 기준으로 다음 회차에 나올 가능성이 가장 큰 순서대로 집결된 list을 print.
    # print ("top 10 list of possibility of occurances:")
    # print (listturplecandidateNoInningOccurs)
    return [ NoInningOccurs[0] for NoInningOccurs in listturplecandidateNoInningOccurs  ]

if __name__ == "__main__":
    '''
    여기에는  후보 숫자 몇개를 선택하는 것이 가장 효율적인지 계산한다.
    즉 후보 숫자가 많을 수록  참 숫자를 많이 포함할 수 있지만, 친밀도 검사에서 많은 경우의 수를 포함하게 된다.
    반대로, 후보 수자가 적을수록 참 숫자를 적게 포함 할 수 있지만, 친밀도 검사에서 적은 경우의 수를 포함하게 된다.
    '''

    # 후보 번호의 개수가 9개 일때, 가장 효율적이다.
    CandidateMax = 9

    listlistInningNosMaster = []
    for line in open("lotto.csv"):
        liststr = line.split(",")
        listno = []
        for no in liststr :
            listno.append(int(no))
        listlistInningNosMaster.append( listno )

    # 먼저 500개를 기본 baseline으로 정한다.
    COUNTBASE = 500

    COUNTMASTER = len(listlistInningNosMaster)
    listlistInningNos = []
    for i in range(COUNTBASE):
        listlistInningNos.append(listlistInningNosMaster[i])

    counttotalmatched = 0
    for i in range(COUNTBASE,COUNTMASTER):
        listcandidates = getNextCandidate6BasedOnInningNos(CandidateMax, listlistInningNos)
        listcandidates.sort()
        matched = 0
        for no in listlistInningNosMaster[i][1:]:
            if no in listcandidates :
                matched += 1
        print("@ %s Inning: %s matched"%(listlistInningNosMaster[i][0], matched))
        print("     candiate : %s"%(str(listcandidates)))
        print("     real val : %s"%str(listlistInningNosMaster[i][1:]))

        counttotalmatched += matched


        listlistInningNos.append(listlistInningNosMaster[i])

    counttrial = COUNTMASTER - COUNTBASE
    rateCandidateInning = 6 / 45

    print()
    print("%s candidate: ___ total matced ___: %s(%s matched/Inning, %s standard)"%(CandidateMax, counttotalmatched,counttotalmatched/counttrial, CandidateMax*rateCandidateInning))

    '''
    결론적으로 후보 숫자 개수는 9개가 가장 적절하다.
    '''


#
# #
# NoCand	fcast	std	    diff
# 14  	    2.24	1.86	0.38
# 12	    1.934	1.6	    0.334
# 9	        1.532	1.2	    0.332
# 13  	    2.058	1.73	0.328
# 15  	    2.321	2	    0.321
# 10  	    1.649	1.33	0.319
# 6	        1.102	0.8	    0.302
# 11  	    1.759	1.46	0.299
# 8	        1.35	1.06	0.29
# 22  	    3.218	2.93	0.288
# 7   	    1.182	0.93	0.252




