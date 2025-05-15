import sys
sys.path.append(r'D:\Northwestern University\RCH-WANG-GROUP - Documents\ORG-RSRCH-WANG-GROUP\Sync to Personal Computers\Chris\Research\Programming Scripts\pySPT')
import SPTpython.config as config
cfg = config.load_config() # script uses config parameters
colors = cfg["color_palette"]

# 'use_function_titles': [
#     "MSDs, superimposed",
#     "MSDs, spread",
#     "eMSDs",
#     "Powerlaws, log",
#     "Powerlaws, linear",
# ]

# 'use_function_titles': [
#     "Emitters, all",
#     "Emitters, traj",
#     "Traj lengths",
#     "Jump distances",
#     "MSDs, superimposed",
#     "MSDs, spread",
#     "eMSDs",
#     "Powerlaws, log",
#     "Powerlaws, linear",
#     "Vertical histograms, density",
#     "Vertical histograms, counts"
#     "Vertical histograms, overlaid, counts", # for repeat delays
#     "Vertical histograms, overlaid, density", # for repeat delays
# ]

# 'use_function_titles': [
#     "Emitters, all",
#     "Emitters, traj",
#     "Traj lengths",
#     "Jump distances",
#     "MSDs, superimposed",
#     "MSDs, spread",
#     "eMSDs",
#     "Powerlaws, log",
#     "Powerlaws, linear",
#     "Vertical histograms, density",
#     "Vertical histograms, counts"
#     "Vertical histograms, overlaid, counts", # for repeat delays
#     "Vertical histograms, overlaid, density", # for repeat delays
# ]

msd_y_range = [5e-7, 5] # um^2
msd_x_range_3sets = [2.5e-1, 5e2]
msd_x_range_4sets = [2.5e-1, 3e4]

comparison_config = {
    ####################################
    # 1. 0x, 10% tracer load, vary delay
    ####################################
    "1. 0x, 10% tracer load, vary delay": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_21_2025_11_03_27\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_21_2025_11_03_21\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_35_47\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 10% Sticker Tracer",
                "[4 s] 10% Sticker Tracer",
                "[40 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "Jump distances",
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ],
        'custom_colors': [
            [colors[2], colors[2], colors[2]],
            [colors[2]]
        ],
        'kwargs': {
            "MSDs, superimposed": {
                'x_range': msd_x_range_3sets,
                'y_range': msd_y_range,
                'show_legend':False,
            },
            "eMSDs": {
                'x_range': msd_x_range_3sets,
                'y_range': msd_y_range,
                'show_legend':False,
            }
        }
    },
    #########################
    # 2. 0x, vary tracer load
    #########################
    "2. 0x, vary tracer load": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_21_2025_11_03_35\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_21_2025_11_03_31\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_35_48\\metadata.json",
                
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.005\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_21_2025_11_03_49\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.005\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_21_2025_11_03_43\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.005\\40s\\nf50_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_35_45\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_21_2025_11_03_27\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_21_2025_11_03_21\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_35_47\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 0.0% Sticker Tracer",
                "[4 s] 0.0% Sticker Tracer",
                "[40 s] 0.0% Sticker Tracer",
                
                "[0.4 s] 0.2% Sticker Tracer",
                "[4 s] 0.2% Sticker Tracer",
                "[40 s] 0.2% Sticker Tracer",
                
                "[0.4 s] 10% Sticker Tracer",
                "[4 s] 10% Sticker Tracer",
                "[40 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4,5,6,7,8,9
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ],
        'kwargs': {
            "MSDs, superimposed": {
                'x_range': msd_x_range_3sets,
                'y_range': msd_y_range,
            },
            "eMSDs": {
                'x_range': msd_x_range_3sets,
                'y_range': msd_y_range,
            }
        }
    },
    #############################
    # 2.1. 0x vert histogram 0.4s
    #############################
    "2.1. 0x vert histogram 0.4s": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_21_2025_11_03_35\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.005\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_21_2025_11_03_49\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_21_2025_11_03_27\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 0.0% Sticker Tracer",
                "[0.4 s] 0.2% Sticker Tracer",
                "[0.4 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "Vertical histograms, overlaid, density", # for repeat delays
        ],
        'kwargs': {
            "Vertical histograms, overlaid, density": {
                "bins": 30,
                "show_legend":False,
            }
        }
    },
    ######################################
    # 3. 6.5x, 10% tracer load, vary delay
    ######################################
    "3. 6.5x, 10% tracer load, vary delay": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_09_2025_15_25_31\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_26_53\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\40s\\nf150_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_27_28\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\400s\\nf30_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_27_36\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 10% Sticker Tracer",
                "[4 s] 10% Sticker Tracer",
                "[40 s] 10% Sticker Tracer",
                "[400 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4
            ],
        'group_by_exp':True,
        'custom_colors': [
            [colors[2], colors[2], colors[2], colors[2]],
            [colors[2]]
        ],
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ],
        'kwargs': {
            "MSDs, superimposed": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
                'show_legend':False,
            },
            "eMSDs": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
                'show_legend':False,
            }
        }
    },
    #####################################
    # 3.1 6.5x, vertical histogram, 0.4 s
    #####################################
    "3.1 6.5x, vertical histogram, 0.4 s": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_11_2025_09_09_45\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\400ms N2\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_15_2025_11_55_24\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_09_2025_15_25_31\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 0.0% Sticker Tracer",
                "[0.4 s] 0.2% Sticker Tracer",
                "[0.4 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "Vertical histograms, overlaid, density", # for repeat delays
        ],
        'kwargs': {
            "Vertical histograms, overlaid, density": {
                "show_legend":False,
            }
        }
    },
    
    ####################################
    # 3.2 6.5x, vertical histogram, 400s
    ####################################
    "3.2 6.5x, vertical histogram, 400s": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\400s\\nf30_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_11_2025_09_09_51\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\400s N2\\nf50_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_15_2025_11_55_35\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\400s\\nf30_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_27_36\\metadata.json",
            ],
        'labels':
            [
                "[4 s] 0.0% Sticker Tracer",
                "[4 s] 0.2% Sticker Tracer",
                "[4 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "Vertical histograms, overlaid, density", # for repeat delays
        ],
        'kwargs': {
            "Vertical histograms, overlaid, density": {
                "bins": 25,
                "show_legend":False,
            }
        }
    },
    
    ######################################
    # 4. 6.5x, 0% tracer load, vary delay
    ######################################
    "4. 6.5x, 0% tracer load, vary delay": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_11_2025_09_09_45\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_11_2025_09_08_54\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_11_2025_09_09_11\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\400s\\nf30_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_11_2025_09_09_51\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 0% Sticker Tracer",
                "[4 s] 0% Sticker Tracer",
                "[40 s] 0% Sticker Tracer",
                "[400 s] 0% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ],
        'kwargs': { 
            "MSDs, superimposed": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
                'show_legend':False,
            },
            "eMSDs": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
                'show_legend':False,
            }
        }
    },
    #######################################
    # 5. 6.5x, 0.2% tracer load, vary delay
    #######################################
    "5. 6.5x, 0.2% tracer load, vary delay": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\400ms N2\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_15_2025_11_55_24\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\4s N2\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_15_2025_11_53_47\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\40s N2\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_15_2025_11_54_21\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\400s N2\\nf50_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_15_2025_11_55_35\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 0.2% Sticker Tracer",
                "[4 s] 0.2% Sticker Tracer",
                "[40 s] 0.2% Sticker Tracer",
                "[400 s] 0.2% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4
            ],
        'group_by_exp':True,
        'custom_colors': [
            [colors[1], colors[1], colors[1], colors[1]],
            [colors[1]]
        ],
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ],
        'kwargs': {
            "MSDs, superimposed": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
                'show_legend':False,
            },
            "eMSDs": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
                'show_legend':False,
            }
        }
},
    ###########################
    # 6. 6.5x, vary tracer load
    ###########################
    "6. 6.5x, vary tracer load": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_11_2025_09_09_45\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_11_2025_09_08_54\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_11_2025_09_09_11\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\400s\\nf30_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_11_2025_09_09_51\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\400ms N2\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_15_2025_11_55_24\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\4s N2\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_15_2025_11_53_47\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\40s N2\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_15_2025_11_54_21\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\400s N2\\nf50_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_15_2025_11_55_35\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_09_2025_15_25_31\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_26_53\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\40s\\nf150_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_27_28\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\400s\\nf30_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_27_36\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 0% Sticker Tracer",
                "[4 s] 0% Sticker Tracer",
                "[40 s] 0% Sticker Tracer",
                "[400 s] 0% Sticker Tracer",

                "[0.4 s] 0.2% Sticker Tracer",
                "[4 s] 0.2% Sticker Tracer",
                "[40 s] 0.2% Sticker Tracer",
                "[400 s] 0.2% Sticker Tracer",

                "[0.4 s] 10% Sticker Tracer",
                "[4 s] 10% Sticker Tracer",
                "[40 s] 10% Sticker Tracer",
                "[400 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4,5,6,7,8,9,10,11,12,
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ],
        'kwargs': {
            "MSDs, superimposed": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
            },
            "eMSDs": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
            }
        }
    },
    #########################
    # 7. 1x, vary tracer load
    #########################
    "7. 1x, vary tracer load": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_09_2025_11_13_49\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0\\4s\\nf200_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_11_13_50\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0\\40s\\nf30_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_42_14\\metadata.json",
                
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.002\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_24_2025_14_02_57\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.002\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_24_2025_14_02_53\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.002\\40s\\nf50_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_42_17\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_24_2025_14_02_49\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_24_2025_14_02_46\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_42_15\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 0% Sticker Tracer",
                "[4 s] 0% Sticker Tracer",
                "[40 s] 0% Sticker Tracer",

                "[0.4 s] 0.2% Sticker Tracer",
                "[4 s] 0.2% Sticker Tracer",
                "[40 s] 0.2% Sticker Tracer",

                "[0.4 s] 10% Sticker Tracer",
                "[4 s] 10% Sticker Tracer",
                "[40 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4,5,6,7,8,9,
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ],
        'kwargs': {
            "MSDs, superimposed": {
                'x_range': msd_x_range_3sets,
                'y_range': msd_y_range,
            },
            "eMSDs": {
                'x_range': msd_x_range_3sets,
                'y_range': msd_y_range,
            }
        }
    },
    ############################################
    # 7.1. 1x vary tracer vertical histogram, 4s
    ############################################
    "7.1. 1x vary tracer vertical histogram, 4s": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0\\4s\\nf200_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_11_13_50\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.002\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_24_2025_14_02_53\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_24_2025_14_02_46\\metadata.json",
            ],
        'labels':
            [
                "[4 s] 0.0% Sticker Tracer",
                "[4 s] 0.2% Sticker Tracer",
                "[4 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "Vertical histograms, overlaid, density", # for repeat delays
        ],
        'kwargs': {
            "Vertical histograms, overlaid, density": {
                "bins": 25,
                "show_legend":False,
            }
        }
    },
    ##############################
    # 8. 0x vs 1x, 10% tracer load
    ##############################
    "8. 0x vs 1x, 10% tracer load": {
        'paths':
            [
                # 0x
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_21_2025_11_03_27\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_21_2025_11_03_21\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_35_47\\metadata.json",

                # 1x
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_24_2025_14_02_49\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_24_2025_14_02_46\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_42_15\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 0x, 10% Sticker Tracer",
                "[4 s] 0x, 10% Sticker Tracer",
                "[40 s] 0x, 10% Sticker Tracer",
                
                "[0.4 s] 1x, 10% Sticker Tracer",
                "[4 s] 1x, 10% Sticker Tracer",
                "[40 s] 1x, 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4,5,6,
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ],
        'kwargs': {
            "MSDs, superimposed": {
                'x_range': msd_x_range_3sets,
                'y_range': msd_y_range,
            },
            "eMSDs": {
                'x_range': msd_x_range_3sets,
                'y_range': msd_y_range,
            }
        }
    },
    
    ############################################
    # 8.1. 0x vs 1x, 10%, vertical histogram, 4s
    ############################################
    "8.1. 0x vs 1x, 10%, vertical histogram, 4s": {
        'paths':
            [
                # 0x
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_21_2025_11_03_21\\metadata.json",

                # 1x
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_24_2025_14_02_46\\metadata.json",
            ],
        'labels':
            [
                "[4 s] 0x, 10% Sticker Tracer",
                "[4 s] 1x, 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "Vertical histograms, overlaid, density", # for repeat delays
        ],
        'kwargs': {
            "Vertical histograms, overlaid, density": {
                "bins": 25,
                "show_legend":False,
            }
        }
    },
    
    #########################
    # 9. 2x, vary tracer load
    #########################
    "9. 2x, vary tracer load": {
        'paths':
            [
               "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0\\replicate\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_May_05_2025_10_33_32\\metadata.json",
               "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_33_29\\metadata.json",
               "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0\\replicate\\40s\\nf50_d40000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_33_30\\metadata.json",
               
               "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.002\\replicate\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_May_05_2025_10_33_40\\metadata.json",
               "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.002\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_33_36\\metadata.json",
               "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.002\\replicate\\40s\\nf50_d40000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_33_38\\metadata.json",
               
               "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.1\\replicate\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_01_2025_15_55_07\\metadata.json",
               "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.1\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_54_55\\metadata.json",
               "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.1\\replicate\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_58_12\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 0% Sticker Tracer",
                "[4 s] 0% Sticker Tracer",
                "[40 s] 0% Sticker Tracer",

                "[0.4 s] 0.2% Sticker Tracer",
                "[4 s] 0.2% Sticker Tracer",
                "[40 s] 0.2% Sticker Tracer",

                "[0.4 s] 10% Sticker Tracer",
                "[4 s] 10% Sticker Tracer",
                "[40 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4,5,6,7,8,9
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ],
        'kwargs': {
            "MSDs, superimposed": {
                'x_range': msd_x_range_3sets,
                'y_range': msd_y_range,
            },
            "eMSDs": {
                'x_range': msd_x_range_3sets,
                'y_range': msd_y_range,
            }
        }
    },
    
    #############################################
    # 9.1. 2x, vary tracer, vertical histogram 4s
    #############################################
    "9.1. 2x, vary tracer, vertical histogram 4s": {
        'paths':
            [
               "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_33_29\\metadata.json",
               "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.002\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_33_36\\metadata.json",
               "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.1\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_54_55\\metadata.json",
            ],
        'labels':
            [
                "[4 s] 0% Sticker Tracer",
                "[4 s] 0.2% Sticker Tracer",
                "[4 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "Vertical histograms, overlaid, density", # for repeat delays
        ],
        'kwargs': {
            "Vertical histograms, overlaid, density": {
                "bins": 25,
                "show_legend":False,
            }
        }
    },
    
    ##########################
    # 10. 3x, vary tracer load
    ##########################
    "10. 3x, vary tracer load": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_02_2025_09_13_48\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_02_2025_09_13_40\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_02_2025_09_13_44\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0\\400s\\nf40_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_02_2025_09_16_36\\metadata.json",
                
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.002\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_26_2025_13_44_58\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.002\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_26_2025_13_44_48\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.002\\40s\\nf50_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_26_2025_13_44_51\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.002\\400s\\nf25_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_26_2025_13_44_59\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_01_2025_15_54_04\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_53_34\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_53_50\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\400s\\nf50_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_54_13\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 0% Sticker Tracer",
                "[4 s] 0% Sticker Tracer",
                "[40 s] 0% Sticker Tracer",
                "[400 s] 0% Sticker Tracer",

                "[0.4 s] 0.2% Sticker Tracer",
                "[4 s] 0.2% Sticker Tracer",
                "[40 s] 0.2% Sticker Tracer",
                "[400 s] 0.2% Sticker Tracer",

                "[0.4 s] 10% Sticker Tracer",
                "[4 s] 10% Sticker Tracer",
                "[40 s] 10% Sticker Tracer",
                "[400 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4,5,6,7,8,9,10,11,12
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ],
        'kwargs': {
            "MSDs, superimposed": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
            },
            "eMSDs": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
            }
        }
    },
    
    ################################################
    # 10.1. 3x, vary tracer, vertical histogram, 40s
    ################################################
    "10.1. 3x, vary tracer, vertical histogram, 40s": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_02_2025_09_13_44\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.002\\40s\\nf50_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_26_2025_13_44_51\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_53_50\\metadata.json",
            ],
        'labels':
            [
                "[40 s] 0% Sticker Tracer",
                "[40 s] 0.2% Sticker Tracer",
                "[40 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "Vertical histograms, overlaid, density", # for repeat delays
        ],
        'kwargs': {
            "Vertical histograms, overlaid, density": {
                "bins": 20,
                "show_legend":False,
            }
        }
    },

    ##########################
    # 11. 4x, vary tracer load
    ##########################
    "11. 4x, vary tracer load": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_May_01_2025_12_27_11\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_27_06\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0\\40s\\nf40_d40000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_27_08\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0\\400s\\nf25_d400000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_27_11\\metadata.json",
                
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.002\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_May_01_2025_12_27_02\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.002\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_26_57\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.002\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_26_59\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.002\\400s\\nf40_d400000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_27_03\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_29_2025_10_20_20\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_14\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\40s\\nf85_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_16\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\400s\\nf50_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_21\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 0% Sticker Tracer",
                "[4 s] 0% Sticker Tracer",
                "[40 s] 0% Sticker Tracer",
                "[400 s] 0% Sticker Tracer",

                "[0.4 s] 0.2% Sticker Tracer",
                "[4 s] 0.2% Sticker Tracer",
                "[40 s] 0.2% Sticker Tracer",
                "[400 s] 0.2% Sticker Tracer",

                "[0.4 s] 10% Sticker Tracer",
                "[4 s] 10% Sticker Tracer",
                "[40 s] 10% Sticker Tracer",
                "[400 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4,5,6,7,8,9,10,11,12
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ],
        'kwargs': {
            "MSDs, superimposed": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
            },
            "eMSDs": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
            }
        }
    },
    
    ################################################
    # 11.1. 4x, vary tracer, vertical histogram, 40s
    ################################################
    "11.1. 4x, vary tracer, vertical histogram, 40s": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0\\40s\\nf40_d40000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_27_08\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.002\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_26_59\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\40s\\nf85_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_16\\metadata.json",
            ],
        'labels':
            [
                "[40 s] 0% Sticker Tracer",
                "[40 s] 0.2% Sticker Tracer",
                "[40 s] 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "Vertical histograms, overlaid, density", # for repeat delays
        ],
        'kwargs': {
            "Vertical histograms, overlaid, density": {
                "bins": 20,
                "show_legend":False,
            }
        }
    },
    
    #################################
    # 12. 10% tracer load, vary xlink
    #################################
    "12. 10% tracer load, vary xlink": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_21_2025_11_03_27\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_21_2025_11_03_21\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_35_47\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_24_2025_14_02_49\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_24_2025_14_02_46\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_42_15\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_01_2025_15_54_04\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_53_34\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_53_50\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\400s\\nf50_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_54_13\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_29_2025_10_20_20\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_14\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\40s\\nf85_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_16\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\400s\\nf50_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_21\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_09_2025_15_25_31\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_26_53\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\40s\\nf150_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_27_28\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\400s\\nf30_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_27_36\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] 0 x/chain",
                "[4 s] 0 x/chain",
                "[40 s] 0 x/chain",

                "[0.4 s] 1 x/chain",
                "[4 s] 1 x/chain",
                "[40 s] 1 x/chain",

                "[0.4 s] 3 x/chain",
                "[4 s] 3 x/chain",
                "[40 s] 3 x/chain",
                "[400 s] 3 x/chain",

                "[0.4 s] 4 x/chain",
                "[4 s] 4 x/chain",
                "[40 s] 4 x/chain",
                "[400 s] 4 x/chain",

                "[0.4 s] 6.5 x/chain",
                "[4 s] 6.5 x/chain",
                "[40 s] 6.5 x/chain",
                "[400 s] 6.5 x/chain",
            ],
            'order':
            [
                1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ],
        'kwargs': {
            "MSDs, superimposed": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
            },
            "eMSDs": {
                'x_range': msd_x_range_4sets,
                'y_range': msd_y_range,
            }
        }
    },
    
    ################################################
    # 13. 10% tracer load, vary xlink, vert hist 40s
    ################################################
    "13. 10% tracer load, vary xlink, vert hist 40s": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_35_47\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_42_15\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_53_50\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\40s\\nf85_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_16\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\40s\\nf150_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_27_28\\metadata.json",
            ],
        'labels':
            [
                "[40 s] 0 x/chain",
                "[40 s] 1 x/chain",
                "[40 s] 3 x/chain",
                "[40 s] 4 x/chain",
                "[40 s] 6.5 x/chain",
            ],
            'order':
            [
                1,2,3,4,5,
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "Vertical histograms, overlaid, density", # for repeat delays
        ],
        'kwargs': {
            "Vertical histograms, overlaid, density": {
                "bins": 30,
                "tight_layout_pad":2,
                "show_legend":False,
            }
        }
    },
    
    #######################
    # 100. PMMA, vary delay
    #######################
    "100. PMMA, vary delay": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M10_X0_T0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_May_02_2025_11_49_49\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M10_X0_T0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_09_59_15\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M10_X0_T0\\40s\\nf100_d40000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_00_19\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M10_X0_T0\\400s\\nf40_d400000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_00_37\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] PMMA",
                "[4 s] PMMA",
                "[40 s] PMMA",
                "[400 s] PMMA",
            ],
            'order':
            [
                1,2,3,4,
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ]
    },
    
    #####################################
    # 101. PMMA vs. 6.5x, 10% tracer load
    #####################################
    "101. PMMA vs. 6.5x, 10% tracer load": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M10_X0_T0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_May_02_2025_11_49_49\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M10_X0_T0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_09_59_15\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M10_X0_T0\\40s\\nf100_d40000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_00_19\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M10_X0_T0\\400s\\nf40_d400000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_00_37\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_09_2025_15_25_31\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_26_53\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\40s\\nf150_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_27_28\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\400s\\nf30_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_27_36\\metadata.json",

            ],
        'labels':
            [
                "[0.4 s] PMMA",
                "[4 s] PMMA",
                "[40 s] PMMA",
                "[400 s] PMMA",
                
                "[0.4 s] 6.5x, 10% Sticker Tracer",
                "[4 s] 6.5x, 10% Sticker Tracer",
                "[40 s] 6.5x, 10% Sticker Tracer",
                "[400 s] 6.5x, 10% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4,5,6,7,8
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
        ]
    },
    #########################
    # 102. 0x dyed and undyed
    #########################
    "102. 0x dyed and undyed": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_01_2025_14_50_17\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_55_22\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T0\\40s\\nf40_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_14_50_05\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_21_2025_11_03_35\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_21_2025_11_03_31\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_35_48\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] Undyed",
                "[4 s] Undyed",
                "[40 s] Undyed",
                
                "[0.4 s] Dyed, 0% Sticker Tracer",
                "[4 s] Dyed, 0% Sticker Tracer",
                "[40 s] Dyed, 0% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4,5,6
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
            "Vertical histograms, overlaid, counts", # for repeat delays
        ]
    },
    #########################
    # 103. 1x dyed and undyed
    #########################
    "103. 1x dyed and undyed": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_24_2025_14_03_01\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_24_2025_14_02_59\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T0\\40s\\nf50_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_24_2025_14_03_00\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_09_2025_11_13_49\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0\\4s\\nf200_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_11_13_50\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0\\40s\\nf30_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_42_14\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] Undyed",
                "[4 s] Undyed",
                "[40 s] Undyed",
                
                "[0.4 s] Dyed, 0% Sticker Tracer",
                "[4 s] Dyed, 0% Sticker Tracer",
                "[40 s] Dyed, 0% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4,5,6
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
            "Vertical histograms, overlaid, counts", # for repeat delays
        ]
    },
    ###########################
    # 104. 6.5x dyed and undyed
    ###########################
    "104. 6.5x dyed and undyed": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_16_2025_10_08_37\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_16_2025_10_08_30\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T0\\40s\\nf125_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_16_2025_10_08_32\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T0\\400s\\nf25_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_16_2025_10_08_38\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_11_2025_09_09_45\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_11_2025_09_08_54\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_11_2025_09_09_11\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\400s\\nf30_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_11_2025_09_09_51\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] Undyed",
                "[4 s] Undyed",
                "[40 s] Undyed",
                "[400 s] Undyed",
                
                "[0.4 s] Dyed, 0% Sticker Tracer",
                "[4 s] Dyed, 0% Sticker Tracer",
                "[40 s] Dyed, 0% Sticker Tracer",
                "[400 s] Dyed, 0% Sticker Tracer",
            ],
            'order':
            [
                1,2,3,4,5,6,7,8
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
            "Vertical histograms, overlaid, counts", # for repeat delays
        ]
    },
    
    #########################
    # 105. 2x, 0.2%, replicate
    #########################
    "105. 2x, 0.2%, replicate": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.002\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_26_2025_13_44_39\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.002\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_26_2025_13_44_31\\metadata.json",       
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.002\\40s\\nf100_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_58_04\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.002\\replicate\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_May_05_2025_10_33_40\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.002\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_33_36\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.002\\replicate\\40s\\nf50_d40000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_33_38\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] Original",
                "[4 s] Original",
                "[40 s] Original",
                
                "[0.4 s] Replicate",
                "[4 s] Replicate",
                "[40 s] Replicate",
            ],
            'order':
            [
                1,2,3,4,5,6,
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
            "Vertical histograms, overlaid, density", # for repeat delays
        ]
    },
    
    ###########################
    # 106. 4x, 10%, replicate
    ###########################
    "106. 4x, 10%, replicate": {
        'paths':
            [
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_01_2025_15_54_40\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_54_27\\metadata.json",  
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\40s\\nf220_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_54_33\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\400s\\nf19_d400000.0_e2560.0_p15.0_NDTiffStack_Apr_01_2025_15_54_42\\metadata.json",

                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_29_2025_10_20_20\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_14\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\40s\\nf85_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_16\\metadata.json",
                "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\400s\\nf50_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_21\\metadata.json",
            ],
        'labels':
            [
                "[0.4 s] Original",
                "[4 s] Original",
                "[40 s] Original",
                "[400 s] Original",
                
                "[0.4 s] Replicate",
                "[4 s] Replicate",
                "[40 s] Replicate",
                "[400 s] Replicate",
            ],
            'order':
            [
                1,2,3,4,5,6,7,8
            ],
        'group_by_exp':True,
        'use_function_titles': [
            "MSDs, superimposed",
            "MSDs, spread",
            "eMSDs",
            "Powerlaws, log",
            "Powerlaws, linear",
            "Vertical histograms, overlaid, density", # for repeat delays
        ]
    },
}

emsd_path_10per = {
    '0x, 10%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_21_2025_11_03_27\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_21_2025_11_03_21\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.1\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_35_47\\metadata.json",
    ],
    
    '1x, 10%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_24_2025_14_02_49\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_24_2025_14_02_46\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.1\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_42_15\\metadata.json",
    ],
    '2x, 10%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.1\\replicate\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_01_2025_15_55_07\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.1\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_54_55\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.1\\replicate\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_58_12\\metadata.json",
    ],
    '3x, 10%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_01_2025_15_54_04\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_53_34\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_53_50\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.1\\400s\\nf50_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_01_2025_15_54_13\\metadata.json",
    ],
    
    '4x, 10%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_29_2025_10_20_20\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_14\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\40s\\nf85_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_16\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.1\\replicate\\400s\\nf50_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_29_2025_10_20_21\\metadata.json",
    ],
    '6.5x, 10%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_09_2025_15_25_31\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_26_53\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\40s\\nf150_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_27_28\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.1\\ambient\\400s\\nf30_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_15_27_36\\metadata.json",
    ],
}

emsd_path_0_2per = {
    '0x, 0.2%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.005\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_21_2025_11_03_49\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.005\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_21_2025_11_03_43\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0.005\\40s\\nf50_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_35_45\\metadata.json",
    ],
    '1x, 0.2%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.002\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_24_2025_14_02_57\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.002\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_24_2025_14_02_53\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0.002\\40s\\nf50_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_42_17\\metadata.json",
    ],
    '2x, 0.2%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.002\\replicate\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_May_05_2025_10_33_40\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.002\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_33_36\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0.002\\replicate\\40s\\nf50_d40000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_33_38\\metadata.json",
    ],
    '3x, 0.2%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.002\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_26_2025_13_44_58\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.002\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_26_2025_13_44_48\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.002\\40s\\nf50_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_26_2025_13_44_51\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0.002\\400s\\nf25_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_26_2025_13_44_59\\metadata.json",
    ],
    '4x, 0.2%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.002\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_May_01_2025_12_27_02\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.002\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_26_57\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.002\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_26_59\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0.002\\400s\\nf40_d400000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_27_03\\metadata.json",
   ],
    '6.5x, 0.2%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\400ms N2\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_15_2025_11_55_24\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\4s N2\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_15_2025_11_53_47\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\40s N2\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_15_2025_11_54_21\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0.002\\N2 RT\\400s N2\\nf50_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_15_2025_11_55_35\\metadata.json",
    ],
}
    
emsd_path_0per = {
    '0x, 0%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_21_2025_11_03_35\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_21_2025_11_03_31\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X0_T1_L0\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_35_48\\metadata.json",
    ],
    '1x, 0%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_09_2025_11_13_49\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0\\4s\\nf200_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_09_2025_11_13_50\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X1_T1_L0\\40s\\nf30_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_28_2025_09_42_14\\metadata.json",
    ],
    '2x, 0%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0\\replicate\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_May_05_2025_10_33_32\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0\\replicate\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_33_29\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X2_T1_L0\\replicate\\40s\\nf50_d40000.0_e2560.0_p15.0_NDTiffStack1_May_05_2025_10_33_30\\metadata.json",
    ],
    '3x, 0%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_02_2025_09_13_48\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_02_2025_09_13_40\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0\\40s\\nf80_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_02_2025_09_13_44\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X3_T1_L0\\400s\\nf40_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_02_2025_09_16_36\\metadata.json",
    ],
    '4x, 0%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_May_01_2025_12_27_11\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_27_06\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0\\40s\\nf40_d40000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_27_08\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X4_T1_L0\\400s\\nf25_d400000.0_e2560.0_p15.0_NDTiffStack1_May_01_2025_12_27_11\\metadata.json",
    ],
    '6.5x, 0%': [
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\400ms\\nf500_d400.0_e400.0_p96.0_NDTiffStack1_Apr_11_2025_09_09_45\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\4s\\nf500_d4000.0_e2560.0_p15.0_NDTiffStack1_Apr_11_2025_09_08_54\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\40s\\nf250_d40000.0_e2560.0_p15.0_NDTiffStack1_Apr_11_2025_09_09_11\\metadata.json",
        "D:\\Northwestern University\\RCH-WANG-GROUP - Documents\\ORG-RSRCH-WANG-GROUP\\Sync to Lab Computers\\Chris\\M7.5_X6.5_T1_L0\\400s\\nf30_d400000.0_e2560.0_p15.0_NDTiffStack1_Apr_11_2025_09_09_51\\metadata.json",
    ]
}
