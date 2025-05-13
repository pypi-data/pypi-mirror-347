import logging
logging.getLogger(__name__)

from . import config
cfg = config.load_config() # script uses config parameters

import numpy as np
import matplotlib.pyplot as plt
import re
from typing import List

from . import postprocessing
from . import utils
from .colors import COLORS

np.random.seed(cfg["random_seed"])

alpha_function = lambda x: np.sqrt(x)

class Comparison:
    def __init__(
        self, 
        paths: List[str], 
        regression_points=':', 
        debug = False, 
        custom_titles = [], 
        custom_order = [], 
        group_by_exp = True, 
        custom_colors = [],
    ):
        """
        Generates a comparison between processing jobs, as specified by the paths

        Args:
            paths (List[str]): list of paths, each containing a .json file
            regression_points (str, optional): which regression points to use in the comparison. Defaults to ':'.

        Returns:
            tuple: contains: list of figures and axes in comparison, and the path to the first post processing job, for saving purposes.
        """
        
        logging.debug("Generating PostProcessingJob objects for comparison")

        self.group_by_exp = group_by_exp
        self.post_processing_objects = []
        for path in paths:
            post_processing_object = postprocessing.PostProcessingJob(path)
            if not post_processing_object:
                print(f"Error: {path} is not a valid post processing job")
            self.post_processing_objects.append(post_processing_object)
            
        if not custom_titles:
            self.post_processing_objects, paths = utils.sort_in_parallel(self.post_processing_objects, paths)        
        
        self.regression_points = regression_points
        self.titles = []
        self.root_path = self.post_processing_objects[0].get_root()
        self.table_data = {}
        
        for path in paths:
            self.titles.append('\\'.join(path.split('\\')[:-1]))
        
        if debug:
            self.titles = ['1','2','3','4']
            self.group_by_exp = False
        elif not custom_titles and not custom_order:
            delays = []
            for post_processing_object in self.post_processing_objects:
                delay = post_processing_object.get_metadata_item("input parameters")["Frame Delay (ms)"]
                delays.append(delay)
            
            # ask user what the datasets should be named
            self.titles, self.group_by_exp, all_titles = map_compare_titles(self.titles, delays)

            # reorder the datasets according to the order of the titles
            suggested_numbers = [1 for _ in range(len(self.titles))]
            this_idx = 1
            for this_title in all_titles:
                for title_idx, title in enumerate(self.titles):
                    if re.search(r'\[\d+.+s] (.+)', title) and re.search(r'\[\d+.+s] (.+)', title).group(1)== this_title:
                        suggested_numbers[title_idx] = this_idx
                        this_idx += 1
            
            # sort based on user input numbers
            self.titles, self.post_processing_objects = reorder_lists_custom(
                self.titles, 
                self.post_processing_objects, 
                numbers = suggested_numbers
            )
        elif custom_titles:
            # reorder according to custom titles
            self.titles, self.post_processing_objects = reorder_lists_custom(
                custom_titles, 
                self.post_processing_objects, 
                numbers = custom_order,
                bypass = True
            )
        
        # set the colors for the plots
        if custom_colors:
            self.colors = custom_colors[0]
            self.colors_condensed = custom_colors[1]
            self.scale_alpha = alpha_function(len(custom_colors[1]))
            
        else:
            colors = cfg["color_palette"]
            self.colors_condensed = []
            ids = []
            self.scale_alpha = 1
            if self.group_by_exp:
                self.colors = []
                for post_processing_object in self.post_processing_objects:
                    if post_processing_object.get_id() in ids:
                        self.colors.append(colors[ids.index(post_processing_object.get_id())])
                    else:
                        ids.append(post_processing_object.get_id())
                        self.colors.append(colors[len(ids)-1])
                        self.colors_condensed.append(colors[len(ids)-1])
                self.scale_alpha = alpha_function(len(ids))
            else:
                self.colors = colors
                self.colors_condensed = colors
            
            if len(self.colors) < len(self.post_processing_objects):
                logging.info("Using wider color palette.")
                self.colors = COLORS
            
            
    def plot(
        self, 
        bypass = False, 
        use_function_titles = [],
        all_kwargs = {},
    ):
        # TODO: make this function not ass
        
        # determine which delays are repeated
        repeat_delays = []
        for post_processing_object in self.post_processing_objects:
            delay = post_processing_object.get_metadata_item("input parameters")["Frame Delay (ms)"]
            if delay not in repeat_delays:
                repeat_delays.append(delay)
        
        # find repeated delays and group postprocessing objects by them
        if len(repeat_delays) > 0:
            post_processing_object_config = {}
            for post_processing_object in self.post_processing_objects:
                delay = post_processing_object.get_metadata_item("input parameters")["Frame Delay (ms)"]
                if delay in repeat_delays:
                    if delay not in post_processing_object_config:
                        post_processing_object_config[delay] = []
                    post_processing_object_config[delay].append(post_processing_object)
                    
        
        function_titles = [
            "Emitters, all",
            "Emitters, traj",
            "Traj lengths",
            "Jump distances",
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
            "Vertical histograms, density",
            "Vertical histograms, counts"
        ]
        if repeat_delays:
            function_titles += [
                "Vertical histograms, overlaid, counts",
                "Vertical histograms, overlaid, density",
            ]
        
        if not bypass:
            categories = {title:[True, bool] for title in function_titles}
            categories["Lag Frame"] = [cfg["lag_frame"], int]
            target_functions, root_reference = utils.solicit_input(categories)
            root_reference.destroy()

            lag_frame = target_functions["Lag Frame"]       
        else:
            lag_frame = cfg["lag_frame"]
            if function_titles:
                target_functions = {}
                for title in function_titles:
                    if title in use_function_titles:
                        target_functions[title] = True
                    else:
                        target_functions[title] = False
            else:
                target_functions = {title:True for title in function_titles}
        
        params = [self.post_processing_objects, self.titles, self.colors]
        params_condensed = [self.post_processing_objects, self.titles, self.colors_condensed]

        functions = [
            lambda **kwargs: compare_emitter_counts_all(*params, **kwargs),
            lambda **kwargs: compare_emitter_counts_traj(*params, **kwargs),
            lambda **kwargs: compare_trajectory_lengths(*params, **kwargs),
            lambda **kwargs: compare_jump_distances(*params, **kwargs),
            lambda **kwargs: compare_MSDs(
                *params, 
                superimpose = True, 
                scale_alpha=self.scale_alpha,
                group_by_exp = self.group_by_exp,
                **kwargs
            ),
            lambda **kwargs: compare_MSDs(
                *params, 
                superimpose = False,
                **kwargs
            ),
            lambda **kwargs: compare_eMSDs(
                *params,
                group_by_exp=self.group_by_exp,
                **kwargs
            ),
            lambda **kwargs: compare_powerlaws(
                *params, 
                regression_points=self.regression_points, 
                mode='log',
                **kwargs
            ),
            lambda **kwargs: compare_powerlaws(
                *params, 
                regression_points=self.regression_points, 
                mode='linear',
                **kwargs
            ),
            lambda **kwargs: compare_vertical_histograms(*params, 
                lag_frame=lag_frame, 
                density=True, 
                save_title='vertical_histogram_comparison_density',
                **kwargs
            ),
            lambda **kwargs: compare_vertical_histograms(*params, 
                lag_frame=lag_frame, 
                density=False, 
                save_title='vertical_histogram_comparison_counts',
                **kwargs
            ),
        ]
        if repeat_delays:
            functions += [
                lambda **kwargs: compare_vertical_histograms_overlaid(
                    *params_condensed, 
                    post_processing_object_config=post_processing_object_config, 
                    lag_frame=lag_frame, 
                    density=False, 
                    save_title='vertical_histogram_comparison_counts_overlaid_counts',
                    **kwargs
                ),
                lambda **kwargs: compare_vertical_histograms_overlaid(
                    *params_condensed, 
                    post_processing_object_config=post_processing_object_config, 
                    lag_frame=lag_frame, 
                    density=True, 
                    save_title='vertical_histogram_comparison_counts_overlaid_density',
                    **kwargs
                ),
            ]
        
        logging.info("Executing comparison functions...")
        figs = {}
        axs = []
        for idx,function_title in enumerate(function_titles):
            if not target_functions[function_title]:
                logging.info(f"Skipping {function_title}")
                continue

            kwargs = {}
            if function_title in all_kwargs:
                kwargs = all_kwargs[function_title]
                
            function_output = functions[idx](**kwargs)
            if len(function_output) == 3:
                fig, ax, title = function_output
                figs[title] = fig
                axs.append(ax)
            else:
                fig, ax, title, table_data = function_output
                figs[title] = fig
                axs.append(ax)
                self.table_data[title] = table_data
            
        return figs, axs, self.root_path
    
    def __str__(self):
        s = ''
        for post_processing_object, title in zip(self.post_processing_objects, self.titles):
            s += f"Metadata for {title}:\n"
            s += post_processing_object.__str__() + '\n\n'
        return s
    
def compare_emitter_counts_all(
    post_processing_objects: List[postprocessing.PostProcessingJob], 
    titles: List[str], 
    colors: List, 
    fig=None, 
    ax=None,
    tight_layout_pad=None,
    show_legend=True,
):
    
    logging.debug("Comparing emitter counts, all emitters")

    if fig == None:
        fig, ax = utils.get_figure()
    
    for color_idx,(post_processing_object, title) in enumerate(zip(post_processing_objects, titles)):
        emitters = post_processing_object.get_df("emitters")
        memory = post_processing_object.get_metadata_item("input parameters")["Memory (frames)"]
        num_frames_list = post_processing_object.get_metadata_item("number of frames")

        postprocessing.plot_emitter_counts_all(
            emitters, 
            num_frames_list, 
            memory,
            color=colors[color_idx], 
            fig=fig, 
            ax=ax, 
            label=title
        )
    
    if show_legend:
        utils.generate_legend(ax, loc='outside')
    
    utils.tight_layout(fig, pad=tight_layout_pad)
    
    return fig, ax, "emitter_comparison_all"

def compare_emitter_counts_traj(
    post_processing_objects: List[postprocessing.PostProcessingJob], 
    titles: List[str], 
    colors: List, 
    fig=None, 
    ax=None,
    tight_layout_pad=None,
    show_legend=True,
):
    
    logging.debug("Comparing emitter counts, emitters within trajectories")

    if fig == None:
        fig, ax = utils.get_figure()
    
    for color_idx,(post_processing_object, title) in enumerate(zip(post_processing_objects, titles)):
        traj = post_processing_object.get_df("trajectories_filtered")
        memory = post_processing_object.get_metadata_item("input parameters")["Memory (frames)"]
        num_frames_list = post_processing_object.get_metadata_item("number of frames")

        postprocessing.plot_emitter_counts_traj(
            traj, 
            num_frames_list, 
            memory,
            color=colors[color_idx], 
            fig=fig, 
            ax=ax, 
            label=title
        )
    
    if show_legend:
        utils.generate_legend(ax, loc='upper right')
    
    utils.tight_layout(fig, pad=tight_layout_pad)
    
    return fig, ax, "emitter_comparison_traj"
    
def compare_trajectory_lengths(
    post_processing_objects: List[postprocessing.PostProcessingJob], 
    titles: List[str], 
    colors: List, 
    fig=None, 
    ax=None,
    tight_layout_pad=None,
    show_legend=True,
):

    logging.debug("Comparing trajectory lengths")
    
    if fig == None:
        fig, ax = utils.get_figure()
    
    table_data = []
    
    for color_idx,(post_processing_object, title) in enumerate(zip(post_processing_objects, titles)):
        table_var = {}
        trajectories_filtered = post_processing_object.get_df("trajectories_filtered")
        memory = post_processing_object.get_metadata_item("input parameters")["Memory (frames)"]
        num_frames_list = post_processing_object.get_metadata_item("number of frames")
        
        postprocessing.plot_trajectory_lengths(
            trajectories_filtered, 
            num_frames_list, 
            memory,
            color=colors[color_idx], 
            fig=fig, 
            ax=ax, 
            label=title, 
            table_var = table_var
        )
        
        table_data.append(table_var)
        
    utils.generate_legend(ax, loc='upper right')
    
    utils.tight_layout(fig, pad=tight_layout_pad)
    
    return fig, ax, "emitter_comparison_traj", table_data

def compare_jump_distances(
    post_processing_objects: List[postprocessing.PostProcessingJob], 
    titles: List[str], 
    colors: List, 
    fig=None, 
    ax=None,
    tight_layout_pad=None,
    show_legend=True,
):
    
    logging.debug("Comparing jump distances")
    
    rows, cols = get_grid_dimensions(len(post_processing_objects))
    if fig == None:
        fig, axs = utils.get_figure(rows, cols, gridspec_kw={'hspace':0, 'wspace':0})
    
    for idx,(post_processing_object, title) in enumerate(zip(post_processing_objects, titles)):
        logging.debug(f"On plot: {idx+1}")

        row = idx // cols
        col = idx % cols
        
        if rows == 1:
            ax = axs[col]
        else:
            ax = axs[row, col]

        postprocessing.plot_jumps(
            post_processing_object.data_dfs['trajectories_filtered'], 
            fig=fig, 
            ax=ax, 
            color=colors[idx],
            label = title,
            axes_labels = False
        )
    
    add_sup_labels(fig, "x (px)", "Frequency")
    utils.tight_layout(fig, pad=tight_layout_pad)
    
    return fig, axs, "jump_distance_comparison"

def compare_MSDs(
    post_processing_objects: List[postprocessing.PostProcessingJob], 
    titles: List[str], 
    colors: List, 
    fig=None, 
    ax=None, 
    superimpose=False, 
    scale_alpha=1,
    group_by_exp=False,
    x_range=None,
    y_range=None,
    tight_layout_pad=None,
    show_legend=True,
):

    logging.debug("Comparing MSDs")

    if not superimpose:
        save_title = "MSD_comparison_spread"
        rows, cols = get_grid_dimensions(len(post_processing_objects))
        if fig == None:
            fig, axs = utils.get_figure(rows, cols, gridspec_kw={'hspace':0, 'wspace':0})
        
        for idx,(post_processing_object, title) in enumerate(zip(post_processing_objects, titles)):
            logging.debug(f"On plot: {idx+1}")

            row = idx // cols
            col = idx % cols
            
            if rows == 1:
                ax = axs[col]
            else:
                ax = axs[row, col]

            postprocessing.plot_MSDs(
                post_processing_object.data_dfs['MSDTrajectories'], 
                post_processing_object.data_dfs['eMSDs'],
                color=colors[idx], 
                fig=fig, 
                ax=ax, 
                label=title, 
                scale_alpha=scale_alpha,
                axes_labels = False,
                x_range=x_range,
                y_range=y_range,
            )

            utils.generate_legend(ax, remove_duplicates = True, loc='lower right')
            
        add_sup_labels(fig, "Lag Time (s)", r'MSD (µm$^2$)')
        utils.tight_layout(fig, pad=tight_layout_pad)
    
        return fig, axs, save_title

    else:
        if fig == None:
            fig, ax = utils.get_figure()
        save_title = "MSD_comparison_superimposed"
        
        zorders = None
        if cfg["randomize_zorder"]:
            lengths = []
            total_count = 0
            for post_processing_object in post_processing_objects:
                length = min(
                    cfg["recommended_cap_msd"],
                    len(post_processing_object.data_dfs['MSDTrajectories'].columns)
                )
                total_count += length
                lengths.append(length)
                
            temp = np.random.permutation(total_count)
            zorders = []
            running_length = 0
            for idx, length in enumerate(lengths):
                zorders += list(temp[running_length:running_length+length])
                running_length += length
                
                
        for idx,(post_processing_object, title) in enumerate(zip(post_processing_objects, titles)):
            logging.debug(f"On plot: {idx+1}")

            postprocessing.plot_MSDs(
                post_processing_object.data_dfs['MSDTrajectories'],
                post_processing_object.data_dfs['eMSDs'], 
                color=colors[idx], 
                fig=fig, 
                ax=ax, 
                label=title, 
                scale_alpha=scale_alpha,
                zorders=zorders,
                x_range=x_range,
                y_range=y_range,
            )

        utils.generate_legend(ax, remove_duplicates = True, group_by_exp=group_by_exp, loc='outside')
            
        utils.tight_layout(fig, pad=tight_layout_pad)
            
        return fig, ax, save_title

def compare_eMSDs(
    post_processing_objects: List[postprocessing.PostProcessingJob], 
    titles: List[str], 
    colors: List, 
    fig=None, 
    ax=None,
    group_by_exp=False,
    x_range=None,
    y_range=None,
    tight_layout_pad = None,
    show_legend=True,
):

    logging.debug("Comparing eMSDs")
                  
    if fig == None:
        fig, ax = utils.get_figure()

    for idx,(post_processing_object, title) in enumerate(zip(post_processing_objects, titles)):
        logging.debug(f"On plot: {idx+1}")
        postprocessing.plot_eMSD(
            post_processing_object.data_dfs['eMSDs'], 
            color=colors[idx], 
            fig=fig, 
            ax=ax, 
            label=title, 
            num_points = cfg["num_emsd_points"],
            x_range=x_range,
            y_range=y_range,
        )

    utils.generate_legend(ax, remove_duplicates=True, group_by_exp=group_by_exp, loc='outside')
        
    utils.tight_layout(fig, pad=tight_layout_pad)
    
    return fig, ax, "eMSD_comparison"

def compare_powerlaws(
    post_processing_objects: List[postprocessing.PostProcessingJob], 
    titles: List[str], 
    colors: List, 
    mode='log', 
    fig=None, 
    ax=None, 
    regression_points=':',
    tight_layout_pad=None,
    show_legend=True,
):

    logging.debug(f"Comparing powerlaws, regression points: {regression_points}")
        
    if mode=='linear':
        rows, cols = get_grid_dimensions(len(post_processing_objects))
        fig, axs = utils.get_figure(rows, cols, sharex=False, sharey=False, gridspec_kw={'hspace':0, 'wspace':0})
        
        for idx,(post_processing_object, title) in enumerate(zip(post_processing_objects, titles)):
            logging.debug(f"On plot: {idx+1}")

            row = idx // cols
            col = idx % cols
            
            if rows == 1:
                ax = axs[col]
            else:
                ax = axs[row, col]

            postprocessing.plot_powerlaw(
                post_processing_object.data_dfs['eMSDs'], 
                mode=mode,
                color=colors[idx], 
                fig=fig, 
                ax=ax, 
                label=title, 
                regression_points=regression_points, 
                num_points_display = cfg["num_emsd_points"],
                axes_labels = False
            )

        add_sup_labels(fig, "Lag Time (s)", r'MSD (µm$^2$)')
        utils.tight_layout(fig, pad=tight_layout_pad)
        
    elif mode == 'log':
        if fig == None:
            fig, ax = utils.get_figure()
        for idx,(post_processing_object, title) in enumerate(zip(post_processing_objects, titles)):
            logging.debug(f"On plot: {idx+1}")

            postprocessing.plot_powerlaw(
                post_processing_object.data_dfs['eMSDs'], 
                mode=mode,
                color=colors[idx], 
                fig=fig, 
                ax=ax, 
                label=title, 
                regression_points=regression_points, 
                num_points_display = cfg["num_emsd_points"]
            )

        utils.generate_legend(ax, loc='outside')
        
        utils.tight_layout(fig, pad=tight_layout_pad)
        
    return fig, ax, f"powerlaw_comparison_{mode}"

def compare_vertical_histograms(
    post_processing_objects: List[postprocessing.PostProcessingJob], 
    titles: List[str], 
    colors: List, 
    lag_frame, 
    fig=None, 
    ax=None, 
    density=True, 
    save_title="vertical_histogram_comparison",
    tight_layout_pad=None,
    show_legend=True,
):

    logging.debug(f"Comparing vertical histograms, lag_frame: {lag_frame}, density: {density}")

    if cfg["frame_histogram_type"] == 'spread':
        rows, cols = get_grid_dimensions(len(post_processing_objects))
        if fig == None:
            fig, axs = utils.get_figure(rows, cols, gridspec_kw={'hspace':0, 'wspace':0})
        
        for idx,(post_processing_object, title) in enumerate(zip(post_processing_objects, titles)):
            logging.debug(f"On plot: {idx+1}")

            row = idx // cols
            col = idx % cols
            
            if rows == 1:
                ax = axs[col]
            else:
                ax = axs[row, col]

            postprocessing.plot_vertical_histogram(
                post_processing_object.data_dfs['MSDTrajectories'], 
                lag_frame=lag_frame, 
                color=colors[idx], 
                fig=fig, 
                ax=ax, 
                label=title,
                density=density,
                axes_labels = False
            )

        utils.tight_layout(fig, pad=tight_layout_pad)
    
        return fig, axs, save_title

    elif cfg["frame_histogram_type"] == 'stacked':
        if fig == None:
            fig, ax = utils.get_figure()

        for idx,(post_processing_object, title) in enumerate(zip(post_processing_objects, titles)):
            logging.debug(f"On plot: {idx+1}")
            
            postprocessing.plot_vertical_histogram(
                post_processing_object.data_dfs['MSDTrajectories'], 
                lag_frame=lag_frame, color=colors[idx], 
                fig=fig, ax=ax, 
                label=title,
                density=density
            )

        utils.generate_legend(ax, remove_duplicates=True, loc='upper left')
        
        utils.tight_layout(fig, pad=tight_layout_pad)
        
        return fig, ax, save_title
    
def compare_vertical_histograms_overlaid(
    post_processing_objects: List[postprocessing.PostProcessingJob], 
    titles: List[str],
    colors: List, 
    post_processing_object_config, 
    lag_frame, 
    fig=None, 
    ax=None, 
    density=False, 
    save_title="vertical_histogram_comparison_overlaid",
    tight_layout_pad=None,
    show_legend=True,
    **kwargs,
):

    logging.debug(f"Comparing vertical histograms, lag_frame: {lag_frame}, density: {density}")

    rows, cols = get_grid_dimensions(len(post_processing_object_config))
    if fig == None:
        fig, axs = utils.get_figure(rows, cols, sharey=False, gridspec_kw={'hspace':0, 'wspace':0})
    
        
    for plot_idx, condition in enumerate(post_processing_object_config):
        logging.info(f"On condition: {condition/1000} s")
        row = plot_idx // cols
        col = plot_idx % cols
        if rows == 1:
            ax = axs[col]
        else:
            ax = axs[row, col]
            
        logging.debug(f"On plot: {plot_idx+1}")
        scale_factors = []

        for idx,post_processing_object in enumerate(post_processing_object_config[condition]):
            if density:
                scale_factor = 1
            else:
                scale_factor = 1/post_processing_object.get_total_frame_count()
            scale_factors.append(scale_factor)
            label = post_processing_object.get_id()
            
            postprocessing.plot_vertical_histogram(
                post_processing_object.data_dfs['MSDTrajectories'], 
                lag_frame=lag_frame, color=colors[idx], 
                fig=fig, ax=ax, 
                label = label,
                title=f'{condition/1000} s',
                density=density,
                scale_factor=scale_factor,
                axes_labels=False,
                show_n = False,
                **kwargs
            )
            
        if show_legend:
            utils.generate_legend(ax, remove_duplicates = True, title = f'{condition/1000} s', fontsize = 12, loc='upper left')
        
        logging.info(f"Scale factors: {scale_factors}")
    
    
    if density:
        ylabel = "Frequency"
    else:
        ylabel = "Counts"
        
    if rows != 1 or cols != 1:
        add_sup_labels(fig, "log10(MSD)", ylabel)
    else:
        ax.set_ylabel(ylabel)
        ax.set_xlabel("log10(MSD)")
        
    utils.tight_layout(fig, pad=tight_layout_pad)
    
    return fig, ax, save_title

def get_id_element(title, el):
    """
    Get the id element from the title string.
    Args:
        title (str): The title string to search.
        el (str): The element to search for (e.g., 'M', 'X', 'T', 'L').
    Returns:
        int: The id element if found, otherwise -1.
    """
    regex_match = r'(' + el + r'\d+\.?\d*)'
    match = re.search(regex_match, title)
    if match is None:
        return -1
    return match.group(1)

def map_compare_titles(titles, delays):
    all_titles = []
    suggestions = []
    
    # remove common information from titles
    title_ids = []
    id_infos = {
        'M':[],
        'X':[],
        'T':[],
        'L':[],
    }
    for title in titles:
        title_ids.append(utils.search_regex_id(title, depth = 1))
        for el in id_infos.keys():
            id_info = get_id_element(title_ids[-1], el)
            if id_info != -1:
                id_infos[el].append(id_info)
            else:
                id_infos[el].append(-1)
    
    for el in id_infos.keys():
        if len(set(id_infos[el])) == 1 and id_infos[el][0] != -1:
            logging.info(f"Removing common info {id_infos[el][0]} from titles")
            add_before = ''
            add_after = ''
            if list(id_infos.keys()).index(el) < 4:
                add_after = '_'
            elif list(id_infos.keys()).index(el) > 0:
                add_before = '_*'
                
            for idx, title in enumerate(title_ids):
                title_ids[idx] = re.sub(add_before + r'(' + el + r'\d+\.?\d*)' + add_after, '', title)
    
    for this_title, delay in zip(title_ids, delays):
        # this_title = utils.search_regex_id(title, depth = 1)
        if this_title not in all_titles:
            all_titles.append(this_title)
            
        if delay < 1000:
            this_title = '[{0:.1f} s] '.format(delay/1000) + this_title
        else:
            this_title = '[{0:.0f} s] '.format(delay/1000) + this_title
        suggestions.append(this_title)
    
    categories = {title:[suggestion,str] for (title, suggestion) in zip(titles, suggestions)}
    categories['group by exp'] = [False,bool]
    categories, root = utils.solicit_input(categories, width=30)
    root.destroy()
    
    output = [categories[title] for title in titles]
    return output, categories['group by exp'], all_titles

def get_grid_dimensions(n):
    cols = int(np.ceil(np.sqrt(n)))
    rows = int(np.ceil(n / cols))
    
    return rows, cols

def reorder_lists_custom(l1, l2, numbers = None, bypass = False):
    # reorder l1 and l2 according to input from l1
    if not bypass:
        if len(l1) != len(l2):
            raise RuntimeError

        if not numbers:
            numbers = [i+1 for i in range(len(l1))]
            
        categories = {l1_item:[i, int] for (l1_item, i) in zip(l1, numbers)}
        new_order, root = utils.solicit_input(categories)
        root.destroy()
    
    new_l1 = [None for _ in range(len(l1))]
    new_l2 = [None for _ in range(len(l1))]
    
    if bypass:
        for idx,number in enumerate(numbers):
            new_l1[number-1] = l1[idx]
            new_l2[number-1] = l2[idx]
        # new_order = {}    
        # TODO: make this into list
        
    else:
        for itr_idx,key in enumerate(new_order.keys()):
            list_idx = new_order[key]-1
            new_l1[list_idx] = l1[itr_idx]
            new_l2[list_idx] = l2[itr_idx]
            
    return new_l1, new_l2

def add_sup_labels(fig, x_label, y_label):
    mid_x = (fig.subplotpars.right + fig.subplotpars.left) / 2
    mid_y = (fig.subplotpars.top + fig.subplotpars.bottom) / 2
    fig.supxlabel(x_label, x=mid_x, y=0.05)
    fig.supylabel(y_label, y=mid_y, x=0.05)