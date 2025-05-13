import logging
logging.getLogger(__name__)

from . import config
cfg = config.load_config() # script uses config parameters

import json
import os
import pandas as pd
import numpy as np
import tkinter
import tkinter.messagebox
import trackpy
import scipy.stats
import copy
import scipy.optimize
from typing import Union, Callable, Iterable
from functools import total_ordering
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

np.random.seed(cfg["random_seed"])

from . import utils
from . import SPTprocessing
from . import MSDExplorer


def combined_box_rayleigh_distribution(x,sig,partition,a):
    return partition*rayleigh_distribution(x,sig) + (1-partition)*two_points_box_distribution(x,a)

def modified_rayleigh_distribution(x,sig1,A):
    return A*(x/sig1**2)*np.exp((-x**2)/(2*sig1**2))

FIT_METHODS = {
    'Modified Rayleigh':modified_rayleigh_distribution,
    'Hybrid':combined_box_rayleigh_distribution
}

@total_ordering
class PostProcessingJob:
    def __init__(self, path: str, old=False, regression_points=':'):
        logging.debug("Instantiated post-processing job.")

        self.data_dfs = {}
        if old == True:
            metadata, self.data_dfs = utils.read_old_format(path)
        else:
            metadata, self.data_dfs = utils.read_new_format(path)
            
        if type(metadata) == list:
            # opened metadata contains previously processed results
            self.all_metadata = metadata
        else:
            metadata['regression points'] = regression_points
            self.all_metadata = [metadata]
            
        self.opened_path = path

    def get_df(self, df: str) -> pd.DataFrame:
        return self.data_dfs[df]
    
    def get_regression_points(self):
        return self.get_last_metadata()['regression points']
    
    def get_metadata_item(self, item: str):
        return self.get_last_metadata()[item]
    
    def get_video_count(self):
        return len(self.get_metadata_item("files"))
    
    def get_frame_count(self,video_idx):
        return self.get_metadata_item("number of frames")[video_idx]
    
    def get_total_frame_count(self):
        return sum(self.get_metadata_item("number of frames"))
    
    def plot(self, which: Union[Callable, str], *args):
        """
        Calls plotting functions according to which ones were specified.
        Can either be a callable or a string that is "all".

        Args:
            which (Union[Callable, str]): which plot functions to execute

        Returns:
            result of called function(s)
        """
        if type(which) == str and which == 'all':
            result = plot_all(self.data_dfs, self.get_regression_points(), self.get_last_metadata())
        elif type(which) == function:
            result = which(*args)
        else:
            raise RuntimeError

        return result

    def recalculate(self):
        """
        Begins recalculation process, by soliciting user input.
        According to that input, reprocess the current job, and append
        the resulting metadata to the object.
        """
        logging.debug("Beginning recalculation")
        
        suggestions = self.get_last_metadata()["input parameters"]
        mitchell_mode_data = self.get_metadata_item('mitchell_mode_data')
        
        categories = copy.deepcopy(cfg["categories"])
        if mitchell_mode_data['mitchell_mode']:
            del categories['Min Mass']
            del categories['Diameter (px)']
        
        new_input, root_reference = utils.solicit_input(categories, suggestions=suggestions)

        if mitchell_mode_data['mitchell_mode']:
            new_input['Min Mass'] = None
            new_input['Diameter (px)'] = None
            
        root_reference.destroy()
        
        changed = find_dict_differences(self.get_last_metadata()["input parameters"], new_input)
        recalculation_level = find_recalculation_level(changed)
        
        self.data_dfs, metadata = SPTprocessing.execute_calculations(
                self.get_metadata_item("files"), new_input, mitchell_mode_data, recalculation_level, self.data_dfs, self.get_last_metadata())
        
        metadata['regression points'] = self.get_regression_points()

        self.all_metadata.append(metadata)
        
    def show_metadata(self):
        logging.debug("Showing current metadata")
        logging.info("\n"+json.dumps(self.all_metadata, indent=4))
    
    def save(self):
        logging.debug("Saving post-processing job")
        save_path = '/'.join(self.opened_path.split('/')[:-2])
        prefix = os.path.split(self.get_last_metadata()["files"][0])[1].split('.tif')[0]
        
        SPTprocessing.save_job(
            save_path=save_path, 
            prefix=prefix,
            metadata=self.all_metadata, 
            data_dfs=self.data_dfs)
        
    def get_root(self):
        return os.path.split(self.get_last_metadata()["files"][0])[0]
    
    def get_all_metadata(self):
        return self.all_metadata
    
    def get_last_metadata(self) -> dict:
        return self.all_metadata[-1]
    
    def get_id(self):
        return utils.search_regex_id(self.opened_path)
    
    def set_regression_points(self, other):
        logging.debug(f"Setting new regression points: {other}")

        self.get_last_metadata()['regression points'] = other
        self.all_metadata[-1]['regression points'] = other
    
    def jump_distance_calculation_scheme(self, scheme: str):
        pass
    
    def find_particle(self, loc_x=np.nan, loc_y=np.nan, plot='', particle=np.nan) -> int:
        logging.debug("Finding particle...")
        
        if particle is np.nan:
            options = {
                'msd':{
                    'data':self.data_dfs['MSDTrajectories'],
                    'cols':['x']
                },
                'traj': {
                    'data':self.data_dfs['trajectories_filtered'],
                    'cols':['x','y']
                },
            }
            
            particle = find_closest_particle(options[plot]['data'],options[plot]['cols'], (loc_x, loc_y))
        
        print_particle(self.data_dfs['trajectories'], self.all_metadata[-1], particle)
        
        root_reference = utils.visualize_particle(self.data_dfs['trajectories'], self.all_metadata[-1], particle)
        root_reference.destroy()
        
        return particle
    
    def show_extreme(self, extreme):
        if extreme not in ['fast','slow']:
            raise ValueError
        
        extreme_particles = find_extreme_particles(self.data_dfs['MSDTrajectories'], extreme = extreme)
        logging.info(f"200 {extreme}est particles: {extreme_particles}")
        trajectories_subset = self.data_dfs['trajectories'].copy(deep=True)
        trajectories_subset = trajectories_subset[trajectories_subset['particle'].isin(map(int, extreme_particles))]

        data_dfs_subset = {}
        
        data_dfs_subset['emitters'] = self.data_dfs['emitters']
        data_dfs_subset['trajectories'] = trajectories_subset
        data_dfs_subset['trajectories_filtered'] = trajectories_subset
        mitchell_mode_data = self.get_metadata_item('mitchell_mode_data')
        
        files = self.get_metadata_item("files")
        user_input = self.get_metadata_item("input parameters")
        
        data_dfs_subset, metadata_subset = SPTprocessing.execute_calculations(
            files, user_input, mitchell_mode_data, skip_step=3, dfs=data_dfs_subset, metadata=copy.deepcopy(self.get_last_metadata())
        )
        
        result = plot_all(data_dfs_subset, self.get_regression_points(), metadata_subset)
        return result

    def explore_msds(self):
        explorer = MSDExplorer.MSDExplorer(self.data_dfs, self.get_last_metadata())
        root_reference = explorer.get_root_reference()
        root_reference.destroy()
        
    def bifurcate(self):
        return plot_bifurcation(self.data_dfs['MSDTrajectories'],self.data_dfs['trajectories_filtered'], self.get_last_metadata())
    
    def __eq__(self, other):
        return self.get_metadata_item("input parameters")["Frame Delay (ms)"] == \
               other.get_metadata_item("input parameters")["Frame Delay (ms)"]
    
    def __lt__(self, other):
        # sort by frame delay
        return self.get_metadata_item("input parameters")["Frame Delay (ms)"] < \
               other.get_metadata_item("input parameters")["Frame Delay (ms)"]
               
    def __str__(self):
        return json.dumps(self.all_metadata,indent=4)

def find_extreme_particles(msds, cap =cfg["num_extreme_trajectories"], extreme='fast'):
    logging.info(f"Finding extremes: cap={cap} extreme={extreme}")
    
    particles = np.array(msds.columns)
    n_particles = len(particles)
    extreme_msds = np.zeros(n_particles)
    
    for idx, particle in enumerate(particles):
        last_point = msds[particle].dropna().iloc[-1]
        
        extreme_msds[idx] = last_point
        
    _, particles_sorted = utils.sort_in_parallel(extreme_msds, particles)

    if extreme == 'fast':
        return particles_sorted[-cap:]
    if extreme == 'slow':
        return particles_sorted[:cap]

def deconvolute_frames(df: Union[pd.DataFrame, pd.Series], num_frames_list: list, memory: int) -> Union[pd.DataFrame, pd.Series]:
    """
    Deconvolutes frames, when several videos were concatenated together.
    This is necessary because when concatenating videos, the frame number
    will continually increase to prevent collisions.
    
    Note that this calculation uses the script constant cfg["blank_frames"],
    which are added to prevent collisioning during linking process.

    Args:
        df (Union[pd.DataFrame, pd.Series]): input data
        num_frames_list (list): list containing number of frames per video

    Returns:
        Union[pd.DataFrame, pd.Series]: deconvoluted data
    """

    # TODO: implement memory in recalculation (since it's used in SPTprocessing.concatenate_emitters)
    logging.debug("Deconvoluting frames")
    
    df_copy = copy.deepcopy(df)
    vidArr = np.array(num_frames_list).cumsum()
    
    if type(df_copy) == pd.DataFrame:
        for idx in range(len(vidArr)-1):
            lower = vidArr[idx]+(idx+1)*(cfg["blank_frames"] + memory)
            upper = vidArr[idx+1]+(idx+1)*(cfg["blank_frames"] + memory)
            
            df_copy.loc[(df_copy['frame'] >= lower) & (df_copy['frame'] <= upper), 'frame'] -= lower
    else:
        for idx in range(len(vidArr)-1):
            lower = vidArr[idx]+(idx+1)*(cfg["blank_frames"] + memory)
            upper = vidArr[idx+1]+(idx+1)*(cfg["blank_frames"] + memory)
            df_copy[(df_copy >= lower) & (df_copy <= upper)] -= lower
        
    return df_copy

def find_recalculation_level(changed: list) -> int:
    """
    Finds at what level to make recalculations. This is performed
    with the cfg["recalculation_levels"] constant from config.py,
    which looks up the lowest level of recalculation necessary.

    Args:
        changed (list): list of parameters that were changed

    Returns:
        int: level at which to make recalculations
    """
    logging.debug("Finding recalculation levels")

    low = np.inf
    for item in changed:
        if cfg["recalculation_levels"][item] < low:
            low = cfg["recalculation_levels"][item]
    
    logging.info(f"Recalculation level: {low}")
    return low

def get_msd_noaverage(trajectory, delay, multiple = False, overlap = False):
    # delay: s, nmPerPix: nm
    # assuming no gaps
    particle = trajectory['particle'].iloc[0]
    msds = np.power((trajectory['y'] - trajectory['y'].iloc[0]),2) + np.power((trajectory['x'] - trajectory['x'].iloc[0]),2)
    msds = msds[1:]
    
    times = [delay*(i+1) for i in range(len(msds))]
    msds.index = times
    
    return msds

def get_all_msds_noaverage(traj, delay, umPerPix = None, multiple = False, overlap = False, cap = None):
    traj_copy = traj.copy(deep=True)
    msds_noaverage = []
    if umPerPix:
        traj_copy['x'] *= umPerPix
        traj_copy['y'] *= umPerPix
        
    particles = pd.unique(traj_copy['particle'])
    if cap and cap < len(particles):
        particles = particles[:cap]
        
    for particle in particles:
        this_traj = traj_copy[traj_copy['particle']==particle]
        msds_noaverage.append(get_msd_noaverage(this_traj, delay, multiple, overlap))
    
    df = pd.concat(msds_noaverage, axis=1)
    df.columns = particles
    return df

def plot_MSDs(
    msds, 
    emsds = None, 
    fig=None, 
    ax=None, 
    color='k', 
    alpha=None, 
    label='', 
    title='', 
    min_traj_frame_len = None, 
    modify_label = True,
    norm_x_val = 1,
    norm_y_val = 1,
    scale_alpha = 1,
    axes_labels = True,
    zorders = None,
    x_range = None,
    y_range = None,
    show_legend=True
):
    
    logging.info("Plotting MSDs...")

    if fig == None or ax == None:
        fig, ax = utils.get_figure()
    
    logging.debug(f"Number of MSDs: {len(msds.columns)}")
    # if msds.shape[1] > cfg["recommended_cap_msd"] and challenge_plot("MSD plot", msds.shape[1], recommended_number=cfg["recommended_cap_msd"]):
    if (msds.shape[1] > cfg["recommended_cap_msd"]):
        msds = reduce_MSDs(msds, cfg["recommended_cap_msd"])

    if emsds is not None:
        uncertainty = get_loc_uncertainty(emsds) # um
    
    if alpha == None:
        alpha = min(50/len(msds.columns), 1)
        logging.debug(f"Setting alpha value to: {alpha}")

    if modify_label:
        if label != '':
            label += f' (N={len(msds.columns)})'
        else:
            label += f'N={len(msds.columns)}'    

    # zorders are randomized
    if type(zorders) == list:
        for idx, col in enumerate(msds.columns):
            if min_traj_frame_len:
                ax.plot(msds.index[:min_traj_frame_len] / norm_x_val, msds[col][:min_traj_frame_len] / norm_y_val, color=color, alpha=alpha / scale_alpha, label=label, zorder=zorders[idx])
            else:
                ax.plot(msds.index / norm_x_val, msds[col] / norm_y_val, color=color, alpha=alpha / scale_alpha, label=label, zorder=zorders[idx])
        
    else:
        if min_traj_frame_len:
            ax.plot(msds.index[:min_traj_frame_len] / norm_x_val, msds.iloc[:min_traj_frame_len] / norm_y_val, color=color, alpha=alpha / scale_alpha, label=label)
        else:
            ax.plot(msds.index / norm_x_val, msds / norm_y_val, color=color, alpha=alpha / scale_alpha, label=label)
    # plot uncertainty circle
    # if emsds is not None:
        # ax.plot(emsds.index[0] / norm_x_val,uncertainty**2 / norm_y_val, marker='o', mec=color, mfc='white', label=label + ' Uncertainty')
    
    if not label and show_legend:
        utils.generate_legend(ax, loc='lower right')
    if title != '':
        ax.set_title(title)
    
    if axes_labels:
        ax.set_xlabel('Lag Time (s)')
        ax.set_ylabel(r'MSD (µm$^2$)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    if x_range is not None:
        ax.set_xlim(x_range[0] / norm_x_val, x_range[1] / norm_x_val)
    
    if y_range is not None:
        ax.set_ylim(y_range[0] / norm_y_val, y_range[1] / norm_y_val)
        
    utils.tight_layout(fig)
    return fig, ax, "MSDs"

def plot_eMSD(
    eMSDs, 
    fig=None, 
    ax=None, 
    plot_MSDs=False, 
    msds=None, 
    color='k', 
    label='', 
    title='', 
    num_points = None,
    x_range=None,
    y_range=None
):
    
    logging.info("Plotting eMSD...")
    
    if plot_MSDs and msds == None:
        raise RuntimeError
    
    if fig == None or ax == None:
        fig, ax = utils.get_figure()
    
    if plot_MSDs:
        plot_MSDs(msds, fig, ax)
    
    if num_points == None:
        ax.plot(eMSDs.index, eMSDs, marker='o', linestyle="None", color=color, label=label, markersize=cfg["point_size"])
    else:
        ax.plot(eMSDs.index[:num_points], eMSDs.iloc[:num_points], marker='o', linestyle="None", color=color, label=label, markersize=cfg["point_size"])
    
    # if title == '':
    #     ax.set_title("Ensemble MSD")
    if title != '':
        ax.set_title(title)
        
    ax.set_xlabel('Lag Time (s)')
    ax.set_ylabel(r'MSD (µm$^2$)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    if x_range is not None:
        ax.set_xlim(x_range[0], x_range[1])
    
    if y_range is not None:
        ax.set_ylim(y_range[0], y_range[1])
    
    utils.tight_layout(fig)
    
    return fig, ax, "eMSD"
    
def plot_traj(
    trajectories, 
    fig=None, 
    ax=None, 
    title=''
):
    
    logging.info("Plotting trajectories...")
    
    if fig == None or ax == None:
        fig, ax = utils.get_figure()

    count = len(trajectories['particle'].unique())
    # if count > cfg["recommended_trajectory_cap"] and challenge_plot("Trajectory plot", count, recommended_number=cfg["recommended_trajectory_cap"]):
    trajectories = reduce_trajectories(trajectories, cfg["recommended_trajectory_cap"])

    trackpy.plot_traj(trajectories, ax=ax, plot_style={'linewidth':2})
    
    if title != '':
        ax.set_title(title)

    ax.set_xlabel("x (px)")
    ax.set_ylabel("y (px)")

    # ax.set_aspect('equal')
    
    utils.tight_layout(fig)
    
    return fig, ax, "trajectories"

def plot_biases(trajectories, figs=None, axs=None):
    logging.info("Plotting pixel biases...")
    
    if figs == None or axs == None:
        figs = []
        axs = []
        for _ in range(2):
            fig, ax = utils.get_figure()
            figs.append(fig)
            axs.append(ax)

    pos_columns = ['x', 'y']  # column labels for the pixel bias plot
    trajectories[pos_columns].applymap(lambda x: x % 1)['x'].hist(ax=axs[0], figure=figs[0])
    trajectories[pos_columns].applymap(lambda x: x % 1)['y'].hist(ax=axs[1], figure=figs[1])
    axs[0].set_title("x pixel bias")
    axs[1].set_title("y pixel bias")
    
    utils.tight_layout(fig)
    
    return figs, axs, ["x_bias", "y_bias"]
    
def plot_powerlaw(
    eMSDs, 
    fig=None, 
    ax=None, 
    mode='log', 
    color='k', 
    label='', 
    regression_points=':', 
    title='', 
    num_points_display=None,
    msds=None,
    axes_labels=True,
    show_legend=True,
):

    logging.info(f"Plotting power law, mode = {mode}. Regression points: {regression_points}")

    if fig == None or ax == None:
        fig, ax = utils.get_figure()
        
    if msds is not None:
        plot_MSDs(msds, fig, ax,color=color)
    
    xs = eMSDs.index.values
    ys = np.array(eMSDs['msd'])
    
    # take subset of regression
    lower = 0
    upper = len(ys)
    if regression_points != ':':
        points = regression_points.split(':')
        if points[0] != '':
            lower = int(points[0])
        if points[1] != '':
            upper = int(points[1])

    values = pd.DataFrame(index=['n', 'A'])
    
    if mode == 'log':
        xs_to_fit = np.log(xs)[lower:upper]
        ys_to_fit = np.log(ys)[lower:upper]
    elif mode =='linear':
        xs_to_fit = xs[lower:upper]
        ys_to_fit = ys[lower:upper]
        
    result = scipy.stats.linregress(xs_to_fit, ys_to_fit)
    intercept = result.intercept
    slope = result.slope
    intercept_stderr = result.intercept_stderr
    logging.info(f"Uncertainty of intercept (no exponential propagation): {intercept_stderr}")

    if mode == 'log':
        values = [slope, np.exp(intercept)]
    elif mode == 'linear':
        values = [slope, intercept]

    if num_points_display != None:
        xs = xs[:num_points_display]
        ys = ys[:num_points_display]

    # raw data
    ax.plot(xs, ys, label='', marker='o', linestyle="None", color=color, markersize=cfg["point_size"])

    # fit data
    if mode == 'log':
        label += " (A: {0:0.3e}, n: {1:0.4f})".format(np.exp(intercept), slope)
        logging.info(f"Found regression values of: A={np.exp(intercept)}, n={slope}")

        ax.plot(xs, np.exp(intercept) * xs ** slope, marker='None', linestyle="-", color=color, label=label)
        ax.set_xscale('log')
        ax.set_yscale('log')
        
    elif mode == 'linear':
        label += "\nσ={0:0.1f}nm".format(np.sqrt(intercept)*1000)
        logging.info(f"Found regression values of: sig^2={intercept} um^2, sig={np.sqrt(intercept)*1000} nm")

        # ensure line goes through y-axis
        xs = np.insert(xs,0,0)
        ax.plot(xs, intercept + slope * xs, marker='None', linestyle="-", color=color, label=label)

        if show_legend:
            utils.generate_legend(ax, loc='lower right')

    # if title == '':
    #     title += f"{mode} plot\n"

    # if mode == 'log':
    #     title += f"A={round(np.exp(intercept), 6)}, n={round(slope, 6)}"
    # elif mode == 'linear':
    #     title += "\nsig={1:0.1f} nm".format(intercept, np.sqrt(intercept)*1000)
    
    ax.set_title(title)
    
    if axes_labels:
        ax.set_xlabel('Lag Time (s)')
        ax.set_ylabel(r'MSD (µm^2)')

    utils.tight_layout(fig)

    return fig, ax, f"powerlaw_{mode}", values

def reduce_MSDs(msds: pd.DataFrame, cap: int) -> pd.DataFrame:
    """
    Shuffle the msd columns, then select the first 0:cap columns
    as a random subset.

    Args:
        msds (pd.DataFrame)
        cap (int)

    Returns:
        pd.DataFrame: random subset of input MSDs
    """
    msds_copy = msds.copy(deep=True)
    columns = np.array(msds.columns)
    np.random.shuffle(columns)
    columns = columns[:cap]
    
    return msds_copy[columns]

def plot_jumps(trajectories, 
    jumps=None, 
    fig=None, 
    ax=None, 
    color='k', 
    bins=500, 
    fit_method='Modified Rayleigh', 
    title='', 
    label = '', 
    axes_labels = True,
    show_legend=True,
):

    logging.info(f"Plotting jump distribution, bins = {bins}")

    if fig == None or ax == None:
        fig, ax = utils.get_figure()
        
    if jumps == None:
        jumps = utils.calculate_jump_lengths(trajectories)

    if label != '':
        label = f"{label}\n(N={len(jumps)})"
    ax.hist(jumps, bins=bins, color=color, density=True, label=label, histtype='step', alpha=0.3)

    if fit_method in FIT_METHODS:
        freq, edges = np.histogram(jumps, bins=bins, density=True)
        xs = np.cumsum(np.diff(edges))
        xs -= xs[0]/2
        
        fitResult,_ = scipy.optimize.curve_fit(FIT_METHODS[fit_method], xs, freq)
        logging.info(f"Fit result: {fitResult} (N={len(jumps)})")

        ax.plot(xs,FIT_METHODS[fit_method](xs,*fitResult), label=f'Fit\n{round_list(fitResult, 3)}', color=color)
        if show_legend:
            utils.generate_legend(ax, loc='upper right')
    
    if axes_labels:
        ax.set_xlabel("x (px)")
        ax.set_ylabel("Frequency")
        
    # if title == '' and fit_method in FIT_METHODS:
    #     ax.set_title(f"Jump Length Distribution\nFit:{fitResult}")
    if title:
        ax.set_title(title)
    
    utils.tight_layout(fig)
    
    return fig, ax, "jump_distribution"

def plot_vertical_histogram(
    msds, 
    lag_frame, 
    fig=None, 
    ax=None, 
    color='k', 
    title='', 
    label='', 
    density=True, 
    bins=None, 
    scale_factor = 1,
    axes_labels = True,
    show_n = True,
):

    logging.info(f"Plotting vertical histogram, frame: {lag_frame}, density: {density}, bins: {bins}")
    
    if fig == None or ax == None:
        fig, ax = utils.get_figure()
    
    if bins == None:
        bins = cfg["num_histogram_bins"]

    try:
        this_data = np.array(msds.loc[msds.index[lag_frame],])
        if 0 in this_data:
            this_data = this_data[~(this_data==0)]
            
        this_data = np.log10(this_data)
        
        if label != '' and show_n:
            label += f' (N={len(msds.columns)})'
        elif show_n:
            label += f'N={len(msds.columns)}'
        
        ax.hist(
            this_data, 
            bins=bins, 
            color=color, 
            label=label, 
            density=density, 
            histtype='step', 
            weights = np.ones(len(this_data)) * scale_factor,
            linewidth=3
        )

        # utils.generate_legend(ax, loc='upper left')
        
    except IndexError:
        logging.warning("Error in vertical histogram plotting!")
    

    # freq, edges = np.histogram(this_data, bins=bins, density=True)
    # xs = np.cumsum(np.diff(edges))
    # xs -= xs[0]/2
    # p0 = [0.5, 1, -2, 0.5, 1, -3]
    # fitResult,_ = scipy.optimize.curve_fit(utils.N_gaussian, xs, freq, p0)
    
    # ax.plot(xs,utils.N_gaussian(xs,*fitResult), label = label + "(fit)")
    
    if axes_labels:
        ax.set_xlabel("log10(MSD)")
        if density:
            ax.set_ylabel("Probability")
        else:
            ax.set_ylabel("Counts")

    # if title == '':
    #     ax.set_title(f"Vertical histogram at frame: {lag_frame}")
    # else:
    #     ax.set_title(title)
    
    save_title = f"vertical_histogram_frame{lag_frame}"
    if density:
        save_title += "_w_density"
    else:
        save_title += "_w_counts"
    
    utils.tight_layout(fig)
    
    return fig, ax, save_title

def plot_emitter_counts_all(
    emitters, 
    num_frames_list, 
    memory, 
    fig=None, 
    ax=None, 
    color='k', 
    label='', 
    title='',
    show_legend=True,
):
    
    def exp_model(xs, A, k, baseline):
        return np.exp(-xs/k)*A + baseline
    
    def two_exp(xs, A1, k1, b1, A2, k2, b2, part):
        return part*exp_model(xs, A1, k1, b1) + (1-part)*exp_model(xs, A2, k2, b2)
    
    logging.info("Plotting emitter counts (all)...")

    if fig == None:
        fig, ax = utils.get_figure()
    
    frames = deconvolute_frames(emitters['frame'], num_frames_list, memory)
    
    # find where there are zero counts and populate them as such
    frames_bin, counts = np.unique(frames, return_counts=True)
    allFrames = np.array([i for i in range(num_frames_list[0])])
    allCounts = []
    for thisFrame in allFrames:
        if thisFrame in frames_bin:
            idx = np.where(frames_bin==thisFrame)[0][0]
            allCounts.append(counts[idx])
        else:
            allCounts.append(0)
            
    logging.info(f"Found {len(frames)}: emitters, average/frame: {np.average(allCounts)}, var: {np.var(allCounts)}")

    if label != '':
        label += f' (N={len(frames)})'
    else:
        label += f'N={len(frames)}'
    
    xs = allFrames[cfg["n_rolling_average"]//2-1:len(allFrames)-cfg["n_rolling_average"]//2]
    ys = utils.rolling_average(allCounts,cfg["n_rolling_average"])/len(num_frames_list)
    try:
        popt, _ = scipy.optimize.curve_fit(two_exp, xs[10:], ys[10:], bounds=((0,0,0,0,0,0,0),(np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,1)))
        logging.info(f"Fit popt for emitters:\nSet 1: {popt[:3]}\nSet 2:{popt[3:6]}\npartition:{popt[6]}")
        ax.plot(xs,two_exp(xs, *popt),color='dimgrey',label = label + " fit")
    except:
        logging.warning("Error in curve fitting of emitters, skipping plotting of fit...")
    ax.plot(xs, ys, color=color,label=label)
    
    if show_legend:
        utils.generate_legend(ax, loc='upper right')
    
    # if title == '':
    #     ax.set_title(f"Emitters vs. Time, all Emitters")
    if title != '':
        ax.set_title(title)

    ax.set_xlabel("Frame")
    ax.set_ylabel("Average #/frame")
    
    utils.tight_layout(fig)
    
    return fig, ax, "emitter_distribution_all"

def plot_emitter_counts_traj(
    traj, 
    num_frames_list, 
    memory, 
    fig=None, 
    ax=None, 
    color='k', 
    label='', 
    title='',
    show_legend=True,
):
        
    logging.info("Plotting emitter counts (traj)...")

    if fig == None:
        fig, ax = utils.get_figure()

    frames = deconvolute_frames(traj['frame'], num_frames_list, memory)
    
    # find where there are zero counts and populate them as such
    frames_bin, counts = np.unique(frames, return_counts=True)
    allFrames = np.array([i for i in range(num_frames_list[0])])
    allCounts = []
    for thisFrame in allFrames:
        if thisFrame in frames_bin:
            idx = np.where(frames_bin==thisFrame)[0][0]
            allCounts.append(counts[idx])
        else:
            allCounts.append(0)
            
    logging.info(f"Found {len(frames)}: emitters, average/frame: {np.average(allCounts)}, var: {np.var(allCounts)}")

    if label != '':
        label += f' (N={len(frames)})'
    else:
        label += f'N={len(frames)}'
        
    ax.plot(allFrames[cfg["n_rolling_average"]//2-1:len(allFrames)-cfg["n_rolling_average"]//2], 
            utils.rolling_average(allCounts,cfg["n_rolling_average"])/len(num_frames_list), 
            color=color,label=label)
    
    if show_legend:
        utils.generate_legend(ax)
    
    # if title == '':
    #     ax.set_title(f"Emitters vs. Time, emitters in trajectories")
    if title != '':
        ax.set_title(title)

    ax.set_xlabel("Frame")
    ax.set_ylabel("Average #/frame")
    
    utils.tight_layout(fig)
    
    return fig, ax, "emitter_distribution_traj"

def plot_trajectory_lengths(
    trajectories_filtered, 
    num_frames_list, 
    memory, 
    fig=None, 
    ax=None, 
    color='k', 
    label='', 
    title='', 
    table_var = {},
    show_legend=True,
):
        
    logging.info("Plotting emitter counts (traj)...")

    if fig == None:
        fig, ax = utils.get_figure()

    trajectories_filtered = deconvolute_frames(trajectories_filtered, num_frames_list, memory)
        
    particles = trajectories_filtered['particle']
    unique, counts = np.unique(particles,return_counts=True)
    
    #################################
    # Analyze distribution and memory
    #################################
    num_traj_w_memory = 0
    len_added = []
    
    for particle in np.unique(particles):
        this_trajectory = trajectories_filtered[trajectories_filtered['particle']==particle]
        expected_len = len(this_trajectory)
        
        diffs = this_trajectory['frame'].diff()
        total_len_added = sum(list(diffs[diffs > 1] - 1))
        if total_len_added > 0:
            len_added.append(total_len_added)
        actual_len = diffs.sum() + 1
        
        if expected_len != actual_len:
            num_traj_w_memory += 1

    message = "Trajectory length distribution information"
    message = "\n" + "-"*len(message) + '\n' + message + '\n' + "-"*len(message)
    message += f"\nTotal trajectory count: {len(unique)}, average/frame: {len(unique)/sum(num_frames_list)}\n"
    message += f"Average length: {np.average(counts)}\n"
    message += f"Min, max length: {np.min(counts)}, {np.max(counts)}\n"
    message += f"St. Dev. length: {np.std(counts)}\n"
    message += f"Mode length: {scipy.stats.mode(counts, keepdims=False).mode} (count={scipy.stats.mode(counts, keepdims=False).count})"
    logging.info(message)
    table_var['Total count'] = len(unique)
    table_var['Average/frame'] = len(unique)/sum(num_frames_list)
    table_var["Average length"] = np.average(counts)
    table_var["Min length"] = np.min(counts)
    table_var["Max length"] = np.max(counts)
    table_var["St. Dev. length"] = np.std(counts)
    table_var["Mode length"] = scipy.stats.mode(counts, keepdims=False).mode
    table_var["Mode count"] = scipy.stats.mode(counts, keepdims=False).count

    if memory != 0:
        message = "Memory information"
        message = "\n" + "-"*len(message) + '\n' + message + '\n' + "-"*len(message)
        message += f"\nMemory parameter used: {memory}\n"
        message += f"Number of trajectories with memory: {num_traj_w_memory} / {len(np.unique(particles))}\n"
        message += "Fraction of trajectories with memory: {0:.4f}\n".format(num_traj_w_memory / len(np.unique(particles)))
        if len(len_added) > 0:
            message += "Average length added by memory: {0:.4f}\n".format(sum(len_added) / len(len_added))
            message += f"Min, max added: {np.min(len_added)}, {np.max(len_added)}\n"
            message += f"St. Dev. length added: {np.std(len_added)}\n"
            message += f"Mode length added: {scipy.stats.mode(len_added, keepdims=False).mode} (count={scipy.stats.mode(len_added, keepdims=False).count})"
        else:
            message += f"Average length added by memory: {np.nan}"
            message += f"Min, max added: {np.nan}\n"
            message += f"St. Dev. length added: {np.nan}\n"
            message += f"Mode length added: {np.nan})"
        logging.info(message)
        

    
    if label != '':
        label += f' (N={len(unique)})'
    else:
        label += f'N={len(unique)}'

    ax.hist(counts, bins=np.logspace(np.log10(7),np.log10(1000), cfg["num_traj_len_bins"]),label=label, histtype='step', color=color)


    # if title == '':
    #     ax.set_title(f"Trajectory Length Comparison")
    if title != '':
        ax.set_title(title)
    ax.set_xscale("log")
    ax.set_xlabel("Log10(trajectory length)")
    ax.set_ylabel("Frequency")
    if show_legend:
        utils.generate_legend(ax, loc='upper right')
    
    utils.tight_layout(fig)
    
    return fig, ax, "trajectory_length_comparison"

def plot_bifurcation(msds, trajectories, metadata):
    # if metadata['bifurcation'] == [None, None]:
    fig, ax, _ = plot_MSDs(msds, title = "Select Point")
    point, root_reference = select_point(fig, ax)
    root_reference.destroy()
    
    above_bifurcation_msds = pd.DataFrame(index=msds.index)
    above_bifurcation_trajectories = pd.DataFrame()
    below_bifurcation_msds = pd.DataFrame(index=msds.index)
    below_bifurcation_trajectories = pd.DataFrame()
    
    for column in msds.columns:
        # interpolation is above selected point
        this_trajectory = trajectories[trajectories['particle']==int(column)]
        if np.interp(point[0],msds.index, msds[column]) > point[1]:
            above_bifurcation_msds[column] = msds[column]
            above_bifurcation_trajectories = pd.concat([above_bifurcation_trajectories, this_trajectory])
        else:
            below_bifurcation_msds[column] = msds[column]
            below_bifurcation_trajectories = pd.concat([below_bifurcation_trajectories, this_trajectory])
    
    emsds_above = pd.DataFrame(SPTprocessing.getEMsds(above_bifurcation_trajectories,metadata['input parameters']['nm Per Pixel'],metadata['input parameters']['Frame Delay (ms)']))
    emsds_below = pd.DataFrame(SPTprocessing.getEMsds(below_bifurcation_trajectories,metadata['input parameters']['nm Per Pixel'],metadata['input parameters']['Frame Delay (ms)']))
    
    regression_points = "0:7"
    # if metadata['regression points'] == ':':
    #     upper = metadata['input parameters']["Min. Traj. Len. (frames)"]
    #     regression_points = f"0:{upper}"
    # else:
    #     regression_points = ":"
    
    fig, ax,_, result_above = plot_powerlaw(emsds_above,regression_points=regression_points,msds=above_bifurcation_msds,color='k')    
    fig, ax,_, result_below = plot_powerlaw(emsds_below,regression_points=regression_points, fig=fig, ax=ax,msds=below_bifurcation_msds,color='r')    
    
    ax.set_title("Above: A={1:.4e}, n={0:.4f}\nBelow: A={3:.4e}, n={2:.4f}".format(*(result_above + result_below)))
    
    utils.tight_layout(fig)
    
    return fig, ax, "bifurcation"

def plot_drifts(
    drifts_list, 
    trajectories,
    memory, 
    num_frames
):
    if drifts_list.empty:
        fig, ax = utils.get_figure()
        ax.set_title("Drifts not computed.")
        return fig, ax, "drifts_list"
    
    num_rows = len(drifts_list.columns)//2
    
    fig, axs = utils.get_figure(
        row=num_rows, 
        col=2, 
        sharex = False, 
        sharey = False,
        fig_height=cfg["fig_height_show"]*num_rows/4,
        fig_width=cfg["fig_width_show"]
    )
    
    frame_offset = 1
    
    for i in range(num_rows):
        if num_rows == 1:
            ax = axs[0]
        else:
            ax = axs[i, 0]
        
        # Plot drifts
        xcol = f'x{i}'
        ycol = f'y{i}'
        x = drifts_list[xcol]
        y = drifts_list[ycol]
        
        ax.plot(x,y)
    
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        norm = plt.Normalize(0, len(x))
        lc = LineCollection(segments, cmap='viridis', norm=norm)
        lc.set_array(np.arange(0,len(x),1))
        lc.set_linewidth(2)
        line = ax.add_collection(lc)
        ax.set_aspect('equal')
        ax.set_xlim(drifts_list[xcol].min(), drifts_list[xcol].max())
        ax.set_ylim(drifts_list[ycol].min(), drifts_list[ycol].max())
        ax.set_xlabel("x (px)")
        ax.set_ylabel("y (px)")
        
        # Plot statistics
        if num_rows == 1:
            ax = axs[1]
        else:
            ax = axs[i, 1]
        
        traj_subset = trajectories[(trajectories['frame'] >= frame_offset) & (trajectories['frame'] < frame_offset + num_frames[i])]
        count_per_frame = np.unique(traj_subset['frame'], return_counts = True)[1]
        
        frame_offset += num_frames[i] + cfg["blank_frames"] + memory
        
        ax.plot(count_per_frame)
        ax.set_xlabel('Frame')
        ax.set_ylabel('Counts')
        

    # fig.colorbar(line, ax=ax)
    
    # fig.suptitle("Drifts")
    
    utils.tight_layout(fig)
    
    return fig, ax, "drifts_list"

def plot_all(data_dfs, regression_points, metadata):
    # package into commands so that they can all be executed nicely in a loop
    if metadata['drift_mode'] == 'all_trajectories':
        drift_trajectories = data_dfs['trajectories']
    elif metadata['drift_mode'] == 'trajectories_filtered':
        drift_trajectories = data_dfs['trajectories_filtered']
        
    msds = data_dfs['MSDTrajectories']
    emsds = data_dfs['eMSDs']
    traj = data_dfs['trajectories_filtered']
    emitters = data_dfs['emitters']
    num_frames = metadata["number of frames"]
    memory = metadata["input parameters"]["Memory (frames)"]
    delay = metadata["input parameters"]["Frame Delay (ms)"] / 1000
    drifts = data_dfs['drifts_list']
    
    
        
    cmds = [
        lambda: plot_MSDs(msds, emsds),
        lambda: plot_eMSD(emsds),
        lambda: plot_traj(traj),
        lambda: plot_biases(traj),
        lambda: plot_powerlaw(emsds, regression_points=regression_points, mode='log'),
        lambda: plot_powerlaw(emsds, regression_points=regression_points, mode='linear'),
        lambda: plot_jumps(traj),
        lambda: plot_vertical_histogram(msds, lag_frame=cfg["lag_frame"], density=True),
        lambda: plot_vertical_histogram(msds, lag_frame=cfg["lag_frame"], density=False),
        lambda: plot_emitter_counts_all(emitters, num_frames, memory),
        lambda: plot_emitter_counts_traj(traj, num_frames, memory),
        lambda: plot_trajectory_lengths(traj, num_frames, memory),
        lambda: plot_drifts(drifts, drift_trajectories, memory, num_frames)
    ]
    
    # if metadata["bifurcation"] != [None, None]:
        # cmds += [lambda: plot_bifurcation(data_dfs['MSDTrajectories'], data_dfs['trajectories_filtered'], metadata)]
    
    figs = {}
    axs = []
    for cmd in cmds:
        fig, ax, title, *_ = cmd()
            
        if type(fig) == list:
            for thisFig, thisAx, thisTitle in zip(fig, ax, title):      
                figs[thisTitle] = thisFig
                axs.append(thisAx)
        else:
            figs[title] = fig
            axs.append(axs)
        
    return figs, axs

def challenge_plot(title, number, recommended_number):
    root = tkinter.Tk()
    root.withdraw()
    answer = tkinter.messagebox.askyesno(title="Large plot", 
                                         message=f"{title} contains {number} items.\n" \
                                                   f"Recommended truncation: {recommended_number}. Truncate?")
    root.destroy()
    
    return answer

def print_particle(trajectories, metadata, particle):
    message = f'\n-------------------------\n'
    message += f'Printout of particle: {particle}\n'
    
    trajectory = trajectories[trajectories['particle'] == int(particle)]
    jumps = utils.calculate_jump_lengths(trajectory)
    
    memory = metadata["input parameters"]["Memory (frames)"]
    num_frames = metadata["number of frames"][0]
    files = metadata["files"]
    video, offset, _ = utils.find_particle_video(trajectory, num_frames, memory, files)
    
    message += f'Number of steps: {len(trajectory)}\n'
    message += f'Average step length: {np.average(jumps)}\n'
    message += f'All steps: {jumps}\n'
    message += f'Particle located in video: {video}\n'
    message += f"Frame start, end: {min(trajectory['frame']) - offset}, {max(trajectory['frame']) - offset}\n"
    message += f'-------------------------'
    
    logging.info(message)

def reduce_trajectories(trajectories: pd.DataFrame, cap: int) -> pd.DataFrame:
    """
    Determine the unique particles, shuffle them, then return the trajectories
    pertaining to those the subset 0:cap of those particles.

    Args:
        trajectories (pd.DataFrame)
        cap (int)

    Returns:
        pd.DataFrame: random subset of input trajectories
    """
    trajectories_copy = trajectories.copy(deep=True)
    
    particles = np.array(trajectories_copy['particle'].unique())
    np.random.shuffle(particles)
    particles = particles[:cap]
    
    return trajectories_copy[trajectories_copy['particle'].isin(particles)]

def two_points_box_distribution(r,a):
    """
    Distribution of interparticle spacing, r, resulting when
    uniformly generating points in a 2D box.
    
    This is slightly more complicated that one might expect since there is
    a piecewise relationship that forms when points are outside the maximum
    circle that can be drawn inside the box.
    
    Solution implemented from: https://people.kth.se/~johanph/habc.pdf

    Args:
        r: interparticle spacing
        a: size of box

    Returns:
        probability of event
    """
    return np.piecewise(
        r,
        [
            r < 0,
            ((r >= 0) & (r < a)), 
            ((r >= a) & (r < np.sqrt(2*a**2))), 
            r >= np.sqrt(2*a**2)],
        [
            lambda _: 0,
            lambda r: 2*r*(((a**2)*np.pi-4*a*r+r**2)/a**4),
            lambda r: 2*r*(-2/a**2+(4/a**2)*np.arcsin(a/r)+(4/a**3)*np.sqrt(r**2-a**2)-np.pi/a**2 - r**2/a**4),
            lambda _: 0
        ]
    )

def rayleigh_distribution(x,sig1,):
    return (x/sig1**2)*np.exp((-x**2)/(2*sig1**2))

def find_closest_particle(data, columns, point):
    """
    Finds the closest particle on the graph, given data and the type of graph
    TODO: probably not call it columns
    Parameters
    ----------
    data: graph data
    columns: whetehr or not to match exactly which columns
    point: point to find closest match to

    Returns particle index
    -------
    """
    if columns == ['x']:
        xtemp = (data.index - point[0]) ** 2
        ytemp = (data - point[1]) ** 2
        distances = ytemp.add(xtemp, axis='index') ** 0.5
        return distances.stack().idxmin()[1]
    elif columns == ['x', 'y']:
        distances = ((data['x'] - point[0]) ** 2 + (data['y'] - point[1]) ** 2) ** 0.5
        idx = np.where(distances.values == distances.min())
        closestPoint = data.iloc[idx]
        return int(closestPoint['particle'])

def get_loc_uncertainty(eMSDs, regression_points = '0:5'):
    xs = eMSDs.index.values
    ys = np.array(eMSDs['msd'])
    
    lower = 0
    upper = len(ys)
    if regression_points != ':':
        points = regression_points.split(':')
        if points[0] != '':
            lower = int(points[0])
        if points[1] != '':
            upper = int(points[1])
            
    xs_to_fit = xs[lower:upper]
    ys_to_fit = ys[lower:upper]
    
    _, intercept, *_ = scipy.stats.linregress(xs_to_fit, ys_to_fit)
    
    uncertainty = np.sqrt(intercept) # in um
    
    return uncertainty

def find_dict_differences(d1: dict, d2: dict) -> list:
    """
    Assuming that the dictionaries have the same keys,
    determine which key-value pairs are different

    Args:
        d1 (dict)
        d2 (dict)

    Returns:
        list: list of keys that were different
    """
    
    differences = []
    
    for key in d1.keys():
        if d1[key] != d2[key]:
            differences.append(key)
            
    return differences

def select_point(fig, ax):
    def click(event):
        if fig.canvas.toolbar.mode == "":
            root.quit()
            nonlocal output
            output +=  [event.xdata, event.ydata]

    output = []
    
    root = tkinter.Tk()
    
    plot_canvas = FigureCanvasTkAgg(fig, master=root)
    plot_canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
    
    fig.canvas.mpl_connect('button_release_event', click)
    
    NavigationToolbar2Tk(plot_canvas, root)
    
    plot_canvas.draw_idle()
    
    root.mainloop()
    
    return output, root

def round_list(l: Iterable, decimals: int, scientific = False):
    return list(np.round(np.array(l), decimals=decimals))

if __name__ == '__main__':
    pass
    