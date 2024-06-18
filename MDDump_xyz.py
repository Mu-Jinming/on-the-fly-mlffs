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

def parseMDDump(filePath):
    with open(filePath, 'r') as f:
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

        for atom in mdStep.atoms:
            print(atom.specie, atom.positons, atom.forces, atom.velocity)

        mdStep.atomNum = len(mdStep.atoms)  
        print(mdStep.atomNum)


parseMDDump('./MD_dump')