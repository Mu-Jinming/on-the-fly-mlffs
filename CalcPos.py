from Atom import Atom

from MDStep import MDStep
from MDDumpConvertXYZ import parseMDDump

def verlet(current_position, dt, current_velocity, current_acceleration):
    next_position = current_position + current_velocity * dt + 0.5 * current_acceleration * dt**2
    return next_position

def calcPosition(thisStep: MDStep, nextStep: MDStep):
    print('Calculating Position')
    for thisStepAtom in thisStep.atoms:
        nextStepAtom = Atom(thisStepAtom.specie)
        for i in range(3):
            #首先计算出第i步的加速度$a_i$，查表得到原子质量m，故$a_i$=$F_i/m$
            # print(thisStepAtom.forces[i])
            if (len(thisStepAtom.acceleration) <= 3):
                thisStepAtom.acceleration.append(thisStepAtom.forces[i] / thisStepAtom.mass )
            #再第i+1步的原子坐标：$\mathbf{r_{i+1}} = \mathbf{r}_i + \mathbf{v}_i \Delta t + \frac{1}{2} \mathbf{a}_i (\Delta t)^2 $
            nextStepAtom.positons.append(verlet(thisStepAtom.positons[i], thisStep.deltaT, thisStepAtom.velocity[i], thisStepAtom.acceleration[i]))

        nextStep.atoms.append(nextStepAtom)

def calcLattice(thisStep: MDStep, nextStep: MDStep):
    print('Calculating Lattice')
    #根据第i步的晶胞参数，计算第i+1步的晶胞参数
    #TODO:
def prodeceXYZtoPridict():
    print('prodeceXYZtoPridict')
    #根据nextStep中第i+1步的坐标，生成xyz文件，用于quip预测
    #TODO:

def calcVelocity(thisStep: MDStep, nextStep: MDStep):
    print('Calculating Velocity')
    #需使用abacus或者gap得到第i+1步的力之后，再使用此函数计算第i+1步的速度
    #求出第i+1步的速度$\mathbf{{v}_{i+1}} = \mathbf{{v}_i} + \frac{1}{2} (\mathbf{a_i} + \mathbf {a_{i+1}}) \Delta t $
    for j in range(nextStep.atoms):
        nextStepAtom = nextStep.atoms[j]
        thisStepAtom = thisStep.atoms[j]
        for i in range(3):
            #先算出第i+1步的加速度
            nextStepAtom.acceleration.append(nextStepAtom.forces[i] / nextStepAtom.mass)
            #再算出第i+1步的速度
            nextStepAtom.velocity.append(thisStepAtom.velocity[i] + 0.5 * (thisStepAtom.acceleration[i] + nextStepAtom.acceleration[i]) * thisStep.deltaT)

def test():
    MDSteps = parseMDDump('./MD_dump')
    thisStep = MDSteps[-1]
    nextIndex = int(thisStep.MDIndex) + 1
    nextStep = MDStep(nextIndex)
    nextStep.atomNum = thisStep.atomNum

    #TODO nextStep.lattice = ?
    
    
    calcPosition(thisStep, nextStep)
    # print(len(nextStep.atoms))
    # print(nextStep.atoms[0].positons)

test()