import os
import csv

path0 = 'D:/MY_Documents/Python Scripts/AdvSimulator4/AdvSimulator4/Result0'

LstFile = os.listdir(path0)

foutName = 'ConferExperiment.csv'
fout = open(foutName, 'w', encoding='utf-8', newline='')
foutW = csv.writer(fout)
#print(LstFile)
#finName = LstFile[0].strip().split('.')
#print(finName)

#a = LstFile[0].strip().split('_')
#print(a)

Header_in = "./Result0/"

for i in range(len(LstFile)):
    finName = LstFile[i]
    LstAttribute = finName.strip().split('_')
    i_Num_mac = LstAttribute[1]
    i_Num_parttype = LstAttribute[2]
    i_Num_fixt = LstAttribute[4]

    EnvCombiName = finName.strip().split('.')
    EnvCombiName0 = EnvCombiName[0]

    fin = open(Header_in + finName, 'r')

    fin0 = fin.readline().split()
    print(fin0)
    makespan = fin0[0]
    i_Num_parts = fin0[1]
    fin2 = fin.readline().split()

    foutW.writerow([finName, EnvCombiName0, i_Num_mac, i_Num_parttype, i_Num_fixt, i_Num_parts, makespan, fin2])
