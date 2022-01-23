# Things to do and not to get lost around codes

## Goals

### branch_dcr
- [ ] spacchettare varie waveform e cercare picchi in singole waveforms
- [ ] analizzare picchi: contarli, misurarne l'ampiezza
- [ ] plot 2D ampiezza vs intervallo di tempo
- [ ] stima grossolana dark count rate considerando numero totale di picchi e tempo totale riportato nel file della waveform

#### functions
Read the header, the UPDATES are the things you should start again to work on.

- [ ] read_wf
- [ ] plot_wf
- [ ] plot_dcr

####################################################################
## Object-orientation

Follow strategy: 1 function = 1 action

### Structure/header

```python
def find_paths(TDIR, DIRPATH, FILEPATH)
"""
MAY BE DIVIDED IN 2 FUNCTIONS:
        get_claro_paths to print only bad and good files
        get_claro_data to get paths and data to be passed inside plot
    HAVE TO CHECK IF DATA EXTRACTION WITH PANDAS IS FASTER THAN STRING-SEARCH
        --> NEED CLOCK
        ------all done------------
"""

def read_data(path)
"""
NAME IS IN CONFLICT WITH claro_read
    What it does: reads all data of files in path
    What it returns: x, y, and GUESSES = [AMPLITUDE, TRANSITION, AMPLITUDE/2]
"""        

def fit_erf(x, y, META, npoints=1000):
"""
what it does: fits the data with an erf function and plots it
            IT DOES 2 THINGS, NO GOOD, NEED TO BE DIVIDED
    NEW THINGS TO DO:
        - return xfit, yfit, and list of parameters with st.dev., not correlation matrix, to be used in annotation in plot
"""

def plot_fit(x, y, xfit, yfit, metafit,
             show_scatter=True, show_fit=True, show_transition=True,
             save=False,
             **kwargs):
"""
    what it does: takes the output of fit_erf (xfit, yfit) and the errors and prints the plot of the best-fit curve upon the data; automatically detects transition point and has option to print it highlighted
"""

#--------------------------------------------------------------------#
# New functions to construct

def errorplot_fit(...):
"""
what it does: prints the minimal, maximal and best fit curves, the first two can be get from +- std.dev.
"""    
```
