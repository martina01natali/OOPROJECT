import os
import re
import time
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib import pyplot as plt
from scipy.signal import argrelextrema


class DarkCounts():
    """Class DarkCounts is used to analyze waveforms and estimate the DCR of a SiPM."""
    
    PARAMS = {'custom_n_events' : 1000,
              'thr' : 0.006,
              'cross_thr' : 10e-3,
              'delay_thr' : 6e-6,
             }
    DATAFILES = { 'wf' : '', 'time' : '' }
    
    #-------------------------------------------------------------------------#
    
    def __init__(self, datafiles:dict=DATAFILES, params:dict=PARAMS):
        """Initializer that takes dict with relative paths of files to process and reads them, creating dataframes associated."""
        
        self._datafiles = datafiles
        self.meta = {'path_wf' : datafiles['wf'], 'path_time' : datafiles['time'],}
        self._params = params
        
        self.wf = pd.DataFrame()
        self.time = pd.DataFrame()
        self.wf_processed = pd.DataFrame()
        self.read_datafiles()
        
    #-------------------------------------------------------------------------#
    
    def __repr__(self):
        print("{:<25}".format("meta:"))
        for key, value in self.meta.items():
            print("{:<25} {:<25}".format(key,value))        
        print("\n{:<25}".format("params:"))
        for key, value in self._params.items():
            print("{:<25} {:<25}".format(key,value))  
        return ""
    
    #-------------------------------------------------------------------------#
    
    # print(u"\u00B1")
    @property
    def dcr(self):
        try:
            print('Estimated DCR: ({:.2e} '.format(self.meta['DCR (Hz)'])\
                  +u"\u00B1"\
                  +' {:.0e}) Hz'.format(self.meta['% bad wf']/100*self.meta['DCR (Hz)']))
            print("\nThe relative error associated to the DCR is equal to the percentage of \'bad\' waveforms detected in the provided dataset ({:.2f}%). This is an arbitrary choice due to lack of multiple measurements on the same instrument.".format(self.meta['% bad wf']))
        except (AttributeError, KeyError) as err:
            print("DCR not estimated yet. Call .analysis() first.")
        
    @property
    def custom_n_events(self):
        return "%d" % self._params['custom_n_events']
    
    @custom_n_events.setter
    def custom_n_events(self, value):
        self._params['custom_n_events'] = value
    
    @property
    def params(self):
        return self._params
    
    @params.setter
    def params(self, value:dict):
        self._params = value
        
    @property
    def datafiles(self):
        return self._datafiles
    
    @datafiles.setter
    def datafiles(self, value:dict):
        self._datafiles = value
        
        
    ###########################################################################
    
    def read_datafiles(self):
        """Basic read function with automatic timestamp or wf file type detection.
        
        Produces attributes self.wf and self.time that are dataframes of data associated to 
        
        """
        
        timestamp_file_name = self._datafiles['time']
        timestamp_path = os.path.join(os.getcwd(),timestamp_file_name)
        self.time = pd.read_csv(timestamp_path) 
        # if file is not found, FileNotFoundError is raised automatically
            
        self.time.rename(columns = {'X: (s)': 'Event', 'Y: (Hits)':'Timestamp'}, inplace = True)
        self.time["Timestamp"] = self.time["Timestamp"].cumsum(axis=0)
                
        wf_file_name = self._datafiles['wf']
        wf_path = os.path.join(os.getcwd(),wf_file_name)
            
        with open(wf_file_name, 'r') as file_wf:
            lines = file_wf.readlines()
            for line_counter, line in enumerate(lines):
                if line.startswith("Record Length"): 
                    self.meta['wf_datapoints'] = int(line.split(',')[-1])
                if line.startswith("Horizontal"):
                    self.meta['time_unit'] = str(line.split(',')[-1]).rstrip("\n")
                if line.startswith("Vertical"):
                    self.meta['ampl_unit'] = str(line.split(',')[-1]).rstrip("\n")
                if line.startswith("FastFrame"):
                    self.meta['wf_events'] = int(line.split(',')[-1])
                if line.startswith("TIME"):
                    self.wf = pd.read_csv(wf_path, header = line_counter-1)
                    break        

    ###########################################################################
    
    def analysis(self, distance=50, many_minima=6250,
                 plot=False, save_plot=False, save_format='png'):
        """Function to analyze waveform data and locate clean signal peaks.
        
        This function finds all the minima in each waveform (wf) and selects the "good ones"
        (clean_min) based on threshold (V) and distance (#). The resulting dataframe has a column "code" that indicates if a clean_min belongs to a good or bad wf: bad wfs are the ones containing a number of relative minima bigger than many_minima or that contain -inf saturated data. Notice that the "good" or "bad" coding makes sense for discriminating between equally clean_min only: discrimination is not provided for minima that are not considered to be "good" signal.
       
       ------
       Input:
       - custom_n_events: int, optional, default 1000
           Number of events to analyze (starts from the first waveform in any case)
       - threshold: float, default 0.006 [V]
           Minimum value of signal to discriminate it from noise, in units of V
       - distance: int, default 50
           Number of data in between two consecutive absolute minima
       - many_minima: int, default 6250 (# data in single waveform)
           Provide a number of minimum minima to be found to turn on or off a warning 
           that is raised if in the waveform there are more than that number of minima.
           Also provides additional column in dataframe with code "bad_wf" for
           waveforms that satisfy the above condition.
       - plot: bool, default False
           If True, plot the scatterplot of the waveforms with the relative minima in a
           recursive way
        - save_plot: bool, default False
           If True, saves the plot in the cwd with format provided by the string save_format.
       
       --------
       Returns:
       - copy of original dataframe with added columns of minima (total) and clean minima (based
           on threshold and distance)
        
        """
        
        if not self.wf_processed.empty:
            answer = input("Analysis has already ben run on this dataset. Check the analyzed dataframe by calling self.wf_processed. Do you want to proceed anyway? (y/n) " )
            if answer=='n': return
        
        start_time = time.time()
        
        custom_n_events = self._params['custom_n_events']
        wf_datapoints = self.meta['wf_datapoints']
        threshold = self._params['thr']
        
        copy = self.wf.copy()
        general_clean_ampl = []
        general_clean_min = []
        general_code_list = []
        time_list = []
        N_bad_wf = 0
            
        for n in range(custom_n_events):
            print("Analysis of event number " + str(n+1), end='\r') #'\r' overwrites output
            event_name = 'Event_' + str(n) + '.' + save_format
            copy["TIME"].loc[wf_datapoints*n: (wf_datapoints*(n+1))-1] += self.time.at[n,"Timestamp"]            
            single_wf = copy.loc[wf_datapoints*n: (wf_datapoints*(n+1))-1].copy()
            minimum_list = argrelextrema(single_wf.CH1.values, np.less_equal, order = distance)[0]
            baseline = np.polyfit(single_wf["TIME"].iloc[0:250], single_wf["CH1"].iloc[0:250],0)[0]
            time_list.append(single_wf.TIME.max()-single_wf.TIME.min())
    
            gap = threshold
            clean_minimum_list = []
            previous_index     = minimum_list[0]
            
            for index in minimum_list:
                if (baseline - single_wf["CH1"].iat[index] > gap)\
                and (index > previous_index + distance)\
                and (single_wf["CH1"].iat[index]!=-np.inf)\
                and (len(minimum_list) < many_minima):
                    general_code_list.append('good')
                    clean_minimum_list.append(index)
                    general_clean_ampl.append(abs(single_wf["CH1"].iat[index])-abs(baseline))
                    previous_index = index
            
            wf_index = (n*wf_datapoints)
            for index in clean_minimum_list:
                general_clean_min.append(index + wf_index)
                
            inf_counts = len(single_wf[single_wf.CH1==-np.inf])
            if (inf_counts == 0)\
            and (len(minimum_list) < many_minima)\
            and (len(clean_minimum_list)):
                code = 'good'
            else:
                N_bad_wf += 1
                code = 'bad'
            
            # Plotting control (for single_wf)
            if plot==True or save_plot==True:
                fig, ax = plt.subplots()
                single_wf.loc[:,'min'] = single_wf.iloc[minimum_list]['CH1']
                single_wf.loc[:,'clean_min'] = single_wf.iloc[clean_minimum_list]['CH1']
                ax.plot(single_wf["TIME"], single_wf['CH1'], linestyle="-", linewidth=1)
                ax.scatter(single_wf["TIME"], single_wf['min'], color="darkred")
                ax.scatter(single_wf["TIME"], single_wf['clean_min'], color="green")
                ax.axhline(baseline, c='b')
                ax.set_title(f'Waveform analysis: event n_{n}')
                ax.set_xlabel('Relative time (s)')
                ax.set_ylabel('Amplitude (V)')
                ax.text(0.8,0.8,
                        code,
                        transform=ax.transAxes,
                        fontsize=12,
                        color='black',
                        bbox=dict(boxstyle="round",
                                  edgecolor="black",
                                  facecolor="palegreen" if code=='good' else "lightsalmon",
                                  alpha=.8),
                       )
                
                if save_plot==True:
                    data_origin = self.meta['wf_path'].split('\\')[-1].split('_')[-2]
                    try:
                        figure_path = os.path.join(os.path.join(os.getcwd(),f'Plots_{data_origin}'), event_name)
                        plt.savefig(figure_path)
                        if plot==False: plt.close()
                    except FileNotFoundError:
                        print(f'Creating "Plots_{data_origin}" subfolder in your current working directory...\n')
                        os.mkdir(f'Plots_{data_origin}')
                        figure_path = os.path.join(os.path.join(os.getcwd(),f'Plots_{data_origin}'), event_name)
                        plt.savefig(figure_path)
                        if plot==False: plt.close()
                    finally:
                        if plot==False: plt.close()
        
        # Metadata update
        total_time = sum(time_list)
        self.meta['total acquis time (s)'] = total_time
        self.meta['n clean minima'] = len(general_clean_min)
        self.meta['% bad wf'] = N_bad_wf/custom_n_events*100
        self.meta['DCR (Hz)'] = self.meta["n clean minima"]/total_time
        
        # Printed output
        print('\nAnalysis completed.')
        print('Number of clean minima found: %d' % len(general_clean_min))
        print('Fraction of waveforms with too many minima or -inf data ("bad_wf") on total: {:.1%}'.format(N_bad_wf/custom_n_events))
        print('Total acquisition time: {0:0.3e} s'.format(total_time))
        print('Estimated DCR: ({:.2e} '.format(self.meta['DCR (Hz)'])\
              +u"\u00B1"+" {:.0e}) Hz".format(self.meta['% bad wf']/100*self.meta['DCR (Hz)']))
            
        # Return control
        clean_ampl = pd.DataFrame(
            {'ampl_min':general_clean_ampl, 'code':general_code_list},
            index=general_clean_min)
            
        copy.loc[:,'clean_min'] = copy.iloc[general_clean_min]['CH1']
        copy = copy.join(clean_ampl)
        copy.code.fillna(value='bad', inplace=True)
        copy['wfID'] = np.array(range(len(copy))) // 6250
        copy.set_index('wfID', append=True, inplace=True)
        
        self.wf_processed = copy
        print("Process completed in %s s." % (format(time.time()-start_time,".2f")))
        print("Processed dataset is stored in attribute .wf_processed.")
        return copy

    ###########################################################################
    
    def analysis_noise(self):
        """Function to polish the dataframe returned from the analysis function and discriminate between noise.
        
        Returns
        -------
        - dataframe with columns "Delta T (s)" and "Amplitude (V)" that can be used for 2D plotting
        """
            
        crosstalk_thr = self._params['cross_thr']
        delayed_cross_thr = self._params['delay_thr']
        
        def noise_discrimination(df, crosstalk_thr, delayed_cross_thr, inplace=True):
            
            if inplace==False: df = df.copy()
    
            df.loc[df['Amplitude (V)'] < crosstalk_thr, 'Noise'] = 'primary dark counts'
            df.loc[(df['Amplitude (V)'] < crosstalk_thr)\
                   & (df['Delta T (s)'] < (delayed_cross_thr)),
                   'Noise'] = 'afterpulse'
            df.loc[df['Amplitude (V)'] >= crosstalk_thr, 'Noise'] = 'crosstalk'
            df.loc[(df['Amplitude (V)'] >= crosstalk_thr)\
                   & (df['Delta T (s)'] < (delayed_cross_thr)),
                   'Noise'] = 'delayed crosstalk'

            return df
        
        try:
            mins = self.wf_processed.dropna()
            mins = mins.loc[mins.code=='good']
            mins['TIME'] = mins['TIME'].diff(periods=1)
            mins = mins.iloc[1:,[0,-2]]
            mins.rename(columns={'TIME':'Delta T (s)','ampl_min':'Amplitude (V)'}, inplace = True)
        
            mins = noise_discrimination(mins,
                                        crosstalk_thr=crosstalk_thr,
                                        delayed_cross_thr=delayed_cross_thr,
                                        inplace=True)
            self.wf_processed = mins
        except AttributeError:
            print("This method can be called only once on a dataset, since it modifies it. You already run it, so you can go ahead! If you want to retrieve the processed dataset, access the attribute .wf_processed or use the return of this function (that is a copy of the attribute).")
        
        copy = self.wf_processed.copy()
        return copy
    
    ###########################################################################
    
    def plot_2d(self, sns_palette='deep', title='2D plot',
            show=True, save=False, save_path='Amplitude_vs_dt', save_extension='pdf',
            **kwargs,):
        """2D plot of DCR with amplitude (V) vs time delta (s) scatterplot and histogram."""
        
        # Preprocessing
        dcr = self.meta['DCR (Hz)']
        mins = self.wf_processed
        n_mins = len(mins)
        noise_list_red = mins.groupby('Noise').count().index.values
        data_origin = self.meta['path_wf'].split('\\')[-1].split('_')[-2]
        
        deep_cmap = sns.color_palette(sns_palette, 10)
        palette = sns.color_palette([deep_cmap[i] for i in range(len(noise_list_red))])
        palette_dict = {noise_list_red[i] : palette[i] for i in range(len(noise_list_red))}
        mean_dict = {key : mins.groupby('Noise').mean().loc[key]['Delta T (s)'] for key in noise_list_red}
        percent_dict = {key : mins.groupby('Noise').count().loc[key].values[0]/n_mins*100 for key in noise_list_red}
        
        # Plotting        
        f = plt.figure(figsize=(10,8))
        gs = f.add_gridspec(2, 1, height_ratios=(5, 3),
                              left=0.1, right=0.9, bottom=0.1, top=0.9,
                              wspace=0, hspace=0)

        ax1 = f.add_subplot(gs[0, 0])
        ax2 = f.add_subplot(gs[1, 0], sharex=ax1)
        
        sns.scatterplot(data=mins, x="Delta T (s)", y="Amplitude (V)", hue="Noise", ax=ax1,
                        hue_order=[key for key in noise_list_red],
                        alpha=0.7, legend=False, palette=sns_palette)
        sns.histplot(data=mins, x="Delta T (s)", hue="Noise", ax=ax2, bins=30,
                    hue_order=[key for key in noise_list_red],
                    multiple="stack", fill=True, log_scale=True, common_norm=True,
                    edgecolor='white', alpha=0.7, palette=sns_palette,
                    legend=False)
        
        ax1.set_title(title+f'_{data_origin}', fontsize=14)
        ax1.set_xscale('log')
        ax2.set_xscale('log')
        ax2.set_ylabel('Counts')
        
        legend_scatter = [Line2D([0], [0], marker='o', color='w', label=key,
                                 markerfacecolor=palette_dict[key], markersize=8) for key in palette_dict.keys()]
        
        legend_hist = [Line2D([0], [0], marker='o', color='w', label=key+' ({0:0.1f}%)'.format(percent_dict[key]),
                                  markerfacecolor=palette_dict[key], markersize=8) for key in palette_dict.keys()]
        
        ax1.legend(handles=legend_scatter, loc='upper left')
        ax2.legend(handles=legend_hist, loc='upper left')
        
        ax1.text(.65, .85,
                 'N good events: %d\n' % self.meta['n clean minima']\
                 +'Acquisition time: {:.2e} s\n'.format(self.meta['total acquis time (s)'])\
                 +'DCR = '+'({:.2e} '.format(dcr)\
                 +r'$\pm$'\
                 +" {:.0e}) Hz".format(self.meta['% bad wf']/100*dcr),
                 ha='left', va='center',
                 transform=ax1.transAxes,
                 fontsize=12,
                 color='black',
                 bbox=dict(boxstyle="square",
                           edgecolor="gray",
                           facecolor="white",
                           alpha=.8,
                          )
                )
        
        # Output control
        if show==True:
            plt.show()
        else:
            plt.close()
        
        if save==True:
            f.savefig(f'{data_origin}_'+save_path+'.'+save_extension)
            
    ###########################################################################
        