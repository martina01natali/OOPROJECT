import os
import re
import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import argrelextrema

####################################################################################

def read_wf(fname):
    """
    Basic read function with automatic timestamp or wf file type detection.
    
    Parameters
    ----------
    - fname: relative path of the file with respect to the current working directory
    
    Returns
    -------
    Pandas' dataframe of the data provided.
    
    ############################ UPDATES TO MAKE ####################################
    - requires both files, one after the other and detects which one is still missing 
        after the first is provided
    - checks if they refer to the same data taking (from the path itself)
    
    #################################################################################

    """
    
    # If the file provided is a timestamp file, follow this routine:
    # - open the file
    # - make a dataframe with the timestamps; the header is as default in line 0
    # - timestamps are relative and provide the time interval with respect to the previous trigger:
    #    make them absolute by computing the cumulative of each timestamp with cumsum method of pd
    if re.search("time.csv", fname): 
        timestamp_file_name = fname
        timestamp_path = os.path.join(os.getcwd(),timestamp_file_name)
        timestamp_table = pd.read_csv(timestamp_path) 
            # if file is not found, FileNotFoundError is raised automatically
        timestamp_table.rename(columns = {'X: (s)': 'Event', 'Y: (Hits)':'Timestamp'}, inplace = True)
        N_of_events = len(timestamp_table) # = 1000
        timestamp_table["Timestamp"] = timestamp_table["Timestamp"].cumsum(axis=0)
        
        return timestamp_table
        
    # If the file provided is a waveform file, follow this routine:
    # - open the file
    # - detect the number of datapoints in each waveform, wf_datapoints = 6250
    # - detect end of header ("TIME") and make a dataframe with the wf data
    elif re.search("wf.csv", fname):
        wf_file_name = fname
        wf_path = os.path.join(os.getcwd(),wf_file_name)
        wf_table = pd.DataFrame()
        
        with open(wf_file_name, 'r') as file_wf:
                # if file is not found, FileNotFoundError is raised automatically
            lines = file_wf.readlines()
            for line_counter, line in enumerate(lines):
                if line.startswith("Record Length"): wf_datapoints = int(line.split(',')[-1]) # = 6250
                if line.startswith("Horizontal"): time_unit = str(line.split(',')[-1]).rstrip("\n") # = s\n
                if line.startswith("Vertical"): ampl_unit = str(line.split(',')[-1]).rstrip("\n") # = V\n
                if line.startswith("FastFrame"): wf_events = int(line.split(',')[-1]) # = 1000
                    # To implement when both files are required by the function
                    # if wf_events != N_of_events: break
                if line.startswith("TIME"):
                    wf_table = pd.read_csv(wf_path, header = line_counter-1)
                    break
        
        meta = pd.DataFrame.from_dict({
            'path' : wf_path,
            'n events' : wf_events,
            'data points' : wf_datapoints,
            'time units' : time_unit, # splitting the string by '\' or '\\' doesn't make it detect the '\n' char
            'ampl units' : ampl_unit,
        }, orient='index')
                    
        return wf_table, meta
    
    else:
        raise NameError("Please provide the path to a waveform or timestamp comma-separated file (.csv).")
        
###############################################################################################

def analysis(timestamp_table, wf_table, N_of_events=1,
             threshold=0.006, distance=50,
             inplace=True):
    """
    This function finds all the minima in the waveforms and selects the "good ones" based on
    - minim amplitude = threshold (V)
    - number of data in between two consecutive absolute minima = distance (adim, integer)
    Option inplace tells if the function modifies the original wf dataframe by adding a column with good minima.
    if inplace == True: return nothing
    if inplace == False: return copy of original dataframe with new column of good minima
    
    ############################ UPDATES TO MAKE ####################################
    - RETURNS wf_table complete with all clean minima
    - MUST HAVE inplace=True/False option: like this you're rewriting wf_table every time
    - must decide if you want or not to be able to plot relative minima
    
    anyway, you can go on with the plot! Hurray!
    #################################################################################
    
    """
    start_time = time.time()
    
    wf_datapoints = wf_table.iloc[:,0].size/1000 #N_of_events

    general_clean_min = []
    
    for n in range(N_of_events): # N_of_events = 1000
        print("Analizzando l'evento numero " + str(n), end='\r') #'\r' overwrites output
        event_name = 'Event_' + str(n) + '.png'
        
        wf_table["TIME"].loc[wf_datapoints*n: (wf_datapoints*(n+1))-1] += timestamp_table.at[n,"Timestamp"]
        
        single_wf = wf_table.loc[wf_datapoints*n: (wf_datapoints*(n+1))-1].copy() #(deep=False)
        if n==0: tot_wf = single_wf.copy()
        minimum_list = argrelextrema(single_wf.CH1.values, np.less_equal, order = distance)[0]
        single_wf.loc[:,'min'] = single_wf.iloc[minimum_list]['CH1']
        
        baseline = np.polyfit(single_wf["TIME"].iloc[0:250], single_wf["CH1"].iloc[0:250],0)[0]

        gap = threshold # default = 50
        distance = distance # default = 50 
        
        clean_minimum_list = []
        previous_index = minimum_list[0]
        for index in minimum_list:
            if (baseline - single_wf["CH1"].iat[index] > gap) and (index > previous_index + distance):
                clean_minimum_list.append(index)
                previous_index = index
                
        single_wf.loc[:,'clean_min'] = single_wf.iloc[clean_minimum_list]['CH1']

        wf_index = (n*wf_datapoints)
        for index in clean_minimum_list:
            general_clean_min.append(index + wf_index)
        
        if n==0:
            tot_wf = single_wf.copy()
        else:
            tot_wf = tot_wf.merge(single_wf, on=single_wf.columns.to_list())
    
    wf_table.loc[:,'min'] = wf_table.loc[general_clean_min]['CH1']
    
    print('\nAnalysis completed.')
    print("\nProcess completed in %s s." % (format(time.time()-start_time,".2f")))

    return tot_wf # general_clean_min