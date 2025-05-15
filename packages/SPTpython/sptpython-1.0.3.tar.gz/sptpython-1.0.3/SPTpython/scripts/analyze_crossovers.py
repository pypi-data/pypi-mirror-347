import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize
import sys
sys.path.append("src")
from scripts.analyze_emsds import open_previous_emsd_results

# config is of the form path:[diffusivity, title]
CONFIG = {
    r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\CPR-ID-226\eMSDs_Feb_04_2025_11_10_27':
        [2e-7,'4x'],
    r'E:\Current Microscope Data\CPR-ID-225\26C\eMSDs_Jan_21_2025_11_09_57':
        [2e-5,'1x'],
    r'E:\Current Microscope Data\CPR-ID-224\26C\eMSDs_Jan_21_2025_11_10_27':
        [2e-7,'2x'],
    r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\CPR-ID-227\eMSDs_Feb_07_2025_13_19_55':
        [2e-7,'8x'],
}

def model(x,y):
    shape = x.shape
    return np.ones(shape)*y

path = list(CONFIG.keys())[3]
DIFFUSIVITY = CONFIG[path][0]
TITLE = CONFIG[path][1]

data_results = open_previous_emsd_results(path, dream_fits_path='', open_handler=False, open_jobs = False)

fig, ax = plt.subplots()

ys_to_fit = None
ts_to_fit = None
all_ts = None
max_idx_ys_to_fit = 2
flip = True

for idx,metadata_path in enumerate(data_results.keys()):
    # fits = data_results[metadata_path]['fits']
    slow_fits = 'Expected_Val_1'
    fast_fits = 'Expected_Val_2'
    if flip:
        slow_fits, fast_fits = fast_fits, slow_fits
        
    extra_infos = data_results[metadata_path]['extra_infos']
    ax.plot(extra_infos.index, np.power(10,extra_infos[slow_fits]),'k-')
    ax.plot(extra_infos.index, np.power(10,extra_infos[fast_fits]),'b-')
    
    if idx <= max_idx_ys_to_fit:
        if not isinstance(ys_to_fit, np.ndarray):
            ys_to_fit = np.array(np.power(10,extra_infos[slow_fits]))
            ts_to_fit = extra_infos.index
        else:
            ys_to_fit = np.append(ys_to_fit, np.power(10,extra_infos[slow_fits]))
            ts_to_fit = np.append(ts_to_fit, extra_infos.index)

    if not isinstance(all_ts, np.ndarray):
        all_ts = np.array(extra_infos.index)
    else:
        all_ts = np.append(all_ts, extra_infos.index)

popt, pcov = scipy.optimize.curve_fit(model, ts_to_fit, ys_to_fit)
print(popt)
ax.plot(all_ts, model(all_ts, *popt), 'r--')
ax.plot(all_ts, 4*DIFFUSIVITY*all_ts, 'g--')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_title(f'{TITLE}, t*={round(popt[0]/(4*DIFFUSIVITY),1)}')
ax.set_xlabel("Time (s)")
ax.set_ylabel("MSD (um^2)")
fig.tight_layout()
print(f"CROSSOVER: {popt[0]/(4*DIFFUSIVITY)}")
plt.savefig(f'logs/simulation saves/{TITLE}_crossover.png')
print(f"Saved {TITLE}.png")
plt.show()