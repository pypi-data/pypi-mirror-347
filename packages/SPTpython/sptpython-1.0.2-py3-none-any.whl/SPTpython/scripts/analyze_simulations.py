import matplotlib.pyplot as plt
from SPTpython.postprocessing import PostProcessingJob
import numpy as np
from SPTpython.utils import get_figure

def read_dream_fits(path):
    contents = ''
    fit_info = {}
    last_path = None
    with open(path, 'r') as fin:
        contents = fin.read()
    for line in contents.split('\n'):
        if 'Path' in line:
            path = line.split('Path: ')[-1].replace(', ','')
            if path not in fit_info.keys():
                fit_info[path] = {
                    'frames':[],
                    'popts':[]
                }
            last_path = path
        elif 'frame' in line:
            frame = line.split("frame: ")[-1].replace(', ','')
            fit_info[last_path]['frames'].append(int(frame))
        elif 'popt' in line:
            popt = line.split("popt: ")[-1].replace('[','').replace(']','')
            popt = popt.split(', ')
            popt = [float(p) for p in popt]
            fit_info[last_path]['popts'].append(popt)
    return fit_info

def compile_dream_fits(paths, output_path):
    all_contents = []
    for path in paths:
        with open(path,'r') as fin:
            contents = fin.read()
            all_contents.append(contents)
    
    with open(output_path, 'w') as fout:
        for contents in all_contents:
            fout.write(contents)
          
def main():
    # paths = [
    #     r'logs/simulation_params/dream_fits_Dec_07_2024_14_54_17.txt',
    #     r'logs/simulation_params/dream_fits_Dec_07_2024_14_54_14.txt',
    #     r'logs/simulation_params/dream_fits_Dec_07_2024_14_54_26.txt',
    #     r'logs/simulation_params/dream_fits_Dec_07_2024_14_54_20.txt',
    #     r'logs/simulation_params/dream_fits_Dec_07_2024_14_54_23.txt'
    # ]
    # compile_dream_fits(paths, r'logs/simulation_params/compiled_dream_fits.txt')
    path = r'logs/simulation_params/compiled_dream_fits.txt'
    all_dream_fits = read_dream_fits(path)
    categories = {}
    for metadata_path in all_dream_fits.keys():
        job = PostProcessingJob(path=metadata_path)
        delay = job.get_metadata_item("input parameters")["Frame Delay (ms)"] / 1000
        ls = metadata_path.split("\\")
        idx = ls.index("Current Microscope Data")
        condition = f"{ls[idx+1]} {ls[idx + 2]}"
        if condition in categories.keys():
            categories[condition].append(
                {
                    'path':metadata_path,
                    'delay':delay
                }
            )
        else:
            categories[condition] = [
                {
                    'path':metadata_path,
                    'delay':delay
                }
            ]
    
    vars = ['k_on', 'K', 'D']
    units = ['s$^-1$','','um$^2$/s']
    for condition in categories.keys():
        fig, axs = plt.subplots(2,2)
        fig.suptitle(condition)
        for i in range(len(vars)):
            axs.reshape(-1)[i].set_xlabel("t (s)")
            axs.reshape(-1)[i].set_ylabel(f"{vars[i]} [{units[i]}]")
            axs.reshape(-1)[i].set_xscale('log')
            axs.reshape(-1)[i].set_yscale('log')
        for data_set_idx, data_set in enumerate(categories[condition]):
            # if data_set_idx == 0:
                # categories[condition][data_set_idx]['data'] = []
            
            these_dream_fits = all_dream_fits[data_set['path']]
            xs = np.array(these_dream_fits['frames']) * data_set['delay']
            all_popts = []
            for _ in range(len(vars)):
                all_popts.append([])
            for popt in these_dream_fits['popts']:
                for i,val in enumerate(popt):
                    all_popts[i].append(val)
                    
            categories[condition][data_set_idx]['data'] = [xs, all_popts]
            for i,popts in enumerate(all_popts):
                axs.reshape(-1)[i].plot(xs, popts,'o')
                
        fig.tight_layout()
        
    colors = ['k'] + plt.rcParams['axes.prop_cycle'].by_key()['color']
    for var_idx, var in enumerate(vars):
        fig, ax = plt.subplots()
        for condition_idx,condition in enumerate(categories.keys()):
            color = colors[condition_idx]
            for data_idx in range(len(categories[condition])):
                data = categories[condition][data_idx]['data']
                label = ''
                if data_idx == 0:
                    label = condition
                ax.plot(data[0], data[1][var_idx], 'o', color=color, label = label)
        ax.legend()
        ax.set_xlabel("t (s)")
        ax.set_ylabel(f"{var} [{units[var_idx]}]")
        ax.set_xscale('log')
        ax.set_yscale('log')
        fig.tight_layout()
                
    plt.show()
        


if __name__ == '__main__':
    main()