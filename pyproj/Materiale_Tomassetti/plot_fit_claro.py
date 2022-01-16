%matplotlib

import re
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.special import erf
from scipy.optimize import curve_fit


def mod_erf(x, ampl, a, b):
    return ampl/2*(1 + erf((x-a)/(b*np.sqrt(2))))


TDIR = "/Users/luca/Documents/didattica/fisica/OOP for experimental data analysis/spunti/bash/secondolotto_1/"
ff = "Station_1__11/Station_1__11_Summary/Chip_001/S_curve/Ch_7_offset_0_Chip_001.txt"


mydata = pd.read_csv(TDIR+ff, sep = "\t", skiprows = 1, header=0, names=['X','Y','Ybis'])
mymeta = pd.read_csv(TDIR+ff, sep="\t", header=None, names=['','transition','width'], nrows=1)
# mydata.plot(x='X', y='Y', kind='scatter')

temp = re.findall("[0-9]+", ff)
metadict = {'station': temp[0],
            'sub': temp[2],
            'chip': temp[5],
            'ch': temp[6],
            'offset': temp[7],
            'transition': mymeta.transition[0],
            'width': mymeta.width[0]}

guesses = [1000,mydata[mydata.Y > 50].X.iloc[0],5]
fit_params, fit_extras = curve_fit(mod_erf, mydata.X, mydata.Y, p0=guesses)

xfit = np.linspace(mydata.X.min(), mydata.X.max(), 1001)
yfit = mod_erf(xfit, *fit_params)

# mydata.plot(x='X', y='Y', kind='scatter')
plt.scatter(mydata.X, mydata.Y, label="data points")
plt.plot(xfit, yfit, label="erf fit")
plt.vlines([fit_params[1],fit_params[1]-fit_params[2],fit_params[1]+fit_params[2]], 0, 1000, alpha=.5, label="transition", linestyle=["-","--","--"])
# plt.axvline(fit_params[1]-fit_params[2], 0, 1000, alpha=.5, label="", linestyle="--")
# plt.axvline(fit_params[1]+fit_params[2], 0, 1000, alpha=.5, label="", linestyle="--")

plt.xlabel('X (arb. units)')
plt.ylabel('Y (arb. units)')
plt.title(f"Fit CLARO: station {metadict['station']}, chip {metadict['chip']}, ch {metadict['ch']}" )
plt.legend(loc='lower right')
# plt.xticks(np.linspace(0, 1, 11))
# plt.yticks(np.linspace(0.5, 1, 6))
plt.minorticks_on()
plt.annotate(f'Transition = {fit_params[1]:.2f}\nWidth = {fit_params[2]*2:.2f}',
             xy=(0.025, .975), xycoords='axes fraction', verticalalignment='top',
             fontsize=11)
plt.annotate(f"(from data file)\nTransition = {metadict['transition']:.2f}\nWidth = {metadict['width']:.2f}",
             xy=(0.025, .6), xycoords='axes fraction', verticalalignment='top',
             fontsize=11, color='gray')
plt.grid(linestyle='-', linewidth=.25)