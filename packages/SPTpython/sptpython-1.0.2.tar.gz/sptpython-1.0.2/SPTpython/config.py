import json
from pathlib import Path
from platformdirs import user_config_dir
import matplotlib.pyplot as plt

APP_NAME = "SPTpython" 
CONFIG_FILE_NAME = "config.json"

DEFAULT_CONFIG = {
    #######################
    # PROCESSING PARAMETERS
    #######################

    # blank frames to put between concatenated emitters to prevent linking across videos
    "blank_frames":2,

    # number of points to use in rolling average 
    "n_rolling_average":10,

    # cap number of trajectories to this number when displaying trajectory plot 
    "recommended_trajectory_cap":1000,

    # list of csv files that get saved
    "saved_csvs":["emitters","MSDTrajectories","trajectories","trajectories_filtered", "eMSDs", "drifts_list"],

    "num_extreme_trajectories":200,

    # parameters available to initial processing
    "categories":{
        "Min Mass": 1000.0,
        "Diameter (px)": 11,
        "nm Per Pixel": 65.0,
        "Frame Delay (ms)": 2000.0,
        "Min. Traj. Len. (frames)": 5,
        "Jump Distance (px)": 3.0,
        "Drift Correction (frames)": 1,
        "Memory (frames)": 0,
        "Trajectories: only consider emitters with frame >={input}":0,
        "Custom Drifts": False,
    },

    # if the given parameter is changed, how much do you need to recalculate
    "recalculation_levels":{
        "Min Mass": 0,
        "Diameter (px)": 0,
        "nm Per Pixel": 4,
        "Frame Delay (ms)": 4,
        "Min. Traj. Len. (frames)": 2,
        "Jump Distance (px)": 1,
        "Drift Correction (frames)": 2,
        "Memory (frames)": 0,
        "Trajectories: only consider emitters with frame >={input}":1
    },

    "metadata_ignore":235, # ignore all metadata with ID < value,

    "compare_paths":[
        r"D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris",
        r"E:\Current Microscope Data",
        r"E:\Old Microscope Data",
    ],

    #####################
    # PLOTTING PARAMETERS
    #####################
    "random_seed":42,

    "num_histogram_bins":75,
    "frame_histogram_type":"spread",
    # cfg["frame_histogram_type"] = "stacked"

    "recommended_cap_msd":1000,
    "randomize_zorder":True,

    "num_emsd_points":10, # number of points to display
    "point_size":10,

    "fig_height_show":8.125,
    "fig_width_show":11.375,

    "font_size":24,
    "legend_kwargs":{
        "fontsize":18,
        "frameon":True,
        "facecolor":"white",
        "fancybox":False,
    },

    "legend_title_kwargs":{
        "size":16,
        "weight":"bold",
    },

    "legend_linewidth":2.5,

    "box_width":2,
    "tick_params_major":{
        "width":2,
        "length":12,
        "direction":"in",
        "which":"major",
        "pad":12,
        
        "left":True,
        "right":True,
        "bottom":True,
        "top":False,
        
        "labelbottom":True,
        "labelleft":True,
        "labelright":False,
        "labeltop":False,
    },

    "tick_params_minor":{
        "width":1.5,
        "length":6,
        "direction":"in",
        "which":"minor",
        "pad":12,
        
        "left":True,
        "right":True,
        "bottom":True,
        "top":False,
        
        "labelbottom":True,
        "labelleft":True,
        "labelright":False,
        "labeltop":False,
    },

    "fig_height_ppt":6.25,
    "fig_width_ppt":8.75,

    "uncertainty":(10**-3)**0.5, # µm

    "lag_frame":5,

    "explore_msds_radius_factor":6, # how much to scale the radii of the circles in the msd explorer

    "drift_mode":"all_trajectories",
    # cfg["drift_mode"] = "trajectories_filtered"

    "color_palette":[
        "#e41a1c",
        "#377eb8",
        "#4daf4a",
        "#984ea3",
        "#ff7f00"
    ],
    # _color_palette = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    "methods":[
        "none",
        "biggest_jump",
        "biggest_displacement",
        "longest_trajectory",
        "longest_memory_addition",
    ],
    "msd_explorer_trajectory_sort_method_idx":1,

    "num_traj_len_bins":100,

    "use_custom_HTML_path":False,
    "custom_HTML_save_path":"",
}

config_dir = Path(user_config_dir(APP_NAME))
config_path = config_dir / CONFIG_FILE_NAME


def ensure_config_exists():
    """Create config directory and settings.json if not already present."""
    if not config_path.exists():
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)

def load_config():
    """Load the user config, merging with defaults."""
    ensure_config_exists()
    config = DEFAULT_CONFIG.copy()
    try:
        with open(config_path) as f:
            user_config = json.load(f)
            config.update(user_config)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[config] Warning: Failed to load config: {e}")
    return config

def save_config(updated_config):
    """Overwrite the user config file with new settings."""
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(updated_config, f, indent=2)