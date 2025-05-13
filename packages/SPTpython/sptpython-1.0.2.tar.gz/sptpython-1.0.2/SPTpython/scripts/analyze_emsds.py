import logging
import logging.config

from SPTpython import postprocessing
from SPTpython import SliderCombo
import SPTpython.utils as utils
from SPTpython.CLI import resize_figure
from SPTpython.math.distribution_functions import *

if __name__ == '__main__':
    from SPTpython.scripts.drive_simulation import Simulation
from SPTpython.scripts.analyze_simulations import read_dream_fits

import tkinter.filedialog
import tkinter

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import json
import copy
from itertools import repeat
import pathlib

import scipy.special
import scipy.optimize

##################
# SCRIPT CONSTANTS
##################

MODES = [
    "2gauss",
    "2chi",
    "distributed_D"
]

MODE = MODES[0]
BYPASS = False
    
CONFIG = {
    "2gauss":{
        "var_names":["D1","D2","Partition","Sigma"],
        "bounds":((0,0,0,0),(np.inf,np.inf,1,np.inf)),
        "p0":(0,1e-5, 0.9,0.018),
        "formats":["{:.2E}","{:.2E}","{:.2f}","{:.1f}"],
        "units":["µm$^2$/s","µm$^2$/s","","nm"],
        "function":two_log10exponential_w_uncertainty,
        "expected_val_function":expected_2log10_exp,
        "jac_fun":jac_2exp,
        "msd_average_mode":"notimeavg"
    },
    "2chi":{
        "var_names":["k1", "D2", "k2", "Partition", "sigma"],
        "bounds":((0,0,0,0,0),(np.inf,np.inf,np.inf,1,np.inf)),
        "p0":(2.3,0.00297,0.55,0.74,0.016),
        "formats":["{:.2E}","{:.2E}","{:.2E}","{:.2f}","{:.1f}"],
        "units":["","µm$^2$/s","","","nm"],
        "function":two_log10_chis,
        "expected_val_function":expected_2log10_chi,
        "jac_fun":jac_2chi,
        "msd_average_mode":"timeavg"
    },
    "distributed_D":{
        "var_names":["k1", "k2", "lam", "a","sigma"],
        "bounds":((0,0,0,0,0),(1,np.inf,np.inf,1,np.inf)),
        "p0":(0.016,2,2,500,0.8),
        "formats":["{:.1f}","{:.1f}","{:.1f}","{:.2f}","{:.1f}"],
        "units":["","","","","nm"],
        "function":distributed_D_and_log10chi,
        "jac_fun":None,
        "msd_average_mode":"timeavg"
    }
}

VAR_NAMES = CONFIG[MODE]['var_names']
BOUNDS = CONFIG[MODE]['bounds']
p0 = CONFIG[MODE]['p0']
FORMATS = CONFIG[MODE]["formats"]
UNITS = CONFIG[MODE]["units"]
FIT_FUNCTION = CONFIG[MODE]["function"]
JAC_FUN = CONFIG[MODE]["jac_fun"]
EXPECTED_VAL_FUNCTION = CONFIG[MODE]["expected_val_function"]
MSD_AVERAGE_MODE = CONFIG[MODE]["msd_average_mode"]

NUM_FRAMES = 6
COLORS = ['k'] + plt.rcParams['axes.prop_cycle'].by_key()['color']
NUM_BINS = 50
SIGMA_POSITION = -1
SAVE = True
MULTIPLE_MSD_MODE = True
OVERLAP_MSD_MODE = True

class EMSD_Explorer(tkinter.Frame):
    """
    EMSD Explorer creates a tkinter frame allowing for interactive
    viewing of individual eMSD fits performed elsewhere in this script.
    """
    
    def __init__(self, parent: tkinter.Frame, these_data_results: dict, color = 'k', dream_fits = None):
        """
        Args:
            parent (tkinter.Tk): parent tkinter instance
            these_data_results (dict): Data results to be visualized. See calculate_msd_fits for more information
            color (str, optional): Default color of plots. Defaults to 'k'.
        """
        
        # Frame setup
        tkinter.Frame.__init__(self, parent)
        self.dream_fits = dream_fits
            
        self.frame_slider = None
        self.color = color
        self.delay_time = these_data_results['job'].get_metadata_item("input parameters")["Frame Delay (ms)"] / 1000 # s
        if __name__ == '__main__':
            self.simulation = Simulation(20000, sim_delay = self.delay_time)
        
        self.set_results(these_data_results, self.color, self.dream_fits)
        
        self.SVars = []
        self.entries = []
        self.entries_frame = tkinter.Frame(master=self)
        
        for entry_label in VAR_NAMES:
            row_frame = tkinter.Frame(master=self.entries_frame)
            
            SVar = tkinter.StringVar(self, value='')
            entry = tkinter.Entry(row_frame, textvariable=SVar)
            entry.bind('<Return>', lambda *_: self.entry_callback())
            
            self.SVars.append(SVar)
            self.entries.append(entry)
            
            tkinter.Label(master=row_frame,text=entry_label).pack(side='left')
            entry.pack(side='left')
            row_frame.pack(side='top')
        
        # Plot setup
        self.fig, self.ax = plt.subplots()
        
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self)
        NavigationToolbar2Tk(self.plot_canvas, self)
        self.plot_canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
        self.frame_slider.pack()

        self.entries_frame.pack()
        
        self.update_frame()

    def entry_callback(self):
        """
        Enables dynamic function of modifying parameters in text boxes.
        When called, grabs those parameters and plots them.
        """
        try:
            values = [float(entry.get()) for entry in self.entries]
            self.plot(values)
        except ValueError:
            logging.warning("Invalid Value! Skipping plotting...")
        
    def update_frame(self):
        """
        Gets called whenver the current frame gets modified.
        Finds the current frame number, and draws the corresponding fit.
        """
        lag_frame = self.frame_slider.get_val()
        
        fit_vals = self.fit_results.iloc[lag_frame]
        if np.nan in fit_vals:
            fit_vals = np.zeros(len(VAR_NAMES))
        for fit_val,svar in zip(fit_vals,self.SVars):
            svar.set(str(fit_val))
            
        self.plot(fit_vals)
        
    def plot(self, fun_vals: np.array):
        """
        Plots eMSD fit based on fun_vals

        Args:
            fun_vals (np.array): Array of numpy fits
        """
        self.ax.clear()
        
        lag_frame = self.frame_slider.get_val()

        # Clea up data and take log10 of it
        this_data = np.array(self.msds.loc[self.msds.index[lag_frame],])
        this_data = this_data[np.isfinite(this_data)]
        if 0 in this_data:
            this_data = this_data[~(this_data==0)]
        this_data = np.log10(this_data)
        
        # Plot original data
        _, bins = np.histogram(this_data, bins=NUM_BINS, density=True)
        self.ax.hist(this_data, bins=bins, density=True, histtype='step',color=self.color)
        
        xlabel = "Log10(MSD)"
        self.ax.set_xlim([self.min_val, self.max_val])
        self.ax.set_ylim([0,2.5])
            
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel("Probability")
        
        xs = np.array([(bins[i] + bins[i+1])/2 for i in range(len(bins)-1)])
    
        # Plot fit
        fit_fun = lambda x, *args, **kwargs:FIT_FUNCTION(x, *args, **kwargs, t=(lag_frame+1)*self.delay_time)
        ys = fit_fun(xs,*fun_vals, debug = False)
        label = ''
        if self.dream_fits != None:
            label = "Experiment"
        self.ax.plot(xs,ys,'o-', color=self.color, label = label)
        
        # Plot simulation, if applicable
        if self.dream_fits != None and self.frame_slider.get_val() + 1 in self.dream_fits['frames']:
            idx = self.dream_fits['frames'].index(self.frame_slider.get_val() + 1)
            simulated_fits = self.dream_fits['popts'][idx]
            self.simulation.set_params(simulated_fits)
            self.simulation.set_frame(self.frame_slider.get_val() + 1)
            self.simulation.run_simulation()
            simulated_ys = self.simulation.get_simulated_ys(input_bins=bins)
            self.ax.plot(xs, simulated_ys, color='darkgrey', label = "Simulation")
            logging.info(f"Simulated fits: {simulated_fits}")

        title = f"Lag Frame: {lag_frame}"
        if label != '':
            self.ax.legend()
        self.ax.set_title(title)
        self.fig.tight_layout()
        self.plot_canvas.draw()
        
    def set_results(self, other: dict, color: str, dream_fits: dict):
        """
        Sets new results to the eMSD explorer.

        Args:
            other (dict): new data results
            color (str): new color to be used
        """
        
        self.data_results = other
        self.delay_time = self.data_results['job'].get_metadata_item("input parameters")["Frame Delay (ms)"] / 1000 # s
        self.dream_fits = dream_fits
        if dream_fits:
            self.dream_fits = dream_fits
            self.simulation.sim_delay = self.delay_time
        self.color = color
        
        self.msds = self.data_results['msds']
        self.fit_results = self.data_results['fits']
        self.max_val = np.log10(self.msds.max(numeric_only=True).max())
        self.min_val = np.log10(self.msds.min(numeric_only=True).min())

        # Initialize frame slider
        if not self.frame_slider:
            self.frame_slider = SliderCombo.SliderCombo(parent=self, title="Lag Frame",
                                        lo=0,hi=len(self.fit_results.index),init_val=0,
                                        background="white", type_=int)
            self.frame_slider.setCommand(self.update_frame)

        else:
            self.frame_slider.configureSlider(lo=0, hi=len(self.fit_results.index))

            # Will update plot
            self.frame_slider.set_val(0, runCmd=True)

class EMSD_Handler:
    """read_dream_fits
    Class that creates an eMSD handler instance, allowing for multiple functions:
    (1) Creates and eMSD explorer (left hand side of window), allowing for individual
        eMSD fits to be visualized
    (2) Creates a second plot frame, allowing for other parameters to be visualized,
        such as fits over time or a plot of iMSD traces going into the fits.
    """
    
    def __init__(self,data_results:dict, dream_fits_path = None, save_path = None, run = True):
        """
        Args:
            data_results (dict): Master data results dict containing several keys pointing to individual data results.
        """
        self.dream_fits_path = dream_fits_path
        if self.dream_fits_path:
            self.dream_fits = (self.dream_fits_path)
        
        # Initialize tkinter window
        self.root = tkinter.Tk()
        
        self.emsd_frame = tkinter.Frame(master=self.root)
        self.plot_frame = tkinter.Frame(master=self.root)

        self.emsd_frame.grid(row=0,column=0,sticky='nsew')
        self.plot_frame.grid(row=0,column=1,sticky='nsew')
        
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_columnconfigure(1,weight=1)
        self.root.grid_rowconfigure(0,weight=1)
        self.root.grid_rowconfigure(1,weight=1)
        
        # Initialize secondary plot frame
        self.plot_fig, self.plot_ax = plt.subplots()
        self.plot_canvas = FigureCanvasTkAgg(self.plot_fig, master=self.plot_frame)
        NavigationToolbar2Tk(self.plot_canvas, self.plot_frame)
        self.plot_canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
        
        self.data_results = data_results
        self.data_results_titles = list(data_results.keys())
        
        self.emsd_option_svar = tkinter.StringVar(self.root,value=self.data_results_titles[0])
        self.emsd_option_svar.trace_add('write', self.load_msds)
        
        emsd_option_menu = tkinter.OptionMenu(self.emsd_frame, self.emsd_option_svar,*self.data_results_titles)
        emsd_option_menu.pack()
        
        plot_options = ["All MSDs", "SSE"] + VAR_NAMES
        # save plots
        if save_path:
            logging.info("Saving plots...")
            for plot_option in plot_options:
                self.curry_plots(plot_option)
                this_save_path = os.path.join(save_path, f"{plot_option}.png")
                self.plot_fig.savefig(this_save_path)
                logging.info(f"Saved plot: {plot_option} to path: {this_save_path}")
                
        if run:
            self.plot_option_svar = tkinter.StringVar(self.root,value=plot_options[0])
            self.plot_option_svar.trace_add('write', self.handle_plot_request)
            
            plot_option_menu = tkinter.OptionMenu(self.plot_frame, self.plot_option_svar,*plot_options)
            plot_option_menu.pack()
            
            self.emsd_explorer = None
            self.load_msds()
            
            self.root.bind("<Left>", lambda _: self.emsd_explorer.frame_slider.arrowCallback(-1))
            self.root.bind("<Right>", lambda _: self.emsd_explorer.frame_slider.arrowCallback(1))
            
            self.plot_msds()
            
            self.root.mainloop()
        
    def handle_plot_request(self, *_):
        """
        When the plot OptionMenu changes value,
        handle the request and plot accordingly.
        """
        self.curry_plots(self.plot_option_svar.get())
    
    def curry_plots(self, plot_type):
        self.plot_ax.clear()

        if plot_type == "All MSDs":
            self.plot_msds()
        elif plot_type == "SSE":
            self.plot_SSEs()
        else:
            self.plot_fits(plot_type)
            
        self.plot_fig.tight_layout()
        self.plot_canvas.draw()
    
    def plot_msds(self):
        """
        Plots combined iMSD plot along with expected values of distributions.
        """
        for i,metadata_path in enumerate(self.data_results_titles):
            msds = self.data_results[metadata_path]['msds']
            postprocessing.plot_MSDs(msds, fig=self.plot_fig, ax=self.plot_ax, color=COLORS[i])

        for i,metadata_path in enumerate(self.data_results_titles):
            expected_val_1 = self.data_results[metadata_path]['extra_infos']['Expected_Val_1']
            self.plot_ax.plot(np.power(10,expected_val_1),linestyle="None",marker='s',mec=COLORS[i], mfc='white',mew=2,ms=7)
            expected_val_2 = self.data_results[metadata_path]['extra_infos']['Expected_Val_2']
            self.plot_ax.plot(np.power(10,expected_val_2),linestyle="None",marker='o',mec=COLORS[i], mfc='white',mew=2,ms=7)
        
    def plot_SSEs(self):
        for i,metadata_path in enumerate(self.data_results_titles):
            SSEs = self.data_results[metadata_path]['extra_infos']['SSE']
            self.plot_ax.plot(SSEs, linestyle="None",marker='o',mfc=COLORS[i])
            
        self.plot_ax.set_xlabel("Lag Time [s]")
        self.plot_ax.set_ylabel(f"SSE")
        self.plot_ax.set_xscale('log')
        self.plot_ax.set_yscale('log')
            
    def plot_fits(self, var_name = None):
        if not var_name:
            var_name = self.plot_option_svar.get()
            
        index = VAR_NAMES.index(var_name)
        
        for i,metadata_path in enumerate(self.data_results_titles):
            xs = self.data_results[metadata_path]['fits'].index
            var_fits = self.data_results[metadata_path]['fits'][var_name]
            self.plot_ax.plot(xs,var_fits, 'o', color=COLORS[i])

        self.plot_ax.set_xlabel("Lag Time [s]")
        self.plot_ax.set_ylabel(f"{var_name} [{UNITS[index]}]")
        self.plot_ax.set_xscale('log')
        if var_name != 'Partition':
            self.plot_ax.set_yscale('log')
    
    def load_msds(self, *_):
        """
        Selects new data_results to be placed into the eMSD explorer
        """
        metadata_path = self.emsd_option_svar.get()
        logging.info(f"Metadata path: {metadata_path}")
        
        idx = list(self.data_results_titles).index(metadata_path)
        color = COLORS[idx]
        
        these_dream_fits = None
        if self.dream_fits_path:
            if metadata_path in self.dream_fits.keys():
                these_dream_fits = self.dream_fits[metadata_path]
            
        if not self.emsd_explorer:
            self.emsd_explorer = EMSD_Explorer(self.emsd_frame, self.data_results[metadata_path], color=color, dream_fits = these_dream_fits)
            self.emsd_explorer.pack(fill=tkinter.BOTH, expand=True)
        else:
            self.emsd_explorer.set_results(self.data_results[metadata_path],color=color, dream_fits = these_dream_fits)
        
def curve_fit(msds: np.array, lag_frame: int, sigma:float, t: float, p0: tuple):
    """
    Curve fitting function that takes the msd values at the input lag frame,
    and fits the selected fitting function to those data. t is ALWAYS a parameter,
    whereas sigma can either be a parameter or fit as a variable.

    Args:
        msds (np.array)
        lag_frame (int)
        sigma (float)
        t (float)
    Returns:
        float: fit results and additional fit information
    """
    logging.debug(f"Curve fit input parameters: lag_frame:{lag_frame}, sigma:{sigma},t:{t}")
    
    this_data = np.array(msds.loc[msds.index[lag_frame],])
    this_data = this_data[np.isfinite(this_data)]
    if 0 in this_data:
        this_data = this_data[~(this_data==0)]
        
    this_data = np.log10(this_data)
    
    hist, bins = np.histogram(this_data, bins=NUM_BINS, density=True)
    
    xs = [(bins[i] + bins[i+1])/2 for i in range(len(bins)-1)]
    jac_fun = None
    
    try:
        # Include sigma in fit
        if sigma is None:
            fit_fun = lambda x, *args, **kwargs:FIT_FUNCTION(x, *args, **kwargs, t=t)
            if JAC_FUN:
                jac_fun = lambda x, *args, **kwargs:JAC_FUN(x, *args, **kwargs, t=t)
            
            fitResult,_ = scipy.optimize.curve_fit(fit_fun, xs, hist, bounds=BOUNDS, p0=p0, jac=jac_fun)
            
            SSE = np.sum(np.power(hist-fit_fun(xs,*fitResult, debug=False),2))

        # Use sigma as parameter
        else:
            fit_fun = lambda x, *args, **kwargs:FIT_FUNCTION(x, *args, **kwargs, sigma=sigma, t=t)
            if JAC_FUN:
                jac_fun = lambda x, *args, **kwargs:JAC_FUN(x, *args, **kwargs, sigma=sigma,t=t, sigma_param = True)
            
            these_bounds = (BOUNDS[0][:-1],BOUNDS[1][:-1])
            this_p0 = p0[:-1]
            fitResult,_ = scipy.optimize.curve_fit(fit_fun, xs, hist, bounds=these_bounds, p0=this_p0, jac=jac_fun)
            
            SSE = np.sum(np.power(hist-fit_fun(xs,*fitResult, debug=False),2))

            fitResult = np.append(fitResult,sigma)
        
    except RuntimeError as e:
        logging.warning("Error in fitting! Returning np.nan values.")
        logging.warning(e)
        fitResult = np.zeros(len(VAR_NAMES))
        fitResult[:] = np.nan
        extra = np.array([np.nan,np.nan,np.nan])

    expected_val_1, expected_val_2 = EXPECTED_VAL_FUNCTION(*fitResult, t=t)
    extra = np.array([SSE,expected_val_1,expected_val_2])

    logging.debug(f"Curve fit values: fitResult: {fitResult}, extra: {extra}")

    return fitResult, extra

def save_results(data_results: dict, path: str):
    """
    Saves all data_results as individual csvs in the given path.

    Args:
        data_results (dict)
        path (str)
    """
    
    time = utils.get_time_str()
    folder_path = os.path.join(path, f"eMSDs_{time}")
    os.mkdir(folder_path)
    logging.info(f"Saving to folder: {folder_path}")    
    
    metadata_files = list(data_results.keys())
    processing_metadata = {
        "input_metadatas":metadata_files,
        "mode":MODE,
        "bypass":BYPASS,
        "mode_config":{key:str(CONFIG[MODE][key]) for key in CONFIG[MODE].keys()},
        "num_frames":NUM_FRAMES,
        "num_bins":NUM_BINS,
        "jobs":[data_results[metadata_path]["job"].get_last_metadata() for metadata_path in metadata_files]
    }
    
    with open(os.path.join(folder_path,"processing_metadata.json"), 'w') as fout:
        fout.write(json.dumps(processing_metadata, indent=4))
    
    for i,metadata_path in enumerate(metadata_files):
        msds = data_results[metadata_path]['msds']
        fits = data_results[metadata_path]['fits']
        extra_info = data_results[metadata_path]['extra_infos']
        
        df_out = copy.deepcopy(fits)
        for column in extra_info.columns:
            df_out[column] = extra_info[column]
            
        msds.to_csv(os.path.join(folder_path, f"{i}_msds.csv"))
        df_out.to_csv(os.path.join(folder_path, f"{i}_fits.csv"))
        
    return folder_path
        
def calculate_msd_fits(path, to_skip = [], save = True, dream_fits_path = None, show_handler = True):
    """
    Given a folder with processed results, grab metadata in that folder,
    and calculate all fits for those processed results, unless being skipped.

    Args:
        path (str): outer path to find metadata files in
        to_skip (list, optional):  list of times to skip, if desired.
        save (bool, optional): Whether to save results into separate folder. Defaults to True.
    """
    logging.info("Beginning calculations...")
    
    if type(path) == str:
        paths = utils.find_all_metadata(path)
        save_dir = path
    elif type(path) == list:
        paths = path
        save_dir = pathlib.Path(paths[0]).parents[2]
        
    post_processing_objects = [postprocessing.PostProcessingJob(metadata_path) for metadata_path in paths]
    post_processing_objects, paths = utils.sort_in_parallel(post_processing_objects, paths) 
    
    data_results = {}
    sigma = None
    
    this_p0 = p0
    for metadata_path, job in zip(paths, post_processing_objects):
        if "no pb" in metadata_path:
            print("Skipping no pb")
            continue
        
        message = f"On metadata: {metadata_path}"
        logging.info(f"{'-'*len(message)}\n{message}\n{'-'*len(message)}")
        delay_time = job.get_metadata_item("input parameters")["Frame Delay (ms)"] / 1000 # s

        if delay_time in to_skip:
            continue
        
        data_results[metadata_path] = {}
        data_results[metadata_path]["job"] = job
        
        if MSD_AVERAGE_MODE != 'timeavg':
            traj = job.get_df("trajectories_filtered")
            logging.info("Calculating msds no time average...")
            um_per_px = job.get_metadata_item("input parameters")["nm Per Pixel"]/1000
            msds = postprocessing.get_all_msds_noaverage(traj, delay_time, umPerPix=um_per_px, multiple = MULTIPLE_MSD_MODE, overlap=OVERLAP_MSD_MODE)
        else:
            msds = job.get_df('MSDTrajectories')
        data_results[metadata_path]["msds"] = msds

        fits = np.zeros((NUM_FRAMES,len(VAR_NAMES)))
        extra_infos = np.zeros((NUM_FRAMES,3))
        fits[:] = np.nan
        
        for lag_frame in range(0,NUM_FRAMES):
            logging.info(f"On lag frame: {lag_frame}")
            if BYPASS:
                break
            
            this_fit,extra_info = curve_fit(msds, lag_frame, sigma = sigma, t=(lag_frame+1)*delay_time, p0=this_p0)
            this_p0 = this_fit
            
            if sigma == None:
                sigma = this_fit[SIGMA_POSITION]
                logging.info(f"Setting sigma to: {sigma} nm")
                
            fits[lag_frame] = this_fit
            extra_infos[lag_frame] = extra_info
        
        var_names = VAR_NAMES
        df_results = pd.DataFrame(fits, columns=var_names)
        df_results.index = [(i+1)*delay_time for i in range(NUM_FRAMES)]
        data_results[metadata_path]["fits"] = df_results
        
        cols = ['SSE','Expected_Val_1','Expected_Val_2']
        df_extra = pd.DataFrame(extra_infos, columns=cols)
        df_extra.index = [(i+1)*delay_time for i in range(NUM_FRAMES)]
        data_results[metadata_path]["extra_infos"] = df_extra
    
    save_path = None
    if save:
        logging.info("Saving results...")
        save_path = save_results(data_results, save_dir)
    
    EMSD_Handler(data_results, dream_fits_path, save_path = save_path, run = show_handler)

def time_histogram(path):
    # WORK IN PROGRESS
    
    paths = utils.find_all_metadata(path)
    
    # data_results = {}
    
    all_msds = []
    for metadata_path in paths[1:2]:
        message = f"On metadata: {metadata_path}"
        logging.info(f"{'-'*len(message)}\n{message}\n{'-'*len(message)}")
        job = postprocessing.PostProcessingJob(metadata_path)
        delay_time = job.get_metadata_item("input parameters")["Frame Delay (ms)"] / 1000 # s

        if delay_time == 4000:
            continue
        
        # data_results[metadata_path] = {}
        # data_results[metadata_path]["job"] = job
        
        
        if MSD_AVERAGE_MODE != 'timeavg':
            traj = job.get_df("trajectories_filtered")
            logging.info("Calculating msds no time average...")
            um_per_px = job.get_metadata_item("input parameters")["nm Per Pixel"]/1000
            msds = postprocessing.get_all_msds_noaverage(traj, delay_time, umPerPix=um_per_px)
        else:
            msds = job.get_df('MSDTrajectories')
        # data_results[metadata_path]["msds"] = msds
        
        all_msds.append(msds)

        # fits = np.zeros((NUM_FRAMES,len(VAR_NAMES)))
        # extra_infos = np.zeros((NUM_FRAMES,3))
        # fits[:] = np.nan
        
        # for lag_frame in range(0,NUM_FRAMES):
        #     logging.info(f"On lag frame: {lag_frame}")
        #     if BYPASS:
        #         break
            
        #     # if lag_frame == 2 and delay_time == 40:
        #         # this_fit,extra_info = curve_fit(msds, lag_frame, t=(lag_frame+1)*delay_time, pause = True)
        #     # else:
        #     this_fit,extra_info = curve_fit(msds, lag_frame, t=(lag_frame+1)*delay_time)
                
        #     fits[lag_frame] = this_fit
        #     extra_infos[lag_frame] = extra_info
        
    min_msd = np.inf
    max_msd = -np.inf
    for msds in all_msds:
        if max_msd < msds.max(numeric_only=True).max():
            max_msd = msds.max(numeric_only=True).max()
        
        if min_msd > msds.min(numeric_only=True).min():
            min_msd = msds.min(numeric_only=True).min()
    
    msd_bins = np.logspace(np.log10(min_msd), np.log10(max_msd), 11)
    time_hists = []
    time_bins = [0]
    for time_factor in range(4):
        base_time = 0.4*np.power(10, time_factor)
        for this_time in range(9):
            time_bins.append((this_time+1)*base_time)
    
    for idx in range(len(msd_bins)-1):
        logging.info("ON NEXT HIST")
        fig, ax = plt.subplots()
        
        bin_low = msd_bins[idx]
        bin_high = msd_bins[idx+1]
        ax.set_title(f"{idx}" + "Bin: {0:.2e},{0:.2e}".format(bin_low, bin_high))
        
        time_hists = []
        widths = np.array(time_bins[1:]) - np.array(time_bins[:-1])

        for msd_idx in range(len(all_msds)):
            time_data = []
            msds = all_msds[msd_idx]
            num_all_points = sum(msds.count())

            points = msds[(msds > bin_low) & (msds < bin_high)].to_records().tolist()
            for point_row in points:
                these_points = point_row[1:]
                count = np.count_nonzero(~np.isnan(these_points))
                time_data += [point_row[0]]*count
            
            # logging.info(len(time_data))
            time_hists.append(time_data)
            # logging.info(sum(hist))
            
            hist, _ = np.histogram(time_data, bins=time_bins,density = False)
            
            ax.bar(time_bins[:-1], hist/num_all_points, width=widths, align='edge', color=COLORS[msd_idx], label=str(msd_idx))

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
        
    plt.show()
    
def analyze_msd_fits(data: dict, save_path = '', show = False):
    """
    Given several msd results, plot comparisons of various parameters and heuristics within those results

    Args:
        data (dict): dictionary of previous results
    """
    for path in data.keys():
        for file in os.listdir(path):
            if 'fits' in file:
                csv = pd.read_csv(os.path.join(path, file),index_col=0)
                data[path]['fits'].append(csv)
            if 'processing_metadata' in file:
                with open(os.path.join(path, file),'r') as fin:
                    data[path]['processing_metadata'] = json.loads(fin.read())

    for column in data[list(data.keys())[0]]['fits'][0].columns:
        logging.info(f"On column: {column}")
        fig, ax = utils.get_figure()
        
        any_negatives = False
        for path_idx,path in enumerate(data.keys()):
            for fit_idx, fits in enumerate(data[path]['fits']):
                if False in list(fits[column] >= 0):
                    any_negatives = True
                
                label = ''
                if fit_idx == 0:
                    label = data[path]['title']
                ax.plot(fits[column], 'o',color=COLORS[path_idx], label=label, markersize=10)
                
                if fit_idx == len(data[path]['fits'])-1:
                    logging.info(f"On dataset: {data[path]['title']}")
                    logging.info(f"Average of last 6 points: {np.mean(fits[column].iloc[-6:])} +/- {np.std(fits[column].iloc[-6:])}")
        
        utils.generate_legend(ax, loc='outside')
        ax.set_xlabel(f"t (s)")
        ax.set_ylabel(f"{column}")
        ax.set_xscale('log')
        if (not any_negatives and column != 'Partition') or column == 'D1':
            ax.set_yscale('log')
        
        resize_figure(fig)
        fig.tight_layout()
        
        if save_path:
            fig.savefig(os.path.join(save_path, f"{column}.png"))
            fig.savefig(os.path.join(save_path, f"{column}.svg"))
    
    if "Expected_Val_1" in data[list(data.keys())[0]]['fits'][0].columns:
        fig, ax = utils.get_figure()
        for path_idx,path in enumerate(data.keys()):
            for fit_idx, fits in enumerate(data[path]['fits']):
                label = ''
                if fit_idx == 0:
                    label = data[path]['title']
                ax.plot(fits["Expected_Val_1"], 'o',color=COLORS[path_idx], label=label, markersize=10)
                ax.plot(fits["Expected_Val_2"], 's',color=COLORS[path_idx], label=label, markersize=10)
        
        utils.generate_legend(ax, loc='outside')
        ax.set_xlabel(f"t (s)")
        ax.set_ylabel(f"Both Expected Vals (um)")
        ax.set_xscale('log')
        if not any_negatives and column != 'Partition':
            ax.set_yscale('log')
        
        resize_figure(fig)
        fig.tight_layout()
        
        if save_path:
            fig.savefig(os.path.join(save_path, f"Expected_Vals.png"))
            fig.savefig(os.path.join(save_path, f"Expected_Vals.svg"))
    
    if show:
        plt.show()    

def log_metadata():
    message = "Script metadata:"
    logging.debug(f"{'-'*len(message)}\n{message}\n{'-'*len(message)}")
    logging.debug(f"MODE: {MODE}")
    logging.debug(f"CONFIG: {CONFIG[MODE]}")
    logging.debug(f"NUM_FRAMES: {NUM_FRAMES}")
    logging.debug(f"NUM_BINS: {NUM_BINS}")
    logging.debug(f"SIGMA_POSITION: {SIGMA_POSITION}")
    logging.debug(f"SAVE: {SAVE}")
    logging.debug(f"MULTIPLE_MSD_MODE: {MULTIPLE_MSD_MODE}")
    logging.debug(f"OVERLAP_MSD_MODE: {OVERLAP_MSD_MODE}")
    logging.debug('-'*15)

def open_previous_emsd_results(path, dream_fits_path, open_handler = True, open_jobs = True):
    files = os.listdir(path)
    metadata_path = None
    fits_files = []
    msd_files = []
    for file in files:
        if "processing_metadata" in file:
            metadata_path = file
        elif 'fits' in file:
            fits_files.append(file)
        elif 'msds' in file:
            msd_files.append(file)
            
    if not metadata_path:
        logging.error("No metadata found in path")
        raise RuntimeError
    
    with open(os.path.join(path, metadata_path), 'r') as fin:
        contents = fin.read()
    processing_metadata = json.loads(contents)
    
    data_results = {}
    job_metadata_paths = processing_metadata['input_metadatas']
    vars = processing_metadata["mode_config"]["var_names"]
    if type(vars) == str:
        vars = eval(vars)
    
    current_vars = CONFIG[processing_metadata['mode']]['var_names']
    if vars != current_vars:
        logging.error(f"Mismatch between saved vars ({vars}) and current vars ({current_vars}). Maybe old implementation?")
        raise RuntimeError
        
    for i,(job_metadata_path, fit_file, msd_file) in enumerate(zip(job_metadata_paths,fits_files, msd_files)):
        data_results[job_metadata_path] = {}
        
        # read job
        if open_jobs:
            job = postprocessing.PostProcessingJob(job_metadata_path)
            data_results[job_metadata_path]['job'] = job
        else:
            data_results[job_metadata_path]['job'] = None

        # read msds
        msds = pd.read_csv(os.path.join(path, msd_file), index_col=0)
        data_results[job_metadata_path]["msds"] = msds
        
        # read fits
        all_fits = pd.read_csv(os.path.join(path, fit_file),index_col=0)
        extra_cols = []
        for col_name in all_fits.columns:
            if col_name not in vars:
                extra_cols.append(col_name)
        
        data_results[job_metadata_paths[i]]['fits'] = all_fits[vars]
        data_results[job_metadata_paths[i]]['extra_infos'] = all_fits[extra_cols]
    
    if open_handler:
        EMSD_Handler(data_results, dream_fits_path)
    
    return data_results

def main():
    path = tkinter.filedialog.askdirectory()
    calculate_msd_fits(path, save=True, show_handler=False)
    
if __name__ == '__main__':
    main()