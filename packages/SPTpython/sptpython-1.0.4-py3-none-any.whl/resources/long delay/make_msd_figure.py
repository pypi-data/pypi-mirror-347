import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pySPT.postprocessing import plot_MSDs
import os

# 2x/chain
path = r'E:\Current Microscope Data\CPR-ID-224\26C\msd_truncated'

datas = []
for file in os.listdir(path):
    if file.endswith(".csv"):
        data = pd.read_csv(os.path.join(path, file), index_col=0)
        datas.append(data)
# data_results = open_previous_emsd_results(path, dream_fits_path='', open_handler=False, open_jobs = False)
# print("Data read")

fig, ax = plt.subplots(figsize=(5,3.3))

cap = 300

for data in datas:
    data = data[data.columns[:cap]]
    plot_MSDs(data, fig=fig, ax=ax, color='k', alpha=0.03)

ts = np.logspace(*np.log10(ax.get_xlim()))

ax.plot(ts[0:40], (4*2e-7*435.6*np.ones(ts.shape))[0:40], 'r--')
ax.plot(ts[20:], 4*2e-7*ts[20:], 'r--')

ax.set_title('')
ax.set_ylim(5e-8, 1.1)
fig.tight_layout(pad=0.2)
# ax.set_xscale('log')
# ax.set_yscale('log')
# ax.set_title(f'{TITLE}, t*={round(popt[0]/(4*DIFFUSIVITY),1)}')
# ax.set_xlabel("Time (s)")
# ax.set_ylabel("MSD (um^2)")
# fig.tight_layout()
# print(f"CROSSOVER: {popt[0]/(4*DIFFUSIVITY)}")
plt.savefig(f'logs/simulation saves/2xmsd.svg')
# print(f"Saved {TITLE}.png")

plt.show()