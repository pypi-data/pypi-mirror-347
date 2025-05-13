import logging
logging.getLogger(__name__)

from . import config
cfg = config.load_config() # script uses config parameters

import matplotlib
import matplotlib.pyplot as plt

import tkinter
import tkinter.filedialog
import os
import pathlib
import webbrowser
import dominate
import dominate.tags
import json
import re
import pims
from typing import List
import numpy as np
import pandas as pd

from . import preprocessing
from . import SPTprocessing
from . import postprocessing
from . import utils
from . import compare
from . import TIFViewer
from .version import __version__

os.system('color')

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class CLI:
    def __init__(self):
        """
        Interfaces with the rest of SPTpython to make calls as requested.
        """
        logging.debug("Initialized CLI")
        self.post_processing_job = None
        self.figs = {}
        self.axs = {}
        self.root_path = ''
        self.regression_points = ':'
        
        self._commands = {
            'commands': {
                'func':self.show_commands,
                'description':'shows all commands',
                'level':'root'
            },
            'open': {
                'func':lambda *args: self.open_metadata(old=False *args),
                'description':'open SPTpython metadata.json format',
                'level':'root'
            },
            'new job': {
                'func':self.start_new_processing_job,
                'description':"start new SPT processing job, use -m for Mitchell's code",
                'level':'root'
            },
            'extract files': {
                'func':self.extract_files,
                'description':'Move .tif files in specified folder up one directory',
                'level':'root'
            },
            'compare': {
                'func':self.compare_outputs,
                'description':'Compares multiple outputs',
                'level':'post-processing',
                'flags':['-g'],
                'flags_description':['2 Gauss']
            },
            'exit': {
                'func':None,
                'description':'exits CLI',
                'level':'root'
            },
            'plot all': {
                'func':lambda *args: self.show_plots('all'),
                'description':'Show all available plots',
                'level':'post-processing'
            },
            'recalculate': {
                'func':self.modify_parameters,
                'description':'Recalculates results',
                'level':'post-processing'
            },
            'show metadata': {
                'func':self.show_metadata,
                'description':'Shows current metadata',
                'level':'post-processing'
            },
            'save': {
                'func':self.save_reprocessing,
                'description':'Saves reprocessing results',
                'level':'post-processing' 
            },
            'save plots': {
                'func':self.call_save_plots,
                'description':'Saves last plots',
                'level':'post-processing' 
            },
            'use points':{
                'func':self.use_points,
                'description':'Saves last plots',
                'level':'post-processing' 
            },
            'find particle':{
                'func':self.find_particle,
                'description':'Finds particle, input as: loc.x loc.y plot [plot options: msd, traj]',
                'level':'post-processing' 
            },
            'show fast':{
                'func':lambda *args: self.show_extreme('fast'),
                'description':f'Shows the fastest {cfg["num_extreme_trajectories"]} trajectories',
                'level':'post-processing' 
            },
            'show slow':{
                'func':lambda *args: self.show_extreme('slow'),
                'description':f'Shows the slowest {cfg["num_extreme_trajectories"]} trajectories',
                'level':'post-processing' 
            },
            'show all':{
                'func':lambda *args: self.show_plots('all'),
                'description':f'Shows all trajectories',
                'level':'post-processing' 
            },
            'show video':{
                'func':lambda *args: self.generate_video_with_circles(),
                'description':f'Shows video with circles around localizations',
                'level':'post-processing' 
            },
            'explore msds':{
                'func':self.explore_msds,
                'description':f'Explore individual msd traces',
                'level':'post-processing'
            },
            'bifurcate':{
                'func':self.bifurcate,
                'description':f'Bifurcate MSDs based on selected point',
                'level':'post-processing'
            },
            'see locs':{
                'func':self.see_locs,
                'description':f'See raw video with localizations',
                'level':None
            },
            'config':{
                'func':self.open_config,
                'description':f'Open user config for SPTpython settings',
                'level':None
            },
        }

    def bifurcate(self):
        if self.post_processing_job is None:
            logging.warning("Job not reopened!")
            return
        
        fig, *_ = self.post_processing_job.bifurcate()
        fig.show()

    def call_save_plots(self, *args):
        """
        Saves plots to folder of current run
        """
        if self.figs is {}:
            print("No plots to save!")
            return
        
        time = utils.get_time_str()
        save_path = os.path.join(self.root_path, f"plots_{time}")
        os.mkdir(save_path)
        
        logging.info(f"Saving plots to path: {save_path}")
        
        save_plots(self.figs, save_path)

    def close_figs(self):
        logging.debug("Closing figures")
        for key in self.figs.keys():
            plt.close(self.figs[key])
        
        self.figs = {}
        self.axs = {}
        
    def compare_outputs(self, *args):
        """
        Compares several finished runs
        """
        logging.debug("Comparing outputs")
        if self.figs is not {}:
            self.close_figs()
        
        debug = False
        if args:
            # debug mode
            comparisons = [
                r'resources\short_Jul_06_2023_11_03_25\metadata.json',
                r'resources\short_Jul_09_2023_07_26_27\metadata.json',
                r'resources\short_Jul_09_2023_07_50_36\metadata.json',
                r'resources\short_Jul_09_2023_08_36_06\metadata.json',
            ]
            self.regression_points = f"0:5"
            debug = True
            
        else:
            paths = []
            for path in cfg["compare_paths"]:
                paths += utils.find_all_metadata(path)
            
            metadatas = []
            for path in paths:
                metadata, _ = utils.read_new_format(path, get_dfs=False)
                metadatas.append(metadata)
                
            paths, metadatas = utils.sort_in_parallel(paths, metadatas, reverse = False, by_date = False)
            
            checklist = Checklist(paths, metadatas)
            comparisons, root_reference = checklist.get()
            root_reference.destroy()
        
            logging.debug(f"Found metadata paths: {paths}")
            
            if self.regression_points == ':':
                upper_point = metadatas[0]["input parameters"]["Min. Traj. Len. (frames)"]
                self.regression_points = f"0:{upper_point}"
                logging.info(f"Using regression points: {self.regression_points}")
                
        logging.info(f"Selected options: {comparisons}")
        
        
        comparison = compare.Comparison(
            paths=comparisons, 
            regression_points=self.regression_points, debug=debug)
        
        self.figs, self.axs, self.root_path = comparison.plot()

        logging.info("Comparison complete")
        
        comparison_metadata = comparison.__str__()
        display_plots_browser(self.figs, self.axs, comparison_metadata, comparison.table_data, comparison.titles)

    def explore_msds(self):
        if self.post_processing_job is None:
            logging.warning("Job not reopened!")
            return
        
        self.post_processing_job.explore_msds()

    def extract_files(self, *args):
        """
        Extracts .tif files from their respective folders, moving them up one directory
        """
        
        extension = None
        if args:
            extension = args[0]
            
        result = preprocessing.extract_files(extension)
        logging.info(f"Moved {result} files")

    def find_particle(self, *args):
        if self.post_processing_job is None:
            logging.warning("Job not reopened!")
            return
        
        if len(args) == 1:
            particle = float(args[0])
            self.post_processing_job.find_particle(particle=particle)
        else:
            loc_x = float(args[0])
            loc_y = float(args[1])
            plot = args[2]
            
            self.post_processing_job.find_particle(loc_x, loc_y, plot)

    def generate_video_with_circles(self):
        if self.post_processing_job is None:
            logging.warning("Job not reopened!")
            return
        
        path = self.post_processing_job.get_metadata_item("files")[0]
        frames = pims.open(path)
        emitters = self.post_processing_job.get_df('emitters')
        
        utils.generate_video_with_circles(frames, emitters)

    def handle_request(self, request: str) -> int:
        logging.debug(f"Handling request: '{request}'")
        """
        Finds the appropriate command and executes it.

        Args:
            request (str): input to terminal

        Returns:
            int: whether to continue terminal loop (has the user typed "exit"?)
        """
        request = request.lower()
        
        if request == 'exit':
            return 0
        
        found_command = False
        for command in self._commands.keys():
            if command in request and not found_command:
                try:
                    found_command = True
                    args = []
                    if request.replace(command,'') != '':
                        args = get_flags(request.replace(command,''))
                    logging.debug(f"Serving command {command} with args {args}")
                    self._commands[command]['func'](*args)
                except NotImplementedError:
                    print("Command is not implemented yet.")
        if not found_command:
            print("Command not recognized.")
            
        return 1

    def modify_parameters(self, *args):
        """
        Modifies processing parameters of previously opened SPT processing run
        """
        if self.post_processing_job is None:
            logging.warning("Job not reopened!")
            return
        
        self.post_processing_job.recalculate()
        logging.info("Done.")

    def open_metadata(self,old=False, *args):
        """
        Opens requested metadata and instantiates a post-processing object appropriately.
        This object handles all post-processing activities.

        Args:
            old (bool, optional): old metadata.dat format from SPTCode. Defaults to False.
        """
        logging.debug("Opening metadata")
        root = tkinter.Tk()
        root.withdraw()
        
        path = tkinter.filedialog.askopenfilename()
        
        self.post_processing_job = postprocessing.PostProcessingJob(path, old, self.regression_points)
        self.root_path = self.post_processing_job.get_root()
        
        root.destroy()

    def open_config(self):
        """
        Opens module config for editing
        """
        os.startfile(config.config_path)

    def save_reprocessing(self, *args):
        logging.debug("Saving reprocessing")
        if self.post_processing_job is None:
            logging.warning("Job not reopened!")
            return
        
        self.post_processing_job.save()
        logging.info("Post-processing saved.")

    def show_commands(self, *args):
        """
        Displays available commands, with color formatting to indicate when they are available
        """
        level_color_dict = {
            'root':style.RED,
            'post-processing':style.GREEN
        }
        
        # descriptions of levels
        print(f"{level_color_dict['root']}root: always available{style.RESET}")
        print(f"{level_color_dict['post-processing']}post-processing: available when data loaded{style.RESET}")
        
        # commands
        delim = '   '
        for command in self._commands.keys():
            message = delim
            message += command
            message += f" ({self._commands[command]['description']})"
            message += f"{level_color_dict[self._commands[command]['level']]}"
            message += f" ({self._commands[command]['level']})"
            message += f"{style.RESET}"
            if 'flags' in self._commands[command].keys():
                message += f'\n{delim}{delim}flags: '
                for idx, flag in enumerate(self._commands[command]['flags']):
                    message += f"{flag} ({self._commands[command]['flags_description'][idx]})"

            print(message)

    def show_extreme(self, extreme:str, browser = True):
        if self.post_processing_job is None:
            logging.warning("Job not reopened!")
            return
        
        self.figs, self.axs = self.post_processing_job.show_extreme(extreme)

        if browser:
            display_plots_browser(self.figs, self.axs, self.post_processing_job.__str__())

    def show_metadata(self, *args):
        logging.debug("Showing metadata")
        if self.post_processing_job is None:
            logging.warning("Job not reopened!")
            return
        
        self.post_processing_job.show_metadata() 

    def show_plots(self, which='all', browser=True):
        """
        Generates plots and shows them, if desired

        Args:
            which (str, optional): which plots to show. currently only supports all plots. Defaults to 'all'.
            browser (bool, optional): whether to open plots in browser. Defaults to True.
        """
        logging.debug("Showing plots")
        if self.figs is not {}:
            self.close_figs()
        
        if self.post_processing_job is None:
            logging.warning("Job not reopened!")
            return
        
        self.figs, self.axs = self.post_processing_job.plot('all')
        
        if browser:
            display_plots_browser(self.figs, self.axs, self.post_processing_job.__str__())
 
    def start_new_processing_job(self, *args):
        """
        Instantiates a new processing job, where several jobs can be queued.
        """
        mitchell_mode = False
        if '-m' in args:
            mitchell_mode = True
        job_count = get_input("Number of Jobs: ", int)
        logging.debug(f"Received request for {job_count} job(s)")

        jobs = SPTprocessing.queue_processing(job_count, mitchell_mode)
        
        for idx, job in enumerate(jobs):
            logging.info(f"On job: {idx+1}")
            
            try:
                SPTprocessing.process_job(job)
            except ValueError as e:
                logging.error(f"Error processing job {idx+1}: {e}")
                logging.info("Skipping job.")
        
        logging.info("Job processing complete.")
        
    def use_points(self, *args):
        """
        Use points in regression according to *args. Any new processing will use these arguments.
        
        *args should be of Python slicing syntax, e.g.
            'lower:upper'
            ':upper'
            'lower:'
            ':' (default)
        """
        points = args[0]
        logging.debug(f"Setting regression points to: {points}")
        self.regression_points = points
        if self.post_processing_job is not None:
            self.post_processing_job.set_regression_points(self.regression_points)
    
    def see_locs(self):
        csv_path = tkinter.filedialog.askopenfilename(title='Select MLE output')
        vid_path = tkinter.filedialog.askopenfilename(title='Select video')
        utils.show_locs(vid_path, csv_path)

class Checklist:
    """
    Generates a window to ask user to select which subset of items
    they want to be used.

    Args:
        items (list): list of items to choose from
        metadatas (list): list of metadata associated with each item

    Returns:
        list: list of items that were selected.
    """
    
    def __init__(self, items: list, metadatas: list, categories = []):
        logging.debug("Starting window for user checklist input")
        self.items = items
        self.items_map = []
        for item in items:
            self.items_map.append(get_postprocessed_str(item))
        
        self.metadatas = metadatas
        self.categories = categories
        
        if categories == []:
            exp_ids = []
            for item in items:
                exp_id = utils.search_regex_id(item)
                if exp_id not in exp_ids:
                    exp_ids.append(exp_id)
            
        self.root = tkinter.Tk()
        tkinter.Label(self.root, text="Select Category:").grid(row=0, column=0, sticky='e')
        self.chosen_category = tkinter.StringVar()
        self.chosen_category.set(exp_ids[0])
        self.chosen_category.trace_add('write',lambda *_: self.choose_id())
        
        ids_optionmenu = tkinter.OptionMenu(self.root,self.chosen_category,*exp_ids)
        ids_optionmenu.grid(row=0,column=1, sticky='w')
        
        selectall_button = tkinter.Button(self.root, text='Select All', command = lambda: self.toggle_all(True))
        deselectall_button = tkinter.Button(self.root, text='Deselect All', command = lambda: self.toggle_all(False))
        selectall_button.grid(row=1,column=0,sticky='e')
        deselectall_button.grid(row=1,column=1,sticky='w')
        
        self.output = []
        self.use_idxs = [i for i in range(len(items))]
        
        self.checkVars = {}
        self.checkButtons = []
        for idx,item in enumerate(items):
            var = tkinter.IntVar()
            checkButton = tkinter.Checkbutton(self.root, text=str(self.items_map[idx]),variable=var)
            self.checkVars[item] = var
            self.checkButtons.append(checkButton)
            # checkButton.grid(row=idx+2,column=0, columnspan = 2,sticky='w')
        
        tkinter.Button(self.root,
            text="Done",
            command=self.close
        ).grid(row=len(items)+2, column=0, columnspan=2)
        
        self.choose_id()
        
        self.root.mainloop()
        
    def get(self):
        return self.output, self.root
    
    def close(self):
        for item in self.checkVars.keys():
            if self.checkVars[item].get():
                self.output.append(item)
            
        self.root.quit()
        
    def choose_id(self):
        # reset checkbuttons
        logging.info("Updating checkboxes...")
        for checkButton in self.checkButtons:
            checkButton.grid_forget()
        
        self.use_idxs = []
        print(self.chosen_category.get())
        
        match_id = self.chosen_category.get()
        for idx, item in enumerate(self.items):
            if match_id == utils.search_regex_id(item):
                self.use_idxs.append(idx)
        
        row = 2
        for idx, checkButton in enumerate(self.checkButtons):
            if idx in self.use_idxs:
                checkButton.grid(row=row, column=0,columnspan=2, sticky='w')
                row += 1
    
    def toggle_all(self,state):
        checkVarNames = list(self.checkVars.keys())
        for idx in self.use_idxs:
            self.checkVars[checkVarNames[idx]].set(int(state))

def clear_files_from_folder(path: str, extension: str):
    logging.debug("Clearing files from folder")
    if not os.path.exists(path):
        return

    for file in os.listdir(path):
        if extension in file:
            logging.debug(f"Removing file: {os.path.join(path,file)}")
            os.remove(os.path.join(path,file))

def display_plots_browser(
    figs: List[plt.figure], 
    axs: List[matplotlib.axes.Axes], 
    metadata = None, 
    table_data = None, 
    titles = None, 
    html_title = '',
    launch_html = True,
):
    logging.info("Displaying plots to browser...")
    if cfg["use_custom_HTML_path"]:
        save_path = cfg["custom_HTML_save_path"]
        logging.info(f"Using custom HTML path: {save_path}")
    else:
        save_path = 'html_out'

    save_path = generate_html(figs, metadata, table_data, save_path=save_path, titles=titles, html_title=html_title)
    
    if launch_html:
        webbrowser.open(os.path.join(save_path,"html.html"))

def generate_html(figs: List[plt.figure], metadata=None, table_data = None, save_path=None, titles = None, html_title = ''):
    """
    Generates an html file containing references to input figures and metadata

    Args:
        figs (List[plt.figure]): list of input figures
        metadata (dict, optional): metadata of figures. Defaults to None.
    """
    logging.info("Generating html...")
    
    title = utils.get_time_str()
    title_w_spaces = title.replace('_', ' ')
    
    if html_title == '':
        output, root = utils.solicit_input({"HTML Title":""})
        root.destroy()
        output = output["HTML Title"]
    else:
        output = html_title
    
    title = f'{output}, {title}'
    title_w_spaces = f'{output}, generated at {title_w_spaces}'
    
    if save_path == None:
        save_path = os.path.join(os.path.split(__file__)[0],"temp_html")
        clear_files_from_folder(save_path,'.svg')
    
    save_path = os.path.join(save_path, title)

    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    
    save_plots(figs, save_path)

    doc = dominate.document(title=title_w_spaces)
    
    with doc.head:
        dominate.tags.style("""\
            td {
                border: 1px solid black;
                border-collapse: collapse;
            }

        """)

    with doc:
        dominate.tags.hgroup(title_w_spaces,style='font-size:48px')
        dominate.tags.p()
        if table_data == None:
            table_data = []
        for table_title in table_data:
            dominate.tags.hgroup(table_title, style='font-size:24px')
            with dominate.tags.table().add(dominate.tags.tbody()):
                this_table_data = table_data[table_title]
                # header row
                row = dominate.tags.tr()
                row += dominate.tags.td("Name")
                for title in titles:
                    row += dominate.tags.td(title)
                for row_title in this_table_data[0].keys():
                    row = dominate.tags.tr()
                    row += dominate.tags.td(row_title)
                    for table_el in this_table_data:
                        value = table_el[row_title]
                        if type(value) == float or type(value) == np.float64:
                            value = round(value, 2)
                        row += dominate.tags.td(value)
                
        dominate.tags.p()
        
        # Add hyperlinks at the top of the HTML file for each image
        dominate.tags.hgroup("Image Links", style='font-size:24px')
        with dominate.tags.ul():
            for image in os.listdir(save_path):
                if ".svg" in image and "_ppt" not in image:
                    dominate.tags.li(dominate.tags.a(image, href=f"#{image}"))

        dominate.tags.p()
        for image in os.listdir(save_path):
            if ".svg" in image and "_ppt" not in image:
                dominate.tags.h2(image.replace(".svg",""), style='font-size:32px')
                # Add the image with an ID for linking
                dominate.tags.img(src=image, id=image)
                # Add a hyperlink below the image to return to the top
                dominate.tags.p(dominate.tags.a("Back to Top", href="#"))

        s = metadata.split('\n')
        display = ''
        for item in s:
            display += item.replace('    ', 'tab_goes_here') + '\n'
        dominate.tags.pre(display)
    
    html_str = doc.__str__()
    html_str = html_str.replace('tab_goes_here','&emsp;')
    
    logging.debug(f"Writing html.html to: {save_path}")
    with open(os.path.join(save_path, "html.html"), 'w') as fout:
        fout.write(html_str)
        
    return save_path

def get_flags(s: str) -> List[str]:
    items = s.split(' ')
    if '' in items:
        while '' in items:
            items.remove('')
    
    return items

def get_input(message: str, type_=str):
    """
    Solicits user input for the CLI

    Args:
        message (str): message to display to the user
        type_ (_type_, optional): desired type of input. Defaults to str.

    Returns:
        type-casted user input
    """
    user_input = input(message)
    logging.debug(f"User input: {user_input}")
    
    go = True
    while go:
        try:
            user_input = type_(user_input)
            logging.debug(f"User input: {user_input}")
            return user_input
        except ValueError:
            print("Input Error")

def save_plots(figs: List[plt.figure], path: str):
    """
    Saves figures to specified path

    Args:
        figs (List[plt.figure]): list of figures
        path (str): path to save figures to
    """
    for key in figs.keys():
        fig = figs[key]
        save_path = os.path.join(path, key + '.svg')
        logging.debug(f"Plot saved to: {save_path}")
        
        resize_figure(fig)
        fig.savefig(save_path)
        fig.savefig(save_path.replace('.svg','.png'))
        
        save_path = os.path.join(path, key + '_ppt.svg')
        fig.set_size_inches(cfg["fig_width_ppt"], cfg["fig_height_ppt"])
        resize_figure(fig)
        fig.savefig(save_path)
        fig.savefig(save_path.replace('.svg','.png'))

def resize_figure(fig):
    """
    Resize the figure so that the axes (plot area) remains the same size
    if the legend is placed outside the axes.

    Parameters:
    - ax: matplotlib Axes object that already has a legend.
    - padding: extra space in inches between axes and legend (only applies to outside legends)
    """
    ax = fig.get_axes()[0]  # Get the first Axes object in the figure
    legend = ax.get_legend()
    if legend is None:
        logging.info("The provided Axes object has no legend.")
        return

    fig.canvas.draw()  # Necessary to compute layout and legend positions

    # Get bounding boxes in figure coordinates
    legend_box = legend.get_window_extent()
    axes_box = ax.get_window_extent()
    
    # Convert from pixels to figure-relative (inches)
    dpi = fig.dpi
    legend_x0, legend_y0 = legend_box.x0 / dpi, legend_box.y0 / dpi
    legend_x1, legend_y1 = legend_box.x1 / dpi, legend_box.y1 / dpi
    axes_x0, axes_y0 = axes_box.x0 / dpi, axes_box.y0 / dpi
    axes_x1, axes_y1 = axes_box.x1 / dpi, axes_box.y1 / dpi

    # Determine if legend is inside or outside axes
    is_outside = (
        legend_x1 < axes_x0 or legend_x0 > axes_x1 or
        legend_y1 < axes_y0 or legend_y0 > axes_y1
    )

    if not is_outside:
        # Legend is inside, do nothing
        return

    # Calculate overlap direction and how much to grow the figure
    fig_width, fig_height = fig.get_size_inches()
    dx, dy = 0, 0

    if legend_x0 >= axes_x1:
        dx = legend_x1 - axes_x1  # Legend on right
    elif legend_x1 <= axes_x0:
        dx = axes_x0 - legend_x0  # Legend on left

    if legend_y0 >= axes_y1:
        dy = legend_y1 - axes_y1  # Legend on top
    elif legend_y1 <= axes_y0:
        dy = axes_y0 - legend_y0  # Legend on bottom

    # Resize figure
    new_width = fig_width + dx
    new_height = fig_height + dy
    fig.set_size_inches(new_width, new_height)
    utils.tight_layout(fig)

def show_locs(vid_path, csv_path):
    logging.info(f"Showing locs of {csv_path} on {vid_path}")
    data = pd.read_csv(csv_path)
    this_data = data[['frame','x [nm]', 'y [nm]']]
    this_data.columns = ['frame','x','y']
    frames = utils.open_frames([vid_path])[0]
    root = tkinter.Tk()
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())
    tifViewer = TIFViewer.TIFViewer(root, frames, frame_bounds=[0,len(frames)], annotate = True, locs=this_data)
    tifViewer.pack(fill=tkinter.BOTH, expand=True)
    root.mainloop()

def generate_video_with_circles(frames, emitters):
    def save():
        path = tkinter.filedialog.asksaveasfile(filetypes=[('Gif','.gif')], defaultextension=[('Gif','.gif')]).name
        output, root_reference = utils.solicit_input(
            categories = {
                "Frame Start":0,
                "Frame End":len(frames),
            }
        )
        root_reference.destroy()
        video.saveGIF(output["Frame Start"], output["Frame End"], path)
    
    root = tkinter.Tk()
    video = TIFViewer.TIFViewer(root, frames, None, [0, len(frames)],emitters = emitters, single_circle=False)
    video.pack(fill=tkinter.BOTH, expand=True)
    
    root.bind("<Left>", lambda _: video.arrow_press(-1))
    root.bind("<Right>", lambda _: video.arrow_press(1))
    
    save_button = tkinter.Button(master=root, text="Save",command=save)
    save_button.pack()
    
    root.mainloop()

def get_postprocessed_str(path):
    exp_id = utils.search_regex_id(path)
    with open(path,'r') as fin:
        data = json.loads(fin.read())
    
    contents = []
    re_match = r"nf\d+.+([a-zA-Z]{3})_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)"
    # print(path)
    mo, day, yr, hour, minute, second = re.search(re_match, path).groups()
    date = f"{mo} {day}, {yr} {hour}:{minute}:{second}"
    if type(data) == list:
        data = data[-1]
    contents.append(f'{data["input parameters"]["Frame Delay (ms)"]/1000} s')
    contents.append(date)
    contents.append(f'{data["input parameters"]["Jump Distance (px)"]} jump')
    contents.append(f'{data["input parameters"]["Drift Correction (frames)"]} drift')
        
    output = exp_id
    for content in contents:
        output += f' [{content}]'
    return output

def start():
    logging.info("Started the CLI")
    
    message = ''
    message += '-------------------------------------------------------------\n'
    message += f'Welcome to the SPTpython command-line interface! (v{__version__})\n'
    message += 'This CLI enables you to pre-process, process, and post-process\n'
    message += 'single-particle tracking videos.\n'
    message += '-------------------------------------------------------------\n'
    
    logging.debug(message)
    print(message)
    
    cli = CLI()
    
    request = get_input( "Input command (commands for a list of commands): ")
    idx = 0
    
    while cli.handle_request(request):
        request = get_input("Input command: ")
        
        idx += 1