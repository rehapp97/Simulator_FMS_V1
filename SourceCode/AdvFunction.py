from AdvStructure import *
from AdvConfig import Config_T as con
import time
import sys

def Machine_Selection_SPT(P):
    min0 = 9999999
    
    temp_Mac = None #Machine_T()
    Ret_Mac = None #Machine_T()

    P.i_Total_Processing_Time = 0
    #print(P.PT)
    for i in range(P.PT.i_Num_Operation):
        Ret_Mac = None
        min0 = 999999
        if (P.PT.i_Num_Alternative_Machine == 0): #첫번째 작업과 마지막 작업은 대안 machine 없다.
            P.Mac_Select[i] = None            
            P.s_Mac_Select_name[i] = None     
            P.i_Mac_Select_index[i] = None    
            P.i_Select_Process_Time[i] = None
            #Ret_Mac = None
        else:
            for j in range(P.PT.i_Num_Alternative_Machine[i]):
                #print(P.PT.Alternative_Mac[i][j])
                temp_Mac = P.PT.Alternative_Mac[i][j]
                temp = P.PT.i_Standard_Time[i][j]
                #print(temp)
                #print(min0)
                if (min0 > temp):
                    temp_i = i #해당 part의 operaiton number
                    temp_j = j #해당 operation의 alternative machine number
                    min0 = temp
                    Ret_Mac = temp_Mac
            if (Ret_Mac != None):
                P.Mac_Select[i] = P.PT.Alternative_Mac[temp_i][temp_j] # Alternative machine들 중에 선택된 machine 할당
                P.s_Mac_Select_name[i] = P.PT.s_Alternative_Machine_Name[temp_i][temp_j] # Alternative machine들 중에 선택된 machine name 할당
                P.i_Mac_Select_index[i] = temp_j # Alternative machine들 중에 선택된 Machie number(index) 할당
                P.i_Select_Process_Time[i] = P.PT.i_Standard_Time[temp_i][temp_j] # Alternative machine들 중에 선택된 processing time 할당

        P.i_Total_Processing_Time += P.i_Select_Process_Time[i]
    return Ret_Mac

def Total_Proc_time_in_Buffer(Q, T):
    proc = 0
    temp = Q.head.next

    while (temp != Q.tail):
        for i in range(temp.Obj.i_Total_Number_Operation):
            if (temp.Obj.Machine_Route[i] == T):      #########배열이 어디서 할당되는건지 나중에 꼭 확인!
                proc += temp.Obj.i_Processing_time[i] #########배열이 어디서 할당되는건지 나중에 꼭 확인!

        temp = temp.next

    return proc 


def Machine_Selection_MNPB(con, P, Job_list): # Minimum Workload (MW)
    min1 = 9999999
    a = 0    
    P.i_Total_Processing_Time = 0

    temp2 = con.ML.head 
    temp_Mac = None      
    temp_previous = None # 이전에 선택된 machine은 그만큼 prosseing time 더해져야 된다.
    Ret_Mac = None        

    for i in range(P.PT.i_Num_Operation):
        P.Mac_Select[i] = None
        P.s_Mac_Select_name[i] = ''
        min1 = 999999
        #####################(위)min을 여기서 다시 설정하는 이유#####################
        temp = 0

        if (P.PT.i_Num_Alternative_Machine[i] == 0): #첫번째 작업과 마지막 작업은 대안 machine 없다.
            P.Mac_Select[i] = None
            P.s_Mac_Select_name[i] = None
            P.i_Mac_Select_index[i] = None
            P.i_Select_Process_Time[i] = None
        else:
            for j in range(P.PT.i_Num_Alternative_Machine[i]):
                temp_Mac = P.PT.Alternative_Mac[i][j]
                temp = Total_Proc_time_in_Buffer(Job_list, temp_Mac) # Job_list가 central buffer 안에 있는 job list를 말한다. 해당 operation의 alternative machine 중에서 한 machine이 들어간다.
                for k in range(con.i_Num_Machines):
                    if (temp_Mac == con.Job_INDEX.machine_name[k]):
                        temp = temp + con.Job_INDEX.i_Machine_pro[k]
                if (min1 > temp):
                    temp_i = i
                    temp_j = j
                    min1 = temp
                    Ret_Mac = temp_Mac
            if (Ret_Mac != None):
                P.Mac_Select[i] = P.PT.Alternative_Mac[temp_i][temp_j] #Machine_T로 받고
                P.s_Mac_Select_name[i] = P.PT.s_Alternative_Machine_Name[temp_i][temp_j]
                P.i_Mac_Select_index[i] = temp_j #Machie number(index)로 받고
                P.i_Select_Process_Time[i] = P.PT.i_Standard_Time[temp_i][temp_j] #그때의 processing time 받기

                temp_previous = Ret_Mac #선택된 machine을 받아서 다음 결정때 검사한다.
                a = P.i_Select_Process_Time[i] #선택된 prosessing time 받아서 다음 결정때 더해준다.

                b = 0
                temp2 = con.ML.head.next
                while (temp2 != con.ML.tail):
                    if (temp_previous == temp2.Obj):
                        con.Job_INDEX.i_Machine_pro[b] += a
                        con.Job_INDEX.machine_name[b] = temp_previous

                    b += 1
                    temp2 = temp2.next
            #######################한 칸 땡기면 P.i_Select_Process_Time[i]으로 None을 받아서 오류뜬다.
            P.i_Total_Processing_Time += P.i_Select_Process_Time[i] #총 processig time 받기
    #print(Ret_Mac)
    return Ret_Mac


def Job_Define_SPPT(con, Pallet_type, Job_list): #Pallet이 한 개 들어오고, 해당 pallet에 
    i = 0
    total_duedate = 0
    o = 0 #fixture에 걸리는 part 확인하기 위함이다.

    Temp_Job = Job_T()
    Temp_Job.i_Total_Number_Operation = 0
    temp_Mac = None

    con.Job_INDEX.machine_name = [] # Machine selection 할때 name list 받기
    con.Job_INDEX.i_Machine_pro = [] # Machine selection 할때 이전 machine들에 대한 processing time 받기
    
    for j in range(con.i_Num_Machines):
        con.Job_INDEX.i_Machine_pro.append(0) #초기화
        con.Job_INDEX.machine_name.append(Machine_T()) #초기화

    Temp_Job.P = []
    for j in range(Pallet_type.i_Num_Fixt):
        min = 99999
        Temp_Job.P.append(Part_T()) # 본 함수에 들어온 pallet에 Part_T()형을 i_Num_Fixt만큼 넣는다.
        test = None
        
        temp = con.Dummy.head.next
        while temp != con.Dummy.tail:
            if temp.Obj.i_Terminated == 0 and temp.Obj.i_Fixture_type == Pallet_type.Fixture[j].i_fixture_no and Pallet_type.Fixture[j].i_rest_Fixture  == 1 and min > temp.Obj.i_All_processing_time:
                test = temp # test에는 i_All_processing_time이 가장 작은 part를 할당한다.
                min = temp.Obj.i_All_processing_time
                o += 1
            temp = temp.next
        if test == None:
            Temp_Job.P[j] = None
            
        else:
            Temp_Job.P[j] = test.Obj
            i += 1
            #print(test.Obj.PT.i_Num_Operation)
            Temp_Job.i_Total_Number_Operation += test.Obj.PT.i_Num_Operation #들어오는 part들의 operation 개수 합치기
            Temp_Job.i_Num_parts = i #몇 개의 part 가 올라갔는지
            Temp_Job.Pallet_job = Pallet_type #Job에 어떤 팔렛이 대응되는지
            Temp_Job.i_Empty = 0 #pallet에 part가 올라가면 0
            total_duedate += test.Obj.i_Due_date
            Temp_Job.f_avg_duedate = total_duedate
            
            if (con.Machine_Selection_Option == 1): #opreation 마다 machine 선택
                temp_Mac = Machine_Selection_SPT(test.Obj)
                
            elif (con.Machine_Selection_Option == 2):
                if (Job_list.nNodes == 0): #buffer에 아무것도 없을때는 SPT로 들어간다
                    temp_Mac = Machine_Selection_SPT(test.Obj)
                else: #buffer에 job이 있으면 machine의 총 processing time들을 계산
                    temp_Mac = Machine_Selection_MNPB(con, test.Obj, Job_list)

            #test.next.pre = test.pre
            #test.pre.next = test.next #선택된 part는 queue에서 사라진다
            #del test
            #con.Dummy.nNodes -= 1
            con.Dummy.pop_it(test)

            Pallet_type.Fixture[j].i_rest_Fixture = 0 #그때 fixture는 사용됨
    l = 0
    #print(Temp_Job)
    return Temp_Job


def Job_Define_EDD(con, Pallet_type, Job_list):
    i = 0
    total_duedate = 0
    min = 999999
    o = 0

    temp_Mac = None #Machine_T()
    Temp_Job = Job_T()
    con.Job_INDEX.machine_name = [] #machine selection 할때 name list 받기
    con.Job_INDEX.i_Machine_pro = [] ##machine selection 할때 이전 machine들에 대한 processing time 받기
    Temp_Job.P = []

    Temp_Job.i_Total_Number_Operation = 0

    temp = None #Cell()
    test = None #Cell()

    for j in range(con.i_Num_Machines):
        con.Job_INDEX.machine_name.append(Machine_T()) #초기화, con.Job_INDEX.machine_name = [Machine_T(), Machine_T(), ..., Machine_T()]
        con.Job_INDEX.i_Machine_pro.append(0) #초기화, con.Job_INDEX.i_Machine_pro = [0, 0, ..., 0]
   
    for j in range(Pallet_type.i_Num_Fixt): #2 or 4
        Temp_Job.P.append(Part_T()) #Temp_Job.P = [Part_T(), Part_T()] or [Part_T(), Part_T(), Part_T(), Part_T()]
        test = None #Cell()
        temp = con.Dummy.head.next
        min = 99999

        while (temp != con.Dummy.tail):
            if (temp.Obj.i_Terminated == 0) and (temp.Obj.i_Fixture_type == Pallet_type.Fixture[j].i_fixture_no) and (Pallet_type.Fixture[j].i_rest_Fixture  == 1) and (min > temp.Obj.i_Due_date):
                test = temp #어떤 part가 들어왔는지
                min = temp.Obj.i_Due_date
                o += 1 #확인 용도
            temp = temp.next

        if test == None:
            Temp_Job.P[j] = None

        else: #test != None
            Temp_Job.P[j] = test.Obj
            i += 1
            Temp_Job.i_Total_Number_Operation += test.Obj.PT.i_Num_Operation #들어오는 part들의 operation 개수 합치기
            Temp_Job.i_Num_parts = i
            Temp_Job.Pallet_job = Pallet_type #Job에 어떤 팔렛이 대응되는지
            Temp_Job.i_Empty = 0 #pallet에 part가 올라가면 0
            total_duedate += test.Obj.i_Due_date
            Temp_Job.f_avg_duedate = total_duedate

            if (con.Machine_Selection_Option == 1): #opreation 마다 machine 선택
                temp_Mac = Machine_Selection_SPT(test.Obj)

            elif (con.Machine_Selection_Option == 2):
                if (Job_list.nNodes == 0): #Buffer에 아무것도 없을 때에는 SPT로 들어간다
                    temp_Mac = Machine_Selection_SPT(test.Obj)
                    
                else: #buffer에 job이 있으면 machine의 총 processing time들을 계산
                    temp_Mac = Machine_Selection_MNPB(con, test.Obj, Job_list)
            #test.next.pre = test.pre
            #test.pre.next = test.next #선택된 part는 queue에서 사라진다
            #del test
            #con.Dummy.nNodes -= 1
            con.Dummy.pop_it(test)

            Pallet_type.Fixture[j].i_rest_Fixture = 0 #그때 fixture는 사용됨

    #print(Temp_Job)
    return Temp_Job


def movement_cal(current_part, current_part_op, temp_op_index, J, part_position_index):
    total_machine_movement = 0
    v = 0
    r = 0
    min = 999

    machine_movement = [0 for i in range(J.i_Num_parts)]
    
    for i in range(1, J.i_Total_Number_Operation):
        #i=1부터이다. 0에는 처음 선택된 값들이 들어가있다. 첫 번째에는 movement가 필요가 없기 때문이다. Total_Number_operation+1 에는 NULL값들이 들어가있다.
        for j in range(J.i_Num_parts): # Pallet에 올라가 있는 part의 수(2 or 4)
            if (temp_op_index[j] != -1):
                if (temp_op_index[j] < J.P[part_position_index[j]].PT.i_Num_Operation - 1):
                    # (위)J.P[part_position_index[j]].PT.i_Num_Operation에는 operation 수 보다 2개가 더 할당되어있기 때문에 진또배기 operation 숫자에 이를때까지만 movement를 계산하는 것이다.
                    if (j == r): #처음에 current part의 position은 0이다. 한번 iteration 후 r의 값은 바뀜 current part의 position 변화 알기 위해 r에 저장
                        if (current_part.Mac_Select[current_part_op + 1] != None):
                            if (current_part.Mac_Select[current_part_op] != current_part.Mac_Select[current_part_op + 1]):
                                v = 1
                                machine_movement[j] = v
                            else: #현재의 part의 operation의 다음 operation이 같은 machine일 경우, movement = 0
                                v = 0
                                machine_movement[j] = v
                        else:
                            temp_op_index[j] = -1 # 해당 pallet에 fixturing된 part의 operation에 대해 machine 할당이 없을 때이다. 즉, machine 할당도 없다.
                            machine_movement[j] = 99
                    else:
                        if (current_part.Mac_Select[current_part_op] != J.P[part_position_index[j]].Mac_Select[temp_op_index[j] + 1]):
                            v = 1
                            machine_movement[j] = v
                        else:
                            v = 0
                            machine_movement[j] = v
                else: # 해당 pallet에 있는 해당 part에 대해서 operation의 할당이 끝났다.
                    temp_op_index[j] = -1
                    machine_movement[j] = 99 # Operation 할당이 다 된 것을 의미한다.
        min = 999
        for k in range(J.i_Num_parts): #최소 movement를 찾는다
            if (machine_movement[k] <= min):
                min = machine_movement[k]
                r = k # Current part의 position이 바뀐다.

        if (machine_movement[r] == 1):
            total_machine_movement += 1
        current_part = J.P[part_position_index[r]] # current_part가 변한다.
        temp_op_index[r] += 1
        current_part_op = temp_op_index[r]
        """
        최소 movement를 찾아서 출력
        for j in range(J.i_Num_parts):
            print('temp part op의 값:', '', temp_op_index[r])
        """
        J.Machine_Route[i] = current_part.Mac_Select[current_part_op]
        J.i_OP_Route[i] = current_part_op
        J.Part_Route[i] = current_part
        J.s_Machine_Name[i] = current_part.s_Mac_Select_name[current_part_op]
        J.i_Processing_time[i] = current_part.i_Select_Process_Time[current_part_op]
        J.i_Total_movement = total_machine_movement
        
    l = 0

    return machine_movement


def Job_route(J): # Part들이 fixturing된 각 pallet(job)의 route를 결정.
    current_part = None # Part_T()
    # int *part_position_index; #Job의 P에는 NULL로 된 part공간이 있다. 따라서 들어있는 P의 postion index가 필요
    machine_movement = [0 for i in range(J.i_Num_parts)] #J의P에 NULL값들을 빼고 메모리공간 만든다
    part_position_index = [0 for i in range(J.i_Num_parts)]
    temp_op_index = [0 for i in range(J.i_Num_parts)] # index는 0 이다.

    J.i_OP_Route = [0 for i in range(J.i_Total_Number_Operation)] #operation route, +1 하는 이유는 첫 번째 operation 표현 용이. 맨 마지막 operation에는 None.
    J.Part_Route = [Part_T() for i in range(J.i_Total_Number_Operation)] #part route
    J.Machine_Route = [Machine_T() for i in range(J.i_Total_Number_Operation)] #machine route
    J.s_Machine_Name = ['' for i in range(J.i_Total_Number_Operation)]
    J.i_Processing_time = [0 for i in range(J.i_Total_Number_Operation)]

    for k in range(J.Pallet_job.i_Num_Fixt):
        if (J.P[k] != None):
            part_number = k
            break

    j = 0
    k = 0
    if (J.P[k] != None):
        part_position_index[j] = k
        k += 1
        for j in range(1, J.i_Num_parts):
            while (k != J.Pallet_job.i_Num_Fixt):
                if (J.P[k] != None):
                    part_position_index[j] = k
                    k += 1
                    break
                else:
                    k += 1
    else:
        k += 1
        for j in range(J.i_Num_parts):
            while (k != J.Pallet_job.i_Num_Fixt):
                if (J.P[k] != None):
                    part_position_index[j] = k
                    k += 1
                    break
                else:
                    k += 1

    J.i_OP_Route[0] = J.P[part_number].i_Current_Process_No + 1 #rand으로 받았을때의 값
    J.Part_Route[0] = J.P[part_number]
    J.Machine_Route[0] = J.P[part_number].Mac_Select[1] #rand으로 하나 받아온다, 랜덤하게 번호생성 후 하나의 part의 첫번째 operation으로 들어간다.
    J.s_Machine_Name[0] = J.P[part_number].s_Mac_Select_name[1] #첫번째 operation이기 때문에
    J.i_Processing_time[0] = J.P[part_number].i_Select_Process_Time[1]
    J.i_Total_movement = 0

    temp_op_index[0] += 1 #첫번째 배열에 들어간 part의 operation 번호
    current_part = J.P[part_number] #현재 part
    current_part_op = J.P[part_number].i_Current_Process_No + 1 #현재 part의 operation 번호
    
    J.i_OP_Route.append(None)        #J.i_OP_Route[J.i_Total_Number_Operation + 1] #마지막값은 0
    J.Part_Route.append(None)        #J.Part_Route[J.i_Total_Number_Operation + 1] #맨마지막은 아무값도 없다
    J.Machine_Route.append(None)     #J.Machine_Route[J.i_Total_Number_Operation + 1] #맨마지막은 아무값도 없다
    J.s_Machine_Name.append(None)    #J.s_Machine_Name[J.i_Total_Number_Operation + 1]
    J.i_Processing_time.append(None) #J.i_Processing_time[J.i_Total_Number_Operation + 1]

    machine_movement = movement_cal(current_part, current_part_op, temp_op_index, J, part_position_index) #movement 계산
    l = 0
    J.i_TWKR = TWKR2(J) # 해당 pallet에 fixturing된 모든 part들의 모든 operation processing time을 합한다.


def movement_cal_HU(temp_route, part_position_index, J, total_num_operation, temp_op_index2, Job_INDEX):
    v = 0
    #print('part의 수: ', J.i_Num_parts)
    for i in range(J.i_Num_parts):
        temp_op_index2[i] = 0
    
    #print('total_num_operation: ', total_num_operation)
    for i in range(total_num_operation - 1):
        #print('total_num_operation: ', total_num_operation)
        #print('temp_route: ', temp_route)
        #print('temp_route[i+1]: ', temp_route[i+1])
        #print('Mac_Select: ', J.P[part_position_index[temp_route[i+1]-1]].Mac_Select)
        #print(temp_op_index2)
        #print('Index: ', temp_op_index2[temp_route[i+1]-1]+1)
        if (J.P[part_position_index[temp_route[i+1]-1]].Mac_Select[temp_op_index2[temp_route[i+1]-1]+1] != None):
            if (J.P[part_position_index[temp_route[i]-1]] == J.P[part_position_index[temp_route[i+1]-1]]):
                #print(J.P[part_position_index[temp_route[i+1]-1]].Mac_Select)
                #print(temp_op_index2[temp_route[i+1]-1]+2)
                if (J.P[part_position_index[temp_route[i]-1]].Mac_Select[temp_op_index2[temp_route[i]-1]+1] == J.P[part_position_index[temp_route[i+1]-1]].Mac_Select[temp_op_index2[temp_route[i+1]-1]+2]):
                    v = v
                else:
                    v += 1
            else:
                if (J.P[part_position_index[temp_route[i]-1]].Mac_Select[temp_op_index2[temp_route[i]-1]+1] == J.P[part_position_index[temp_route[i+1]-1]].Mac_Select[temp_op_index2[temp_route[i+1]-1]+1]):
                    v = v
                else:
                    v += 1

        else:
            v = v
        
        temp_op_index2[temp_route[i]-1] += 1
        #print(temp_op_index2[temp_route[i]-1])
    
    machine_movement = v
    return machine_movement

def TWKR2(J):
    sum = 0
    for i in range(J.i_Total_Number_Operation):
        sum += J.i_Processing_time[i]

    return sum


def Job_route_HU(J, Job_INDEX):
    r = 0
    total_machine_movement = 0
    v = 0
    j = 0
    k = 0
    min = 999

    total_num_operation = J.i_Total_Number_Operation #총 operation개수
    Num_part_on_pallet = J.i_Num_parts #몇개의 part가 올라와있는지

    current_part = None
    machine_movement = [0 for i in range(J.i_Num_parts)] #J의P에 NULL값들을 빼고 메모리공간 만든다 
    #[0 for i in range(J.i_Num_parts)]
    part_position_index = [0 for i in range(J.i_Num_parts)] #Job의 P에는 NULL로 된 part공간이 있다. 따라서 들어있는 P의 postion index가 필요
    #[0 for i in range(J.i_Num_parts)]
    part_position_index2 = [0 for i in range(J.i_Num_parts)] #쓰지 않는다.
    #[0 for i in range(J.i_Num_parts)]
    temp_op_index = [0 for i in range(J.i_Num_parts)]
    temp_op_index2 = [0 for i in range(Num_part_on_pallet)] #part들의 operation index, part들의 현재 operation index
    #print(temp_op_index2)
    """
    for k in range(Num_part_on_pallet):
        temp_op_index[k] = 0 
        temp_op_index2[k] = 0 #index는 0이다
    """

    temp = [] #임시 operation 순서
    temp2 = []
    Job_route = [] #job route = final job route 순서

    for j in range(total_num_operation):
        Job_route.append(1)
        temp.append(0)
        temp2.append(0)

    for k in range(J.Pallet_job.i_Num_Fixt):
        if (J.P[k] != None):
            part_number = k
            break

    J.i_OP_Route = [0 for i in range(J.i_Total_Number_Operation + 1)] #operation route
    J.Part_Route = [] #part route
    J.Machine_Route = [] #machine route
    J.s_Machine_Name = []
    J.i_Processing_time = [0 for i in range(J.i_Total_Number_Operation + 1)]

    for k in range(J.i_Total_Number_Operation + 1):
        J.Part_Route.append(Part_T())
        J.Machine_Route.append(Machine_T())
        J.s_Machine_Name.append('')

    J.i_OP_Route[0] = J.P[part_number].i_Current_Process_No + 1 #rand으로 받았을때의 값
    J.Part_Route[0] = J.P[part_number]
    J.Machine_Route[0] = J.P[part_number].Mac_Select[1] #rand으로 하나 받아온다 //랜덤하게 번호생성 후 하나의 part의 첫번째 operation으로 들어간다
    J.s_Machine_Name[0] = J.P[part_number].s_Mac_Select_name[1] #첫번째 operation이기 때문에 
    J.i_Processing_time[0] = J.P[part_number].i_Select_Process_Time[1]
    J.i_Total_movement = 0

    temp_op_index[0] += 1 #첫번째 배열에 들어간 part의 operation 번호
    current_part = J.P[part_number] #현재 part
    current_part_op = J.P[part_number].i_Current_Process_No + 1 #현재 part의 operation 번호

    J.i_OP_Route.append(None) #[J.i_Total_Number_Operation + 1] = None
    J.Part_Route.append(None) #[J.i_Total_Number_Operation + 1] = None
    J.Machine_Route.append(None) #[J.i_Total_Number_Operation + 1] = None
    J.s_Machine_Name.append(None) #[J.i_Total_Number_Operation + 1] = None
    J.i_Processing_time.append(None) #[J.i_Total_Number_Operation + 1] = None

    j = 0
    k = 0

    if (J.P[k] != None):
        part_position_index[j] = k
        k += 1
        for j in range(1, J.i_Num_parts):
            while (k != J.Pallet_job.i_Num_Fixt):
                if (J.P[k] != None):
                    part_position_index[j] = k
                    k += 1
                    break
                else:
                    k += 1
    else:
        k += 1
        for j in range(J.i_Num_parts):
            while(k != J.Pallet_job.i_Num_Fixt):
                if (J.P[k] != None):
                    part_position_index[j] = k
                    k += 1
                    break
                else:
                    k += 1

    for a in range(1, total_num_operation): #route 알고리즘 결정 여기서 a는 현재 operation 길이 사이즈이다.
        Job_INDEX.i_Total_movement = 99 #movement 다시 초기화
        for i in range(J.i_Num_parts):
            if (temp_op_index[i] != -1):
                if (temp_op_index[i] < J.P[part_position_index[i]].PT.i_Num_Operation - 1): #J의 P의 operation 숫자보다 작을때만!
                    if (i == r): #처음에 current part의 position은 0이다. 한번 iteration 후 r의 값은 바뀐다. current part의 position 변화 알기 위해 r에 저장.
                        if (current_part.Mac_Select[current_part_op + 1] != None):
                            if (current_part.Mac_Select[current_part_op] != current_part.Mac_Select[current_part_op+1]):
                                v = 1
                                machine_movement[i] = v

                            else:
                                v = 0
                                machine_movement[i] = v
                        else:
                            temp_op_index[i] = -1
                            machine_movement[i] = 99
                    else:
                        #print(current_part.Mac_Select)
                        #print(current_part.Mac_Select[current_part_op])
                        if (current_part.Mac_Select[current_part_op] != J.P[part_position_index[i]].Mac_Select[temp_op_index[i]+1]):
                            v = 1
                            machine_movement[i] = v
                        else:
                            v = 0
                            machine_movement[i] = v
                else:
                    temp_op_index[i] = -1
                    machine_movement[i] = 99 #operation 할당 다 된것을 의미

        min = 999
        for k in range(J.i_Num_parts): #최소 movement찾는다
            if (machine_movement[k] <= min):
                min = machine_movement[k]
                r = k #current part의 position이 바뀐다
    
        if (machine_movement[r] == 1):
            total_machine_movement += 1
    
        current_part = J.P[part_position_index[r]]
        temp_op_index[r] += 1
        current_part_op = temp_op_index[r]
        ############여기 for문 2개는 추가되는 operation을 하나씩 사이에 넣어보면서 route들 생성하고 그때 route들의 machine movement를 계산한 후 업데이트!    
        #print(a+1)
        for p in range(a+1): #operation 1개 추가 되면서 operation 길이 사이즈가 한개 늘어남
            index = 0
            for s in range(a): #하나씩 다 넣어본다
                if (p == s):
                    temp[p] = r + 1
                    index += 1

                    temp[p + 1] = Job_route[s]
                    index += 1

                else:
                    temp[index] = Job_route[s]
                    index += 1

                    if (p == a):
                        temp[a] = r + 1

                #part_position_index[r]을 새로운 operation으로 추가한다 
                #temp를 결정하면 됨. 계속 바껴야됨 체크!

            Job_INDEX.i_temp = movement_cal_HU(temp, part_position_index, J, a+1, temp_op_index2, Job_INDEX) #생성된 route의 movement 계산

            if (Job_INDEX.i_temp < Job_INDEX.i_Total_movement): # movement 더 작은 route면 Job_route로 업데이트
                Job_INDEX.i_Total_movement = Job_INDEX.i_temp
                for k in range(total_num_operation):
                    temp2[k] = temp[k]

        for k in range(total_num_operation):
            Job_route[k] = temp2[k]

    for j in range(Num_part_on_pallet):
        temp_op_index2[j] = 0

    for j in range(total_num_operation): #가장 좋은 job route를 J에 업데이트
        J.i_OP_Route[j] = (temp_op_index2[Job_route[j]-1]) + 1
        J.Part_Route[j] = J.P[part_position_index[Job_route[j]-1]]
        J.Machine_Route[j] = J.P[part_position_index[Job_route[j]-1]].Mac_Select[temp_op_index2[Job_route[j]-1]+1]
        J.s_Machine_Name[j] = J.P[part_position_index[Job_route[j]-1]].s_Mac_Select_name[temp_op_index2[Job_route[j]-1]+1]
        J.i_Processing_time[j] = J.P[part_position_index[Job_route[j]-1]].i_Select_Process_Time[temp_op_index2[Job_route[j]-1]+1]
        
        temp_op_index2[Job_route[j]-1] += 1


    J.i_TWKR = TWKR2(J)
    J.i_Total_movement = Job_INDEX.i_Total_movement


def movement_cal_recursive(temp_route, part_position_index, J, total_num_operation, temp_op_index2, Job_INDEX):
    v = 0

    for i in range(J.i_Num_parts):
        temp_op_index2[i] = 0
    #print(total_num_operation)

    for i in range(total_num_operation-1):
        if (J.P[part_position_index[temp_route[i+1]-1]].Mac_Select[temp_op_index2[temp_route[i+1]-1]+1] != None):
            if (J.P[part_position_index[temp_route[i]-1]] == J.P[part_position_index[temp_route[i+1]-1]]):
                if (J.P[part_position_index[temp_route[i]-1]].Mac_Select[temp_op_index2[temp_route[i]-1]+1] == J.P[part_position_index[temp_route[i+1]-1]].Mac_Select[temp_op_index2[temp_route[i+1]-1]+2]):
                    v = v
                else:
                    v += 1
            else:
                if (J.P[part_position_index[temp_route[i]-1]].Mac_Select[temp_op_index2[temp_route[i]-1]+1] == J.P[part_position_index[temp_route[i+1]-1]].Mac_Select[temp_op_index2[temp_route[i+1]-1]+1]):
                    v = v
                else:
                    v += 1
        else:
            v = v

        temp_op_index2[temp_route[i]-1] += 1

    machine_movement = v
    return machine_movement


def recursive(step, mat, num, Job_route, total_num_operation, Num_part_on_pallet, part_position_index, J, temp_op_index2, Job_INDEX):
    temp = None
    for i in range(Num_part_on_pallet):
        if (num[i] > 0):
            num[i] -= 1
            mat[step] = i+1
            
            if (step == total_num_operation-1):
                Job_INDEX.i_temp = movement_cal_recursive(mat, part_position_index, J, total_num_operation, temp_op_index2, Job_INDEX)
                if (Job_INDEX.i_temp < Job_INDEX.i_Total_movement):
                    Job_INDEX.i_Total_movement = Job_INDEX.i_temp
                    for k in range(total_num_operation):
                        Job_route[k] = mat[k]
            temp = recursive(step+1, mat, num, Job_route, total_num_operation, Num_part_on_pallet, part_position_index, J, temp_op_index2, Job_INDEX)

            num[i] += 1
    if (temp == 0):
        return 0
    else:
        return 1


def Job_route_DP(J, Job_INDEX):
    total_num_operation = J.i_Total_Number_Operation #총 operation개수
    Num_part_on_pallet = J.i_Num_parts #몇개의 part가 올라와있는지

    temp_op_index2 = [0 for i in range(Num_part_on_pallet)] #part들의 현재 operation index, index는 0이다
    part_position_index = [0 for i in range(Num_part_on_pallet)] #Job의 P에는 NULL로 된 part공간이 있다. 따라서 들어있는 P의 postion index가 필요
    Job_route = [0 for i in range(total_num_operation)]
    num = [0 for i in range(Num_part_on_pallet)]
    mat = [0 for i in range(total_num_operation)]

    j = 0
    k = 0

    if (J.P[k] != None):                         ##########
        part_position_index[j] = k               ##########
        k += 1
        for j in range(1, J.i_Num_parts):
            while (k != J.Pallet_job.i_Num_Fixt):
                if (J.P[k] != None):
                    part_position_index[j] = k
                    k += 1
                    break
                else:
                    k += 1
    else:
        k += 1
        for j in range(J.i_Num_parts):
            while (k != J.Pallet_job.i_Num_Fixt):
                if (J.P[k] != None):
                    part_position_index[j] = k
                    k += 1
                    break
                else:
                    k += 1

    for j in range(Num_part_on_pallet):
        num[j] = J.P[part_position_index[j]].PT.i_Num_Operation - 2 #여기서 위치도 알아야됨

    step = 0
    r = recursive(step, mat, num, Job_route, total_num_operation, Num_part_on_pallet, part_position_index, J, temp_op_index2, Job_INDEX) #job route 결정

    J.i_OP_Route = [0 for i in range(J.i_Total_Number_Operation + 1)] #operation route
    J.Part_Route = [] #part route
    J.Machine_Route = [] #machine route
    J.s_Machine_Name = []
    J.i_Processing_time = [0 for i in range(J.i_Total_Number_Operation + 1)]
    
    for k in range(J.i_Total_Number_Operation + 1):
        J.Part_Route.append(Part_T())
        J.Machine_Route.append(Machine_T())
        J.s_Machine_Name.append('')
    
    for j in range(Num_part_on_pallet):
        temp_op_index2[j] = 0

    if (r != 0):
        for j in range(total_num_operation):
            J.i_OP_Route[j] = (temp_op_index2[Job_route[j]-1])+1
            J.Part_Route[j] = J.P[part_position_index[Job_route[j]-1]]
            J.Machine_Route[j] = J.P[part_position_index[Job_route[j]-1]].Mac_Select[temp_op_index2[Job_route[j]-1]+1]
            J.s_Machine_Name[j] = J.P[part_position_index[Job_route[j]-1]].s_Mac_Select_name[temp_op_index2[Job_route[j]-1]+1]
            J.i_Processing_time[j] = J.P[part_position_index[Job_route[j]-1]].i_Select_Process_Time[temp_op_index2[Job_route[j]-1]+1]

            temp_op_index2[Job_route[j]-1] += 1

    J.i_OP_Route.append(None)
    J.Part_Route.append(None)
    J.Machine_Route.append(None)
    J.s_Machine_Name.append(None)
    J.i_Processing_time.append(None)

    J.i_TWKR = TWKR2(J)


def Loading(con): #Job_Define_FIFO 추가
    con.J = [Job_T() for i in range(con.i_Num_pallet)] #con.J 에 대한 첫 할당
    tem_Job = None # Job_T()
    con.Job_index = con.Job_INDEX.i_Job_index
    Job_list = con.Job_queue #Job_list에 대한 첫 할당

    for i in range(con.i_Num_pallet): #Input_Sequence_Option을 결정한 뒤, tem_Job에 정해진 룰의 return값을 할당
        if (con.Pallet_type[i].i_rest_Pallet == 1): #해당 Pallet이 system으로 들어가면 0으로 바뀌고, 그렇지 않으면 1 
            if (con.Input_Sequence_Option == 1):
                tem_Job = Job_Define_SPPT(con, con.Pallet_type[i], Job_list)
            elif (con.Input_Sequence_Option == 2):
                tem_Job = Job_Define_EDD(con, con.Pallet_type[i], Job_list)
            if (tem_Job.i_Empty == 0): # Part가 올라간 pallet만 job으로 define, pallet에 올라가는 part가 없으면 tem_Job.i_Empty = 1
                con.Pallet_type[i].i_rest_Pallet = 0
                con.J[con.Job_index].P = []
                for j in range(tem_Job.Pallet_job.i_Num_Fixt):
                    con.J[con.Job_index].P.append(tem_Job.P[j])
                    if (con.J[con.Job_index].P[j] != None):
                        con.J[con.Job_index].P[j].i_Job_No = con.Job_index #어떤 job에 속하는지
                con.J[con.Job_index].Pallet_job = tem_Job.Pallet_job
                con.J[con.Job_index].i_Empty = tem_Job.i_Empty
                con.J[con.Job_index].i_Total_Number_Operation = (tem_Job.i_Total_Number_Operation - (2 * tem_Job.i_Num_parts))
                con.J[con.Job_index].i_Job_No = con.Job_index
                con.J[con.Job_index].i_Num_parts = tem_Job.i_Num_parts # 몇 개의 part가 올라갔는지
                con.J[con.Job_index].i_current_position = 0 # Route들을 들고 다닐 때 필요하다.
                con.J[con.Job_index].i_current_state = 0 # '1'이면 작업중이다.
                con.J[con.Job_index].f_avg_duedate = (tem_Job.f_avg_duedate) / (tem_Job.i_Num_parts)
                
                # 해당 con.Job_index에 해당하는 pallet이 con.i_Num_pallet 만큼 차례대로 들어간다.
                #Job route를 greedy 방법으로 결정
                if (con.Job_route_Option == 1):
                    Job_route(con.J[con.Job_index])
                # Job route를 HU 방법으로 결정
                elif (con.Job_route_Option == 2):
                    con.Job_INDEX.i_Total_movement = 99
                    con.Job_INDEX.i_temp = 99
                    Job_route_HU(con.J[con.Job_index], con.Job_INDEX)
                # Job route를 DP 방법으로 결정
                elif (con.Job_route_Option == 3):
                    con.Job_INDEX.i_Total_movement = 99
                    con.Job_INDEX.i_temp = 99
                    Job_route_DP(con.J[con.Job_index], con.Job_INDEX)
                
                Job_list.push_back(con.J[con.Job_index]) # Part가 올라간 pallet만 buffer(job_list)로 간다 리스트에 뒤에서 부터 삽입
                con.Job_index += 1
        """
        else:
            print("No more pallet") #만약 남는 팔렛이 없다면?? 어떻게 ??
        """
        #print(con.Dummy.head.next.next.Obj.Mac_Select)
        con.Job_INDEX.i_Job_index = con.Job_index
        #print(Job_list.head.next.Obj.i_Processing_time)
    #print(con.Job_queue)


def Find_last_job(JL):
    temp = JL.tail.pre
    if (temp == JL.head):
        temp_Job = None
    else:
        temp_Job = temp.Obj

    return temp_Job


def Dispatching_FIFO(M, Job_queue, Time): # M = Mac_temp(현재 machine), Job_queue = central buffer, Time = simulation time
    temp_Job = None
    i_Next_Rest_Time = M.i_Next_Rest_Time
    temp = Job_queue.head.next

    while (temp != Job_queue.tail):
        if ((temp.Obj.i_Processing_time[temp.Obj.i_current_position] + Time)<=i_Next_Rest_Time) and (temp.Obj.i_current_state==0) and (temp.Obj.Machine_Route[temp.Obj.i_current_position]==M) and (temp.Obj.i_Terminate!=1):
            # print("FIFO Time:", Time)
            # Current state가 0이고, 지금 할 operation의 processing time이 machine의 next_rest_time을 넘지 않고, 그때의 route의 machine과 M machine이 같고, pallet(job)의 i_Terminated가 1이 아닐때.
            temp_Job = temp.Obj #그때의 job이 temp_job이 된다.
            break

        temp = temp.next

    if (temp_Job == None):
        return None
    else:
        return temp_Job


def Dispatching_SPT(M, Job_queue, Time):
    i_min = 9999999
    temp = Job_queue.head.next
    temp_Job = None
    i_Next_Rest_Time = M.i_Next_Rest_Time

    while (temp != Job_queue.tail):
        if ((temp.Obj.i_Processing_time[temp.Obj.i_current_position]+Time) <= i_Next_Rest_Time) and (temp.Obj.i_current_state == 0) and ((temp.Obj.Machine_Route[temp.Obj.i_current_position]) == M) and (temp.Obj.i_Terminate != 1):
            #current state가 0이고, 지금 할 operation의 processing time이 machine의 next_rest_time을 넘지 않고, 그때의 route의 machine과 M machine이 같을때
            if (i_min > temp.Obj.i_Processing_time[temp.Obj.i_current_position]):
                temp_Job = temp.Obj #그때의 job이 temp_job이 된다
                i_min = temp.Obj.i_Processing_time[temp.Obj.i_current_position] #그때의 job의 processing time이 min 값이 된다

        temp = temp.next

    if (temp_Job == None):
        return None
    else:
        return temp_Job


def Dispatching_TWKR(M, Job_queue, Time):
    i_max = 0
    temp = Job_queue.head.next
    temp_Job = None
    i_Next_Rest_Time = M.i_Next_Rest_Time

    while (temp != Job_queue.tail):
        if ((temp.Obj.i_Processing_time[temp.Obj.i_current_position]+Time) <= i_Next_Rest_Time) and (temp.Obj.i_current_state == 0) and ((temp.Obj.Machine_Route[temp.Obj.i_current_position]) == M) and (temp.Obj.i_Terminate != 1):
            #current state가 0이고, 지금 할 operation의 processing time이 machine의 next_rest_time을 넘지 않고, 그때의 route의 machine과 M machine이 같을때
            if (i_max > temp.Obj.i_TWKR):
                temp_Job = temp.Obj #그때의 job이 temp_job이 된다
                i_max = temp.Obj.i_TWKR #그때의 job의 processing time이 min 값이 된다

        temp = temp.next

    if (temp_Job == None):
        return None
    else:
        return temp_Job


def Dispatching_MST(M, Job_queue, Time): #M = Mac_Temp
    d_min = 9999999
    temp = Job_queue.head.next
    temp_Job = None
    i_Next_Rest_Time = M.i_Next_Rest_Time
    #print(temp.Obj)

    while (temp != Job_queue.tail):
        #print('temp.Obj.i_TWKR:', temp.Obj.i_TWKR)
        #print('Time:', Time), Time: 현 시점
        v = temp.Obj.f_avg_duedate - Time - temp.Obj.i_TWKR
        if ((temp.Obj.i_Processing_time[temp.Obj.i_current_position]+Time) <= i_Next_Rest_Time) and (temp.Obj.i_current_state == 0) and ((temp.Obj.Machine_Route[temp.Obj.i_current_position]) == M) and (temp.Obj.i_Terminate != 1):
            #current state가 0이고, 지금 할 operation의 processing time이 machine의 next_rest_time을 넘지 않고, 그때의 route의 machine과 M machine이 같을때
            if (d_min > v):
                temp_Job = temp.Obj
                d_min = v

        temp = temp.next

    #print(type(temp_Job.Part_Route[1].Machine_Sequence))

    if (temp_Job == None):
        return None
    else:
        return temp_Job


def max(a, b):
    if (a>b):
        return a
    else:
        return b


def Dispatching_MDD(M, Job_queue, Time):
    d_min = 9999999
    temp = Job_queue.head.next
    temp_Job = None
    i_Next_Rest_Time = M.i_Next_Rest_Time

    while (temp != Job_queue.tail):                                  #############################################################   
        v = max(int(temp.Obj.f_avg_duedate), Time + temp.Obj.i_TWKR) #############################################################
        if ((temp.Obj.i_Processing_time[temp.Obj.i_current_position]+Time) <= i_Next_Rest_Time) and (temp.Obj.i_current_state == 0) and ((temp.Obj.Machine_Route[temp.Obj.i_current_position]) == M) and (temp.Obj.i_Terminate != 1):
            #current state가 0이고, 지금 할 operation의 processing time이 machine의 next_rest_time을 넘지 않고, 그때의 route의 machine과 M machine이 같을때
            if (d_min > v):
                temp_Job = temp.Obj
                d_min = v

        temp = temp.next

    if (temp_Job == None):
        return None
    else:
        return temp_Job


def Dispatching_Option_Selection(Dispatching_Option, Mac_Temp, Job_queue, Time):
    if (Dispatching_Option == 1):
        Job_temp = Dispatching_FIFO(Mac_Temp, Job_queue, Time)

    elif (Dispatching_Option == 2):
        Job_temp = Dispatching_SPT(Mac_Temp, Job_queue, Time)

    elif (Dispatching_Option == 3):
        Job_temp = Dispatching_TWKR(Mac_Temp, Job_queue, Time)
                
    elif (Dispatching_Option == 4):
        Job_temp = Dispatching_MST(Mac_Temp, Job_queue, Time)

    elif (Dispatching_Option == 5):
        Job_temp = Dispatching_MDD(Mac_Temp, Job_queue, Time)

    else:
        print('Dispatching Option Error')
        return -1
    
    return Job_temp


def input_Last_to_Job_List(JL, J, trans):
    JL.push_back(J)
    #JL.head.next.Obj = J
    #JL.head.next.Obj2 = J.Part_Route[J.i_current_position]
    JL.tail.pre.Obj2 = J.Part_Route[J.i_current_position]

    JL.tail.pre.operation = J.i_OP_Route[J.i_current_position]
    JL.tail.pre.Start_time = J.i_Current_Process_Completion_time - J.i_Processing_time[J.i_current_position]
    JL.tail.pre.End_time = J.i_Current_Process_Completion_time
    JL.tail.pre.PID = J.Part_Route[J.i_current_position].PT.s_PID[J.i_current_position]
    """
    JL.head.next.Obj.operation = J.i_OP_Route[J.i_current_position]
    JL.head.next.Obj.Start_time = J.i_Current_Process_Completion_time - J.i_Processing_time[J.i_current_position]
    JL.head.next.Obj.End_time = J.i_Current_Process_Completion_time
    JL.head.next.Obj.PID = J.Part_Route[J.i_current_position].PT.s_PID[J.i_current_position]
    """
    return JL.nNodes

def input_Last_to_Machine_Sched_List(ML, M, St, Ed, str0):
    #ML.tail = temp2
    ML.push_back(M)
    ML.tail.pre.Start_time = St
    ML.tail.pre.End_time = Ed
    ML.tail.pre.PID = str0
    """
    M.Start_time = St
    M.End_time = Ed
    M.PID = str0
    """
    return ML.nNodes


def event_Executer(con, Time): # Time = Simulation_time
    #in to the machine from queue
    a = 0
    b = 0
    check = 0
    EV = 0

    trans = con.i_Transportation_time
    temp_cell_job = con.Job_queue.head.next
    CM_Temp = con.ML.head.next
    
    Mac_Temp = None
    Job_temp = None
    Pre_Job = None # 이전 job 체크해서 transportation time 추가

    while (CM_Temp != con.ML.tail): # Machine별 event 체크
        Mac_Temp = CM_Temp.Obj
        
        # End of the vacation time in calender
        if (Mac_Temp.i_Working_or_Rest == 0) and (Mac_Temp.i_Next_Working_time == Time):
            Mac_Temp.i_Current_Schedule += 1
            if (Mac_Temp.i_Current_Schedule == Mac_Temp.i_Number_Schedule):
                Mac_Temp.i_Next_Working_time = -1
                #####################(위)Mac_Temp.i_Next_Working_time = -1#####################
                Mac_Temp.i_Next_Rest_Time = 31536000 # 1년
            else:
                Mac_Temp.i_Next_Working_time = -1
                Mac_Temp.i_Next_Rest_Time = Mac_Temp.i_Machine_Schedule[Mac_Temp.i_Current_Schedule]
            Mac_Temp.i_Working_or_Rest = 1
            EV = 1

        # Change a machine to vacate mode by calender (비우기 모드로 변경)
        if (Mac_Temp.i_Working_or_Rest == 1) and (Mac_Temp.i_Next_Rest_Time == Time):
            Mac_Temp.i_Current_Schedule += 1
            if (Mac_Temp.i_Current_Schedule == Mac_Temp.i_Number_Schedule):
                Mac_Temp.i_Next_Rest_Time = -1
                Mac_Temp.i_Next_Working_time = 31536000
            else:
                Mac_Temp.i_Next_Working_time = Mac_Temp.i_Machine_Schedule[Mac_Temp.i_Current_Schedule]
                Mac_Temp.i_Next_Rest_Time = -1
            
            Mac_Temp.i_Working_or_Rest = 0
            EV = 1

        # Available machine 에서 dispatching rule을 이용하여 process를 시작한다.
        if (Mac_Temp.i_Current_State == 0) and (Mac_Temp.i_Working_or_Rest == 1): # i_Current_State가 0이면 할 수 있다.
            Pre_Job = Find_last_job(Mac_Temp.Job_Sequence) # 이전 job을 찾는 것이다.
            if (Pre_Job == None):
                Job_temp = Dispatching_Option_Selection(con.Dispatching_Option, Mac_Temp, con.Job_queue, Time)
                if (Job_temp == -1):
                    return -1

            else: # Pallet(job) 선택
                if (Pre_Job.Machine_Route[Pre_Job.i_current_position] == Mac_Temp):
                    #print("@@@@@@@@")
                    if (Pre_Job.i_current_state == 0): # Job(pallet)이 process 중이 아니어야되고
                        if (Mac_Temp.i_End_time == Time): # 그 때의 machine이 방금 끝나야 된다. 이전에 끝났던 machine이 쉬다가 다시 똑같은 job을 받을 경우에는 이동시간 추가되어야 한다.
                            Job_temp = Pre_Job
                        else:
                            Job_temp = Dispatching_Option_Selection(con.Dispatching_Option, Mac_Temp, con.Job_queue, Time)                            
                            if (Job_temp == -1):
                                return -1
                    else:
                        Job_temp = Dispatching_Option_Selection(con.Dispatching_Option, Mac_Temp, con.Job_queue, Time)
                        if (Job_temp == -1):
                            return -1
                else:
                    Job_temp = Dispatching_Option_Selection(con.Dispatching_Option, Mac_Temp, con.Job_queue, Time)
                    if (Job_temp == -1):
                        return -1
            if (Job_temp != None): # Process 시작
                #print("Time:", Time)
                if (Pre_Job == Job_temp): # Pallet(job) 입장에서의 completion time
                    if (Mac_Temp.i_End_time == Time): #그 때의 machine이 방금 끝나야 된다. 이전에 끝났던 machine이 쉬다가 다시 똑같은 job을 받을 경우에는 이동시간 추가되어야 한다.
                        Job_temp.i_Current_Process_Completion_time = Time + Job_temp.i_Processing_time[Job_temp.i_current_position]
                    else:
                        Job_temp.i_Current_Process_Completion_time = Time + trans + Job_temp.i_Processing_time[Job_temp.i_current_position]
                else:
                    Job_temp.i_Current_Process_Completion_time = Time + trans + Job_temp.i_Processing_time[Job_temp.i_current_position]
                
                input_Last_to_Job_List(Mac_Temp.Job_Sequence, Job_temp, trans) # Dispatching rule에서 지금 machine에 process될 수 있는 pallet을 선택했기 때문에, 지금 machine의 Job_Sequence에 넣어도 되는 것이다.

                Mac_Temp.i_Current_State = 1 # Machine이 process 중이다.
                Mac_Temp.i_Current_Job_Start_Time = Time
                #####################(위)왜 Time과 같아지게 되는걸까?#####################

                if (Pre_Job == Job_temp): # Machine 입장에서의 End time
                    if (Mac_Temp.i_End_time == Time): #그 때의 machine이 방금 끝나야 된다. 이전에 끝났던 machine이 쉬다가 다시 똑같은 job을 받을 경우에는 이동시간 추가되어야 한다.
                        Mac_Temp.i_Current_Job_End_Time = Time + Job_temp.i_Processing_time[Job_temp.i_current_position]
                        Mac_Temp.i_End_time = Time + Job_temp.i_Processing_time[Job_temp.i_current_position]
                    else:
                        Mac_Temp.i_Current_Job_End_Time = Time + trans + Job_temp.i_Processing_time[Job_temp.i_current_position]
                        Mac_Temp.i_End_time = Time + trans + Job_temp.i_Processing_time[Job_temp.i_current_position]
                else:
                    Mac_Temp.i_Current_Job_End_Time = Time + trans + Job_temp.i_Processing_time[Job_temp.i_current_position]
                    Mac_Temp.i_End_time = Time + trans + Job_temp.i_Processing_time[Job_temp.i_current_position]

                Mac_Temp.i_Current_Part_ID = Job_temp.Part_Route[Job_temp.i_current_position].PT.i_Job_ID  #현재 machine process중인 part type
                Mac_Temp.i_Current_Part_No = Job_temp.Part_Route[Job_temp.i_current_position].i_Part_No    #현재 machine이 process중인 part 번호
                Mac_Temp.i_Current_Job_No = Job_temp.i_Job_No                                              #현재 machine이 process중인 Job

                con.Job_INDEX.i_Last_processing_time = Job_temp.i_Processing_time[Job_temp.i_current_position]
                
                #print("@@@@@@@@@")
                # Part 기준으로 machine이랑 시간 받는다.
                input_Last_to_Machine_Sched_List(Job_temp.Part_Route[Job_temp.i_current_position].Machine_Sequence, Mac_Temp, Mac_Temp.i_Current_Job_Start_Time, Mac_Temp.i_Current_Job_End_Time, Job_temp.Part_Route[Job_temp.i_current_position].PT.s_PID[Job_temp.i_OP_Route[Job_temp.i_current_position]])

                temp = Job_temp.Part_Route[Job_temp.i_current_position].Machine_Sequence.tail.pre

                Job_temp.i_TWKR = Job_temp.i_TWKR - Job_temp.i_Processing_time[Job_temp.i_current_position]
                #print("Time:", Time)
                Job_temp.i_current_position += 1

                Job_temp.i_current_state = 1 # Pallet(job)이 process 중이다.

                EV = 1

        if (Mac_Temp.i_Current_Job_End_Time == Time):
            Mac_Temp.i_Current_Part_ID = -1
            Mac_Temp.i_Current_Part_No = -1
            Mac_Temp.i_Current_Job_No = -1
            Mac_Temp.i_Current_Job_End_Time = -1
            Mac_Temp.i_Current_Job_Start_Time = -1
            Mac_Temp.i_Current_State = 0 # Machine 사용 가능

            Job_temp = Mac_Temp.Job_Sequence.tail.pre.Obj
            Job_temp.i_Current_State = 0 #다시 이 job은 선택 될 수 있다.

            if (Job_temp.Part_Route[(Job_temp.i_current_position)-1].i_Terminated == 1):
                Cell_Temp = Job_temp.Part_Route[(Job_temp.i_current_position)-1].Machine_Sequence.head.next
                while (Cell_Temp.next != Job_temp.Part_Route[(Job_temp.i_current_position)-1].Machine_Sequence.tail):
                    Cell_Temp = Cell_Temp.next

                Job_temp.Part_Route[(Job_temp.i_current_position)-1].i_completion_time = Cell_Temp.i_End_time #그 때 part의 종료시간
                Job_temp.i_Completion_time = Cell_Temp.i_End_time #Job의 종료시간. 계속해서 업데이트된다. Part들의 종료시간 중에 하나가 job의 종료시간이다.                    
                
            EV = 1

        CM_Temp = CM_Temp.next

    k = 0
    while (temp_cell_job != con.Job_queue.tail):
        k += 1
        if (temp_cell_job.Obj.i_Processing_time[(temp_cell_job.Obj.i_current_position)+1] == None):
            #print("Time:", Time)
            temp_cell_job.Obj.i_Terminate = 1
            EV = 1

        temp_cell_job = temp_cell_job.next

    #Dummy Processing - stack to as/rs station
    temp_cell_job = con.Job_queue.head.next
    while (temp_cell_job != con.Job_queue.tail): ## Job이 끝나면 job_queue buffer에서 제거해준다.
        #print("######")
        if (temp_cell_job.Obj.i_Terminate == 1):
            #print("Time:", Time)
            temp_cell_job.Obj.Pallet_job.i_rest_Pallet = 1 #그 때의 pallet은 사용 가능.        

            for i in range(temp_cell_job.Obj.Pallet_job.i_Num_Fixt):
                temp_cell_job.Obj.Pallet_job.Fixture[i].i_rest_Fixture = 1 #그때 pallet의 fixture는 사용가능

            b += 1
            #print("$$$$$$")
            for i in range(temp_cell_job.Obj.Pallet_job.i_Num_Fixt):
                if (temp_cell_job.Obj.P[i] != None):
                    #print("@@@@@@@@")
                    temp_cell_job.Obj.P[i].i_Terminated = 1
                    con.Dummy.push_back(temp_cell_job.Obj.P[i]) #job이 다 끝났다면 그때의 P는 dummy로 간다
                    #####################(위)왜 Dummy에 push back을 하는건가?#####################
                    #####################(위)Dummy에는 공정이 안된 가공물들을 넣는 곳 아니엇나?#####################

            con.Job_queue.pop_it(temp_cell_job)

            temp_cell_job = con.Job_queue.head.next
            EV = 1
            continue
        temp_cell_job = temp_cell_job.next

    CJ_Temp = con.Dummy.head.next

    while (CJ_Temp != con.Dummy.tail): #언로딩 체크
        next_part = 100000000 #아무값 지정

        if (CJ_Temp.Obj.i_Terminated == 1): #끝났으면 빠져 나가고 삭제
            if (con.J[CJ_Temp.Obj.i_Job_No].i_Completion_time == Time):
                if (CJ_Temp.Obj.PT.i_Pre_part == -2):
                    con.Dummy.pop_it(CJ_Temp)
            a += 1
            CJ_Temp = con.Dummy.head.next
            EV = 1
            continue
        CJ_Temp = CJ_Temp.next
    
    check = con.Job_INDEX.i_Job_index

    if (con.Dummy.nNodes != 0):
        Loading(con)
        if (check != con.Job_INDEX.i_Job_index):
            EV = 1
    return EV


def Simulation_Start(con):
    k = 0
    b = 0
    c = 1500
    Simulation_time = 0
    Terminated = 0
    temp_job_cell = con.Job_queue.head.next
    CJ_temp = con.Dummy.head.next
    con.Job_INDEX.i_Last_processing_time = 0

    while True:
        event = 1
        while (event != 0):
            event = event_Executer(con, Simulation_time)
            #Main procedure
            if (event == -1): #error check
                return -1 #return to main - terminated
            #while - checking event in the same time
        
        Simulation_time += 1 #time increase => there is no event
        #print("Simulation_time:", Simulation_time)
        Terminated = 0

        for i in range(con.i_Num_Parts):
            Terminated += con.P[i].i_Terminated
        if (Terminated == con.i_Num_Parts):
            break
        print("Simulation_time:", Simulation_time)
    temp_job_cell = con.Job_queue.head

    k = 0
    while (temp_job_cell != con.Job_queue.tail): #언로딩 체크
        temp_job_cell = temp_job_cell.next
    
    CJ_temp = con.Dummy.head

    k = 0
    while (CJ_temp != con.Dummy.tail):
        k += 1
        CJ_temp = CJ_temp.next

    return Simulation_time


def Main():
    finName = 'practice_data.txt'
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
    con0 = con(RuleCombi1, fin, fout)

    load = Loading(con0)

    Completion_Time = Simulation_Start(con0)    #event_Executer

    Completion_Time = Completion_Time + con0.Job_INDEX.i_Last_processing_time + con0.i_Transportation_time
    
    End = time.time()
    f_Duration = End - Begin

    ############################################################################

    tardy = 0
    if (Completion_Time == -1):
        return -1

    Max = 0
    N_tardy = 0
    avr_Flow_Time = 0

    for i in range(con0.i_Num_Parts):
        """ 
        Cell_Temp = con0.P[i].Machine_Sequence.head.next        
        while (Cell_Temp.next != con0.P[i].Machine_Sequence.tail):
            Cell_Temp = Cell_Temp.next
        """
        con0.P[i].i_completion_time = con0.P[i].Machine_Sequence.tail.pre.Obj.i_End_time

    for i in range(con0.i_Num_Parts):
        #if (con0.P[i].PT.i_Pre_part != -1):
        avr_Flow_Time += con0.P[i].i_completion_time
        tardy += max(con0.P[i].i_completion_time - con0.P[i].i_Due_date, 0)
        if (Max < max(con0.P[i].i_completion_time - con0.P[i].i_Due_date, 0)):
            Max = max(con0.P[i].i_completion_time - con0.P[i].i_Due_date, 0)

        if ((max(con0.P[i].i_completion_time - con0.P[i].i_Due_date, 0)) != 0):
            N_tardy += 1

        avr_Tardy = tardy / con0.i_Num_Parts
        total_Flow_Time = avr_Flow_Time
        avr_Flow_Time /= con0.i_Num_Parts


    #foutName.writelines(Completion_Time, '', tardy, '', total_Flow_Time, f_Duration)
    
    return 0
    #print(iDuration)
Main()