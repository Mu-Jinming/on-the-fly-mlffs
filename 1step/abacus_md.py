import subprocess
import sys
import os
from MDStep import MDStep

def modifySTRU(thisStep: MDStep, STRUFile):
    #决定nextStep要通过ABACUS运行，故先根据thisStep的信息来构建STRU文件。主要是把位置信息和速度信息写入。
    #写入速度的时候，针对hBN-md：要写入的V = thisStep.velocity / 21.87695

    




def abacusMd(abacusBuildPath, workdir):
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

    # commands = 'mpirun -n 4 /home/jinming/abacus-develop/build/abacus'
    commands = 'mpirun -n 4 %s'%(abacusBuildPath)

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

