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
from matplotlib.backends.backend_pdf import PdfPages

###############################################################################
#                                Single class                                 #
###############################################################################

class Single():
    """Class for analysis of a single amplifier.
    This class is not a child class of Claro but it encapsulates some
    methods from it, so they must go together.
    If you're working with a single file instead of a dictionary from
    Claro object, you can create a Single object by providing a dict
    with the path only:
    
    fileinfo:dict = {
     'path': 'example.txt',
    }
    Notice that with this construction the property self.fileinfos will
    have its default values, which are all the necessary keys and empty
    strings for string values, and None values for arithmetic values.
    """
    
    FILEINFO = {
        'path' : '',
        'station': '',
        'sub': '',
        'chip':'',
        'ch':'',
        'offset':'',
        'amplitude': None,
        'transition': None,
        'width': None,
    }
    
    def __init__(self, fileinfo:dict=FILEINFO):
        self.fileinfo   = fileinfo
        self.path       = fileinfo['path']
        data = pd.read_csv(self.path, sep='\t', header=None, skiprows=None)
        self.x          = data.iloc[2:,0].to_numpy()
        self.y          = data.iloc[2:,1].to_numpy()
        self.amplitude  = data.iloc[0,0]
        self.transition = data.iloc[0,1]
        self.width      = -data.iloc[0,2]
        self._meta      = { 'path' : self.path, 'amplitude' : self.amplitude, 
                           'transition' : self.transition, 'width' : self.width }
        self.fit_params = { 'a' : None, 't' : None, 'w' : None, 'code' : '', }
        self.fit_guess  = [ self.amplitude, self.transition, self.width ]
    
    def __repr__(self):
        for key, value in self._meta.items():
            print("{:<25} {:<25}".format(key,value))
        return  f"x data: {self.x}\n" \
                f"y data: {self.y}\n" \
                f"fit_params : {self.fit_params}\n" \
                f"fit_guess: {self.fit_guess}\n"
    
    ###########################################################################    
    
    def fit_erf(self, guesses:list='default', interactive=True):
        """Fit the provided x,y data with a modified erf function.
    
        If interactive==True prints message to tell the user if the fitting procedure converged.
        If interactive==False, tells nothing. In any case returns a dict with the fit parameters
        and a code that can be 'good' or 'bad' depending on the result of the fit.
        The code is used by function plot_fit, for example, to determine whether or not to
        produce the plot of the fit.
        If log==True produces a file log_unfit with paths to the good files whose data
        couldn't be fitted.
        
        Return
        ------
        - dict with parameters of the fit and metadata 'code'= ['good' or 'bad']
        
        """
        
        x = self.x
        y = self.y
        meta = self._meta
        
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("ignore")
                    
                if guesses=='default':
                    guesses=self.fit_guess
                
                fit_params, fit_covar = curve_fit(Claro.func, x, y, p0=guesses)
                fit_dev = np.sqrt(np.diag(fit_covar))
                all_params = np.append(fit_params, fit_dev)
                
                # Warnings catch
                if w: meta['code'] = 'warning'
                
                for i in all_params:
                    if i == np.inf:
                        meta['code'] = 'inf'
                        raise ValueError(f'Fit returned an inf parameter. Please try with different guesses.')
                    elif i < 1e-6:
                        meta['code'] = 'zero'
                        raise ValueError(f'Fit returned a parameter that is < 1e-6 or negative. Please try with different set of guesses.')
                if interactive==True: print("Fit ok!")
                    
        except (ValueError,RuntimeError) as err:
            meta['code'] = 'error'
            if interactive==True: print(f'Error: {err}.\nThe fit parameters are not returned.')
        
        else: 
            self.fit_params = {
                'a' : [fit_params[0], fit_dev[0]],
                't' : [fit_params[1], fit_dev[1]],
                'w' : [fit_params[2], fit_dev[2]],
                'code' : 'good'
            }
            
    ###########################################################################
            
    def plot(self, npoints=1000,
             interactive=False,
             show_scatter=True, show_fit=True, show_transition=True,
             save=False, save_dir=".\\", save_format="pdf"):
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
            if metafit['code']!='good':
                raise ValueError("Error: the provided fit has invalid parameters. "
                                 +f"Plot {title} will not be plotted.\r")
        
            # Show plot of fit (default = True)
            if show_fit == True:
                
                # x,y data computed as a grid of npoints and using parameters of the fit
                fit_params = [metafit['a'][0], metafit['t'][0], metafit['w'][0]]
                fit_errs = [metafit['a'][1], metafit['t'][1], metafit['w'][1]]
                xfit = np.linspace(x.min(), x.max(), npoints)
                yfit= func(xfit, *fit_params)
                
                plt.plot(xfit, yfit, label='erf fit', zorder=1, color='r', alpha=0.8)
                plt.annotate(f"Fit parameters\nAmplitude = ({fit_params[0]:.2f}"\
                             +r" $\pm$ "+f"{fit_errs[0]:.2f})\n"\
                             +f"Transition = ({fit_params[1]:.2f}"+r" $\pm$ "\
                             +f"{fit_errs[1]:.2e})\n"\
                             +f"Width = ({fit_params[2]:.2f}"+r" $\pm$ "+f"{fit_errs[2]:.2e})",
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
                plt.annotate(f"Transition = {fit_params[1]:.2f}\nWidth = {fit_params[2]:.2f}", 
                             xy=(0.025, .6), xycoords='axes fraction', verticalalignment='top',)
    
        except ValueError as err: 
            if interactive==True: print(err)
        
        if save == True:
            if not os.path.exists(save_dir): os.mkdir(save_dir)
            plt.savefig(save_dir\
                        +f"St-{fileinfo['station']}_chip-{fileinfo['chip']}_c-{fileinfo['ch']}."\
                        +save_format)
            
            
###############################################################################
#                                Claro class                                  #
###############################################################################

class Claro():
    """Class dedicated to analysis of the whole batch of files in secondolotto_1.
    
    The class provides a function (.get_fileinfos()) to walk over a provided
    top directory and find all the files that match a given directory path
    and filename. The function must be called outside of the initializer.
    Other ethods provided for analysis:
    - print_log: prints the lists of readable files, unreadable files and,
    if analysis_loop() has already been called, can print the log of
    unfittable files;
    - [@staticmethod] find_fileinfos: returns the dict with the metadata
    of a single file, provided the path of the latter or the station, chip,
    ch and offset values;
    - analysis_loop: analyzes all readable files found by get_fileinfos that
    contain "good" data and fits each of them with a modified erf function;
    this function exploits the Single.fit_erf() function to fit;
    - plot_loop: loops on all good and fittable files that are found and
    exploits the Single.plot() function to plot them;
    - plot_MultiPage: does the same as plot_loop, but stores the plots in
    a multi-page pdf, with a number of plots per page that is user-defined;
    - hist_tw: plots the histograms ot transition and widths values, and
    provides an option to choose the source of those values: allowed sources
    are the raw data, the fitted data or the difference between the two.
    - [@staticmethod] func, skew_gauss, gauss are mathematical support
    functions for fitting and represent a modified erf function and the
    pdfs of a skewed, not-normalized gaussian and a not-normalized gaussian.  
    """
    
    PARAMS = {
        "DIRPATH"  : "*Station_1__*\Station_1__??_Summary\Chip_???\S_curve",
        "FILEPATH" : "Ch_*_offset_*_Chip_*.txt",
        "OUTFILE"  : "claro_files.txt",
        "OUTBAD"   : "bad_files.txt",
        "UNFIT"    : "unfit_files.txt",
    }
    
    def __init__(self, TDIR, params:dict=PARAMS, custom_n_files='all'):
        
        # User options
        self.custom_n_files = custom_n_files
        self.logoption = True
        
        # Attributes
        self._tdir = TDIR # has @property and @.setter methods
        self._params = params
        
        # from get_fileinfos()
        self.fileinfos = { 'path' : {'path' : None,
                                     'station': None,
                                     'sub': None,
                                     'chip':None,
                                     'ch':None,
                                     'offset':None,
                                     'amplitude': None,
                                     'transition': None,
                                     'width': None, }
                         }
        self.good_files, self.bad_files = [], []
        self.meta = { 'nfiles' : None, 'ngood' : None, 'nbad' : None, }
        self.tlist, self.wlist = [], []
        
        # from analysis_loop
        self.fit_tlist, self.fit_wlist = [], []
        self.fit_tdiff, self.fit_wdiff = [], []
        self.unfit_files = []
        
    #-------------------------------------------------------------------------#
        
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
    
    ###########################################################################
    
    def get_fileinfos(self):
        """Function that walks on all subdirectories of TDIR that match DIRPATH and FILEPATH.
            
        Has an interactive interface for the user and returns a dict containing the following
        keys: path, station, sub, chip, ch, offset, amplitude, transition, width.
        """
        
        # Returns processing time as well.
        start_time = time.time()
        
        TDIR = self._tdir
        custom_n_files=self.custom_n_files
        log=self.logoption
        
        if isinstance(TDIR, str)==False:
            raise NameError('Please provide a string with delimiter: double backslash (\\\) as top directory path.')
        
        del self.fileinfos
        self.fileinfos = {}
        del self.meta
        self.meta = {}
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
                                    if log: self.good_files.append(thisfile)
                                    self.tlist.append(self.fileinfos[thisfile]['transition'])
                                    self.wlist.append(-self.fileinfos[thisfile]['width'])
                            except (ValueError, IndexError):
                                print(f"Error: Couldn't read data in: {thisfile}. "
                                +f"First word: {firstline[0]}. Going on...", end='\r')
                                if log: self.bad_files.append(thisfile)
                                pass
        
        bad_counts = tot_counts-good_counts
        self.meta = { 'nfiles' : tot_counts, 'ngood' : good_counts, 'nbad' : bad_counts }
        print("\n\nProcess completed in %s s." % (format(time.time()-start_time,".2f")))
        print(f"\nTotal number of files found: {tot_counts}.")
        print(f"Total number of good files: {good_counts}. Output paths to good files are stored in self.claro_files. Print it with print_log().")
        print("Total number of bad files: {0[0]} ({0[1]:.1%}) out of total). Output paths to bad files are stored in self.bad_files. Print it with print_log().".format([bad_counts, bad_counts/tot_counts]))
        
    ###########################################################################
    
    def print_log(self, good_files=True, bad_files=True, unfit_files=True):
        """Prints the lists of good, bad and unfit files onto three separate txt files."""
        
        OUTFILE = self._params['OUTFILE']
        OUTBAD  = self._params['OUTBAD']
        UNFIT = self._params['UNFIT']
        
        if good_files:
            if os.path.isfile(OUTFILE): os.remove(OUTFILE)
            for file in self.good_files:
                with open(OUTFILE, "a") as output:
                    output.write(file+"\n")
        if bad_files:
            if os.path.isfile(OUTBAD): os.remove(OUTBAD)
            for file in self.bad_files:
                with open(OUTBAD, "a") as output:
                    output.write(file+"\n")
        if unfit_files:
            try:
                if os.path.isfile(UNFIT): os.remove(UNFIT)
                for file in self.unfit_files:
                    with open(UNFIT, "a") as output:
                        output.write(file+"\n")
            except KeyError:
                print("Please run analysis_loop() method before trying to print unfit_files.")
    
    
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
    
    def analysis_loop(self, fit_dict=None):
        """Analyzes the whole dataset in fileinfos reading files as Single objects.
        
        Produces lists of transition points (x) and widths deduced from fit, self.fit_tlist and self.fit_wlist.
        Accepts parameters to pass to fit_erf(): fit_dict=dict(guesses:list='default', interactive=True).
        """
        
        # Returns processing time as well.
        start_time = time.time()
        
        if fit_dict==None:
            fit_dict=dict(guesses='default', interactive=False)
        for fileinfo in self.fileinfos.values():
            single = Single(fileinfo)
            single.fit_erf(**fit_dict)
            fileinfo['fit_params'] = single.fit_params
            if single.fit_params['code']=='good':
                self.fit_tlist.append(single.fit_params['t'][0])
                self.fit_wlist.append(single.fit_params['w'][0])
                self.fit_tdiff.append(single.transition-single.fit_params['t'][0])
                self.fit_wdiff.append(single.width-single.fit_params['w'][0])
            else:
                self.unfit_files.append(fileinfo['path'])
        
        print("\nProcess completed in %s s." % (format(time.time()-start_time,".2f")))
        return self.fileinfos

    ###########################################################################
    
    def plot_loop(self, fit_dict=None, plot_dict=None, show=False):
        """Analyzes and plots the whole dataset exploiting Single objects.
        
        Produces separate plots in a loop.
        Accepts dict with parameters passed to Single.fit_erf() (refer to analysis_loop
        for list of params in docstring) and Single.plot(): (npoints=1000, interactive=False,
        show_scatter=True, show_fit=True, show_transition=True, save=False, save_dir='.\plot',
        save_format='pdf', show=True).
        """
        
        if fit_dict==None:
            fit_dict=dict(guesses='default', interactive=False)
        if plot_dict==None:
            plot_dict=dict(npoints=1000, interactive=False, log=True, show_scatter=True, show_fit=True, show_transition=True, save=False, save_dir='.\plot', save_format='pdf')
            
        for fileinfo in self.fileinfos.values():
            single = Single(fileinfo)
            single.fit_erf(**fit_dict)
            single.plot(**plot_dict)
            if show: plt.show()
            plt.close()
    
    def plot_MultiPage(self, fit_dict=None, plot_dict=None, save=True, save_path='aHundredPlots.pdf'):
        """Loop on the files and print plots on multi-page pdf.
        
        Accepts **kwargs as dict with parameters passed to Single.fit_erf()
        (refer to analysis_loop for list of params in docstring) and
        Single.plot(): (self, npoints=1000, interactive=False, log=True,
        show_scatter=True, show_fit=True, show_transition=True, save=False,
        save_dir='.\plot', save_format='pdf', show=True, **kwargs).
        Be aware that plot_dict options regulate showing or not of plots.
        
        #######################***WARNING***#######################
        This method takes a while to print the pdf. Use it responsibly.
        """
        
        with PdfPages(save_path) as pdf:
            per_page = int(input("How many plots do you want per page? Allowed values are 1,2,3,4,6. "))
            if per_page==1: nrows, ncols = 1, 1
            elif per_page==2: nrows, ncols = 2, 1
            elif per_page==3: nrows, ncols = 3, 1
            elif per_page==4: nrows, ncols = 2, 2
            elif per_page==6: nrows, ncols = 3, 2
            else: raise NameError("Please run again and choose one of the allowed number of subplots.")
            if fit_dict==None:
                fit_dict=dict(guesses='default', interactive=False)
            if plot_dict==None:
                plot_dict=dict(npoints=1000, interactive=False, show_scatter=True, show_fit=True, show_transition=True, save=False, save_dir='.\plot', save_format='pdf')
                
            for n, fileinfo in enumerate(self.fileinfos.values()):
                # Preprocessing
                print(f"Reading file n. {n}...", end='\r')
                single = Single(fileinfo)
                single.fit_erf(**fit_dict)
           
                # Plotting and saving on multipage pdf
                index = n%per_page+1
                if index==1:
                    fig=plt.figure(figsize=(10,15))
                fig.add_subplot(nrows,ncols,index)
                single.plot(**plot_dict)
                if index==per_page or n==(len(self.fileinfos.values())-1):
                    if save:
                        pdf.savefig(fig)
                        plt.close()
                    
            print(f"Process completed. Output file: {save_path}")
            plt.close()
    
    ###########################################################################
    
    def hist_tw(self, ax, source:str='file'):
        """Produces histograms of transition points and widths from file or from fit.
        
        Source can be 'file' or 'fit' or 'diff': the latter prints the
        histogram of differences bet fitted and from file.
        Can be called only after preprocessing via analysis_loop(). 
        Needs externally-provided figure, axis and saving control. 
        """
        
        if source=='file':
            t_list = self.tlist
            w_list = self.wlist
        elif source=='fit':
            t_list = self.fit_tlist
            w_list = self.fit_wlist
        elif source=='diff':
            t_list = self.fit_tdiff
            w_list = self.fit_wdiff
        else:
            raise NameError("Please provide 'fit' or 'file' as source for transition points and widths to plot.")
        
        annotation_kwargs = {'xy':(.1,.1), 'xycoords':'axes fraction',
                             'bbox':dict(boxstyle="round",edgecolor="black",facecolor="white",alpha=.8)}
        #-----------------------------
        # Transition histogram
        ax[0].set_title(f"Transition points' histogram [{source}]", fontsize=12)
        ax[0].tick_params(axis='y', which='minor', width=0)
        ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))
        counts, bins, pads = ax[0].hist(t_list, bins=int(np.sqrt(len(t_list))), density=False,
                                    label='Transition points (x)', alpha=.9,
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
                       +"\nMean: ({:.2e}".format(popt[1])+r'$\pm$'+'{:.0e})'.format(pdev[1])\
                       +"\nDev: ({:.2e}".format(popt[2])+r'$\pm$'+'{:.0e})'.format(pdev[2]),
                       **annotation_kwargs)
        
        #-----------------------------
        # Widths' histogram
        ax[1].set_title(f"Widths' histogram [{source}]", fontsize=12)
        ax[1].tick_params(axis='y', which='minor', width=0)
        ax[1].yaxis.set_major_locator(MaxNLocator(integer=True))
        counts, bins, pads = ax[1].hist(w_list, bins=int(np.sqrt(len(w_list))), density=False,
                                label='Transition points (x)', alpha=.9,
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
                       +"\nMean: ({:.2e}".format(popt[1])+r'$\pm$'+'{:.0e})'.format(pdev[1])\
                       +"\nDev: ({:.2e}".format(popt[2])+r'$\pm$'+'{:.0e})'.format(pdev[2]),
                       **annotation_kwargs)
    
    
    ###########################################################################
    # Mathematical functions, static methods    
    ###########################################################################
    
    @staticmethod
    def func(x, ampl, a, b):
        """Modified erf function.
        
        Amplitude ampl and shift on the vertical axis ampl/2,
        inflection point at a, normalization proportional to b.
        Deafult guesses are [AMPLITUDE, TRANSITION, AMPLITUDE/2].
        """
        
        return ampl/2*(1+sp.erf((x-a)/(b/2*np.sqrt(2))))
    
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