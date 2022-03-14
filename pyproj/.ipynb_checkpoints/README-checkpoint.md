# README - pyproj

This is the main README file for the project in Python.
Keep updated with your main progress, issues, big fixes.
"--" this tells you that a fix is rated low priority

---

## branch_dcr
- [x] spacchettare varie waveform e cercare picchi in singole waveforms
- [x] analizzare picchi: contarli, misurarne l'ampiezza
- [x] plot 2D ampiezza vs intervallo di tempo
- [x] stima grossolana dark count rate considerando numero totale di picchi e tempo totale riportato nel file della waveform
- [x] add annotation with estimated DCR on 2D plot

---

## branch_claro
- [x] produce claro_files.txt with paths to good files (process_claro_loop)
- [x] produce bad_files.txt with paths to bad files
- [x] understand what data you need for fitting and make a list of them --> look at plot_fit_claro-py in materiale_tom
- [x] produce plot of a single file
    - [x] make sure ticks of y axes are manually aligned
    - [x] make sure it can work an all files
    - [x] bring metadata from fileinfos dict down to plotting
    - [x] add annotations
    - [x] add fit parameters+errors
    - [x] use metadata to write correct title for plot
    - [x] sistemare font of axes' names and annotations
- [x] implement object-orientation (make classes and functions)
    - [x] make the plot a function
    - [x] produce plots with automatic loop, and choose different plots with different methods defined in a single class
    - [x] define what function you want in your class
    - [x] build the class with functions to read and plot files
    - [x] create different kind of plots and build functions in your class
        - [ ] all channels of a single chip on the same page
- [x] istogramma di punti di transizione e widths per tutti i file (optional)
- [x] confronto tra fit e transition point per ogni chip (optional)

- [x] merge process_claro_loop and claro_fit_single

- [x] UPDATE DOCUMENTATION OF FUNCTIONS IN claro_fit.py

---

## branch_sipm
