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

    def makeListTurpleNumInningOccurs(self):
        #마지막 회차 기준으로 다음 회차에 나올 가능성을  listturple형태로 계산
        listturpleNumInningOccurs = []
        for no in range(1, MAXNO+1) :
            for diffinning in range(1, MAXDIFFINNING + 1) :
                listturpleNumInningOccurs.append((no, diffinning,self.dictdictdiffInning[no][diffinning] ))
        return listturpleNumInningOccurs

class   CombiRestCloseness():
    def __init__(self, listlistinningnos, combin, restn):
        if combin < restn  and (combin + restn) >= 6 :
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

        if not hasattr(self, "listcombinrestnclosesorted") :
            print("listcombinrestnclosesorted is not exist")
            return

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
        if not hasattr(self, "ddictcombinrestncloseness") :
            print("ddictcombinrestncloseness is not exist")
            exit()

        if len(listcombi) != self.combin  or len(listrestn) != self.restn :
            print("the length of parameter is not proper")
            exit()
        listcombi.sort()
        listrestn.sort()
        return self.ddictcombinrestncloseness.get((tuple(listcombi), tuple(listrestn)), 0)

    def getlistbestrest(self, listcombi):
        if not hasattr(self, "listcombinrestnclosesorted") :
            print("listcombinrestnclosesorted is not exist")
            exit()

        listcombi.sort()
        tupletemp = tuple(listcombi)
        for combinrestnclose in self.listcombinrestnclosesorted :
            combinrestn , close = combinrestnclose
            tuplecombi, tuplerest = combinrestn
            if tuplecombi == tupletemp :
                return list(tuplerest)


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

    combi4rest2close = CombiRestCloseness(listlistinningnos, 4, 2)
    # combi4rest2close.writecombirestclose()

    clsvar = CLSVAR()

    clsvar.combi1rest1close = combi1rest1close
    clsvar.combi2rest1close = combi2rest1close
    clsvar.combi2rest2close = combi2rest2close
    clsvar.combi3rest2close = combi3rest2close
    clsvar.combi3rest1close = combi3rest1close
    clsvar.combi4rest1close = combi4rest1close
    clsvar.combi4rest2close = combi4rest2close

    tableinningno.writeCombiMatchwithTable(4,3,1,clsvar)

    exit()

    # How to select and candidate the number
    # 1. writeCombiMatchwithTable(4,3,1,clsvar) 실행
    # 2. csv file에서  lenmax_1 == 2 이고, combi intersection이 가장 큰 것 ( 여기서는 2 ) 만을 선택한다. ==> lenmax = 3 인 집단과의 유사성을 활용.
    # 3. closeness가 모두 1인 것만 선택한다. 2 이상은 가능성이 적은 것으로 판단.
    # 4. combi가 같은  2개의 조합에서,  그 inning 간격 + last inning = 현재 진행 innning과 가장 비슷한 것을 후보로 선택한다.
    # 5. 20161021일 기준으로 22,33,36,37 이 후보이다.
    # 6 22,33,36,37의 combi 에서  intersection=2을 만들어 낸  combi을  lenmax = 3의 그룹에서 찾는다.
    #  --> 3,13,33,37 이다.  해당 inning과 no6은
    # 434	3	13	20	24	33	37
    # 572	3	13	18	33	37	45
    # 698	3	11	13	21	33	37 ( 가장 최근 --> 제거 )
    #  22,33,36,37 와 차집합을 판단하면,    3, 13, 18, 20, 24, 45 이 나온다.

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






