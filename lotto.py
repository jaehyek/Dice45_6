# -*- coding: utf-8 -*-
#from operator import itemgetter
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
        self.dictNumFreq = {}               # { 1:freq, 2:freq, ... }
        self.dictSumFreq = {}               # {sum:freq, sum:freq, ... }
        self.listlistFreqSum = []           # { freq:sum, freq:sum, ... }  reversed ranking.

        self.listtupleNoFreqSorted = []     # [(no1, freq),(no2,freq),...]  sorted on freq
        self.listdictinningmods = []        # [{inning,mod2,mod3,mod5,mod9,modall, sum}, {...}, ...]

        for line in open(filecsv):
            if len(line.split()) ==0 :
                continue
            listno = [int(aa) for aa in line.split(",")]
            self.listlistinningnos.append( listno )

        # sorting based on inning
        self.listlistinningnos = sorted(self.listlistinningnos, key=lambda listInningNos: listInningNos[0] )
        self.createdictNumFreq()
        self.create_dictsumfreq()

        #--------------------------------------

        self.createlisttupleNoFreqSorted()
        self.createlistdictModBalanceWithTable()


    def getlistlistInningNos(self):
        return self.listlistinningnos

    def getNosWithInning(self, inning):
        return self.listlistinningnos[inning-1][1:]

    def createdictNumFreq(self):
        '''
        dict을 만들어서, 주어진 숫자에 대해  빈도수를 알수 있도록 한다.
        :return:
        '''
        dictNumFreq = collections.defaultdict(int)
        for listno in self.listlistinningnos:
            for no in listno[1:]:
                dictNumFreq[int(no)] += 1

        self.dictNumFreq = dictNumFreq ;

    def get_Probability_from_dictNumFreq(self, listnos):
        '''
        listnos의 6개의 숫자 각각이 나타났던 빈도수를 합하여 percentage으로 return한다.
        :param listnos:
        :return:
        '''

        ## 먼저 전체 숫자 개수를 구한다.
        ntotal = len(self.listlistinningnos) * 6

        ## 각각의 숫자에 대해 빈도수를 구한다.
        nsubtotal = 0
        for no in listnos :
            nsubtotal += self.dictNumFreq[no]

        return nsubtotal / ntotal


    def get_Modn_Probability(self, Modn, listnos):
        '''
        각 innning 별로, 6 숫자들을 Modular 을 했을 때,
        Mod0 =개수 Mod1=개수 를 dict type key으로 하고, 해당 빈도수를 개수로 count하며,
        parameter listno에 대해 percentage을 return한다.

        예를 들면,  mod 3 인 경우  mod0:1개, mod1:2개, mod2:3개 나올 수 있고,
        key value 는 "123"이 된다.  아래 dictModstrCount는 key에 해당하는 빈도수를 count한다.

        return 값은  parameter listno을  key으로 변환하고,  dictModstrCount에서 찾아서
        전체 대비, percentage 값으로 반환한다.

        그리고 반복하여 call 경우을 대비하여,  각 Modn에 대비 strAttributename에
        통계정보인 dictModstrCount를 저장한다.

        :param Modn: modular n
        :param listnos:
        :return:
        '''

        # 먼저 class내에 dictModstrCount_Modn 이라는 attribute가 있는지 확인하다.
        strAttributename = "dictModstrCount_" + str(Modn)
        if not hasattr(self, strAttributename) :
            dictModstrCount = collections.defaultdict(int)
            for listinningnos in self.listlistinningnos :
                listmodcount = [ 0 for aa in range(Modn)]
                for no in listinningnos[1:] :
                    listmodpos = no % Modn
                    listmodcount[listmodpos] += 1
                # mod type 을  str형태로 key을 만든다.
                modkey = "".join([str(aa) for aa in listmodcount])
                dictModstrCount[modkey] += 1

            self.__dict__[strAttributename] = dictModstrCount
        else:
            dictModstrCount = self.__dict__[strAttributename]

        # parameter에 대한 key str 을 생성
        listmodcount = [0 for aa in range(Modn)]
        for no in listnos:
            listmodpos = no % Modn
            listmodcount[listmodpos] += 1
        modkey = "".join([str(aa) for aa in listmodcount])
        freq = dictModstrCount.get(modkey, 0)


        return freq / len(self.listlistinningnos)


    def create_dictsumfreq(self):
        '''
        각 inning에 포함된 모든 숫자를 더하여,  합에 대해 빈도수를 찾을 수 있도록
        :return:
        '''

        dictSumFreq = collections.defaultdict(int)
        for listinningnos in self.listlistinningnos:
            dictSumFreq[sum(listinningnos[1:])] += 1

        self.dictSumFreq = dictSumFreq;

        # 순위를 만들어 저장한다.
        listlistFreqSum = []
        for ssum, freq in dictSumFreq.items() :
            listlistFreqSum.append([freq, ssum])
        self.listlistFreqSum = sorted(listlistFreqSum, key=lambda  listfreqsum: listfreqsum[0], reverse=True)

    def get_Probability_from_dictSumFreq(self, listnos):
        '''
        parameter listnos의 합에 해당하는 빈도수를 구하고, 확률을 return한다.
        :param listnos:
        :return:
        '''
        return self.dictSumFreq[sum(listnos)] / len(self.listlistinningnos)

    def get_bestcombi6_from_listfreqsum(self, listcombi5):
        '''
        combi5을 이용하여 combi6을 구성할 때, listfreqsum을 이용하여 최적의 combi6을 만들어서
        return한다.  ranking 정보와 함께.
        :param listcombi5:
        :return:
        '''
        sum5 = sum(listcombi5)
        listcombi6 = listcombi5[:]
        ranking = -1 ;
        freqprev = 0
        for listFreqSum in self.listlistFreqSum :
            freq = listFreqSum[0]
            sum6 = listFreqSum[1]
            if freqprev != freq :
                ranking += 1
                freqprev = freq
            if sum5 < sum6 :
                no6 = sum6 - sum5
                if not no6 in range(1, MAXNO+1) :
                    continue
                if no6 in listcombi5 :
                    continue
                listcombi6 = listcombi5[:]
                listcombi6.append(no6)
                listcombi6.sort()
                return listcombi6, ranking
        listcombi6.append(0)
        return listcombi6, -1



    # ========================================================


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

        del dictNumFreq

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
        '''
        숫자 6개를   MOd=2 을 적용시,
        :param listnos:
        :return:
        '''
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
        dicttemp["modall"] = all([dicttemp["mod2"],dicttemp["mod3"],dicttemp["mod5"],dicttemp["mod9"]])
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
            dicttemp["modall"] = all([dicttemp["mod2"],dicttemp["mod3"],dicttemp["mod5"],dicttemp["mod9"]])
            dicttemp["sum"] = sum(listinningnos[1:])
            listdictinningmods.append(dicttemp)

        self.listdictinningmods = listdictinningmods

    def getlistdictModBalanceWithTable(self):
        return self.listdictinningmods

    def writelistdictModBalanceWithTable(self, filecsv='modbal.csv'):
        f = open(filecsv, 'w')
        f.write("inning,no1,no2,no3,no4,no5,no6,mod2,mod3,mod5,mod9,modall,sum\n")
        leninningnos = len(self.listlistinningnos)
        for idx in range(leninningnos) :
            f.write(",".join([str(aa)for aa in self.listlistinningnos[idx] ]) + ",")
            dicttemp = self.listdictinningmods[idx]
            f.write(str(dicttemp["mod2"]) + ",")
            f.write(str(dicttemp["mod3"]) + ",")
            f.write(str(dicttemp["mod5"]) + ",")
            f.write(str(dicttemp["mod9"]) + ",")
            f.write(str(dicttemp["modall"]) + ",")
            f.write(str(dicttemp["sum"]) + "\n")
        f.close()

    def writeCombiMatchwithTable(self, combi, combiinside, combirest, clsvar, filecsv='combimatch.csv'):
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
                f.write(str(lenmax) + "," + ",".join([str(aa) for aa in tuplecombi]) +"," + str(order) +"," + str(inning+1) +"," + str(sum(tuplecombi)) + ",")

                # write nos , sum
                f.write(",".join([str(aa) for aa in listnos]) + "," + str(sum(listnos)) + ",")

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
                f.write(str(lenmax_1) + "," + ",".join([str(aa) for aa in tuplecombi]) +"," + str(order) +"," + str(inning+1) +"," + str(sum(tuplecombi)) + ",")

                # write nos , sum
                f.write(",".join([str(aa) for aa in listnos]) + "," + str(sum(listnos)) + ",")

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
                f.write("D" + "," + ",".join([str(aa) for aa in tuplecombi]) +"," + str(isection) +"," + str(inning+1) +"," + str(sum(tuplecombi)) + ",")

                # write nos , sum
                f.write(",".join([str(aa) for aa in listnos]) + "," + str(sum(listnos)) + ",")

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

    def getdictFreqListcombi(self, combi):
        """
        self.listlistinningnos을 활용하여 , 
        6개의 숫자에서 추출된 combi 의 발생빈도를 계산한다.
        return 값은 defaultdict으로  key= 발생빈도, value=  combi의 list
        
        cdictCombiFrequency : 저장소로,  type은 Dict type의 Counter.
        setCombiFrequency : set type으로  빈도의 수자의 set.
        
        :param combi: combination 숫자
        :return: defaultdict으로  key= 발생빈도, value=  combi의 list
        """
        cdictCombiFrequency = collections.Counter()
        for listinningnos in self.listlistinningnos :
            for tuplecombi in itertools.combinations ( listinningnos[1:], combi) :
                cdictCombiFrequency[tuplecombi] += 1

        # calculate the kind of combiFrequency
        setCombiFrequency = set(cdictCombiFrequency.values())
        # print(setCombiFrequency)

        ddictFreqListcombi = collections.defaultdict(list)
        for tuplecombifreq  in cdictCombiFrequency.items() :
            tuplecombi, freq = tuplecombifreq
            ddictFreqListcombi[freq].append(tuplecombi)

        return ddictFreqListcombi

class   MinNumFreq():
    '''
    6 숫자에서 가장 작은 숫자만의 빈도를 계산하고, 확률를 계산한다.
    '''
    def __init__(self, listlistinningnos):
        self.dictMinnumFreq = collections.defaultdict(int)
        self.listlistFreqMinnum = []
        self.totalnum = len(listlistinningnos)
        self.listEffectiveNum80 = []
        for listinningnos in listlistinningnos:
            self.dictMinnumFreq[listinningnos[1]] += 1

        # [[freq, Minnum], [freq, Minnum],[freq, Minnum], ...] 을 생성및 sort
        for minnum, freq in self.dictMinnumFreq.items():
            self.listlistFreqMinnum.append([freq, minnum])

        # sorting
        self.listlistFreqMinnum = sorted(self.listlistFreqMinnum, key= lambda listfreqnum: listfreqnum[0], reverse=True)

        # 누적하여 80%의 빈도에 해당하는 숫자만 유효한 것으로 판단하여, 그 해당하는 num list을 만든다.
        maxaccum = self.totalnum * 0.8
        accum = 0
        for freq, minnum in self.listlistFreqMinnum :
            if accum <= maxaccum :
                self.listEffectiveNum80.append(minnum)
            else :
                break
            accum += freq

    def __str__(self):
        outstring = ""
        for FreqMinnum in self.listlistFreqMinnum:
            outstring += str(FreqMinnum) + ",\n"
        return outstring

    def get_Minnum_Probability(self, Minnum):
        # 만일 Minnum가 self.listEffectiveNum80 에 해당되지 않는다면, 0 을 return한다.
        if not Minnum in self.listEffectiveNum80 :
            return 0
        freq = self.dictMinnumFreq.get(Minnum, 0 )
        return freq / self.totalnum

    def get_listEffectiveNum80(self):
        return self.listEffectiveNum80

class   MaxNumFreq():
    '''
    6 숫자에서 가장 큰 숫자만의 빈도를 계산하고, 확률를 계산한다.
    '''
    def __init__(self, listlistinningnos):
        self.dictMaxnumFreq = collections.defaultdict(int)
        self.listlistFreqMaxnum = []
        self.totalnum = len(listlistinningnos)
        self.listEffectiveNum80 = []
        for listinningnos in listlistinningnos:
            self.dictMaxnumFreq[listinningnos[-1]] += 1

        # [[freq, Maxnum], [freq, Maxnum],[freq, Maxnum], ...] 을 생성및 sort
        for Maxnum, freq in self.dictMaxnumFreq.items():
            self.listlistFreqMaxnum.append([freq, Maxnum])

        # sorting
        self.listlistFreqMaxnum = sorted(self.listlistFreqMaxnum, key= lambda listfreqnum: listfreqnum[0], reverse=True)

        # 누적하여 80%의 빈도에 해당하는 숫자만 유효한 것으로 판단하여, 그 해당하는 num list을 만든다.
        maxaccum = self.totalnum * 0.8
        accum = 0
        for freq, Maxnum in self.listlistFreqMaxnum :
            if accum <= maxaccum :
                self.listEffectiveNum80.append(Maxnum)
            else :
                break
            accum += freq

    def __str__(self):
        outstring = ""
        for FreqMaxnum in self.listlistFreqMaxnum:
            outstring += str(FreqMaxnum) + ",\n"
        return outstring

    def get_Maxnum_Probability(self, Maxnum):
        # 만일 Maxnum가 self.listEffectiveNum80 에 해당되지 않는다면, 0 을 return한다.
        if not Maxnum in self.listEffectiveNum80 :
            return 0
        freq = self.dictMaxnumFreq.get(Maxnum, 0 )
        return freq / self.totalnum

    def get_listEffectiveNum80(self):
        return self.listEffectiveNum80

class PrimeFreq():
    '''
    소수(prime number)에 대해 그 빈도수를 구하고,  확률를 구한다.
    '''
    def __init__(self, listlistinningnos):
        self.listprime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
        self.dictPrimeFreq = collections.defaultdict(int)    # [[소수:발견된수],[소수:발견된수], ... ]
        self.listlistFreqPrime = []                         # [[발견된수, 소수],[발견된수, 소수],...]
        self.totalprime = 0         #  모든 inning에서 발견된 총 소수의 개수

        # inning내에  솟수가 포함한 개수에 대한 통계 --> prime의 개수 패턴에 의한 확률을 구하고자 함.
        self.listInningPrimeCount = [0, 0, 0, 0, 0, 0, 0]
        # self.listInningPrimeCount[0]  : inning 내에 소수가 포함되지 않은 inning의 수.
        # self.listInningPrimeCount[1]  : inning 내에 소수가 1개 포함한 inning의 수.

        for listinningnos in listlistinningnos :
            InningPrimeCount = 0
            for no in listinningnos[1:] :
                if no in self.listprime :
                    self.dictPrimeFreq[no] += 1
                    self.totalprime += 1
                    InningPrimeCount += 1
            self.listInningPrimeCount[InningPrimeCount] += 1

        totalinning = len(listlistinningnos)
        self.listInningPrimeCount = [ aa / totalinning for aa in self.listInningPrimeCount ]

        # list을 만들고, sort한다.
        for prime, freq in self.dictPrimeFreq.items() :
            self.listlistFreqPrime.append([freq, prime])

        # sort
        self.listlistFreqPrime = sorted(self.listlistFreqPrime, key=lambda  listfreqprime: listfreqprime[0], reverse=True)

    def __str__(self):
        outstring = ""
        for listFreqPrime in self.listlistFreqPrime :
            outstring += str(listFreqPrime) + ",\n"
        return outstring

    def get_listlistFreqPrime(self):
        return self.listlistFreqPrime

    def getPrimeProbability(self, prime):
        # 해당 prime에 해당하는  확률을 return.
        if not prime in self.listprime :
            return 0 ;
        count = self.dictPrimeFreq[prime]
        return count / self.totalprime

    def getPrime6Probability(self, listnos):
        '''
        6 개 숫자에 대해, 솟수가 있다면, 해당 확률을 받아서  합을 return한다.
        :param listnos:
        :return:
        '''
        return sum([self.getPrimeProbability(aa) for aa in listnos])

    def getPrimeCountPatternProbability(self, listnos):
        '''
        listnos 내의 소수의 개수를 구하고, 해당 확률을 return한다.
        :param listnos:
        :return:
        '''
        primecount = [ aa in self.listprime for aa in listnos].count(True)
        return self.listInningPrimeCount[primecount]

    def get_listInningPrimeCount(self):
        # inning별 발생한 소수의 개수에 대한 통계 return .
        return self.listInningPrimeCount



class   CombiCloseness():
    def __init__(self, ncombi,listlistinningnos ):
        '''
        6개의 숫자에서 n개의 combination을 tuple로 정의하고, 각 inning에서
        그 tuple이 반복해서 나타나는지 회수를 count하고, percentage을 반환한다.
        :param ncombi:
        :param listlistinningnos:
        '''
        self.ncombi = ncombi
        self.dictTuplecombiCount = {}
        self.combitotal = 0
        self.listlistCountTuplecombi = []


        dictTuplecombiCount = collections.defaultdict(int)
        for  listinningnos in listlistinningnos :
            for tuplecombi in itertools.combinations(listinningnos[1:],ncombi ) :
                dictTuplecombiCount[tuplecombi] += 1

        self.dictTuplecombiCount = dictTuplecombiCount
        ## 총 combi의 total은 6가지 숫자에서 combi의 경우의 수에  총 inning 의 수의 곱이다.
        self.combitotal = len([aa for aa in itertools.combinations(range(6), ncombi)]) * len(listlistinningnos)

        ## dictTuplecombiCount을 이용해서 [[count, (combi)],[count, (combi)], ... ] 을 만든다.
        ## 추가하여 count을 기준으로 sort을 한다.
        listlistCountTuplecombi = []
        for tuplecombi, count in dictTuplecombiCount.items():
            listlistCountTuplecombi.append([count, tuplecombi])

        self.listlistCountTuplecombi = sorted(listlistCountTuplecombi, key=lambda listcounttuple: listcounttuple[0], reverse=True)
        del listlistCountTuplecombi

    def __str__(self):
        outstring = ""
        for listCountTuplecombi in self.listlistCountTuplecombi :
            outstring += str(listCountTuplecombi) + ",\n"
        return outstring

    def getCombiProbability(self, tuplecombi):
        '''
        self.ncombi 개수의  listcombi에 해당하는 count 구하고 그 확률를 return한다.
        :param
        :return:
        '''
        if type(tuplecombi) != tuple :
            raise Exception("Not match the list type")

        if len(tuplecombi) != self.ncombi :
            raise Exception("Not Match the combi count")

        count = self.dictTuplecombiCount.get(tuplecombi, 0)
        return count / self.combitotal

    def getCombi6Probability(self, listcombi6):
        '''
        6개의 숫자 list을 받아서,  ncombi에 의한  재현 count을 확률로 반환한다.
        :param listcombi6:
        :return:
        '''

        if type(listcombi6) != list:
            raise Exception("Not match the list type")

        if len(listcombi6) != 6:
            raise Exception("Not Match the combi count")

        listcombi6.sort()

        probtotal = 0
        for tuplecombi in itertools.combinations(listcombi6, self.ncombi) :
            probtotal += self.getCombiProbability(tuplecombi)

        return probtotal

    def getlistlistCountTuplecombi(self):
        return self.listlistCountTuplecombi


    def getBestCombiFromGivenTuple(self, tuplenos):
        '''
        주어지는 두개의 숫자에 대해, 가장 확률이 놓은 best combi을 list으로 반환한다.
        :param no:
        :return:
        '''

        # 먼저 listnos의 개수는  self.ncombi 보다 개수가 작아야 한다.
        if len(tuplenos) >= self.ncombi :
            raise  Exception("Listnos의 개수가 너무 크다.")
            exit(0)

        found = False
        bestcount = 0
        listtuple = []
        for count, tuplecombi in self.listlistCountTuplecombi :
            if tuplenos in itertools.combinations(tuplecombi, len(tuplenos)) :
                if found == False : #처음 발견
                    found = True
                    bestcount = count
                    listtuple.append(tuplecombi)
                else :              # 계속 search중
                    if bestcount == count :     # 추가 발견
                        listtuple.append(tuplecombi)
                    else:
                        # 발생빈도가 더 낮은 것이 발견이 되었으므로, search stop한다.
                        break
        return listtuple




'''
전략1)
    . 6개의 숫자중 min 숫자의  freq을 구하고,  그 중 순위별로 누적했을 때, 80%에 드는 숫자를  후보자로 선택 - min
    . 6개의 숫자중 max 숫자의  freq을 구하고,  그 중 순위별로 누적했을 때, 80%에 드는 숫자를  후보자로 선택 - max
    . min max을 합하고, 이 중 2 숫자를 추출하여 combi2하고  combi2에 대해 closessness 구하여, 순위를 별로, 20% 에 드는 
       combi2을 산출한다.
    . 앞에서 combi2을 산출했으므로,  45개의 숫자 중에   min max에 해당하는 숫자범위를 제거한 나머지에 대해, combi4을 형성하고, 
        combi4 closeness을 산출한다.   이 중에서, 상위 20%에 해당하는 combi4 을 선택한다. 
    . for loop을 시행하면서 combi2, combi4의  조합으로 combi6을 형성하고, combi6에 대해    
        get_Probability_from_dictNumFreq()      --> 각 숫자의 빈도수에 대한 확률의 합.
        get_Modn_Probability(2, listcombi6)     --> mod 2을 했을 때, pattern에 의한 확률
        get_Modn_Probability(3, listcombi6)     --> mod 3을 했을 때, pattern에 의한 확률
        get_Modn_Probability(5, listcombi6)     --> mod 5을 했을 때, pattern에 의한 확률
        get_Modn_Probability(7, listcombi6)     --> mod 7을 했을 때, pattern에 의한 확률
        get_Modn_Probability(9, listcombi6)     --> mod 9을 했을 때, pattern에 의한 확률
        getPrimeCountPatternProbability(listcombi6) --> 소수 발생빈도 pattern에 의한 확률
        을 시행하고 나온 각 확률을 곱하여 나온 값으로 순위로 매기고, 최상위 10개만 print한다. 
        
전략2)
    .전략1에서는 min max을 구하고, 이를 합쳐고 그 중 2숫자로 combi2을 형성하면,   min max의 조합으로 반드시
        이루어 지지 않는다.   전략2에서는  min max 가 반드시 포함되도록  min, max에서 각각 한 개의 숫자를 선택하고,   
    . combi4을 형성하는 것은 전략1의 방법으로 시햏한다.
    . combi6을 형성하고 평가하는 것은 전략1의 방법으로 시행한다.      
        
전략3)
    . 6개의 숫자중 min 숫자의  freq을 구하고,  그 중 순위별로 누적했을 때, 80%에 드는 숫자를  후보자로 선택 - min
    . 6개의 숫자중 max 숫자의  freq을 구하고,  그 중 순위별로 누적했을 때, 80%에 드는 숫자를  후보자로 선택 - max
    . min에서 가장 closeness가 좋은 숫자를 구한다.   -->  minc 라 명명.  --> listminminc을 구함.
    . max에서 가장 closeness가 좋은 숫자를 구한다.   --> maxcs라 명명.   --> listmaxmaxc을 구함.
    . 45개의 숫자에서  위의 min group을 빼고,  max group을 빼고,  minness을 빼고, maxness을 빼고, 나머지에서 
       2 숫자를 추출하여 combi2을 만들고,   min minness max maxness combi2을 합하여 combi6을 만들고, 
    . combi6에 대해
        get_Probability_from_dictNumFreq()      --> 각 숫자의 빈도수에 대한 확률의 합.
        get_Modn_Probability(2, listcombi6)     --> mod 2을 했을 때, pattern에 의한 확률
        get_Modn_Probability(3, listcombi6)     --> mod 3을 했을 때, pattern에 의한 확률
        get_Modn_Probability(5, listcombi6)     --> mod 5을 했을 때, pattern에 의한 확률
        get_Modn_Probability(7, listcombi6)     --> mod 7을 했을 때, pattern에 의한 확률
        get_Modn_Probability(9, listcombi6)     --> mod 9을 했을 때, pattern에 의한 확률
        getPrimeCountPatternProbability(listcombi6) --> 소수 발생빈도 pattern에 의한 확률
        을 시행하고 나온 각 확률을 곱하여 나온 값으로 순위로 매기고, 최상위 10개만 print한다. 
            
전략4)
    . 6개의 숫자중 min 숫자의  freq을 구하고,  그 중 순위별로 누적했을 때, 80%에 드는 숫자를  후보자로 선택 - min
    . 6개의 숫자중 max 숫자의  freq을 구하고,  그 중 순위별로 누적했을 때, 80%에 드는 숫자를  후보자로 선택 - max
    . min에서 가장 closeness가 좋은 숫자를 구한다.   --> minc 라 명명.  --> listminmincminc2을 구함.
    . max에서 가장 closeness가 좋은 숫자를 구한다.   --> maxc 명명.   --> listmaxness을 구함.
    . min, minness와 가장 closeness가 좋은 tuple을 구한다. 즉 (min, minc, mincc )
    . max, maxness와 가장 closeness가 좋은 tuple을 구한다. 즉 (max, maxc, maxcc )
    . (min, minness, minminness ) 와 (max, maxness, maxmaxness )을 합하여 combi6에 대해
        get_Probability_from_dictNumFreq()      --> 각 숫자의 빈도수에 대한 확률의 합.
        get_Modn_Probability(2, listcombi6)     --> mod 2을 했을 때, pattern에 의한 확률
        get_Modn_Probability(3, listcombi6)     --> mod 3을 했을 때, pattern에 의한 확률
        get_Modn_Probability(5, listcombi6)     --> mod 5을 했을 때, pattern에 의한 확률
        get_Modn_Probability(7, listcombi6)     --> mod 7을 했을 때, pattern에 의한 확률
        get_Modn_Probability(9, listcombi6)     --> mod 9을 했을 때, pattern에 의한 확률
        getPrimeCountPatternProbability(listcombi6) --> 소수 발생빈도 pattern에 의한 확률
        을 시행하고 나온 각 확률을 곱하여 나온 값으로 순위로 매기고, 최상위 10개만 print한다.         
'''




if __name__ == "__main__":
    '''
    아래의 code은 전략3을 이용하여  후보를 산출한다.
    '''

    tableinningno = TableInningNo("lotto.csv")
    listlistinningnos = tableinningno.getlistlistInningNos()      # 차수, 당첨번호 list

    Stratey = 4

    if Stratey == 1 :

        # 1) ------------------------------------------------------------------
        # 각 inning중에, 최소 숫자에 대해, 그 빈도를 구하고, 빈도가 큰 것 부터 누적하여
        #  80%에 해당하는 최소 숫자의 list을 구한다.
        minnumfreq = MinNumFreq(listlistinningnos)
        listEffectiveNum80_min = minnumfreq.get_listEffectiveNum80()

        # 2) ------------------------------------------------------------------
        # 각 inning중에, 최대 숫자에 대해, 그 빈도를 구하고, 빈도가 큰 것 부터 누적하여
        #  80%에 해당하는 최대 숫자의 list을 구한다.
        maxnumfreq = MaxNumFreq(listlistinningnos)
        listEffectiveNum80_max = maxnumfreq.get_listEffectiveNum80()

        # 3) ------------------------------------------------------------------
        # listEffectiveNum80_min, listEffectiveNum80_max 을 합치고,  2 숫자를 뽑아서
        # 친밀도를 구하고,  sort 했을 때, 상위 20% 에 해당하는 combi을 구해본다.

        ## combi 2 에 대해서, closeness을 만든다.
        combi2closeness = CombiCloseness(2, listlistinningnos)
        listEffectiveNum80_minmax = listEffectiveNum80_min + listEffectiveNum80_max
        listEffectiveNum80_minmax.sort()
        listlistClosenessTuplecombi2 = []
        for tuplecombi2 in itertools.combinations(listEffectiveNum80_minmax, 2):
            listlistClosenessTuplecombi2.append([combi2closeness.getCombiProbability(tuplecombi2), tuplecombi2])

        # sort
        listlistClosenessTuplecombi2 = sorted(listlistClosenessTuplecombi2, key=lambda listclose: listclose[0],
                                              reverse=True)

        # listlistClosenessTuplecombi2 중에서  상위 20% 만 모은다.
        listlistClosenessTuplecombi2 = listlistClosenessTuplecombi2[0:int(len(listlistClosenessTuplecombi2) * 0.2)]

        # 4) ------------------------------------------------------------------
        # 6숫자 중에  2개를 구했으므로, 나머지 4개를  총 45개 중에서  combi4closeness 상위 20%에 해당하는 combi4를 구한다.

        listcombi4candidate = list(set(range(1, MAXNO + 1)) - set(listEffectiveNum80_minmax))
        listcombi4candidate.sort()

        ## combi 4 에 대해서, closeness instantance 을 만든다.
        combi4closeness = CombiCloseness(4, listlistinningnos)

        # listcombi4candidate 에서 closeness가 좋은  상위 20%을 추출한다.
        listlistProbTupleCombi4 =[]
        for tuplecombi4 in itertools.combinations(listcombi4candidate, 4) :
            listlistProbTupleCombi4.append([combi4closeness.getCombiProbability(tuplecombi4), tuplecombi4])

        listlistProbTupleCombi4 = sorted(listlistProbTupleCombi4, key=lambda listProbTupleCombi4: listProbTupleCombi4[0], reverse=True)
        listlistProbTupleCombi4 = listlistProbTupleCombi4[0:int(len(listlistProbTupleCombi4) * 0.2)]

        ## 여기서는 listlistClosenessTuplecombi2, listlistProbTupleCombi4 가 구해진 상태이다.
        ## combi2, combi4의 조합으로 combi6을 만들고, mod_N 의 확률를  계산하고, sort하고,  후보를 구한다.

        primefreq = PrimeFreq(listlistinningnos)
        listlistProbListcombi6 = []

        looptotal = len(listlistClosenessTuplecombi2) * len(listlistProbTupleCombi4)
        remainedlooptotal = looptotal
        for closeness, tuplecombi2 in listlistClosenessTuplecombi2 :
            for prob, tuplecomb4 in listlistProbTupleCombi4 :
                remainedlooptotal -= 1
                print("remained looptotal : %d"% remainedlooptotal)
                listcombi6 = list(tuplecombi2) + list(tuplecomb4)
                listcombi6.sort()

                ## [1,2,3,4,5,6] 6개의 각각의 숫자에 대해 빈도수를 합산하여 percentage을 구한다.
                no_freq_probability = tableinningno.get_Probability_from_dictNumFreq(listcombi6) * 100

                ## [1,2,3,4,5,6] 6개의 숫자에 각각 mod n 을 실행하고, 빈도수를 key 패턴으로 할 때, 주어진 패턴 확률를 구한다.
                mod2_probability = tableinningno.get_Modn_Probability(2, listcombi6) * 100
                mod3_probability = tableinningno.get_Modn_Probability(3, listcombi6) * 100
                mod5_probability = tableinningno.get_Modn_Probability(5, listcombi6) * 1000
                mod7_probability = tableinningno.get_Modn_Probability(7, listcombi6) * 1000
                mod9_probability = tableinningno.get_Modn_Probability(9, listcombi6) * 1000
                primepattern_probability = primefreq.getPrimeCountPatternProbability(listcombi6) * 10

                total_prob = no_freq_probability * mod2_probability * mod3_probability * mod5_probability * \
                        mod7_probability * mod9_probability * primepattern_probability
                listlistProbListcombi6.append([total_prob, listcombi6])


        # sort
        print("looptotal : %d" % looptotal)
        print("sorting...")
        listlistProbListcombi6 = sorted(listlistProbListcombi6, key=lambda listProbListcombi6: listProbListcombi6[0], reverse=True)

        # 상위 10개 추출
        listlistProbListcombi6 = listlistProbListcombi6[0:10]

        #
        pprint.pprint(listlistProbListcombi6)
        '''
        [[22632994.098827098, [5, 11, 16, 24, 27, 28]],
         [21733930.120755, [5, 11, 24, 27, 28, 30]],
         [20079872.630242936, [3, 9, 20, 25, 26, 42]],
         [19925540.048664305, [7, 9, 18, 20, 31, 40]],
         [19314225.80173182, [2, 14, 15, 31, 33, 34]],
         [17235726.506940257, [1, 3, 9, 16, 20, 32]],
         [17179377.159404814, [14, 15, 26, 27, 37, 38]],
         [15326241.298750699, [9, 20, 21, 32, 37, 43]],
         [14734010.318822956, [1, 9, 13, 24, 32, 40]],
         [14386858.088470662, [6, 9, 19, 32, 35, 38]]]
        '''

        exit(0)

    elif Stratey == 3 :

        # 1) ------------------------------------------------------------------
        # 각 inning중에, 최소 숫자에 대해, 그 빈도를 구하고, 빈도가 큰 것 부터 누적하여
        #  80%에 해당하는 최소 숫자의 list을 구한다.
        minnumfreq = MinNumFreq(listlistinningnos)
        listEffectiveNum80_min = minnumfreq.get_listEffectiveNum80()

        # 2) ------------------------------------------------------------------
        # 각 inning중에, 최대 숫자에 대해, 그 빈도를 구하고, 빈도가 큰 것 부터 누적하여
        #  80%에 해당하는 최대 숫자의 list을 구한다.
        maxnumfreq = MaxNumFreq(listlistinningnos)
        listEffectiveNum80_max = maxnumfreq.get_listEffectiveNum80()

        # 3) ------------------------------------------------------------------
        # listEffectiveNum80_min에 closeness가 좋은  (min,minness) list 을 구한다.

        combi2closeness = CombiCloseness(2, listlistinningnos)
        listtupleminness = []
        for no in listEffectiveNum80_min :
            listtupleminness += combi2closeness.getBestCombiFromGivenTuple((no,))

        # 4) ------------------------------------------------------------------
        # listEffectiveNum80_max에 closeness가 좋은  (max,maxness) list 을 구한다.

        listtuplemaxness = []
        for no in listEffectiveNum80_max:
            listtuplemaxness += combi2closeness.getBestCombiFromGivenTuple((no,))

        # 5) ------------------------------------------------------------------
        # 45개의 숫자에서  위의 min group을 빼고,  max group을 빼고,  minness을 빼고, maxness을 빼고, 나머지에서
        # 2 숫자를 추출하여 combi2을 만들고,   min minness max maxness combi2을 합하여 combi6을 만들고,

        primefreq = PrimeFreq(listlistinningnos)
        listlistProbListcombi6 = []

        looptotal = len(listtupleminness) * len(listtuplemaxness)
        remainedlooptotal = looptotal

        for tupleminness in listtupleminness :
            for tuplemaxness in listtuplemaxness :
                # 먼저 45숫자에서 tupleminness, tuplemaxness 을 제거한다.
                remainedlooptotal -= 1
                print("remained looptotal : %d" % remainedlooptotal)

                setcombi2candidate = set(range(1,MAXNO+1)) - set(listEffectiveNum80_min) - set(listEffectiveNum80_max) - \
                    set(tupleminness) - set(tuplemaxness)
                for tuplecombi2 in  itertools.combinations(setcombi2candidate, 2) :
                    listcombi6 = list(tupleminness) + list(tuplemaxness) + list(tuplecombi2)
                    listcombi6.sort()

                    ## [1,2,3,4,5,6] 6개의 각각의 숫자에 대해 빈도수를 합산하여 percentage을 구한다.
                    no_freq_probability = tableinningno.get_Probability_from_dictNumFreq(listcombi6) * 100

                    ## [1,2,3,4,5,6] 6개의 숫자에 각각 mod n 을 실행하고, 빈도수를 key 패턴으로 할 때, 주어진 패턴 확률를 구한다.
                    mod2_probability = tableinningno.get_Modn_Probability(2, listcombi6) * 100
                    mod3_probability = tableinningno.get_Modn_Probability(3, listcombi6) * 100
                    mod5_probability = tableinningno.get_Modn_Probability(5, listcombi6) * 1000
                    mod7_probability = tableinningno.get_Modn_Probability(7, listcombi6) * 1000
                    mod9_probability = tableinningno.get_Modn_Probability(9, listcombi6) * 1000
                    primepattern_probability = primefreq.getPrimeCountPatternProbability(listcombi6) * 10

                    total_prob = no_freq_probability * mod2_probability * mod3_probability * mod5_probability * \
                                 mod7_probability * mod9_probability * primepattern_probability
                    listlistProbListcombi6.append([total_prob, listcombi6])

        # sort
        print("looptotal : %d" % looptotal)
        print("sorting...")
        listlistProbListcombi6 = sorted(listlistProbListcombi6,
                                        key=lambda listProbListcombi6: listProbListcombi6[0],
                                        reverse=True)

        # 상위 10개 추출
        listlistProbListcombi6 = listlistProbListcombi6[0:10]

        #
        pprint.pprint(listlistProbListcombi6)
        exit(0)

        '''
        [[27450711.28157679, [7, 17, 20, 33, 36, 39]],
         [25332426.164360717, [7, 20, 31, 33, 36, 39]],
         [20479814.74198086, [7, 8, 20, 31, 33, 39]],
         [19943339.11865594, [3, 14, 19, 20, 25, 36]],
         [17990709.305761784, [4, 17, 20, 21, 26, 43]],
         [17945560.51062213, [1, 3, 9, 20, 26, 42]],
         [17881839.65792056, [7, 8, 20, 26, 31, 39]],
         [16067052.866889883, [4, 20, 21, 26, 37, 43]],
         [14848255.562978264, [7, 20, 23, 26, 36, 39]],
         [14637317.769698134, [3, 19, 20, 22, 36, 39]]]
        '''
    elif Stratey == 4  :
        # 1) ------------------------------------------------------------------
        # 각 inning중에, 최소 숫자에 대해, 그 빈도를 구하고, 빈도가 큰 것 부터 누적하여
        #  80%에 해당하는 최소 숫자의 list을 구한다.
        minnumfreq = MinNumFreq(listlistinningnos)
        listEffectiveNum80_min = minnumfreq.get_listEffectiveNum80()

        # 2) ------------------------------------------------------------------
        # 각 inning중에, 최대 숫자에 대해, 그 빈도를 구하고, 빈도가 큰 것 부터 누적하여
        #  80%에 해당하는 최대 숫자의 list을 구한다.
        maxnumfreq = MaxNumFreq(listlistinningnos)
        listEffectiveNum80_max = maxnumfreq.get_listEffectiveNum80()

        # 3) ------------------------------------------------------------------
        # listEffectiveNum80_min에 closeness가 좋은  (min,minness) list 을 구한다.

        combi2closeness = CombiCloseness(2, listlistinningnos)
        listtupleminminc = []
        for no in listEffectiveNum80_min:
            listtupleminminc += combi2closeness.getBestCombiFromGivenTuple((no,))

        # 4) ------------------------------------------------------------------
        # listEffectiveNum80_max에 closeness가 좋은  (max,maxness) list 을 구한다.

        listtuplemaxmaxc = []
        for no in listEffectiveNum80_max:
            listtuplemaxmaxc += combi2closeness.getBestCombiFromGivenTuple((no,))

        # 5) ------------------------------------------------------------------
        # min, minness와 가장 closeness가 좋은 tuple을 구한다. 즉 (min, minness, minminness )
        combi3closeness = CombiCloseness(3, listlistinningnos)

        listtupleminmincmincc = []
        for tupleminminc in listtupleminminc :
            listtupleminmincmincc += combi3closeness.getBestCombiFromGivenTuple(tupleminminc)

        # 6) ------------------------------------------------------------------
        # max, maxness와 가장 closeness가 좋은 tuple을 구한다. 즉 (max, maxness, maxmaxness )
        listtuplemaxmaxcmaxcc = []
        for tuplemaxmaxc in listtuplemaxmaxc:
            listtuplemaxmaxcmaxcc += combi3closeness.getBestCombiFromGivenTuple(tuplemaxmaxc)

        # 7) ------------------------------------------------------------------
        # max, maxness와 가장 closeness가 좋은 tuple을 구한다. 즉 (max, maxness, maxmaxness )

        primefreq = PrimeFreq(listlistinningnos)
        listlistProbListcombi6 = []
        listlistProbListcombi5 = []     # combi5 이하인 것을 모은다.

        looptotal = len(listtupleminmincmincc) * len(listtuplemaxmaxcmaxcc)
        remainedlooptotal = looptotal

        for tupleminmincmincc in listtupleminmincmincc:
            for tuplemaxmaxcmaxcc in listtuplemaxmaxcmaxcc:

                remainedlooptotal -= 1
                print("remained looptotal : %d" % remainedlooptotal)

                listcombi6 = list(tupleminmincmincc) + list(tuplemaxmaxcmaxcc)
                listcombi6 = list(set(listcombi6))              # 중복 제거를 위해
                listcombi6.sort()

                if len(listcombi6) != 6 :
                    print("Not lenght 6 :" + str(listcombi6))
                    listlistProbListcombi5.append(listcombi6)
                    continue

                ## [1,2,3,4,5,6] 6개의 각각의 숫자에 대해 빈도수를 합산하여 percentage을 구한다.
                no_freq_probability = tableinningno.get_Probability_from_dictNumFreq(listcombi6) * 100

                ## [1,2,3,4,5,6] 6개의 숫자에 각각 mod n 을 실행하고, 빈도수를 key 패턴으로 할 때, 주어진 패턴 확률를 구한다.
                mod2_probability = tableinningno.get_Modn_Probability(2, listcombi6) * 100
                mod3_probability = tableinningno.get_Modn_Probability(3, listcombi6) * 100
                mod5_probability = tableinningno.get_Modn_Probability(5, listcombi6) * 1000
                mod7_probability = tableinningno.get_Modn_Probability(7, listcombi6) * 1000
                mod9_probability = tableinningno.get_Modn_Probability(9, listcombi6) * 1000
                primepattern_probability = primefreq.getPrimeCountPatternProbability(listcombi6) * 10

                total_prob = no_freq_probability * mod2_probability * mod3_probability * mod5_probability * \
                             mod7_probability * mod9_probability * primepattern_probability
                listlistProbListcombi6.append([total_prob, listcombi6])

        # sort
        print("looptotal : %d" % looptotal)
        print("sorting...")
        listlistProbListcombi6 = sorted(listlistProbListcombi6,
                                        key=lambda listProbListcombi6: listProbListcombi6[0],
                                        reverse=True)

        # 상위 10개 추출
        listlistProbListcombi6 = listlistProbListcombi6[0:10]

        #
        pprint.pprint(listlistProbListcombi6)

        print("------------------- -------------------------------------------")
        print("------------------  번외  계산       --------------------------")
        # 위에서  6개의 후자 숫자중 일부 중복이 발생하여,  5개 혹은 4개의 숫자가  후보로 나오는 경우가 있다.
        # combi5 후보는  combi4을 포함하는 경우만 선택하고,
        # 각 inniung 의 sum 통계 빈도수를  활용하여,  combi5 후보의 나머지 숫자를 선택한다.
        #
        # 다음은 combi4, combi5을 골라낸다.
        listlistcombi4 = []
        listlistcombi5 = []
        while( len(listlistProbListcombi5) > 0 ):
            listtemp = listlistProbListcombi5.pop()
            if len(listtemp) == 5 :
                listlistcombi5.append(listtemp)
            elif len(listtemp) == 4 :
                listlistcombi4.append(listtemp)

        # combi4 을 포함하는 combi5을  listlistcombi5에서 찾아고
        listlistcombi6_other =[]
        for  listcombi5 in listlistcombi5 :
            for listcombi4 in listlistcombi4 :
                if set(listcombi5).issuperset(set(listcombi4)) :
                    # combi5가 combi4을 포함하는 경우  나머지 숫자를 sum 통계치에서 선택한다.
                    print(str(listcombi4) + " : " + str(listcombi5), end=", ")
                    listcombi6, ranking = tableinningno.get_bestcombi6_from_listfreqsum(listcombi5)
                    listlistcombi6_other.append(listcombi6)
                    print( str(listcombi6) + " : " + str(ranking))


        for listcombi6 in listlistcombi6_other :
            no_freq_probability = tableinningno.get_Probability_from_dictNumFreq(listcombi6) * 100

            ## [1,2,3,4,5,6] 6개의 숫자에 각각 mod n 을 실행하고, 빈도수를 key 패턴으로 할 때, 주어진 패턴 확률를 구한다.
            mod2_probability = tableinningno.get_Modn_Probability(2, listcombi6) * 100
            mod3_probability = tableinningno.get_Modn_Probability(3, listcombi6) * 100
            mod5_probability = tableinningno.get_Modn_Probability(5, listcombi6) * 1000
            mod7_probability = tableinningno.get_Modn_Probability(7, listcombi6) * 1000
            mod9_probability = tableinningno.get_Modn_Probability(9, listcombi6) * 1000
            primepattern_probability = primefreq.getPrimeCountPatternProbability(listcombi6) * 10

            total_prob = no_freq_probability * mod2_probability * mod3_probability * mod5_probability * \
                         mod7_probability * mod9_probability * primepattern_probability

            listlistProbListcombi6.append([total_prob, listcombi6])

        listlistProbListcombi6 = sorted(listlistProbListcombi6,
                                        key=lambda listProbListcombi6: listProbListcombi6[0],
                                        reverse=True)

        # 상위 10개 추출
        listlistProbListcombi6 = listlistProbListcombi6[0:10]

        #
        pprint.pprint(listlistProbListcombi6)



        exit(0)

        '''
        [[13956489.684306161, [1, 2, 19, 33, 35, 36]],
         [10137410.194234882, [6, 17, 28, 36, 39, 40]],
         [6456033.970150298, [1, 5, 6, 34, 37, 38]],
         [4135602.4222009843, [3, 20, 25, 33, 36, 44]],
         [4135602.4222009843, [3, 20, 25, 33, 36, 44]],
         [3641326.5745393103, [6, 17, 25, 28, 33, 36]],
         [3641326.5745393103, [6, 17, 25, 28, 33, 36]],
         [3614069.5018205964, [5, 6, 11, 28, 34, 44]],
         [3531621.685352094, [1, 3, 20, 31, 34, 44]],
         [3426588.9286397556, [3, 20, 21, 22, 24, 37]]]
        ------------------- -------------------------------------------
        ------------------  번외  계산       --------------------------
        [8, 34, 36, 39] : [8, 25, 34, 36, 39], [8, 23, 25, 34, 36, 39] : 0
        [8, 34, 36, 39] : [8, 25, 34, 36, 39], [8, 23, 25, 34, 36, 39] : 0
        [8, 34, 36, 39] : [8, 27, 34, 36, 39], [8, 21, 27, 34, 36, 39] : 0
        [8, 34, 36, 39] : [8, 17, 34, 36, 39], [8, 17, 31, 34, 36, 39] : 0
        [5, 27, 35, 43] : [5, 17, 27, 35, 43], [1, 5, 17, 27, 35, 43] : 0
        [5, 27, 34, 44] : [5, 27, 34, 35, 44], [5, 20, 27, 34, 35, 44] : 0
        [5, 27, 35, 43] : [5, 27, 34, 35, 43], [5, 21, 27, 34, 35, 43] : 0
        [5, 27, 34, 44] : [5, 27, 31, 34, 44], [5, 24, 27, 31, 34, 44] : 0
        [1, 5, 34, 44] : [1, 5, 31, 34, 44], [1, 5, 13, 31, 34, 44] : 0
        [[13956489.684306161, [1, 2, 19, 33, 35, 36]],
         [10137410.194234882, [6, 17, 28, 36, 39, 40]],
         [6456033.970150298, [1, 5, 6, 34, 37, 38]],
         [4135602.4222009843, [3, 20, 25, 33, 36, 44]],
         [4135602.4222009843, [3, 20, 25, 33, 36, 44]],
         [3641326.5745393103, [6, 17, 25, 28, 33, 36]],
         [3641326.5745393103, [6, 17, 25, 28, 33, 36]],
         [3614069.5018205964, [5, 6, 11, 28, 34, 44]],
         [3531621.685352094, [1, 3, 20, 31, 34, 44]],
         [3426588.9286397556, [3, 20, 21, 22, 24, 37]]]
         --> 번외 계산은  큰 영향이 없다.
        '''

