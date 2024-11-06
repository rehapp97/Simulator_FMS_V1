# Common variables ; 전역변수
import copy
import os
import re
#import numpy as np

sepSp = " "

def FileWrite (fout, str1):
    #str1 = str1 + '\n'#줄바꿈
    fout.writelines(str1)
    
def FileWriteN (fout, str1):
    str1 = str1 + '\n'#줄바꿈
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

#import copy
def DeepCopyObj(ObjFrom):
    ObjTmp = copy.deepcopy(ObjFrom)
    return ObjTmp

#import os
def RunShellCmd(CmdStr0):
    os.system(CmdStr0)
    print(CmdStr0)