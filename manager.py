import os
from MDStep import MDStep
from Atom import Atom
from CalcPos import calcPosition, calcLattice, prodeceXYZtoPridict, calcVelocity
from gap_fit import gap_fit, preditct
from abacus_md import abacusMd, createSTRU, parseAtoms
from MDDumpConvertXYZ import parseXYZ, parseMDDump, produceXYZtoTrain
def getInitialData():
    steps = parseMDDump('./1step/TiNB/OUT.ABACUS/MD_dump')
    
    traindataFilePath = './XYZ/initial10Steps.xyz'
    produceXYZtoTrain(traindataFilePath, steps)
    gap_fit('./GAP_SOAP.xml', traindataFilePath)
    return steps
    
def onthefly(sumSteps, abacusCheckInterval):
    steps = getInitialData()
    print('-----------------------------')
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
            abacusMd('', workDir)

        nextStep = MDStep(str(int(thisStep.MDIndex) + 1))
        calcLattice(latticeSaveStep, nextStep)
        calcPosition(thisStep, nextStep)
        XYZFilePath = prodeceXYZtoPridict(nextStep)
        resultFileName = 'step_' + str(nextStep.MDIndex) + '.xyz'
        resultFilePath = os.path.join('./XYZ/PredictResult/', resultFileName)
        preditct('./GAP_SOAP.xml', XYZFilePath, resultFilePath)
        print('predict end')
        print('-----------------------------')
        nextStep = parseXYZ(resultFilePath, int(nextStep.MDIndex)) #重新读取包含预测力的nextstep
        calcVelocity(thisStep, nextStep)
        thisStep = nextStep
        
onthefly(10,1)


