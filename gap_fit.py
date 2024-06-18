
import quippy.descriptors
import subprocess
from quippy.potential import Potential
import numpy as np
import ase.io
import matplotlib.pyplot as plt


def gap_fit():
    print("gap_fit()")
    command = """gap_fit"""
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    print("标准输出:", result.stdout)
    print("错误输出:", result.stderr)

def preditct():
    print("preditct()")

    quip_command = "quip F=T atoms_filename=validate.xyz param_filename=GAP_soap.xml"
    grep_command = "grep AT"
    sed_command = "sed 's/AT//'"

    # 创建第一个子进程，运行 quip 命令
    quip_process = subprocess.Popen(quip_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 创建第二个子进程，运行 grep 命令，将 quip 的输出传递给 grep
    grep_process = subprocess.Popen(grep_command, shell=True, stdin=quip_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 创建第三个子进程，运行 sed 命令，将 grep 的输出传递给 sed
    sed_process = subprocess.Popen(sed_command, shell=True, stdin=grep_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 获取最终输出并写入文件
    with open('quip_validate.xyz', 'w') as output_file:
        for line in sed_process.stdout:
            output_file.write(line.decode('utf-8'))

    # 确保所有进程都完成
    quip_process.stdout.close()
    grep_process.stdout.close()
    sed_process.stdout.close()

    quip_process.wait()
    grep_process.wait()
    sed_process.wait()

    # 检查错误输出
    quip_stderr = quip_process.stderr.read().decode('utf-8')
    grep_stderr = grep_process.stderr.read().decode('utf-8')
    sed_stderr = sed_process.stderr.read().decode('utf-8')

    if quip_stderr:
        print(f"quip error: {quip_stderr}")
    if grep_stderr:
        print(f"grep error: {grep_stderr}")
    if sed_stderr:
        print(f"sed error: {sed_stderr}")

def force_plot(in_file, out_file, ax, symbol='HfO', title='Plot of force'):
    """ Plots the distribution of firce components per atom on the output vs the input
        only plots for the given atom type(s)"""

    in_atoms = ase.io.read(in_file, ':')
    out_atoms = ase.io.read(out_file, ':')
    # 打印 in_atoms 和 out_atoms 的内容
    # print("In atoms:")
    # for atom in in_atoms:
    #     print("Positions:", atom.positions)
    #     print("Forces:", atom.get_forces())
    #     print("Symbols:", atom.get_chemical_symbols())
        
    # print("Out atoms:")
    # for atom in out_atoms:
    #     print("Positions:", atom.positions)
    #     print("Forces:", atom.get_forces())
    #     print("Symbols:", atom.get_chemical_symbols())

    # extract data for only one species
    in_force, out_force = [], []
    for at_in, at_out in zip(in_atoms, out_atoms):
        # get the symbols
        sym_all = at_in.get_chemical_symbols()
        # add force for each atom
        for j, sym in enumerate(sym_all):
            if sym in symbol:
                in_force.append(at_in.get_forces()[j])
                #out_force.append(at_out.get_forces()[j]) \
                # print(at_out.arrays['force'][j])
                out_force.append(at_out.arrays['force'][j]) # because QUIP and ASE use different names
                
    # convert to np arrays, much easier to work with
    #in_force = np.array(in_force)
    #out_force = np.array(out_force)
    # scatter plot of the data
    ax.scatter(in_force, out_force)
    # get the appropriate limits for the plot
    for_limits = np.array(in_force + out_force)
    flim = (for_limits.min() - 1, for_limits.max() + 1)
    ax.set_xlim(flim)
    ax.set_ylim(flim)
    # add line of
    ax.plot(flim, flim, c='k')
    # set labels
    ax.set_ylabel('force by GAP / (eV/Å)')
    ax.set_xlabel('force by ABACUS / (eV/Å)')
    #set title
    ax.set_title(title)
    # add text about RMSE
    _rms = rms_dict(in_force, out_force)
    rmse_text = 'RMSE:\n' + str(np.round(_rms['rmse'], 3)) + ' +- ' + str(np.round(_rms['std'], 3)) + 'eV/Å'
    print(title, rmse_text)
    ax.text(0.9, 0.1, rmse_text, transform=ax.transAxes, fontsize='large', horizontalalignment='right',
            verticalalignment='bottom')
    
def rms_dict(x_ref, x_pred):
    """ Takes two datasets of the same shape and returns a dictionary containing RMS error data"""

    x_ref = np.array(x_ref)
    x_pred = np.array(x_pred)

    if np.shape(x_pred) != np.shape(x_ref):
        raise ValueError('WARNING: not matching shapes in rms')

    error_2 = (x_ref - x_pred) ** 2

    average = np.sqrt(np.average(error_2))
    std_ = np.sqrt(np.var(error_2))

    return {'rmse': average, 'std': std_}

def main():
    #gap_fit()
    #preditct()

    fig, ax_list = plt.subplots(nrows=3, ncols=2, gridspec_kw={'hspace': 0.3})
    fig.set_size_inches(15, 20)
    ax_list = ax_list.flat[:]
    force_plot('./validate_raw.xyz', './quip_validate_3b.xyz', ax_list[2], 'Hf', 'Force - Hf')
    force_plot('./validate_raw.xyz', './quip_validate_3b.xyz', ax_list[3], 'O', 'Force - O')


if __name__ == "__main__":
    main()