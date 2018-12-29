from lotto import *

def MappingCombi3ToPlate45(nCombi):
    combiFrom45 = CombiFrom45()
    listtuplecombifrom45 = combiFrom45.GetListCombiFrom45(nCombi)

    tableinningno = TableInningNo("lotto.csv")

    # nCombi 일어나는 경우에 대해 발생회수별로  조사한다.
    dictnCombiFreq = tableinningno.GetDictCombiFreq(nCombi)

    totalCombiNO = len(listtuplecombifrom45)
    freqCombiNo = len(dictnCombiFreq)

    print("Combination : %d"%nCombi)
    print("Total Combi NO : %d" % totalCombiNO )
    print("Freq Combi NO : %d"%  freqCombiNo )
    print("Rate : %f"%(freqCombiNo/totalCombiNO))
    print("Diff : %d" % ( totalCombiNO - freqCombiNo))

    dictFreqListCombi = tableinningno.GetDictFreqListCombi(nCombi)
    for freq, listCombi in dictFreqListCombi.items() :
        print("freq:%d, len:%d"%(freq, len(listCombi)))

    print("-----------------------------------------------------------------")

    Found45 = 1 ;       #처음이거나, tuple에서 마지막 45 숫자를 발견했을 경우.
    for tuplecombi in listtuplecombifrom45:
        # 처음이므로, tuple을 print한다.
        if( Found45 == 1 ):
            print(tuplecombi, end=": ")
            Found45 = 0
        print("%02d," % dictnCombiFreq.get(tuplecombi, 0 ), end="")
        if( 45 in tuplecombi):
            print("\n", end="")
            Found45 = 1


if __name__ == "__main__":
    MappingCombi3ToPlate45(4)

'''
Combination : 3
Total Combi NO : 14190
Freq Combi NO : 9860
Rate : 0.694856
Diff : 4330
freq:1, len:5234
freq:3, len:1200
freq:2, len:3007
freq:4, len:328
freq:5, len:66
freq:6, len:25

(14, 30, 31): 고려하자.
(15, 21, 22):
(18, 31, 32):
(21, 26, 27):
(34, 42, 43): 고려하자.

---------------------------
(8, 20, 28)
(12, 14, 22)
(11, 14, 20)
(11, 27, 45)

(15, 29, 36)
(15, 29, 37)
(15, 30, 37)
-----------------------------
(16, 22, 33)
(17, 31, 41)

(20, 25, 35)
(34, 43, 44)
--------------------------------
(최종선정.)
(8, 20, 28) (16, 22, 33)
(15, 29, 37) (17, 31, 41)
(15, 30, 37) (34, 43, 44)


-----------------------------------------------------------------
(1, 2, 3): 03,02,01,03,01,03,04,03,01,01,01,01,03,02,02,03,05,02,00,00,03,01,04,02,01,02,01,00,01,00,01,02,00,02,01,04,00,01,00,03,00,01,01,
(1, 3, 4): 01,00,01,01,03,01,01,01,04,00,03,02,02,02,03,00,04,03,02,01,02,03,02,04,01,02,02,02,04,00,01,02,01,03,00,00,01,03,03,02,01,03,
(1, 4, 5): 01,02,00,03,01,02,00,02,01,01,00,02,01,01,01,01,00,00,03,00,00,01,00,01,01,00,03,00,01,01,00,00,02,03,01,02,02,02,00,00,03,
(1, 5, 6): 03,00,00,02,01,02,02,02,02,00,01,00,03,02,03,02,00,01,02,01,01,03,01,01,02,01,01,00,05,01,03,01,01,02,01,02,02,00,01,00,
(1, 6, 7): 00,00,03,00,01,00,00,02,00,03,02,00,01,02,00,01,00,01,01,00,01,04,00,00,01,00,01,01,00,00,00,00,01,00,01,03,00,00,01,
(1, 7, 8): 01,01,01,01,02,00,01,01,01,00,02,01,01,00,01,03,01,00,01,02,00,00,00,00,00,01,02,01,01,04,02,00,01,01,04,00,00,00,
(1, 8, 9): 01,01,02,01,03,01,01,00,03,04,02,00,02,02,01,03,00,01,01,01,04,00,02,01,02,03,00,01,02,03,04,00,00,04,02,02,02,
(1, 9, 10): 02,01,04,00,02,00,02,04,00,01,00,04,00,02,00,01,01,01,04,03,00,01,01,01,00,01,01,00,01,01,01,01,01,01,00,00,
(1, 10, 11): 00,03,04,00,01,04,02,01,02,04,01,00,01,02,02,03,02,03,02,00,02,03,01,00,03,01,02,01,00,04,01,02,02,01,01,
(1, 11, 12): 02,02,02,02,01,03,03,00,00,02,01,03,03,01,02,00,03,00,01,00,01,00,02,01,02,01,01,01,02,00,02,00,02,01,
(1, 12, 13): 01,02,01,03,01,03,00,01,03,01,05,00,00,03,02,03,02,00,00,02,02,01,02,02,01,01,01,01,03,03,03,00,02,
(1, 13, 14): 01,00,01,00,01,01,01,01,02,00,01,01,02,00,03,01,00,00,02,02,03,01,01,02,01,02,02,00,01,03,00,02,
(1, 14, 15): 00,02,00,02,00,02,01,00,00,00,00,02,01,01,02,00,00,01,01,02,01,00,02,00,01,00,01,01,02,01,00,
(1, 15, 16): 01,01,01,02,02,00,01,01,01,03,01,00,01,00,00,00,01,00,01,01,01,01,00,01,01,01,03,00,01,02,
(1, 16, 17): 02,03,01,02,01,00,00,01,01,01,00,01,01,01,00,01,01,02,01,01,01,02,00,02,02,01,02,00,00,
(1, 17, 18): 00,01,02,02,01,00,02,01,01,01,04,04,01,03,02,01,01,02,01,01,00,02,02,02,02,01,02,03,
(1, 18, 19): 01,01,00,00,02,01,00,01,02,00,03,02,00,02,01,02,00,01,01,03,00,01,02,01,01,01,01,
(1, 19, 20): 02,00,00,00,03,00,01,01,01,00,01,00,00,00,02,01,01,00,01,01,02,01,03,01,01,00,
(1, 20, 21): 00,01,01,03,03,03,02,02,01,02,01,01,02,01,03,01,02,00,01,02,01,01,01,01,02,
(1, 21, 22): 01,01,02,01,03,02,00,04,00,01,01,01,01,02,02,01,01,01,02,03,01,00,02,01,
(1, 22, 23): 00,00,02,00,00,02,00,00,01,01,02,00,00,00,02,01,00,01,00,01,00,00,01,
(1, 23, 24): 00,01,01,01,02,01,01,01,00,01,03,01,00,01,01,01,02,00,03,01,01,01,
(1, 24, 25): 01,01,01,01,02,03,01,01,01,01,01,01,00,00,00,02,01,03,00,02,00,
(1, 25, 26): 01,00,02,00,00,00,00,00,00,01,01,01,02,01,01,01,00,00,01,01,
(1, 26, 27): 03,03,03,00,01,01,01,02,03,02,02,00,00,04,03,02,02,01,00,
(1, 27, 28): 03,03,01,00,02,02,01,03,02,02,00,01,02,00,02,00,00,01,
(1, 28, 29): 01,01,00,02,00,04,03,01,02,00,00,04,04,02,02,01,04,
(1, 29, 30): 00,01,01,03,02,01,01,03,01,00,01,00,01,01,01,01,
(1, 30, 31): 00,01,00,03,01,01,00,00,00,00,02,01,01,00,00,
(1, 31, 32): 00,00,03,00,00,00,00,00,01,00,01,02,02,00,
(1, 32, 33): 01,00,02,01,02,00,00,03,02,01,00,00,03,
(1, 33, 34): 01,02,00,01,00,00,01,00,02,02,00,01,
(1, 34, 35): 01,03,02,01,03,02,01,02,03,03,02,
(1, 35, 36): 00,01,00,00,01,02,01,02,01,02,
(1, 36, 37): 02,00,01,02,03,02,00,01,01,
(1, 37, 38): 01,01,03,01,02,02,00,01,
(1, 38, 39): 00,02,01,00,00,00,01,
(1, 39, 40): 01,00,00,02,00,01,
(1, 40, 41): 03,01,01,01,01,
(1, 41, 42): 02,02,01,00,
(1, 42, 43): 02,02,00,
(1, 43, 44): 01,01,
(1, 44, 45): 00,
(2, 3, 4): 01,03,01,02,00,01,00,03,03,01,01,02,01,01,00,00,05,00,02,01,02,01,02,05,00,00,01,00,00,00,00,00,00,01,01,01,01,00,01,02,03,00,
(2, 4, 5): 02,01,00,02,00,00,02,00,00,00,03,02,04,00,01,04,02,00,01,01,02,02,03,02,01,00,03,01,01,04,01,02,01,01,01,00,00,00,02,01,00,
(2, 5, 6): 02,01,01,00,01,03,01,01,01,01,01,01,03,01,02,00,00,01,02,00,00,02,01,00,00,01,03,01,01,00,01,00,00,02,01,00,00,00,02,00,
(2, 6, 7): 01,01,01,00,01,03,02,01,00,03,01,01,02,02,02,01,00,00,01,00,00,03,01,01,01,00,03,01,00,00,00,00,00,01,00,01,00,01,01,
(2, 7, 8): 01,02,01,00,02,01,01,03,01,03,01,02,01,01,01,00,03,02,01,01,01,03,01,00,00,03,01,00,01,00,01,01,02,01,01,02,02,03,
(2, 8, 9): 01,00,01,00,01,02,02,00,04,01,01,02,01,02,01,01,04,01,01,01,03,02,02,01,05,01,02,02,03,03,02,00,03,01,01,01,01,
(2, 9, 10): 01,00,01,00,00,01,01,02,00,01,00,00,01,02,01,03,01,00,01,00,00,01,00,01,01,00,00,00,01,00,02,01,01,01,00,02,
(2, 10, 11): 01,02,01,01,01,01,00,02,03,00,00,02,00,00,01,01,00,00,00,00,02,02,01,01,01,01,00,01,01,00,00,01,00,02,01,
(2, 11, 12): 01,02,01,02,01,03,02,02,00,03,00,01,00,02,03,03,03,00,01,01,01,01,01,01,01,02,00,04,00,01,02,01,01,01,
(2, 12, 13): 00,02,03,00,02,00,03,02,01,01,02,02,00,00,01,01,00,00,02,00,03,01,00,00,02,01,02,03,02,02,00,02,02,
(2, 13, 14): 01,01,01,00,01,01,01,00,00,00,00,02,00,01,03,01,02,01,00,00,01,00,00,01,01,00,00,00,03,00,02,02,
(2, 14, 15): 01,01,02,00,00,00,01,03,01,01,01,00,01,01,01,02,00,01,01,00,00,01,00,01,00,03,01,01,00,01,02,
(2, 15, 16): 01,00,01,02,04,02,03,04,02,02,00,01,02,02,01,02,00,00,05,00,01,01,00,00,01,01,01,01,03,02,
(2, 16, 17): 02,00,03,02,00,00,00,01,01,02,01,01,02,02,01,01,01,02,02,02,00,00,02,02,01,02,00,01,02,
(2, 17, 18): 01,04,01,01,01,00,04,00,02,03,03,02,02,02,02,01,01,00,01,02,02,03,01,01,02,00,00,03,
(2, 18, 19): 02,01,02,00,01,02,01,00,01,01,02,00,01,02,02,02,00,01,01,01,01,01,00,01,01,01,00,
(2, 19, 20): 01,00,00,01,03,03,01,02,02,01,00,01,01,00,03,03,02,01,01,02,00,02,04,01,01,03,
(2, 20, 21): 01,00,00,02,01,00,03,00,02,01,00,00,04,04,02,00,01,01,00,01,00,00,01,01,01,
(2, 21, 22): 01,00,00,02,01,01,01,01,00,00,00,02,04,00,01,00,01,01,00,01,02,01,01,02,
(2, 22, 23): 01,01,02,00,02,00,00,01,01,01,01,00,00,02,01,00,00,01,01,00,00,02,01,
(2, 23, 24): 00,01,00,00,00,00,00,01,00,00,02,00,00,01,01,00,02,01,00,01,02,00,
(2, 24, 25): 00,00,01,01,01,01,01,01,01,02,01,01,01,00,01,02,02,01,01,02,02,
(2, 25, 26): 03,01,04,02,00,02,01,01,01,00,03,03,01,03,02,01,02,01,01,04,
(2, 26, 27): 02,00,01,00,00,00,00,00,00,00,02,00,00,02,00,00,04,03,00,
(2, 27, 28): 01,00,01,00,01,02,00,02,01,01,01,01,01,02,02,01,02,00,
(2, 28, 29): 01,01,01,01,00,02,01,00,02,01,02,00,00,02,00,01,02,
(2, 29, 30): 01,01,01,00,01,00,01,00,01,01,01,00,00,02,01,01,
(2, 30, 31): 01,00,01,01,00,01,00,02,00,01,01,01,00,00,02,
(2, 31, 32): 01,02,04,01,00,01,01,00,01,00,02,00,00,01,
(2, 32, 33): 01,01,01,02,00,00,01,00,00,00,01,02,01,
(2, 33, 34): 02,03,03,03,00,01,03,03,01,00,01,00,
(2, 34, 35): 02,00,01,01,00,02,01,03,01,01,04,
(2, 35, 36): 01,02,00,01,01,02,01,01,00,00,
(2, 36, 37): 01,00,02,00,01,02,00,00,00,
(2, 37, 38): 00,02,01,03,00,01,00,01,
(2, 38, 39): 00,01,00,02,00,00,03,
(2, 39, 40): 00,01,01,00,01,03,
(2, 40, 41): 01,01,01,00,00,
(2, 41, 42): 03,02,02,02,
(2, 42, 43): 00,00,03,
(2, 43, 44): 04,01,
(2, 44, 45): 00,

'''