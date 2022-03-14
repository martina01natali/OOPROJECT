"""
Fare plot con subplots con entrambe le condizioni sperimentali caldo (roomT) e freddo (LN2): roomT in alto e freddo sotto.
A sinistra fwd e a destra rversed con sovraimposto fit
"""
# Script to read SiPM files
# Make a script which goal is to:
#

import os
import re
import csv
import fnmatch
import numpy as np
import pandas as pd
import matplotlib as mplt
import matplotlib.pyplot as plt
from scipy import special as sp
from scipy.optimize import curve_fit

###########################################################
class iv():

# Nell'init metto la lettura del file
# In tutti gli altri metodi utilizzerò i dati letti nell'init e farò le varie cose che voglio fare

    def __init__(self, temperature, datafiles=None):
        if datafiles is None:
                datafiles = {'FWD': [], 'REV':[]}

        self.temperature = temperature
        self.params = params[temperature]
        self.degree = params[degree]
        self.datafiles = datafiles
        self.ivf = pd.DataFrame()
        self.ivr = pd.DataFrame

    for datafile in datafiles['FWD']:

# Metodo che fa i fit della FWD
# Notare che anche nel codice di Tom ci sono delle cose che andrebbero protette con dei try o dei raise error

    def fit_ivf(self):
        self.fitf = self.ivf[self.ivf.V > self.params['threshold']]

        fit_par, fit_extra = Polynomial.fit(self.fitf.V, self.fitf.I, deg=1,
        )


    def fit_ivr(self):

    def fir_iv(self):
