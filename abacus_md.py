import subprocess
import sys
import os
from MDStep import MDStep
import shutil

def parseAtoms(step: MDStep):
    #根据原子符号，将step.atoms写入到dictionary中{atom.specie : atoms[]}
    atomsDict = {}
    for atom in step.atoms:
        specie = atom.specie
        if specie not in atomsDict:
            atomsDict[specie] = []
        atomsDict[specie].append(atom)
    return atomsDict
def createSTRU(thisStep: MDStep):
    #决定thisStep要通过ABACUS运行，故先根据thisStep的位置和速度来构建STRU文件。主要是把位置信息和速度信息写入。
    #写入速度的时候，针对hBN-md：写入的V = thisStep.velocity / 21.87695
    # 指定要创建的文件夹的名称或路径

    fileName = f"step_{thisStep.MDIndex}"
    folderName = os.path.join("./1step/TiNB/", fileName)

    # 使用os.path.exists()检查文件夹是否已经存在
    if not os.path.exists(folderName):
        # 使用os.mkdir()创建文件夹
        os.mkdir(folderName)
        print(f"文件夹 '{folderName}' 已创建。")
    else:
        print(f"文件夹 '{folderName}' 已存在。")

    #将INPUT文件复制一份到新文件下
    sourceINPUT = "./1step/TiNB/INPUT"
    # 构建新的INPUT文件路径
    thisStepINPUT = os.path.join(folderName, "INPUT")

    # 检查目标文件是否已存在
    if not os.path.exists(thisStepINPUT):
        shutil.copy(sourceINPUT, thisStepINPUT)
        print(f"文件 '{sourceINPUT}' 已成功复制到 '{thisStepINPUT}'。")
    else:
        print(f"文件 '{thisStepINPUT}' 已存在，无需复制。")
    
    STRUPath = os.path.join(folderName, "STRU")

    initContent = """ATOMIC_SPECIES
Ti  47.867  /home/jinming/on-the-fly-mlffs/1step/TiNB/upf/Ti.upf
N   14.007  /home/jinming/on-the-fly-mlffs/1step/TiNB/upf/N.upf
B   10.81   /home/jinming/on-the-fly-mlffs/1step/TiNB/upf/B.upf

NUMERICAL_ORBITAL
/home/jinming/on-the-fly-mlffs/1step/TiNB/orb/Ti_gga_10au_100Ry_4s2p2d1f.orb
/home/jinming/on-the-fly-mlffs/1step/TiNB/orb/N_gga_10au_100Ry_2s2p1d.orb
/home/jinming/on-the-fly-mlffs/1step/TiNB/orb/B_gga_10au_100Ry_2s2p1d.orb

LATTICE_CONSTANT
1.8897260000

LATTICE_VECTORS
    20.0763846187        0.0000000000        0.0000000000
    -10.0381923094       17.3866592300        0.0000000000
    0.0000000000        0.0000000000       30.0000000000

ATOMIC_POSITIONS
Direct

        """
    atomsDict = parseAtoms(thisStep)
    with open(STRUPath, "w") as f:
        f.write(initContent + '\n')
        for specie, atoms in atomsDict.items():
            f.write(specie + '\n')
            f.write("0.0000   #magnetism" + '\n')
            f.write(str(len(atoms)) + '\n')
            for atom in atoms:
                space = '        '
                m111v = " m 1 1 1 v "
                print(atom.positons)
                print(atom.velocity)
                content = space + str(atom.positons[0]) +space + str(atom.positons[1])+ space + str(atom.positons[2]) + m111v + str(atom.velocity[0] / 21.87695) + space + str(atom.velocity[1] / 21.87695) + space + str(atom.velocity[2] / 21.87695)
                # content = space + atom.positons[0] +space + atom.positons[1]+ space + atom.positons[2] + m111v + space + atom.velocity[0] / 21.87695 + space + atom.velocity[1] / 21.87695 + space + atom.velocity[2] / 21.87695
                f.write(content + '\n')
                f.write('\n')

# from MDDumpConvertXYZ import parseXYZ
# step2 = parseXYZ('./XYZ/PredictResult/step_2.xyz', 2) #step2中有位置、力
# print(step2.MDIndex)
# for atom in step2.atoms:
#     for i in range(3):
#         print(atom.forces)
#         atom.acceleration.append(atom.forces[i] / atom.atomicMassMap[atom.specie])
#         atom.velocity.append(1.1111 * atom.acceleration[i]) #随便编的数据，测试能否生成STRU文件
# createSTRU(step2)

def abacusMd(abacusBuildPath, workdir):
    originalDir = os.getcwd()
    os.chdir(workdir)

    # 查看当前设置的 OMP_NUM_THREADS 环境变量
    omp_num_threads = os.environ.get('OMP_NUM_THREADS', '未设置')
    print(f"当前设置的 OMP_NUM_THREADS: {omp_num_threads}")

    # 设置环境变量 OMP_NUM_THREADS
    os.environ['OMP_NUM_THREADS'] = '5'

    omp_num_threads = os.environ.get('OMP_NUM_THREADS', '未设置')
    print(f"当前设置的 OMP_NUM_THREADS: {omp_num_threads}")

    proc = subprocess.Popen(
        "/bin/bash",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=True
    )

    commands = 'mpirun -n 4 /home/jinming/abacus-develop/build/abacus'
    # commands = 'mpirun -n 4 %s'%(abacusBuildPath)

    proc.stdin.write(commands.encode())
    proc.stdin.flush()
    proc.stdin.close()

    # Real time stdout of subprocess
    stdout = []
    while True:
        line = proc.stdout.readline().decode()
        stdout.append(line)

        if line == "" and proc.poll() is not None:
            break

        # Print outputs
        sys.stdout.write(line)

    # Wait for child process and get return code
    return_code = proc.wait()
    print(f"Child process return code: {return_code}")
    os.chdir(originalDir)

abacusMd(1, './1step/TiNB/step_19')