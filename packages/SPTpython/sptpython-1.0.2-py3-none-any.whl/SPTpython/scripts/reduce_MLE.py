import pandas as pd
import tkinter.filedialog
import os
import re
import pathlib

INTENSITY_CUTOFF = 4000

def find_csvs(path: str) -> dict:
    """
    Locates all csv files in the given path that match a specific naming pattern.
    The pattern is defined by a regular expression

    Args:
        path (str): outer path to look in

    Returns:
        dict: dictionary with keys as delay values and values as lists of file paths
    """
    
    delays = {}
    re_match = r'.+MLE.+nf\d+_d(\d+\.\d+)_e\d+\.\d+_p\d+\.\d+_NDTiffStack\d*\.csv'
    for root, _, tempfiles in os.walk(top=path, topdown=False):
        for name in tempfiles:
            if re.match(re_match, str(os.path.join(root,name))):
                delay = float(re.match(re_match, str(os.path.join(root,name))).group(1))
                if delay not in delays:
                    delays[delay] = []
                delays[delay].append(os.path.join(root,name))
    return delays

def reduce_csv(open_path: str, save_path: str) -> None:
    """
    Reduces the csv file by applying an intensity cutoff using INTENSITY_CUTOFF

    Args:
        open_path (str): location of input csv file
        save_path (str): location to save the reduced csv file
    """
    
    data = pd.read_csv(open_path)
    data_reduced = data[data['intensity [photons]'] > INTENSITY_CUTOFF]
    try:
        print(f"New count: {len(data_reduced)} / {len(data)} ({len(data_reduced)/len(data)*100:.2f}%)")
    except ZeroDivisionError:
        print("No data left after cutoff")
    data_reduced.to_csv(save_path, index=False)

def main():
    path = tkinter.filedialog.askdirectory(title='Select outer directory')
    csvs = find_csvs(path)
    
    for delay in csvs:
        print(f"Processing delay: {delay}")
        for csv_path in csvs[delay]:
            original_folder = os.path.split(os.path.split(csv_path)[0])[1]
            outer_folder = pathlib.Path(csv_path).parents[1]
            save_folder = os.path.join(outer_folder, f'{original_folder}_reduced')
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, f"{os.path.split(csv_path)[1]}")
            reduce_csv(csv_path, save_path)
            with open(os.path.join(save_folder, 'cutoff.txt'), 'a') as f:
                f.write(f"Intensity cutoff: {INTENSITY_CUTOFF}\n")

if __name__ == '__main__':
    main()