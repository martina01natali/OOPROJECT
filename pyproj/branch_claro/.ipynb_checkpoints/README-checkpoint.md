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
    - [ ] create different kind of plots and build functions in your class
        - [ ] all channels of a single chip on the same page
- [ ] istogramma di punti di transizione e widths per tutti i file (optional)
- [ ] confronto tra fit e transition point per ogni chip (optional)

- [x] merge process_claro_loop and claro_fit_single
