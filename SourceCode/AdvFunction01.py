from AdvStructure import *
from AdvConfig01 import Config_T as con
import time
import sys
from CommonFunctions import *
from operator import itemgetter, attrgetter

def Operation_sequencing_SMPT(con2, Job): #shortest minimum processing time
    LstPart = []
    Job.Part_Route = [None for i in range(Job.i_Total_Number_Operation+1)]
    Job.i_OP_Route = [None for i in range(Job.i_Total_Number_Operation+1)]

    for i in range(Job.Pallet_job.i_Num_Fixt):
        LstOp = []
        if (Job.P[i] != None):
            for j in range(Job.P[i].PT.i_Num_Operation):
                if (Job.P[i].PT.i_Num_Alternative_Machine[j] != 0):            
                    i_Operation_Idx = j
                    i_min_proc = min(Job.P[i].PT.i_Standard_Time[j])
                    LstOp.append([Job.P[i].i_Part_index, Job.P[i].PT.i_Fixture_Type, i_Operation_Idx, Job.P[i], i_min_proc])
            LstPart.append(LstOp)

    for i in range(Job.i_Total_Number_Operation):
        min0 = 999999
        for j in range(len(LstPart)):
            Temp_op = LstPart[j][0]
            if (Temp_op[4] < min0):
                min0 = Temp_op[4]
                min0_part_idx = j
        Job.i_OP_Route[i] = LstPart[min0_part_idx][0][2]
        Job.Part_Route[i] = LstPart[min0_part_idx][0][3]
        #con2.J[con2.Job_index].Part_Route[i] = LstPart[min0_part_idx][0][3]
        #con2.J[con2.Job_index].i_OP_Route[i] = LstPart[min0_part_idx][0][2]       
        del LstPart[min0_part_idx][0]

        for j in range(len(LstPart)):
            if (len(LstPart[j])==0):
                del LstPart[j]
                break

    l = 0
    return Job

def Operation_sequencing_SAPT(con2, Job): #shortest average processing time
    LstPart = []
    Job.Part_Route = [None for i in range(Job.i_Total_Number_Operation+1)]
    Job.i_OP_Route = [None for i in range(Job.i_Total_Number_Operation+1)]

    for i in range(Job.Pallet_job.i_Num_Fixt):
        LstOp = []
        if (Job.P[i] != None):
            for j in range(Job.P[i].PT.i_Num_Operation):
                if (Job.P[i].PT.i_Num_Alternative_Machine[j] != 0):
                    i_Operation_Idx = j
                    f_Avg_proc = sum(Job.P[i].PT.i_Standard_Time[j])/len(Job.P[i].PT.i_Standard_Time[j])
                    LstOp.append([Job.P[i].i_Part_index, Job.P[i].PT.i_Fixture_Type, i_Operation_Idx, Job.P[i], f_Avg_proc])
            LstPart.append(LstOp)

    for i in range(Job.i_Total_Number_Operation):
        min0 = 999999
        for j in range(len(LstPart)):
            Temp_op = LstPart[j][0]
            if (Temp_op[4] < min0):
                min0 = Temp_op[4]
                min0_part_idx = j
        Job.i_OP_Route[i] = LstPart[min0_part_idx][0][2]
        Job.Part_Route[i] = LstPart[min0_part_idx][0][3]
        #con2.J[con2.Job_index].Part_Route[i] = LstPart[min0_part_idx][0][3]
        #con2.J[con2.Job_index].i_OP_Route[i] = LstPart[min0_part_idx][0][2]
        del LstPart[min0_part_idx][0]

        for j in range(len(LstPart)):
            if (len(LstPart[j])==0):
                del LstPart[j]
                break

    l = 0
    return Job

def Operation_sequencing_STPT(con2, Job):
    LstPart = []
    Job.Part_Route = [None for i in range(Job.i_Total_Number_Operation+1)]
    Job.i_OP_Route = [None for i in range(Job.i_Total_Number_Operation+1)]

    for i in range(Job.Pallet_job.i_Num_Fixt):
        LstOp = []
        if (Job.P[i] != None):
            for j in range(Job.P[i].PT.i_Num_Operation):
                if (Job.P[i].PT.i_Num_Alternative_Machine[j] != 0):
                    i_Operation_Idx = j
                    i_Sum_proc = sum(Job.P[i].PT.i_Standard_Time[j])
                    LstOp.append([Job.P[i].i_Part_index, Job.P[i].PT.i_Fixture_Type, i_Operation_Idx, Job.P[i], i_Sum_proc])
            LstPart.append(LstOp)

    for i in range(Job.i_Total_Number_Operation):
        min0 = 999999
        for j in range(len(LstPart)):
            Temp_op = LstPart[j][0]
            if (Temp_op[4] < min0):
                min0 = Temp_op[4]
                min0_part_idx = j
        Job.i_OP_Route[i] = LstPart[min0_part_idx][0][2]
        Job.Part_Route[i] = LstPart[min0_part_idx][0][3]
        #con2.J[con2.Job_index].Part_Route[i] = LstPart[min0_part_idx][0][3]
        #con2.J[con2.Job_index].i_OP_Route[i] = LstPart[min0_part_idx][0][2]       
        del LstPart[min0_part_idx][0]

        for j in range(len(LstPart)):
            if (len(LstPart[j])==0):
                del LstPart[j]
                break

    l = 0
    return Job


def Operation_seqeuncing_option(Operation_Sequence_Option, con2, Job):
    if (Operation_Sequence_Option == 1):
        Job = Operation_sequencing_SMPT(con2, Job)
    elif (Operation_Sequence_Option == 2):
        Job = Operation_sequencing_SAPT(con2, Job)
    elif (Operation_Sequence_Option ==3):
        Job = Operation_sequencing_STPT(con2, Job)
    else:
        print('Operation seqeuncing Error')
        return -1        

    return Job

def Initial_Mac_selection(con2, Job):
    #P.Mac_Select, P.s_Mac_Select_name, P.i_Mac_Select_index, P.i_Select_Process_Time
    Temp_mac = None
    Temp_proc = None
    min0 = 999999

    i_Op_idx = Job.i_OP_Route[0] #무조건 0
    Temp_part = Job.Part_Route[0]

    #Job.Machine_Route = [None for i in range(Job.i_Total_Number_Operation+1)]
    #Job.s_Machine_Name = [None for i in range(Job.i_Total_Number_Operation+1)]
    #Job.i_Processing_time = [None for i in range(Job.i_Total_Number_Operation+1)]

    LstMac = []

    for i in range(Job.Pallet_job.i_Num_Fixt):
        if (Job.P[i] == Temp_part):
            i_Select_part_indx = i
            #Job.P[i].i_Select_Process_Time[i_Op_idx] = min(Job.P[i].PT.i_Standard_Time[i_Op_idx])
            if (Job.P[i].PT.i_Num_Alternative_Machine[i_Op_idx] != 0):
                for j in range(Job.P[i].PT.i_Num_Alternative_Machine[i_Op_idx]):
                    Temp_mac = con2.ML.head.next
                    while (Temp_mac != con2.ML.tail):
                        if (Temp_mac.Obj == Job.P[i].PT.Alternative_Mac[i_Op_idx][j]):
                            LstMac.append([j+1, Job.P[i].PT.Alternative_Mac[i_Op_idx][j], Job.P[i].PT.s_Alternative_Machine_Name[i_Op_idx][j], Job.P[i].PT.i_Standard_Time[i_Op_idx][j], Job.P[i].PT.s_Alternative_Machine_Name[i_Op_idx][j]])
                        Temp_mac = Temp_mac.next  
                LstMac = sorted(LstMac, key=itemgetter(3))

    Job.P[i_Select_part_indx].i_Mac_Select_index[i_Op_idx] = LstMac[0][0]
    Job.P[i_Select_part_indx].Mac_Select[i_Op_idx] = LstMac[0][1]
    Job.P[i_Select_part_indx].s_Mac_Select_name[i_Op_idx] = LstMac[0][2]
    Job.P[i_Select_part_indx].i_Select_Process_Time[i_Op_idx] = LstMac[0][3] #Operation 별로 선택된 processing time
    Job.P[i_Select_part_indx].i_Total_Processing_Time += LstMac[0][3]

    Job.Machine_Route[0] = LstMac[0][1]
    Job.s_Machine_Name[0] = LstMac[0][2]
    Job.i_Processing_time[0] = LstMac[0][3]
    #con2.J[con2.Job_index].Machine_Route[0] = LstMac[0][1]
    #con2.J[con2.Job_index].s_Machine_Name[0] = LstMac[0][2]
    #con2.J[con2.Job_index].i_Processing_time[0] = LstMac[0][3]
    
    #con2.Job_INDEX.i_Machine_pro[LstMac[0][0]] += LstMac[0][3]
    #con2.Job_INDEX.machine_name[LstMac[0][0]] = LstMac[0][2]
    
    l = 0
    return Job

def TWKR0(J): #Total work remaining(현재꺼 빼고)
    f_Remain_NotIt = 0 #현재 position에 해당하는(machine이 정해진) operation을 제외하고, 나머지 operations processing time의 합
    Temp_op_idx = J.i_current_position
    for i in range(J.i_Total_Number_Operation-(Temp_op_idx-1)):
        i_Sum = 0
        i_Length = len(J.Part_Route[Temp_op_idx+1].PT.i_Standard_Time[J.i_OP_Route[Temp_op_idx+1]])
        i_Sum += sum(J.Part_Route[Temp_op_idx+1].PT.i_Standard_Time[J.i_OP_Route[Temp_op_idx+1]]) / len(J.Part_Route[Temp_op_idx+1].PT.i_Standard_Time[J.i_OP_Route[Temp_op_idx+1]])
        f_Remain_NotIt += (i_Sum / i_Length)

    TWKR = J.i_Processing_time[J.i_current_position] + f_Remain_NotIt
    return TWKR

def Loading(con1): #추후에 element로 i_Time 추가
    LLBuffer = con1.Job_queue
    i_Trans = con1.i_Transportation_time
    LstPallet_list = []

    con1.Job_index = con1.Job_INDEX.i_Job_index
    
    for i in range(con1.i_Num_pallet):
        if (con1.Pallet_type[i].i_rest_Pallet == 1):

            for j in range(con1.i_Num_Machines):
                con1.Job_INDEX.machine_name.append(None)
                con1.Job_INDEX.i_Machine_pro.append(0)

            Num_part = 0
            i_Total_duedate = 0
            Temp_job = Job_T()
            Temp_job.i_Total_Number_Operation = 0
            Temp_job.P = []

            for j in range(con1.Pallet_type[i].i_Num_Fixt):
                test = None
                Temp_job.P.append(Part_T())
                temp_part = con1.Dummy.head.next

                while (temp_part != con1.Dummy.tail):
                    if (temp_part.Obj.i_Terminated==0)and(temp_part.Obj.i_Fixture_type==con1.Pallet_type[i].Fixture[j].i_fixture_no)and(con1.Pallet_type[i].Fixture[j].i_rest_Fixture==1):
                        test = temp_part

                    if (test != None): #하나의 fixture에 실린게 있으면 while문을 끝내고 다른 fixture에 대한 
                        break
                    else:
                        temp_part = temp_part.next

                if test == None:
                    Temp_job.P[j] = None
                else:
                    Temp_job.P[j] = test.Obj
                    Temp_job.i_Total_Number_Operation += test.Obj.PT.i_Num_Operation
                    Temp_job.Pallet_job = con1.Pallet_type[i]
                    Num_part += 1
                    Temp_job.i_Num_parts = Num_part
                    Temp_job.i_Empty = 0 #Pallet에 part들이 올라가는것이 없으면 1
                    i_Total_duedate += test.Obj.i_Due_date
                    Temp_job.f_avg_duedate = i_Total_duedate #올라간 part들의 평균 due-date, 뒷 부분 코드에서 올라간 part의 수로 나눈다.
                    con1.Dummy.pop_it(test)
                    con1.Pallet_type[i].Fixture[j].i_rest_Fixture = 0
                    

            #if (test != None):
            if (Temp_job.i_Empty == 0): #pallet에 part들이 올라가는것이 없으면, 1
                con1.Pallet_type[i].i_rest_Pallet == 0
                con1.J[con1.Job_index].P = [None for i in range(Temp_job.Pallet_job.i_Num_Fixt)]


                for k in range(Temp_job.Pallet_job.i_Num_Fixt):
                    con1.J[con1.Job_index].P[k] = Temp_job.P[k]
                    if (con1.J[con1.Job_index].P[k] != None):
                        con1.J[con1.Job_index].P[k].i_Job_No = con1.Job_index
                        
                con1.J[con1.Job_index].Pallet_job = Temp_job.Pallet_job
                con1.J[con1.Job_index].i_Empty = Temp_job.i_Empty
                con1.J[con1.Job_index].i_Total_Number_Operation = Temp_job.i_Total_Number_Operation - (2*Temp_job.i_Num_parts)
                con1.J[con1.Job_index].i_Job_No = con1.Job_index
                con1.J[con1.Job_index].i_Num_parts = Temp_job.i_Num_parts
                con1.J[con1.Job_index].i_current_position = 0
                con1.J[con1.Job_index].i_current_state = 0
                con1.J[con1.Job_index].f_avg_duedate = Temp_job.f_avg_duedate/Temp_job.i_Num_parts

                con1.J[con1.Job_index].Part_Route = [None for i in range(con1.J[con1.Job_index].i_Total_Number_Operation+1)]
                con1.J[con1.Job_index].i_OP_Route = [None for i in range(con1.J[con1.Job_index].i_Total_Number_Operation+1)]
                con1.J[con1.Job_index].Machine_Route = [None for i in range(con1.J[con1.Job_index].i_Total_Number_Operation+1)]
                con1.J[con1.Job_index].s_Machine_Name = [None for i in range(con1.J[con1.Job_index].i_Total_Number_Operation+1)]
                con1.J[con1.Job_index].i_Processing_time = [None for i in range(con1.J[con1.Job_index].i_Total_Number_Operation+1)]

                """
                for k in range(Temp_job.Pallet_job.i_Num_Fixt):
                    if (Temp_job.P[k] != None):
                        Temp_job.P[k].i_Job_No = con1.Job_index
                Temp_job.i_Job_No = con1.Job_index
                Temp_job.i_current_position = 0
                Temp_job.i_current_state = 0
                Temp_job.f_avg_duedate = Temp_job.f_avg_duedate/Temp_job.i_Num_parts
                """
                    
                Operation_seqeuncing_option(con1.Operation_Sequence_Option, con1, con1.J[con1.Job_index])
                Initial_Mac_selection(con1, con1.J[con1.Job_index])
                Temp_job.i_TWKR = TWKR0(con1.J[con1.Job_index])
                #con1.J[con1.Job_index].i_TWKR = TWKR0(con1.J[con1.Job_index])
                #LLBuffer.push_back(Temp_job)
                #LstPallet_list.append(Temp_job)
                #con1.J[con1.Job_index] = Temp_job

                LLBuffer.push_back(con1.J[con1.Job_index])

                con1.Job_index += 1
        
        con1.Job_INDEX.i_Job_index = con1.Job_index

    l = 0

def Find_last_job(LstJL): #현재 machine의 job_sequence를 searching하여, 대기하고 있는 job 중에 processing할 job을 찾기 전에 이전에 수행할 job이 있는지 판단
    Temp = None
    Temp_job = None

    Temp = LstJL.tail.pre
    if (Temp == LstJL.head):
        Temp_job = None
    else:
        Temp_job = Temp.Obj
    return Temp_job

def Dispatching_SOPT(M, Job_queue, Time):
    min0 = 99999999
    Temp = Job_queue.head.next
    Temp_job = None
    i_Next_rest_time = M.i_Next_Rest_Time
    a = 0
    while (Temp != Job_queue.tail):
        if (Temp.Obj.i_current_state==0):
            if ((Temp.Obj.i_Processing_time[Temp.Obj.i_current_position]+Time <= i_Next_rest_time)and(Temp.Obj.Machine_Route[Temp.Obj.i_current_position]==M)and(Temp.Obj.i_Terminate!=1)):
                if (min0 > Temp.Obj.i_Processing_time[Temp.Obj.i_current_position]):
                    Temp_job = Temp.Obj
                    min0 = Temp.Obj.i_Processing_time[Temp.Obj.i_current_position]
        Temp = Temp.next
        

    if (Temp_job == None):
        return None
    else:
        return Temp_job

def Dispatching_MWKR(M, Job_queue, Time): #most remaining work
    min0 = 99999999
    Temp = Job_queue.head.next
    Temp_job = None
    i_Next_rest_time = M.i_Next_Rest_Time

    while (Temp != Job_queue.tail):

        if (Temp.Obj.i_current_state==0):
            if ((Temp.Obj.i_Processing_time[Temp.Obj.i_current_position]+Time <= i_Next_rest_time)and(Temp.Obj.Machine_Route[Temp.Obj.i_current_position]==M)and(Temp.Obj.i_Terminate!=1)):
                i_TWKR = TWKR0(Temp.Obj)
                if (min0 > i_TWKR):
                    Temp_job = Temp.Obj
                    min0 = i_TWKR
        Temp = Temp.next

    if (Temp_job == None):
        return None
    else:
        return Temp_job    


def max0(a, b):
    if (a > b):
        return a
    else:
        return b


def Dispatching_option_selection(Dispatching_Option, Mac_Temp, Job_Queue, Time):
    if (Dispatching_Option == 1):
        Job_temp = Dispatching_SOPT(Mac_Temp, Job_Queue, Time) #shortest operation processing time
    elif (Dispatching_Option == 2):
        Job_temp = Dispatching_MWKR(Mac_Temp, Job_Queue, Time) ##most remaining work
    else:
        print('Dispatching Option Error')
        return -1 
    return Job_temp

def Input_Last_to_Job_List(JL, Job): #JL --> Machine이 처리해야하는 job sequence
    JL.push_back(Job)

    JL.tail.pre.Obj2 = Job.Part_Route[Job.i_current_position]
    JL.tail.pre.operation = Job.i_OP_Route[Job.i_current_position]
    JL.tail.pre.Start_time = Job.i_Current_Process_Completion_time - Job.i_Processing_time[Job.i_current_position]
    JL.tail.pre.End_time = Job.i_Current_Process_Completion_time
    JL.tail.pre.PID = Job.Part_Route[Job.i_current_position].PT.s_PID[Job.i_OP_Route[Job.i_current_position]]

    return JL.nNodes

def Input_last_to_Machine_Sched_list(ML, M, St, Ed, Str): #현재 job의 operation position에 해당하는 part의 machine sequence(길이는 operation의 수만큼)
    ML.push_back(M)
    ML.tail.pre.Start_time = St
    ML.tail.pre.End_time = Ed
    ML.tail.pre.PID = Str

    return ML.nNodes

def Machine_selection_SW(con2, Job): #shortest work, processing time
    min0 = 99999999
    Temp_mac = con2.ML.head.next
    LstMac = []

    while (Temp_mac != con2.ML.tail):
        ML_accum_pro = 0
        for i in range(Job.Part_Route[Job.i_current_position].PT.i_Num_Alternative_Machine[Job.i_OP_Route[Job.i_current_position]]):
            
            if (Job.Part_Route[Job.i_current_position].PT.Alternative_Mac[Job.i_OP_Route[Job.i_current_position]][i] == Temp_mac.Obj):
                
                i_Proc = Job.Part_Route[Job.i_current_position].PT.i_Standard_Time[Job.i_OP_Route[Job.i_current_position]][i]
                
                Temp_job = con2.Job_queue.head.next
                while (Temp_job != con2.Job_queue.tail):
            
                    if (Temp_job.Obj.i_current_state==0):
            
                        if (Temp_job.Obj.Machine_Route[Temp_job.Obj.i_current_position]==Temp_mac.Obj)and(Temp_job.Obj.i_Terminate!=1):
            
                            ML_accum_pro += Temp_job.Obj.i_Processing_time[Temp_job.Obj.i_current_position]
            
                    Temp_job = Temp_job.next
                LstMac.append([Temp_mac.Obj, Temp_mac.Obj.i_Machine_No, Temp_mac.Obj.s_Machine_Name, ML_accum_pro, i_Proc])
        Temp_mac = Temp_mac.next

    LstMac = sorted(LstMac, key=itemgetter(3, 4))

    Job.Part_Route[Job.i_current_position].Mac_Select[Job.i_OP_Route[Job.i_current_position]] = LstMac[0][0]
    Job.Part_Route[Job.i_current_position].s_Mac_Select_name[Job.i_OP_Route[Job.i_current_position]] = LstMac[0][2]
    Job.Part_Route[Job.i_current_position].i_Mac_Select_index[Job.i_OP_Route[Job.i_current_position]] = LstMac[0][1]
    Job.Part_Route[Job.i_current_position].i_Select_Process_Time[Job.i_OP_Route[Job.i_current_position]] = LstMac[0][4]
    Job.Part_Route[Job.i_current_position].i_Total_Processing_Time += LstMac[0][4]

    Job.i_Processing_time[Job.i_current_position] = LstMac[0][4]
    Job.Machine_Route[Job.i_current_position] = LstMac[0][0]
    Job.s_Machine_Name[Job.i_current_position] = LstMac[0][2]    

    #con2.Job_INDEX.i_Machine_pro[LstMac[0][1]] += LstMac[0][4]
    #con2.Job_INDEX.machine_name[LstMac[0][1]] = LstMac[0][1]    

    return Job

def Machine_selection_SQ(con2, Job): #shortest queue, 갯수
    min0 = 99999999
    Temp_job = con2.Job_queue.head.next
    Temp_mac = con2.ML.head.next
    LstMac = []

    while (Temp_mac != con2.ML.tail):
        Waiting_pallets = 0
        if (Job.Part_Route[Job.i_current_position].PT.i_Num_Alternative_Machine[Job.i_OP_Route[Job.i_current_position]] != 0):

            for i in range(Job.Part_Route[Job.i_current_position].PT.i_Num_Alternative_Machine[Job.i_OP_Route[Job.i_current_position]]): #2 or 4

                if (Job.Part_Route[Job.i_current_position].PT.Alternative_Mac[Job.i_OP_Route[Job.i_current_position]][i] == Temp_mac.Obj):

                    i_Proc = Job.Part_Route[Job.i_current_position].PT.i_Standard_Time[Job.i_OP_Route[Job.i_current_position]][i]
                    
                    Temp_job = con2.Job_queue.head.next
                    while (Temp_job != con2.Job_queue.tail):
                        
                        if (Temp_job.Obj.i_current_state==0):
                        
                            if (Temp_job.Obj.Machine_Route[Temp_job.Obj.i_current_position]==Temp_mac.Obj)and(Temp_job.Obj.i_Terminate!=1):
                        
                                Waiting_pallets += 1
                        Temp_job = Temp_job.next
                    LstMac.append([Temp_mac.Obj, Temp_mac.Obj.i_Machine_No, Temp_mac.Obj.s_Machine_Name, Waiting_pallets, i_Proc])
        Temp_mac = Temp_mac.next        

    LstMac = sorted(LstMac, key=itemgetter(3, 4))

    Job.Part_Route[Job.i_current_position].Mac_Select[Job.i_OP_Route[Job.i_current_position]] = LstMac[0][0]
    Job.Part_Route[Job.i_current_position].i_Mac_Select_index[Job.i_OP_Route[Job.i_current_position]] = LstMac[0][1]
    Job.Part_Route[Job.i_current_position].s_Mac_Select_name[Job.i_OP_Route[Job.i_current_position]] = LstMac[0][2]
    Job.Part_Route[Job.i_current_position].i_Select_Process_Time[Job.i_OP_Route[Job.i_current_position]] = LstMac[0][4]
    Job.Part_Route[Job.i_current_position].i_Total_Processing_Time += LstMac[0][4]

    Job.i_Processing_time[Job.i_current_position] = LstMac[0][4]
    Job.Machine_Route[Job.i_current_position] = LstMac[0][0]
    Job.s_Machine_Name[Job.i_current_position] = LstMac[0][1]

    #con2.Job_INDEX.i_Machine_pro[LstMac[0][1]] += LstMac[0][4]

    return Job



def Machine_selection_option(Mac_selec_option, con2, Job):
    if (Mac_selec_option == 1):
        Job = Machine_selection_SW(con2, Job)
    if (Mac_selec_option == 2):
        Job = Machine_selection_SQ(con2, Job)
    
    return Job



def Job_completion(con2):
    Cell_job = con2.Job_queue.head.next
    while (Cell_job != con2.Job_queue.tail):
        if (Cell_job.Obj.i_Total_Number_Operation == Cell_job.Obj.i_current_position+1):
            if (Cell_job.Obj.i_Processing_time[Cell_job.Obj.i_current_position+1] == None):
                Cell_job.Obj.i_Terminate = 1

        Cell_job = Cell_job.next
        
    return 1



def Event_executer(con2, i_Time):
    i_EV = 0
    v = 0

    i_Trans = con2.i_Transportation_time
    CM_temp = con2.ML.head.next
    
    Pre_job = None #이전 job 체크해서 transportation time 추가
    Job_temp = None
    Mac_temp = None

    while (CM_temp != con2.ML.tail): #Machine마다 event 체크
        v += 1
        #print("Mac", v, "체크")
        Mac_temp = CM_temp.Obj
        #End of the vacation time in calender.
        if (Mac_temp.i_Working_or_Rest == 0) and (Mac_temp.i_Next_Working_time == i_Time):
            #현재 machine이 Rest 중이고, i_Next_Working_time(540, 1080,...)이 i_Time일 때
            Mac_temp.i_Current_Schedule += 1
            if (Mac_temp.i_Current_Schedule == Mac_temp.i_Number_Schedule):
                #현재 machine의 할당된 schedule 수를 채웠으면
                #i_Number_Schedule은 스케줄 수이다. 마지막까지 오면 machine은 계속 on 상태
                Mac_temp.i_Next_Working_time = -1
                Mac_temp.i_Next_Rest_Time = 31536000
            else:
                Mac_temp.i_Next_Working_time = -1
                Mac_temp.i_Next_Rest_Time = Mac_temp.i_Machine_Schedule[Mac_temp.i_Current_Schedule]

            Mac_temp.i_Working_or_Rest = 1 #1이면 machine 사용가능
            i_EV = 1 #(1)현재 machine이 rest 상태에 있고, i_Next_Working_time=480(1020, ...)이 현재 simulation time일 때, event +1


        #Change a machine to a vacate mode by calender.
        if (Mac_temp.i_Working_or_Rest == 1) and (Mac_temp.i_Next_Rest_Time == i_Time):
            #현재 machine이 working 중이고, i_Next_Rest_Time(480, 1020,...)이 i_Time일 때
            Mac_temp.i_Current_Schedule += 1
            if (Mac_temp.i_Current_Schedule == Mac_temp.i_Number_Schedule):
                Mac_temp.i_Next_Rest_Time = -1
                Mac_temp.i_Next_Working_time = 31536000
            else:
                Mac_temp.i_Next_Working_time = Mac_temp.i_Machine_Schedule[Mac_temp.i_Current_Schedule]
                Mac_temp.i_Next_Rest_Time = -1
            
            Mac_temp.i_Working_or_Rest = 0 #0이면 machine 사용불가
            i_EV = 1 #(2)현재 machine이 working 상태에 있고, i_Next_Rest_Time=480(1020, ...)이 현재 simulation time일 때, event +1


        #Available machine에서 dispatching rule을 이용하여 processing을 시작한다.
        if (Mac_temp.i_Current_State == 0) and (Mac_temp.i_Working_or_Rest == 1):
            #현재 machine이 비었고, working 중이어서 available할 때
            Pre_job = Find_last_job(Mac_temp.Job_Sequence)
            if (Pre_job == None):
                Job_temp = Dispatching_option_selection(con2.Dispatching_Option, Mac_temp, con2.Job_queue, i_Time)
            else:
                if (Pre_job.Machine_Route[Pre_job.i_current_position] == Mac_temp):
                    if (Pre_job.i_current_state == 0):
                        if (Mac_temp.i_End_time == i_Time):
                            Job_temp = Pre_job
                        else:
                            Job_temp = Dispatching_option_selection(con2.Dispatching_Option, Mac_temp, con2.Job_queue, i_Time)
                    else:
                        Job_temp = Dispatching_option_selection(con2.Dispatching_Option, Mac_temp, con2.Job_queue, i_Time)
                else:
                    Job_temp = Dispatching_option_selection(con2.Dispatching_Option, Mac_temp, con2.Job_queue, i_Time)


            #Dispatching rule을 이용하여 job(Job_temp)이 선택되었으니, processing을 시작한다.
            if (Job_temp != None):
                #if (Pre_job != None):
                #    print("Pre_job: 앞서 완료된 job define.")

                #Job(pallet) 입장에서 시간 속성값들 추가
                if (Pre_job == Job_temp):
                    if (Mac_temp.i_End_time == i_Time): #현재 machine이 방금 끝나야한다. 이전에 끝났던 machine이 쉬다가 다시 똑같은 job을 받을 경우에는 이동시간이 추가되어야한다.
                        Job_temp.i_Current_Process_Completion_time = i_Time + Job_temp.i_Processing_time[Job_temp.i_current_position] #한 machine에 같은 job이 들어오면 trans 제외한다.
                    else: #현재 machine에서 같은 job을 처리한다카더라도 한참 뒤에 같은 job을 처리하는 경우는 trans를 더해준다.
                        Job_temp.i_Current_Process_Completion_time = i_Time + i_Trans + Job_temp.i_Processing_time[Job_temp.i_current_position]
                else: #이전 job과 현재 선택된 job이 다를 경우
                    Job_temp.i_Current_Process_Completion_time = i_Time + i_Trans + Job_temp.i_Processing_time[Job_temp.i_current_position]

                Input_Last_to_Job_List(Mac_temp.Job_Sequence, Job_temp) #Machine 측면에서 J의 part까지 받는다
                Mac_temp.i_Current_State = 1 #Machine이 process 중이다.
                Mac_temp.i_Current_Job_Start_Time = i_Time

                #Machine 입장에서 시간 속성값들 추가
                if (Pre_job == Job_temp):
                    if (Mac_temp.i_End_time == i_Time):
                        Mac_temp.i_Current_Job_End_Time = i_Time + Job_temp.i_Processing_time[Job_temp.i_current_position]
                        Mac_temp.i_End_time = i_Time + Job_temp.i_Processing_time[Job_temp.i_current_position]
                    else:
                        Mac_temp.i_Current_Job_End_Time = i_Time + i_Trans + Job_temp.i_Processing_time[Job_temp.i_current_position]
                        Mac_temp.i_End_time = i_Time + i_Trans + Job_temp.i_Processing_time[Job_temp.i_current_position]
                else:
                    Mac_temp.i_Current_Job_End_Time = i_Time + i_Trans + Job_temp.i_Processing_time[Job_temp.i_current_position]
                    Mac_temp.i_End_time = i_Time + i_Trans + Job_temp.i_Processing_time[Job_temp.i_current_position]
                    
                Mac_temp.i_Current_Part_ID = Job_temp.Part_Route[Job_temp.i_current_position].PT.i_Job_ID #현재 machine이 process 중인 part type
                Mac_temp.i_Current_Part_No = Job_temp.Part_Route[Job_temp.i_current_position].i_Part_No #현재 machinedl process 중인 part 번호
                Mac_temp.i_Current_Job_No = Job_temp.i_Job_No

                con2.Job_INDEX.i_Last_processing_time = Job_temp.i_Processing_time[Job_temp.i_current_position]

                Input_last_to_Machine_Sched_list(Job_temp.Part_Route[Job_temp.i_current_position].Machine_Sequence, Mac_temp, Mac_temp.i_Current_Job_Start_Time, Mac_temp.i_Current_Job_End_Time, Job_temp.Part_Route[Job_temp.i_current_position].PT.s_PID[Job_temp.i_OP_Route[Job_temp.i_current_position]])
                # -->Part 측면에서 machine이랑 시간 받는다.
                
                temp = None
                temp = Job_temp.Part_Route[Job_temp.i_current_position].Machine_Sequence.tail.pre
                
                #Job_temp.i_TWKR = Job_temp.i_TWKR - Job_temp.i_Processing_time[Job_temp.i_current_position]
                
                Job_temp.i_current_position += 1 #선택된 job의 position을 1만큼 증가시킨다.
                Job_temp.i_current_state = 1 #Process중이다.
                
                #Job_temp = Machine_selection_option(con2.Machine_Selection_Option, con2, Job_temp) #끝난 operation의 다음 operation에 대한 machine selection

                l = 0
                i_EV = 1 #(3)현재 machine이 processing을 시작해서, 이에 대한 정보를 넣을 때, event +1


    #while (CM_temp != con2.ML.tail):
        if (Mac_temp.i_Current_Job_End_Time == i_Time): #Machine이 processing을 완료, 동시에 다음 operation에 대한 machine selection 진행
            Mac_temp.i_Current_Part_ID = -1
            Mac_temp.i_Current_Part_No = -1
            Mac_temp.i_Current_Job_No = -1
            Mac_temp.i_Current_Job_End_Time = -1
            Mac_temp.i_Current_Job_Start_Time = -1
            Mac_temp.i_Current_State = 0 #현재 Machine이 사용가능으로 바뀐다.

            Job_temp = Mac_temp.Job_Sequence.tail.pre.Obj
            Job_temp.i_current_state = 0

            if (Job_temp.i_Total_Number_Operation != Job_temp.i_current_position):
                Job_temp = Machine_selection_option(con2.Machine_Selection_Option, con2, Job_temp)
                # --> 끝난 operation의 다음 operation에 대한 machine selection

            #Job_temp.i_current_state = 0

            #Cell_mac = None
            if (Job_temp.Part_Route[Job_temp.i_current_position-1].i_Terminated == 1):

                Cell_mac = Job_temp.Part_Route[Job_temp.i_current_position-1].Machine_Sequence.head.next
                while (Cell_mac.next != Job_temp.Part_Route[Job_temp.i_current_position-1].Machine_Sequence.tail):
                    
                    Cell_mac = Cell_mac.next

                Job_temp.Part_Route[Job_temp.i_current_position-1].i_completion_time = Cell_mac.Obj.i_End_time ##현재 part의 종료시간
                Job_temp.i_Completion_time = Cell_mac.Obj.i_End_time #Job의 종료시간. 계속해서 update 됨 . part들의 종료시간중에 하나가 job의 종료시간임
            
            i_EV = 1 #(4)현재 machine이 processing 하던 것을 완료했을 때, event +1
        CM_temp = CM_temp.next



    #Job이 완료됨에 따라 Terminate 변수 증가시킨다.
    Cell_job = con2.Job_queue.head.next
    while (Cell_job != con2.Job_queue.tail):
        if (Cell_job.Obj.i_Total_Number_Operation == Cell_job.Obj.i_current_position+1):
            if (Cell_job.Obj.i_Processing_time[Cell_job.Obj.i_current_position+1] == None):
                Cell_job.Obj.i_Terminate = 1
                i_EV = 1 #(5)현재 job(pallet) 내 모든 operation의 processing을 완료했을 때, event +1
        Cell_job = Cell_job.next


    #Dummy Processing - stack to as/rs station
    b = 0 #Check용
    Cell_job = con2.Job_queue.head.next
    while (Cell_job != con2.Job_queue.tail): #Job이 끝나면 job_queue(buffer)에서 제거해준다.
        
        if (Cell_job.Obj.i_Terminate == 1):
            Cell_job.Obj.Pallet_job.i_rest_Pallet = 1 #완료된 job(pallet)은 사용가능하다.
            
            for i in range(Cell_job.Obj.Pallet_job.i_Num_Fixt):
                Cell_job.Obj.Pallet_job.Fixture[i].i_rest_Fixture = 1 #완료된 Fixture는 사용가능하다.

            for i in range(Cell_job.Obj.Pallet_job.i_Num_Fixt):
                if (Cell_job.Obj.P[i] != None): #Loading쪽을 보면 test = None으로 할당될 수 있기 때문에, None이 아닐때로 조건문건거다.
                    Cell_job.Obj.P[i].i_Terminated = 1
                    con2.Dummy.push_back(Cell_job.Obj.P[i])
                    #Job이 다 끝났다면, loading되어 있던 P도 완료된 것이므로 dummy로 간다. Pallet에 올라가지 못했던 part들 뒤로 쌓인다고 생각하면 된다.
                    #결국, Setup station쪽으로 모인다고 생각하면 된다.

            con2.Job_queue.pop_it(Cell_job)
            Cell_job = con2.Job_queue.head.next

            i_EV = 1 #(6)현재 job이 완료됐다면, 해당 job(pallet)에 loading되어 있는 part를 dummy(Linked List)의 뒷 쪽으로 쌓는다, event +1
            continue
        Cell_job = Cell_job.next
    

    a = 0 #Check용
    CJ_temp = con2.Dummy.head.next
    while (CJ_temp != con2.Dummy.tail):
        i_Next_part = 99999999 #-> Repalletizing할 때 필요하다.
        if (CJ_temp.Obj.i_Terminated == 1): #끝났으면 빠져 나가고 삭제
            if (con2.J[CJ_temp.Obj.i_Job_No].i_Completion_time == i_Time):
                #if (con2.CJ_temp.Obj.PT.i_Pre_part == -1):
                #    i_Next_part = con2.CJ_temp.Obj.PT.i_Job_ID
                #    due = CJ_temp.Obj.i_Due_date
                #    temp_loading = con2.System.head.next
                #    while (temp_loading != con2.System.tail):
                con2.Dummy.pop_it(CJ_temp)
                CJ_temp = con2.Dummy.head.next
                i_EV = 1 #(7)Dummy에서 완료된 part들은 빼는 것이다, event +1
                continue
        CJ_temp = CJ_temp.next

    
    i_Check = con2.Job_INDEX.i_Job_index
    if (con2.Dummy.nNodes != 0):
        Loading(con2)
        if (i_Check != con2.Job_INDEX.i_Job_index):
            i_EV = 1 #(8)남은 parts loading, event +1

    l = 0
    return i_EV


def Simulation_start(con1):
    i_Simulation_time = 0
    Terminated = 0

    while True:
        event = 1
        while (event != 0):
            event = Event_executer(con1, i_Simulation_time)
            if (event == -1):
                return -1
        i_Simulation_time += 1 #Time이 증가하면 event가 없다는 뜻이다.
        #print(i_Simulation_time)
        #print(Terminated)

        l = 0
        Terminated = 0
        for i in range(con1.i_Num_Parts):
            Terminated += con1.P[i].i_Terminated

        l = 0
        """
        for i in range(con1.i_Num_Parts):
            if (con1.P[i].i_Terminated != 1):
                print("제거되지 않은 part:", con1.P[i].i_Part_index)
                print('Fixture type:', con1.P[i].i_Fixture_type)
        """
        
        if (con1.i_Num_Parts == Terminated): #모든 part에 대한 공정이 끝났으면 simulation을 종료한다.
            break
        
        l = 0
    
    l = 0
    return i_Simulation_time


def Main():
    finName = 'practice_data.txt'
    #finName = sys.argv[5]
    #finName = sys.argv[1] #1부터 시작
    fin = open(finName, 'r')

    foutName = 're.txt'
    #foutName = sys.argv[2]
    fout = open(foutName, 'w')

    #python my_cf.py 1 1 1 1 input.txt re.txt
    #RuleCombi1 = [Input_Sequence_Option(2), Operation_Sequence_Option(2), Machine_Selection_Option(3), Dispatching_Option(5)]
    #RuleCombi1 = [int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])]
    #RuleCombi1 = [int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])]
    RuleCombi1 = [1, 1, 1, 1]
    #argvLst = []

    Begin = time.time()

    con0 = con(RuleCombi1, fin, fout)
    load = Loading(con0)
    Completion_Time = Simulation_start(con0)    #event_Executer
    Completion_Time = Completion_Time + con0.Job_INDEX.i_Last_processing_time + con0.i_Transportation_time
    #print("Completion_Time:", Completion_Time)

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
        l = 0
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

    l = 0
    i_Num_operations = 0
    for i in range(con0.i_Num_Parts):
        i_Num_operations += con0.P[i].PT.i_demand * (con0.P[i].PT.i_Num_Operation - 2)

    Extract_attribute = str(Completion_Time), ' ', str(con0.i_Num_Parts), ' ', str(i_Num_operations), '\n'
    #Extract_RuleCombi = sys.argv[3], ' ', sys.argv[4], ' ', sys.argv[5], ' ', sys.argv[6]
    FileWrite(fout, Extract_attribute)
    #FileWrite(fout, Extract_RuleCombi)
    #print(tardy)


    return 0
    #print(iDuration)
    
Main()