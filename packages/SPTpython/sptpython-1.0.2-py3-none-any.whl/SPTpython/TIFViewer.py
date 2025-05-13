import logging
logging.getLogger(__name__)

from . import config
cfg = config.load_config() # script uses config parameters

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import PIL.Image
import tkinter
import ctypes
import numpy as np
import pandas as pd
import cv2
import trackpy

from .SliderCombo import SliderCombo

ctypes.windll.shcore.SetProcessDpiAwareness(2)

class TIFViewer(tkinter.Frame):
    """
    Class for handling viewing of .tif files. Inherits from frame so can be used in other
    tkinter() objects.
    """

    _MAX_MIN_MASS = 10_000_000

    def __init__(self, parent, frames, trajectory = None, frame_bounds = None, background='white', 
                 imshow_style=None, diameter=7, emitters = None, single_circle = True, annotate = False, locs = None):  # params [FRAME, MINMASS, RADIUS]

        tkinter.Frame.__init__(self, parent)

        #############
        # Initialize Variables
        #############

        self.background = background
        self.frames = frames
        self.frame_bounds = frame_bounds
        self.circles = []
        self.saving = False
        self.configure(background=self.background)
        self.after_ids = []
        self.diameter = diameter
        self.trajectory = trajectory
        self.single_circle = single_circle
        self.emitters = emitters 
        self.annotate = annotate
        self.locs = locs
        if self.emitters is None:
            self.emitters = pd.DataFrame()

        #############
        # Initialize Frame
        #############

        self.plot_frame = tkinter.Frame(self, background=self.background)
        self.modifier_frame = tkinter.Frame(self, background=self.background)
        self.button_frame = tkinter.Frame(self, background=self.background)

        self.plot_frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.modifier_frame.grid(row=1, column=0, sticky=tkinter.NSEW)
        self.button_frame.grid(row=2, column=0, sticky=tkinter.NSEW)

        self.frame_slider = SliderCombo(self.modifier_frame, 
                                       title="Frame", 
                                       lo=self.frame_bounds[0], 
                                       hi=self.frame_bounds[1], 
                                       init_val=self.frame_bounds[0],
                                       background=self.background,
                                       type_=int)
        
        # set initial values for vmin, vmax sliders
        frame = self.frames[len(self.frames)//2]
        mean = np.mean(frame)
        stdev = np.var(frame)**0.5
        
        vmin_init = int(max(0, mean-stdev*2))
        vmax_init = int(min(65536, mean+stdev*6))
        self.imshow_style = {"vmin":vmin_init,"vmax":vmax_init}
        
        self.vmin_slider = SliderCombo(self.modifier_frame,
                                       title="vmin",
                                       lo=0,
                                       hi=self.frames[0].max(),
                                       init_val=vmin_init,
                                       background=self.background,
                                       type_=int)

        self.vmax_slider = SliderCombo(self.modifier_frame,
                                       title="vmax",
                                       lo=0,
                                       hi=self.frames[0].max(),
                                       init_val=vmax_init,
                                       background=self.background,
                                       type_=int)
        
        self.play_button = tkinter.Button(self.button_frame, text="Play", command=self.play)
        self.stop_button = tkinter.Button(self.button_frame, text="Stop", command=self.stop)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        self.tif_fig, self.tif_ax = plt.subplots()
        self.tif_fig.tight_layout()
        self.tif_canvas = FigureCanvasTkAgg(self.tif_fig, master=self.plot_frame)
        self.tif_canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
        
        self.bind("<Left>", lambda _: self.arrow_press(-1))
        self.bind("<Right>", lambda _: self.arrow_press(1))
        
        self.frame_slider.configureSlider(lo=self.frame_bounds[0], hi=self.frame_bounds[1])

        self.frame_slider.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        self.vmin_slider.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        self.vmax_slider.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        self.frame_slider.setCommand(self.update_plot)
        self.vmin_slider.setCommand(self.update_plot)
        self.vmax_slider.setCommand(self.update_plot)
        
        self.play_button.grid(row=0, column=0, sticky=tkinter.E)
        self.stop_button.grid(row=0, column=1, sticky=tkinter.W)

        self.update_plot()
        
    def set_emitters(self, other):
        self.emitters = other

    def update_imshow(self):
        vmin = self.vmin_slider.get_val()
        vmax = self.vmax_slider.get_val()

        self.imshow_style.update({'vmin':vmin, 'vmax':vmax})

    def set_mode_multiple(self):
        self.single_circle = False
    
    def set_mode_single(self):
        self.single_circle = True

    def play(self):
        """
        Begins advancing through the frames of the .tif file automatically. Recursive until stopped.
        Delayed using the self.after method of tkinter.
        """
        frame = self.frame_slider.get_val()
        if frame + 1 > self.frame_bounds[1]:
            self.stop()
        else:
            self.frame_slider.set_val(frame + 1, True)
            self.after_ids.append(self.after(200, self.play))

    def stop(self):
        for after_id in self.after_ids:
            self.after_cancel(after_id)
        self.after_ids = []

    def update_plot(self):
        """
        Plot update function that unpacks the current values for frame,minMass,and diameter. If emitters were passed
        into the object, localization is not necessary. If it is, then localizes and displays the result.
        There is also an edge case where a trajectory is being shown on the TIFViewer, and if it is the first
        time the trajectory is being shown, the TIFViewer "scrolls" to the beginning of the trajectory.
        Returns: None
        -------
        """
        self.update_imshow()
        
        self.tif_ax.clear()
        for circle in self.circles:
            circle.remove()
        self.circles = []

        frame = self.frame_slider.get_val()

        self.tif_ax.imshow(self.frames[frame], cmap='gray', **self.imshow_style)
        self.tif_ax.set_title(f"Frame: {frame}")

        self.draw_circle()
        
        if self.annotate:
            these_locs = self.locs[self.locs['frame'] == frame+1]
            for _, loc in these_locs.iterrows():
                circle = plt.Circle((loc['x']/cfg["categories"]['nm Per Pixel'][0], loc['y']/cfg["categories"]['nm Per Pixel'][0]), radius=self.diameter, color='red', fill=False)
                self.tif_ax.add_patch(circle)

        self.tif_canvas.draw_idle()

    def draw_circle(self):
        """
        Function that draws a circle on the tif_canvas according to a displayed trajectory. Also handles removing and
        redrawing that circle if necessary.
        
        Draws multiple circles if draw_multiple is true
        
        Returns: None
        -------
        """

        frame = self.frame_slider.get_val()
        
        color = 'blue'
        
        # draw all circles in frame
        if not self.emitters.empty and not self.single_circle:
            emitters_subset = self.emitters[self.emitters['frame']==frame]
            for _, emitter in emitters_subset[['x','y']].iterrows():
                loc = (emitter['x'], emitter['y'])
                
                circle = plt.Circle(loc, 
                                        radius=self.diameter/2*cfg["explore_msds_radius_factor"], color='magenta', linewidth=2, fill=False)
                
                self.circles.append(circle)

        if self.trajectory is not None:
            # case: memory was used and frame is not in trajectory. In this case draw the circle at the last known position of the particle, and change color
            if frame not in np.array(self.trajectory['frame']):
                last_frame_in_trajectory = -1
                for i,this_frame in enumerate(np.array(self.trajectory['frame'])):
                    if this_frame > frame and last_frame_in_trajectory == -1:
                        last_frame_in_trajectory = np.array(self.trajectory['frame'])[i-1]
                
                frame = last_frame_in_trajectory
                color = 'red'

            this_trajectory_frame = self.trajectory[self.trajectory['frame'] == frame]
            coords = (this_trajectory_frame['x'], this_trajectory_frame['y'])

            if self.saving and color == 'blue':
                color = 'red'
            elif self.saving:
                color = 'blue'
                
            circle = plt.Circle(coords, 
                                    radius=self.diameter/2*cfg["explore_msds_radius_factor"], color=color, linewidth=3, fill=False)
            
            self.circles.append(circle)

        for circle in self.circles:
            self.tif_ax.add_artist(circle)

    def arrow_press(self, direction):
        frame = self.frame_slider.get_val()
        if 0 < frame + direction < self.frame_bounds[1] + 1:
            self.frame_slider.set_val(frame + direction, True)

    def saveGIF(self,frame_start,frame_end,save_path):
        """
        Saves a gif of the current .tif file according to input parameters.
        This is done with animations in matplotlib.
        """
        images = []
        ani_figure = plt.figure()
        ani_figure.patch.set_alpha(0)
        plt.axis('off')
        ani_figure.tight_layout()
        frame_before = self.frame_slider.get_val()

        self.saving = True
        for frame in range(frame_start, frame_end + 1):
            self.frame_slider.set_val(frame, True)
            self.tif_fig.savefig('temp.jpg')
            img = cv2.imread("temp.jpg")
            image = PIL.Image.fromarray(img)
            # self.tif_canvas.draw()
            # image = PIL.Image.frombytes('RGB', self.tif_canvas.get_width_height(), self.tif_canvas.tostring_rgb())
            images.append([plt.imshow(image, animated=True, cmap='gray')])

        ani = animation.ArtistAnimation(ani_figure, images, interval=200, blit=True, repeat_delay=1000)
        ani.save(save_path, writer=animation.PillowWriter(fps=5))

        self.saving = False

        self.frame_slider.set_val(frame_before, True)

if __name__ == '__main__':
    import pandas as pd
    import pims

    root = tkinter.Tk()
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())
    
    path = "resources/long delay/trajectories_filtered.csv"
    vidPath = "resources/short.tif"
    filtered_trajectories = pd.read_csv(path, index_col=0)
    filtered_trajectories=filtered_trajectories.rename(columns={'frame.1':'frame'})
    particle = 2684
    
    trajectory = filtered_trajectories[filtered_trajectories['particle'] == particle]
    frames = pims.open(vidPath)
    
    frameBounds = [min(trajectory['frame']), max(trajectory['frame'])]
    frames_subset = frames[frameBounds[0]:frameBounds[1]]
    
    tif = TIFViewer(root, frames, trajectory, frameBounds)
    
    tif.pack(fill=tkinter.BOTH, expand=True)
    
    root.mainloop()