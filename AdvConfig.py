import random
import re
import sys
from AdvStructure import *
#from Function import *
from CommonVariables import *
import time
from operator import itemgetter, attrgetter
from CommonFunctions import *

class Config_T():
    def __init__(self, R0, fin0, fout0): #, fout0, argvLst): 
        self.Job_index = 0
        self.i_Num_Machines = 0
        self.i_Num_parttype = 0
        self.i_Num_pallet = 0
        self.i_Num_fixturetype = 0
        self.i_Num_operation = 0
        self.i_Num_part_dependency = 0
        self.i_Transportation_time = 0
        self.i_Num_Rmc = 0
        self.i_Num_Parts = 0
        self.i_Completion_Time = 0
        self.i_Avr_Flow_Time = 0
        self.i_Fixture_Type = 0
        self.i_Release = 0
        self.i_Demand = 0
        self.i_Due_Date = 0
        self.i_Num_Process =0
        self.i_Pre_part = 0
        self.i_Num_alter_Machine = 0
        self.i_Num_fixt = 0
        
        self.Job_INDEX = None
        self.JL = None
        self.ML = None
        self.System = None #모든 part들을 system에 둔다.
        self.Dummy = None #모든 part 중 loading 조건이 되는 part들을 dummy(로딩가능한 part들 두는곳) 에 둔다.
        self.Job_queue = None #사실상 central buffer

        self.Machine_schedule = [] #기계 별 유휴시간
        self.PT = []
        self.RMC = []
        self.P = [] #전체 개별 가공품의 갯수 한계
        self.LstP_sorted = []
        self.J = [] #전체 job의 갯수 한계
        self.Pallet_type = []
        self.Fixture = []
        self.Loading_schedule = [] #로딩 언로딩 가능 시간
        self.part_due2 = []
        self.s_Pid = []
        self.Machine_Name = []
        self.i_release_time = [] 
        self.i_Machine_No = [] 

        self.Input_Sequence_Option = R0[0]
        self.Operation_Sequence_Option = R0[1]
        self.Machine_Selection_Option = R0[2]
        self.Dispatching_Option = R0[3]

        self.fin = fin0
        self.fout = fout0
        self.initialize()


    def initialize(self):
        self.read_data(self.fin)
        self.initialize_Job_INDEX(self.fin)
        self.initialize_Machine_List(self.fin)
        self.initialize_Job_List(self.fin)
        self.initialize_Machine_Queue()
        self.initialize_Joblist_Queue()
        self.initialize_Setting(self.fin)
        self.fin.close()


    def read_data(self, fin):
        sTmpLst1 = fin.readline().split()
        iTmpLst1 = StrTo_intList1(sTmpLst1)
        self.i_Num_Machines = iTmpLst1[0]
        self.i_Num_parttype = iTmpLst1[1]
        self.i_Num_pallet = iTmpLst1[2]
        self.i_Num_fixturetype = iTmpLst1[3]
        self.i_Num_operation = iTmpLst1[4]

        TmpLst_bool = fin.readline()
        
        sTmpLst1 = fin.readline().split()
        self.i_Num_part_dependency = int(sTmpLst1[0])
        sTmpLst1 = fin.readline().split()
        self.i_Transportation_time = int(sTmpLst1[0])
        
        TmpLst_bool = fin.readline()


    def initialize_Job_INDEX(self, fin):
        self.Job_INDEX = Job_Index0()


    def initialize_Machine_List(self, fin):
        int_temp = []
        temp = None
        self.ML = LList_T()
        self.Pallet_type = [Pallet_T() for i in range(self.i_Num_pallet)]

        sTmpLst1 = fin.readline().split() #str_Machine_Name
        
        for i in range(self.i_Num_Machines):
            temp_Mac = Machine_T()
            temp_Mac.i_Current_Job_End_Time = -1
            temp_Mac.i_Current_Job_Start_Time = -1
            temp_Mac.i_Current_State = 0
            temp_Mac.i_idle_time = 0
            temp_Mac.i_Total_Working_Time = 0
            temp_Mac.Job_Sequence = LList_T()
            temp_Mac.s_Machine_Name = sTmpLst1[i]
            self.ML.push_back(temp_Mac) #machine을 list에 하나씩 삽입
        #print('Machine list: ', self.ML)
        temp = self.ML.head

        sTmpLst1 = fin.readline().split() #i_release_time
        iTmpLst1 = StrTo_intList1(sTmpLst1)
        for i in range(self.i_Num_Machines):
            temp = temp.next #ML이므로 temp.Obj = Machine_T()
            #temp.Obj.Machine_Queue = LList_T()  #필요없다.
            temp.Obj.i_release_time = iTmpLst1[i]

        temp = self.ML.head
        sTmpLst1 = fin.readline().split() #i_Machine_No
        iTmpLst1 = StrTo_intList1(sTmpLst1)
        for i in range(self.i_Num_Machines):
            temp = temp.next
            temp.Obj.i_Machine_No = iTmpLst1[i]
        #print('Machine number: ', iTmpLst1)

        TmpLst_bool = fin.readline()
        
        for i in range(self.i_Num_pallet):
            sTmpLst1 = fin.readline().split() #팔렛 정보
            iTmpLst1 = StrTo_intList1(sTmpLst1)
            self.i_Num_fixt = int(iTmpLst1[0])
            self.Pallet_type[i].i_Num_Fixt = self.i_Num_fixt
            self.Pallet_type[i].Fixture = [Fixture_T() for i in range(self.i_Num_fixt)]
            self.Pallet_type[i].i_Pallet_index = i
            self.Pallet_type[i].i_rest_Pallet = 1
            self.Pallet_type[i].i_number_Pallet = 1

            for j in range(self.i_Num_fixt): #j = 0, 1
                fixture_type = iTmpLst1[j+1]
                #self.Pallet_type[i].Fixture[j] = Fixture_T()
                self.Pallet_type[i].Fixture[j].i_number_Fixture = 1 #fixture type의 갯수가 1개, fixture는 무한대
                
                self.Pallet_type[i].Fixture[j].i_fixture_no = fixture_type #어떤 fixture type인지
                self.Pallet_type[i].Fixture[j].i_rest_Fixture = self.Pallet_type[i].Fixture[j].i_number_Fixture #
                # i_rest_Fixture -> 사용중이면 1, 아니면 0
        TmpLst_bool = fin.readline()
        
        temp = self.ML.head
        
        for i in range(self.i_Num_Machines):
            temp = temp.next
            sTmpLst1 = fin.readline().split()
            iTmpLst1 = StrTo_intList1(sTmpLst1)
            int_temp.append(iTmpLst1) #기계의 유휴시간 받기

            temp.Obj.i_Current_Schedule = 0
            if (temp.Obj.i_release_time == 0): #기계의 준비시간이 0 면 바로 작업가능
                temp.Obj.i_Machine_Schedule = int_temp[i] #해당 machine의 i_Machine_Schedule에 할당
                temp.Obj.i_Number_Schedule = len(temp.Obj.i_Machine_Schedule)
                if (temp.Obj.i_Number_Schedule != 0):
                    temp.Obj.i_Next_Rest_Time = temp.Obj.i_Machine_Schedule[0] #다음 쉬는 시간은 첫번째 작업이 끝난후
                    temp.Obj.i_Next_Working_time = -1
                else:
                    temp.Obj.i_Next_Rest_Time = 31536000
                    temp.Obj.i_Next_Working_time = -1
                temp.Obj.i_Working_or_Rest = 1 #일할 수 있는 시간 안에 있으면 1, 아닐 경우는 0
            temp.Obj.i_Current_Schedule = 0

        TmpLst_bool = fin.readline()

        #print('Number of machines: ', self.i_Num_Machines)
        #print('Number of pallet: ', self.i_Num_pallet)
    
    def initialize_Job_List(self, fin):
        temp_char = ''
        temp_char2 = ''
        NJ = 0
        self.PT = [Part_Type_T() for j in range(self.i_Num_parttype)]

        for i in range(self.i_Num_parttype): #i_Num_parttype = i_Num_fixturetype
            sTmpLst1 = fin.readline().split()
            iTmpLst1 = StrTo_intList1(sTmpLst1)            
            #print(iTmpLst1)
            
            self.i_Fixture_Type = iTmpLst1[0]
            self.i_Release = iTmpLst1[1]
            self.i_Demand = iTmpLst1[2]
            self.i_Due_Date = iTmpLst1[3]
            self.i_Num_Process = iTmpLst1[4]
            self.i_Pre_part = int(iTmpLst1[5])

            sTmpLst1 = fin.readline().split()
            iTmpLst1 = StrTo_intList1(sTmpLst1)
            self.part_due2 = iTmpLst1 #해당 part_type에 포함되는 각 part들의 due_date

            NJ += self.i_Demand
            
            self.PT[i].i_Fixture_Type = self.i_Fixture_Type #PT -> part_type
            self.PT[i].i_release_time = self.i_Release
            self.PT[i].i_demand = self.i_Demand
            self.PT[i].i_Due_Date = self.i_Due_Date
            self.PT[i].i_Num_Operation = self.i_Num_Process
            self.PT[i].i_Job_ID = i
            ##Part가 들어있는 팔렛을 가리키는 걸까?
            self.PT[i].i_Pre_part = self.i_Pre_part
            self.PT[i].i_part_due = self.part_due2
            
            sTmpLst1 = fin.readline().split() #operaion id
            self.PT[i].s_PID = sTmpLst1 #Process id

            self.PT[i].i_Num_Alternative_Machine = [0 for j in range(self.i_Num_Process)]
            self.PT[i].s_Alternative_Machine_Name = [[] for j in range(self.i_Num_Process)]
            self.PT[i].i_Standard_Time = [[] for j in range(self.i_Num_Process)]
            self.PT[i].Alternative_Mac = [[] for j in range(self.i_Num_Process)]
            for j in range(self.i_Num_Process):
                sTmpLst1 = fin.readline().split()
                self.PT[i].i_Num_Alternative_Machine[j] = int(sTmpLst1[0])
                self.PT[i].s_Alternative_Machine_Name[j] = []
                self.PT[i].i_Standard_Time[j] = []
                self.PT[i].Alternative_Mac[j] = []
                for k in range(self.PT[i].i_Num_Alternative_Machine[j]):
                    self.PT[i].s_Alternative_Machine_Name[j].append(sTmpLst1[2*k+1])
                    self.PT[i].i_Standard_Time[j].append(int(sTmpLst1[2*k+2]))
        
                    temp_char = self.PT[i].s_Alternative_Machine_Name[j][k]

                    Node = self.ML.head.next                      
                    while Node != self.ML.tail:                 
                        temp_char2 = Node.Obj.s_Machine_Name    
                        if temp_char == temp_char2:             
                            break                                 
                        Node = Node.next 
                    self.PT[i].Alternative_Mac[j].append(Node.Obj)
                    #ML list에서 같은 이름의 machine을 가지는 node의 machine이 PT[i].Alternative mac이 된다
            TmpLst_bool = fin.readline()
        #print(self.PT[1].Alternative_Mac[3])
        
        self.i_Num_Parts = NJ #NJ가 Total number of part이 된다, NJ는 Demand만큼 더해진다
        
        Type = 0
        r = 0
        Demand = 0

        self.P = [Part_T() for i in range(NJ)]
        for i in range(NJ):
            self.P[i].PT = self.PT[Type] #P에 대해 어떤 Part type인지 지정
            self.P[i].i_Current_Process_No = 0
            self.P[i].i_Fixture_type = self.P[i].PT.i_Fixture_Type #PT의 fixture type을 받아온다
            self.P[i].i_Part_No = Demand
            self.P[i].i_Due_date = self.P[i].PT.i_part_due[r] #해당 part type(fixture type)에서 part_due2 리스트의 r번째 part의 due date
            self.P[i].Machine_Sequence = LList_T() #Part의 machine sequence를 나타내는 list
            self.P[i].i_release_time = self.P[i].PT.i_release_time #PT의 release time을 받아옴

            Tmp1 = self.P[i].PT.i_Num_Operation
            self.P[i].i_Select_Process_Time = [0 for j in range(Tmp1)] #operation 별로 선택된 프로세싱 타임
            self.P[i].Mac_Select = [Machine_T() for j in range(Tmp1)] #operation별로 선택된 machine
            self.P[i].s_Mac_Select_name = ['' for j in range(Tmp1)]
            #Tmp1 = self.P[i].PT.i_Num_Operation
            self.P[i].i_Mac_Select_index = [0 for j in range(Tmp1)] #operation 별로 선택된 machine 인덱스
            self.P[i].i_Terminated = 0 # Part 공정이 완료되면 '1'로 바뀐다.
            #P[i].ATWK = TWKR(&P[i], 0); #TWKR 총 대안 processing time 합한것에 그만큼의 process plan depth 나눈것. p1은 228/3 = 76의 값을 가짐
            self.P[i].i_Part_index = i
            Demand += 1
            r += 1
        
            if (Demand == self.P[i].PT.i_demand): # 각 Part type의 demand에 충족되면, 다음 part는 다음 part type으로 할당한다.
                Type += 1
                r = 0
                Demand = 0


    def initialize_Machine_Queue(self):
        self.Dummy = LList_T()
        self.System = LList_T()


    def initialize_Joblist_Queue(self):
        self.Job_queue = LList_T()
        self.J = [Job_T() for i in range(self.i_Num_pallet*10000)]
    
    
    def initialize_Setting(self, fin):
        temp = 0
        LstP = []
        LstSum_min_proc = []

        for i in range(self.i_Num_Parts):
            i_Sum_All_op_proc = 0
            for j in range(self.P[i].PT.i_Num_Operation):
                if (self.P[i].PT.i_Num_Alternative_Machine[j] != 0):
                    i_Sum_All_op_proc += min(self.P[i].PT.i_Standard_Time[j])
            LstSum_min_proc.append(i_Sum_All_op_proc)

        #self.i_Num_Parts = 모든 parttype 의 demand까지 합한 것
        for i in range(self.i_Num_Parts): #machine 셀렉션
            self.P[i].i_All_processing_time = 0 #초기화
            for j in range(self.P[i].PT.i_Num_Operation):
                if (self.P[i].PT.i_Num_Alternative_Machine[j] == 0): #첫번째 작업과 마지막 작업은 대안machine 없음
                    temp = 0
                else:
                    for k in range(self.P[i].PT.i_Num_Alternative_Machine[j]):
                        temp = self.P[i].PT.i_Standard_Time[j][k]
                        self.P[i].i_All_processing_time += temp #Alternative machine들에서의 모든 processing time을 더한다. 
            self.System.push_back(self.P[i])
        
        for i in range(self.i_Num_Parts): #[index, i_Due_date, i_All_processing_time]
                LstP.append([self.P[i].i_Part_index, self.P[i].i_Due_date, self.P[i].i_All_processing_time, LstSum_min_proc[i], self.P[i]])
        if (self.Input_Sequence_Option == 1):
            LstP = sorted(LstP, key=itemgetter(1, 3))
        else:
            LstP = sorted(LstP, key=itemgetter(2, 1))
        for i in range(self.i_Num_Parts):
            self.Dummy.push_back(LstP[i][4])
        l = 0
        """

        temp_check = self.Dummy.head.next
        while temp_check != self.Dummy.tail:
            #print(temp_check.Obj.i_Part_index)
            temp_check = temp_check.next
        """

        return 1
"""
def Main():
    finName = 'practice_data0.txt'
    #finName = sys.argv[5]
    fin = open(finName, 'r')

    foutName = 're.txt'
    #foutName = sys.argv[6]
    fout = open(foutName, 'w')

    #python my_cf.py 1 1 1 1 input.txt re.txt
    #RuleCombi1 = [Input_Sequence_Option(2), Machine_Selection_Option(2), Job_route_Option(3), Dispatching_Option(5)]
    #RuleCombi1 = [int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])]
    RuleCombi1 = [1, 1, 1, 1]
    #argvLst = []

    Begin = time.time()
    con0 = Config_T(RuleCombi1, fin, fout)


    #foutName.writelines(Completion_Time, '', tardy, '', total_Flow_Time, f_Duration)
    
    return 0
    #print(iDuration)
Main()
"""