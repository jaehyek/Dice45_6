# -*- coding: utf-8 -*-
from operator import itemgetter
import itertools
import collections
import pprint
MAXNO = 45
SELNO = 6
MAXDIFFINNING = 60

class TableInningNo():
    def __init__(self, filecsv):
        self.listlistinningnos = []         # [[inning, no1,on2,no3,no4,no5,no6],[...],...]
        self.listtupleNoFreqSorted = []     # [(no1, freq),(no2,freq),...]  sorted on freq
        self.listdictinningmods = []        # [{inning,mod2,mod3,mod5,mod9,modsum, sum}, {...}, ...]

        for line in open(filecsv):
            listno = [int(aa) for aa in line.split(",")]
            self.listlistinningnos.append( listno )

        # sorting based on inning
        self.listlistinningnos = sorted(self.listlistinningnos, key=lambda listInningNos: listInningNos[0] )
        self.createlistdictModBalanceWithTable()
        self.createlisttupleNoFreqSorted()

    def getlistlistInningNos(self):
        return self.listlistinningnos

    def getNosWithInning(self, inning):
        return self.listlistinningnos[inning-1][1:]

    def createlisttupleNoFreqSorted(self):
        dictNumFreq = {}
        for i in range(1,MAXNO+1 ):
            dictNumFreq[i] = 0

        for listno in self.listlistinningnos:
            for no in listno[1:]:
                dictNumFreq[int(no)] += 1

        listtupleNoFreqSorted =  dictNumFreq.items()

        # 당점된 횟수가 많은 것 부터 나열하기.
        self.listtupleNoFreqSorted = sorted( listtupleNoFreqSorted, key=lambda tupleNoFreq: tupleNoFreq[1], reverse=True)

    def getlisttupleNoFreqSorted(self):
        return self.listtupleNoFreqSorted

    def writelisttupleNoFreqSorted(self, filecsv='NoFreq.csv'):
        f = open(filecsv, 'w' )
        f.write("No,Frequence,\n")
        for tupleNoFreq in self.listtupleNoFreqSorted :
            f.write(",".join([str(aa) for aa in tupleNoFreq]) + "\n")
        f.close()

    def getMatchingCombiCount(self, listNos):
        matchingcount = 0
        listmatchinning = []
        for listInningNos in self.listlistinningnos :
            listbools = []
            for no in listNos :
                listbools.append(no in listInningNos[1:])

            if all(listbools) :
                matchingcount += 1
                listmatchinning.append(listInningNos[0])

        return matchingcount, listmatchinning

    def getMod2Balance(self, listnos):
        listtemp = [ aa%2  for aa in listnos]
        countmod0 = listtemp.count(0)
        countmod1 = listtemp.count(1)
        return True if countmod0 == countmod1 else False

    def getMod3Balance(self, listnos):
        listtemp = [ aa%3  for aa in listnos]
        countmod0 = listtemp.count(0)
        countmod1 = listtemp.count(1)
        countmod2 = listtemp.count(2)
        return True if countmod0 == countmod1 and countmod1 == countmod2 else False

    def getMod5Balance(self, listnos):
        listtemp = [ aa%5  for aa in listnos]
        countmod0 = listtemp.count(0)
        countmod1 = listtemp.count(1)
        countmod2 = listtemp.count(2)
        countmod3 = listtemp.count(3)
        countmod4 = listtemp.count(4)
        listcheck = []
        listcheck.append(countmod0 in [1,2])
        listcheck.append(countmod1 in [1,2])
        listcheck.append(countmod2 in [1,2])
        listcheck.append(countmod3 in [1])
        listcheck.append(countmod4 in [1,2])
        return True if all(listcheck) == True else False

    def getMod9Balance(self, listnos):
        listtemp = [ aa%5  for aa in listnos]
        countmod0 = listtemp.count(0)
        countmod1 = listtemp.count(1)
        countmod2 = listtemp.count(2)
        countmod3 = listtemp.count(3)
        countmod4 = listtemp.count(4)
        countmod5 = listtemp.count(5)
        countmod6 = listtemp.count(6)
        countmod7 = listtemp.count(7)
        countmod8 = listtemp.count(8)

        listcheck = []
        listcheck.append(countmod0 in [0,1])
        listcheck.append(countmod1 in [0,1])
        listcheck.append(countmod2 in [0,1])
        listcheck.append(countmod3 in [0,1,2])
        listcheck.append(countmod4 in [0,1,2])
        listcheck.append(countmod5 in [0,1])
        listcheck.append(countmod6 in [0,1])
        listcheck.append(countmod7 in [0,1])
        listcheck.append(countmod8 in [0,1])

        return True if all(listcheck) == True else False

    def getModBalance(self, listnos):
        listcheck=[]
        listcheck.append(self.getMod2Balance(listnos))
        listcheck.append(self.getMod3Balance(listnos))
        listcheck.append(self.getMod5Balance(listnos))
        listcheck.append(self.getMod9Balance(listnos))

        return True if all(listcheck) == True else False

    def getdictModBalanceWithInning(self, inning):
        dicttemp = {}
        dicttemp["inning"] = inning
        dicttemp["mod2"] = self.getMod2Balance(self.listlistinningnos[inning -1][1:])
        dicttemp["mod3"] = self.getMod3Balance(self.listlistinningnos[inning -1][1:])
        dicttemp["mod5"] = self.getMod5Balance(self.listlistinningnos[inning -1][1:])
        dicttemp["mod9"] = self.getMod9Balance(self.listlistinningnos[inning -1][1:])
        dicttemp["modsum"] = all([dicttemp["mod2"],dicttemp["mod3"],dicttemp["mod5"],dicttemp["mod9"]])
        return dicttemp

    def createlistdictModBalanceWithTable(self):
        listdictinningmods = []
        for listinningnos in self.listlistinningnos :
            dicttemp = {}
            dicttemp["inning"] = listinningnos[0]
            dicttemp["mod2"] = self.getMod2Balance(listinningnos[1:])
            dicttemp["mod3"] = self.getMod3Balance(listinningnos[1:])
            dicttemp["mod5"] = self.getMod5Balance(listinningnos[1:])
            dicttemp["mod9"] = self.getMod9Balance(listinningnos[1:])
            dicttemp["modsum"] = all([dicttemp["mod2"],dicttemp["mod3"],dicttemp["mod5"],dicttemp["mod9"]])
            dicttemp["sum"] = sum(listinningnos[1:])
            listdictinningmods.append(dicttemp)

        self.listdictinningmods = listdictinningmods

    def getlistdictModBalanceWithTable(self):
        return self.listdictinningmods

    def writelistdictModBalanceWithTable(self, filecsv='modbal.csv'):
        f = open(filecsv, 'w')
        f.write("inning,no1,no2,no3,no4,no5,no6,mod2,mod3,mod5,mod9,modsum,sum\n")
        leninningnos = len(self.listlistinningnos)
        for idx in range(leninningnos) :
            f.write(",".join([str(aa)for aa in self.listlistinningnos[idx] ]) + ",")
            dicttemp = self.listdictinningmods[idx]
            f.write(str(dicttemp["mod2"]) + ",")
            f.write(str(dicttemp["mod3"]) + ",")
            f.write(str(dicttemp["mod5"]) + ",")
            f.write(str(dicttemp["mod9"]) + ",")
            f.write(str(dicttemp["modsum"]) + ",")
            f.write(str(dicttemp["sum"]) + "\n")
        f.close()

    def writeCombiMatchwithTable(self, combi, closeness, filecsv='combimatch.csv'):
        '''
        :param combi: can be 3, 4,5 which means that 3 is (no1, no2, n3 ) in inning's numbers .
                     similarly 4 means (no1,no2,no3,no4) in inning's numbers .
                     similarly 5 means (no1,no2,no3,no4,no4) in inning's numbers.
                     finally the purpose of 5 combination is to search if the 5 number of a inning is
                       appear again in other inning's numbers .
                     if there are several case of re-occurences,  write the re-occurence's count and info  to file.
        :param closeness: write the clsoeness to file if there is not None .
                     closeness is value between two number of not-combination numbers
        :param filecsv: file name to save which will composed of "combimatch" + combi + .csv
        :return: no return
        '''
        filecsv = (str(combi) + ".").join(filecsv.split("."))
        listlistmax = []
        listlistmax_1 = []
        lenmax = 0
        lenmax_1 = 0
        lenlistlistinningnos = len(self.listlistinningnos)
        for idx in range(lenlistlistinningnos) :
            if idx % 100 == 0  :
                print("\n")
            print(".", end="")
            listidx2 = [aa for aa in range(lenlistlistinningnos)]
            listidx2.remove(idx)
            listfindturplecombi = [bb for bb in itertools.combinations(self.listlistinningnos[idx][1:], combi )]
            for findtuplecombi in listfindturplecombi :
                # check it findtuplecombi is already found and recorded in list  listlistmax and listlistmax_1, if then, skip .
                boolexist = False
                for combiidxs in listlistmax :
                    if findtuplecombi == combiidxs[0] :
                        boolexist = True
                        break
                for combiidxs in listlistmax_1 :
                    if findtuplecombi == combiidxs[0] :
                        boolexist = True
                        break
                if boolexist == True :
                    continue

                listfoundcombiidxs = []
                for idx2 in listidx2 :
                    if set(findtuplecombi).issubset(self.listlistinningnos[idx2][1:]) :
                        listfoundcombiidxs.append(idx2 )
                lenfound = len(listfoundcombiidxs)
                if lenfound == 0 :
                    continue
                if lenfound >= 1 :
                    # add itself.
                    listfoundcombiidxs.insert(0,idx )
                    listfoundcombiidxs.insert(0,findtuplecombi)
                    lenfound += 1

                if lenfound > lenmax :
                    lenmax_1 = lenmax
                    lenmax = lenfound
                    listlistmax_1 = listlistmax
                    listlistmax = [listfoundcombiidxs]
                    continue
                elif lenfound == lenmax :
                    listlistmax.append( listfoundcombiidxs)
                    continue
                elif lenfound == lenmax_1 :
                    listlistmax_1.append( listfoundcombiidxs)
                    continue
                else:
                    continue
        print("\n")
        f = open(filecsv, 'w')

        strcombi = ["C" + str(aa) for aa in range(1,combi+1)]
        strdiffno = ["D" + str(aa) for aa in range(1, 6-combi + 1 )]
        f.write("countfound" +","+ ",".join(strcombi) + "," + "order,inning,no1,no2,no3,no4,no5,no6,sum," + ",".join(strdiffno) + "," )
        if closeness != None :
            lendiffcombi = len([aa for aa in itertools.combinations(range(6-combi),2 )])
            strdiffnoclose = [ "DClo" + str(aa) for aa in range(lendiffcombi)]
            f.write(",".join(strdiffnoclose) + ",")
        f.write("\n")

        for listcombiidxs in listlistmax :
            listcombi = list(listcombiidxs[0])
            order = 1
            for idxs in listcombiidxs[1:] :
                listnos = self.listlistinningnos[idxs][1:]
                f.write(str(lenmax) + ","+ ",".join([str(aa) for aa in listcombi])+","+str(order) +","+ str(idxs+1)+",")
                f.write(",".join([str(aa) for aa in listnos]) + ","+ str(sum(listnos)) + "," )
                listtemp = list(set(listnos)-set(listcombi))
                listtemp.sort()
                f.write(",".join([str(aa) for aa in listtemp]) + ",")

                # write the info of closeness
                if closeness != None :
                    f.write(",".join([str(aa) for aa in closeness.getlistcloseness(listtemp)]) + ",")
                f.write("\n")
                order += 1

        for listcombiidxs in listlistmax_1 :
            listcombi = list(listcombiidxs[0])
            order = 1
            for idxs in listcombiidxs[1:] :
                listnos = self.listlistinningnos[idxs][1:]
                f.write(str(lenmax_1) + "," + ",".join([str(aa) for aa in listcombi])+","+str(order) +","+ str(idxs+1)+",")
                f.write(",".join([str(aa) for aa in listnos]) + ","+ str(sum(listnos)) + "," )
                listtemp = list(set(listnos)-set(listcombi))
                listtemp.sort()
                f.write(",".join([str(aa) for aa in listtemp ]) + ",")

                # write the info of closeness
                if closeness != None :
                    f.write(",".join([str(aa) for aa in closeness.getlistcloseness(listtemp)]) + ",")
                f.write("\n")
                order += 1

        f.close()


class Closeness():
    def __init__(self):
        dictdictcloseness = {}

        for no1 in range(1, MAXNO+1) :
            dictcloseness = {}
            for no2 in range(no1+1, MAXNO+1):
                dictcloseness[no2] = 0
            dictdictcloseness[no1] = dictcloseness
        self.dictdictcloseness = dictdictcloseness

        self.listlistsortcloseness1to1 = []

    def __str__(self):
        outstring = ""
        for no1 in range(1, MAXNO+1) :
            outstring += str(no1) + ":"
            dictcloseness = self.dictdictcloseness[no1]
            for no2 in range(no1+1, MAXNO+1):
                outstring += str((no2,dictcloseness[no2] )) + ","
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

    def getlistcloseness(self, listnos):
        if len(listnos) in [0,1]  :
            return [1]
        return  [self.getcloseness( bb[0], bb[1] ) for bb in itertools.combinations(listnos, 2)]


    def createCloseness1to1(self, listlistInningNos) :
        # create the closeness between 2 numbers of Inningnos ,and create  at self.dictdictcloseness
        for listweekno in listlistInningNos :
            for tuplecombi in itertools.combinations(listweekno[1:], 2) :
                self.putcloseness(tuplecombi[0], tuplecombi[1])

    def createlistlistSortCloseness1to1(self):
        # sort Closeness1to1 according to closeness , and save to  self.listlistsortcloseness1to1
        listlistsortcloseness1to1 =[]
        for no1 in range(1, MAXNO+1) :
            for no2 in range(no1+1, MAXNO+1):
                listlistsortcloseness1to1.append([self.dictdictcloseness[no1][no2], no1, no2])

        self.listlistsortcloseness1to1 =  sorted(listlistsortcloseness1to1, key=lambda closeness2pair : closeness2pair[0], reverse= True)

    def getlistlistSortCloseness1to1(self):
        return self.listlistsortcloseness1to1

    def createddictcombi4rest1to1closeness(self, listlistInningNos):
        self.ddictcombi4to1closeness = collections.defaultdict(int)
        for listinningnos in listlistInningNos :
            for tuplecombi4 in itertools.combinations(listinningnos[1:], 4) :
                for rest1 in (set(listinningnos[1:])-set(tuplecombi4)) :
                    self.ddictcombi4to1closeness[tuplecombi4,rest1] += 1

    def writeddictcombi4rest1to1closeness(self, filename='combi4rest1to1closeness.csv'):
        if not hasattr(self, "ddictcombi4to1closeness") :
            print("ddictcombi4to1closeness is not exist")
            return
        listcombi4to1closenesssorted =  sorted( self.ddictcombi4to1closeness.items(), key=lambda  combi4to1close: combi4to1close[1], reverse=True )

        f = open(filename, "w")
        for combi4to1closeness in listcombi4to1closenesssorted :
            combi4to1, closeness = combi4to1closeness
            combi4, to1 = combi4to1
            f.write(str(combi4) + ",")
            f.write(str(to1) + ",")
            f.write(str(closeness) + "\n")
            # f.write(",".join[str(combi4), str(to1), str(closeness)] + "\n")
        f.close()

    def getlistFoundFromListCloseness2pair(self,no,noexcept,depth=1):
        if len(self.listlistsortcloseness1to1) == 0 :
            print("len of ListCloseness2pair is 0 ")
            exit()
        listret = []
        depthvalue = 0
        depthcount = 0
        for listcloseness2pair in self.listlistsortcloseness1to1 :
            if no in listcloseness2pair[1:] :
                if noexcept in listcloseness2pair[1:] :     # skip
                    continue
                if depthvalue != listcloseness2pair[0] :
                    depthcount += 1
                    depthvalue = listcloseness2pair[0]
                if depthcount > depth :
                    break
                listret.append(listcloseness2pair)
        return listret



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

    tableinningno = TableInningNo("lotto.csv")
    listlistinningnos = tableinningno.getlistlistInningNos()      # 차수, 당첨번호 list

    # tableinningno.writelisttupleNoFreqSorted()
    # tableinningno.writelistdictModBalanceWithTable()

    # print modbalance with all of inning
    # listdictinningmods = tableinningno.getlistdictModBalanceWithTable()
    # pprint.pprint(listdictinningmods, width=200)

    # 각 회차에서 같이 나왔던 회수 구하기.(친밀성 구하기 )
    closeness = Closeness()
    closeness.createCloseness1to1(listlistinningnos)
    # print("closeness of two number ")
    # print(closeness)

    # 가장 높은 친밀도를 가진 2 숫자의 조합을 print.
    # closeness.createlistlistSortCloseness1to1()
    # pprint.pprint ( closeness.getlistlistSortCloseness1to1() )

    closeness.createddictcombi4rest1to1closeness(listlistinningnos)
    closeness.writeddictcombi4rest1to1closeness()

    exit()
    tableinningno.writeCombiMatchwithTable(3,closeness)

    exit()

    tupleNoFreqSorted = tableinningno.getlisttupleNoFreqSorted()      #  listtuple (당첨번호, 당첨회수 )
    # 1. 당첨회수가 많은 숫자와  1차 pair와 2차 pair .
    listdictFreqCloseClose=[]
    for NoFreq in tupleNoFreqSorted[0:3 ] :
        for listcloseness2pairFirst in closeness.getlistFoundFromListCloseness2pair(NoFreq[0],0, depth=2)[:10] :
            # Fstcloseness2pair : First order closeness2pair
            closeness2pairFirst_No = listcloseness2pairFirst[1] if listcloseness2pairFirst[1] != NoFreq[0] else listcloseness2pairFirst[2]
            for listcloseness2pairSecond in closeness.getlistFoundFromListCloseness2pair(closeness2pairFirst_No,NoFreq[0], depth=2)[:10] :
                # Seccloseness2pair : Second order closeness2pair
                closeness2pairSecond_No = listcloseness2pairSecond[1] if listcloseness2pairSecond[1] != closeness2pairFirst_No else listcloseness2pairSecond[2]

                print("Rank No : %s, first pair: %s, second pair : %s"%(NoFreq[0],closeness2pairFirst_No, closeness2pairSecond_No ))
                dicttemp = {}
                dicttemp["No1"] = NoFreq[0]
                dicttemp["No1Feq"] = NoFreq[1]
                dicttemp["No2"] = closeness2pairFirst_No
                dicttemp["No2Close1"] = listcloseness2pairFirst[0]
                dicttemp["No3"] = closeness2pairSecond_No
                dicttemp["No3Close2"] = listcloseness2pairSecond[0]
                dicttemp["total"] = NoFreq[1] + listcloseness2pairFirst[0] + listcloseness2pairSecond[0]

                listdictFreqCloseClose.append(dicttemp)

    listdictFreqCloseClose = sorted(listdictFreqCloseClose, key=lambda dictFreqCloseClose: dictFreqCloseClose["total"], reverse=True)

    #  이렇게 조사된  pair가 실질적으로 효과가 있는지 이전의 회차에서 조사한다.
    for  dictFreqCloseClose in listdictFreqCloseClose :
        dictFreqCloseClose["tablematchcount"] = tableinningno.getMatchingCombiCount([ dictFreqCloseClose["No1"],dictFreqCloseClose["No2"],dictFreqCloseClose["No3"] ])

    pprint.pprint(listdictFreqCloseClose, width=200 )
    exit()


    # 각 번호별 다음회차에 나올 확률구하기
    nextsel = calNextSelectionStat()
    nextsel.makenextInning(listlistinningnos)
    print ( "calculation of number next occurance : ")
    print ( nextsel)

    #마지막 회차 기준으로 다음 회차에 나올 가능성을  listturple형태로 계산하고 sorting.tuple형태 : ( 번호, diffinning, 발생횟수)
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
        if no in listlistinningnos[-diffinning][1:] :
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






