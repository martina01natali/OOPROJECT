import os
import re
import time
import math
import fnmatch
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy import special as sp
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from numpy.polynomial import Polynomial


# Class definition

class iv():
    """Class for analysis of iv curves of SiPMs.

    # Constructor
    -------------
    iv(temperature:list, datafiles:dict=None, params:dict=None)

    # Attributes
    ------------
    iv.datafiles        Returns the list of the datafiles provided.
    iv.temperature      Returns the temperature.
    iv.ncells           Returns the number of cells in the SiPM.
    iv.params           Returns the dict with the parameters.
    iv.revFitDegree     Returns the chosen degree of the polynomial used to perform the fit of the reverse-bias curve.

    ## Raw data
    iv.ivf              Dataframe with forward (FWD) curve data.
    iv.ivr              Dataframe with reverse (REV) curve data.

    ## Computed properties
    iv.Rq               List with quenching resistance and its error.
    iv.Rq_ind           List with individual cells' quenching resistance and its error.
    iv.Vbd              List with the breakdown voltage and its error.
    iv.printRq          Prints the total and individual cells' quenching resistance.

    ## Fitted data
    iv.fitf             Dataframe with columns I,V where I is the linearly fitted values for the forward direction.
    iv.fitr

    # Methods
    ---------
    __repr__            Magic method to represent instance iv().

    ## Fit
    iv.fit_ivf          Performs the linear fit of the forward curve and computes the quenching resistance.
    iv.fit_ivr          Performs the polynomial fit of the reversed curve and computes the breakdown voltage.
    iv.fit_iv           Performs both fits.

    ## Plot
    iv.plot_ivf         Plots the forward curve, fit and quenching resistance.
    iv.plot_ivr         Plots the reverse curve, discrete derivative, skew gaussian fit and breakdown voltage.
    iv.plot_iv          Shows both forward and reverse plots.


    """

    def __init__(self, temperature:list, datafiles:dict=None, params:dict=None):

        if datafiles is None:
            datafiles = {'FWD': [], 'REV': []}

        if params is None:
            params = {'LN2':   {'threshold': 2,
                                'rev_limits': (41.9,42.4),
                                'xlim': (40,44),
                                'ylim': (1e-12,1e-7),
                                'plt_idx': 0,
                                },
                      'RoomT': {'threshold': 1.25,
                                'rev_limits': (51.9,52.4),
                                'xlim': (50,54),
                                'ylim': (1e-10,1e-4),
                                'plt_idx': 1,
                                },
                      'revFitDegree': 4,
                      'ncells':11188,
         }

        self.datafiles = datafiles
        self.temperature = temperature
        self.ncells = params['ncells']
        self.params = params[temperature]
        self.revFitDegree = params['revFitDegree']

        self.ivf = pd.DataFrame()
        self.ivr = pd.DataFrame()

        for datafile in datafiles['FWD']:
            tempdf = read_df_iv(datafile)
            self.ivf = pd.concat([self.ivf, tempdf], ignore_index=True)
        
        for datafile in reversed(datafiles['REV']):
            answ = input(f"You are working on the REV file {datafile}. Do you want to proceed? (y/n) (n will make you choose another file)")
            if answ=='y':
                tempdf = read_df_iv(datafile)
                self.ivr = pd.concat([self.ivr, tempdf], ignore_index=True)
                break
            else:
                continue

    #--------------------------------

    def __repr__(self):
        return f"temperature: {self.temperature}\n" \
               f"params:      {self.params}\n" \
               f"datafiles:   {self.datafiles}\n\n" \
               f"FWD DF:      {self.ivf.shape[0]} data points in {self.ivf.filename.unique().size} group\n" \
               f"REV DF:      {self.ivr.shape[0]} data points in {self.ivr.filename.unique().size} group\n\n"

    #--------------------------------

    def printRq(self):
        """Print the total and individual-cells' quenching resistance computed by .fit_iv().

        Raises an error if the parameter has not been computed yet.
        """

        try:
            print(f"Quenching resistance: Rq = {self.Rq[0]} ± {self.Rq[1]}")
            print(f"Number of cells: {self.ncells}.\nIndividual cells' quenching resistance: Rq_ind = {self.Rq_ind[0]} ± {self.Rq_ind[1]}")
        except AttributeError as err:
            print(f"[!] Quenching resistance hasn't been computed yet.\n    Call .fit_iv() first.")

    #--------------------------------

    def fit_ivf(self):
        """Class' method that performs fit for current vs tension (forward).

        Exploits dataframe of forward data, threshold of forward data and fit type, given by the params dictionary.

        The quenching resistance is computed from the Ohm's law, as the inverse of the proportionality constant between current and voltage and it corresponds to the total quenching resistance of the SiPM. The expected order of magnitude is 10^2 Ohm.
        To get the cell's individual quenching resistance one must take into account the number of cells of the SiPM: the cells should be in parallel, since they are working at the same voltage, so the individual quenching resistance should be the product between the total quenching resistance and the number of cells.

        """

        self.fitf = self.ivf[ self.ivf.V > self.params['threshold'] ]

        fit_par, fit_extra = Polynomial.fit(self.fitf.V, self.fitf.I, deg = 1, full=True)
        self.fitf = self.fitf.assign( I = lambda x: Polynomial(fit_par.convert().coef)(x.V) )

        self.Rq = [ 1/fit_par.convert().coef[1] ]     # quenching resistance
        self.Rq.append( fit_extra[0][0] )       # delta_Rq (residuals)
        ncells = self.ncells
        self.Rq_ind = [ self.Rq[0]*ncells ]     # individual cells' quenching resistance
        self.Rq_ind.append( self.Rq[1]*ncells )       # delta_Rq (residuals)

    #--------------------------------

    def fit_ivr(self):
        """Class' method that performs fit for current vs tension (reversed).

        The goal is to compute the breakdown voltage, that corresponds to the voltage value of the saddle point in the reverse curve. To do so, one must compute the (normalized) derivative of I vs V and maximize it. To estimate the maximum point and its error, a skew gaussian fit is performed on the higher data of the derivative.

        This method fits the normalized (wrt current) derivative dI/dV using a polynomial of degree provided by revFitDegree (external dict params) and returns the df self.fitr with the fitted data in the new column norm_dIdV. The fit is performed in the range of V provided by rev_limits in the params dict.
        This method exploits the support functions derivative(x,y) and skew_gauss(x, A, mean, dev, alpha, c).
        """

        # Computation of discrete derivative
        self.ivr = self.ivr.assign( norm_dIdV = lambda x: (1/x['I'][1:-1])*derivative(x.V,x.I) )

        self.fitr = self.ivr[ ( self.ivr.V >= self.params['rev_limits'][0] ) & ( self.ivr.V <= self.params['rev_limits'][1] ) ]

        fit_par, fit_extra = Polynomial.fit(self.fitr.V, self.fitr.norm_dIdV, deg = self.revFitDegree, full=True)
        self.fitr = self.fitr.assign( norm_dIdV = lambda x: Polynomial(fit_par.convert().coef)(x.V) )

        self.Vbd = [np.nan,np.nan]

        # Skew gaus fit
        self.norm_dIdV_fit = pd.DataFrame(
            self.fitr[ self.fitr.norm_dIdV > self.fitr.norm_dIdV.max()*0.5 ].copy(),
        )

        diff_list = list(np.diff(self.norm_dIdV_fit['norm_dIdV'][:-1]) - np.diff(self.norm_dIdV_fit['norm_dIdV'][1:]))

        # I am evaluating both the difference with the precedent and the
        # subsequent value at the same time by making the difference between
        # the differences, that gives me
        # a_m -> 2a_n - a_n-1 - a_n+1 with m in range(1,n-1)
        # so I have to append and prepend a value (0)
        diff_list = [0] + diff_list + [0]
        self.norm_dIdV_fit['diff'] = diff_list

        # Poi uso questo parametro per rimuovere i valori troppo diversi dai
        # vicini e ricostruisco il dataframe _fit considerando solo i punti che
        # soddisfano questa condizione
        self.norm_dIdV_fit = self.norm_dIdV_fit[self.norm_dIdV_fit['diff'].abs() < 5]

        # Definiamo anche dei limiti ai parametri della gaussiana distorta: A, mean, devst, alpha:
        # - A puo' variare tra il minimo e il massimo delle y
        # - mean tra x.min e max.x
        # - la dev tra 0 e x.max-x.min
        # - il parametro alpha varia tra -inf e inf
        # - il parametro c varia tra 0 e x.max
        fit_bounds = [
            [ # list of minimum values for all parameters
                self.norm_dIdV_fit.norm_dIdV.min()*0.1,
                self.norm_dIdV_fit.V.min(),
                0,
                -np.inf,
                0,
            ],
            [ # list of maximum values for all parameters
                self.norm_dIdV_fit.norm_dIdV.max(),
                self.norm_dIdV_fit.V.max(),
                self.norm_dIdV_fit.V.max()-self.norm_dIdV_fit.V.min(),
                np.inf,
                self.norm_dIdV_fit.V.max(),
            ]
        ]

        # Ora possiamo chiamare la funzione curve_fit del pacchetto optimize di
        # scipy, che fitta i parametri della nostra gaussiana sulle nostre x
        # (V) e y (I^-1 dI/dV) e restituisce i parametri (popt) e la matrice
        # di covarianza (pcov)

        popt, pcov = curve_fit(skew_gauss,
                               self.norm_dIdV_fit.V,
                               self.norm_dIdV_fit.norm_dIdV,
                               bounds=fit_bounds,
                               maxfev=1000,
                              )

        A, mean, dev, alpha, c = popt[0], popt[1], popt[2], popt[3], popt[4]

        self.norm_dIdV_fit['gauss'] = skew_gauss(self.fitr.V, A, mean, dev, alpha, c)

        self.Vbd = [mean, dev]

    #--------------------------------

    def fit_iv(self):
        """Performs both forward and reverse fit with this single method.

        """

        self.fit_ivf()
        self.fit_ivr()

    #--------------------------------

    def plot_ivf(self,temperature,ax):
        """Class' method: plot of forward, current vs voltage scatterplot and fit.

        The figure ax is provided as an argument.
        """

        ax[0].scatter(self.ivf.V,self.ivf.I, marker='.', s=5) # scatterplot
        ax[0].plot(self.fitf.V, self.fitf.I, color='darkred') # fit curve

        ax[0].text(0.1,0.8,
                   r'$R_q=$'+'({:.2f}'.format(self.Rq[0])+r'$\pm$'+'{:.0e})'.format(self.Rq[1])\
                   + r' $\Omega$',
                   transform=ax[0].transAxes,
                   fontsize=12,
                   color='darkred')

        ax[0].set_ylabel("Current (A)")
        ax[0].set_xlabel("Voltage (V)")
        ax[0].grid(True)
        ax[0].set_title(f"FWD @{self.temperature}")

    #--------------------------------

    def plot_ivr(self,temperature,ax):
        """Class' method: plot of reversed, current vs voltage scatterplot and fit.
        """

        ax[1].set_yscale("log")
        ax[1].scatter(self.ivr.V,self.ivr.I, marker='.', s=5)

        ax[1].set_ylabel("Current (A)")
        ax[1].set_xlabel("Voltage (V)")
        ax[1].set_xlim(self.params['xlim'])
        ax[1].set_ylim(self.params['ylim'])
        ax[1].grid(True)
        ax[1].set_title(f"REV @{self.temperature}")

        ax_twin = ax[1].twinx()
        ax_twin.tick_params(axis='y', colors='darkgreen')

        ax_twin.scatter(self.fitr.V,self.fitr.norm_dIdV, marker='.', s=5, color='darkgreen')
        ax_twin.set_ylabel(r"i$^{-1}$$\frac{dI}{dV}$ (V$^{-1}$)", color='darkgreen')
        ax_twin.plot(self.norm_dIdV_fit.V, self.norm_dIdV_fit.gauss, linewidth=1, color='darkorange')

        ax_twin.text(1.3,0.8,
                     r'$V_b=$'+'({:.2f}'.format(self.Vbd[0])+r'$\pm$'+'{:.2f}) V'.format(self.Vbd[1]),
                     transform=ax[0].transAxes,
                     fontsize=12,
                     color='darkorange')

    #--------------------------------

    def plot_iv(self, temperature, ax):
        """Class' method: shows forward and reverse plots.
        """

        self.plot_ivf(temperature, ax)
        self.plot_ivr(temperature, ax)

################################################################################

# Support functions

def read_df_iv(filename):
    """Reads the SiPM IV csv file

    Removes the header, finds the column names, keeps the (renamed) I and V columns, adding the provenance filename columns.

    Arguments
    ---------
    filename: complete path to csv file

    Returns
    -------
    pd.DataFrame with V, I and filename columns
    """

    try:
        # Open the file and read its lines into a list (one line per element):
        with open(filename, 'r') as file_sipm:
            lines = file_sipm.readlines()
        # cycle through the lines lookin for the column names line (starting with "Index")
        # and reading back the csv file from there into a DataFrame and returning it
        for line_counter, line in enumerate(lines):
            if line.startswith("Index"):
                tempdf = pd.read_csv(filename, header = line_counter)
                # add a column with the filename
                tempdf['filename'] = filename.split('/')[-1]
                # drop unnecessary columns and rename columns
                return tempdf[['Value','Reading','filename']].rename(columns={'Reading':'I','Value':'V'})

        # if header is not found, raise exception
        raise ValueError("Header not found")

    except ValueError as err:
        print(f"[!] Error: {err}")

# -----------------------------------------

def derivative(X, Y):
    """Computes a discrete derivative as the ratio of differences of y and x between two consequent data.

    """

    dx = np.diff(X[:-1]) + np.diff(X[1:])
    dy = np.diff(Y[:-1]) + np.diff(Y[1:])
    return dy/dx

# -----------------------------------------


def skew_gauss(x, A, mean, dev, alpha, c):
    """Skew, not-normalized and shifted gaussian distribution.

    References:
    - https://www.wolframalpha.com/input?i=skew+gaussian+distribution
    - https://stackoverflow.com/questions/15400850/scipy-optimize-curve-fit-unable-to-fit-shifted-skewed-gaussian-curve
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skewnorm.html

    """

    pdf = (1/(dev*np.sqrt(2*math.pi)))*np.exp(-(x-mean)**2/(2*dev**2))
    cdf = sp.erf((-alpha*((x-mean)/dev))/(np.sqrt(2)))
    # not-normalization is obtained by *A
    return A*pdf*cdf+c # not normalized, skewed, shifted gaussian
