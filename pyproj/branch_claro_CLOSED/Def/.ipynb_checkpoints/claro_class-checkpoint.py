import os
import re
import csv
import time
import math
import fnmatch
import warnings
import numpy as np
import pandas as pd
import matplotlib as mplt
import matplotlib.pyplot as plt
import scipy.stats as ss
from scipy import special as sp
from scipy.optimize import curve_fit
from matplotlib.ticker import MaxNLocator

###############################################################################
#                                Single class                                 #
###############################################################################

class Single():
    
    def __init__(self, fileinfo:dict):
        self.path = fileinfo['path']
        self.read_data()
        self._meta = {
            'path' : self.path,
            'amplitude' : self.amplitude,
            'transition' : self.transition,
            'width' : self.width
        }
        self.fit_guess = [
            self.amplitude,
            self.transition,
            self.amplitude/2
        ]
        self.fileinfo = fileinfo
    
    def __repr__(self):
        for key, value in self._meta.items():
            print("{:<25} {:<25}".format(key,value))
        return  f"x data: {self.x}\n" \
                f"y data: {self.y}\n" \
                f"fit_guess: {self.fit_guess}"
    
    def read_data(self):
        data = pd.read_csv(self.path, sep='\t', header=None, skiprows=None)
        self.x = data.iloc[2:,0].to_numpy()
        self.y = data.iloc[2:,1].to_numpy()
        self.amplitude = data.iloc[0,0]
        self.transition = data.iloc[0,1]
        self.width = -data.iloc[0,2]
        
    #-------------------------------------------------------------------------#
    
    def fit_erf(self, guesses:list='default',
                interactive=True, log=False, warnings_ignore=True,
                npoints=1000):
        """Fit the provided x,y data with a modified erf function.
    
        If interactive==True prints message to tell the user if the fitting procedure converged.
        If interactive==False, tells nothing. In any case returns a dict with the fit parameters
        and a code that can be 'good' or 'bad' depending on the result of the fit.
        The code is used by function plot_fit, for example, to determine whether or not to
        produce the plot of the fit.
        If log==True produces a file log_unfit with paths to the good files whose data
        couldn't be fitted.
        If warnings_ignore==True doesn't print any warning but mantains the log. 
        
        Return
        ------
        - dict with parameters of the fit and metadata 'code'= ['good' or 'bad']
        
        """
        
        x = self.x
        y = self.y
        meta = self._meta
        
        # Default dict of fit parameters
        self.fit_params = {
                'params' : None,
                'errors' : None,
                'code' : 'bad',
        }
        
        try:
            if warnings_ignore==True:
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("ignore")
                    
            if guesses=='default':
                guesses=self.fit_guess
            
            bad_list = []            
            fit_params, fit_covar = curve_fit(Claro.func, x, y, p0=guesses)
            fit_dev = np.sqrt(np.diag(fit_covar))
            all_params = np.append(fit_params, fit_dev)
            
            # Warnings catch
            if w:
                if log==True: bad_list.append(meta['path'])
            
            for i in all_params:
                if i == np.inf:
                    raise ValueError(f'Fit returned an inf parameter. Please try with different guesses.')
                elif i < 1e-6:
                    raise ValueError(f'Fit returned a parameter that is < 1e-6 or negative. Please try with different set of guesses.')
            if interactive==True: print("Fit ok!")
                    
        except ValueError as err:
            if log==True: bad_list.append(meta['path'])
            if interactive==True: print(f'Error: {err}.\nThe fit parameters are not returned.')
                
        except RuntimeError as err:
            if log==True: bad_list.append(meta['path'])
            if interactive==True: print(err)
        
        else: 
            self.fit_params = {
                'params' : [fit_params[i] for i in range(len(fit_params))],
                'errors' : [fit_dev[i] for i in range(len(fit_dev))],
                'code' : 'good'
            }
            # self.fit_params = {
            #     'amplitude' : [fit_params[0], fit_dev[0]],
            #     'transition_x' : [fit_params[1], fit_dev[1]],
            #     'transition_y' : [fit_params[2], fit_dev[2]],
            #     'code' : 'good'
            # }
        
        finally:
            if log==True:
                with open("log_unfit.txt", "a") as output:
                    if bad_list: output.write(bad_list[0]+"\n")
            
    #-------------------------------------------------------------------------#
            
    def plot(self, npoints=1000,
             interactive=False, log=True,
             show_scatter=True, show_fit=True, show_transition=True,
             save=False, save_path='.\plot', save_format='pdf', show=True,
             **kwargs):
        """Scatterplot of data, with options to plot both the erf fit and transition point."""
        
        x = self.x
        y = self.y
        metafit = self.fit_params
        fileinfo = self.fileinfo
        func = Claro.func
        
        title = f"Fit CLARO: station {fileinfo['station']}, chip {fileinfo['chip']}, ch {fileinfo['ch']}"
        
        font = {
        'fontsize': plt.rcParams['axes.titlesize'],
        'fontweight' : plt.rcParams['axes.titleweight'],
        'verticalalignment': 'baseline',
        }
        
        # When printing on a multipage pdf, don't initialize any figure
        # plt.figure(figsize=(5,5), tight_layout=True)
        
        plt.title(title, fontdict=font)
        
        # Show scatterplot of data (default = True)
        if show_scatter == True:
            plt.scatter(x, y, label='Data points', zorder=2)
            plt.annotate(f"From data file\nTransition = {fileinfo['transition']:.2f}\n"
                         +f"Width = {fileinfo['width']:.2f}",
                         xy=(0.025, .975), xycoords='axes fraction',
                         verticalalignment='top', color='gray', alpha=0.8)
            plt.xlabel('x [arb units]', fontdict=font)
            plt.ylabel('y [arb units]', fontdict=font)
        
        try:
            if metafit['code']=='bad':
                if log==True:
                    with open("log_unplot.txt", "a") as output:
                        output.write(fileinfo['path']+"\n")
                raise ValueError("Error: the provided fit has invalid parameters. "
                                 +f"Plot {title} will not be plotted. Unfitted files' paths in log_unplot.txt\r")
        
            # Show plot of fit (default = True)
            if show_fit == True:
                
                # x,y data computed as a grid of npoints and using parameters of the fit
                fit_params = metafit['params']
                fit_errs = metafit['errors']
                xfit = np.linspace(x.min(), x.max(), npoints)
                yfit= func(xfit, *fit_params)
                
                plt.plot(xfit, yfit, label='erf fit', zorder=1, color='r', alpha=0.8)
                plt.annotate(f"Fit parameters\nAmplitude = ({fit_params[0]:.2f}"\
                             +r" $\pm$ "+f"{fit_errs[0]:.2f})\n"\
                             +f"Transition = ({fit_params[1]:.2f}"+r" $\pm$ "\
                             +f"{fit_errs[1]:.2e})\n"\
                             +f"Width = ({fit_params[2]*2:.2f}"+r" $\pm$ "+f"{fit_errs[2]*2:.2E})",
                             xy=(0.025, .3), xycoords='axes fraction', verticalalignment='top',
                             color='r', alpha=0.8,
                             bbox=dict(boxstyle="square", fc="white", ec="black", lw=1, alpha=0.8))
                
            # Show transition point
            if show_transition == True:
                xtrans = fit_params[1]
                ytrans = func(xtrans, *fit_params)
                plt.scatter(xtrans, ytrans, s=100, c='darkred', marker='*',
                            zorder=2, label='Transition point')
                plt.vlines(x=xtrans, ymin=y[0], ymax=y[-1], linestyles='dashed',
                            alpha=0.5, zorder=1)
                plt.hlines(y=ytrans, xmin=x[0], xmax=x[-1], linestyles='dashed',
                            alpha=0.5, zorder=1)
                plt.annotate(f"Transition = {fit_params[1]:.2f}\nWidth = {fit_params[2]*2:.2f}", 
                             xy=(0.025, .6), xycoords='axes fraction', verticalalignment='top',)
    
        except ValueError as err: 
            if interactive==True: print(err)
        
        if save == True:
            plt.show()
            plt.savefig(save_path+'.'+save_format)
            plt.close()
        if show == True:
            plt.show()
            plt.close()
        else:
            plt.close()
    
###############################################################################
#                                Claro class                                  #
###############################################################################

class Claro():
    
    # def __init__():
    # def __repr__():
    # def get_fileinfo():
    # def find_fileinfo():

    # def hist_tw():
    # 
    # @staticmethod
    # def func():
    # @staticmethod
    # def skew_gaus():
    # @staticmethod
    # def gaus():
        
    #-------------------------------------------------------------------------#
    
    PARAMS = {
        "DIRPATH"  : "*Station_1__*\Station_1__??_Summary\Chip_???\S_curve",
        "FILEPATH" : "Ch_*_offset_*_Chip_*.txt",
        "OUTFILE"  : "claro_files.txt",
        "OUTBAD"   : "bad_files.txt",
    }
    
    def __init__(self, TDIR, params:dict=PARAMS, custom_n_files='all', log:bool=True):
        
        # User options
        self.custom_n_files = custom_n_files
        self.logoption = log
        
        # Attributes
        self._tdir = TDIR
        self._params = params
        self.fileinfos = dict()
        self.good_files = []
        self.bad_files = []
        self.meta = dict()
        
        self.tlist = []
        self.wlist = []
        self.fit_tlist = []
        self.fit_wlist = []
        
    def __repr__(self):
        return  f"top dir:   {self._tdir}\n" \
                f"params:    {self._params}\n" \
                f"meta:      {self.meta}\n"
    
    
    @property
    def tdir(self):
        return self._tdir
    @tdir.setter
    def tdir(self, value):
        self._tdir = value
    
    def get_fileinfos(self):
        """Function that walks on all subdirectories of TDIR that match DIRPATH and FILEPATH.
            
        Has an interactive interface for the user and returns a dict containing the following keys: path, station, sub, chip, ch, offset, amplitude, transition, width.
        """
        
        # Returns processing time as well.
        start_time = time.time()
        
        TDIR = self._tdir
        OUTFILE = self._params['OUTFILE']
        OUTBAD  = self._params['OUTBAD']
        custom_n_files=self.custom_n_files
        log=self.logoption
        
        if isinstance(TDIR, str)==False:
            raise NameError('Please provide a string with delimiter: double backslash (\\\) as top directory path.')
    
        enter = input(f'The default subfolders\' paths are {self._params["DIRPATH"]}.\n'
                        +f'The default file names are {self._params["FILEPATH"]}.\n'
                        +f'To confirm, press Enter. Press any other key to change the paths.\n')
        if enter != '':
            self._params['DIRPATH']  = input('Please provide subfolders\' paths. You may use wildcards.\n')
            self._params['FILEPATH'] = input('Please provide file names. You may use wildcards.\n')
        
        for file in [OUTFILE, OUTBAD]:
            if log==True and os.path.isfile(file): os.remove(file)
        
        DIRPATH=self._params['DIRPATH']
        FILEPATH=self._params['FILEPATH']
        fileinfos = dict()
        tot_counts  = 0
        good_counts = 0
        
        for root, dirs, files in os.walk(TDIR):
            if fnmatch.fnmatch(root, TDIR + DIRPATH):
                for f in files:
                    if custom_n_files!='all':
                        if tot_counts>(custom_n_files-1): break
                    if fnmatch.fnmatch(f, FILEPATH):
                        tot_counts += 1
                        print(f'Processing file n. {tot_counts}...', end='\r')
                        thisfile = os.path.join(root,f)
                        with open(thisfile) as csvfile:
                            # print(f'Reading {thisfile}', end='\r')
                            lines = csvfile.readlines()
                            firstline = lines[0].split()
                            try:
                                if isinstance(float(firstline[2]), float):
                                    temp = re.findall("[0-9]+", thisfile)
                                    self.fileinfos[thisfile] = {
                                            'path' : thisfile,
                                            'station': temp[0],
                                            'sub': temp[2],
                                            'chip': temp[5],
                                            'ch': temp[6],
                                            'offset': temp[7],
                                            'amplitude': float(firstline[0]),
                                            'transition': float(firstline[1]),
                                            'width': float(firstline[2]),
                                            }
                                    good_counts += 1
                                    self.good_files.append(thisfile)
                                    self.tlist.append(self.fileinfos[thisfile]['transition'])
                                    self.wlist.append(self.fileinfos[thisfile]['width'])
                                if log==True:
                                    with open(OUTFILE, "a") as output:
                                        output.write(thisfile+"\n")
                            except (ValueError, IndexError):
                                print(f"Error: Couldn't read data in: {thisfile}. "
                                +f"First word: {firstline[0]}. Going on...", end='\r')
                                self.bad_files.append(thisfile)
                                if log==True:
                                    with open(OUTBAD, "a") as output:
                                        output.write(thisfile+"\n")
                                pass
        
        bad_counts = tot_counts-good_counts
        print("\n\nProcess completed in %s s." % (format(time.time()-start_time,".2f")))
        print(f"\nTotal number of files found: {tot_counts}.")
        print(f"Total number of good files: {good_counts}. Output paths to good files are stored in {OUTFILE}")
        print("Total number of bad files: {0[0]} ({0[1]:.1%}) out of total). Output paths to bad files are stored in {0[2]}".format([bad_counts, bad_counts/tot_counts, OUTBAD]))
        
        self.meta = {
            'nfiles' : tot_counts,
            'ngood' : good_counts,
            'nbad' : bad_counts
        }
        
    ###########################################################################
    @staticmethod
    def find_fileinfos(fileinfos, path:str=None, chip:str='001', ch:str='0', station:str='1', sub:str='11',) -> dict():
        """Returns metadata of file with given chip, ch, station and sub"""
        for entry in fileinfos.items():
            i = entry[1]
            if path is None:
                if i['station']==station and i['sub']==sub and i['chip']==chip and i['ch']==ch:
                    return i
                    break
            else:
                if i['path']==path:
                    return i
                    break
        raise NameError('No matching file found in provided dict.')
        
    ###########################################################################
    
    # def make_child --> implement inheritance
    # def plot_single():
    # """Plot all the files you've walked through, making them Single objects, in a loop"""
    # --> produce fit_tlist and fit_wlist and logs unfitted and unplotted
    # --> build histograms of differences between file and plot
    
    def plot_loop(self, plot=True, **kwargs):
        """Analyze and plot the whole dataset exloiting Single objects.
        1. loop over all files stored in self.fileinfos
        2. produce a Single object for each
        3. fit and plot the Single object
        Accepts **kwargs as dict with parameters passed to Single.plot().
        """
        for fileinfo in self.fileinfos.values():
            single = Single(fileinfo)
            single.fit_erf()
            ################### TO UPDATE/FINISH #########################
            # if plot==True: single.plot(**kwargs)
            # self.fit_tlist.append(single.fit_params['params'][1]) # amplitude, transx, width
            # self.fit_wlist.append(single.fit_params['params'][2])
            ############ what about the errors on trans and width? an error barplot? #############        
    
    ###########################################################################
    
    def plot_MultiPage(self, log=False, save=False, save_path = 'aHundredPlots.pdf'):
    # Loop on the files and print plots on multi-page pdf

    # custom_n_files = 100     # This is used to break the printing of plots: comment the line
                            # or assign to 'all' to plot all the files

    # Histograms of transition points and widths
    tw_hist = True # Choose True or False for plotting, showing and saving
    t_list = []
    w_list = []
    
    with PdfPages(save_path) as pdf:
        per_page = 0
        while not per_page:
            per_page = int(input("How many plots do you want per page? Allowed values are 1,2,3,4,6. "))
            if per_page==1: nrows, ncols = 1, 1
            elif per_page==2: nrows, ncols = 2, 1
            elif per_page==3: nrows, ncols = 3, 1
            elif per_page==4: nrows, ncols = 2, 2
            elif per_page==6: nrows, ncols = 3, 2
            # else: raise NameError("Please run again and choose one of the allowed number of subplots.")
        
        for n, file in enumerate(a.values()): # file is the sub-dict, access keys via file['key']
    
            # Preprocessing
            print(f"Reading file n. {n}...", end='\r')
            x,y,meta = read_data(file['path'])
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                metafit = fit_erf(x,y,meta, interactive=False, log=log_choice)
    
            meta['fit_dict'] = metafit
            
            # Building lists of transition points and widths
            t_list.append(meta['transition'])
            w_list.append(meta['width'])
            
            # Plotting and saving on multipage pdf
            if isinstance(custom_n_files,int):
                if n>=custom_n_files: continue
            index = n%per_page+1
            if index==1:
                fig=plt.figure(figsize=(10,15)) 
            fig.add_subplot(nrows,ncols,index)
            plot_fit(x, y, metafit, fileinfo=file, show=True, save=False, log=log_choice)
            if index==per_page or n==len(a.values())-1:
                if save_choice: pdf.savefig(fig)
                plt.close(fig)
        plt.close()
    
    ###########################################################################
    
    def hist_tw(t_list, w_list, ax):
        
        annotation_kwargs = {'xy':(.1,.7), 'xycoords':'axes fraction',
                             'bbox':dict(boxstyle="round",edgecolor="black",facecolor="white",alpha=.8)}
        
        #-----------------------------------------   
        
        # Transition histogram
        ax[0].set_title("Transition points' histogram", fontsize=12)
        ax[0].tick_params(axis='y', which='minor', width=0)
        ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))
        counts, bins, pads = ax[0].hist(t_list, bins=int(np.sqrt(len(t_list))/4), density=False,
                                    label='Transition points (x)', alpha=.5,
                                    log=False, rwidth=1)
        
        fit_bounds = [ [0,0,0], [sum(counts)*np.diff(bins)[0],max(bins),max(bins)] ]
        popt, pcov = curve_fit(Claro.gauss, bins[:-1], counts, bounds=fit_bounds, maxfev=1000)
        pdev = np.sqrt(np.diag(pcov))
        A, mean, dev = popt[0], popt[1], popt[2]
        x = np.linspace(min(t_list), max(t_list), 1000)
        fit = Claro.gauss(x, A, mean, dev)
        ax[0].plot(x, fit, c='red')
        
        ax[0].annotate(f"N entries: {len(t_list)}\n"\
                       +"Fit type: gauss"\
                       +"\nMean: ({:.1e}".format(popt[1])+r'$\pm$'+'{:.1e})'.format(pdev[1])\
                       +"\nDev: ({:.1e}".format(popt[2])+r'$\pm$'+'{:.1e})'.format(pdev[2]),
                       **annotation_kwargs)
        
        #-----------------------------------------   
        
        # Widths' histogram
        ax[1].set_title("Widths' histogram", fontsize=12)
        ax[1].tick_params(axis='y', which='minor', width=0)
        ax[1].yaxis.set_major_locator(MaxNLocator(integer=True))
        counts, bins, pads = ax[1].hist(w_list, bins=int(np.sqrt(len(w_list))/4), density=False,
                                label='Transition points (x)', alpha=.5,
                                log=False, rwidth=1)
        
        fit_bounds = [ [0,0,0,0] , [sum(counts)*np.diff(bins)[0],max(bins),max(bins),np.inf] ]
        popt, pcov = curve_fit(Claro.skew_gauss, bins[:-1], counts, bounds=fit_bounds, maxfev=1000)
        pdev = np.sqrt(np.diag(pcov))
        A, mean, dev, alpha = popt[0], popt[1], popt[2], popt[3]
        x = np.linspace(min(w_list), max(w_list), 1000)
        fit = Claro.skew_gauss(x, A, mean, dev, alpha)
        ax[1].plot(x, fit, c='red')
        
        ax[1].annotate(f"N entries: {len(w_list)}\n"\
                       +"Fit type: skew gauss"\
                       +"\nMean: ({:.1e}".format(popt[1])+r'$\pm$'+'{:.1e})'.format(pdev[1])\
                       +"\nDev: ({:.1e}".format(popt[2])+r'$\pm$'+'{:.1e})'.format(pdev[2]),
                       **annotation_kwargs)
    
    ###########################################################################
    @staticmethod
    def func(x, ampl, a, b):
        """Modified erf function.
        
        Amplitude ampl and shift on the vertical axis ampl/2,
        inflection point at a, normalization proportional to b.
        Deafult guesses are [AMPLITUDE, TRANSITION, AMPLITUDE/2].
        """
        
        return ampl/2*(1+sp.erf((x-a)/(b*np.sqrt(2))))
    
    ###########################################################################
    @staticmethod
    def skew_gauss(x, A, mean, dev, alpha,):
        """Skew, not-normalized and shifted gaussian distribution.
    
        References:
        - https://www.wolframalpha.com/input?i=skew+gaussian+distribution
        - https://stackoverflow.com/questions/15400850/scipy-optimize-curve-fit-unable-to-fit-shifted-skewed-gaussian-curve
        - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skewnorm.html
    
        """
        
        import math
        import scipy.special as sp
        
        pdf = (1/(dev*np.sqrt(2*np.pi)))*np.exp(-pow((x-mean),2)/(2*pow(dev,2)))
        cdf = sp.erfc((-alpha*(x-mean))/(dev*np.sqrt(2)))
        return A*pdf*cdf
    
    ###########################################################################
    @staticmethod
    def gauss(x, A, mean, dev):
        """Not-normalized, shifted gaussian distribution."""
        
        import math
        
        pdf = (1/(dev*np.sqrt(2*math.pi)))*np.exp(-(x-mean)**2/(2*dev**2))
        return A*pdf