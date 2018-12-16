# -*- coding: utf-8 -*-
from operator import itemgetter
import itertools
import collections
import pprint
MAXNO = 45
SELNO = 6
MAXDIFFINNING = 60

class CLSVAR():
    def __init__(self):
        pass

class TableInningNo():
    def __init__(self, filecsv):
        self.listlistinningnos = []         # [[inning, no1,on2,no3,no4,no5,no6],[...],...]

        self.listtupleNoFreqSorted = []     # [(no1, freq),(no2,freq),...]  sorted on freq
                                            #  번호당 출현 회수를 저장
                                            # 관련함수 : writelisttupleNoFreqSorted

        for line in open(filecsv):
            if len(line.split()) ==0 :
                continue
            listno = [int(aa) for aa in line.split(",")]
            self.listlistinningnos.append( listno )

        # sorting based on inning
        self.listlistinningnos = sorted(self.listlistinningnos, key=lambda listInningNos: listInningNos[0] )
        self.createlisttupleNoFreqSorted()          # self.listtupleNoFreqSorted 을 생성한다.

    def getlistlistInningNos(self):
        '''
        listlistinningnos을 반환한다.
        :return:
        '''
        return self.listlistinningnos

    # Region : listtupleNoFreqSorted --------------------------------------------------------
    # 숫자 1개에 대한 통계.

    def createlisttupleNoFreqSorted(self):
        '''
        45개의 숫자에 대한 발생빈도를 조사하여 sort하고, listtupleNoFreqSorted 에 저장한다.
        :return:
        '''
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

    # Region : --------------------------------------------------------
    # nCombi 1개에 대한 통계.

    def  GetDictCombiFreq(self, nCombi):
        '''
        self.listlistinningnos을 활용하여 ,
        6개의 숫자에서 추출된 combi 의 발생빈도를 계산한다.

        :param nCombi:
        :return:
        '''

        # count dict 을 생성 : key:combi, value=freq
        cdictCombiFrequency = collections.Counter()
        for listinningnos in self.listlistinningnos:
            for tuplecombi in itertools.combinations(listinningnos[1:], nCombi):
                cdictCombiFrequency[tuplecombi] += 1

        return cdictCombiFrequency

    def GetDictFreqListCombi(self, nCombi):
        """
        self.listlistinningnos을 활용하여 ,
        6개의 숫자에서 추출된 combi 의 발생빈도를 계산한다.

        return 값은 defaultdict으로  key= 발생빈도, value=  combi의 list

        :param nCombi: combination 숫자
        :return: defaultdict으로  key= 발생빈도, value=  combi의 list
        """

        # count dict 을 생성 : key:combi, value=freq
        cdictCombiFrequency = collections.Counter()
        for listinningnos in self.listlistinningnos :
            for tuplecombi in itertools.combinations ( listinningnos[1:], nCombi) :
                cdictCombiFrequency[tuplecombi] += 1


        # defaultdict 생성 :  key:freq  value= list[combi]
        ddictFreqListcombi = collections.defaultdict(list)
        for tuplecombifreq  in cdictCombiFrequency.items() :
            tuplecombi, freq = tuplecombifreq
            ddictFreqListcombi[freq].append(tuplecombi)

        return ddictFreqListcombi

    # Region : --------------------------------------------------------
    def writeCombiMatchwithTable(self, combi, combiinside, combirest, clsvar, filecsv='combimatch.csv'):
        '''
        목적 : combi-n이 다른 회에도 나타나는지 조사해서 파일에 write한다.

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

        filecsv = (str(combi) + str(combiinside)+str(combirest) +".").join(filecsv.split("."))
        listlistmax = []            # list of max-reproduced combi pair
        listlistmax_1 = []          # list of max-1-reproduced combi pair
        # listlistmax format
        # [[(combi), inning1, inning2, ..]],[(combi), inning3, inning4], [...],... ]

        lenmax = 0                  # max count of len( listlistmax[0][1:] )  , max count of inning1, inning2, ...
        lenmax_1 = 0                # max count of len( listlistmax_1[0][1:] )  , max count of inning3, inning4, ...

        lenlistlistinningnos = len(self.listlistinningnos)
        for idx in range(lenlistlistinningnos) :
            if idx % 100 == 0  :
                print("\n")
            print(".", end="")

            # idx  :  first index of self.listlistinningnos
            # idx2 :  second index of self.listlistinningnos
            listidx2 = [aa for aa in range(lenlistlistinningnos)]
            listidx2.remove(idx)
            listfindtuplecombi = [bb for bb in itertools.combinations(self.listlistinningnos[idx][1:], combi )]
            for findtuplecombi in listfindtuplecombi :
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

        combinrestnclose= 0
        if clsvar != None :
            # combinrestnclose = clsvar.combi1rest1close
            if combiinside == 4 and combirest == 2  :
                combinrestnclose = clsvar.combi4rest2close
            elif combiinside == 4 and combirest == 1  :
                combinrestnclose = clsvar.combi4rest1close
            elif combiinside == 3 and combirest == 2  :
                combinrestnclose = clsvar.combi3rest2close
            elif combiinside == 3 and combirest == 1  :
                combinrestnclose = clsvar.combi3rest1close
            elif combiinside == 2 and combirest == 1  :
                combinrestnclose = clsvar.combi2rest1close
            elif combiinside == 2 and combirest == 2  :
                combinrestnclose = clsvar.combi2rest2close
            elif combiinside == 1 and combirest == 1  :
                combinrestnclose = clsvar.combi1rest1close
            else:
                print("error of combination and rest parameter")


        strcombi = ["C" + str(aa) for aa in range(1,combi+1)]
        strdiffno = ["D" + str(aa) for aa in range(1, 6-combi + 1 )]
        strdiffno.append("D_sum")
        f.write("countfound" +","+ ",".join(strcombi) + "," + "order,inning,C_sum,no1,no2,no3,no4,no5,no6,sum," + ",".join(strdiffno) + "," )
        if combinrestnclose != None :
            lendiffcombi = len([aa for aa in itertools.combinations(range(6-combi),2 )])
            strdiffnoclose = [ "DClo" + str(aa) for aa in range(lendiffcombi)]
            f.write(",".join(strdiffnoclose) + ",")
        f.write("\n")

        listcombiidxscombiinsidecombirestclosenessMax = []
        for listcombiidxs in listlistmax :
            tuplecombi = list(listcombiidxs[0])
            order = 1
            for inning in listcombiidxs[1:] :
                listnos = self.listlistinningnos[inning][1:]

                # write Combination , order, inning, c_sum
                f.write(str(lenmax) + ","+ ",".join([str(aa) for aa in tuplecombi])+","+str(order) +","+ str(inning+1)+"," + str(sum(tuplecombi)) + ",")

                # write nos , sum
                f.write(",".join([str(aa) for aa in listnos]) + ","+ str(sum(listnos)) + "," )

                listrest = list(set(listnos)-set(tuplecombi))
                listrest.sort()

                # write rest
                f.write(",".join([str(aa) for aa in listrest]) + "," + str(sum(listrest)) + ",")

                # write the info of closeness
                if clsvar != None :
                    for tuplepair in itertools.combinations( list(tuplecombi), combiinside) :
                        for tuplerest in itertools.combinations( listrest, combirest) :
                            closeness = combinrestnclose.getcloseness(list(tuplepair), list(tuplerest))
                            listcombiidxscombiinsidecombirestclosenessMax.append([listcombiidxs,tuplepair,tuplerest,closeness  ])
                            f.write(str(closeness)   + ",")
                f.write("\n")
                order += 1

        listcombiidxscombiinsidecombirestclosenessMax_1 = []
        for listcombiidxs in listlistmax_1 :
            tuplecombi = list(listcombiidxs[0])
            order = 1
            for inning in listcombiidxs[1:] :
                listnos = self.listlistinningnos[inning][1:]

                # write Combination , order, inning, c_sum
                f.write(str(lenmax_1) + ","+ ",".join([str(aa) for aa in tuplecombi])+","+str(order) +","+ str(inning+1)+"," + str(sum(tuplecombi)) + ",")

                # write nos , sum
                f.write(",".join([str(aa) for aa in listnos]) + ","+ str(sum(listnos)) + "," )

                listrest = list(set(listnos)-set(tuplecombi))
                listrest.sort()

                # write rest
                f.write(",".join([str(aa) for aa in listrest]) + "," + str(sum(listrest)) + ",")

                # write the info of closeness
                if clsvar != None :
                    for tuplepair in itertools.combinations( list(tuplecombi), combiinside) :
                        for tuplerest in itertools.combinations( listrest, combirest) :
                            closeness = combinrestnclose.getcloseness(list(tuplepair), list(tuplerest))
                            listcombiidxscombiinsidecombirestclosenessMax_1.append([listcombiidxs,tuplepair,tuplerest,closeness  ])
                            f.write(str(closeness)   + ",")
                f.write("\n")
                order += 1

        if len(listlistmax_1) == 0 :
            f.close()

        # listcombiidxscombiinsidecombirestclosenessMax_1 - listcombiidxscombiinsidecombirestclosenessMax
        # if combination of combiinside and combirest is same
        # and if the closeness of Max_1 is same or greater than Max .

        listtodelete = []
        for combiidxscombiinsidecombirestclosenessMax_1 in listcombiidxscombiinsidecombirestclosenessMax_1 :
            combiidxsMax_1, combiinsideMax_1, combirestMax_1, closenessMax_1 = combiidxscombiinsidecombirestclosenessMax_1
            for combiidxscombiinsidecombirestclosenessMax in listcombiidxscombiinsidecombirestclosenessMax :
                combiidxsMax, combiinsideMax, combirestMax, closenessMax = combiidxscombiinsidecombirestclosenessMax
                if combiinsideMax_1 == combiinsideMax and combirestMax_1 == combirestMax and closenessMax_1 >= closenessMax :
                    listtodelete.append(combiidxscombiinsidecombirestclosenessMax_1)

        print("len of combiidxscombiinsidecombirestclosenessMax_1 to delete is %s" % (len(listtodelete)))
        for combiidxscombiinsidecombirestclosenessMax_1 in listtodelete :
            combiidxsMax_1, combiinsideMax_1, combirestMax_1, closenessMax_1 = combiidxscombiinsidecombirestclosenessMax_1
            try:
                listlistmax_1.remove(combiidxsMax_1)
            except:
                continue

        print("len of listlistmax_1 after deleting is %s" % (len(listlistmax_1)))
        # print the combiidxscombiinsidecombirestclosenessMax_1
        for listcombiidxs in listlistmax_1 :
            tuplecombi = list(listcombiidxs[0])

            # calculte the max number of intersection count of tuplecombi with listlistmax_1
            maxintersection = max( [len(set(tuplecombi).intersection(set(listcombiidxs[0]))) for listcombiidxs in listlistmax])
            isection = "isection%s"%maxintersection
            for inning in listcombiidxs[1:] :
                listnos = self.listlistinningnos[inning][1:]

                # write Combination , order, inning, c_sum
                f.write("D" + ","+ ",".join([str(aa) for aa in tuplecombi])+","+str(isection) +","+ str(inning+1)+"," + str(sum(tuplecombi)) + ",")

                # write nos , sum
                f.write(",".join([str(aa) for aa in listnos]) + ","+ str(sum(listnos)) + "," )

                listrest = list(set(listnos)-set(tuplecombi))
                listrest.sort()

                # write rest
                f.write(",".join([str(aa) for aa in listrest]) + "," + str(sum(listrest)) + ",")

                # write the info of closeness
                if clsvar != None :
                    for tuplepair in itertools.combinations( list(tuplecombi), combiinside) :
                        for tuplerest in itertools.combinations( listrest, combirest) :
                            closeness = combinrestnclose.getcloseness(list(tuplepair), list(tuplerest))
                            f.write(str(closeness)   + ",")
                f.write("\n")

        f.close()

class InningModuleBalnace:
    def _init__(self, listlistinningnos):
        self.listlistinningnos = listlistinningnos
        self.listdictinningmods = []  # [{inning,mod2balance,mod3balance,mod5balance,mod9balance,modsumbalance, sum}, {...}, ...]

        self.CreateListDictModBalance()  # self.listdictinningmods 을 생성한다.
        # 회차별  2,3,5,9 modulation 의 balance을  list을 저장되어 있다.
        # 관련 함수 : getlistdictModBalanceWithTable, writelistdictModBalanceWithTable

    def getMod2Balance(self, listnos):
        '''
        받은 번호들을 각각  2 modulation했을 때,  modulation 종류 별로 같은 수의 개수가 있다면 balance가 되었다고 true을 return한다.
        :param listnos:
        :return:
        '''
        listtemp = [aa % 2 for aa in listnos]
        countmod0 = listtemp.count(0)
        countmod1 = listtemp.count(1)
        return True if countmod0 == countmod1 else False

    def getMod3Balance(self, listnos):
        '''
        받은 번호들을 각각  3 modulation했을 때,  modulation 종류 별로 같은 수의 개수가 있다면 balance가 되었다고 true을 return한다.
        :param listnos:
        :return:
        '''
        listtemp = [aa % 3 for aa in listnos]
        countmod0 = listtemp.count(0)
        countmod1 = listtemp.count(1)
        countmod2 = listtemp.count(2)
        return True if countmod0 == countmod1 and countmod1 == countmod2 else False

    def getMod5Balance(self, listnos):
        listtemp = [aa % 5 for aa in listnos]
        countmod0 = listtemp.count(0)
        countmod1 = listtemp.count(1)
        countmod2 = listtemp.count(2)
        countmod3 = listtemp.count(3)
        countmod4 = listtemp.count(4)
        listcheck = []
        listcheck.append(countmod0 in [1, 2])
        listcheck.append(countmod1 in [1, 2])
        listcheck.append(countmod2 in [1, 2])
        listcheck.append(countmod3 in [1])
        listcheck.append(countmod4 in [1, 2])
        return True if all(listcheck) == True else False

    def getMod9Balance(self, listnos):
        listtemp = [aa % 5 for aa in listnos]
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
        listcheck.append(countmod0 in [0, 1])
        listcheck.append(countmod1 in [0, 1])
        listcheck.append(countmod2 in [0, 1])
        listcheck.append(countmod3 in [0, 1, 2])
        listcheck.append(countmod4 in [0, 1, 2])
        listcheck.append(countmod5 in [0, 1])
        listcheck.append(countmod6 in [0, 1])
        listcheck.append(countmod7 in [0, 1])
        listcheck.append(countmod8 in [0, 1])

        return True if all(listcheck) == True else False

    def CreateListDictModBalance(self):
        '''
        회차별  2,3,5,9 modulation의 balance 결과를  listdict type으로  반환한다.
        :return:
        '''
        listdictinningmods = []
        for listinningnos in self.listlistinningnos:
            dicttemp = {}
            dicttemp["inning"] = listinningnos[0]
            dicttemp["mod2"] = self.getMod2Balance(listinningnos[1:])
            dicttemp["mod3"] = self.getMod3Balance(listinningnos[1:])
            dicttemp["mod5"] = self.getMod5Balance(listinningnos[1:])
            dicttemp["mod9"] = self.getMod9Balance(listinningnos[1:])
            dicttemp["modsum"] = all([dicttemp["mod2"], dicttemp["mod3"], dicttemp["mod5"], dicttemp["mod9"]])
            dicttemp["sum"] = sum(listinningnos[1:])
            listdictinningmods.append(dicttemp)

        self.listdictinningmods = listdictinningmods

    def GetListDictInningModuleBance(self):
        return self.listdictinningmods

    def WriteListDictModBalanceWithTable(self, filecsv='modbal.csv'):
        f = open(filecsv, 'w')
        f.write("inning,no1,no2,no3,no4,no5,no6,mod2,mod3,mod5,mod9,modsum,sum\n")
        leninningnos = len(self.listlistinningnos)
        for idx in range(leninningnos):
            f.write(",".join([str(aa) for aa in self.listlistinningnos[idx]]) + ",")
            dicttemp = self.listdictinningmods[idx]
            f.write(str(dicttemp["mod2"]) + ",")
            f.write(str(dicttemp["mod3"]) + ",")
            f.write(str(dicttemp["mod5"]) + ",")
            f.write(str(dicttemp["mod9"]) + ",")
            f.write(str(dicttemp["modsum"]) + ",")
            f.write(str(dicttemp["sum"]) + "\n")
        f.close()

class CombiFrom45:
    def _init__(self ):
        return

    def GetListCombiFrom45(self, nCombi):
        '''
        45개의 숫자에서  nCombi 조합에 해당하는 combination을 만들어 반환한다.
        :param nCombi:
        :return:
        '''
        listtuplecombi = []
        for tuplecombi in itertools.combinations(range(1, MAXNO+1), nCombi):
            listtuplecombi.append(tuplecombi)
        return listtuplecombi



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

    def makeListtupleNumInningOccurs(self):
        #마지막 회차 기준으로 다음 회차에 나올 가능성을  listtuple형태로 계산
        listtupleNumInningOccurs = []
        for no in range(1, MAXNO+1) :
            for diffinning in range(1, MAXDIFFINNING + 1) :
                listtupleNumInningOccurs.append((no, diffinning,self.dictdictdiffInning[no][diffinning] ))
        return listtupleNumInningOccurs

class   CombiRestCloseness():
    """
    6개의 숫자에서 관심의 combi (combination) 와 rest(나머지)에 대한  친밀도(closeness = 발현된 회수 )을  구하고 이를 sort해서
    self.listcombinrestnclosesorted 에 저장한다.
    """
    def __init__(self, listlistinningnos, combin, restn):
        if combin < restn  or (combin + restn) >= 6 :
            print("parameter error : combin, restn")
            exit()

        self.combin = combin
        self.restn = restn
        self.ddictcombinrestncloseness = collections.defaultdict(int)
        for listinningnos in listlistinningnos :
            for tuplecombi in  itertools.combinations(listinningnos[1:], combin) :
                listtemp = list(tuplecombi)
                listtemp.sort()
                tuplecombi = tuple(listtemp)
                for tuplerest in itertools.combinations(set(listinningnos[1:]) - set(tuplecombi), restn ) :
                    listtemp = list(tuplerest)
                    listtemp.sort()
                    tuplerest = tuple(listtemp)
                    self.ddictcombinrestncloseness[tuplecombi,tuplerest ] += 1

        self.listcombinrestnclosesorted = sorted(self.ddictcombinrestncloseness.items(), key=lambda  combirestclose: combirestclose[1],reverse=True )

    def writecombirestclose(self, filename=""):
        if len(filename) == 0 :
            filename = "combi%srest%scloseness.csv"%(self.combin, self.restn)

        f = open(filename, "w")
        for combinrestnclose in self.listcombinrestnclosesorted :
            combinrestn, closeness = combinrestnclose
            tuplecombi, tuplerest = combinrestn
            f.write(str(tuplecombi) + ",")
            f.write(str(tuplerest) + ",")
            f.write(str(closeness) + "\n")
        f.close()

    def getcloseness(self, listcombi,listrestn):
        if len(listcombi) != self.combin  or len(listrestn) != self.restn :
            print("the length of parameter is not proper")
            exit()
        listcombi.sort()
        listrestn.sort()
        valret =  self.ddictcombinrestncloseness.get((tuple(listcombi), tuple(listrestn)), 0)
        if (valret == 0  ) :
            valret = self.ddictcombinrestncloseness.get((tuple(listrestn), tuple(listcombi)), 0)
        return valret

    def getlistbestrest(self, listcombi):
        """
        listcombi에 가장 closeness가 좋은 listrest을 찾아서 return 한다.
        :param listcombi:
        :return:
        """
        if not hasattr(self, "listcombinrestnclosesorted") :
            print("listcombinrestnclosesorted is not exist")
            exit()

        listcombi.sort()
        tupletemp = tuple(listcombi)
        for combinrestnclose in self.listcombinrestnclosesorted :
            combinrestn , close = combinrestnclose
            tuplecombi, tuplerest = combinrestn
            if tuplecombi == tupletemp :
                return list(tuplerest), close

    def getlisttupleSubordinateRest(self, listcombi):
        """
        최상의 closeness보다 1이 작은 closeness을 가지는 (listcombi, listrest) pair중에
        parameter의 listcombi에 pair인 rest의 list을 구하고 return한다.
        :param listcombi: 찾을 combi list
        :return:
        """

        if self.combin != len(listcombi) :
            return []

        # 먼저 closeness의 max을 구한다.
        max_1count = max(set(self.ddictcombinrestncloseness.values())) -1
        findcombit = sorted(listcombi)
        listtuplerest = []

        # listcombi가 같고, closeness가 max_1count인 rest을 구하고, list에 저장한다.
        for combinrestnclose in self.listcombinrestnclosesorted :
            combinrestn , close = combinrestnclose
            tuplecombi, tuplerest = combinrestn
            if max_1count == close and findcombit == sorted(tuplecombi) :
                listtuplerest.append(tuplerest)

        return listtuplerest

