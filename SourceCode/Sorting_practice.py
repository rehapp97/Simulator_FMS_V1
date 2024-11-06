from operator import itemgetter, attrgetter

class student():
    def __init__(self):
        self.Grade = ''
        self.Age = 0
        self.Index = 0
        self.executer()

    def executer(self):
        self.__repr__()

    #def __repr__(self):
    #    return repr((self.Grade, self.Age, self.Index))

class Con():
    def __init__(self):
        self.StuedentList = []
        self.age = [17, 21, 13]
        self.grade = ['A', 'B', 'C']
        self.index = [3, 2, 1]
        self.Executer()

    def get_attr(self):
        for i in range(3):
            self.StuedentList.append(student())
            self.StuedentList[i].Grade = self.grade[i]
            self.StuedentList[i].Age = self.age[i]
            self.StuedentList[i].Index = self.index[i]

        print(self.StuedentList)

        #print("첫 리스트:", self.StuedentList)
        #[('A', 17, 3), ('B', 21, 2), ('C', 13, 1)]
        #Age순 -> [('C', 13, 1), ('A', 17, 3), ('B', 21, 2)]
    def sorting(self):
        sorted(self.StuedentList, key=attrgetter('Age'))
        #print("AGE:", self.StuedentList[0].Age)
        #print("AGE:", self.StuedentList[1].Age)
        #print("AGE:", self.StuedentList[2].Age)

    def Executer(self):
        self.get_attr()
        self.sorting()

def Main(Con0):
    Start = Con0()
    print("수정 리스트:", Start.StuedentList)
    #print("AGE:", Start.StuedentList[0].Age)
    #print("AGE:", Start.StuedentList[1].Age)
    #print("AGE:", Start.StuedentList[2].Age)

Main(Con)