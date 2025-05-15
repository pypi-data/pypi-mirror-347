import os
import pims
import tifffile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import json

def add_sup_labels(fig, x_label, y_label):
    mid_x = (fig.subplotpars.right + fig.subplotpars.left) / 2
    mid_y = (fig.subplotpars.top + fig.subplotpars.bottom) / 2
    fig.supxlabel(x_label, x=mid_x, y=0.05)
    fig.supylabel(y_label, y=mid_y, x=0.05)

fig, ax = plt.subplots(2,2, gridspec_kw={'hspace': 0, 'wspace': 0})

add_sup_labels(fig, 'X-axis', 'Y-axis')
fig.tight_layout

plt.show()