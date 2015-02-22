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



if __name__ == "__main__":

    tableinningnum = TableInningNum("lotto.csv")
    listlistInningNos = tableinningnum.getweekno()
    listtupleNumFreq = tableinningnum.calNumFreq()

    # 당점된 횟수가 많은 것 부터 나열하기.
    listRankingNumFreq = sorted( listtupleNumFreq, key=lambda freq: freq[1], reverse=True)
    print ( "listRankingNumFreq :" )
    print ( listRankingNumFreq )

    # 각 회차에서 같이 나올 확률구하기.(친밀성 구하기 )
    closeness = Closeness()
    closeness.makeCloseness(listlistInningNos)
    print("closeness of two number ")
    print(closeness)

    # 각 번호별 다음회차에 나올 확률구하기
    nextsel = calNextSelectionStat()
    nextsel.makenextInning(listlistInningNos)
    print ( "calculation of number next occurance : ")
    print ( nextsel)

    #마지막 회차 기준으로 다음 회차에 나올 가능성을  listturple형태로 계산하고 sorting.( 번호, diffinning, 발생횟수)
    listturpleNumInningOccurs = nextsel.makeListTurpleNumInningOccurs()
    listturpleNumInningOccurs = sorted(listturpleNumInningOccurs, key= lambda tripair: tripair[2], reverse=True)
    print ("Based on the last Inning, possibility of listturpleNumInningOccurs")
    print (listturpleNumInningOccurs)

    # 마지막 회차 기준으로 다음에 나올 수 있는 숫자를 CandidateNoMax 개수만큼 후보자를 구한다.
    listturplecandidateNoInningOccurs = []
    CandidateNoMax = 9
    occursprev = 10000

    for turpleNumInningOccurs in listturpleNumInningOccurs :
        no, diffinning, occurs = turpleNumInningOccurs
        if len(listturplecandidateNoInningOccurs) >= CandidateNoMax  and occursprev > occurs :
            break

        # no가 이전의 -diffinning에서 존재했는지 조사.
        if no in listlistInningNos[-diffinning][1:] :
            # listturplecandidateNoInningOccurs에 이미 같은 번호가 있는지 조사한다.
            if not no in [ NoInningOccurs[0] for NoInningOccurs in listturplecandidateNoInningOccurs  ]:
                listturplecandidateNoInningOccurs.append(turpleNumInningOccurs)
                occursprev = occurs


    # 마지막 회차 기준으로 다음 회차에 나올 가능성이 가장 큰 순서대로 집결된 list을 print.
    print ("top 10 list of possibility of occurances:")
    print (listturplecandidateNoInningOccurs)


    # listturplecandidateNoInningOccurs = list [ turple(no, diffinning, countadvent)]

    # listturplecandidateNoInningOccurs 을 기준으로, 숫자6개(lotto 수자 6개 )를 뽑아서 조합을 만들수 있는 경우에 대한 list을 만든다.
    # list의 내용은 listturplecandidateNoInningOccurs의 index을 지칭한다.

    listlistcandidate6index = []
    sizeCandidatelist = len(listturplecandidateNoInningOccurs)

    for i in range(sizeCandidatelist):
        for j in range(sizeCandidatelist-1):
            for k in range(sizeCandidatelist-2):
                for l in range(sizeCandidatelist-3) :
                    for m in range(sizeCandidatelist-4):
                        for n in range(sizeCandidatelist-5):
                            listbase = [ a for a in range(sizeCandidatelist)]
                            listout = []
                            listout.append(listbase.pop(i))
                            listout.append(listbase.pop(j))
                            listout.append(listbase.pop(k))
                            listout.append(listbase.pop(l))
                            listout.append(listbase.pop(m))
                            listout.append(listbase.pop(n))
                            listout.sort()
                            listlistcandidate6index.append(listout)

    #각 index값 기준으로 sort을 하고,
    listlistcandidate6index = sorted(listlistcandidate6index,key=itemgetter(0,1,2,3,4,5))

    # 중복을 제거한다.
    listprev = [ 1,1,1,1,1,1]
    listlistcandidate6indexWithoutDup = []
    for listcandidate6index in listlistcandidate6index :
        if listprev != listcandidate6index :
            listlistcandidate6indexWithoutDup.append(listcandidate6index)
        listprev = listcandidate6index

    print("listlistcandidate6indexWithoutDup count:%s"%(len(listlistcandidate6indexWithoutDup)))


    # index을 숫자로 변화하고, 친밀도를 붙여 list을 만든다.
    listlistcandidate6NoCloseness = []
    for listcandidate6index in listlistcandidate6indexWithoutDup :
        listcandidate6No = [listturplecandidateNoInningOccurs[index][0] for index in listcandidate6index ]
        listcandidate6No.sort()
        val = closeness.cal6MemberCloseness( listcandidate6No )
        listcandidate6No.append(val)
        listlistcandidate6NoCloseness.append(listcandidate6No)

    print("listlistcandidate6NoCloseness count:%s"%len(listlistcandidate6NoCloseness))




    # closeness기준으로 listlistcandidate6NoCloseness를 sort한다. 역순으로.
    listlistcandidate6NoCloseness = sorted(listlistcandidate6NoCloseness, key= lambda noclose: noclose[-1], reverse=True)

    # 30개만 print한다.
    count = 30
    i = 0
    while(i < count ):
        print(listlistcandidate6NoCloseness[i])
        i += 1






