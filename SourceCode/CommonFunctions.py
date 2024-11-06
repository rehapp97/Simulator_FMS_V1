# Common Functions ; 전역변수
import copy
import os #shell cmd run
import sys #argc, argv
import re
#import numpy as np

sepSp = " "

def FileWrite (fout, str1):
    #str1 = str1 + '\n'#줄바꿈
    fout.writelines(str1)
    
def FileWriteN (fout, str1):
    str1 = str1 + '\n' #줄바꿈
    fout.writelines(str1)

def StrListTo_intList(strLst1):
    strLst2 = list(map(str.strip, strLst1))
    strLst2.remove('')
    #print(strLst2)
    iList1 = list(map(int, strLst2))
    return iList1    

def StrListTo_intList1(strLst1):
    strLst2 = list(map(str.strip, strLst1))
    #print(strLst2)
    iList1 = list(map(int, strLst2))
    return iList1    

def StrListTo_floatList(strLst1):
    strLst2 = list(map(str.strip, strLst1))
    strLst2.remove('')
    #print(strLst2)
    #fList1 = np.array(strLst2, dtype=float)
    fList1 = list(map(float, strLst2))
    return fList1    

#import re
def StrTo_intList(str1):
    #strLst1 = str1.strip().split(' ')
    str2 = " ".join(re.split("\s+", str1.strip(), flags=re.UNICODE))
    strLst1 = str2.strip().split(' ')
    #print(strLst1)
    iList1 = list(map(int, strLst1))
    return iList1

def StrTo_intList1(str1):
    strLst1 = []
    for i in range(len(str1)):
        strLst1.append(int(str1[i]))
    #strLst1 = str1.strip().split(' ')
    iList1 = list(map(int, strLst1))
    return iList1

def intListToStrList(iList1):
    sList1 = list(map(str, iList1))
    return sList1

def intListToStr(iList1):
    sList1 = list(map(str, iList1))
    str1 = ' '.join(sList1)
    return str1

def intListToStr0(iList1):
    sList1 = list(map(str, iList1))
    str1 = ''.join(sList1)
    return str1

def iList1D(Len0):# int
    List0 = [0 for i in range(Len0)]
    return List0

def iList1D_init(Len0, init):# int, init value
    List0 = [init for i in range(Len0)]
    return List0

def iList2D(Len1, Len2):# int, int
    List0 = []
    for i in range(Len1):
        LTmp0 = []
        for j in range(Len2):
            LTmp0.append(0)
        List0.append(LTmp0)
    return List0

def iList2D_init(Len1, Len2, init):# int, int, init value
    List0 = []
    for i in range(Len1):
        LTmp0 = []
        for j in range(Len2):
            LTmp0.append(init)
        List0.append(LTmp0)
    return List0


def iList2Dfree(Len1, Len2s):# int, int_list
    List0 = []
    for i in range(Len1):
        LTmp0 = []
        for j in range(Len2s[i]):
            LTmp0.append(0)
        List0.append(LTmp0)
    return List0

def iList2Dfree_init(Len1, Len2s, init):# int, int_list, init value
    List0 = []
    for i in range(Len1):
        LTmp0 = []
        for j in range(Len2s[i]):
            LTmp0.append(init)
        List0.append(LTmp0)
    return List0

def StrList_toStr(List): 
    return ' '.join(List) 

def FindLstValuePosition(Lst0, value0):
    RetLst1 = [i for i, value in enumerate(Lst0) if value == value0]
    return RetLst1

def Lst2DcolSortMain(Lst_in, idxLst0):#+:Asc, -:Desc, 0:NoSort; input Real_idx+1 
    iR = len(Lst_in[0])
    iC = len(Lst_in)
    #idxLen = len(idxLst0)
    idxTmp1 = -1
    AD_Tmp1 = 0
    idxLst1 = []
    ADLst1 = []
    
    if ((iC > 1) and (iR > 0)):
        for Lidx in idxLst0:
            idxTmp1 = (-Lidx-1) if Lidx < 0 else (Lidx-1)
            idxLst1.append(idxTmp1)
            AD_Tmp1 = -1 if Lidx < 0 else 1 if Lidx > 0 else 0#1:Ascend, -1:Descend, 0:NoSort
            ADLst1.append(AD_Tmp1)
        #for Lidx

        #Lst_in.sort(key = lambda Lin: (ADLst1[0]*Lin[idxLst1[0]], ADLst1[1]*Lin[idxLst1[1]], ADLst1[2]*Lin[idxLst1[2]]))#len 3 case
        Lst_in.sort(key = lambda Lin: tuple(map(lambda AD, idx: AD*Lin[idx], ADLst1, idxLst1)))
    else:
        print('Error in sortLst2DcolMain: Short input List')
    #if ((iC > 1)
def Lst2DcolSort3(Lst_in, idx01, idx02, idx03):#+:Asc, -:Desc; input Real_idx+1 
    iLstTmp1 = [idx01, idx02, idx03]
    Lst2DcolSortMain(Lst_in, iLstTmp1)
def Lst2DcolSort2(Lst_in, idx01, idx02):#+:Asc, -:Desc; input Real_idx+1 
    iLstTmp1 = [idx01, idx02]
    Lst2DcolSortMain(Lst_in, iLstTmp1)
def Lst2DcolSort1(Lst_in, idx01):#+:Asc, -:Desc; input Real_idx+1 
    iLstTmp1 = [idx01]
    Lst2DcolSortMain(Lst_in, iLstTmp1)

def Lst2DcolAddOrderAllMain(Lst_in, idx0, startNum):#idx0 (+:Asc, -:Desc; input Real_idx+1)
    #LenLst1 = len(Lst_in)
    idxTmp1 = -1
    i1 = startNum
    if idx0 > -1:#>=0 Asc
        idxTmp1 = (idx0-1) if idx0 > 0 else 0
        for El in Lst_in:
            El[idxTmp1] = i1
            i1 += 1
        #for El
    else:#<0 Desc
        idxTmp1 = -idx0-1
        for El in reversed(Lst_in):
            El[idxTmp1] = i1
            i1 += 1
        #for El
    #if idx0 > -1

def Lst2DcolAddOrderAll0Main(Lst_in, idx0, startNum, idxComp0):#idx0 (+:Asc, -:Desc; input Real_idx+1); idxComp0(Real_idx)
    #same order prints : 123456 -> 122446
    ElBefore = 0
    idxTmp1 = -1
    i1 = startNum
    i2 = startNum
    if idx0 > -1:#>=0 Asc
        idxTmp1 = (idx0-1) if idx0 > 0 else 0
        for El in Lst_in:
            if (i1 == startNum): i2 = i1
            else: 
                if (ElBefore != El[idxComp0]) and (i1 != i2): i2 = i1
            #if
            El[idxTmp1] = i2
            ElBefore = El[idxComp0]
            i1 += 1
        #for El
    else:#<0 Desc
        idxTmp1 = -idx0-1
        for El in reversed(Lst_in):
            if (i1 == startNum): i2 = i1
            else:
                if (ElBefore != El[idxComp0]) and (i1 != i2): i2 = i1
            #if
            El[idxTmp1] = i2
            ElBefore = El[idxComp0]
            i1 += 1
        #for El
    #if idx0 > -1

def Lst2DcolExt(Lst_in):
    i1 = 0
    for El in Lst_in:
        #El.extend(i1)#error
        El.append(i1)
        i1 += 1
    #for El

def Lst2DrowValUpdate(Lst2D_in, Lst1D_in, idx0):
    for i, El in enumerate(Lst2D_in):
        El[idx0] = Lst1D_in[i]
    #for El

def Lst2DrowValAdd(Lst2D_in, Lst1D_in, idx0):
    for i, El in enumerate(Lst2D_in):
        El[idx0] += Lst1D_in[i]
    #for El

def Lst2DrowRetLst(Lst2D_in, idx0):
    #iLstRet = []
    iLstRet = list(map(lambda El1: El1[idx0], Lst2D_in))
    return iLstRet

def Lst2DrowMinVal(Lst2D_in, idx0):
    RetVal = 0
    LstTmp1 = Lst2DrowRetLst(Lst2D_in, idx0)
    RetVal = min(LstTmp1)
    return RetVal

def Lst2DrowMaxVal(Lst2D_in, idx0):
    RetVal = 0
    LstTmp1 = Lst2DrowRetLst(Lst2D_in, idx0)
    RetVal = max(LstTmp1)
    return RetVal

def Lst2DchgRC(Lst2D_in):
    iLstRet = []
    for i1 in range(len(Lst2D_in[0])):
        iLstRet.append(Lst2DrowRetLst(Lst2D_in, i1))
    #for i1
    return iLstRet

def FprtLst2D(fout0, Lst2Din0):
    r1 = len(Lst2Din0)
    c1 = len(Lst2Din0[0])
    strTmp1 = ''
    strTmp2 = ''
    for r in range(r1):
        for c in range(c1):
            strTmp2 = '\n' if (c == (c1 - 1)) else sepSp
            strTmp1 = str(Lst2Din0[r][c]) + strTmp2
            FileWrite(fout0, strTmp1)
        #for c
    #for r
    FileWriteN(fout0, sepSp)
#def FprtLst2D

#import copy
def DeepCopyObj(ObjFrom):
    ObjTmp = copy.deepcopy(ObjFrom)
    return ObjTmp

#import os
def RunShellCmd(CmdStr0):
    os.system(CmdStr0)
    print(CmdStr0)

#
#=====================================================================================================
