import matplotlib.pyplot as plt

#######################
# PROCESSING PARAMETERS
#######################

# blank frames to put between concatenated emitters to prevent linking across videos
_blank_frames = 2

# number of points to use in rolling average 
_n_rolling_average = 10

# cap number of trajectories to this number when displaying trajectory plot 
_recommended_trajectory_cap = 1000

# list of csv files that get saved
_saved_csvs = ['emitters','MSDTrajectories','trajectories','trajectories_filtered', 'eMSDs', 'drifts_list']

_num_extreme_trajectories = 200

# parameters available to initial processing
_categories = {
    'Min Mass': [1000,float],
    'Diameter (px)': [11,int],
    'nm Per Pixel': [65,float],
    'Frame Delay (ms)': [2000,float],
    'Min. Traj. Len. (frames)': [5,int],
    'Jump Distance (px)': [3.0,float],
    'Drift Correction (frames)': [1, int],
    'Memory (frames)': [0, int],
    'Trajectories: only consider emitters with frame >={input}':[0, int],
    'Custom Drifts': [False, bool],
}

# if the given parameter is changed, how much do you need to recalculate
_recalculation_levels = {
    'Min Mass': 0,
    'Diameter (px)': 0,
    'nm Per Pixel': 4,
    'Frame Delay (ms)': 4,
    'Min. Traj. Len. (frames)': 2,
    'Jump Distance (px)': 1,
    'Drift Correction (frames)': 2,
    'Memory (frames)': 0,
    'Trajectories: only consider emitters with frame >={input}':1
}

_metadata_ignore = 235 # ignore all metadata with ID < value

_compare_paths = [
    r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris',
    r'E:\Current Microscope Data',
    r'E:\Old Microscope Data',
]

#####################
# PLOTTING PARAMETERS
#####################
SMALL_PPT = False

_random_seed = 42

_num_histogram_bins = 75
_frame_histogram_type = 'spread'
# _frame_histogram_type = 'stacked'

_recommended_cap_msd = 1000
_randomize_zorder = True

_num_emsd_points = 10 # number of points to display
_point_size = 10

_fig_height_show = 8.125
_fig_width_show = 11.375

_font_size = 24
_legend_kwargs = {
    "fontsize":18,
    "frameon":True,
    "facecolor":"white",
    "fancybox":False
}

_legend_title_kwargs = {
    "size":16,
    "weight":"bold"
}

_legend_linewidth = 2.5

_box_width = 2
_tick_params_major = {
    'width':2,
    'length':12,
    'direction':'in',
    'which':'major',
    'pad':12,
    
    'left':True,
    'right':True,
    'bottom':True,
    'top':False,
    
    'labelbottom':True,
    'labelleft':True,
    'labelright':False,
    'labeltop':False,
}

_tick_params_minor = {
    'width':1.5,
    'length':6,
    'direction':'in',
    'which':'minor',
    'pad':12,
    
    'left':True,
    'right':True,
    'bottom':True,
    'top':False,
    
    'labelbottom':True,
    'labelleft':True,
    'labelright':False,
    'labeltop':False,
}

if SMALL_PPT:
    _fig_height_ppt = 8
    _fig_width_ppt = 8
    _font_size = 26
    _legend_kwargs.update({'fontsize':20})
    del _tick_params_major['pad']
    del _tick_params_minor['pad']

else:
    _fig_height_ppt = 6.25
    _fig_width_ppt = 8.75

_fix_MSD_y_range = True
_msd_y_range = [5e-7, 5] # um^2

_uncertainty = (10**-3)**0.5 # µm

_lag_frame = 5

_explore_msds_radius_factor = 6 # how much to scale the radii of the circles in the msd explorer

_drift_mode = 'all_trajectories'
# _drift_mode = 'trajectories_filtered'

_color_palette = [
    '#e41a1c',
    '#377eb8',
    '#4daf4a',
    '#984ea3',
    '#ff7f00'
]
# _color_palette = plt.rcParams['axes.prop_cycle'].by_key()['color']

methods = {
    0:'none',
    1:'biggest_jump',
    2:'biggest_displacement',
    3:'longest_trajectory',
    4:'longest_memory_addition',
}
_msd_explorer_trajectory_sort_method = methods[1]

_num_traj_len_bins = 100

_use_custom_HTML_path = True
_custom_HTML_save_path = r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Personal Computers\Chris\Research\Slides\4th year review\htmls'