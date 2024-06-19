class Atom:
    def __init__(self, specie, positons, forces, velocity):
        self.specie = specie
        self.positons = positons
        self.forces = forces
        self.velocity = velocity

class MDStep:
    # atomNum, lattice, atoms
    def __init__(self, MDIndex):
        self.MDIndex = MDIndex
        self.lines = [] #包含每一步的原始数据
        self.lattice = []
        self.atoms = []
        self.atomNum = 0

def parseMDDump(mddumpFilePath):
    with open(mddumpFilePath, 'r') as f:
        lines = f.readlines()
        # print(lines)

    MDSteps = []
    for line in lines :
        line = line.strip()
        if line.startswith('MDSTEP'):
            print(line)
            number = line.split(":")[1].strip()
            mdStep = MDStep(MDIndex = number)
            MDSteps.append(mdStep)
        mdStep.lines.append(line)    

    for mdStep in MDSteps:
        for i in range(len(mdStep.lines)):
            line = mdStep.lines[i]
            if line.startswith('LATTICE_VECTOR'):
                for j in range(1,4):
                    #print(mdStep.lines[i+j])
                    latticeLine = mdStep.lines[i+j].split()
                    latticeLine = [float(x) for x in latticeLine]
                    #print(latticeLine)
                    mdStep.lattice.append(latticeLine)
            
            if line.startswith('INDEX'): #第i行开头是INDEX
                j=1
                atomNum = 0
                while(lines[i+j] is not None and lines[i+j].startswith('INDEX')==False):
                    atomLine = lines[i+j].split()
                    #print(atomLine)
                    if len(atomLine) == 0:
                        break
                    atomNum = max(atomNum, int(atomLine[0]))
                    specie = atomLine[1]
                    positions = [float(x) for x in atomLine[2:5]]
                    forces = [float(x) for x in atomLine[5:8]]
                    velocity = [float(x) for x in atomLine[8:11]]
                    #print(atomNum, specie, positions, forces, velocity)

                    
                    atom = Atom(specie, positions, forces, velocity)
                    mdStep.atoms.append(atom)
                    j+=1
        #print(mdStep.lattice)

        # for atom in mdStep.atoms:
        #     print(atom.specie, atom.positons, atom.forces, atom.velocity)
        mdStep.atomNum = len(mdStep.atoms)
        print(mdStep.lattice)

    return MDSteps

def produceXYZ(XYZFilePath, mddumpFilePath):
    MDSteps = parseMDDump(mddumpFilePath)
    with open(XYZFilePath, 'w') as f:
        for mdStep in MDSteps:
            f.write(str(mdStep.atomNum)+'\n')
            line = ''
            for latticeLine in mdStep.lattice:
                line = line+' '.join(str(x) for x in latticeLine)
                line = line+' '
                #print(line)

            f.write(f'Lattice="{line.strip()}"'+' ')
            f.write('Properties=species:S:1:pos:R:3:forces:R:3 pbc="T T T"'+'\n')
            
            for atom in mdStep.atoms:
                f.write(atom.specie+' ')
                for x in atom.positons:
                    f.write(str(x)+' ')
                for x in atom.forces:
                    f.write(str(x)+' ')
                f.write('\n')
        with open('./e0', 'r') as fe0:
            f.write(fe0.read())
        

produceXYZ('./test_MD_dump.xyz', './MD_dump')