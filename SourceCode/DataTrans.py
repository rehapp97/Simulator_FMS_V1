from AdvStructure import *
from AdvConfig01 import Config_T as con
from CommonFunctions import *
import sys
import csv

def Data_Transform():
    finName = 'Practice.csv'
    fin = open(finName, 'r', encoding='utf-8')
    finSep = finName.split('.')

    foutName = finSep[0] + '_' + 'trans' + '.csv'
    fout = open(foutName, 'w', encoding='utf-8', newline='')

    finR = csv.reader(fin)
    foutW = csv.writer(fout)

    for i in finR[1:]:
        print(i)


Data_Transform()

