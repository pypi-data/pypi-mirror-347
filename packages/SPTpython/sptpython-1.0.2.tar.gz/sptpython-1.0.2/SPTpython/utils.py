import logging
logging.getLogger(__name__)

import winsound
import tkinter
import numpy as np
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import datetime
import tkinter
import tkinter.filedialog
import scipy.stats
import pims
import pathlib
import dpath
from typing import Union
import json
import concurrent.futures
from typing import List
import re

if __name__ != '__main__':
    from . import TIFViewer
    from . import config
    cfg = config.load_config() # script uses config parameters

    font = {'family' : 'sans-serif',
            'weight' : 'normal',
            'size'   : cfg["font_size"]}

    matplotlib.rc('font', **font)
        
class Version:
    def __init__(self, s):
        self.version = s
    def __lt__(self, other_version):
        this_version_split = self.version.split('.')
        other_version_split = other_version.version.split('.')
        for this_idx,this_item in enumerate(this_version_split):
            if this_idx >= len(other_version_split):
                return False
            elif int(this_item) < int(other_version_split[this_idx]):
                return True
        return False
         
def calculate_jump_lengths(trajectories, log = True):
    if log:
        logging.info("Calculating jump distribution...")
    all_jumps = []
    for particle in trajectories['particle'].unique():
        subset = np.array(trajectories[trajectories['particle']==particle][['y','x']])
        
        # pythagorean theorem
        jumps = np.sqrt(np.sum(np.diff(subset,axis=0)**2,axis=1))

        all_jumps += list(jumps)

    all_jumps.sort()
    all_jumps = np.array(all_jumps)
    
    return all_jumps

def check_string_type(s: str, type_: type):
    """
    Collects the information in the string and type casts it to see if there is an error.
    If there is an error, recursively truncate string until the issue is resolved, 
    or until string is empty
    """
    try:
        if s != '':
            type_(s)
            return s
        elif s == '':
            return s
    except ValueError:
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
        s = s[:-1]  # truncate last character
        return check_string_type(s,type_)
    
def compatibilize_metadata(metadata):
    logging.debug("Compatibilizing metadata...")
    version_metadata_changes = {
        "0.7": [
            {
                'item':'input parameters/Trajectories: only consider emitters with frame >={input}', 
                'default_value':0,
                'callback':None
            }
        ],
        "0.10": [
            {
                'item':'MSD num_traj_per_point',
                'default_value':-1,
                'callback':get_num_traj_per_msd_point
            }
        ],
        "0.12": [
            {
                'item':'bifurcation',
                'default_value':[None, None],
                'callback':None
            }
        ],
        "0.14": [
            {
                'item':'drift_mode',
                'default_value':'trajectories_filtered',
                'callback':None
            },
            {
                'item':'mitchell_mode_data',
                'default_value':{'mitchell_mode':False, 'path':None},
                'callback':None
            }
        ]
    }
    
    if type(metadata) == list:
        # not entirely sure if this is good coding practice but this is what I'm going for
        # this solves the issue of compatibilizing reprocessing outputs that store metadata as a list
        for this_metadata in metadata:
            compatibilize_metadata(this_metadata)

        return metadata
        
    metadata_version = metadata["SPTpython version"]
    callbacks = []
    
    for version in version_metadata_changes.keys():
        if Version(version) > Version(metadata_version):
            for change in version_metadata_changes[version]:
                logging.debug(f"Adding value: {change['default_value']} to dict path: {change['item']}")
                dpath.new(metadata, change['item'], change['default_value'])
                callbacks.append(change['callback'])
                
    return metadata, callbacks

def find_all_metadata(path, skip_times = [], only_last_metadata = False):
    files = []
    for root, _, tempfiles in os.walk(top=path, topdown=False):
        for name in tempfiles:
            if root.split(path)[1] != '' and name == 'metadata.json':
                add = True
                for skip_time in skip_times:
                    if skip_time in root:
                        add = False
                regex_match = search_regex_id(os.path.join(root,name))
                if re.search(r'CPR-ID-(\d+)', regex_match) != None:
                    if int(re.search(r'CPR-ID-(\d+)', regex_match).group(1)) < cfg["metadata_ignore"]:
                        add = False
                if add:
                    # print(os.path.join(root, name))
                    files.append(os.path.join(root,name))
                
    return files

def find_csv(root_path, csv_to_match):
    files = os.listdir(root_path)

    for file in files:
        if csv_to_match in file:
            return os.path.join(root_path,file)
    else:
        return ""

def find_particle_video(trajectory: pd.DataFrame, num_frames: int, memory: int, files: list):
    """
    Given a particle trajectory, find which video generated that trajectory.
    This is needed since common videos are concatenated together, so this will
    un-concatenate them and find the original.

    Args:
        trajectory (pd.DataFrame)
        num_frames (int): number of frames in each video
        memory (int): memory used in original calculation
        files (list): list of frames used in original calculation

    Returns:
        tuple: file of trajectory, offset of that trajectories' frames used during calculation concatentation
    """
    startFrame = min(trajectory['frame'])
    framesIdx = 0
    offset = 0
    temp = startFrame
    while temp >= 0:
        temp -= num_frames + memory + cfg["blank_frames"]
        if temp >= 0:
            offset += num_frames + memory + cfg["blank_frames"]
        
        if temp >= 0:
            framesIdx += 1

    return files[framesIdx], offset, framesIdx
  
def generate_legend(ax: matplotlib.axes.Axes, remove_duplicates = True, group_by_exp = False, **legend_kwargs_in):
    if remove_duplicates:
        handles, labels = ax.get_legend_handles_labels()
        unique = []
        for i, (h, l) in enumerate(zip(handles, labels)):
            if l not in labels[:i]:
                unique.append((h, l))
                
    if group_by_exp and remove_duplicates:
        # collapse common experiments into one legend entry, concatenating delays
        exps = []
        for el in unique:
            regex_match = r'\[.+?s\] ([\w\.% ]+)(?:\(N=\d+\))?'
            if re.search(regex_match, el[1]) != None:
                exp = re.search(regex_match, el[1]).group(1)
                if exp not in exps:
                    exps.append(exp)
        
        unique_condensed = []
        for exp in exps:
            delays = []
            found = False
            for el in unique:
                if re.search(regex_match, el[1]) != None:
                    this_exp = re.search(regex_match, el[1]).group(1)
                    if this_exp == exp:
                        if not found:
                            unique_condensed.append((el[0], exp))
                            found = True
                        delays.append(re.search(r'\[(.+?) s\]', el[1]).group(1))
            new_label = f'{exp}'
            unique_condensed[-1] = (unique_condensed[-1][0], new_label)

        unique = unique_condensed
    
    legend_kwargs = cfg["legend_kwargs"].copy()
    legend_kwargs.update(legend_kwargs_in)
    if 'loc' in legend_kwargs_in.keys() and legend_kwargs_in['loc'] == 'outside':
        legend_kwargs['bbox_to_anchor'] = (1, 1)
        legend_kwargs['loc'] = 'upper left'
    if remove_duplicates:
        legend = ax.legend(*zip(*unique), title_fontproperties = cfg["legend_title_kwargs"], **legend_kwargs)
    else:
        legend = ax.legend(title_fontproperties = cfg["legend_title_kwargs"], **legend_kwargs)
    # legend.get_frame().set_alpha(0)
    
    for line in legend.get_lines():
        line.set_linewidth(cfg["legend_linewidth"])
    
    if remove_duplicates:
        for legend_handle in legend.legendHandles: 
            legend_handle.set_alpha(1)
    
    return legend

def gaussian(x, sig, mu):
    return (1/(sig*2*np.pi))*np.exp(-0.5*np.power((x-mu)/sig,2))

def get_figure(row=None, col=None, sharex=True, sharey=True, fig_height=None, fig_width=None, gridspec_kw = {}):
    """
    Common figure generator
    """
    if __name__ != '__main__':
        fig_height = cfg["fig_height_show"]
        fig_width = cfg["fig_width_show"]
        box_width = cfg["box_width"]
    
    if row != None:
        fig, ax = plt.subplots(row, col, sharex=sharex, sharey=sharey, gridspec_kw=gridspec_kw)
    else:
        fig, ax = plt.subplots()
        # ax.spines[['right', 'top']].set_visible(True)
        
    fig.set_figheight(fig_height)
    fig.set_figwidth(fig_width)
    
    if type(ax) == np.ndarray:
        for _, this_ax in enumerate(ax.flat):
            this_ax.tick_params(**cfg["tick_params_major"])
            this_ax.tick_params(**cfg["tick_params_minor"])
            for x in this_ax.spines.values():
                x.set_linewidth(box_width)
    else:
        ax.tick_params(**cfg["tick_params_major"])
        ax.tick_params(**cfg["tick_params_minor"])
        
        for x in ax.spines.values():
            x.set_linewidth(box_width)
    
    if row==1 and col==1:
        ax = [ax]
    return fig, ax

def get_msd_noaverage(trajectory, delay):
    # delay: s, nmPerPix: nm
    # assuming no gaps
    particle = trajectory['particle'].iloc[0]
    msds = np.power((trajectory['y'] - trajectory['y'].iloc[0]),2) + np.power((trajectory['x'] - trajectory['x'].iloc[0]),2)
    msds = msds[1:]
    
    times = [delay*(i+1) for i in range(len(msds))]
    msds.index = times
    
    return msds

def get_num_traj_per_msd_point(metadata, data_dfs):
    msds = data_dfs['MSDTrajectories']
    s = ''
    for idx in range(len(msds.index)):
        count = int(msds.loc[msds.index[idx]].count())
        s += f'{idx}:{count},'
        # if idx % 10 == 0:
            # s += '\n'
    
    metadata["MSD num_traj_per_point"] = s
    
    return metadata, data_dfs

def get_time_str():
    return datetime.datetime.now().strftime("%b_%d_%Y_%H_%M_%S")

def N_gaussian(x, *args):
    As = args[0::3]
    sigs = args[1::3]
    mus = args[2::3]
    
    return np.sum(
        np.array(
            [A*gaussian(x,sig,mu) for A,sig,mu in zip(As, sigs, mus)]
        ),
        axis = 0
    )
  
def open_frames(filepaths) -> List[pims.tiff_stack.TiffStack_tifffile]:
    """
    Uses multithreaded execution to open several frames concurrently.

    Args:
        filepaths (list): list of paths to open

    Returns:
        List[pims.tiff_stack.TiffStack_tifffile]: list of opened frames
    """
    
    logging.info(f"Input filepaths: {filepaths}")
    
    if len(filepaths) > 1:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = executor.map(pims_open, filepaths)
    else:
        result = [pims_open(filepaths[0])]

    frames_list = [frames for frames in result]
    logging.debug(f"Frames list: {frames_list}")

    return frames_list

def pims_open(filepath):
    return pims.open(filepath)

def read_new_format(path, get_dfs = True):
    """
    Reads in previous information, including metadata and previous results

    Args:
        path (str): path of metadata.json file

    Returns:
        tuple: contains: metadata and data_dfs
    """
    
    # logging.info("Reading previous run...")
    
    with open(path,'r') as fin:
        data = fin.read()
    
    metadata = json.loads(data)
    if type(metadata) == list:
        # TODO: currently lossy operation
        metadata = metadata[-1]
    metadata, callbacks = compatibilize_metadata(metadata)
    metadata['metadata_path'] = path
    
    root_path = os.path.split(path)[0]
    data_dfs = {}
    
    if get_dfs:
        for csv_to_match in cfg["saved_csvs"]:
            csv_path = find_csv(root_path, csv_to_match)
            logging.debug(f"Found csv path: {csv_path}")
            if csv_path != "":
                data_dfs[csv_to_match] = pd.read_csv(csv_path, index_col=0)
            else:
                data_dfs[csv_to_match] = pd.DataFrame()
        
        data_dfs['trajectories_filtered'] = data_dfs['trajectories_filtered'].rename(columns={'frame.1':'frame'})
        data_dfs['trajectories'] = data_dfs['trajectories'].rename(columns={'frame.1':'frame'})

        for callback in callbacks:
            if callback:
                metadata, data_dfs = callback(metadata, data_dfs)

    return metadata, data_dfs

def read_old_format(path):
    raise NotImplementedError

def rolling_average(x,n):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[n:] - cumsum[:-n]) / float(n)

def search_regex_id(s, depth = 0):
    # depth is how far back the path is from the metadata.json file
    # depth > 0
    
    # def get_exp_id_from_path(path):
    # regex_match = re.search(r'CPR-ID-(\d+)',path)
    # if regex_match:
    #     return int(regex_match.group(1))
    # else:
    #     return -1
    
    # with groups
    # file_regexs = [r'CPR-ID-(\d+)', r'M(\d+\.?\d*)_X(\d+\.?\d*)_T(\d)(_L(\d+\.?\d*))?']
    file_regexs = [
        r'(CPR-ID-\d+)', 
        r'(M\d+\.?\d*_X\d+\.?\d*_T\d_?L?\d*\.?\d*)'
    ]
    
    for regex in file_regexs:
        regex_match = re.search(regex, s)
        if regex_match:
            found_idx = -1
            parts = pathlib.Path(s).parts
            for idx, folder in enumerate(parts):
                if re.search(regex, folder):
                    found_idx = idx
                    break
            to_add = ""
            if found_idx != -1 and found_idx + 4 - depth < len(parts):
                # concatenate subfolders containing more metadata
                # e.g.: extract "ambient" from subpath path
                # s = M7.5_X6.5_T1_L0.002\ambient\test\400ms\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_15_2025_11_27_27\metadata.json
                to_add = '-'.join(parts[found_idx+1:len(parts)-3+depth])
                to_add = '-' + to_add
            return regex_match.group(1) + to_add

    return ''

def solicit_input(categories: dict, suggestions = {}, width=15) -> Union[list, tkinter.Tk]:
    """
    Generates a window that asks user for input according to the input categories. 
    Categories has the form 'key':default_value (type gets inferred)
    Currently bools are not supported.
    If the user tries to input something that is not of the correct type,
    this function prevents the user from actually typing it in.

    Args:
        categories (dict): which categories to solicit input from

    Returns:
        Union[list, tkinter.Tk]: list of resulting values,
            and a Tk reference to be able to fully close the root.
    """
    logging.debug("Starting window for user input")
       
    def close():
        for key in entryVars.keys():
            type_ = type(categories[key])
            output[key] = type_(entryVars[key].get())
        
        logging.debug(f"Received user input of --\n{output}")
            
        root.quit()
        
    def select_all():
        for title in entryVars.keys():
            if type(entryVars[title]) == tkinter.IntVar:
                entryVars[title].set(1)
                
    def deselect_all():
        for title in entryVars.keys():
            if type(entryVars[title]) == tkinter.IntVar:
                entryVars[title].set(0)
       
    root = tkinter.Tk()
    
    entryVars = {}
    output = {}
    entries = []
    bool_count = 0
    row = 0
    for key in categories.keys():
        output[key] = None
    
    for idx, title in enumerate(categories.keys()):
        if title in suggestions:
            default_value = suggestions[title]
        else:
            default_value = categories[title]
            
        type_ = type(categories[title])
        
        label = tkinter.Label(root,text=title)
        label.grid(row=row,column=0, sticky='e')
        
        if type_ != bool:
            entrySVar = tkinter.StringVar(root)
            entrySVar.set(str(default_value))
            # make sure stringVar stays of the right type
            entrySVar.trace('w', lambda *_: entrySVar.set(check_string_type(entrySVar.get(), type_)))
            entryVars[title] = entrySVar
            
            entry = tkinter.Entry(root, textvariable=entrySVar, width=width)
            entries.append(entry)
            entry.grid(row=row,column=1)
            
        elif type_ == bool:
            entryBool = tkinter.IntVar(root)
            entryBool.set(default_value)
            entryVars[title] = entryBool
            
            entry = tkinter.Checkbutton(root, variable=entryBool)
            entries.append(entry)
            entry.grid(row=row,column=1)
        
            bool_count += 1
        
        row += 1
    
    if bool_count >= 2:
        tkinter.Button(root,
            text="Select All",
            command=select_all
        ).grid(row=row, column=0)
        tkinter.Button(root,
            text="Deselect All",
            command=deselect_all
        ).grid(row=row, column=1)
        row += 1
        
    tkinter.Button(root,
        text="Done",
        command=close
    ).grid(row=row, column=0, columnspan=2)
    
    entries[0].focus_set()
    root.mainloop()
            
    return output, root

def sort_by_date(s):
    path = s[0]
    date = re.search('[a-zA-Z]{3}_[0-9]{2}_[0-9]{4}_[0-9]{2}_[0-9]{2}_[0-9]{2}', path).group()
    date = datetime.datetime.strptime(date, "%b_%d_%Y_%H_%M_%S")
    return date

def sort_in_parallel(l1, l2, reverse = False, by_date = False):
    """
    Sorts l1 and l2 according to the items of l1.
    """
    if len(l1) != len(l2):
        raise RuntimeError
    
    if by_date:
        combined = sorted(zip(l1, l2), key=sort_by_date)
    else:
        combined = sorted(zip(l1, l2))

    l1_new = [l1 for l1, _ in combined]
    l2_new = [l2 for _, l2 in combined]
    
    if reverse:
        l1_new.reverse()
        l2_new.reverse()
        
        return l1_new, l2_new
        
    return l1_new, l2_new

def tight_layout(fig, pad = None):
    """
    Calls tight_layout on the figure, and then draws it.
    """
    if pad == None:
        fig.tight_layout()
    else:
        fig.tight_layout(pad=pad)

def truncate_emitters_by_frame(emitters: pd.DataFrame, frame: int, inclusive=True) ->  pd.DataFrame:
    logging.info(f"Truncating emitters to only those with frame >= {frame} (inclusive: {inclusive})")
    if inclusive:
        subset = emitters[emitters['frame'] >= frame]
    else:
        subset = emitters[emitters['frame'] > frame]
        
    return subset

def verify_original_video_file(file):
    # regex matches .tif file naming convention
    to_match = '^nf\d+_d\d+\.\d+_e\d+\.\d+_p\d+\.\d+_NDTiffStack\d*\.tif$'
    result = re.search(to_match, file)
    if result:
        return True
    return False
    
def verify_file_format(s: str):
    """
    Common format in video acquisition:
    nfX_dY_eZ_pW,
    where
    X: number of frames,
    Y: delay between frames (in ms),
    Z: exposure of each frame (in ms),
    W: power of laser for each frame
    
    This function checks whether the input string contains that format.

    Args:
        s (str): input string that 

    Returns:
        bool
    """
    checks = ['nf','d','e','p']
    
    items = s.split('_')
    for idx,item in enumerate(items):
        if idx >= len(checks):
            return True
        
        if checks[idx] not in item:
            return False
        
        try:
            float(item.replace(checks[idx],''))
        except ValueError:
            return False
        
    return True

def visualize_particle(trajectories, metadata, particle, frames_list = None, parent = None):
    """
    Given a partcicle's trajectory and metadata, find which video
    that particle came from, and display the appropriate subset of the video.

    Args:
        trajectories (pd.DataFrame): all trajectories
        metadata (dict): metadata of the particle
        particle (int): trackpy generated ID of particle

    Returns:
        tkinter.Tk: reference to root to be destroyed later.
    """
    logging.info(f"Visualizing particle: {particle}")
    
    trajectory = trajectories[trajectories['particle'] == int(particle)].copy(deep=True)

    memory = metadata["input parameters"]["Memory (frames)"]
    num_frames = metadata["number of frames"][0]
    files = metadata["files"]
    video, offset, video_idx = find_particle_video(trajectory, num_frames, memory, files)
    
    # traj_copy = copy.deepcopy(trajectory)
    # traj_copy['frame'] -= offset
    # print(traj_copy.__str__())
    
    if not frames_list:
        frames = pims.open(video)
    else:
        frames = frames_list[video_idx]
    print(frames)
    print(trajectory)
        
    trajectory['frame'] -= offset
    frame_bounds = [min(trajectory['frame']), max(trajectory['frame'])]
    
    if "Diameter (px)" in metadata["input parameters"].keys():
        diameter = metadata["input parameters"]["Diameter (px)"]
    else:
        diameter = cfg["categories"]['Diameter (px)'][0]
        
    if diameter == None:
        diameter = cfg["categories"]['Diameter (px)'][0]
    
    
    if parent == None:
        root = tkinter.Tk()
        root.protocol("WM_DELETE_WINDOW", lambda: root.quit())
        tifViewer = TIFViewer.TIFViewer(root, frames, trajectory, frame_bounds, diameter=diameter)
        tifViewer.pack(fill=tkinter.BOTH, expand=True)
        root.mainloop()
        return root
    else:
        tifViewer = TIFViewer.TIFViewer(parent, frames, trajectory, frame_bounds, diameter=diameter)
        return tifViewer

if __name__ == '__main__':
    fig, ax = get_figure(2,2)
    