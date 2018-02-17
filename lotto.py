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
        self.dictNumFreq = {}               # { 1:freq, 2:freq, ... }

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

        #--------------------------------------

        self.createlisttupleNoFreqSorted()
        self.createlistdictModBalanceWithTable()


    def getlistlistInningNos(self):
        return self.listlistinningnos

    def getNosWithInning(self, inning):
        return self.listlistinningnos[inning-1][1:]

    def createdictNumFreq(self):
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
        return sum([ self.getPrimeProbability(aa) for aa in listnos])

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
        self.listsortlistCountTuplecombi = []


        dictTuplecombiCount = collections.defaultdict(int)
        for  listinningnos in listlistinningnos :
            for tuplecombi in itertools.combinations(listinningnos[1:],ncombi ) :
                dictTuplecombiCount[tuplecombi] += 1

        self.dictTuplecombiCount = dictTuplecombiCount
        ## 총 combi의 total은 6가지 숫자에서 combi의 경우의 수에  총 inning 의 수의 곱이다.
        self.combitotal = len([aa for aa in itertools.combinations(range(6), ncombi)]) * len(listlistinningnos)

        ## dictTuplecombiCount을 이용해서 [[count, (combi)],[count, (combi)], ... ] 을 만든다.
        ## 추가하여 count을 기준으로 sort을 한다.
        listsortlistCountTuplecombi = []
        for tuplecombi, count in dictTuplecombiCount.items():
            listsortlistCountTuplecombi.append([count, tuplecombi])

        self.listsortlistCountTuplecombi = sorted(listsortlistCountTuplecombi, key=lambda  listcounttuple: listcounttuple[0], reverse=True)
        del listsortlistCountTuplecombi

    def __str__(self):
        outstring = ""
        for listCountTuplecombi in self.listsortlistCountTuplecombi :
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

    def getListSortlistCountTuplecombi(self):
        return self.listsortlistCountTuplecombi


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
        for count, tuplecombi in self.listsortlistCountTuplecombi :
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


    # --------------------------------------
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
        return self.ddictcombinrestncloseness.get((tuple(listcombi), tuple(listrestn)), 0)

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

        # listlistProbListcombi5을 처리한다.
        #
        listlistcombi4 = []
        listlistcombi5 = []
        while( len(listlistProbListcombi5) > 0 ):
            listtemp = listlistProbListcombi5.pop()
            if len(listtemp) == 5 :
                listlistcombi5.append(listtemp)
            elif len(listtemp) == 4 :
                listlistcombi4.append(listtemp)

        # combi4 을 포함하는 combi5을  listlistcombi5에서 찾아서 print한다.
        for  listcombi5 in listlistcombi5 :
            for listcombi4 in listlistcombi4 :
                if set(listcombi5).issuperset(set(listcombi4)) :
                    print(str(listcombi4) + " : " + str(listcombi5))




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
        [8, 34, 36, 39] : [8, 25, 34, 36, 39]
        [8, 34, 36, 39] : [8, 25, 34, 36, 39]
        [8, 34, 36, 39] : [8, 27, 34, 36, 39]
        [8, 34, 36, 39] : [8, 17, 34, 36, 39]
        [5, 27, 35, 43] : [5, 17, 27, 35, 43]
        [5, 27, 34, 44] : [5, 27, 34, 35, 44]
        [5, 27, 35, 43] : [5, 27, 34, 35, 43]
        [5, 27, 34, 44] : [5, 27, 31, 34, 44]
        [1, 5, 34, 44] : [1, 5, 31, 34, 44]
        '''




    # combi에 대한  restn의 친밀도를 가진 classs을 생성한다. 혹은 file write한다.
    # 시사점 : 최고의 친밀도를 가진 combi와 restn을 다시 발생할 가능성이 없는 것이다.
    # 이를 활용해서,  후보 숫자들을 filter할 수 있다.
    combi1rest1close = CombiRestCloseness(listlistinningnos, 1, 1)
    # combi1rest1close.writecombirestclose()

    combi2rest1close = CombiRestCloseness(listlistinningnos, 2, 1)
    # combi2rest1close.writecombirestclose()

    combi2rest2close = CombiRestCloseness(listlistinningnos, 2, 2)
    # combi2rest2close.writecombirestclose()

    combi3rest2close = CombiRestCloseness(listlistinningnos, 3, 2)
    # combi3rest2close.writecombirestclose()

    combi3rest1close = CombiRestCloseness(listlistinningnos, 3, 1)
    # combi3rest1close.writecombirestclose()

    combi4rest1close = CombiRestCloseness(listlistinningnos, 4, 1)
    # combi4rest1close.writecombirestclose()


    # 공통 class을 만들어서  변수들을 저장한다.
    clsvar = CLSVAR()

    # 후보 숫자들을  filter할 수 있는  class들을 저장한다.
    clsvar.combi1rest1close = combi1rest1close
    clsvar.combi2rest1close = combi2rest1close
    clsvar.combi2rest2close = combi2rest2close
    clsvar.combi3rest2close = combi3rest2close
    clsvar.combi3rest1close = combi3rest1close
    clsvar.combi4rest1close = combi4rest1close

    # ----------------------------------------------------------------------------------------
    # 아래의 의도는 combination=5 이고, freq=2(max)인  combi를 찾고,
    # 그 combi의 공통된 특성이  combination=4 인 class에서는  어떤 freq
    # 에서 많이 출현했는지 관찰하고, 그 후보를 선택한다.

    # 먼저 combination=5 이고, freq=2(max)인  combi list을 구한다.
    ddictFreqListcombi5 = tableinningno.getdictFreqListcombi(5)
    combi5MaxFreq = max(ddictFreqListcombi5.keys())
    # print("Combi=5, max = %s" % combi5MaxFreq)

    # combi=5 이면,  최대 빈도는 2 이다. print해서 확인해 본다.
    # pprint.pprint(ddictFreqListcombi5[combi5MaxFreq])

    '''
    [(14, 27, 30, 31, 40),
     (14, 15, 18, 21, 26),
     (10, 22, 34, 36, 44),
     (15, 19, 21, 34, 44),
     (16, 26, 31, 36, 43),
     (11, 17, 21, 26, 36),
     (7, 22, 24, 31, 34)  ==> 추가
     ] '''

    # combi=4 경우에 대해, 각각 출현빈도에 대한 combi list을 구한다.
    ddictFreqListcombi4 = tableinningno.getdictFreqListcombi(4)
    combi4MaxFreq = max(ddictFreqListcombi4.keys())
    # print("Combi=4, max = %s" % combi4MaxFreq)
    # pprint.pprint(ddictFreqListcombi4[combi4MaxFreq])
    '''
    [(12, 24, 27, 32),
     (16, 34, 42, 45),
     (17, 32, 33, 34),
     (2, 4, 31, 34),
     (14, 22, 35, 39),
     (11, 26, 29, 44),
     (1, 8, 18, 29),
     (4, 20, 26, 35),
     (3, 13, 33, 37),
     (9, 12, 39, 43)  ==> 추가
     ]
    '''

    # print("Combi=4, max-1 = %s" % (combi4MaxFreq-1))
    # pprint.pprint(ddictFreqListcombi4[combi4MaxFreq-1])

    # combi=3 경우에 대해, 각각 출현빈도에 대한 combi list을 구한다.
    ddictFreqListcombi3 = tableinningno.getdictFreqListcombi(3)
    combi3MaxFreq = max(ddictFreqListcombi3.keys())
    # print("Combi=3, max = %s" % combi3MaxFreq)
    # pprint.pprint(ddictFreqListcombi3[combi3MaxFreq])

    # combi=2 경우에 대해, 각각 출현빈도에 대한 combi list을 구한다.
    ddictFreqListcombi2 = tableinningno.getdictFreqListcombi(2)
    combi2MaxFreq = max(ddictFreqListcombi2.keys())

    # 각 ddictFreqListcombi에 대해 조합의 수를 print한다.

    for freq in sorted(list(ddictFreqListcombi5.keys())) :
        if freq == 1 :
            continue
        print("Combi=5, freq=%s, count=%s"%(freq, len(ddictFreqListcombi5[freq])))

    for freq in sorted(list(ddictFreqListcombi4.keys())) :
        if freq == 1 :
            continue
        print("Combi=4, freq=%s, count=%s"%(freq, len(ddictFreqListcombi4[freq])))

    for freq in sorted(list(ddictFreqListcombi3.keys())) :
        if freq == 1 :
            continue
        print("Combi=3, freq=%s, count=%s"%(freq, len(ddictFreqListcombi3[freq])))

    for freq in sorted(list(ddictFreqListcombi2.keys())) :
        if freq == 1 :
            continue
        print("Combi=2, freq=%s, count=%s"%(freq, len(ddictFreqListcombi2[freq])))

    alloutput = '''
    Combi=5, freq=2, count=7
    Combi=4, freq=2, count=378
    Combi=4, freq=3, count=10
    Combi=3, freq=2, count=2847
    Combi=3, freq=3, count=1035
    Combi=3, freq=4, count=265
    Combi=3, freq=5, count=55
    Combi=3, freq=6, count=11
    Combi=2, freq=2, count=2
    Combi=2, freq=3, count=1
    Combi=2, freq=4, count=3
    Combi=2, freq=5, count=15
    Combi=2, freq=6, count=35
    Combi=2, freq=7, count=46
    Combi=2, freq=8, count=65
    Combi=2, freq=9, count=82
    Combi=2, freq=10, count=114
    Combi=2, freq=11, count=131
    Combi=2, freq=12, count=113
    Combi=2, freq=13, count=99
    Combi=2, freq=14, count=86
    Combi=2, freq=15, count=78
    Combi=2, freq=16, count=35
    Combi=2, freq=17, count=37
    Combi=2, freq=18, count=16
    Combi=2, freq=19, count=15
    Combi=2, freq=20, count=8
    Combi=2, freq=21, count=4
    Combi=2, freq=22, count=2
    Combi=2, freq=23, count=1
    Combi=2, freq=24, count=1
    '''

    print("-------------------------------- search a proper freq of combi4freq class to search combi5freq2 candidate  ----------------------")

    listfreq = list(ddictFreqListcombi4.keys())
    listfreq.remove(1)
    listfreq.sort()
    for freq in listfreq:
        listcombi = ddictFreqListcombi4[freq]
        countcombi = len(listcombi)
        sum = 0
        for tuplecombi5 in ddictFreqListcombi5[2]:
            listsuperset = [set(tuplecombi5).issuperset(set(tuplecombi)) for tuplecombi in listcombi ]
            sum += listsuperset.count(True)
        print("combi5freq2, combi4freq%s, rate=%s"%(freq, sum/countcombi ))

    print("-------------------------------- search a proper freq of combi3freq class to search combi5freq2 candidate  ----------------------")

    listfreq = list(ddictFreqListcombi3.keys())
    listfreq.remove(1)
    listfreq.sort()
    for freq in listfreq:
        listcombi = ddictFreqListcombi3[freq]
        countcombi = len(listcombi)
        sum = 0
        for tuplecombi5 in ddictFreqListcombi5[2]:
            listsuperset = [set(tuplecombi5).issuperset(set(tuplecombi)) for tuplecombi in listcombi]
            sum += listsuperset.count(True)
        print("combi5freq2, combi3freq%s, rate=%s" % (freq, sum / countcombi))

    print("-------------------------------- search a proper freq of combi2freq class to search combi5freq2 candidate  ----------------------")

    listfreq = list(ddictFreqListcombi2.keys())
    listfreq.remove(1)
    listfreq.sort()
    for freq in listfreq:
        listcombi = ddictFreqListcombi2[freq]
        countcombi = len(listcombi)
        sum = 0
        for tuplecombi5 in ddictFreqListcombi5[2]:
            listsuperset = [set(tuplecombi5).issuperset(set(tuplecombi)) for tuplecombi in listcombi]
            sum += listsuperset.count(True)
        print("combi5freq2, combi2freq%s, rate=%s" % (freq, sum / countcombi))

    output = '''
    ------- search a proper freq of combi4freq class to search combi5freq2 candidate  ----------------------
    combi5freq2, combi4freq2, rate=0.09259259259259259
    combi5freq2, combi4freq3, rate=0.0
    ------- search a proper freq of combi3freq class to search combi5freq2 candidate  ----------------------
    combi5freq2, combi3freq2, rate=0.006322444678609062
    combi5freq2, combi3freq3, rate=0.02995169082125604
    combi5freq2, combi3freq4, rate=0.06037735849056604
    combi5freq2, combi3freq5, rate=0.07272727272727272
    combi5freq2, combi3freq6, rate=0.09090909090909091
    ------- search a proper freq of combi2freq class to search combi5freq2 candidate  ----------------------
    combi5freq2, combi2freq2, rate=0.0
    combi5freq2, combi2freq3, rate=0.0
    combi5freq2, combi2freq4, rate=0.0
    combi5freq2, combi2freq5, rate=0.0
    combi5freq2, combi2freq6, rate=0.0
    combi5freq2, combi2freq7, rate=0.0
    combi5freq2, combi2freq8, rate=0.0
    combi5freq2, combi2freq9, rate=0.012195121951219513
    combi5freq2, combi2freq10, rate=0.03508771929824561
    combi5freq2, combi2freq11, rate=0.07633587786259542
    combi5freq2, combi2freq12, rate=0.035398230088495575
    combi5freq2, combi2freq13, rate=0.12121212121212122
    combi5freq2, combi2freq14, rate=0.10465116279069768
    combi5freq2, combi2freq15, rate=0.1282051282051282
    combi5freq2, combi2freq16, rate=0.11428571428571428
    combi5freq2, combi2freq17, rate=0.16216216216216217
    combi5freq2, combi2freq18, rate=0.125
    combi5freq2, combi2freq19, rate=0.2
    combi5freq2, combi2freq20, rate=0.25
    combi5freq2, combi2freq21, rate=0.25
    combi5freq2, combi2freq22, rate=0.5
    combi5freq2, combi2freq23, rate=1.0
    combi5freq2, combi2freq24, rate=0.0
    '''

    # combi5freq2의 후보는  각  combi의 발생했던 숫자들을 고려하여,
    # combi4freq2 ( 378 개)
    # combi3freq5 ( 55개, 근데 combi3freq6 은 추가로 나올 수 없다.  freq=6이 최고 이므로 )
    # combi2freq17(37개), combi2freq18(16개), combi2freq19(15개)

    # combi4freq2 에서 combi3freq5의 교집합은 ?
    print("---- listcombi4CandidateFromCombi3freq5 ----")
    setCombi4candidate = set()
    for combituple4 in ddictFreqListcombi4[2] :
        countboolcombisuperset = [ set(combituple4).issuperset(combituple3) for combituple3 in ddictFreqListcombi3[5]].count(True)
        if countboolcombisuperset > 1 :
            setCombi4candidate.add(combituple4)
            print("%s:%s"%(combituple4, countboolcombisuperset))

    # combi4freq2 에서 combi2freq17의 교집합은 ?
    print("---- listcombi4CandidateFromCombi2freq17 ----")
    for combituple4 in ddictFreqListcombi4[2]:
        countboolcombisuperset = [set(combituple4).issuperset(combituple2) for combituple2 in
                                  ddictFreqListcombi2[17]].count(True)
        if countboolcombisuperset > 1:
            setCombi4candidate.add(combituple4)
            print("%s:%s" % (combituple4, countboolcombisuperset))

    # combi4freq2 에서 combi2freq18의 교집합은 ?
    print("---- listcombi4CandidateFromCombi2freq18 ----")
    for combituple4 in ddictFreqListcombi4[2]:
        countboolcombisuperset = [set(combituple4).issuperset(combituple2) for combituple2 in
                                  ddictFreqListcombi2[18]].count(True)
        if countboolcombisuperset > 1:
            setCombi4candidate.add(combituple4)
            print("%s:%s" % (combituple4, countboolcombisuperset))

    # combi4freq2 에서 combi2freq19의 교집합은 ?
    print("---- listcombi4CandidateFromCombi2freq19 ----")
    for combituple4 in ddictFreqListcombi4[2]:
        countboolcombisuperset = [set(combituple4).issuperset(combituple2) for combituple2 in
                                  ddictFreqListcombi2[19]].count(True)
        if countboolcombisuperset > 1:
            setCombi4candidate.add(combituple4)
            print("%s:%s" % (combituple4, countboolcombisuperset))
    print("====== combituple4 total sum : %s======" %(len(setCombi4candidate)))
    pprint.pprint(setCombi4candidate)

    output = '''
    ====== combituple4 total sum : 35======
    {(1, 2, 8, 38),
     (1, 3, 8, 42),
     (1, 6, 17, 28),
     (1, 10, 20, 40),
     (1, 12, 18, 23),
     (2, 3, 20, 27),
     (2, 5, 11, 39),
     (2, 15, 21, 34), : 3 번 ( 후보 )
     (2, 15, 28, 34),
     (2, 16, 19, 34),
     (2, 19, 34, 45), : 3 번 ( 후보 )
     (3, 11, 37, 43),
     (4, 7, 19, 40),
     (4, 7, 33, 40),
     (4, 12, 24, 27),
     (7, 11, 13, 33),
     (7, 24, 37, 40),
     (7, 37, 38, 40),
     (8, 19, 25, 34),
     (11, 13, 33, 37),
     (11, 23, 29, 44),
     (12, 32, 33, 40),
     (13, 25, 29, 33),
     (13, 33, 37, 45),
     (14, 15, 18, 21),
     (14, 15, 21, 26),
     (14, 18, 21, 26),
     (14, 19, 25, 34),
     (15, 19, 21, 34),
     (17, 31, 37, 40),
     (18, 21, 23, 39),
     (19, 21, 34, 44),
     (19, 25, 26, 27),
     (19, 25, 41, 45),
     (24, 32, 33, 40)}  
    '''

    # combi2을 찾기 위해서
    # combi3freq5 에서 combi2freq17의 교집합은 ?
    print("---- listCombi2freq17CandidateFromCombi3freq5 ----")
    setCombi2candidate = set()
    for combituple2 in ddictFreqListcombi2[17]:
        countboolcombisubset = [set(combituple2).issubset(combituple3) for combituple3 in
                                  ddictFreqListcombi3[5]].count(True)
        if countboolcombisubset > 1:
            setCombi2candidate.add(combituple2)
            print("%s:%s" % (combituple2, countboolcombisubset))

    print("---- listCombi2freq18CandidateFromCombi3freq5 ----")
    for combituple2 in ddictFreqListcombi2[18]:
        countboolcombisubset = [set(combituple2).issubset(combituple3) for combituple3 in
                                ddictFreqListcombi3[5]].count(True)
        if countboolcombisubset > 1:
            setCombi2candidate.add(combituple2)
            print("%s:%s" % (combituple2, countboolcombisubset))

    print("---- listCombi2freq19CandidateFromCombi3freq5 ----")
    for combituple2 in ddictFreqListcombi2[19]:
        countboolcombisubset = [set(combituple2).issubset(combituple3) for combituple3 in
                                ddictFreqListcombi3[5]].count(True)
        if countboolcombisubset > 1:
            setCombi2candidate.add(combituple2)
            print("%s:%s" % (combituple2, countboolcombisubset))

    print("====== combituple2 total sum : %s======" % (len(setCombi2candidate)))
    pprint.pprint(setCombi2candidate)

    output = '''
    ---- listCombi2freq17CandidateFromCombi3freq5 ----
    (18, 31):2
    (34, 45):2
    ---- listCombi2freq18CandidateFromCombi3freq5 ----
    (29, 44):3 --> ( 후보 )
    ---- listCombi2freq19CandidateFromCombi3freq5 ----
    (34, 44):2
    (12, 24):2
    ====== combituple2 total sum : 5======
    {(12, 24), (34, 45), (29, 44), (34, 44), (18, 31)}
    '''
    # 위의 combituple4 의 후보와 combituple2 의 후보를 결합하여 최종 숫자를 완성한다.
    decision = '''
    (2, 15, 21, 34) + (29, 44)
    (2, 19, 34, 45) + (29, 44)
    '''

    exit(0)

    # ddictFreqListcombi5[combi5MaxFreq=2] 들은 ddictFreqListcombi4[combi4MaxFreq-1 = 2]에서 나오고 있다.
    # ddictFreqListcombi4[3] 이 이니고.
    # print("-------------------------------- search ddictFreqListcombi4[combi4MaxFreq-1] candidate from combi3 class ----------------------")
    # for tuplecombi4 in ddictFreqListcombi4[combi4MaxFreq-1] :
    #     print("combi4 is ", end="")
    #     print(tuplecombi4)
    #     for freqkey in ddictFreqListcombi3.keys() :
    #         for  tuplecombi3 in ddictFreqListcombi3[freqkey] :
    #             if tuplecombi3 in itertools.combinations(tuplecombi4, 3 ) :
    #                 print(tuplecombi3, end="")
    #                 print(" exist in freq %s" % freqkey)
    #
    # 너무 많은 결과가 나와서 의미가 없다.

    print("-------------------------------- search combi5 candidate from combi3 class ----------------------")
    for tuplecombi5 in ddictFreqListcombi5[combi5MaxFreq]:
        print("combi5 is ", end="")
        print(tuplecombi5)
        for freqkey in ddictFreqListcombi3.keys():
            for tuplecombi3 in ddictFreqListcombi3[freqkey]:
                if tuplecombi3 in itertools.combinations(tuplecombi5, 3):
                    print(tuplecombi3, end="")
                    print(" exist in freq %s" % freqkey)
    # 2017.9.17일 기준으로 바로위의 결과는 다음과 같고, ddictFreqListcombi3[3]에서 주로 후보군이 많이 나온다.
    '''
combi5 is (14, 27, 30, 31, 40)
(14, 27, 31) exist in freq 3
(14, 27, 40) exist in freq 3
(27, 30, 31) exist in freq 3
(27, 30, 40) exist in freq 3
(27, 31, 40) exist in freq 3
(30, 31, 40) exist in freq 3
(14, 30, 40) exist in freq 2
(14, 30, 31) exist in freq 4
(14, 31, 40) exist in freq 4
(14, 27, 30) exist in freq 5
combi5 is (14, 15, 18, 21, 26)
(14, 15, 21) exist in freq 3
(14, 18, 26) exist in freq 3
(15, 18, 26) exist in freq 3
(15, 21, 26) exist in freq 3
(14, 21, 26) exist in freq 2
(14, 15, 26) exist in freq 4
(14, 15, 18) exist in freq 4
(14, 18, 21) exist in freq 4
(15, 18, 21) exist in freq 4
(18, 21, 26) exist in freq 4
combi5 is (10, 22, 34, 36, 44)
(10, 22, 44) exist in freq 3
(22, 36, 44) exist in freq 3
(34, 36, 44) exist in freq 3
(10, 22, 36) exist in freq 3
(10, 34, 44) exist in freq 3
(22, 34, 44) exist in freq 3
(10, 22, 34) exist in freq 2
(10, 34, 36) exist in freq 2
(10, 36, 44) exist in freq 4
(22, 34, 36) exist in freq 4
combi5 is (15, 19, 21, 34, 44)
(19, 34, 44) exist in freq 3
(15, 19, 44) exist in freq 3
(15, 21, 44) exist in freq 3
(15, 34, 44) exist in freq 3
(15, 19, 21) exist in freq 2
(19, 21, 44) exist in freq 2
(19, 21, 34) exist in freq 4
(21, 34, 44) exist in freq 4
(15, 19, 34) exist in freq 5
(15, 21, 34) exist in freq 6
combi5 is (16, 26, 31, 36, 43)
(16, 31, 43) exist in freq 3
(16, 31, 36) exist in freq 3
(26, 31, 43) exist in freq 3
(26, 36, 43) exist in freq 3
(16, 26, 31) exist in freq 2
(16, 26, 36) exist in freq 2
(16, 26, 43) exist in freq 2
(16, 36, 43) exist in freq 2
(31, 36, 43) exist in freq 2
(26, 31, 36) exist in freq 4
combi5 is (11, 17, 21, 26, 36)
(11, 17, 26) exist in freq 3
(11, 17, 36) exist in freq 3
(17, 21, 36) exist in freq 3
(11, 21, 26) exist in freq 3
(11, 21, 36) exist in freq 3
(11, 26, 36) exist in freq 2
(17, 21, 26) exist in freq 2
(21, 26, 36) exist in freq 4
(17, 26, 36) exist in freq 5
(11, 17, 21) exist in freq 5
combi5 is (7, 22, 24, 31, 34)
(7, 22, 24) exist in freq 3
(7, 24, 34) exist in freq 3
(7, 22, 31) exist in freq 2
(7, 24, 31) exist in freq 2
(7, 31, 34) exist in freq 2
(22, 24, 31) exist in freq 2
(22, 24, 34) exist in freq 2
(24, 31, 34) exist in freq 4
(22, 31, 34) exist in freq 4
(7, 22, 34) exist in freq 4
    '''

    # 정리하자면,
    # combi=5, freq=2 인 경우는  현재 최고의 조합이다. 그러나,  같은 후보를 구하기 위해서는
    # combi=5, freq=1 인 경우에서 찾아야 하겠지만,   combi=5, freq=1 조합은 모든 inning에서 찾을 수 있으므로
    # 사실상 의미가 없다.

    # combi=4, freq=3(현재 Max)에서  combi=5, freq=2 조합이 될  후보군을 추출한다.  하지만,
    # combi=4, freq=3 인 후보군이  될 수 가 없다.  왜냐하면,  combi=4, freq=3 조합이 한 번 더 나오면
    # 이는 combi=4, freq=4 인 경우가 되고 그런 경우는 현재 나온 이력이 없으므로,  후보군이 될 수 가 없다.


    print("-------------------------------- print combi4 freq=2  ----------------------")
    pprint.pprint(len(ddictFreqListcombi4[2]))
    print("-------------------------------- print combi3 freq=3  ----------------------")
    pprint.pprint(len(ddictFreqListcombi3[3]))

    # 즉 후보군은 combi=4, freq=2 에서 찾아야 한다.  2017.09.17 기준으로 378 개의 후보가 나온다.
    # 즉 후보군은 combi=3, freq=3 에서 찾아야 한다.  2017.06.17 기준으로 1035 개의 후보가 나온다.

    print("-------------------------------- if ddictFreqListcombi3[3] in ddictFreqListcombi4[2] ----------------------")
    # 다음은 combi=4, freq=2 의 후보군과 combi=3, freq=3 의 후보군의 교집합을 찾아보자.
    listcombi42combi33 =[]
    for tuplecombi4 in ddictFreqListcombi4[2]:
        listcontain = [ set(tuplecombi4).issuperset(set(tuplecombi3)) for tuplecombi3 in ddictFreqListcombi3[3] ]
        if any(listcontain) :
            listcombi42combi33.append(tuplecombi4)
    print("len(listcombi42combi33) = %s"%(len(listcombi42combi33)))
    # 현재 까지 위의 결론은  2017.06.17 기준으로 318개가 나온다.
    print("-------------------------------- condition :  combi4 freq=2  and  restn, close  ----------------------")

    # ddictFreqListcombi4[2] 은 combi=4, freq=2  조합의 list이다.
    # 친밀도를 구하기 위해  combi3rest2close 을 사용한다.
    # combi4rest2close 은 절적하지 않다. 이미 포화이므로.
    #
    setmax = set()
    list_close8_tuplecombi4 = []
    for tuplecombi4 in ddictFreqListcombi4[2] :
        print("tuplecombi4 : ", end="")
        print(tuplecombi4)
        close_sum_for_tuplecombi4 = 0
        for tuplecombi3 in itertools.combinations(tuplecombi4, 3 ) :
            restn, close = combi3rest2close.getlistbestrest(list(tuplecombi3))
            setmax.add(close)
            close_sum_for_tuplecombi4 += close
            print("tuplecombi3 : ", end="")
            print(tuplecombi3, end="")
            print("  restn : ", end="")
            print(restn, end="")
            print("\t\tclose : %s" % close)

        if close_sum_for_tuplecombi4 == 8 :
            list_close8_tuplecombi4.append(tuplecombi4)

    print("max close is %s" % max(setmax))

    # close을 확인해 보면, max=2 이다.
    # 그래서 combi=4 조건에서 combi=3을 구하면, 4가지가 나오고, restn=2 인 경우에 대해,
    # 전부 close= 2,2,2,2 가 나오는 경우 즉 close_sum_for_tuplecombi4 = 8 이 되는 combi=4만 모은다
    pprint.pprint(list_close8_tuplecombi4)

    print("-------------------------------- list_close8_tuplecombi4 에 대해, 각각 restn을 print하기  ----------------------")

    # list_close8_tuplecombi4 에 있는  combi=4에 대해, (combi=3, restn=2)인 restn을 구하고,
    # restn 의 각각의 원소의 빈도수를 구해서, 빈도수가 많은 restn을 포함하는 combi=4 를 선택한다.

    ddict_no_freq = collections.defaultdict(int)
    for tuplecombi4 in list_close8_tuplecombi4 :
        print("tuplecombi4 : ", end="")
        print(tuplecombi4 ,end=" ")
        for tuplecombi3 in itertools.combinations(tuplecombi4, 3 ) :
            restn, close = combi3rest2close.getlistbestrest(list(tuplecombi3))
            print(restn, end=" ")
            for rest in restn :
                if not rest in list(tuplecombi4) :
                    ddict_no_freq[rest] += 1

        print(" ")

    pprint.pprint(ddict_no_freq)

    # ddict_no_freq 을 보고서, 가장 빈도수가 큰 숫자를 포함하는 combi=4을 선택하고, restn도 선택한다.

    '''
    최종적으로 선택한 것은 
    14, 15, 18, 21, 26, 34  
    11, 17, 21, 26, 36, 44
    '''

    exit(0)



    setitemcount = set()
    setitemmax = set()
    listlistTuplecombiCdicttemp = []
    for tuplecombi in listtuplecombimax_1 :
        cdicttemp = collections.Counter()

        for tuplerest in combi4rest1close.getlisttupleSubordinateRest(list(tuplecombi)) :
            cdicttemp[tuplerest] += 1

        for listtuplerest in [combi3rest1close.getlisttupleSubordinateRest(list(aa)) for aa in itertools.combinations(tuplecombi, 3 )]:
            for tuplerest in listtuplerest:
                cdicttemp[tuplerest] += 1

        for listtuplerest in [combi3rest2close.getlisttupleSubordinateRest(list(aa)) for aa in itertools.combinations(tuplecombi, 3 )]:
            for tuplerest in listtuplerest:
                cdicttemp[tuplerest] += 1

        for listtuplerest in [combi2rest2close.getlisttupleSubordinateRest(list(aa)) for aa in itertools.combinations(tuplecombi, 2 )]:
            for tuplerest in listtuplerest:
                cdicttemp[tuplerest] += 1

        for listtuplerest in [combi2rest1close.getlisttupleSubordinateRest(list(aa)) for aa in itertools.combinations(tuplecombi, 2 )]:
            for tuplerest in listtuplerest:
                cdicttemp[tuplerest] += 1

        print(str(tuplecombi) + ": ", end="")
        print("\titemcount: %s, " % len(cdicttemp), end="")
        print("\titemmax : %s" % max(cdicttemp.values()))

        listlistTuplecombiCdicttemp.append([tuplecombi,cdicttemp])

        setitemcount.add(len(cdicttemp))
        setitemmax.add(max(cdicttemp.values()))

    minitemcount = min(setitemcount)
    maxitemmax = max(setitemmax)
    print("----------------------------------------------------------------")
    print("minitemcount : %s,  " % minitemcount, end="")
    print("maxitemmax : %s,  " % maxitemmax)
    print("\n")
    for listTuplecombiCdicttemp in listlistTuplecombiCdicttemp :
        if max(listTuplecombiCdicttemp[1].values()) == maxitemmax : # and len(listTuplecombiCdicttemp[1]) == minitemcount:
            print("\n" + str(listTuplecombiCdicttemp[0]) + " : ")
            for key in listTuplecombiCdicttemp[1] :
                print("\t" + str(key) +"\t:"+ str(listTuplecombiCdicttemp[1][key]))
        else:
            print(".", end="")

    """
    위의 print에서 maxitemmax==7 인 경우를 찾아보면 아래처럼 tuplecombi, tuplerest의 조합이 3가지 나온다. 이를 채택한다.
    (6, 12, 17, 32) : (18, 31)
    (14, 15, 26, 35) : (18, 21)
    (15, 18, 21, 35) : (14, 26)
    """

    exit()

    tableinningno.writeCombiMatchwithTable(4,3,1,clsvar)

    listcandidate = [22,33,36,37]
    listexcept = [3, 11, 13, 18, 20,21, 24, 45]
    listcandidateplus = list( set(range(1,46)) - set(listcandidate) - set(listexcept) )

    value = 0
    for combicandi in itertools.combinations(listcandidate, 2 ) :
        for combicandiplus in  itertools.combinations(listcandidateplus, 2 ) :
            value = max([value, combi2rest2close.getcloseness( list(combicandi),list(combicandiplus) ) ])

    print("max of combicandi and combicandiplus is %s" % value )
    for combicandi in itertools.combinations(listcandidate, 2 ) :
        for combicandiplus in  itertools.combinations(listcandidateplus, 2 ) :
            if  combi2rest2close.getcloseness( list(combicandi),list(combicandiplus) ) == value :
                print("big combi is %s %s"%(combicandi,combicandiplus ))

    exit()

    # How to select and candidate the number
    # 1. writeCombiMatchwithTable(4,3,1,clsvar) 실행. 즉  combi=4, combiinside=3, rest=1 을 실행하고, listmax, listmax_1을  만든다.
    # 2. 앞에서 만든  (combiinside, rest, closeness) 조합을 만족하는 것으로,   listmax_1 - listmax 을 실행하여 Diff group을 만들고,
    # 3. Diff group와 listmax 와의 set 차집합 중, 가장 개수가 큰 것을 isection%s 으로 표시.
    # 4. csv file에서  lenmax_1 == 2 이고, combi intersection이 가장 큰 것 ( 여기서는 2 ) 만을 선택한다. ==> lenmax = 3 인 집단과의 유사성을 활용.
    # 5. closeness가 모두 1인 것만 선택한다. 2 이상은 가능성이 적은 것으로 판단.
    # 6. combi가 같은  2개의 조합에서,  그 inning 간격 + last inning = 현재 진행 innning과 가장 비슷한 것을 후보로 선택한다.
    # 7. 20161021일 기준으로 22,33,36,37 이 후보이다.
    # 8. 22,33,36,37의 combi 에서  intersection=2을 만들어 낸  combi을  lenmax = 3의 그룹에서 찾는다.
    #  --> 3,13,33,37 이다.  해당 inning과 no6은
    # 434	3	13	20	24	33	37
    # 572	3	13	18	33	37	45
    # 698	3	11	13	21	33	37
    #  22,33,36,37 와 차집합을 판단하면,   ( 3, 11, 13, 18, 20,21, 24, 45)은 나오지 않을 숫자이다.

    # max of combicandi and combicandiplus is 2
    # big combi is (22, 36) (10, 34)
    # big combi is (22, 36) (10, 44)
    # big combi is (22, 36) (34, 44)
    # big combi is (22, 37) (16, 17)
    # big combi is (22, 37) (23, 25)
    # big combi is (22, 37) (27, 31)
    # big combi is (33, 36) (4, 25)   --> 선택 2 가지 이므로 , 3가지는 달성되어야 할 목표이다.
    # big combi is (33, 36) (7, 40)   --> 선택 2 가지 이므로 , 3가지는 달성되어야 할 목표이다.
    # big combi is (33, 37) (2, 35)
    # big combi is (36, 37) (12, 34)
    # big combi is (36, 37) (16, 38)

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

    #마지막 회차 기준으로 다음 회차에 나올 가능성을  listtuple형태로 계산하고 sorting.tuple형태 : ( 번호, diffinning, 발생횟수)
    listtupleNumInningOccurs = nextsel.makeListtupleNumInningOccurs()
    listtupleNumInningOccurs = sorted(listtupleNumInningOccurs, key= lambda tripair: tripair[2], reverse=True)
    print ("Based on the last Inning, possibility of listtupleNumInningOccurs")
    print (listtupleNumInningOccurs)

    # 마지막 회차 기준으로 다음에 나올 수 있는 숫자를 CandidateNoMax 개수만큼 후보자를 구한다.
    listtuplecandidateNoInningOccurs = []
    CandidateNoMax = 9
    occursprev = 10000

    for tupleNumInningOccurs in listtupleNumInningOccurs :
        no, diffinning, occurs = tupleNumInningOccurs
        if len(listtuplecandidateNoInningOccurs) >= CandidateNoMax  and occursprev > occurs :
            break

        # no가 이전의 -diffinning에서 존재했는지 조사.
        if no in listlistinningnos[-diffinning][1:] :
            # listtuplecandidateNoInningOccurs에 이미 같은 번호가 있는지 조사한다.
            if not no in [ NoInningOccurs[0] for NoInningOccurs in listtuplecandidateNoInningOccurs  ]:
                listtuplecandidateNoInningOccurs.append(tupleNumInningOccurs)
                occursprev = occurs


    # 마지막 회차 기준으로 다음 회차에 나올 가능성이 가장 큰 순서대로 집결된 list을 print.
    print ("top 10 list of possibility of occurances:")
    print (listtuplecandidateNoInningOccurs)


    # listtuplecandidateNoInningOccurs = list [ tuple(no, diffinning, countadvent)]

    # listtuplecandidateNoInningOccurs 을 기준으로, 숫자6개(lotto 수자 6개 )를 뽑아서 조합을 만들수 있는 경우에 대한 list을 만든다.
    # list의 내용은 listtuplecandidateNoInningOccurs의 index을 지칭한다.

    listlistcandidate6index = []
    sizeCandidatelist = len(listtuplecandidateNoInningOccurs)

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
        listcandidate6No = [listtuplecandidateNoInningOccurs[index][0] for index in listcandidate6index ]
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






