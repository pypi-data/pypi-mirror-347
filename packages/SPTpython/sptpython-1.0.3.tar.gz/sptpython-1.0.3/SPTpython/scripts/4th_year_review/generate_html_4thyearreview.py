import logging
import logging.config
import datetime

import SPTpython.utils as utils
import SPTpython.compare as compare
import SPTpython.CLI as CLI
import SPTpython.config as config
cfg = config.load_config() # script uses config parameters
from comparison_config import comparison_config
from SPTpython.scripts import analyze_emsds

import json
import os
import matplotlib.pyplot as plt
import pandas as pd

def write_metadata_json(path):
    search_path = r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris'
    metadata_list = utils.find_all_metadata(search_path)
    metadata_dict = {}
    for metadata in metadata_list:
        id = utils.search_regex_id(metadata)
        if id not in metadata_dict:
            metadata_dict[id] = []
        metadata_dict[id].append(metadata)
    with open(os.path.join(path, 'all_metadata.json'), 'w') as f:
        json.dump(metadata_dict, f, indent=4)
        
        
def make_htmls(write_data = True):
    launch_html = False
    
    comparison_titles = [
        # idx = 0
        "1. 0x, 10% tracer load, vary delay",
        "2. 0x, vary tracer load",
        "2.1. 0x vert histogram 0.4s",
        "3. 6.5x, 10% tracer load, vary delay",
        "3.1 6.5x, vertical histogram, 0.4 s",
        # idx = 5
        "3.2 6.5x, vertical histogram, 400s",
        "4. 6.5x, 0% tracer load, vary delay",
        "5. 6.5x, 0.2% tracer load, vary delay",
        "6. 6.5x, vary tracer load",
        "7. 1x, vary tracer load",
        # idx = 10
        "7.1. 1x vary tracer vertical histogram, 4s",
        "8. 0x vs 1x, 10% tracer load",
        "8.1. 0x vs 1x, 10%, vertical histogram, 4s",
        "9. 2x, vary tracer load",
        "9.1. 2x, vary tracer, vertical histogram 4s",
        # idx = 15
        "10. 3x, vary tracer load",
        "10.1. 3x, vary tracer, vertical histogram, 40s",
        "11. 4x, vary tracer load",
        "11.1. 4x, vary tracer, vertical histogram, 40s",
        "12. 10% tracer load, vary xlink",
        # idx = 20
        "13. 10% tracer load, vary xlink, vert hist 40s",
        "100. PMMA, vary delay",
        "101. PMMA vs. 6.5x, 10% tracer load",
        "102. 0x dyed and undyed",
        "103. 1x dyed and undyed",
        # idx = 25
        "104. 6.5x dyed and undyed",
        "105. 2x, 0.2%, replicate",
        "106. 4x, 10%, replicate",
    ]
    
    comparison_titles = [
        comparison_titles[16],
        comparison_titles[18],
    ]
    
    for comparison_title in comparison_titles:
        message = f"On title: {comparison_title}..."
        logging.info("-"*len(message))
        logging.info(message)
        logging.info("-"*len(message))
        
        
        plt.close('all')
        
        paths = comparison_config[comparison_title]['paths']
        labels = comparison_config[comparison_title]['labels']
        order = comparison_config[comparison_title]['order']
        group_by_exp = comparison_config[comparison_title]['group_by_exp']
        use_function_titles = comparison_config[comparison_title]['use_function_titles']
        kwargs = {}
        if "kwargs" in comparison_config[comparison_title]:
            kwargs = comparison_config[comparison_title]['kwargs']
        
        custom_colors = []
        if "custom_colors" in comparison_config[comparison_title]:
            custom_colors = comparison_config[comparison_title]['custom_colors']
        comparison = compare.Comparison(
            paths = paths,
            regression_points = '0:5',
            custom_titles = labels,
            custom_order = order,
            group_by_exp = group_by_exp,
            custom_colors = custom_colors,
        )
        
        logging.info("Comparison object created")
        logging.info("Plotting...")
        figs, axs, root_path = comparison.plot(
            bypass=True,
            use_function_titles = use_function_titles,
            all_kwargs = kwargs
        )
        
        comparison_metadata = comparison.__str__()
        
        if write_data:
            CLI.display_plots_browser(
                figs, 
                axs, 
                comparison_metadata, 
                comparison.table_data, 
                comparison.titles,
                comparison_title,
                launch_html=launch_html,
            )

def run_analyze_emsds():
    for key in emsd_path_0per:
        if '2x' in key:
            analyze_emsds.calculate_msd_fits(emsd_path_0per[key], save=True, show_handler=False)

def run_compare_emsds():
    data_0per = {
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X0_T1_L0\eMSDs_May_07_2025_12_47_41':
            {'title':'0x, 0%', 'fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X1_T1_L0\eMSDs_May_07_2025_12_47_44':
            {'title':'1x, 0%', 'fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X2_T1_L0\replicate\eMSDs_May_07_2025_13_35_35':
            {'title':'2x, 0%', 'fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X3_T1_L0\eMSDs_May_07_2025_12_47_51':
            {'title':'3x, 0%', 'fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X4_T1_L0\eMSDs_May_07_2025_12_47_58':
            {'title':'4x, 0%', 'fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X6.5_T1_L0\eMSDs_May_07_2025_12_48_40':
            {'title':'6.5x, 0%', 'fits':[]},
    }
    
    data_0_2per = {
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X0_T1_L0.005\eMSDs_May_07_2025_12_49_15':
            {'title':'0x, 0.2%', 'fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X1_T1_L0.002\eMSDs_May_07_2025_12_49_22':
            {'title':'1x, 0.2%', 'fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X2_T1_L0.002\replicate\eMSDs_May_07_2025_13_33_43':
            {'title':'2x, 0.2%', 'fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X3_T1_L0.002\eMSDs_May_07_2025_12_49_34':
            {'title':'3x, 0.2%', 'fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X4_T1_L0.002\eMSDs_May_07_2025_12_49_41':
            {'title':'4x, 0.2%', 'fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X6.5_T1_L0.002\N2 RT\eMSDs_May_07_2025_12_50_57':
            {'title':'6.5x, 0.2%', 'fits':[]},
    }
    
    data_10per = {
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X0_T1_L0.1\eMSDs_May_07_2025_09_19_04':
            {'title':'0x, 10%','fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X1_T1_L0.1\eMSDs_May_07_2025_09_19_10':
            {'title':'1x, 10%','fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X3_T1_L0.1\eMSDs_May_07_2025_09_19_30':
            {'title':'3x, 10%','fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X4_T1_L0.1\replicate\eMSDs_May_07_2025_09_19_40':
            {'title':'4x, 10%','fits':[]},
        r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Lab Computers\Chris\M7.5_X6.5_T1_L0.1\ambient\eMSDs_May_07_2025_09_20_49':
            {'title':'6.5x, 10%','fits':[]},
    }
    
    logging.info("Analyzing 10% eMSDs...")
    analyze_emsds.analyze_msd_fits(data_10per, save_path = 'analysis/4th_year_review/emsd_comparisons_10%')
    logging.info("\n\nAnalyzing 0% eMSDs...")
    analyze_emsds.analyze_msd_fits(data_0per, save_path = 'analysis/4th_year_review/emsd_comparisons_0%')
    logging.info("\n\nAnalyzing 0.2% eMSDs...")
    analyze_emsds.analyze_msd_fits(data_0_2per, save_path = 'analysis/4th_year_review/emsd_comparisons_0.2%')

def diffusivities_aggregated_plot():
    path = r'scripts/4th_year_review/diffusivities_aggregated.xlsx'
    data = pd.read_excel(path)
    
    fig, ax = utils.get_figure(
        fig_height=config.cfg["fig_height_ppt"],
        fig_width=config.cfg["fig_width_ppt"],
    )
    
    ax.plot(data[data.columns[11]], data[data.columns[12]]*(10**6), 'o', color=colors[0], label='0%', markersize=12)
    ax.plot(data[data.columns[11]], data[data.columns[13]]*(10**6), 'o', color=colors[1], label='0.2%', markersize=12)
    ax.plot(data[data.columns[11]], data[data.columns[14]]*(10**6), 'o', color=colors[2], label='10%', markersize=12)
    
    ax.errorbar(data[data.columns[11]], data[data.columns[12]]*(10**6), yerr=data[data.columns[16]]*(10**6),fmt='none',color=colors[0],capsize=7,capthick=3,elinewidth=3)
    ax.errorbar(data[data.columns[11]], data[data.columns[13]]*(10**6), yerr=data[data.columns[17]]*(10**6),fmt='none',color=colors[1],capsize=7,capthick=3,elinewidth=3)
    ax.errorbar(data[data.columns[11]], data[data.columns[14]]*(10**6), yerr=data[data.columns[18]]*(10**6),fmt='none',color=colors[2],capsize=7,capthick=3,elinewidth=3)
    
    # ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlabel("# xlink/chain")
    ax.set_ylabel("Diffusivity (nm$^2$/s)")
    
    utils.generate_legend(ax, loc='outside')
    utils.tight_layout(fig)
    CLI.resize_figure(fig)
    fig.savefig(os.path.join('scripts/4th_year_review', 'diffusivities_aggregated.png'))
    fig.savefig(os.path.join('scripts/4th_year_review', 'diffusivities_aggregated.svg'))
    
    plt.show()

if __name__ == '__main__':
    time = datetime.datetime.now().strftime("%b_%d_%Y_%H_%M_%S")
    if not os.path.exists('logs/processing'):
        os.makedirs('logs/processing')
    logging.config.fileConfig(r"SPTpython/logging.conf", defaults={'logfilename': f'logs/processing/{time}.log'})

    # path = r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Personal Computers\Chris\Research\Programming Scripts\pySPT\analysis'
    # write_metadata_json(path)
    # make_htmls(write_data=True)
    # run_analyze_emsds()
    # run_compare_emsds()
    # diffusivities_aggregated_plot()