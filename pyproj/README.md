# Things to do and not to get lost around codes

## Related projects/goals
- [ ] build matplotlib or plotting guide (e.g. as a notebook or md file)
- [x] implement git version control and transport your project on main GIT repo

## Goals
### process_claro
- [x] produce claro_files.txt with paths to good files (process_claro_loop)
- [x] produce bad_files.txt with paths to bad files
- [x] understand what data you need for fitting and make a list of them --> look at plot_fit_claro-py in materiale_tom
- [ ] produce plot of a single file
    - [x] make sure ticks of y axes are manually aligned
    - [x] make sure it can work an all files
    - [x] bring metadata from fileinfos dict down to plotting
    - [x] add annotations
    - [x] add fit parameters+errors
    - [x] use metadata to write correct title for plot
    - [ ] sistemare font of axes' names and annotations
- [ ] implement object-orientation (make classes and functions)
    - [x] make the plot a function
    - [x] produce plots with automatic loop, and choose different plots with different methods defined in a single class
    - [x] define what function you want in your class
    - [ ] build the class with functions to read and plot files
 
- [x] merge process_claro_loop and claro_fit_single

### SiPM
- [ ] 
    - [ ] 


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