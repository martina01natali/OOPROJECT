import pandas as pd
import numpy as np
from numpy.polynomial import Polynomial
from matplotlib import pyplot as plt
import time
from tqdm import tqdm

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
          'degree': 4
         }

###############################################################

class iv():
    """Class used for analysis of data from forward and reverse bias SiPM response.
    
    """
    
    # This is the initializer
    # From the init we understand that any instance will have at least some parameters linked to temperature and datafiles 
    def __init__(self, temperature, datafiles=None):
        
        if datafiles is None:
            datafiles = {'FWD': [], 'REV': []}

        # Definition of all the instance's attributes
        self.temperature = temperature
        self.params = params[temperature]
        self.degree = params['degree']
        self.datafiles = datafiles
        
        # Notice that I can define attributes of any type: a class is the definition of a custom type, and can be built on any other type of object
        self.ivf = pd.DataFrame()
        self.ivr = pd.DataFrame()

        # Here I build the dataframe ivf, that is an attribute of the instance; for every acquisition I have a couple of dataframes that contain both the forward and the reversed voltage data
        for datafile in datafiles['FWD']:
            ############# WARNING ###############
            # datafile not defined yet
            #####################################
            tempdf = read_df_iv(datafile)
            self.ivf = pd.concat([self.ivf, tempdf], ignore_index=True)

        for datafile in reversed(datafiles['REV']):
            ############# WARNING ###############
            # there may be something to add or correct here
            #####################################
            
            # reversed() and final break to keep only the last REV file
            # for datafile in datafiles['REV']:
            # final break to keep only the first REV file
            tempdf = read_df_iv(datafile)
            self.ivr = pd.concat([self.ivr, tempdf], ignore_index=True)
            break

    def printRq(self):
        try:
            print(f"Quenching resistance: Rq = {self.Rq[0]} ± {self.Rq[1]}")
        except AttributeError as err:
            print(f"[!] Quenching resistance hasn't been computed yet.\n    Call .fit_iv() first.")

    def __repr__(self):
        return f"temperature: {self.temperature}\n" \
               f"params:      {self.params}\n" \
               f"datafiles:   {self.datafiles}\n\n" \
               f"FWD DF:      {self.ivf.shape[0]} data points in {self.ivf.filename.unique().size} group\n" \
               f"REV DF:      {self.ivr.shape[0]} data points in {self.ivr.filename.unique().size} group\n\n"


    # Metodo della classe che performa effettivamente il fit nel nostro caso (corrente vs versione)
    # Utilizza come attributi il DataFrame dei dati, il valore di soglia dopo il quale fittare (dal dizionario)..
    # ..e il tipo di fit (sempre dal dizionario)

    def fit_ivf(self):
        # subsetting the dataframe:
        self.fitf = self.ivf[ self.ivf.V > self.params['threshold'] ]

        fit_par, fit_extra = Polynomial.fit(self.fitf.V, self.fitf.I, deg = 1, full=True) # linear fit (polynomial deg=1)
        self.fitf = self.fitf.assign( I = lambda x: Polynomial(fit_par.convert().coef)(x.V) )

        # print(fit_par)
        # print(fit_extra)

        self.Rq = [ 1/fit_par.convert().coef[1] ]     # quenching resistance
        self.Rq.append( fit_extra[0][0] )       # delta_Rq (residuals)

    def fit_ivr(self):
        # calculating the normalized derivative from data points
        self.ivr = self.ivr.assign( norm_dIdV = lambda x: (1/x['I'][1:-1])*derivative(x.V,x.I) )
        # subsetting the dataframe:
        self.fitr = self.ivr[ ( self.ivr.V >= self.params['rev_limits'][0] ) & ( self.ivr.V <= self.params['rev_limits'][1] ) ]
        
        fit_par, fit_extra = Polynomial.fit(self.fitr.V, self.fitr.norm_dIdV, deg = self.degree, full=True) # polynomial fit (polynomial deg=4)
        self.fitr = self.fitr.assign( norm_dIdV = lambda x: Polynomial(fit_par.convert().coef)(x.V) ) # replace calculated data points with fitted data points

        self.Vbd = [np.nan,np.nan]
        # self.Vbd = 


    def fit_iv(self):
        self.fit_ivf()
        self.fit_ivr()


        # A questo punto, abbiamo assegnato come attributi della classe le x e y del fit..
        # ..e la resistenza di quenching, che stampiamo sul terminale
        # print('Quenching resistance = {:.2f} ohm'.format(self.quenching_resistance))


    # Metodo della classe per creare e mostrare i plot ( e fit) sullo schermo
    # Utilizza come attributi i due DataFrame, le x e y della funzione di fit..
    # ..e gli intervalli di x e y per il plot in rev
    def plot_iv(self, temperature, ax):
        self.plot_ivf(temperature, ax)
        self.plot_ivr(temperature, ax)

    def plot_ivf(self,temperature,ax):
        # Il primo elemento della lista ax corrisponde al plot in fwd
        # Creiamo lo scatter plot, con corrente sulle y, tensione sulle x, e dimezione dei punti 5
        ax[0].scatter(self.ivf.V,self.ivf.I, marker='.', s=5)
        # Creiamo anche un testo, che posizioniamo in alto a sx (coordinate relative) con la resistenza di quenching
        ax[0].text(0.1,0.8,r'$R_q=$'+'{:.2f}'.format(self.Rq[0]), transform=ax[0].transAxes,fontsize=12, color='darkred')
        # Nominiamo gli assi
        ax[0].set_ylabel("Current (A)")
        ax[0].set_xlabel("Voltage (V)")
        # Aggiungiamo la funzione del fit, usando plot
        ax[0].plot(self.fitf.V, self.fitf.I, color='darkred')
        # Aggiungiamo la griglia per facilitare la lettura del plot e un titolo
        ax[0].grid(True)
        ax[0].set_title(f"FWD @{self.temperature}")


    def plot_ivr(self,temperature,ax):
        # Il secondo elemento della lista ax corrisponde al plot in rev
        # Settiamo prima la scala logaritmica..
        ax[1].set_yscale("log")
        # ..poi creiamo lo scatter plot, con corrente sulle y, tensione sulle x, e dimezione dei punti 5
        ax[1].scatter(self.ivr.V,self.ivr.I, marker='.', s=5)
        # Nominiamo  gli assi e settiamo gli intervalli presi dai nostri parametri
        ax[1].set_ylabel("Current (A)")
        ax[1].set_xlabel("Voltage (V)")
        ax[1].set_xlim(self.params['xlim'])
        ax[1].set_ylim(self.params['ylim'])
        # Aggiungiamo la griglia per facilitare la lettura del plot e un titolo
        ax[1].grid(True)
        ax[1].set_title(f"REV @{self.temperature}")

        # Sullo stesso grafico, vogliamo anche plottare I^-1 dI/dV, che creiamo utilizzando la helper function di derivazione
        # self.table_sipm_rev['Sella'] = (1./self.table_sipm_rev["Reading"][1:-1]) \
                # * derivative(self.table_sipm_rev["Value"],self.table_sipm_rev["Reading"])
        # pre farlo, creiamo un gemello dell'axis (vogliamo i plot sovrapposti)..
        ax_twin = ax[1].twinx()
        # ..settiamo il colore dell'asse y di sinistra..
        ax_twin.tick_params(axis='y', colors='darkgreen')
        # ..e creiamo lo scatter plot dello stesso colore
        ax_twin.scatter(self.fitr.V,self.fitr.norm_dIdV, marker='.', s=5, color='darkgreen')
        # Finiamo assegnando anche al suo asse y un nome (usando formula matematica in LaTex)
        ax_twin.set_ylabel(r"i$^{-1}$$\frac{dI}{dV}$ (V$^{-1}$)", color='darkgreen')

        # Per il fit sulle -I dI/dV definiamo una sottotabella intorno al massimo valore di I^-1 dI/dV
        # self.table_sipm_rev_fit = self.table_sipm_rev[ self.table_sipm_rev['Sella'] > self.table_sipm_rev['Sella'].max()*0.2 ].copy()
        # Inoltre, voglio eliminare i valori estremi
        # Prima di tutto, definisco un'ulteriore colonna dove calcolo le differenze rispetto ai valori vicini
        # diff_list = list(np.diff(self.table_sipm_rev_fit['Sella'][:-1]) - np.diff(self.table_sipm_rev_fit['Sella'][1:]))
        # diff_list = [0] + diff_list + [0]
        # self.table_sipm_rev_fit['diff'] = diff_list
        # # Poi uso questo parametro per rimuovere i valori troppo diversi dai vicini
        # self.table_sipm_rev_fit = self.table_sipm_rev_fit[self.table_sipm_rev_fit['diff'].abs() < 5]

        # Definiamo anche dei limiti ai parametri della gaussiana distorta: A, mean, devst, alpha:
        # - A puo' variare tra il minimo e il massimo delle y
        # - mean tra il minimo e il massimo delle x
        # - le due devst tra 0 e la differenza tra il minimo e il massimo delle x
        # - il parametro alpha varia tra -inf e inf
        # fit_bounds = [ [ self.table_sipm_rev_fit['Sella'].min()*0.1,self.table_sipm_rev_fit['Value'].min() ,0,-np.inf ],\
                    # [ self.table_sipm_rev_fit['Sella'].max(), self.table_sipm_rev_fit['Value'].max() , self.table_sipm_rev_fit['Value'].max()-self.table_sipm_rev_fit['Value'].min(), np.inf] ]
        # Ora possiamo chiamare la funzione curve_fit del pacchetto optimize di scipy, che fitta i parametri della nostra gaussiana sulle nostre x (V) e y (I^-1 dI/dV)..
        # ..e restituisce i parametri (popt) e la matrice di covarianza (pcov)
        # popt, pcov = optimize.curve_fit(skew_gauss, self.table_sipm_rev_fit["Value"], self.table_sipm_rev_fit['Sella'], maxfev=1000, bounds=fit_bounds)
        # Disegnamo ora la nostra gaussiana, ottenendo le y dalla funzione gaussiana coi valori di A, mean, e devst ottenuti dal fit
        ax_twin.plot(self.fitr.V, self.fitr.norm_dIdV, linewidth=1, color='darkorange')
        # Infine, come per il plot precedente, rappresentiamo accanto alla curva la media della gaussiana,..
        # ..ovvero la tensione di breakdown
        ax_twin.text(1.5,0.8,r'$V_b=$'+'{:.2f} V'.format(self.Vbd[0]),\
                    transform=ax[0].transAxes,fontsize=12, color='darkorange')


# --------------- FUNCTIONS ---------------

def read_df_iv(filename):
    """
    Reads the SiPM IV csv file
    removing the header, finding the column names,
    keeping the (renamed) I and V columns,
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

def derivative(X, Y):
    dx = np.diff(X[:-1]) + np.diff(X[1:])
    dy = np.diff(Y[:-1]) + np.diff(Y[1:])
    return dy/dx
