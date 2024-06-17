class Atom:
    def __init__(self, species, positon, force, velocity):
        self.species = species
        self.positon = positon
        self.force = force
        self.velocity = velocity

class MDStep:
    # atomNum, lattice, atoms
    def __init__(self, MDIndex):
        self.MDIndex = MDIndex

#MDSTEP:
    #LATTICE_VECTOR -- lattice
    #index -- atomNum
    #
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
            

            
        


parseMDDump('./MD_dump')