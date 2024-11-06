from CommonFunctions import *

def BatchGen1(EnvCombi0, RuleCombi0):
    ExeFilename = 'AdvFunction01.py'
    #Header_in = "./Input/"
    Header_in = "./Input_confer/"
    #Header_out = "./Result/"
    Header_out = "./Result_confer/"
    Tail = ".txt "
    
    finEC = open(EnvCombi0, 'r')
    finRC = open(RuleCombi0, 'r')
    StrLstEC1 = EnvCombi0.strip().split('.')
    BatchFileName = StrLstEC1[0]+'-Batch.txt'
    print(BatchFileName)
    foutBat = open(BatchFileName, 'w')

    LstEC = finEC.readlines()
    LstRC = finRC.readlines()

    finEC.close()
    finRC.close()
    
    path0 = '.\\BatchGen\\BatFile\\'

    for EC1 in LstEC:
        StrLstEC1 = EC1.strip().split('_')
        StrEC1 = '_'.join(StrLstEC1[1:])
        #ResultECName = 're_'+StrEC1
        #print(ResultECName)
        inst = 0
        for RC1 in LstRC:
            inst += 1
            LstStrRC = RC1.strip().split(' ')
            #print(LstStrRC)
            #PrtStr1 = ExeFilename + sepSp + Header_in + 'Instance_' + StrEC1 + Tail + Header_out + 're_' + StrEC1 + '_' + str(inst) + Tail + LstStrRC[0] + sepSp + LstStrRC[1] + sepSp + LstStrRC[2] +sepSp + LstStrRC[3]
            PrtStr1 = 'python' + sepSp + ExeFilename + sepSp + Header_in + 'Instance_' + StrEC1 + Tail + Header_out + 're_' + StrEC1 + '_' + LstStrRC[0] + '_' + LstStrRC[1] + '_' + LstStrRC[2] + '_' + LstStrRC[3] + Tail + LstStrRC[0] + sepSp + LstStrRC[1] + sepSp + LstStrRC[2] +sepSp + LstStrRC[3]
            #print(PrtStr1)
            FileWriteN(foutBat, PrtStr1)
        #for RC1
    #for EC1

    foutBat.close()
#def BatchGen1

#BatchGen1('EnvCombi-SmallLUL.txt', 'RuleCombi.txt')
#BatchGen1('EnvCombi-ConferTight.txt', 'RuleCombi.txt')
#BatchGen1('EnvCombi-Defense-test.txt', 'RuleCombi.txt')
BatchGen1('EnvCombi-confer.txt', 'RuleCombi.txt')