import logging
import logging.config
import datetime
import time
import copy
import tkinter
import tkinter.filedialog
import tkinter.messagebox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from SPTpython import postprocessing
from SPTpython import simulate
from SPTpython import utils
from SPTpython.C_code import kinetic_monte_carlo

import numpy as np
import pandas as pd
import scipy
import scipy.optimize
import os
import json
import sys

from resources.BUMPSDriver import BUMPS
import bumps.names as bmp


import trackpy as tp
from trackpy.motion import _msd_N
import warnings

# Previous results for March APS poster
# optimized parameters with exchange
# variables = [1.8088044177631577, 1.1699436871945772, 3.2672224394561398, 0.01035645933014354, 0.08424508240297714]
# optimized parameters without exchange
# variables = [0.5526902387609649, 0.29166666666666663, 6.806713415533625, 0.02157595693779904, 0.025741552956465238]

def msd_iter(pos, lagtimes):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        for idx,lt in enumerate(lagtimes):
            diff = pos[lt:] - pos[:-lt]
            N = _msd_N(len(pos), lagtimes)[idx]
            yield np.concatenate((np.nanmean(diff, axis=0),
                                  np.nanmean(diff**2, axis=0),
                                    np.nanstd(diff**2, axis=0, ddof=len(diff)-N)))

def get_msd_timeaveraged(trajectory,nmPerPix, delay, bifurcate = None, start_lag = 0):
    if bifurcate:
        traj1 = trajectory.iloc[:bifurcate]
        traj2 = trajectory.iloc[bifurcate:]
        
        traj1_result = get_msd_timeaveraged(traj1, nmPerPix, delay, bifurcate = None, start_lag = 0)
        traj2_result = get_msd_timeaveraged(traj2, nmPerPix, delay, bifurcate = None, start_lag = delay*bifurcate)
        traj2_result['msd'] += traj1_result['msd'].iloc[-1]
        return [traj1_result, traj2_result]
    
    pos = trajectory.set_index('frame')[['x','y']] * nmPerPix/1000
    pos = pos.reindex(np.arange(pos.index[0], 1 + pos.index[-1]))

    lagtimes = np.arange(1, len(pos))

    itr = msd_iter(pos.values, lagtimes)
    result = pd.DataFrame(itr, columns = ['<x>','<y>','<x^2>','<y^2>','std(x^2)','std(y^2)'], index=lagtimes)

    result['msd'] = result[['<x^2>','<y^2>']].sum(1)
    result['msd_std'] = np.sqrt(result['std(x^2)']**2+result['std(x^2)']**2)
    result['lagt'] = result.index.values*delay + start_lag
    result.index.name = 'lagt'
    
    result['N'] = _msd_N(len(pos), lagtimes) * len(trajectory) / len(pos)
    return result

def gamma(x,k,theta):
    return (np.power(x,k-1)*np.exp(-x/theta))/(scipy.special.gamma(k)*np.power(theta,k))

def double_gamma(x,k1, theta1, k2, theta2, p):
    return p*gamma(x, k1, theta1) + (1-p)*gamma(x, k2, theta2)

def fit_gamma(xs,bins, visualize = True):
    freq, edges = np.histogram(xs, bins=bins, density=True)
    xs = np.cumsum(np.diff(edges))
    xs -= xs[0]/2
    
    fitResult,_ = scipy.optimize.curve_fit(gamma, xs, freq)
    
    if visualize:
        plt.figure()
        plt.plot(xs, freq, label='Experiment')
        plt.plot(xs, gamma(xs, *fitResult),'o', label='Fit')
        plt.legend()
    
    return fitResult, xs, freq

def simulation_step(variables, **kwargs):
    ### unpack variables
    k_on = variables[0]
    K = variables[1]
    gauss_noise = variables[2]
    D = variables[3]
    
    n_frames = kwargs['n_frames']
    delay = kwargs['delay']
    N_particles = kwargs['N_particles']
    box_size = kwargs['box_size']
    use_noise = kwargs['use_noise']
    KMC_time_of_interest = kwargs['KMC_time_of_interest']

    ### begin calculations
    exp_time = n_frames * delay
    k_off = k_on/K
    
    # with diffusivity
    # t0 = time.time()
    # times, states = simulate.KMC(N_particles,exp_time,k_on,k_off)
    # times, states = kinetic_monte_carlo.run_kinetic_monte_carlo(N_particles, exp_time, k_on, k_off)
    # t1 = time.time()
    particle_info = kinetic_monte_carlo.run_kinetic_monte_carlo(N_particles, k_on, k_off, n_frames-1, delay)
    # particle_info = simulate.process_KMC(times, states, exp_time, time_of_interest=KMC_time_of_interest)
    # t2 = time.time()
    # video = simulate.simulate_video(particle_info, D, delay, n_frames, box_size)
    video = simulate.simulate_video_from_C(particle_info, D, delay, n_frames, box_size)
    # t3 = time.time()
    if use_noise:
        video = simulate.simulate_noise(N_particles, n_frames, gauss_noise, video)
    # t4 = time.time()
    # if (t2-t1 > 0.2) or (t3-t2 > 0.2) or (t4-t3 > 0.2):
        # print(f"t2:{t2-t1},t3:{t3-t2},t4:{t4-t3}")
    return video

def iterate_simulation(variables, **kwargs):
    # global iteration_count
    # iteration_count += 1
    # if 'n_iterations_total' in kwargs.keys():
    #     logging.info(f"Itr: {iteration_count} / {kwargs['n_iterations_total']}")
    # else:
    #     logging.info(f"Itr: {iteration_count}")

    ### unpack variables
    heuristic = kwargs['heuristic']
    experimental_data = kwargs['experimental_data']
    bins = kwargs['bins']
    lag_frame = kwargs['lag_frame']
    get_dist = kwargs['get_dist']
    N_particles = kwargs['N_particles']
    n_frames = kwargs['n_frames']
    delay = kwargs['delay']
    video = simulation_step(variables, **kwargs)
    traj = None
    # Calculate heuristic data to plug into comparison of error
    if heuristic == 'noavg':
        data_simulated = np.sum(np.power(video[lag_frame,:,:] - video[0,:,:],2),axis=1)
        # data_simulated = postprocessing.get_all_msds_noaverage(traj, delay)
    elif heuristic == 'timeavg':
        traj = simulate.construct_dataframe(video,N_particles, n_frames)
        data_simulated = tp.imsd(traj, 1, 1/delay)
    elif heuristic == 'jumps':
        traj = simulate.construct_dataframe(video,N_particles, n_frames)
        data_simulated = utils.calculate_jump_lengths(traj, log = False)
    
    if heuristic == 'noavg':
        simulated_compare = np.log10(data_simulated)
    elif heuristic == 'timeavg':
        simulated_compare = np.log10(np.array(data_simulated.loc[data_simulated.index[lag_frame],]))
    elif heuristic == 'jumps':
        simulated_compare = data_simulated
    
    # Calculate SSE
    simulated_histogram,_ = np.histogram(simulated_compare, bins=bins, density = True)
    experimental_histogram,_ = np.histogram(experimental_data, bins=bins, density = True)

    err = np.sum(np.power(simulated_histogram-experimental_histogram,2))
    # logging.info(f"Err: {err}\n")
    if not get_dist:
        if err == np.nan:
            return np.infty
        return err
    else:
        if err == np.nan:
            return np.infty, data_simulated

    return err, data_simulated, traj, simulated_histogram

def generate_tkinter(sim_kwargs, show_experiment=True):
    """
    Generates a interactive window allowing for manual iteration of testing parameter values

    Args:
        k_on (float): forward rate constant
        K (float): equilibrium K value
        gauss_noise (list): localization uncertainty noise parameters
        D (float): particle diffusivity
        params (tuple): tuple of values containing video parameter information
        experimental_data (np.array): experimental data values to match to
        bins (??): common bin object to be used in all histograms
    """
    
    def recalculate():
        sim_vars = (float(entries[0].get()),float(entries[1].get()),float(entries[2].get()),float(entries[3].get()))
        err, data_simulated, traj = iterate_simulation(sim_vars, **sim_kwargs)

        if sim_kwargs['heuristic'] in ['noavg','timeavg']:
            simulated_compare = np.log10(np.array(data_simulated.loc[data_simulated.index[sim_kwargs['lag_frame']],]))
        else:
            simulated_compare = data_simulated
        
        ax1.clear()
        bins = sim_kwargs['bin_count']
        if show_experiment:
            bins=sim_kwargs['bins']
            ax1.hist(sim_kwargs['experimental_data'],bins=bins, density = True, histtype='step', label = "Experiment")

        ax1.hist(simulated_compare, bins=bins, density = True, histtype='step', label = "Simulated w/exchange")
        ax1.legend()
        plot_canvas.draw()
    
    ###############
    # TKINTER SETUP
    ###############
    root = tkinter.Tk()
    root.bind("<Return>",lambda _: recalculate())
    
    entry_frame = tkinter.Frame(master=root)
    plot_frame = tkinter.Frame(master=root)
    entry_frame.pack(side=tkinter.TOP)
    plot_frame.pack(side=tkinter.TOP,fill=tkinter.BOTH, expand=True)
    
    entries_config = {
        "k_on":sim_kwargs['k_on'],
        "K":sim_kwargs['K'],
        "gauss_noise":sim_kwargs['gauss_noise'],
        "D":sim_kwargs['D']
    }
    entries = []
    for title in entries_config.keys():
        tkinter.Label(master=entry_frame,text=title).pack(side=tkinter.LEFT)
        entries.append(tkinter.Entry(master=entry_frame))
        entries[-1].insert(0,entries_config[title])
        entries[-1].pack(side=tkinter.LEFT)
    
    fig, ax1 = plt.subplots()
    fig.tight_layout()
    
    plot_canvas = FigureCanvasTkAgg(fig, master=root)
    plot_canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)

    recalculate()    

    root.mainloop()

def visualize_msds(msds, color = 'k', title = ''):
    plt.figure()
    plt.plot(msds, color + '-',alpha=0.02)
    plt.xscale('log')
    plt.yscale('log')
    if title:
        plt.title(title)

def visualize_vert_hist(msds, lag_frame, bins, title = ''):
    msd = np.log10(np.array(msds.loc[msds.index[lag_frame],]))
    plt.figure()
    plt.hist(msd[~np.isnan(msd)], bins=bins, density = True)
    
    if title:
        plt.title(title)

def grid_minimizer(path, sim_kwargs, minimizer_kwargs):
    sim_vars = [
        sim_kwargs['k_on'],
        sim_kwargs['K'],
        sim_kwargs['gauss_noise'],
        sim_kwargs['D']
    ]
    if minimizer_kwargs['space'] == 'linear':
        frac_lo = 1/minimizer_kwargs['frac_variability']
        frac_hi = minimizer_kwargs['frac_variability']
    elif minimizer_kwargs['space'] == 'log':
        frac_lo = 1/(10**minimizer_kwargs['decades_per_side'])
        frac_hi = 10**minimizer_kwargs['decades_per_side']
    
    n_samples = minimizer_kwargs['n_samples_range']
    sim_kwargs['get_dist'] = False
    sim_kwargs['n_iterations_total'] = len(sim_vars) * n_samples * minimizer_kwargs['n_iteration_samples']
    
    bounds = [
        (sim_vars[0]*frac_lo, sim_vars[0]*frac_hi),
        (sim_vars[1]*frac_lo, sim_vars[1]*frac_hi),
        (sim_vars[2]*frac_lo, sim_vars[2]*frac_hi),
        (sim_vars[3]*frac_lo, sim_vars[3]*frac_hi),
    ]
    
    s = '\n'.join([str(bound) for bound in bounds])
    logging.info(f"Bounds:\n{s}")
    
    result = []
    iteration_times = []
    average_errors = []
    
    # Loop 1: step through each bound
    for idx,bound in enumerate(bounds):
        if minimizer_kwargs['space'] == 'linear':
            variations = np.linspace(bound[0], bound[1], n_samples)
        elif minimizer_kwargs['space'] == 'log':
            variations = np.logspace(np.log10(bound[0]), np.log10(bound[1]), n_samples)

        idxmin = 0
        min_err = np.infty
        
        # Loop 2: step through each variation of each bound
        for variation_idx, variation in enumerate(variations):
            sim_vars[idx] = variation
            logging.info(sim_vars)
            
            # Loop 3: sample each bound several times. done with multiprocessing
            samples = []
            print("Beginning multiprocessing...")
            time_before = time.time()
            
            for _ in range(minimizer_kwargs['n_iteration_samples']):
                samples.append(iterate_simulation(sim_vars, **sim_kwargs))
            
            time_after = time.time()
            logging.info(f"Time taken: {round(time_after - time_before,1)} s")
                
            iteration_err = np.average(samples)
            average_errors.append(np.average(samples))
            
            if iteration_err < min_err:
                idxmin = variation_idx
                min_err = iteration_err
                

        sim_vars[idx] = variations[idxmin]
        logging.info(f"For bound: min: {variations[idxmin]}")
        result.append(variations[idxmin])
    
    logging.info(f"Average errors average: {np.average(average_errors)}")
    logging.info(f"Maximum error: {np.max(average_errors)}")
    logging.info(f"Minimum error: {np.min(average_errors)}")
    logging.info(f"StDev error: {np.std(average_errors)}")

    logging.info(f"Final result: {result}")
    return result

class Simulation:
    _BOX_SIZE = 58.5
    _HEURISTIC = 'noavg'
    _BIN_CONFIG = {
        'noavg':50,
        'timeavg':50,
        'jumps':100
    }
    _DEFAULT_PARAMS = {
        'k_on':2e-2,
        'K':1.5e0,
        'D':1e-6,
        'f_xlink':1,
        'dp':1
    }
    # either off, random, or seeded
    _USE_NOISE = {
        "r_KMC":"random",
        "r_init_pos":"random",
        "r_brownian":"random",
        "r_loc_uncertainty":"random"
    }
    _DEFAULT_LOC_UNCERTAINTY = 1.2e-2
    _UNCERTAINTY_THRESHOLD = 0.5
    _WRITE_DATA = True
    _SIMULATION_CODE = "C"
    _EXP_MSD_CAP = 10 # number or none

    def __init__(self, n_particles, metadata_paths = [], sim_delay = None, params = None, loc_uncertainty = None):
        self.n_particles = n_particles
        self.metadata_paths = metadata_paths
        self.exp_um_per_pix = 0.065
        
        self.jobs = []
        self.exp_delays = []
        self.exp_um_per_pixs = []
        self.exp_min_traj_lens = []
        self.exp_idx = 0 # default to 0
        for metadata_path in self.metadata_paths:
            job = postprocessing.PostProcessingJob(metadata_path)
            self.jobs.append(job)
            self.exp_delays.append(job.get_metadata_item("input parameters")["Frame Delay (ms)"]/1000)
            self.exp_um_per_pixs.append(job.get_metadata_item("input parameters")["nm Per Pixel"]/1000)
            self.exp_min_traj_lens.append(job.get_metadata_item("input parameters")["Min. Traj. Len. (frames)"])

        self.sim_delay = sim_delay if sim_delay else self.exp_delay
        self.loc_uncertainty = loc_uncertainty if loc_uncertainty else self._DEFAULT_LOC_UNCERTAINTY
        self.sim_frame = None
        self.bin_count = self._BIN_CONFIG[self._HEURISTIC]
        self.bins = None
        self.all_exp_msds = []
        self.simulated_msds = None
        self.experimental_data = None
        self.experimental_ys = None
        self.experimental_y_uncertainties = None
        self.exp_msd_cap = self._EXP_MSD_CAP
        self.n_xlink_cap = -1
        self.xs = None
        # self.gauss_noise = gauss_noise if gauss_noise else 0
        self.num_frames = -1
        self.replicate = np.array([])
        self.replicate2 = np.array([])
        
        self.mask = np.full(self.bin_count,True)
                
        self.simulated_video = None

        if not params:
            params = self._DEFAULT_PARAMS
        self.params = {
            'k_on':params['k_on'],
            'K':params['K'],
            'D':params['D'],
            'f_xlink':params['f_xlink'],
            'dp':params['dp']
        }
        
    def set_params(self, other):
        if type(other) is dict:
            self.params = other
        elif type(other) is list:
            for i, key in enumerate(self.params.keys()):
                self.params[key] = other[i]
                
    def set_exp_msd_cap(self,other):
        self.exp_msd_cap = other
    
    def set_frame(self, new_frame, num_frames = None, new_hist_frame = True, update_experimental = True):
        self.sim_frame = new_frame
        
        if num_frames:
            self.num_frames = num_frames
        elif self.num_frames <= new_frame:
            self.num_frames = new_frame + 1
        
        if self.metadata_paths and update_experimental:
            if new_frame > self.exp_min_traj_lens[self.exp_idx]:
                RuntimeWarning(f"Input frame ({new_frame}) greater than experimental min. traj. frame len ({self.exp_min_traj_lens[self.exp_idx]}). Statistics could be worse.")

            # update experimental data based on new frame
            self.set_all_experimental_data(new_hist_frame = new_hist_frame)
            
            # default to first set of data
            self.experimental_ys, self.bins = np.histogram(self.experimental_data, bins=self.bin_count, density = True)
            unc_hist, _ = np.histogram(self.experimental_data,bins=self.bins,density = False)
            self.experimental_y_uncertainties = 1/np.sqrt(unc_hist)
            self.mask = self.experimental_y_uncertainties < self._UNCERTAINTY_THRESHOLD
            logging.info(f"len(mask): {np.count_nonzero(self.mask)} / ({self.bin_count})")
            
            self.xs = np.array([(self.bins[i] + self.bins[i+1])/2 for i in range(len(self.bins)-1)])
    
    def set_all_exp_msds(self):
        self.all_exp_msds = []
        for job, exp_delay, exp_um_per_pix in zip(self.jobs, self.exp_delays, self.exp_um_per_pixs):
            traj_filtered = job.get_df('trajectories_filtered')
            msds_experiment = postprocessing.get_all_msds_noaverage(
                traj_filtered, 
                exp_delay, 
                exp_um_per_pix,
                cap=self.exp_msd_cap
            )
            self.all_exp_msds.append(msds_experiment)
    
    def set_all_experimental_data(self, all_data = None, new_hist_frame = True):
        if all_data:
            self.experimental_data = all_data
            return # correct(?)
        
        if self._HEURISTIC == 'noavg' and new_hist_frame:
            if self.all_exp_msds == []:
                self.set_all_exp_msds()

            msds_experiment = self.all_exp_msds[self.exp_idx]
            experimental_data = np.log10(np.array(msds_experiment.loc[msds_experiment.index[self.sim_frame],]))

        elif self._HEURISTIC == 'timeavg':
            raise RuntimeError("timeavg not fully implemented")
            # experimental_data = self.job.get_df("MSDTrajectories")
        elif self._HEURISTIC == 'jumps':
            raise RuntimeError('Jumps not fully implemented')
            # experimental_data = utils.calculate_jump_lengths(job.get_df('trajectories_filtered'), log = False)

        if new_hist_frame:
            experimental_data = experimental_data[~np.isnan(experimental_data)]

            self.experimental_data = experimental_data
        
    def run_simulation(self, n_particles = None, use_KMC = True, cached_particles = None):
        info_dict = copy.deepcopy(self.params)
        info_dict['n_particles'] = n_particles
        info_dict['sim_frame'] = self.sim_frame
        info_dict['sim_delay'] = self.sim_delay
        logging.info(f"Running simulation with the following parameters:\n{json.dumps(info_dict,indent=4)}")
        if not n_particles:
            n_particles = self.n_particles
            
        k_off = self.params['k_on']/self.params['K']
        
        if self.num_frames < 1:
            logging.error("Simulation set to run with less than 1 frame. Aborting...")
            raise RuntimeError

        if not use_KMC and not isinstance(cached_particles, np.ndarray):
            particle_info = np.ones((n_particles, self.num_frames-1))
            video = simulate.simulate_video_from_C(
                particle_info, 
                self.params['D'], 
                self.sim_delay, 
                self.num_frames, 
                self._BOX_SIZE,
                self._USE_NOISE
            )
            
        if use_KMC and isinstance(cached_particles, np.ndarray):
            logging.info("Using cached particles...")
            video = simulate.simulate_video_from_C(
                cached_particles, 
                self.params['D'], 
                self.sim_delay, 
                self.num_frames, 
                self._BOX_SIZE,
                self._USE_NOISE
            )
            particle_info = cached_particles

        if self._SIMULATION_CODE == 'Python' and use_KMC and not isinstance(cached_particles, np.ndarray):
            times, states = simulate.KMC(n_particles,self.sim_delay*self.num_frames,self.params['k_on'],k_off, self._WRITE_DATA)
            particle_info = simulate.process_KMC(times, states, self.sim_delay*self.num_frames)
            video = simulate.simulate_video(particle_info, self.params['D'], self.sim_delay, self.num_frames, self._BOX_SIZE)

        elif use_KMC and not isinstance(cached_particles, np.ndarray):
            # print(f"kon, {self.params['k_on']}, koff,{k_off}")
            particle_info, xlink_config = kinetic_monte_carlo.run_kinetic_monte_carlo(
                n_particles, 
                self.params['dp'],
                self.params['f_xlink'],
                
                self.params['k_on'], 
                k_off,
                self.num_frames-1, 
                self.sim_delay,
                self._WRITE_DATA,
                self._USE_NOISE["r_KMC"],
                self.n_xlink_cap
            )
            logging.info("xlink info:")
            counts, bins = np.histogram(xlink_config, bins=np.arange(np.max(xlink_config)+2))
            for i in range(len(counts)):
                logging.info(f"\tN={bins[i]}: {counts[i]}")
            # print(particle_info)
            video = simulate.simulate_video_from_C(
                particle_info, 
                self.params['D'], 
                self.sim_delay, 
                self.num_frames, 
                self._BOX_SIZE,
                self._USE_NOISE
            )
        
        video = simulate.simulate_noise(n_particles, self.num_frames, self.loc_uncertainty, video, self._USE_NOISE["r_loc_uncertainty"])
        # t4 = time.time()
        # if (t2-t1 > 0.2) or (t3-t2 > 0.2) or (t4-t3 > 0.2):
            # print(f"t2:{t2-t1},t3:{t3-t2},t4:{t4-t3}")
        self.simulated_video = video
        self.simulated_msds = np.sum(np.power(self.simulated_video[self.sim_frame,:,:] - self.simulated_video[0,:,:],2),axis=1)
        
        return particle_info
    
    def get_simulated_ys(self, input_bins = None):
        # Calculate heuristic data to plug into comparison of error
            # data_simulated = postprocessing.get_all_msds_noaverage(traj, delay)
        # elif heuristic == 'timeavg':
        #     traj = simulate.construct_dataframe(video,N_particles, n_frames)
        #     data_simulated = tp.imsd(traj, 1, 1/delay)
        # elif heuristic == 'jumps':
        #     traj = simulate.construct_dataframe(video,N_particles, n_frames)
        #     data_simulated = utils.calculate_jump_lengths(traj, log = False)
        
        if self._HEURISTIC == 'noavg':
            simulated_compare = np.log10(self.simulated_msds)
        # elif heuristic == 'timeavg':
        #     simulated_compare = np.log10(np.array(data_simulated.loc[data_simulated.index[lag_frame],]))
        # elif heuristic == 'jumps':
        #     simulated_compare = data_simulated
        
        these_bins = self.bins
        if isinstance(input_bins,np.ndarray):
            # input bins take priority
            these_bins = input_bins
        elif not isinstance(these_bins,np.ndarray):
            these_bins = self.bin_count
        
        if self.metadata_path:
            simulated_histogram,_ = np.histogram(simulated_compare, bins=these_bins, density = True)
            # experimental_histogram,_ = np.histogram(self.experimental_data, bins=self.bins, density = True)

            # err = np.sum(np.power(simulated_histogram-experimental_histogram,2))
        else:
            simulated_histogram,bins = np.histogram(simulated_compare, bins=these_bins, density = True)
            self.xs = np.array([(bins[i] + bins[i+1])/2 for i in range(len(bins)-1)])

        return simulated_histogram
        
    def plot_simulation_histogram(self, run = False):
        if run:
            self.run_simulation()
        ys = self.get_simulated_ys()
        
        if self.metadata_path:
            plt.plot(self.xs[self.mask], self.experimental_ys[self.mask], 'ko', label='experiment')
            plt.errorbar(self.xs[self.mask], self.experimental_ys[self.mask], yerr=self.experimental_y_uncertainties[self.mask], color='k')

        plt.plot(self.xs[self.mask], ys[self.mask], 'bo', label='Simulated')
        plt.legend()
    
    def show_plot(self):
        plt.show()
    
    def show_interactive(self):
        root = tkinter.Tk()
        interactive_frame = InteractiveSimulation(root, self)
        interactive_frame.pack(fill=tkinter.BOTH, expand=True)
        root.mainloop()
    
    def dream_fun(self, xs, k_on, K, D, mask, num_dream_fun_iters):
        self.params.update({
            'k_on': k_on,
            'K': K,
            'D': D
        })
        sample = np.zeros((num_dream_fun_iters,self.bin_count))[:,mask]
        
        for i in range(num_dream_fun_iters):
            self.run_simulation()
            ys = self.get_simulated_ys()
            sample[i,:] = ys[mask]
        return np.average(sample, axis=0)
        
    
    def dream_fit(self, initial_guess = None):
        num_dream_fun_iters = 5
        
        if initial_guess == None:
            initial_guess = self.params
            
        pars = [
            bmp.Parameter(name='k_on',value=initial_guess['k_on']).range(1e-6,10),
            bmp.Parameter(name='K',value=initial_guess['K']).range(1e-3,200),
            # bmp.Parameter(name='gauss_noise',value=initial_guess['gauss_noise']).range(1e-5,1),
            bmp.Parameter(name='D',value=initial_guess['D']).range(1e-7,1)
        ]
        
        fun = lambda xs, k_on, K, D: self.dream_fun(xs,  k_on, K, D, self.mask, num_dream_fun_iters)
        f = BUMPS()
        f.addfunction(fun,pars)
        f.addmodel(self.xs[self.mask], self.experimental_ys[self.mask], self.experimental_y_uncertainties[self.mask])
        f.setproblem(f.models)
        f.fitproblem()

        popt = f.getparameters()
        logging.info(f"Popt: {popt}")
        return popt
        
    def CGI_video(self):
        def advance(direction):
            nonlocal frame
            nonlocal circles
            if frame + direction < 0 or frame + direction > self.num_frames - 1:
                return
            frame += direction
            
            for circle in circles:
                circle.remove()
            circles = []
            
            ax1.set_title(f"Frame: {frame+1}")
            for coords in self.simulated_video[frame,:,:]:
                circle = plt.Circle(coords,circle_size,color='orange')
                circles.append(circle)
                ax1.add_patch(circle)
                
            fig.tight_layout()
            plot_canvas.draw()
        
        frame = 0
        circles = []
        circle_size = 1
        self.run_simulation()
        box_size = self._BOX_SIZE
        
        root = tkinter.Tk()

        root.bind('<Left>', lambda _: advance(-1))
        root.bind('<Right>', lambda _: advance(1))
        
        fig, ax1 = plt.subplots()
        
        plot_canvas = FigureCanvasTkAgg(fig, master=root)
        plot_canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
        
        ax1.set_xlim([0,box_size])
        ax1.set_ylim([0,box_size])
        ax1.set_xlabel('x (px)')
        ax1.set_ylabel('y (px)')
        ax1.set_aspect('equal')
        
        advance(0)
        
        root.mainloop()
    
    def export_simulation_to_dict(self):
        info = {}
        info["CONSTANTS"] = {}
        info["CONSTANTS"]["_BOX_SIZE"] = self._BOX_SIZE
        info["CONSTANTS"]["_HEURISTIC"] = self._HEURISTIC
        info["CONSTANTS"]["_BIN_CONFIG"] = self._BIN_CONFIG
        info["CONSTANTS"]["_DEFAULT_PARAMS"] = self._DEFAULT_PARAMS
        info["CONSTANTS"]["_USE_NOISE"] = self._USE_NOISE
        info["CONSTANTS"]["_UNCERTAINTY_THRESHOLD"] = self._UNCERTAINTY_THRESHOLD
        info["CONSTANTS"]["_WRITE_DATA"] = self._WRITE_DATA
        info["CONSTANTS"]["_SIMULATION_CODE"] = self._SIMULATION_CODE
        
        info["CURRENT_TIME"] = utils.get_time_str()
        info["EXP_METADATA"] = {}
        for metadata_path in self.metadata_paths:
            info["EXP_METADATA"]["Paths"] = metadata_path
            info["EXP_METADATA"]["Metadatas"] = [job.get_last_metadata() for job in self.jobs]
        
        info["SIM_PARAMS"] = {}
        info["SIM_PARAMS"]['n_particles'] = self.n_particles
        info["SIM_PARAMS"]['params'] = self.params
        info["SIM_PARAMS"]['sim_delay'] = self.sim_delay
        info["SIM_PARAMS"]['bin_count'] = self.bin_count
        if isinstance(self.bins, np.ndarray):
            info["SIM_PARAMS"]['bins'] = list(self.bins)
        else:
            info["SIM_PARAMS"]['bins'] = self.bins
        info["SIM_PARAMS"]['sim_frame'] = self.sim_frame

        return info
        
    def __str__(self):
        return json.dumps(self.export_simulation_to_dict(), indent=4)

class InteractiveSimulation(tkinter.Frame):
    """
    Generates a interactive window allowing for manual iteration of testing parameter values

    Args:
        k_on (float): forward rate constant
        K (float): equilibrium K value
        gauss_noise (list): localization uncertainty noise parameters
        D (float): particle diffusivity
        params (tuple): tuple of values containing video parameter information
        experimental_data (np.array): experimental data values to match to
        bins (??): common bin object to be used in all histograms
    """
    _ENTRY_ROW_COUNT = 4
    _INTVAR_COL_COUNT = 5
    
    def __init__(self, parent, simulation):
        tkinter.Frame.__init__(self, parent)
        self.root_reference = parent
        self.simulation = simulation
        
        ###############
        # TKINTER SETUP
        ###############
        self.root_reference.bind("<Return>",lambda _: self.refresh())
        
        self.plot_frame = tkinter.Frame(master=self)
        self.title_frame = tkinter.Frame(master=self)
        self.modifier_frame = tkinter.Frame(master=self)
        self.entry_frame = tkinter.Frame(master=self.modifier_frame)
        self.checkbutton_frame = tkinter.Frame(master=self.modifier_frame)
        
        self.title_frame.pack(side=tkinter.TOP, expand=False)
        self.modifier_frame.pack(side=tkinter.TOP, expand=False)
        self.plot_frame.pack(side=tkinter.TOP,fill=tkinter.BOTH, expand=True)
        self.entry_frame.pack(side=tkinter.LEFT, expand=False)
        self.checkbutton_frame.pack(side=tkinter.RIGHT, expand=False)

        if self.simulation.metadata_paths:
            tkinter.Label(master=self.title_frame, text = self.simulation.metadata_paths[0]).pack()
        
        self.save_button = tkinter.Button(master=self.entry_frame, text='Save', command=self.save)
        self.save_msd_button = tkinter.Button(master=self.entry_frame, text='Save MSD', command=self.save_msd)
        self.save_button.grid(row=0, column=0)
        self.save_msd_button.grid(row=1, column=0)

        ####################
        # INITIALIZE ENTRIES
        ####################
        self.entries_config = {
            "k_on":{'init_val':self.simulation.params['k_on'],'format':'{:.2e}', 'type':float},
            "K":{'init_val':self.simulation.params['K'],'format':'{:.2e}', 'type':float},
            "gauss_noise":{'init_val':self.simulation.loc_uncertainty,'format':'{:.2e}', 'type':float},
            "D":{'init_val':self.simulation.params['D'],'format':'{:.2e}', 'type':float},
            "f_xlink":{'init_val':self.simulation.params['f_xlink'],'format':'{:.2e}', 'type':float},
            "dp":{'init_val':self.simulation.params['dp'],'format':'{:.2e}', 'type':int},
            "sim_delay":{'init_val':self.simulation.sim_delay,'format':'{:.2e}', 'type':float},
            "vert. frame":{'init_val':self.simulation.sim_frame,'format':'{:.2e}', 'type':int},
            "num frames":{'init_val':self.simulation.sim_frame+3,'format':'{:.2e}', 'type':int},
            "exp_msd_num":{'init_val':self.simulation._EXP_MSD_CAP,'format':'{:.2e}', 'type':int},
            "n_xlink_cap":{'init_val':self.simulation.n_xlink_cap,'format':'{:.2e}', 'type':int},
        }
        if self.simulation.metadata_paths:
            self.entries_config["vert. metadata"] = {}

        if self.simulation.metadata_paths:
            self.metadata_options = [str(exp_delay) for exp_delay in self.simulation.exp_delays]
            self.metadata_option_svar = tkinter.StringVar(self)
            self.metadata_option_svar.set(self.metadata_options[self.simulation.exp_idx])
            self.metadata_option_svar.trace_add('write',lambda *_: self.refresh())
            self.metadata_menu = tkinter.OptionMenu(self.entry_frame, self.metadata_option_svar, *self.metadata_options)
            
        for i,title in enumerate(self.entries_config.keys()):
            row = i//self._ENTRY_ROW_COUNT
            col_label = 2*(i%self._ENTRY_ROW_COUNT)+1
                
            if title == 'vert. metadata':
                tkinter.Label(master=self.entry_frame, text=title).grid(row=row, column=col_label)
                self.metadata_menu.grid(row=row, column=col_label+1)
            else:
                tkinter.Label(master=self.entry_frame,text=title).grid(row=row, column=col_label)
                entry = tkinter.Entry(master=self.entry_frame, width=10)
                self.entries_config[title]['entry'] = entry
                self.entries_config[title]['entry'].insert(0,self.entries_config[title]['init_val'])
                self.entries_config[title]['entry'].grid(row=row,column=col_label+1)
        
        ####################
        # INITIALIZE INTVARS
        ####################

        self.intvar_config = {
            "normalize axes":{'int_var':None, 'init_check':True},
            "all_msds":{'int_var':None, 'init_check':True},
            "show exp":{'int_var':None, 'init_check':True},
            "show sim":{'int_var':None, 'init_check':True},
            "use KMC":{'int_var':None, 'init_check':True},
            "show_max_px":{'int_var':None, 'init_check':True},
            "cutoff_max_px":{'int_var':None, 'init_check':False},
        }
        for random_type in self.simulation._USE_NOISE.keys():
            noise_val = self.simulation._USE_NOISE[random_type]
            init_val = True if noise_val == 'random' else False
            self.intvar_config[random_type] = {
                'int_var':None, 'init_check':init_val
            }

        for i,title in enumerate(self.intvar_config.keys()):
            row = i % self._INTVAR_COL_COUNT
            col = i//self._INTVAR_COL_COUNT

            int_var = tkinter.IntVar(master=self)
            self.intvar_config[title]['int_var'] = int_var
            checkbutton = tkinter.Checkbutton(self.checkbutton_frame, text=title, variable=int_var, command=self.refresh)
            self.intvar_config[title]['checkbutton'] = checkbutton
            self.intvar_config[title]['checkbutton'].grid(row=row, column=col)
            if self.intvar_config[title]['init_check']:
                self.intvar_config[title]['checkbutton'].select()
                
        #################
        # INITIALIZE PLOT
        #################
        
        self.fig, self.ax = plt.subplots()
        self.fig.tight_layout()
        self.xlim = []
        self.ylim = []
        self.param_text = ''
        self.last_parameters = None
        self.max_px_Ds = []
        self.cached_info = []
        self.cached_msds = []
        
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.plot_canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
        NavigationToolbar2Tk(self.plot_canvas, self)

        self.refresh()

    def get_parameters(self):
        these_parameters = {}
        for title in self.entries_config.keys():
            if title == 'vert. metadata':
                these_parameters[title] = self.metadata_option_svar.get()
            else:
                type_ = self.entries_config[title]['type']
                datum = type_(self.entries_config[title]['entry'].get())
                these_parameters[title] = datum
        for title in self.intvar_config.keys():
            these_parameters[title] = self.intvar_config[title]['int_var'].get()
        return these_parameters

    def update_parameters(self):
        if self.simulation.metadata_paths:
            self.simulation.exp_idx = self.metadata_options.index(self.metadata_option_svar.get())
        try:
            these_parameters = self.get_parameters()
            
            self.simulation.set_params(
                {
                    'k_on':float(these_parameters['k_on']),
                    'K':float(these_parameters['K']),
                    'D':float(these_parameters['D']),
                    'f_xlink':float(these_parameters['f_xlink']),
                    'dp':int(these_parameters['dp'])
                }
            )
            self.simulation.sim_delay = float(these_parameters['sim_delay'])
            self.simulation.loc_uncertainty = float(these_parameters["gauss_noise"])
            self.simulation.n_xlink_cap = int(these_parameters["n_xlink_cap"])
            if int(these_parameters["exp_msd_num"]) != self.simulation.exp_msd_cap:
                self.simulation.n_particles = int(these_parameters["exp_msd_num"])
                self.simulation.set_exp_msd_cap(int(these_parameters["exp_msd_num"]))
                self.simulation.set_all_exp_msds()
                
            noise_keys = list(self.simulation._USE_NOISE.keys())
            for title in self.intvar_config.keys():
                if title in noise_keys:
                    option = self.intvar_config[title]['int_var'].get()
                    val_to_use = 'random' if option else 'off'
                    self.simulation._USE_NOISE[title] = val_to_use

        except ValueError:
            "Unexpected input!"
            
        self.param_text = ''
        padding = 0
        for title in these_parameters.keys():
            if len(title) > padding:
                padding = len(title)
                
        for title in these_parameters.keys():
            this_text = title + ': '
            self.param_text += f'{this_text:>{padding+2}}'
            self.param_text += str(these_parameters[title])
            self.param_text += '\n'
            
        vert_frame = int(these_parameters['vert. frame'])
        num_frames = int(these_parameters['num frames'])
        use_KMC = self.intvar_config["use KMC"]['int_var'].get()
        
        needs_recalculation = self.needs_recalculation(these_parameters)
        if needs_recalculation:
            logging.info("Needs recalculation: Yes")
        else:
            logging.info("Needs recalculation: No")
            
        return vert_frame, num_frames, use_KMC, needs_recalculation
                
    def needs_recalculation(self, new_parameters):
        if self.last_parameters == None:
            self.last_parameters = new_parameters
            return True

        old_parameters = self.last_parameters
        self.last_parameters = new_parameters

        differences_needing_recalculation = ['k_on', 'K', 'f_xlink','dp','num_frames','all_msds','exp_msd_num','use KMC','r_KMC']
        these_differences = []
        
        for title in new_parameters.keys():
            if new_parameters[title] != old_parameters[title]:
                these_differences.append(title)
        
        for title in these_differences:
            if title in differences_needing_recalculation:
                return True
        
        return False

    def refresh(self):
        vert_frame, num_frames, use_KMC, needs_recalculation = self.update_parameters()

        use_cached_info = False
        if not needs_recalculation and self.cached_info != []:
            use_cached_info = True
        elif needs_recalculation and self.cached_info != []:
            self.cached_info = []
            self.cached_msds = []
            
        if (self.max_px_Ds == [] or needs_recalculation) and self.intvar_config['all_msds']['int_var'].get():
            self.max_px_Ds = []
            get_max_ds = True
        else:
            get_max_ds = False

        #########################
        # Option 1: Plot all msds
        #########################
        if self.intvar_config['all_msds']['int_var'].get():
            self.ax.clear()
            for i,exp_msds in enumerate(self.simulation.all_exp_msds):
                ###################
                # EXPERIMENTAL DATA
                ###################
                norm_x_val = 1 if not self.intvar_config['normalize axes']['int_var'].get() else 1/self.simulation.params['k_on']
                norm_y_val = 1 if not self.intvar_config['normalize axes']['int_var'].get() else self.simulation.loc_uncertainty**2
                
                if self.intvar_config['show exp']['int_var'].get():
                    postprocessing.plot_MSDs(
                        exp_msds, 
                        color='k',
                        fig=self.fig, 
                        ax=self.ax,
                        alpha=min(20/self.simulation.exp_msd_cap, 1), 
                        min_traj_frame_len=self.simulation.exp_min_traj_lens[i]+3,
                        norm_x_val=norm_x_val,
                        norm_y_val=norm_y_val)
                    
                if get_max_ds:
                    self.max_px_Ds.append(np.max(np.max(exp_msds,axis=1) / exp_msds.index))
                if self.intvar_config['show_max_px']['int_var'].get():
                    self.ax.plot(exp_msds.index[:num_frames] / norm_x_val, exp_msds.index[:num_frames] * self.max_px_Ds[i] / norm_y_val, 'r--')

                ################
                # SIMULATED DATA
                ################
                if not needs_recalculation and use_cached_info:
                    logging.info("Using cached particle info...")
                    this_info = self.cached_info[i]
                    self.simulation.sim_delay = self.simulation.exp_delays[i]
                    self.simulation.set_frame(vert_frame, num_frames = num_frames, update_experimental=False)
                    self.simulation.run_simulation(n_particles = self.simulation.exp_msd_cap, use_KMC = use_KMC, cached_particles = this_info)
                    this_video = self.simulation.simulated_video
                    
                else:
                    logging.info("Generating new particle info...")
                    self.simulation.sim_delay = self.simulation.exp_delays[i]
                    self.simulation.set_frame(vert_frame, num_frames = num_frames, update_experimental=False)
                    particle_info = self.simulation.run_simulation(n_particles = self.simulation.exp_msd_cap, use_KMC = use_KMC)
                    self.cached_info.append(particle_info)
                    this_video = self.simulation.simulated_video
                    
                msd_simulated = self.get_msd_simulated(this_video)
                if needs_recalculation:
                    self.cached_msds.append(msd_simulated)
                
                if self.intvar_config['cutoff_max_px']['int_var'].get():
                    to_keep_cols, to_throw_cols = self.truncate_msds(msd_simulated, self.max_px_Ds[i])
                else:
                    to_keep_cols = msd_simulated.columns
                    to_throw_cols = []
                
                if self.intvar_config['show sim']['int_var'].get(): 
                    postprocessing.plot_MSDs(
                        msd_simulated[to_throw_cols], 
                        color='grey',
                        fig=self.fig, 
                        ax=self.ax,
                        alpha=(min(20/self.simulation.exp_msd_cap, 1))/2, 
                        min_traj_frame_len=num_frames,
                        norm_x_val=norm_x_val,
                        norm_y_val=norm_y_val)
                    postprocessing.plot_MSDs(
                        msd_simulated[to_keep_cols], 
                        color='r',
                        fig=self.fig, 
                        ax=self.ax,
                        alpha=min(20/self.simulation.exp_msd_cap, 1), 
                        min_traj_frame_len=num_frames,
                        norm_x_val=norm_x_val,
                        norm_y_val=norm_y_val)
                    
            self.ax.set_title('')
            if norm_y_val != 1:
                self.ax.set_xlabel("Lag Time / (1/k_on)")
                self.ax.set_ylabel(f"MSD (µm$^2$) / σ$^2$")
                
            self.fig.tight_layout()
 
            self.plot_canvas.draw()
        
        ###################################
        # Option 2: plot vertical histogram
        ###################################
        else:
            self.simulation.set_frame(vert_frame)
            self.simulation.run_simulation(use_KMC = use_KMC)
            msd_simulated = self.get_msd_simulated(self.simulation.simulated_video)
            
            data_trunc = None
            if self.intvar_config['cutoff_max_px']['int_var'].get():
                factor = self.simulation.exp_delays[self.simulation.exp_idx]/self.simulation.sim_delay
                to_keep_cols, to_throw_cols = self.truncate_msds(msd_simulated, self.max_px_Ds[self.simulation.exp_idx]*factor)
                if to_throw_cols.size != 0:
                    data_trunc = np.log10(msd_simulated[to_keep_cols].iloc[vert_frame])
            data_all = np.log10(msd_simulated.iloc[vert_frame])
            # data = data[data!=-np.inf]
            
            self.ax.clear()
            if self.simulation.metadata_paths:
                # default to first experimental data
                self.ax.hist(self.simulation.experimental_data,bins=self.simulation.bins, density = True, histtype='step', label = "Experiment", color='k')
                # ax1.errorbar(self.xs, self.experimental_ys, self.experimental_y_uncertainties, color='k')
            if data_trunc is not None:
                self.ax.hist(data_trunc, bins=self.simulation.bins, density = True, histtype='step', label = "Truncated Sim", color='r')
                self.ax.hist(data_all, bins=self.simulation.bin_count, density = True, histtype='step', label = "All Sim", color='grey')
            else:
                self.ax.hist(data_all, bins=self.simulation.bin_count, density = True, histtype='step', label = "Simulated w/exchange", color='r')
                
            if self.intvar_config['show_max_px']['int_var'].get():
                max_val = np.log10(self.max_px_Ds[self.simulation.exp_idx]*self.simulation.exp_delays[self.simulation.exp_idx]*vert_frame)
                print("Max val:",max_val)
                self.ax.plot([max_val,max_val],[0,self.ax.get_ylim()[1]],'r--')

            self.ax.legend()
            xlim = list(self.ax.get_xlim())
            xlim[0] -= 2
            xlim[1] += 2
            # ylim = list(self.ax.get_ylim())
            self.ax.set_xlim(xlim)
            # self.ax.set_ylim(ylim)
            self.ax.set_xlabel("Log10 (MSD)")
            self.ax.set_ylabel("Probability")
            
            self.plot_canvas.draw()

        return
    
    def get_msd_simulated(self, this_video):
        traj_subset = this_video[:,:self.simulation.exp_msd_cap,:]
        
        frame_indices = np.repeat(np.arange(traj_subset.shape[0]), traj_subset.shape[1])
        particle_indices = np.tile(np.arange(traj_subset.shape[1]), traj_subset.shape[0])

        traj_simulated = pd.DataFrame({
            'frame': frame_indices,
            'particle': particle_indices,
            'x': traj_subset[:, :, 0].flatten(),
            'y': traj_subset[:, :, 1].flatten()
        })
        return postprocessing.get_all_msds_noaverage(traj_simulated, self.simulation.sim_delay)
    
    def save(self):
        path = 'logs/simulation saves'
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, f'{utils.get_time_str()}.png')
        props = dict(boxstyle='round',facecolor='white',alpha=0)
        self.ax.text(1.03,0.98,self.param_text,transform=self.ax.transAxes, fontsize=10, fontweight='normal', verticalalignment='top', bbox=props)
        self.fig.tight_layout()     
        logging.info(f"Saving to path: {path}")
        self.fig.savefig(path)   
        
    def truncate_msds(self, msds, max_px_D):
        msds_cut = msds > (np.array(msds.index * max_px_D))[:, np.newaxis]
        to_keep_cols = np.nonzero(np.invert(np.any(msds_cut, axis=0)))[0]
        to_throw_cols = np.nonzero(np.any(msds_cut, axis=0))[0]
        return to_keep_cols, to_throw_cols

    def save_msd(self):
        if self.cached_info == []:
            tkinter.messagebox.showerror("Error", "No simulation data to save!")
            return
        path = 'logs/simulation MSDs'
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, f'{utils.get_time_str()}')
        os.mkdir(path)
        for i,msds in enumerate(self.cached_msds):
            exp_delay = self.simulation.exp_delays[i]
            exp_delay_str = f"{exp_delay}s".replace('.','_')
            msds.to_csv(os.path.join(path,f'{exp_delay_str}.csv'))
        with open(os.path.join(path,'metadata.json'),'w') as fout:
            json.dump(self.get_parameters(),fout,indent=4)
            
        logging.info(f"Saved MSDs to path: {path}")
            
def stat_check(sim_kwargs):
    sim_vars = (
        sim_kwargs['k_on'],
        sim_kwargs['K'],
        sim_kwargs['D']
    )
    
    # check jumps
    fig1, ax1 = plt.subplots()    
    
    video = simulation_step(sim_vars, **sim_kwargs)
    traj_exp = sim_kwargs['postprocessing_job'].get_df('trajectories_filtered')
    traj_sim = simulate.construct_dataframe(video, sim_kwargs['N_particles'], sim_kwargs['n_frames'])
    postprocessing.plot_jumps(traj_exp, fig=fig1, ax=ax1, color='k')
    postprocessing.plot_jumps(traj_sim, fig=fig1, ax=ax1, color='b')
    
    ax1.set_title("Jumps Comparison")

    # check MSDs
    fig2, ax2 = plt.subplots()

    msds_experiment = postprocessing.get_all_msds_noaverage(traj_exp, sim_kwargs['postprocessing_job'].get_metadata_item("input parameters")["Frame Delay (ms)"]/1000,sim_kwargs['um_per_pix'])
    msds_sim = postprocessing.get_all_msds_noaverage(traj_sim, sim_kwargs['delay'],sim_kwargs['um_per_pix'])

    postprocessing.plot_MSDs(msds_experiment, fig=fig2, ax=ax2,color='k', label='experiment')
    postprocessing.plot_MSDs(msds_sim, fig=fig2, ax=ax2,color='b', label='simulation')
    
    ax2.set_title("MSDs comparison")

    plt.show()
        
def model_ys(_, *p, **kwargs):
    # logging.info(f"p:{p}")
    mask = kwargs['mask']
    sample = np.zeros((1,kwargs['bin_count']))[:,mask]
    for i in range(1):
        _, _, _, ys = iterate_simulation(p, **kwargs)
        sample[i,:] = ys[mask]
    # logging.info(f"Highest std: {np.max(np.std(sample, axis=0))}")
    return np.average(sample, axis=0)

def run_dream():
    skip_times = ['400s','4000s']
    n_particles_dream = 10000

    os.makedirs("logs/simulation_params", exist_ok=True)
    output_path = f"logs/simulation_params/dream_fits_{utils.get_time_str()}.txt"
    
    # path_sets = [
    #     id217_22C_metadatas,
    #     id217_50C_metadatas,
    #     id218_22C_metadatas,
    #     id218_50C_metadatas,
    #     id215_22C_metadatas
    # ]
    # from emsd fitting program
    loc_uncertainties = [
        15.345,
        15.071,
        10.665,
        18.91,
        13.87
    ]

    if len(sys.argv) > 1:
        set_idx = int(sys.argv[1])
        logging.info(f"Setting path set to be: {path_sets[set_idx]}")
        path_sets = [path_sets[set_idx]]
        loc_uncertainties = [loc_uncertainties[set_idx]]

    frames_of_interest = [1,2,3,4,5,6,7,8,9,10]
    for loc_uncertainty, path_set in zip(loc_uncertainties, path_sets):
        logging.info(f"On path set: {path_set}")
        for path in path_set:
            for frame in frames_of_interest:
                simulation = Simulation(metadata_path=path, n_particles = n_particles_dream)
                logging.info(f"Setting localization uncertainty to: {loc_uncertainty/1000}")
                simulation.loc_uncertainty = loc_uncertainty/1000
                simulation.set_frame(frame)
                try:
                    popt = simulation.dream_fit()
                    logging.info(simulation)
                    with open(output_path,'a') as fout:
                        fout.write(f"Path: {path}, \nframe: {frame}, \npopt: {popt}\n\n")
                except Exception as e:
                    print("Exception")
                    print(e)

def calc_aggregated_koff(k_on, k_off, n):
    if n == 1:
        return n*(k_off/k_on)
    As = np.zeros(n+1)
    As[n] = n*(k_off/k_on)
    As[n-1] = (As[n]*((n-1)*k_off+(n-n+1)*k_on)-n*k_off)/((n-n+2)*k_on)
    for i in np.flip(np.arange(2,n-1)):
        print(n,i)
        As[i] = (As[i+1]*(i*k_off+(n-i)*k_on)-(i+1)*k_off*As[i+2])/((n-i+1)*k_on)
    As[1] = k_off*As[2]
    print(As)
    return As[1]

def main():
    # set up logging    
    time = datetime.datetime.now().strftime("%b_%d_%Y_%H_%M_%S")
    if not os.path.exists('logs/simulation/'):
        os.makedirs('logs/simulation')
    logging.config.fileConfig("logging.conf", defaults={'logfilename': f'logs/simulation/{time}.log'})
    
    logging.info("Initialized simulation script")
    
    # run_dream()
    outer_path = tkinter.filedialog.askdirectory()
    paths = utils.find_all_metadata(outer_path)
    simulation = Simulation(n_particles = 1, sim_delay = 400, metadata_paths=paths)
    # simulation = Simulation(n_particles = 5000, sim_delay = 400)
    # simulation = Simulation(n_particles = 20, sim_delay = 40, metadata_path=path3)
    # simulation.params['D'] = 1e-2
    # simulation.params['gauss_noise'] = 0.1
    simulation.set_frame(5)
    # simulation.CGI_video()
    simulation.show_interactive()

    # simulation.set_params({
    #     'k_on':0.01,
    #     'K':1,
    #     'gauss_noise':0.001,
    #     'D':3.076e-3,
    # })
    # simulation.show_interactive()

    
    # initialize_kwargs(path, sim_kwargs)
    
    # modes = {
    #     4: "minimizer",
    #     5: "stat_check",
    #     6: "dream",
    # }
    # mode = ""
    # minimizer_kwargs = {
    #     'frac_variability':0.8,
    #     'n_samples_range':8,
    #     'n_iteration_samples':15,
    #     'space':'log', # log or linear
    #     'decades_per_side':0.2
    # }
\
    
    ###########
    # EXECUTION
    ###########
    
    # if mode == 'interactive':
    #     logging.info(f"Beginning interactive tkinter window.\nSimulation parameters:\n{sim_kwargs}")
    #     generate_tkinter(sim_kwargs)
    
    # elif mode == 'interactive_no_experiment':
    #     logging.info(f"Beginning interactive tkinter window, no experimental comparison.\nSimulation parameters:\n{sim_kwargs}")
    #     generate_tkinter(sim_kwargs, show_experiment=False)
        
    # elif mode == 'video':
    #     CGI_video(sim_kwargs)
        
    # elif mode == 'stat_check':
    #     stat_check(sim_kwargs)
    
    # elif mode == 'minimizer':
    #     logging.info(f"Beginning minimizer.\nSimulation parameters:\n{sim_kwargs}\nMinimizer parameters:\n{minimizer_kwargs}")
    #     previous_result = [0,0,0,0,0]
    #     result = grid_minimizer(path, sim_kwargs, minimizer_kwargs)
        
    #     count = 0
    #     while result != previous_result:
    #         previous_result = result
    #         # global iteration_count
    #         # iteration_count = 0
            
    #         sim_kwargs.update({
    #             'k_on':result[0],
    #             'K':result[1],
    #             'gauss_noise':result[2],
    #             'D':result[3],
    #         })
            
    #         with open(f'logs/simulation_params/{time}.txt','a') as fout:
    #             fout.write(str(result) + '\n')
            
    #         result = grid_minimizer(path,sim_kwargs, minimizer_kwargs)
            
    #         count += 1
            
    #         if count > 100:
    #             logging.info("Stopping simulations...")
    #             break
            
    # elif mode == 'dream':
    #     pass
    #     # for path in paths:
    #     #     execute_dream(path, sim_kwargs)
            
if __name__ == '__main__':
    # k_on = 5
    # k_off = 0.02
    # n = 4
    # for i in range(5):
    #     print(calc_aggregated_koff(k_on, k_off, i+1))
    main()