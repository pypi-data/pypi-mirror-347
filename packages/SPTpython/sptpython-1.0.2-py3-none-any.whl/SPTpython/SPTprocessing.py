import logging
logging.getLogger(__name__)

from . import config
cfg = config.load_config() # script uses config parameters

import trackpy
import tkinter
import tkinter.filedialog
import concurrent.futures
import itertools
import pandas as pd
import numpy as np
import json
import os
import pathlib
import psutil
import copy
import warnings
from typing import List
import re

from . import utils
from .version import __version__

def queue_processing(job_count, mitchell_mode):
    """
    Solicits user input for each job, adding them to a list to be
    unpacked later

    Args:
        job_count (int): number of jobs

    Returns:
        list: job list
    """
    logging.info("Starting processing queue")
    
    if mitchell_mode: 
        message = "Select Output from Mitchell's Code"
    else:
        message = 'Select .tif files'
    
    jobs = []
    previous_data_paths = []
    files = []
    
    for _ in range(job_count):
        root = tkinter.Tk()
        root.withdraw()
        
        if mitchell_mode:
            outer_folder = tkinter.filedialog.askdirectory(title="Select folder containing csvs")
            previous_data_paths = [os.path.join(outer_folder, file) for file in os.listdir(outer_folder) if file.endswith('.csv')]
            # previous_data_paths = tkinter.filedialog.askopenfilenames(title=message)
            
            # guess location of previous videos, should be one directory up.
            need_manual_input = False
            videos_path = pathlib.Path(previous_data_paths[0]).parents[1]
            files = ['']*len(previous_data_paths)
            
            for idx,previous_data_path in enumerate(previous_data_paths):
                number_to_match = get_file_number(previous_data_path,'.csv')
                for file in os.listdir(videos_path):
                    if utils.verify_original_video_file(file):
                        video_number = get_file_number(file,'.tif')
                        if video_number == number_to_match:
                            files[idx] = os.path.join(videos_path, file)
            if '' in files:
                need_manual_input = True
            else:
                logging.info("Manual input found associations:")
                for previous_data_path, file in zip(previous_data_paths, files):
                    logging.info(f"{previous_data_path} -> {file}")
            
            
            if need_manual_input:
                files = tkinter.filedialog.askopenfilenames(title = "Select associated videos")

                if len(previous_data_paths) != len(files):
                    logging.error(f"Invalid number of files selected! Expected: {job_count}, got {len(previous_data_paths)} outputs and {len(files)} video files.")
                    raise RuntimeError
                
                # ensure that videos/outputs get paired properly
                file_sort_dict = {}
                for i in range(len(previous_data_paths)):
                    file_sort_dict[previous_data_paths[i]] = i
                    file_sort_dict[files[i]] = i
            
                file_sorted, root_reference = utils.solicit_input(file_sort_dict)
                root_reference.destroy()
                
                previous_data_paths_idxs = [file_sorted[previous_path] for previous_path in previous_data_paths]
                files_idxs = [file_sorted[file] for file in files]
            
                _, previous_data_paths = utils.sort_in_parallel(previous_data_paths_idxs, previous_data_paths)
                _, files = utils.sort_in_parallel(files_idxs, files)
            
        else:
            files = tkinter.filedialog.askopenfilenames(title = message)
        
        
        suggestions = {}
        
        # grab the float in front of the d in the file name
        regex = r'nf\d+_d(\d+\.\d+)_e\d+\.\d+_p\d+\.\d+_NDTiffStack\d*\.tif$'
        delay = float(re.search(regex, files[0]).group(1))
        suggestions['Frame Delay (ms)'] = delay
        
        categories = copy.deepcopy(cfg["categories"])
        
        if mitchell_mode:
            del categories['Min Mass']
            del categories['Diameter (px)']
            
        user_input, root_reference = utils.solicit_input(categories, suggestions = suggestions)
        root_reference.destroy()
        
        if user_input['Custom Drifts']:
            path = tkinter.filedialog.askopenfilename(title="Select custom drift file")
        else:
            path = None
            
        jobs.append([files, user_input, {'mitchell_mode':mitchell_mode, 'path':previous_data_paths}, path])
    
    logging.debug(f"Jobs received: \n{jobs}")
    return jobs

def localize_emitter_files(frames_list: list, diameter_list: List[int], min_mass_list: List[float]) -> List[pd.DataFrame]:
    """
    Uses multiprocessing execution to localize several videos at once.

    Args:
        frames_list (list): frames to use in localization
        diameter_list (List[int]): diameter (odd int)
        min_mass_list (List[float]): list of min masses to use

    Returns:
        List[pd.DataFrame]: _description_
    """
    logging.info("Localizing emitters...")

    if len(frames_list) == 1:
        if type(frames_list) is itertools.repeat:
            frames_list = [frames_list.__next__()]
            
        if type(diameter_list) is itertools.repeat:
            diameter_list = [diameter_list.__next__()]
            
        if type(min_mass_list) is itertools.repeat:
            min_mass_list = [min_mass_list.__next__()]
            
        # no multiprocessing necessary
        return [localize_emitters(frames_list[0], diameter_list[0], min_mass_list[0])]
    
    multiprocessing_success = True
    
    # check anticipated file sizes
    total_size = 0
    free_memory = psutil.virtual_memory()[1]
    for frames in frames_list:
        filename = frames._filename
        this_size = os.path.getsize(filename)
        if this_size > free_memory:
            logging.error("Single video file size greater than available memory!")
            raise MemoryError
        total_size += this_size
        
    # do multicore processing
    if total_size < free_memory:
        logging.info("Beginning multicore processing...")
        with concurrent.futures.ProcessPoolExecutor() as executor:
            result = []
            try:
                frames = list(map(list, frames_list))
                for thisResult in executor.map(localize_emitters, frames, diameter_list, min_mass_list):
                    try:
                        result.append(thisResult)
                    except MemoryError:
                        pass
            except concurrent.futures.process.BrokenProcessPool:
                logging.exception("Memory error in multiprocessing. Switching to single core processing...")
                multiprocessing_success = False

    # do single core processing
    if not multiprocessing_success or total_size >= free_memory:
        logging.info("Beginning single core processing...")
        result = []
        for i,(frames,diameter,minMass) in enumerate(zip(frames_list,diameter_list,min_mass_list)):
            logging.info(f"On video: {i+1}/{len(frames_list)}")
            result.append(localize_emitters(frames,diameter,minMass))

    logging.info("Returning result of emitters localization")

    return result

def localize_emitters(frames, diameter, minMass):
    trackpy.feature.logger.disabled = True
    
    # catch expected warning indicating no emitters were found in a particular frame
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        output = trackpy.batch(list(frames), diameter, minmass=minMass, processes=1)
    
    return output

def concatenate_emitters(emitters_list: List[pd.DataFrame], num_frames_list: List[int], memory: int) -> pd.DataFrame:
    """
    Concatenates the results of several localizations

    Args:
        emitters_list (List[pd.DataFrame]): list of localizations
        num_frames_list (List[int]): list of number of frames per video
        memory (int): memory to be used in linking process

    Returns:
        pd.DataFrame: single DataFrame of concatenated emitters
    """

    logging.info("Concatenating emitters...")
    emitters = pd.DataFrame()
    
    total_frames = 0
    for i, temp in enumerate(emitters_list):
        if i != 0:
            # collision handling
            temp['frame'] = temp['frame'] + total_frames

        # this calculation is made to offset the frames such that trajectories do not get linked in between videos
        total_frames += num_frames_list[i] + memory + cfg["blank_frames"]
        if not temp.empty:
            emitters = pd.concat([emitters, temp], ignore_index=True)
    
    return emitters

def link_trajectories(emitters, jump_distance, memory):
    logging.info("Starting trajectory linking...")

    trackpy.linking.linking.logger.disabled = True

    return trackpy.link_df(emitters, jump_distance, memory=memory)

def filterTrajectories(trajectories, minTrajFrameLength):
    logging.info("Starting trajectory filtering...")
    trajectories_filtered = trackpy.filter_stubs(trajectories, minTrajFrameLength)
    
    return trajectories_filtered

def getMSDTrajectories(trajectories, nmPerPix, delay, memory):
    msds = trackpy.imsd(trajectories, nmPerPix / 1000, 1000/delay)
    if memory:
        msds[msds==0]=np.nan
    
    return msds

def getEMsds(trajectories, nmPerPix, delay):
    return trackpy.emsd(trajectories, nmPerPix / 1000, 1000/delay)

def correct_drift(trajectories, driftCorrection, numFrames, memory, custom_drift = None):
    if driftCorrection == 0:
        return trajectories, pd.DataFrame()
    else:
        return compute_drifts(trajectories, driftCorrection, numFrames, memory, custom_drift = custom_drift)
        # return trackpy.subtract_drift(trajectories,trackpy.compute_drift(trajectories,driftCorrection))
    # # Apply drift correction
    # if self.driftCorrectionFrames != 0:
    #     print("HERE")
    #     self.trajectories_filtered = self.computeDrifts()
    #     # filter again to see if any trajectories
    #     self.trajectories_filtered = tp.filter_stubs(self.trajectories_filtered, self.minTrajFrameLength)

def compute_drifts(trajectories_filtered, driftCorrectionFrames, numFrames, memory, custom_drift = None):
    drifts_list = []
    filtered_list = []
    traj = trajectories_filtered.copy(deep = True)
    if driftCorrectionFrames == 0:
        return traj

    frameStart = 0
    if custom_drift:
        previous_drifts = pd.read_csv(custom_drift, index_col = 0)
    for idx,videoLength in enumerate(numFrames):
        frameEnd = frameStart + videoLength
        trajSubset = traj[(traj['frame'] >= frameStart) & (traj['frame'] < frameEnd)]

        if custom_drift:
            drifts = previous_drifts[[f'y{idx}',f'x{idx}']].rename(columns={f'y{idx}':'y',f'x{idx}':'x'})
        else:
            drifts = trackpy.compute_drift(trajSubset,
                                        smoothing=driftCorrectionFrames)
        filtered = trackpy.subtract_drift(trajSubset, drifts)

        # sometimes drift subtraction will not apply correctly if implicated emitters aren't continuous across the video
        # (ex.: if there are empty frames)
        # This results in the first frame(s) of a trajectory not having an associated drift value,
        # resulting in discontinuous jumps in the trajectories
        # To remedy this, we determine which portions of trajectories don't have associated drift values,
        # and remove them.
        # missing_drifts = list(set(filtered.index).difference(set(drifts.index)))
        # filtered = filtered.drop(axis=0,index=missing_drifts)

        filtered_list.append(filtered)
        
        if not custom_drift:
            drifts.index = drifts.index - frameStart
        drifts_list.append(drifts)
        
        frameStart += videoLength + cfg["blank_frames"] + memory

    all_drifts = pd.concat(drifts_list, axis=1)
    column_names = []
    for i in range(len(numFrames)):
        column_names += [f'y{i}', f'x{i}']
    all_drifts.columns = column_names
    return pd.concat(filtered_list), all_drifts

def save_job(save_path, prefix, metadata, data_dfs):
    logging.info("Exporting data...")
    time = utils.get_time_str()
    folder = prefix + '_' + time
    
    folder_path = os.path.join(save_path, folder)
    os.mkdir(folder_path)

    with open(os.path.join(folder_path,'metadata.json'),'w') as fout:
        fout.write(json.dumps(metadata))
    
    for df in data_dfs.keys():
        path = os.path.join(folder_path, df + '.csv')
        data_dfs[df].to_csv(path)

def execute_calculations(files: List[str], user_input: dict, mitchell_mode_data, skip_step=0, dfs=None, metadata=None, custom_drifts = None):
    """
    Executes calculations of a job. If reprocessing, can skip certain steps according to skip_step
    (higher values indicate more steps skipped)

    Args:
        files (List[str]): list of files to use in calculation
        user_input (dict): processing parameters to use in calculation
        skip_step (int, optional): how many steps to skip. Defaults to 0.
        dfs (List[pd.DataFrame], optional): if skipping steps, previous calculations to use. Defaults to None.
        metadata (dict, optional): if skipping steps, previous metadata to use. Defaults to None.

    Raises:
        RuntimeError: raises error if attempting to skip steps but previous information was not passed in

    Returns:
        tuple: list of dataframes containing calculation results as well as associated metadata.
    """
    if skip_step > 0 and (dfs == None or metadata == None):
        raise RuntimeError

    if dfs is not None:
        data_dfs = copy.deepcopy(dfs)
        uniqueTrajNumber = metadata['trajectories no filter']
        uniqueTrajNumberFiltered = metadata['trajectories filter']
        num_frames_list = metadata['number of frames']
    else:
        data_dfs = {}
    
    if mitchell_mode_data['mitchell_mode']:
        minMass = None
        diameter = None
    else:
        minMass = user_input['Min Mass']
        diameter = user_input['Diameter (px)']
    
    nmPerPix = user_input['nm Per Pixel']
    delay = user_input['Frame Delay (ms)']
    minTrajFrameLen = user_input['Min. Traj. Len. (frames)']
    jump_distance = user_input['Jump Distance (px)']
    driftCorrection = user_input['Drift Correction (frames)']
    memory = user_input['Memory (frames)']
    emitterTrajTruncate = user_input['Trajectories: only consider emitters with frame >={input}']
    
    if skip_step < 1 and not mitchell_mode_data['mitchell_mode']:
        frames_list = utils.open_frames(files)
        num_frames_list = [len(frames) for frames in frames_list]
        emitters_list = localize_emitter_files(frames_list,
                            itertools.repeat(diameter), 
                            itertools.repeat(minMass))
        
        emitters = concatenate_emitters(emitters_list, num_frames_list, memory)
        data_dfs['emitters'] = emitters
        
    elif mitchell_mode_data['mitchell_mode']:
        # open output from Mitchell's code and compatibilize
        
        num_frames_list = []
        for file in files:
            match = re.search(r'nf(\d+)_d\d+.\d+_e\d+.\d+_p\d+.\d_NDTiffStack\d*\.tif$', file)
            if match:
                num_frames_list.append(int(match.group(1)))
            else:
                raise RuntimeError(f"Invalid file name: {file}")
        
        data_paths = mitchell_mode_data['path']
        datas = [pd.read_csv(data_path) for data_path in data_paths]

        for i in range(len(datas)):
            datas[i] = datas[i].drop(columns = [
                    'sigma [nm]', 
                    'var x', 
                    'var y', 
                    'xy covariance', 
                    'squared distance', 
                    'uncertainty [nm]', 
                    'offset [photon]',
                    'bkgstd [photon]',
                    'uncertainty [nm]',
                    'id',
                    'emitter index'
                ])
            
            datas[i].columns = ['frame','mass','x','y']
            
            # Problem: Mitchell's code uses MATLAB, so localizations start on frame=1,
            # but this code starts indexing by 0, so subtract 1 off here.
            datas[i].frame -= 1
            datas[i][['x','y']] /= nmPerPix
            
        emitters = concatenate_emitters(datas, num_frames_list, memory)
        data_dfs['emitters'] = emitters
    
    if skip_step < 2:
        if emitterTrajTruncate > 0:
            emitters = utils.truncate_emitters_by_frame(data_dfs['emitters'], emitterTrajTruncate)
        else:
            emitters = data_dfs['emitters']
        
        trajectories = link_trajectories(emitters, jump_distance, memory)
        data_dfs['trajectories'] = trajectories
    
    if skip_step < 3:
        drift_mode = cfg["drift_mode"]
        
        if custom_drifts:
            logging.info(f"Using custom drift file: {custom_drifts}")
            traj, drifts_list = correct_drift(data_dfs['trajectories'], driftCorrection, num_frames_list, memory, custom_drift = custom_drifts)
            data_dfs['drifts_list'] = drifts_list
            
        if drift_mode == 'all_trajectories' and not custom_drifts:
            logging.info(f"Correcting drift, mode: {drift_mode}")
            traj, drifts_list = correct_drift(data_dfs['trajectories'], driftCorrection, num_frames_list, memory)
            data_dfs['drifts_list'] = drifts_list
        else:
            traj = data_dfs['trajectories']
        
        trajectories_filtered = filterTrajectories(traj, minTrajFrameLen)
        
        if drift_mode == 'trajectories_filtered' and not custom_drifts:
            logging.info(f"Correcting drift, mode: {drift_mode}")
            trajectories_filtered, drifts_list = correct_drift(trajectories_filtered, driftCorrection, num_frames_list, memory)
            data_dfs['drifts_list'] = drifts_list
            
        data_dfs['trajectories_filtered'] = trajectories_filtered
    
    if skip_step < 4:
        if skip_step > 1:
            trajectories = data_dfs['trajectories']
            
        data_dfs['trajectories_filtered'] = trajectories_filtered
        
        uniqueTrajNumber = trajectories['particle'].nunique()
        uniqueTrajNumberFiltered = trajectories_filtered['particle'].nunique()

        logging.info(f"Before: {uniqueTrajNumber}")
        logging.info(f"After: {uniqueTrajNumberFiltered}")
    
    if skip_step < 5:
        MSDTrajectories = getMSDTrajectories(data_dfs['trajectories_filtered'], nmPerPix, delay, memory)
        data_dfs['MSDTrajectories'] = MSDTrajectories

    if skip_step < 6:
        ensembleMSD = trackpy.emsd(data_dfs['trajectories_filtered'], nmPerPix / 1000, 1000/delay)
        ensembleMSDFrame = ensembleMSD.to_frame()
        data_dfs['eMSDs'] = ensembleMSDFrame
    
    metadata = get_metadata(user_input, files, data_dfs['emitters'], uniqueTrajNumber, uniqueTrajNumberFiltered, num_frames_list, mitchell_mode_data)
    return data_dfs, metadata

def get_metadata(user_input, files, emitters, uniqueTrajNumber, uniqueTrajNumberFiltered, num_frames_list, mitchell_mode_data):
    return {
        "input parameters":user_input,
        "files":files,
        "number of emitters":len(emitters),
        "trajectories no filter":uniqueTrajNumber,
        "trajectories filter":uniqueTrajNumberFiltered,
        "number of frames":num_frames_list,
        "drift_mode":cfg["drift_mode"],
        "mitchell_mode_data":mitchell_mode_data,
        "SPTpython version":__version__
    }
    
def get_file_number(file, extension = ''):
    # grabs the number on the end of a string
    
    # old naming convention where first file was not numbered, but the rest were
    if file[-len(extension)-1] == 'k':
        return 1
    
    to_match = f'\d+\{extension}$'
    num = re.search(to_match, file).group()
    return int(num[:-len(extension)])

def process_job(job):
    files = job[0]
    user_input = job[1]
    mitchell_mode_data = job[2]
    custom_drifts = job[3]
    
    data_dfs, metadata = execute_calculations(files, user_input, mitchell_mode_data, custom_drifts = custom_drifts)
    
    save_path = os.path.split(files[0])[0]
    prefix = os.path.split(files[0])[1].split('.tif')[0]
    
    save_job(save_path, 
             prefix,
             metadata, 
             data_dfs)
    
    logging.info("Job done.")