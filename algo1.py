
from lotto import *

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

    # -------------------------------------------------------------------------
    # combi5가 일어나는 경우에 대해 발생회수별로  조사한다.
    ddictFreqListcombi5 = tableinningno.GetDictFreqListCombi(5)
    combi5MaxFreq = max(ddictFreqListcombi5.keys())
    print("Combi=5, max = %s" % combi5MaxFreq)

    # combi5MaxFreq가 max이기 때문에 다음의 경우 combi5MaxFreq + 1 인 경우가 발생하지 않는다.
    # 즉 combi5MaxFreq -1 에 해당하는 group 이 다음에 일어날 후보이다.
    candidate_listcombi5 = ddictFreqListcombi5[combi5MaxFreq -1]

    pprint.pprint(len(candidate_listcombi5))

    # -------------------------------------------------------------------------
    # combi=4 경우에 대해, 각각 출현빈도에 대한 combi list을 구한다.
    ddictFreqListcombi4 = tableinningno.GetDictFreqListCombi(4)
    combi4MaxFreq = max(ddictFreqListcombi4.keys())

    # combi4MaxFreq가  max이기 때문에 다음의 경우 combi4MaxFreq + 1 인 경우가 발생하지 않는다.
    # 즉 candidate_listcombi5 에서  combi4MaxFreq인 경우을  제거 한다.
    notcandidate_listcombi4 = ddictFreqListcombi4[combi4MaxFreq]

    diff_combi5 = []
    for combi5t in candidate_listcombi5 :
        for combi4t in notcandidate_listcombi4 :
            if( set(combi4t).issubset(combi5t)):
                diff_combi5.append(combi5t)

    candidate_listcombi5 = list( set(candidate_listcombi5) - set(diff_combi5))
    pprint.pprint(len(candidate_listcombi5))

    # 반대로, combi4MaxFreq-1 의 경우는   오히려 잘 나타나는 경우이므로 이를 candidate_listcombi5 에서 찾는다.
    candidate_listcombi4 = ddictFreqListcombi4[combi4MaxFreq -1]

    diff_combi5 = []
    for combi5t in candidate_listcombi5:
        for combi4t in candidate_listcombi4:
            if (set(combi4t).issubset(combi5t)):
                diff_combi5.append(combi5t)

    candidate_listcombi5 = diff_combi5
    pprint.pprint(len(candidate_listcombi5))

    # -------------------------------------------------------------------------
    # combi=3 경우에 대해, 각각 출현빈도에 대한 combi list을 구한다.
    ddictFreqListcombi3 = tableinningno.GetDictFreqListCombi(3)
    combi3MaxFreq = max(ddictFreqListcombi3.keys())

    # combi3MaxFreq 가  max이기 때문에 다음의 경우 combi3MaxFreq + 1 인 경우가 발생하지 않는다.
    # 즉 candidate_listcombi5 에서  combi3MaxFreq 인 경우을  제거 한다.
    notcandidate_listcombi3 = ddictFreqListcombi3[combi3MaxFreq]

    diff_combi5 = []
    for combi5t in candidate_listcombi5:
        for combi3t in notcandidate_listcombi3:
            if (set(combi3t).issubset(combi5t)):
                diff_combi5.append(combi5t)

    candidate_listcombi5 = list(set(candidate_listcombi5) - set(diff_combi5))
    pprint.pprint(len(candidate_listcombi5))

    # 반대로, combi3MaxFreq-1 의 경우는   오히려 잘 나타나는 경우이므로 이를 candidate_listcombi5 에서 찾는다.
    candidate_listcombi3 = ddictFreqListcombi3[combi3MaxFreq - 1]

    diff_combi5 = []
    for combi5t in candidate_listcombi5:
        for combi3t in candidate_listcombi3:
            if (set(combi3t).issubset(combi5t)):
                diff_combi5.append(combi5t)

    candidate_listcombi5 = diff_combi5
    pprint.pprint(len(candidate_listcombi5))

    # ---------------------------------------------------------------------
    # combi=2 경우에 대해, 각각 출현빈도에 대한 combi list을 구한다.
    ddictFreqListcombi2 = tableinningno.GetDictFreqListCombi(2)
    combi2MaxFreq = max(ddictFreqListcombi2.keys())

    # combi3MaxFreq 가  max이기 때문에 다음의 경우 combi3MaxFreq + 1 인 경우가 발생하지 않는다.
    # 즉 candidate_listcombi5 에서  combi3MaxFreq 인 경우을  제거 한다.
    notcandidate_listcombi2 = ddictFreqListcombi2[combi2MaxFreq]

    diff_combi5 = []
    for combi5t in candidate_listcombi5:
        for combi2t in notcandidate_listcombi2:
            if (set(combi2t).issubset(combi5t)):
                diff_combi5.append(combi5t)

    candidate_listcombi5 = list(set(candidate_listcombi5) - set(diff_combi5))
    pprint.pprint(len(candidate_listcombi5))

    # 반대로, combi3MaxFreq-1 의 경우는   오히려 잘 나타나는 경우이므로 이를 candidate_listcombi5 에서 찾는다.
    candidate_listcombi2 = ddictFreqListcombi2[combi2MaxFreq - 1]

    diff_combi5 = []
    for combi5t in candidate_listcombi5:
        for combi2t in candidate_listcombi2:
            if (set(combi2t).issubset(combi5t)):
                diff_combi5.append(combi5t)

    candidate_listcombi5 = diff_combi5
    pprint.pprint(len(candidate_listcombi5))
    pprint.pprint(candidate_listcombi5)
    print("----- candidate_listcombi5 is finished ----")

    # ---------------------------------------------------------------------
    # 이제 candidate_listcombi5 에는 3개의 후보가 존재한다.  2018.8.25일 기준으로 .
    # 지금 부터,  1:1의 closeness 을 계산해서 큰 closeness을 선택한다.

    # 먼저 combi5에 각각에 해당하는 inning의 전체 숫자 6개를  45개의 숫자에서 제거된 closeness 후보 숫자를 구한다.
    dictlistcombi5listcloseness1 = {}
    for listinningnos in listlistinningnos :
        nos = listinningnos[1:]
        inning = listinningnos[0]
        for combi5 in candidate_listcombi5 :
            if set(combi5).issubset(set(nos)) :
                print("inning:%d "% inning)
                candidate_listno = list(set([ aa for aa in range(1 ,46)]) - set(nos))
                dictlistcombi5listcloseness1[combi5] = candidate_listno

    # dictlistcombi5listcloseness1 에는 { [combi5]:[39개의 후보숫자], ... }

    # listcloseness1 중에 가장 큰 1:1 closeness 값을 갖는 숫자 list을 찾는다.
    dictlistcombi5listcloseness1_tmp = {}
    for listcombi5, listcloseness1 in dictlistcombi5listcloseness1.items() :
        dict_no_sumcloseness = {}
        for candidate_no in listcloseness1 :
            sum = 0
            for  combi in itertools.combinations(listcombi5, 1 ) :
                sum = sum + combi1rest1close.getcloseness(list(combi) ,[candidate_no] )
            dict_no_sumcloseness[candidate_no] = sum
        maxcloseness = max(dict_no_sumcloseness.values())
        # maxclose에 해당하는 candiate no을 모은다.
        listmaxcloseno = [ no for no, sum in dict_no_sumcloseness.items() if sum == maxcloseness ]
        dictlistcombi5listcloseness1_tmp[listcombi5] = listmaxcloseno

    dictlistcombi5listcloseness1 = dictlistcombi5listcloseness1_tmp

    # dictlistcombi5listcloseness1 에는 { [combi5]:[1 or 2개의 후보숫자], ... }
    # 후보수자 2개 이상이면  combi2rest1close에서 찾아서  1개의 후보를 찾는다.

    dictlistcombi5listcloseness1_tmp = {}
    for listcombi5, listcloseness1 in dictlistcombi5listcloseness1.items():
        if(len(listcloseness1) == 1 ):
            dictlistcombi5listcloseness1_tmp[listcombi5] = listcloseness1
            continue
        dict_no_sumcloseness = {}
        for candidate_no in listcloseness1:
            sum = 0
            for combi in itertools.combinations(listcombi5, 2):
                sum = sum + combi2rest1close.getcloseness(list(combi), [candidate_no])
            dict_no_sumcloseness[candidate_no] = sum
        maxcloseness = max(dict_no_sumcloseness.values())
        # maxclose에 해당하는 candiate no을 모은다.
        listmaxcloseno = [no for no, sum in dict_no_sumcloseness.items() if sum == maxcloseness]
        dictlistcombi5listcloseness1_tmp[listcombi5] = listmaxcloseno

    dictlistcombi5listcloseness1 = dictlistcombi5listcloseness1_tmp

    # 이제 combi5에 대한 1 숫자를 다 구했다.
    # print한다.

    for tuplecombi5, listcloseness1 in dictlistcombi5listcloseness1.items() :
        combi6 = list(tuplecombi5) + listcloseness1
        combi6.sort()
        print(combi6)


    exit(0)

'''
최종 후보 숫자들. 2018.8.25
[14, 15, 25, 31, 34, 44]
[10, 18, 26, 31, 34, 44]
[10, 13, 26, 31, 34, 44]
'''
