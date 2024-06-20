from MDDumpConvertXYZ import MDStep, Atom, parseMDDump

def verlet(current_position, dt, current_velocity, current_acceleration):
    next_position = current_position + current_velocity * dt + 0.5 * current_acceleration * dt**2
    return next_position

def calcPosition(thisStep: MDStep, nextStep: MDStep):
    for thisStepAtom in thisStep.atoms:
        nextStepAtom = Atom(thisStepAtom.specie)
        for i in range(3):
            #首先计算出第i步的加速度$a_i$，查表得到原子质量m，故$a_i$=$F_i/m$
            thisStepAtom.acceleration[i] = thisStepAtom.forces[i] / thisStepAtom.mass 
            #再第i+1步的原子坐标：$\mathbf{r_{i+1}} = \mathbf{r}_i + \mathbf{v}_i \Delta t + \frac{1}{2} \mathbf{a}_i (\Delta t)^2 $
            nextStepAtom.positons[i] = verlet(thisStepAtom.positons[i], thisStep.deltaT, thisStepAtom.velocity[i], thisStepAtom.acceleration[i])

        nextStep.atoms.append(nextStepAtom)

def test():
    
    MDSteps = parseMDDump('./MD_dump')
    thisStep = MDSteps[-1]
    nextIndex = int(thisStep.MDIndex) + 1
    nextStep = MDStep(nextIndex)
    nextStep.atomNum = thisStep.atomNum
    nextStep.lattice = thisStep.lattice
    
    calcPosition(thisStep, nextStep)

    print(nextStep.atoms[0].positons)

test()