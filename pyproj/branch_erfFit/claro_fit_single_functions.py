#!/usr/bin/env python3
"""
Claro_fit homework
**Due Tuesday Nov. 23rd, 2021**
Using Pandas + Scipy
- read one of the claro file
- plot the data points
- fit data with a modified erf function

**Due Friday Dec. 3rd, 2021**
- create function to make the plot
- be sure that function works for all the "good files" in secondolotto_1
- embedd this script by importing it in process_claro_fit
- make everything object-oriented

"""

import pandas as pd
import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt
from scipy import special as sp
from scipy.optimize import curve_fit

#######################################################################

def func(x, a, b, d):
    """
    The correct form of a modified erf function would be
    func(a, ampl, a, b)
        return ampl/2*(1+erf((x-a)/(b*np.sqrt(2))))
    Instead, this function uses a simpler form for the erf function, with parameters the amplitude, rigid shift
    and transition point shift.
    """
    return a*sp.erf((x-b))+d

#######################################################################

def claro_fit(thisfile, # finish arguments ):
    meta = 'INSERT META FROM PROCESS_CLARO_FIT'
    data = 

    AMPLITUDE = 
    TRANSITION = fileinfos['transition']
    WIDTH = -fileinfos['width']



# Fit the data with an erf function



xgrid = np.linspace(xdata.min(), xdata.max(), 500)

GUESSES = [AMPLITUDE, TRANSITION, AMPLITUDE]

popt, pcov = curve_fit(func, data.x, data.y1, p0=GUESSES)

# It is better to define the transition point TRANSITION on the x axis as the first point which y is more than zero
# Also the amplitude of the dataset will be AMPLITUDE
# Also the metadata/parameters should be passed as an input to the initial guess of the fit

TRANSITION1 = popt[1]
AMPLITUDE = data.y1.max()-data.y1.min()

# Scatterplot

plt.figure()
fig, ax = plt.subplots(figsize=(5,5), dpi=300, tight_layout=True)

ygrid = func(xgrid, *popt)

plt.title('Fit CLARO: station 1, chip 259, ch 7')
plt.scatter(data.x, data.y1, label='Data points', zorder=2)
plt.plot(xgrid, ygrid, label='erf fit', zorder=1)
plt.axvline(x=TRANSITION, linestyle='--', label='Transition', alpha=0.5)
plt.xlabel('x [arb units]')
plt.ylabel('y [arb units]')
plt.legend(loc='lower right')
plt.show()

# Use annotate() to create annotation (text) on the plot for parameters provided by the fit and parameters provided by the file
# Use vlines instead of axvline to polish the code when adding also lines of width centered on the transition vertical line
