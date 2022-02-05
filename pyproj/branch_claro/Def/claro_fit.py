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
# def fileinfo(TDIR, DIRPATH="*Station_1__*\Station_1__??_Summary\Chip_*\S_curve",
#                FILEPATH="Ch_*_offset_*_Chip_*.txt")
# 
# def read_data(path)
#
# def fileinfo_find(fileinfo, chip, ch, station='1', sub='11',)
# 
# def fit_erf(x, y, META, npoints=1000)
# 
# def func(x, ampl, a, b)
#     """
#     Modified erf function with amplitude ampl and shift on the vertical axis ampl/2,
#     inflection point at a, normalization proportional to b.
#     Guesses may be provide as a list e.g. [AMPLITUDE, TRANSITION, AMPLITUDE/2].
#     """
#     
# def fit_erf(x, y, META, npoints=1000)
#     
# def plot_fit(x, y, metafit, fileinfo, npoints=1000,
#              show_scatter=True, show_fit=True, show_transition=True,
#              save=False, save_path='.\plot', save_format='pdf', show=True,
#              **kwargs)
# 
#################################################################################################

def fileinfo(TDIR, DIRPATH="*Station_1__*\Station_1__??_Summary\Chip_???\S_curve",
             FILEPATH="Ch_*_offset_*_Chip_*.txt",
             custom_n_files='all',):
    """Function that walks on all subdirectories of TDIR that match DIRPATH and FILEPATH.
    
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
    fileinfos = dict()
    tot_counts  = 0
    good_counts = 0
    
    for root, dirs, files in os.walk(TDIR):
        if fnmatch.fnmatch(root, TDIR + DIRPATH):
            for f in files:
                if custom_n_files!='all':
                    if tot_counts>custom_n_files: break
                if fnmatch.fnmatch(f, FILEPATH):
                    tot_counts += 1
                    thisfile = os.path.join(root,f)
                    with open(thisfile) as csvfile:
                        print(f'Reading {thisfile}', end='\r')
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
                            with open(OUTFILE, "w+") as output:
                                output.write(thisfile+"\n")
                        except ValueError:
                            print(f"ValueError: Couldn't read data in: {thisfile}. Going on...", end='\r')
                            with open(OUTBAD, "w+") as output:
                                output.write(thisfile+"\n")
                            pass
                        except IndexError:
                            print(f"ValueError: Bad data in: {thisfile}. First line: {lines[0]}. Going on...",
                                  end='\r')
                            with open(OUTBAD, "w+") as output:
                                output.write(thisfile+"\n")
                            pass
    
    bad_counts = tot_counts-good_counts
    print("\n\nProcess completed in %s s." % (format(time.time()-start_time,".2f")))
    print(f"\nTotal number of files found: {tot_counts}.")
    print(f"Total number of good files: {good_counts}. Output paths to good files are stored in {OUTFILE}")
    print("Total number of bad files: {0[0]} ({0[1]:.1%}) out of total). Output paths to bad files are stored in {0[2]}".format([bad_counts, bad_counts/tot_counts, OUTBAD]))
    
    return fileinfos

#################################################################################################

def fileinfo_find(fileinfo, chip, ch, station='1', sub='11',):
    for entry in fileinfo.items():
        i = entry[1]
        if i['station']==station and i['sub']==sub and i['chip']==chip and i['ch']==ch:
            path = i['path']
            return path
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
        if guesses=='default':
            guesses=[meta['amplitude'], meta['transition'], meta['amplitude']/2]
        
        bad_list = []            
        fit_params, fit_covar = curve_fit(func, x, y, p0=guesses)
        
        with warnings.catch_warnings(record=True) as w:
            if w:
                if log==True: bad_list.append(meta['path'])
            if warnings_ignore==True: warnings.simplefilter("ignore")

        fit_dev = np.sqrt(np.diag(fit_covar))
        all_params = np.append(fit_params, fit_dev)
        
        for i in all_params:
            if i == np.inf:
                raise ValueError(f'Fit returned an inf parameter. Please try with different GUESSES.')
            elif i < 1e-6:
                raise ValueError(f'Fit returned a parameter that is < 1e-6 or negative. Please try with different set of guesses.')
        if interactive==True: print("Fit ok!")
                
    except ValueError as err:
        if log==True:
            if log==True: bad_list.append(meta['path'])
        if interactive==True: print(f'Error: {err}.\nThe fit parameters are not returned.')
            
    except RuntimeError as err:
        if log==True:
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
        with open("log_unfit.txt", "a") as output:
            if bad_list: output.write(bad_list[0]+"\n")
        return fit_dict

#################################################################################################

def func(x, ampl, a, b):
    """Modified erf function.
    
    Amplitude ampl and shift on the vertical axis ampl/2,
    inflection point at a, normalization proportional to b.
    Deafult guesses are [AMPLITUDE, TRANSITION, AMPLITUDE/2].
    """
    
    return ampl/2*(1+sp.erf((x-a)/(b*np.sqrt(2))))
    
#################################################################################################

def plot_fit(x, y, metafit, fileinfo, npoints=1000,
             interactive=False, log=True,
             show_scatter=True, show_fit=True, show_transition=True,
             save=False, save_path='.\plot', save_format='pdf', show=True,
             **kwargs):
    """[Function documentation]
    
    """
    
    title = f"Fit CLARO: station {fileinfo['station']}, chip {fileinfo['chip']}, ch {fileinfo['ch']}"
    
    font = {
    'fontsize': plt.rcParams['axes.titlesize'],
    'fontweight' : plt.rcParams['axes.titleweight'],
    'verticalalignment': 'baseline',
    # 'horizontalalignment': plt.loc,
    }
    
    plt.figure(figsize=(5,5), tight_layout=True)
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
    
        # x,y data computed as a grid of npoints and using parameters of the fit
        fit_params = metafit['params']
        fit_errs = metafit['errors']
        
        xfit = np.linspace(x.min(), x.max(), npoints)
        yfit= func(xfit, *fit_params)
        
                             
        # Show plot of fit (default = True)
        if show_fit == True: 
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
    
    if save == True:
        plt.savefig(save_path+'.'+save_format)
    
    if show == True:
        plt.show()
        plt.close()
    else:
        plt.close()