#!/usr/bin/env python

# %matplotlib # namespace not used for now

import os
import re
import csv
import time
import fnmatch
import warnings
import numpy as np
import pandas as pd
import matplotlib as mplt
import matplotlib.pyplot as plt
from scipy import special as sp
from scipy.optimize import curve_fit

######################################## HEADER #################################################
# def fileinfo(TDIR, DIRPATH="*Station_1__*\Station_1__??_Summary\Chip_???\S_curve",
#              FILEPATH="Ch_*_offset_*_Chip_*.txt",
#              custom_n_files='all',
#              log=True)
# def fileinfo_find(fileinfo, chip, ch, station='1', sub='11',) -> dict():
# def read_data(path):
# def fit_erf(x, y, meta, guesses='default',
#             interactive=True, log=True, warnings_ignore=True, 
#             npoints=1000):
# def plot_fit(x, y, metafit, fileinfo, npoints=1000,
#              interactive=False, log=True,
#              show_scatter=True, show_fit=True, show_transition=True,
#              save=False, save_path='.\plot', save_format='pdf', show=True,
#              **kwargs):
# def hist_tw(t_list, w_list, ax):
# def func(x, ampl, a, b):
# def skew_gauss(x, A, mean, dev, alpha,):
# def gauss(x, A, mean, dev):
#################################################################################################

def fileinfo(TDIR, DIRPATH="*Station_1__*\Station_1__??_Summary\Chip_???\S_curve",
             FILEPATH="Ch_*_offset_*_Chip_*.txt",
             custom_n_files='all',
             log=True):
    """Function that walks on all subdirectories of TDIR that match DIRPATH and FILEPATH.
    
    Inputs
    ------
    TDIR: absolute path
        Path to the top directory.
    DIRPATH: relative path, wildcards admitted
        Regular expression with relative path to the folders and subfolders
        where the walk will take place.
    FILEPATH: relative path, wildcard admitted
        Regular expression with relative path to the files to walk on.
    custom_n_files: int or str, default='all'
        Arbitrary number of files to process, used for testing purposes.
    
    Returns
    -------
    - dict containing the following keys:
        - path
        - station
        - sub
        - chip
        - ch
        - offset
        - amplitude 
        - transition
        - width
    
    """
    
    # Returns processing time as well.
    start_time = time.time()
    
    if isinstance(TDIR, str)==False:
        raise NameError('Please provide a string with delimiter: double backslash (\\\) as top directory path.')

    enter = input(f'The default subfolders\' paths are {DIRPATH}.\n'
                    +f'The default file names are {FILEPATH}.\n'
                    +f'To confirm, press Enter. Press any other key to change the paths.\n')
    if enter != '':
        DIRPATH  = input('Please provide subfolders\' paths. You may use wildcards.\n')
        FILEPATH = input('Please provide file names. You may use wildcards.\n')
    
    OUTFILE = "claro_files.txt"
    OUTBAD  = 'bad_files.txt'
    for file in [OUTFILE, OUTBAD]:
        if log==True and os.path.isfile(file): os.remove(file)
    
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
                                fileinfos[thisfile] = {
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
                            if log==True:
                                with open(OUTFILE, "a") as output:
                                    output.write(thisfile+"\n")
                        except (ValueError, IndexError):
                            print(f"Error: Couldn't read data in: {thisfile}. "
                            +f"First word: {firstline[0]}. Going on...", end='\r')
                            if log==True:
                                with open(OUTBAD, "a") as output:
                                    output.write(thisfile+"\n")
                            pass
    
    bad_counts = tot_counts-good_counts
    print("\n\nProcess completed in %s s." % (format(time.time()-start_time,".2f")))
    print(f"\nTotal number of files found: {tot_counts}.")
    print(f"Total number of good files: {good_counts}. Output paths to good files are stored in {OUTFILE}")
    print("Total number of bad files: {0[0]} ({0[1]:.1%}) out of total). Output paths to bad files are stored in {0[2]}".format([bad_counts, bad_counts/tot_counts, OUTBAD]))
    
    return fileinfos

#################################################################################################

def fileinfo_find(fileinfo, chip, ch, station='1', sub='11',) -> dict():
    """Returns metadata of file with given chip, ch, station and sub"""
    
    for entry in fileinfo.items():
        i = entry[1]
        if i['station']==station and i['sub']==sub and i['chip']==chip and i['ch']==ch:
            path = i['path']
            return i
            break
    raise NameError('No mathing file found in provided dict.')

#################################################################################################

def read_data(path):
    data = pd.read_csv(path, sep='\t', header=None, skiprows=None)
    x = data.iloc[2:,0].to_numpy()
    y = data.iloc[2:,1].to_numpy()
    AMPLITUDE = data.iloc[0,0]
    TRANSITION = data.iloc[0,1]
    WIDTH = -data.iloc[0,2]
    META = {
        'path' : path,
        'amplitude' : AMPLITUDE,
        'transition' : TRANSITION,
        'width' : WIDTH
    }
    return x, y, META

#################################################################################################

def fit_erf(x, y, meta, guesses='default',
            interactive=True, log=True, warnings_ignore=True, 
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
    - dict with parameters of the fit and metadata 'code'=['good' or 'bad']
    
    """
    
    # Sample dict of fit parameters
    fit_dict = {
            #'params' : list(np.zeros(3)), #[amplitude, transition, width/2]
            #'errors' : list(np.zeros(3)),
            'code' : 'bad'
        }
    
    try:
        if warnings_ignore==True:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("ignore")
                
        if guesses=='default':
            guesses=[meta['amplitude'], meta['transition'], meta['amplitude']/2]
        
        bad_list = []            
        fit_params, fit_covar = curve_fit(func, x, y, p0=guesses)
        fit_dev = np.sqrt(np.diag(fit_covar))
        all_params = np.append(fit_params, fit_dev)
        
        # Warnings catch
        if w:
            if log==True: bad_list.append(meta['path'])
        
        for i in all_params:
            if i == np.inf:
                raise ValueError(f'Fit returned an inf parameter. Please try with different GUESSES.')
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
        fit_dict = {
            'params' : [fit_params[i] for i in range(len(fit_params))], #[amplitude, transition, width/2]
            'errors' : [fit_dev[i] for i in range(len(fit_dev))],
            'code' : 'good'
        }
        return fit_dict
    
    finally:
        if log==True:
            with open("log_unfit.txt", "a") as output:
                if bad_list: output.write(bad_list[0]+"\n")
        return fit_dict

    
#################################################################################################

def plot_fit(x, y, metafit, fileinfo, npoints=1000,
             interactive=False, log=True,
             show_scatter=True, show_fit=True, show_transition=True,
             save=False, save_path='.\plot', save_format='pdf', show=True,
             **kwargs):
    """Scatterplot of data, with options to plot both the erf fit and transition point.
    
    """
    
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
        # plt.legend(loc='lower right', fontsize = 8)
    
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
            plt.annotate(f"Fit parameters\nAmplitude = ({fit_params[0]:.2f}"+r" $\pm$ "+f"{fit_errs[0]:.2f})\n"
                         +f"Transition = ({fit_params[1]:.2f}"+r" $\pm$ "+f"{fit_errs[1]:.2E})\n"
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
    
    # The following lines are to uncomment when the function is used
    # as a stand-alone, without any external way to save
    
    # if save == True:
    #     plt.savefig(save_path+'.'+save_format)
    # if show == True:
    #     plt.show()
    #     plt.close()
    # else:
    #     plt.close()

#################################################################################################

def hist_tw(t_list, w_list, ax):
    
    import math
    import scipy.stats as ss
    import scipy.special as sp
    from scipy.optimize import curve_fit
    from matplotlib.ticker import MaxNLocator
    
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
    popt, pcov = curve_fit(gauss, bins[:-1], counts, bounds=fit_bounds, maxfev=1000)
    pdev = np.sqrt(np.diag(pcov))
    A, mean, dev = popt[0], popt[1], popt[2]
    x = np.linspace(min(t_list), max(t_list), 1000)
    fit = gauss(x, A, mean, dev)
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
    popt, pcov = curve_fit(skew_gauss, bins[:-1], counts, bounds=fit_bounds, maxfev=1000)
    pdev = np.sqrt(np.diag(pcov))
    A, mean, dev, alpha = popt[0], popt[1], popt[2], popt[3]
    x = np.linspace(min(w_list), max(w_list), 1000)
    fit = skew_gauss(x, A, mean, dev, alpha)
    ax[1].plot(x, fit, c='red')
    
    ax[1].annotate(f"N entries: {len(w_list)}\n"\
                   +"Fit type: skew gauss"\
                   +"\nMean: ({:.1e}".format(popt[1])+r'$\pm$'+'{:.1e})'.format(pdev[1])\
                   +"\nDev: ({:.1e}".format(popt[2])+r'$\pm$'+'{:.1e})'.format(pdev[2]),
                   **annotation_kwargs)
    
#################################################################################################

def func(x, ampl, a, b):
    """Modified erf function.
    
    Amplitude ampl and shift on the vertical axis ampl/2,
    inflection point at a, normalization proportional to b.
    Deafult guesses are [AMPLITUDE, TRANSITION, AMPLITUDE/2].
    """
    
    return ampl/2*(1+sp.erf((x-a)/(b*np.sqrt(2))))

#################################################################################################

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

#################################################################################################

def gauss(x, A, mean, dev):
    """Not-normalized, shifted gaussian distribution."""
    
    import math
    
    pdf = (1/(dev*np.sqrt(2*math.pi)))*np.exp(-(x-mean)**2/(2*dev**2))
    return A*pdf