import logging
logging.getLogger(__name__)

from . import config
cfg = config.load_config() # script uses config parameters

import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import os
import pims
import win32api
import copy

from . import utils

class MSDExplorer:
    def __init__(self, data_dfs, metadata):
        plt.rcParams['font.size'] = 12
        self.msds = data_dfs['MSDTrajectories']
        self.trajectories = data_dfs['trajectories_filtered']
        self.drifts = data_dfs['drifts_list']
        self.metadata = metadata
        self.nm_per_px = self.metadata['input parameters']['nm Per Pixel']
        
        self.msd_idx = 0
        # sort by longest trajectories
        self.msd_ids = self.sort_trajectories()
        
        # remove drifts from trajectories
        # self.msd_ids = list(self.msds.columns)
        if self.metadata['input parameters']['Drift Correction (frames)'] != 0:
            self.trajectories = remove_drifts(self.trajectories, self.drifts, self.metadata['input parameters']['Memory (frames)'], self.metadata['number of frames'])
        
        self.root = tkinter.Tk()

        self.left_frame = tkinter.Frame()
        self.left_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self.right_frame = tkinter.Frame()
        self.right_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        
        self.label_svar = tkinter.StringVar(self.left_frame, value=f"MSD ID: {self.msd_ids[self.msd_idx]}")
        self.label = tkinter.Label(self.left_frame, textvariable=self.label_svar)
        self.label.pack()
        
        self.save_button = tkinter.Button(master=self.right_frame, text="Save", command = self.save)
        
        # self.fig, self.axs = plt.subplots(2,1)
        self.fig, self.ax = plt.subplots()
        self.ax2 = self.ax.twinx()
        
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self.left_frame)
        self.plot_canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
        
        self.root.bind("<Up>", lambda _: self.change_particle(1))
        self.root.bind("<Down>", lambda _: self.change_particle(-1))
        self.root.bind("<Left>", lambda _: self.change_frame(-1))
        self.root.bind("<Right>", lambda _: self.change_frame(1))
        
        # initialize msd plot
        # self.axs[0].plot(self.get_msd(self.msd_ids[self.msd_idx]), 'ko-')
            
        # self.axs[0].set_xlabel('Lag Time (s)')
        # self.axs[0].set_ylabel(r'MSD (µm$^2$)')
        # self.axs[0].set_xscale('log')
        # self.axs[0].set_yscale('log')
        self.trajectory = self.trajectories[self.trajectories['particle']==int(self.msd_ids[self.msd_idx])]
        times = self.trajectory.index*self.metadata['input parameters']['Frame Delay (ms)']/1000
        times = times-times[0]
        xs = self.trajectory['x']*self.nm_per_px
        self.ax.plot(times, xs-xs.iloc[0], 'r', label = 'y')
        self.ax.set_xlabel("time (s)")
        self.ax.set_ylabel("x pos (nm)")
        self.ax2.set_ylabel("x pos (px)")
        self.ax2.set_ylim(np.array(self.ax.get_ylim())/self.nm_per_px)

        ys = self.trajectory['y']*self.nm_per_px
        self.ax.plot(times, ys-ys.iloc[0], 'k', label = 'x')
        self.ax.set_xlabel("time (s)")
        self.ax.set_ylabel("Position (nm)")
        self.ax.legend()
        # rect = matplotlib.patches.Rectangle((0,-_uncertainty),times[-1],2*_uncertainty,color='r',alpha=0.2)
        # self.axs[1].add_patch(rect)
        
        # initialize video
        if not os.path.exists(metadata['files'][0]):
            for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
                if os.path.exists(drive + metadata['files'][0][3:]):
                    for idx,file in enumerate(metadata['files']):
                        file = drive + metadata['files'][0][3:]
                        metadata['files'][idx] = file
        self.frames_list = [pims.open(path) for path in metadata["files"]]
        self.tifViewer = utils.visualize_particle(self.trajectories, metadata,self.msd_ids[self.msd_idx],self.frames_list,self.right_frame)
        self.tifViewer.pack(side=tkinter.TOP,fill=tkinter.BOTH, expand=True)
        self.save_button.pack(side=tkinter.TOP)
        
        self.fig.tight_layout()
        
        self.plot_canvas.draw_idle()
        
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.root.quit())
        
        self.root.mainloop()
        
    def sort_trajectories(self):
        method = cfg["msd_explorer_trajectory_sort_method"]
        default = list(np.unique(self.trajectories['particle']))
        
        if method == 'biggest_jump':
            msd_idxs = list(self.trajectories['particle'].value_counts().index)
            jumps = [None for _ in range(len(self.trajectories['particle'].unique()))]
            
            for i,msd_idx in enumerate(msd_idxs):
                trajectory = self.trajectories[self.trajectories['particle']==msd_idx]
                max_jump = trajectory[['y','x']].diff().abs().max().max()
                jumps[i] = max_jump
                
            jumps, msd_idxs = utils.sort_in_parallel(jumps, msd_idxs, reverse=True)
            return msd_idxs
        
        if method == 'biggest_displacement':
            msd_idxs = list(self.trajectories['particle'].value_counts().index)
            displacements = [None for _ in range(len(self.trajectories['particle'].unique()))]
            
            for i,msd_idx in enumerate(msd_idxs):
                trajectory = self.trajectories[self.trajectories['particle']==msd_idx][['y','x']]
                max_displacement = (trajectory - trajectory.iloc[0]).max().max()
                displacements[i] = max_displacement
                
            displacements, msd_idxs = utils.sort_in_parallel(displacements, msd_idxs, reverse=True)
            return msd_idxs
            
        if method == 'longest_trajectory':
            return list(self.trajectories['particle'].value_counts().index)
        
        if method == 'longest_memory_addition':
            memory = self.metadata['input parameters']['Memory (frames)']
            if memory == 0:
                logging.warning("No Memory to sort by, returning default sort")
                return default
            
            particles = np.unique(self.trajectories['particle'])
            
            particles_without_memory = list(copy.deepcopy(particles))
            particles_with_memory = []
            len_added = []
            
            for particle in particles:
                this_trajectory = self.trajectories[self.trajectories['particle']==particle]
                
                diffs = this_trajectory['frame'].diff()
                total_len_added = sum(list(diffs[diffs > 1] - 1))
                if total_len_added > 0:
                    particles_with_memory.append(particle)
                    len_added.append(total_len_added)
                    particles_without_memory.remove(particle)

            len_added, particles_with_memory = utils.sort_in_parallel(len_added, particles_with_memory, reverse=True)
            
            return particles_with_memory + particles_without_memory

        return default
            
        
    def get_msd(self, idx):
        trajectory = self.trajectories[self.trajectories['particle']==int(idx)]
        msd = utils.get_msd_noaverage(trajectory, delay=self.metadata['input parameters']['Frame Delay (ms)']/1000)
        return msd

    def save(self):
        path = os.path.join(os.path.split(self.metadata['files'][0])[0],"saved_particles")
        if not os.path.exists(path):
            os.mkdir(path)
        
        particle = self.msd_ids[self.msd_idx]
        trajectory = self.trajectories[self.trajectories['particle'] == int(particle)].copy(deep=True)

        memory = self.metadata["input parameters"]["Memory (frames)"]
        num_frames = self.metadata["number of frames"][0]
        files = self.metadata["files"]
        _, offset, _ = utils.find_particle_video(trajectory, num_frames, memory, files)
        
        trajectory['frame'] -= offset
        frame_bounds = [min(trajectory['frame']), max(trajectory['frame'])]
        
        self.tifViewer.saveGIF(frame_bounds[0],frame_bounds[1],os.path.join(path, f'{particle}.gif'))
        self.fig.savefig(os.path.join(path,f'{particle}_msd.png'))

    def get_root_reference(self):
        return self.root
    
    def change_particle(self,dir):
        if self.msd_idx + dir >= len(self.msd_ids) or self.msd_idx + dir < 0:
            return
        
        self.msd_idx += dir
        self.label_svar.set(f"MSD ID: {self.msd_ids[self.msd_idx]}")
        self.ax.clear()
        
        self.trajectory = self.trajectories[self.trajectories['particle']==int(self.msd_ids[self.msd_idx])]
        times = self.trajectory.index*self.metadata['input parameters']['Frame Delay (ms)']/1000
        times = times-times[0]
        xs = self.trajectory['x']*self.metadata['input parameters']['nm Per Pixel']
        self.ax.plot(times, xs-xs.iloc[0], 'r', label = 'y')
        self.ax.set_xlabel("time (s)")
        self.ax.set_ylabel("x pos (nm)")

        ys = self.trajectory['y']*self.metadata['input parameters']['nm Per Pixel']
        self.ax.plot(times, ys-ys.iloc[0], 'k', label = 'x')
        self.ax.set_xlabel("time (s)")
        self.ax.set_ylabel("Position (nm)")
        self.ax2.set_ylabel("x pos (px)")
        self.ax2.set_ylim(np.array(self.ax.get_ylim())/self.nm_per_px)
        
        self.ax.legend()
        # rect = matplotlib.patches.Rectangle((0,-_uncertainty),times[-1],2*_uncertainty,color='r',alpha=0.2)
        # self.axs[1].add_patch(rect)
        
        new_tifViewer = utils.visualize_particle(self.trajectories, self.metadata,self.msd_ids[self.msd_idx],self.frames_list,self.right_frame)
        self.tifViewer.destroy()
        new_tifViewer.pack(fill=tkinter.BOTH, expand=True)
        self.tifViewer = new_tifViewer
        
        self.fig.tight_layout()
        
        self.plot_canvas.draw()
        
    def change_frame(self, dir):
        self.tifViewer.arrow_press(dir)

def remove_drifts(trajectories, drifts, memory, num_frames):
    columns = drifts.columns
    
    all_drifts = drifts[[columns[0], columns[1]]]
    
    frame_offset = num_frames[0] + cfg["blank_frames"] + memory
    for idx in range(len(columns)//2 - 1):
        these_drifts = drifts[[columns[2*(idx+1)],columns[2*(idx+1)+1]]]
        these_drifts = these_drifts.set_index(these_drifts.index + frame_offset)
        these_drifts.columns = ['y0','x0']
        
        all_drifts = pd.concat([all_drifts, these_drifts])
        
        frame_offset += num_frames[idx] + cfg["blank_frames"] + memory
        
    for frame in all_drifts.index:
        if frame in trajectories.index:
            trajectories.loc[frame,'y'] = trajectories.loc[frame,'y'] + all_drifts.loc[frame,'y0']
            trajectories.loc[frame,'x'] = trajectories.loc[frame,'x'] + all_drifts.loc[frame,'x0']
            
    return trajectories