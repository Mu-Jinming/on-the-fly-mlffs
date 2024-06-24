from Atom import Atom

from MDStep import MDStep


def parseMDDump(mddumpFilePath):
    print("parseMDDump")
    #读取md_dump文件，将每一步的每个原子的位置、力、速度保存到MDSteps[]中
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
        print('------------------------------------------:')
        lines = mdStep.lines
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith('LATTICE_VECTOR'):
                for j in range(1,4):
                    #print(lines[i+j])
                    latticeLine = lines[i+j].split()

                    # print(latticeLine)
                    latticeLine = [float(x) for x in latticeLine]
                    #print(latticeLine)
                    mdStep.lattice.append(latticeLine)
            
            if line.startswith('INDEX'): #第i行开头是INDEX
                j=1
                atomNum = 0
                while(lines[i+j] is not None and lines[i+j].startswith('INDEX')==False):
                    atomLine = lines[i+j].split()
                    # print(atomLine)

                    if len(atomLine) == 0:
                        break
                    atomNum = max(atomNum, int(atomLine[0]))
                    specie = atomLine[1]
                    positions = [float(x) for x in atomLine[2:5]]
                    # print(positions)
                    forces = [float(x) for x in atomLine[5:8]]
                    # print(forces)
                    velocity = [float(x) for x in atomLine[8:11]]
                    #print(atomNum, specie, positions, forces, velocity)

                    atom = Atom(specie)
                    atom.positons = positions
                    atom.forces = forces
                    atom.velocity = velocity

                    #TODO:atom.mass待添加，目前默认为15

                    mdStep.atoms.append(atom)
                    j+=1
        #print(mdStep.lattice)

        # for atom in mdStep.atoms:
        #     print(atom.specie, atom.positons, atom.forces, atom.velocity)

        # print(mdStep.atoms[0].positons[0])

        mdStep.atomNum = len(mdStep.atoms)
        # print(mdStep.lattice)

    return MDSteps

def produceXYZtoTrain(XYZFilePath, mddumpFilePath):
    print("produceXYZtoTrain")
    #生成的xyz文件用于训练gap模型
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

def parseXYZ(XYZFilePath, MDIndex:int): #new一个MDStep(MDIndex)对象。读取xyz文件，并将每个原子的位置、力保存到对象中。
    print("parseXYZ")
    thisStep = MDStep(str(MDIndex))
    with open(XYZFilePath, 'r') as file:
        header = file.readline()
        atomCount = int(header.strip())
        content = file.readline().strip()
        lattice_str = content.split('Lattice="')[1].split('"')[0]
        print(atomCount)
        print(lattice_str)
        for i in range(atomCount):
            line = file.readline().strip()
            atom_str = line.split()
            atom = Atom(atom_str[0])
            atom.positons = [float(x) for x in atom_str[1:4]]
            atom.forces = [float(x) for x in atom_str[9:12]]
            thisStep.atoms.append(atom)
        print(thisStep.atoms[1].forces)
        print(file.readline())
    return thisStep
        
#parseXYZ('./XYZ/PredictResult/step_2.xyz', MDStep(MDIndex = '2'))

# produceXYZtoTrain('./test_MD_dump.xyz', './MD_dump')