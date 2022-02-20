# import argparse
import os
import re
import time
import math
import scipy
import fnmatch
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy import special as sp
# from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from numpy.polynomial import Polynomial



params = {'LN2':   {'threshold': 2, 
                    'rev_limits': (41.9,42.4),
                    'xlim': (40,44),
                    'ylim': (1e-12,1e-7),
                    'plt_idx': 0},
          'RoomT': {'threshold': 1.25,
                    'rev_limits': (51.9,52.4),
                    'xlim': (50,54),
                    'ylim': (1e-10,1e-4),
                    'plt_idx': 1},
          'revFitDegree': 4
         }

### TO BE COMPLETED ###

class iv():
    """Class for analysis of iv curves of SiPMs
    
    """
    
    def __init__(self, temperature, datafiles=None):

        if datafiles is None:
            datafiles = {'FWD': [], 'REV': []}
        
        ### Attributes ###
        
        # Here I initialize the attributes of the instance of the class
        self.temperature = temperature
        self.params = params[temperature]
        self.revFitDegree = params['revFitDegree']
        self.datafiles = datafiles
        
        self.ivf = pd.DataFrame() #empty attribute, only fixing the type
        self.ivr = pd.DataFrame() #empty attribute, only fixing the type
        
        for datafile in datafiles['FWD']:
            tempdf = read_df_iv(datafile)
            self.ivf = pd.concat([self.ivf, tempdf], ignore_index=True)

        for datafile in reversed(datafiles['REV']):
            # reversed() and final break to keep only the last REV file
            # the read_df_iv function is a function defined outside of this class, 
            tempdf = read_df_iv(datafile) 
            self.ivr = pd.concat([self.ivr, tempdf], ignore_index=True)
            break

    ### Methods ###
    
    # magic method that can be used to impose a certain representation of the instance of the class
    # this method is called by repr(object_name), that returns an object, and is printed out if you
    # call print(repr(object))
    # the str method does the same, but is intended to be human readable, whilst repr is machine-readable
    # in fact, calling str(object) would return the printed version of repr, since str calls repr inside
    def __repr__(self):
        return f"temperature: {self.temperature}\n" \
               f"params:      {self.params}\n" \
               f"datafiles:   {self.datafiles}\n\n" \
               f"FWD DF:      {self.ivf.shape[0]} data points in {self.ivf.filename.unique().size} group\n" \
               f"REV DF:      {self.ivr.shape[0]} data points in {self.ivr.filename.unique().size} group\n\n"
    
    #--------------------------------
    
    def printRq(self):
        """Print the quenching resistance computed by .fit_iv()
        
        Raises an error if the parameter has not been computed yet.
        
        """
        
        try:
            print(f"Quenching resistance: Rq = {self.Rq[0]} ± {self.Rq[1]}")
        except AttributeError as err:
            print(f"[!] Quenching resistance hasn't been computed yet.\n    Call .fit_iv() first.")
            
    #--------------------------------

    # Metodo della classe che performa effettivamente il fit iv forward nel nostro caso
    # Utilizza come attributi il DataFrame dei dati, il valore di soglia dopo il quale fittare (dal dizionario)
    # e il tipo di fit (sempre dal dizionario)

    def fit_ivf(self):
        """Class' method that performs fit for current vs tension (forward)
        
        Exploits threshold of class' instance and fit type.
        
        """
        
        # subsetting the dataframe by taking only values with voltage above threshold
        self.fitf = self.ivf[ self.ivf.V > self.params['threshold'] ]
        
        # linear fit (polynomial deg=1)
        # Polynomial (from numpy.polynomial) creates a polynomial function with given parameters
        # the fit method performs a polynomial fit on given x and y values and provided degree
        fit_par, fit_extra = Polynomial.fit(self.fitf.V, self.fitf.I, deg = 1, full=True)
        
        # the following line substitues current values I in the dataframe with the expected
        # values computed with the linear fit
        # the series.convert().coef method is found in the documentation and is used to
        # extract the coefficients of the fit
        self.fitf = self.fitf.assign( I = lambda x: Polynomial(fit_par.convert().coef)(x.V) )

        print(fit_par)
        print(fit_extra)
        
        # the quenching resistance is computed from the Ohm's law, as the inverse of the
        # proportionality constant between current and voltage
        
        ##################### UPDATES TO MAKE #################################
        # I think the quenching resistance that is computed in this way is the total
        # quenching resistance (should be of order 10^2). To get the cell's
        # individual quenching resistance one must take into account the number
        # of cells of the SiPM
        # - [ ] find # cells of SiPM (in csv datafile?)
        # the cells should be in parallel, since they are working at the same voltage
        # so the individual quenching resistance should be the 
        
        self.Rq = [ 1/fit_par.convert().coef[1] ]     # quenching resistance
        self.Rq.append( fit_extra[0][0] )       # delta_Rq (residuals)


    #--------------------------------
    
    def fit_ivr(self):
        """Class' method that performs fit for current vs tension (reversed)
        
        Fits the normalized (wrt current) derivative dI/dV using a polynomial of degree
        provided by revFitDegree (external dict params) and returns the df self.fitr
        with the fitted data in norm_dIdV. 
        
        """
        
        # calculating the normalized derivative from data points
        # creation of a new column norm_dIdV that contains
        # the normalized derivative dI/dV wrt the current
        # (find more on the slides provided by Guarise)
        # derivative is a user-defined function (found after the end of the class)
        self.ivr = self.ivr.assign( norm_dIdV = lambda x: (1/x['I'][1:-1])*derivative(x.V,x.I) )
        
        # subsetting the dataframe based on reversed values in the
        # range provided by rev_limits (given by external params dict)
        self.fitr = self.ivr[ ( self.ivr.V >= self.params['rev_limits'][0] ) & ( self.ivr.V <= self.params['rev_limits'][1] ) ]
        
        # polynomial fit with degree provided externally as revFitDegree
        fit_par, fit_extra = Polynomial.fit(self.fitr.V, self.fitr.norm_dIdV, deg = self.revFitDegree, full=True)
        
        # replace calculated data points of normalized derivative with fitted data points
        self.fitr = self.fitr.assign( norm_dIdV = lambda x: Polynomial(fit_par.convert().coef)(x.V) )
        
        ##################### UPDATES TO MAKE #################################
        # - [ ] maximize derivative norm_dIdV
        # - [ ] get point of maximum = breakdown voltage (now is NaN :) )
        # THIS IS DONE WITH THE PLOT plot_ivr
        #######################################################################
        
        self.Vbd = [np.nan,np.nan] # breakdown voltage as an attribute

    #--------------------------------

    def fit_iv(self):
        self.fit_ivf()
        self.fit_ivr()
        
    #--------------------------------
        
    # A questo punto, abbiamo assegnato come attributi della classe le x e y del fit..
    # ..e la resistenza di quenching, che stampiamo sul terminale
    # print('Quenching resistance = {:.2f} ohm'.format(self.quenching_resistance))

    # Metodo della classe per creare e mostrare i plot ( e fit) sullo schermo
    # Utilizza come attributi i due DataFrame, le x e y della funzione di fit..
    # ..e gli intervalli di x e y per il plot in rev
    def plot_iv(self, temperature, ax):
        """Class' method: shows forward and reverse plots.
        
        
        """
        
        self.plot_ivf(temperature, ax)
        self.plot_ivr(temperature, ax)
        
    #--------------------------------

    def plot_ivf(self,temperature,ax):
        """Class' method: plot of forward, current vs voltage scatterplot and fit.
        
        The figure ax is provided as an argument.
        
        """
        
        ax[0].scatter(self.ivf.V,self.ivf.I, marker='.', s=5) # scatterplot
        ax[0].plot(self.fitf.V, self.fitf.I, color='darkred') # fit curve
        
        # Creiamo anche un testo, che posizioniamo in alto a sx (coordinate relative) con la resistenza di quenching
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
        
        # Il secondo elemento della lista ax corrisponde al plot in rev

        ax[1].set_yscale("log")
        ax[1].scatter(self.ivr.V,self.ivr.I, marker='.', s=5)

        ax[1].set_ylabel("Current (A)")
        ax[1].set_xlabel("Voltage (V)")
        ax[1].set_xlim(self.params['xlim'])
        ax[1].set_ylim(self.params['ylim'])
        ax[1].grid(True)
        ax[1].set_title(f"REV @{self.temperature}")

        ax_twin = ax[1].twinx()
        ax_twin.tick_params(axis='y', colors='darkgreen') # different color for left y axis
        
        # Plot on the same graph the fitted normalized derivative
        ax_twin.scatter(self.fitr.V,self.fitr.norm_dIdV, marker='.', s=5, color='darkgreen')
        ax_twin.set_ylabel(r"i$^{-1}$$\frac{dI}{dV}$ (V$^{-1}$)", color='darkgreen')
        
        # Per il fit sulle -I dI/dV definiamo una sottotabella intorno al massimo valore di I^-1 dI/dV
        # New dataframe _fit with values   
        self.norm_dIdV_fit = pd.DataFrame(
            self.fitr[ self.fitr.norm_dIdV > self.fitr.norm_dIdV.max()*0.5 ].copy(),
        )
        # print(self.norm_dIdV_fit.columns)
        # print(len(self.norm_dIdV_fit))
                    
        # Inoltre, voglio eliminare i valori estremi
        # Prima di tutto, definisco un'ulteriore colonna dove calcolo le differenze rispetto ai valori vicini
        # I am evaluating both the difference with the precedent and the subsequent value
        # at the same time by making the difference between the differences, that gives me
        # a_m -> 2a_n - a_n-1 - a_n+1 with m in range(1,n-1)
        # so I have to append and prepend a value (0)
        # the new dataframe column is only allowed to be created with ['col name']
        
        diff_list = list(np.diff(self.norm_dIdV_fit['norm_dIdV'][:-1]) - np.diff(self.norm_dIdV_fit['norm_dIdV'][1:]))
        
        # There's a problem in matching the index length and the number of values in the list
        # to be honest I just don't know why
        # UPDATE: solved problem by passing to diff a list of values instad of a series: self.norm_dIdV_fit['norm_dIdV']
        diff_list = [0] + diff_list + [0] # WHAT IS THAAAT # BEAUTIFUL
        self.norm_dIdV_fit['diff'] = diff_list
        
        # Poi uso questo parametro per rimuovere i valori troppo diversi dai vicini
        # e ricostruisco il dataframe _fit considerando solo i punti che soddisfano
        # questa condizione
        # I have to use ['diff'] to produce a series, if I was using the reduced
        # notation with the dot I would end up with a list (that wa the initial
        # object with whom I created the dataframe column)
        # Most of the times the difference between the two is null or negligible
        # but when creating columns via external arrays or data this may impact
        # the range of the methods that can be used upon the column
        
        self.norm_dIdV_fit = self.norm_dIdV_fit[self.norm_dIdV_fit['diff'].abs() < 5]
        # CHECK
        # print(self.norm_dIdV_fit.columns)
        # print(len(self.norm_dIdV_fit))
        
        #######################################################################
        # The goal is to fit the points of the normalized derivative that are near its max
        # with a gaussian fit, in order to get the mean value (corresponding to the breakdown voltage)
        # and the standard deviation (corrisponding to the error of the bkg voltage)
        #######################################################################
        
        # Definiamo anche dei limiti ai parametri della gaussiana distorta: A, mean, devst, alpha:
        # - A puo' variare tra il minimo e il massimo delle y
        # - mean tra x.min e max.x
        # - le due (???) devst tra 0 e x.max-x.min
        # - il parametro alpha varia tra -inf e inf
        # - il parametro c varia tra 0 e x.max
            
        fit_bounds = [
            [ # list of minimum values for all parameters
                self.norm_dIdV_fit.norm_dIdV.min()*0.1, # min A
                self.norm_dIdV_fit.V.min(), # min mean
                0, # min dev
                -np.inf, # min alpha
                0, # min c
            ],
            [ # list of maximum values for all parameters
                self.norm_dIdV_fit.norm_dIdV.max(),
                self.norm_dIdV_fit.V.max(),
                self.norm_dIdV_fit.V.max()-self.norm_dIdV_fit.V.min(),
                np.inf,
                self.norm_dIdV_fit.V.max(),
            ]
        ]
                
        # Ora possiamo chiamare la funzione curve_fit del pacchetto optimize di scipy, che fitta i parametri della nostra gaussiana sulle nostre x (V) e y (I^-1 dI/dV)..
        # ..e restituisce i parametri (popt) e la matrice di covarianza (pcov)
        
        popt, pcov = scipy.optimize.curve_fit(skew_gauss,
                                              self.norm_dIdV_fit.V,
                                              self.norm_dIdV_fit.norm_dIdV,
                                              bounds=fit_bounds) # maxfev=1000, p0 = GUESSES
        
        # Disegnamo ora la nostra gaussiana, ottenendo le y dalla funzione gaussiana coi valori di A, mean, e devst ottenuti dal fit
        A, mean, dev, alpha, c = popt[0], popt[1], popt[2], popt[3], popt[4]
        # print("Skew gaussian fit parameters:\n", A, mean, dev, alpha, c, "\n")
        
        # Build the gaussian using all the more x points that you can 
        self.norm_dIdV_fit['gauss'] = skew_gauss(self.fitr.V, A, mean, dev, alpha, c)
        
        
        ax_twin.plot(self.norm_dIdV_fit.V, self.norm_dIdV_fit.gauss, linewidth=1, color='darkorange')
        self.Vbd = [mean, dev]
        
        
        # Infine, come per il plot precedente, rappresentiamo accanto alla curva la media della gaussiana,..
        # ..ovvero la tensione di breakdown
        ax_twin.text(1.3,0.8,
                     r'$V_b=$'+'({:.2f}'.format(self.Vbd[0])+r'$\pm$'+'{:.2f})'.format(self.Vbd[1]),
                     transform=ax[0].transAxes,
                     fontsize=12,
                     color='darkorange')


# --------------- FUNCTIONS ---------------

def read_df_iv(filename):
    """Reads the SiPM IV csv file
    
    Removes the header, finds the column names,
    keeps the (renamed) I and V columns,
    adding the provenance filename columns.

    Argument:
    filename -- complete path to csv file

    Returns:
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
    dx = np.diff(X[:-1]) + np.diff(X[1:])
    dy = np.diff(Y[:-1]) + np.diff(Y[1:])
    return dy/dx

#--------------------------------
# References: 
# https://www.wolframalpha.com/input?i=skew+gaussian+distribution
# https://stackoverflow.com/questions/15400850/scipy-optimize-curve-fit-unable-to-fit-shifted-skewed-gaussian-curve
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skewnorm.html

def skew_gauss(x, A, mean, dev, alpha, c):
    pdf = (1/(dev*np.sqrt(2*math.pi)))*np.exp(-(x-mean)**2/(2*dev**2))
    cdf = sp.erf((-alpha*((x-mean)/dev))/(np.sqrt(2)))
    # not-normalization is obtained by *A
    return A*pdf*cdf+c # not normalized, skewed, shifted gaussian