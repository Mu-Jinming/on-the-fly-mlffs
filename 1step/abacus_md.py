import subprocess
import os

def runABACUS(ABACUSBuildPath):
    #切换工作目录
    #os.chdir(workdir)
    command = 'mpirun -n 8 %s' % ABACUSBuildPath

    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        # 打印命令输出
        print(f"命令 '{command}' 的输出:")
        print(stdout.decode('utf-8'))
        
        # 检查是否有错误
        if process.returncode != 0:
            print(f"执行命令 '{command}' 时出错:")
            print(stderr.decode('utf-8'))
    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    ABACUSBuildPath = "/home/jinming/abacus-develop/build/abacus"
    runABACUS(ABACUSBuildPath)

