import random
import re
import sys
import itertools
import os
import csv

def FileWrite(Input_File0, str0):
    str0 = str0 + '\n'
    Input_File0.writelines(str0)

def intList_to_write(Input_File0, intList):
    strList = " ".join(map(str, intList))
    strList = strList + '\n'
    Input_File0.writelines(strList)

path0 = 'D:/MY_Documents/Python Scripts/AdvSimulator4/AdvSimulator4/Input_confer'
LstFile = os.listdir(path0)

foutName = 'EnvCombi-confer.txt'
fout = open(foutName, 'w')

for i in range(len(LstFile)):
    Env = LstFile[i].strip().split('.')
    Env = Env[0]
    FileWrite(fout, Env)
