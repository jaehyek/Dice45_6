import random
import pprint
from lotto import TableInningNo

def findMaxValueIndexlist(listvalue ) :
    """
    listvalue 에서  가장 큰 숫자의 위치를 list으로 만들어서 반환한다.
    :param listvalue: 
    :return: 
    """
    nMax = max(listvalue)
    listtemp = []
    for index in range(len(listvalue)):
        if nMax == listvalue[index] :
            listtemp.append(index)
    return  listtemp

class   MarKovState(object) :
    def __init__(self, npos, nstates ):
        '''
        MarKovState class 는  npos당 Markov 상태를  nstates x nstates matrix 형태로 state을 관리한다.
        즉 [n][m]에서   숫자 n은  현재 상태를 나태내고, m은 다음으로 이동했던 숫자를 나타내고, 
        self.listlistliststate[n][m]은  이동했던 숫자에 대한 빈도수를 나타낸다. 
        self.listlistliststate[n][0]은 사용하지 않는다. 단지 index 을 편하게 하기 위해서.
        
        :param npos:  로또의  각 자리의 수자 개수
        :param nstates: 각 자리마다의  나타날 수 있는 상태 개수
        '''

        self.npos = npos
        self.listlistliststate = []
        for pos in range(npos) :
            listlistpos = []
            self.listlistliststate.append(listlistpos)
            for i in range( nstates + 1 ) :
                liststate = []
                listlistpos.append(liststate)
                for j in range(nstates + 1 ) :
                    liststate.append(0)

        # self.listcurstate는 각 자리에 대한 현 상태를 나타낸다.
        self.listcurstate = []
        for i in range(npos) :
            self.listcurstate.append(0)

    def setPositionliststate(self, liststate):
        """
        position별 state을 list으로 받아서,  각 position에 state을 설정한다.
        :param liststate: position별 state을 list
        :return: 
        """
        for pos in range(len(liststate)) :
            listliststate = self.listlistliststate[pos]
            statenext = liststate[pos]
            statecurr = self.listcurstate[pos]

            # save next state to self.listcurstate
            self.listcurstate[pos] = statenext

            # check the first try, and then just pass
            if statecurr == 0 :
                continue

            # increment the statenext frequency according to statecurr
            listliststate[statecurr][statenext] += 1

    def getMostNextStatesforpositions(self):
        listtemp = []
        for pos in range(self.npos) :
            liststatenext = self.listlistliststate[pos][self.listcurstate[pos]]
            listtemp.append(findMaxValueIndexlist(liststatenext))
        return listtemp
            
    def setfirstlocationliststate(self, liststate ):
        """
        position은 첫번재 하나만 사용하고, serial state을 list으로 받아서 설정한다.
        :param liststate: serial state
        :return: 
        """
        listliststate = self.listlistliststate[0]
        
        for statenext in liststate :
            statecurr = self.listcurstate[0]
            # statenext 을 저장
            self.listcurstate[0] = statenext
            listliststate[statecurr][statenext] += 1 

    def get6MostNextStatefor1position(self):
        """
        self.listcurstate[0]의 현재의 상태에서 6개의 statenext을 추출해 낸다.
        이 때, 후보의 statenext가 여러 개가 될 수가 있으므로, 각각에 대해서도 
        다음의 statenext 호보를 내기 위해, recursive하게 call한다.
        :return: 
        """
        statecurr = self.listcurstate[0]

        self.listliststatereturn = []
        self.mostnextstate6 = [ 0 for aa in range(6)]
        # get the statenext list
        self.recursiveMostNextState(0, findMaxValueIndexlist(self.listlistliststate[0][statecurr]))

        return self.listliststatereturn
        
    def recursiveMostNextState(self, startindex, listnextstate):
        for nextstate in listnextstate :
            self.mostnextstate6[startindex] = nextstate
            if startindex == 5 :
                # mostnextstate6 에 6개가 채워져, listliststatereturn 에 저장한다.
                self.listliststatereturn.append(self.mostnextstate6[0:])

            else :
                # 다시 recursive하게 call 한다.
                self.recursiveMostNextState( startindex + 1 , findMaxValueIndexlist(self.listlistliststate[0][nextstate]))

def getlistMarKovfrom6position():
    """
    6자리 Position에 대해 각각 Markov을 적용한다.
    출력은 각 6 position에 대해 1개씩 다음의 state값을 출력한다. 
    :return: 
    """

    tableinningno = TableInningNo("lotto.csv")
    listlistinningnos = tableinningno.getlistlistInningNos()  # 차수, 당첨번호 list

    # 6개의 위치에 대해 각각 Markov 의 45 x 45 state을 정의한다.
    clsmarkov = MarKovState(6, 45)

    # 6개의 위치에 대해 각각 state(숫자)을 list 으로  전달,  state을  설정한다.
    for listinningnos in listlistinningnos :
        listtemp = listinningnos[1:]
        # listtemp은 항상 sort되어 있으므로, 결과에서 한 쪽 치우친 결과를 낳는다. -> shuffle을 시킨다.
        random.shuffle(listtemp)
        clsmarkov.setPositionliststate(listtemp)

    #마지막 state에 대해, 각 위치별  다음 후보 숫자들을 구하고 print한다.
    print(clsmarkov.getMostNextStatesforpositions())

    # 결론, 의미있는  list을 구할 수 없다.
    # 이유는  45x45의 matrix에서 의미있게 적절한 갯수가 있어야 하는데,
    # 755회의 숫자는 턱없이 부족하기 때문이다. 45x45 = 2045이다.




def getlistMarKovfromSerialNos():
    """
    6개의 번호를 serial 숫자로 보고, 전체 회수에 대해 Markov을 적용한다. 
    즉 자리 위치에 상관없이 적용하고. 순차적으로 6자리 후보를 찾는다.
    :return: 
    """
    tableinningno = TableInningNo("lotto.csv")
    listlistinningnos = tableinningno.getlistlistInningNos()  # 차수, 당첨번호 list

    # 1개의 위치에 대해 각각 Markov 의 45 x 45 state을 정의한다.
    clsmarkov = MarKovState(1, 45)

    for listinningnos in listlistinningnos:
        listtemp = listinningnos[1:]
        # listtemp은 항상 sort되어 있으므로, 결과에서 한 쪽 치우친 결과를 낳는다. -> shuffle을 시킨다.
        random.shuffle(listtemp)
        clsmarkov.setfirstlocationliststate(listtemp)

    listlistnos = clsmarkov.get6MostNextStatefor1position()
    print("the output count is %d" % (len(listlistnos)))

    # 나온 결과는  내부에 중복 되는 숫자가 있고, sort할 필요가 있다.
    for listno in listlistnos[::-1]:
        if len(set(listno)) < 6:
            listlistnos.remove(listno)
            continue
        listno.sort()

    print("the output count is %d" % (len(listlistnos)))
    pprint.pprint(listlistnos)

    # random.shuffle 에 따라, 항상 다른 결과를 만들어 낸다.



if __name__ == "__main__":
    getlistMarKovfrom6position()
    # getlistMarKovfromSerialNos()

    
    
