import os
from MDStep import MDStep
from Atom import Atom
from CalcPos import calcPosition, calcLattice, prodeceXYZtoPridict, calcVelocity
from gap_fit import gap_fit, preditct, rms_dict
from abacus_md import abacusMd, createSTRU, parseAtoms, createRestartFile
from MDDumpConvertXYZ import parseXYZ, parseMDDump, produceXYZtoTrain
import numpy as np
from datetime import datetime
def getInitialData():
    steps = parseMDDump('./1step/TiNB/OUT.ABACUS/MD_dump')
    traindataFilePath = './XYZ/initial10Steps.xyz'
    produceXYZtoTrain(traindataFilePath, steps)
    gap_fit('./GAP_SOAP.xml', traindataFilePath)
    with open('./on-the-fly_RunTime_log', 'w') as f:
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'initial fit done at {formatted_time}\n')
    return steps
    
def refit(steps):
    n = len(steps)
    traindataFilePath = f'./XYZ/refit_{n}steps.xyz'
    print(traindataFilePath)
    gap_fit('./ttttGAP_SOAP.xml', traindataFilePath)
    with open('./on-the-fly_RunTime_log', 'w') as f:
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'refit done at {formatted_time}\n')

def getRMSE(AabcusStep, GapStep):
    ref = []
    pred = []
    for i in range(len(AabcusStep.atoms)):
        refi = []
        predi = []
        for j in range(3):
            refi.append(AabcusStep.atoms[i].forces[j])
            predi.append(GapStep.atoms[i].forces[j])
        ref.append(refi)
        pred.append(predi)
    dict = rms_dict(ref, pred)
    rmse_text ='step_' + AabcusStep.MDIndex + ' RMSE:\n' + str(np.round(dict['rmse'], 3)) + ' +- ' + str(np.round(dict['std'], 3)) + 'eV/Å\n'
    print(rmse_text)
    with open('./on-the-fly_RunTime_log', 'w') as f:
        f.write(rmse_text)
    return dict['rmse']
def onthefly(sumSteps, abacusCheckInterval):
    steps = getInitialData()
    print('onthefly')
    print('-----------------------------')

    thisStep = steps[-1]
    latticeSaveStep = steps[0]
    count = 0
    for i in range(sumSteps):
        count +=1
        if count==abacusCheckInterval:
            count = 0
            #根据thisStep的信息构造出STRU
            workDir = createSTRU(thisStep)
            createRestartFile(thisStep, workDir)
            abacusMd('', workDir)
            with open('./on-the-fly_RunTime_log', 'w') as f:
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f'abacus step {thisStep.MDIndex} done at {formatted_time}\n')
            mdSteps = parseMDDump(os.path.join(workDir, 'OUT.ABACUS/MD_dump'))
            abacusStep = mdSteps[0]
            steps[-1] = abacusStep
            rmse = getRMSE(abacusStep, thisStep)
            if rmse > 1:
                refit(steps)
                with open('./on-the-fly_RunTime_log', 'w') as f:
                    f.write(f'refit at {steps[-1].MDIndex}\n')

        nextStep = MDStep(str(int(thisStep.MDIndex) + 1))
        calcLattice(latticeSaveStep, nextStep)
        calcPosition(thisStep, nextStep)
        XYZFilePath = prodeceXYZtoPridict(nextStep)
        resultFileName = 'step_' + str(nextStep.MDIndex) + '.xyz'
        resultFilePath = os.path.join('./XYZ/PredictResult/', resultFileName)
        preditct('./GAP_SOAP.xml', XYZFilePath, resultFilePath)
        with open('./on-the-fly_RunTime_log', 'w') as f:
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f'GAP predict step {thisStep.MDIndex} done at {formatted_time}\n')
        print('-----------------------------')
        nextStep = parseXYZ(resultFilePath, int(nextStep.MDIndex)) #重新读取包含预测力的nextstep
        calcVelocity(thisStep, nextStep)
        thisStep = nextStep
        steps.append(thisStep)
        
onthefly(500,10)

# mdSteps = parseMDDump(os.path.join('./1step/TiNB/abacus_step_16', 'OUT.ABACUS/MD_dump'))
# AabcusStep = mdSteps[0]
# GapStep = parseXYZ('./XYZ/PredictResult/step_16.xyz', 16)
# def tttgetRMSE(AabcusStep, GapStep):
#     ref = []
#     pred = []
#     for i in range(len(AabcusStep.atoms)):
#         refi = []
#         predi = []
#         for j in range(3):
#             refi.append(AabcusStep.atoms[i].forces[j])
#             predi.append(GapStep.atoms[i].forces[j])
#         ref.append(refi)
#         pred.append(predi)
#     dict = rms_dict(ref, pred)
#     rmse_text = 'step_' + AabcusStep.MDIndex + ' RMSE:\n' + str(np.round(dict['rmse'], 3)) + ' +- ' + str(np.round(dict['std'], 3)) + 'eV/Å'
#     print(rmse_text)
#     return dict['rmse']

# tttgetRMSE(AabcusStep, GapStep)