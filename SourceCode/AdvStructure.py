# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 23:42:29 2020

@author: Seong-sik Heo
"""

#import sys
#sys.setrecursionlimit(5000)
from CommonVariables import DeepCopyObj

class node_T():
    def __init__(self):
        self.Obj = None
        self.Obj_idx = -1
        self.Obj2 = None
        self.Obj2_idx = -1
        self.pre = None
        self.next = None
        self.Start_time = -1
        self.End_time = -1
        self.PID = ''
        self.operation = -1

#     def __init__(self, Obj0):
#         self.Obj = Obj0
#         self.pre = None
#         self.next = None
    def __str__(self):
        return str(self.Obj)
    def get_obj(self, Obj0):#예를 들어, node_T.get_obj(Cell())
        self.Obj = Obj0
    def print_O(self):
        print(self.Obj)
        #self.Obj.print0()
    """
    def prt_id(self):
        self.Obj.prt_id()
    """

class LList_T():
    def __init__(self):
        self.head = node_T()
        self.tail = node_T()
        self.nNodes = 0
        self.head.next = self.tail
        self.head.pre = self.tail
        self.tail.next = self.head
        self.tail.pre = self.head
    def __str__(self):
        prtTmp = ''
        posit = self.head
        while (posit.next != self.tail):
            posit = posit.next
            prtTmp += str(posit)
        #while
        return prtTmp
    def push_back(self, Obj0):
        Tmp_node = node_T()
        
        self.tail.pre.next = Tmp_node
        Tmp_node.next = self.tail
        Tmp_node.pre = self.tail.pre
        self.tail.pre = Tmp_node
        
        Tmp_node.get_obj(Obj0)
        self.nNodes += 1
        return self.nNodes
    def pop_back(self):
        if self.nNodes == 0:
            print('No elements in List_T')
            Tmp_Obj = None
        else:
            Tmp_node = self.tail.pre
            Tmp_Obj = Tmp_node.Obj #self.tail.pre.Obj
            #self.tail.pre.pre.next = self.tail
            #self.tail.pre = self.tail.pre.pre
            Tmp_node.pre.next = self.tail
            self.tail.pre = Tmp_node.pre
            del Tmp_node
        return Tmp_Obj
    def pop_it(self, node0):
        node0.next.pre = node0.pre
        node0.pre.next = node0.next
        self.nNodes -= 1
        Tmp_Obj = node0.Obj
        del node0
        return Tmp_Obj
    def del_it(self, node0):
        node0.next.pre = node0.pre
        node0.pre.next = node0.next
        self.nNodes -= 1
        NextNode = node0.next
        return NextNode
    def copy(self, List0):
        posit = self.head
        while (posit.next != self.tail):
            posit = posit.next
            List0.push_back(DeepCopyObj(posit.Obj))
        #while
    def clear(self):
        Tmp_node = None
        while (self.nNodes != 0):
            Tmp_node = self.head.next
            self.pop_it(Tmp_node)
        #while
    def begin(self):
        return self.head.next
    def end(self):
        return self.tail.pre
    def print_L(self):
        posit = self.head
        while (posit.next != self.tail):
            posit = posit.next
            posit.print_O()
    """
    def prt_id(self):
        #self.Obj.prt_id()
        posit = self.head
        while (posit.next != self.tail):
            posit = posit.next
            posit.prt_id()
    """
class Job_Index0():
    def __init__(self):
        self.i_Job_index = 0 
        self.i_Machine_pro = [] #프로세싱 타임들 받아서 다음 machine 결정할때 이전꺼의 processing time도 고려한다
        self.i_Last_processing_time = 0 #시뮬레이션에서 타임 마지막에다가 마지막 processing time을 더해준다 makespan을위해
        self.i_Total_movement = 0
        self.i_temp = 0
        self.machine_name = [] #프로세싱 타임들 받아서 다음 machine 결정할때 이전꺼의 machine 고려한다
        

class Machine_T():
    def __init__(self):
        self.i_Current_State = 0 #0 이면, machine 가능 / 1이면, machine 불가
        self.i_Current_Job_No = 0
        self.i_Current_Part_ID = 0
        self.i_Current_Part_No = 0
        self.i_Current_Job_Start_Time = 0
        self.i_Current_Job_End_Time = 0
        self.i_Total_Working_Time = 0
        self.i_End_time = 0
        #계속해서 End 업데이트해서 들고있는다. Dispacting 할때 end time과 현재 time이 같을때 동일한 machine에서 process되는지 체크하기 위함이다.
        self.i_release_time = 0 #필요없음
        self.i_idle_time = 0 #필요없음
        self.i_Machine_State = 0 #Auto(1) or Manual(0) machine, 나랑 관계없음
        self.i_Machine_Schedule = [] #0
        self.i_Working_or_Rest = 0 #1이면 가능, 0이면 불가
        self.i_Next_Working_time = 0
        self.i_Next_Rest_Time = 0
        self.i_Number_Schedule = 0
        self.i_Current_Schedule = 0
        self.i_Machine_No = 0
        self.s_Machine_Name = ''
        self.Job_Sequence = None
        self.Machine_Queue = None #필요없다.
    """
    def prt_id(self):
        print("Machine_T:", self.i_Machine_No, "-", self.i_Current_Job_No)
    """
    
class Fixture_T():
    def __init__(self):
        self.i_number_Fixture = 0 #Fixture는 무한대
        self.i_rest_Fixture = 0 #사용중이면 1 아니면 0
        self.i_fixture_no = 0 #Pallet에 올라간 fixture의 넘버
        
class Pallet_T():
    def __init__(self):
        self.i_Pallet_index = 0
        self.i_Num_Fixt = 0 #Pallet의 fixture 갯수
        self.i_number_Pallet = 0 #1로 둔다
        self.i_rest_Pallet = 0 #1 또는 들어가면 0으로 바뀌고
        self.Fixture = None #Fixture_T()
        
class Part_Type_T():
    def __init__(self):
        self.i_demand = 0
        self.i_Job_ID = 0
        self.i_Due_Date = 0
        self.i_Fixture_Type = 0
        self.i_Pre_part = 0
        self.i_part_due = 0
        self.i_release_time = 0
        self.i_Num_Operation = 0
        self.i_Num_Alternative_Machine = []
        self.i_Standard_Time = []
        self.s_PID = 0
        self.s_Alternative_Machine_Name = []
        self.Alternative_Mac = None
        
class Part_T():
    def __init__(self):
        self.i_Total_Processing_Time = 0 #선택된 machine의 총 가공시간
        self.i_All_processing_time = 0 #모든 대안들의 가공시간을 더한것
        self.i_Current_Process_Completion_time = 0
        self.i_Current_Process_Standard_Time = 0
        self.i_completion_time = 0
        self.i_release_time = 0
        self.i_multiplier = 0
        self.i_Part_No = 0 #몇 번 part인지 index
        self.i_Job_No = 0 #어떤 job에 속한 것인지
        self.i_Due_date = 0 #part별로 due date 있다
        self.i_Terminated = 0
        self.i_Pallet_type = 0
        self.i_Fixture_type = 0
        self.i_Current_Process_No = 0
        self.i_Current_Alt_Mac_index = 0
        self.f_ATWK = ''
        self.i_Mac_Select_index = [] #machine selection 된 후 machine index list
        self.i_Select_Process_Time = [] #machine selection 된 후 processing time        
        self.s_Mac_Select_name = []
        self.s_Current_Process = ''
        self.s_Current_Machine = ''
        self.PT = None #Part_Type_T()
        self.Machine_Sequence = None #Mac_list()
        self.Mac_Temp = None #Machine_T()
        self.Mac_Select = None #machine selection 된 후 machine list
        self.i_Part_index = 0
    """
    def prt_id(self):
        print("Part_T:", self.i_Job_No, "-", self.i_Part_No)
    """    


class Job_T():
    def __init__(self):
        self.i_Total_Number_Operation = 0
        self.i_Num_parts = 0 #몇개의 part가 올라갔는지
        self.Dependent_part = 0 #dependent part의 첫번째 part가 하나라도 올라가 있으면 1 아니면 0
        self.i_OP_Route = []
        #올라온 part들의 Operation number를 가지고 있는다. Route 결정할때 필요!
        self.i_Processing_time = []
        self.i_Total_movement = 0 #machie route의 총 movement
        self.i_current_position = 0 #이걸로 route들 하나씩 이동!
        self.i_current_state = 0 #프로세스 중인지 아닌지, 1이면 프로세스중, 0이면 buffer에 있음
        self.i_Machine_Route_index = 0
        self.i_Current_Process_Completion_time = 0
        self.i_Current_Process_Standard_Time = 0
        self.i_Terminate = 0
        self.i_Job_No = 0
        self.i_Empty = 1 #pallet에 part들이 올라가는것이 없으면, 1
        self.i_Completion_time = 0
        self.i_Release_time = 0
        self.i_TWKR = 0
        self.f_avg_duedate = 0 #올라간 part들의 평균 due-date
        self.s_Machine_Name = []
        self.P = None #Part_T()
        self.Machine_Sequence = None #LList_T()#Mac_list()
        self.Machine_Route = [] #Machine_T()
        #이게 어디서 할당되는건지 꼭 확인! 올라온 part들의 operation에 해당하는 machine
        self.Part_Route = [] #Part_T()
        #올라온 part들의 operation이 어떤 part인지
        self.Pallet_job = None #Pallet_T()
        #어떤 pallet인지
        
        #Machine_Route, Part_Route, i_OP_Route, s_Machine_Name, i_Total_movement
        #해당 다섯 가지가 하나로 같이 묶인다. 그 position에 그 part-operation-machine이다.