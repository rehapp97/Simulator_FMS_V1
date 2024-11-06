import random
import re
import sys
import itertools

def FileWrite(Input_File0, str0):
    str0 = str0 + '\n'
    Input_File0.writelines(str0)

def intList_to_write(Input_File0, intList):
    strList = " ".join(map(str, intList))
    strList = strList + '\n'
    Input_File0.writelines(strList)

def CombiGen():
    CombiTxt = open('RuleCombi.txt', 'w')

    Palletizing = [1]
    Operation_sequencing = [1, 2]
    Machine_selection = [1, 2]
    Pallet_process_sequencing = [1, 2]

    LstCombi = list(itertools.product(*[Palletizing, Operation_sequencing, Machine_selection, Pallet_process_sequencing]))
    print(len(LstCombi))

    for i in range(len(LstCombi)):
        intList_to_write(CombiTxt, LstCombi[i])

CombiGen()
