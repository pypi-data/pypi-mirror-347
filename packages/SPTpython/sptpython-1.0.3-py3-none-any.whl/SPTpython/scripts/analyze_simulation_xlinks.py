import matplotlib.pyplot as plt
import pandas as pd
import os
from pySPT import utils

path_config = {
    '0x':r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Personal Computers\Chris\Research\Programming Scripts\pySPT\logs\simulation MSDs\Feb_12_2025_16_23_25',
    '1x':r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Personal Computers\Chris\Research\Programming Scripts\pySPT\logs\simulation MSDs\Feb_12_2025_16_06_22',
    '2x':r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Personal Computers\Chris\Research\Programming Scripts\pySPT\logs\simulation MSDs\Feb_12_2025_16_09_42',
    '3x':r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Personal Computers\Chris\Research\Programming Scripts\pySPT\logs\simulation MSDs\Feb_12_2025_16_15_10',
    '4x':r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Personal Computers\Chris\Research\Programming Scripts\pySPT\logs\simulation MSDs\Feb_12_2025_16_20_50',
}
colors = {
    '0x':'black',
    '1x':'red',
    '2x':'blue',
    '3x':'green',
    '4x':'purple',
}

data = {}

for path in path_config:
    for file in os.listdir(path_config[path]):
        if file.endswith('.csv'):
            if path not in data:
                data[path] = []
            df = pd.read_csv(os.path.join(path_config[path], file), index_col=0)
            data[path].append(df)


for label in data:
    for datum in data[label]:
        plt.plot(datum, color=colors[label], alpha=10/len(df.columns))   

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Time (s)')
plt.ylabel('MSD (um^2)')
plt.tight_layout()
xlim = plt.xlim()
ylim = plt.ylim()
plt.savefig('logs/simulation saves/simulation compare xlink/compare_all.png')

plt.clf()
for label in data:
    for datum in data[label]:
        plt.plot(datum, color=colors[label], alpha=10/len(df.columns))

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Time (s)')
    plt.ylabel('MSD (um^2)')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.tight_layout()
    plt.savefig(f'logs/simulation saves/simulation compare xlink/{label}.svg')
    plt.clf()