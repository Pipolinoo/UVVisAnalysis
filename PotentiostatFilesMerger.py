import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, time, datetime

import os
from glob import glob
from scipy.integrate import trapz
import matplotlib.cm as cm
import locale
from dateutil.parser import *
from matplotlib.ticker import FuncFormatter, MaxNLocator
from functools import partial
import matplotlib as mpl

from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)

import matplotlib.dates as mdates



PATH = 'UVVis/UVVisCell_Sample04_50nmSi_SolarGen/Potentiostate'
EXT = '*.DTA'
filterString = ''
all_filenames = [file
                 for path, subdir, files in os.walk(PATH)
                 for file in sorted(glob(os.path.join(path, EXT)), key=os.path.getmtime)]

print(len(all_filenames))
skipRowsDict = {
    'LSV': 56,
    'CHRONOA': 61
}

all_potentiostateFiles = []
for filename in all_filenames[0:50]:
    now = None
    identifier = None

    with open(filename, mode='rt') as file:
        lines = file.readlines()
        date = lines[3].strip().split('\t')[2]
        time = lines[4].strip().split('\t')[2]
        datetimeString = date + ' ' + time

        now = parse(datetimeString)

        identifier = lines[1].strip().split('\t')[1]

    data = pd.read_csv(filename, delim_whitespace=True, header=None, skiprows=skipRowsDict[identifier],
                       names=['Pt', 'T', 'Vf', 'Im', 'Vu', 'Sig', 'Ach', 'IERange', 'Over', 'Cycle', 'Temp'],
                       decimal=",")
    data.date = now
    data.identifier = identifier

    all_potentiostateFiles.append(data)

    print(len(all_potentiostateFiles))

for z, file in enumerate(all_potentiostateFiles):
    # file['intensity_smoothed'] = file['intensity'].rolling(200, win_type='nuttall').mean().shift(-100).fillna(1)
    # integrateValue = trapz(file['intensity'], x=file['wavelength'])
    file['T'] = pd.to_timedelta(file['T'], unit='s')
    file['actualTime'] = file.date + file['T']

mergedFile = pd.concat(all_potentiostateFiles)
mergedFileReduced = mergedFile[['actualTime', 'T', 'Vf', 'Im']]

mergedFileReduced.to_csv(f'{PATH}/MergedFile.csv')

