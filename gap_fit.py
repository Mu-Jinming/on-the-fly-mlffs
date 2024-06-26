
import subprocess
import numpy as np
import ase.io
import matplotlib.pyplot as plt


def gap_fit(modelFile, inputFile, callback=None):
    print("Running gap_fit()")

    # 直接定义命令字符串
    command = f"""gap_fit force_parameter_name=forces \
        do_copy_at_file=F sparse_separate_file=F gp_file={modelFile} at_file={inputFile} \
        default_sigma={{0.001 0.5 0.0 0.0}} \
        gap={{soap cutoff=4.0 \
        covariance_type=dot_product \
        zeta=2 \
        delta=100.0 \
        atom_sigma=0.7 \
        l_max=6 \
        n_max=6 \
        n_sparse=200 \
        sparse_method=cur_points}}"""

    try:
        subprocess.run(command, shell=True, check=True, executable='/bin/bash')
        print("命令执行成功。")
        if callback:
            callback()
    except subprocess.CalledProcessError as e:
        print(f"执行命令时出错: {e}")

def preditct(modelFile, inputFile, outputFile):
    print("preditct()")

    # 要执行的命令
    command = f"quip E=T F=T atoms_filename={inputFile} param_filename={modelFile} | grep AT | sed 's/AT//' > {outputFile}"
    print(command)

    # 执行命令
    try:
        subprocess.run(command, shell=True, check=True, executable='/bin/bash')
        print("命令执行成功。")
    except subprocess.CalledProcessError as e:
        print(f"执行命令时出错: {e}")



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

# traindataFilePath = './XYZ/initial10Steps.xyz'

# gap_fit('./GAP_SOAP.xml', traindataFilePath)
# gap_fit('./gaptest/GAP_3b.xml', './gaptest/test_MD_dump.xyz')

# def main():

    # gap_fit('./gaptest/GAP_3b.xml', './gaptest/test_MD_dump.xyz')

    # preditct('./GAP_3b.xml', 'validate.xyz', './quip_3b_validate.xyz')
    # preditct('./GAP_3b.xml', './XYZ/WaitForPredict/step_2.xyz', './XYZ/PredictResult/step_2.xyz')

    # fig, ax_list = plt.subplots(nrows=3, ncols=2, gridspec_kw={'hspace': 0.3})
    # fig.set_size_inches(15, 20)
    # ax_list = ax_list.flat[:]
    # force_plot('./validate_raw.xyz', './quip_validate_3b.xyz', ax_list[2], 'Hf', 'Force - Hf')
    # force_plot('./validate_raw.xyz', './quip_validate_3b.xyz', ax_list[3], 'O', 'Force - O')


# if __name__ == "__main__":
#     main()