%matplotlib

# import argparse
import os
import re
import time
import fnmatch
import numpy as np
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt
from numpy.polynomial import Polynomial

from iv_sipm_class import *

### TO BE ADAPTED TO YOUR FILESYSTEM ###
# BASEPATH = "/Users/luca/Downloads/HPK-R00030/"
BASEPATH = "Data/"

myfiles = {'LN2':   {'FWD': [], 'REV': []},
           'RoomT': {'FWD': [], 'REV': []} }

TEMPERATURES = list(myfiles.keys())
DIRECTIONS = ['FWD','REV']

### Prepare DICT with files to be processed
for root, dirs, files in os.walk(BASEPATH):
    
    if "DCR" in dirs:
        dirs.remove('DCR')
    
    if fnmatch.fnmatch(root, "*LN2"):
        myfiles['LN2'] = {D: [os.path.join(root, file) for file in files if file.find(D) > -1] for D in DIRECTIONS}
        myfiles['LN2']['REV'].sort()

    if fnmatch.fnmatch(root, "*RoomT"):
        myfiles['RoomT'] = {D: [os.path.join(root, file) for file in files if file.find(D) > -1] for D in DIRECTIONS }
        myfiles['RoomT']['REV'].sort()

fig, ax = plt.subplots(2,2)

datafiles = myfiles[TEMPERATURES[0]]
sipmf = iv(TEMPERATURES[0],datafiles)

datafiles = myfiles[TEMPERATURES[1]]
sipmc = iv(TEMPERATURES[1],datafiles)

sipmf.fit_iv()
sipmc.fit_iv()

sipmc.plot_iv('RoomT',ax[0])
sipmf.plot_iv('LN2',ax[1])
fig.tight_layout()

# # FWD
# # plt.scatter(sipm1.ivf.V, sipm1.ivf.I, marker='.', color='darkgrey')
# # plt.plot(sipm1.fitf.V, sipm1.fitf.I, color='darkred')

# # REV
# plt.scatter(sipm1.ivr.V, sipm1.ivr.norm_dIdV, marker='.', color='darkgrey')
# plt.plot(sipm1.fitr.V, sipm1.fitr.norm_dIdV, color='darkred')
