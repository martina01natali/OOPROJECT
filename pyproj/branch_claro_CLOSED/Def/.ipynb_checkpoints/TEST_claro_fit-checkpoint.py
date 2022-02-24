###############################################################################
#                      TEST code for claro_fit.py                             #
###############################################################################

from claro_fit import *
from matplotlib.backends.backend_pdf import PdfPages

a = fileinfo('C:\\Users\\MARTINA\\Desktop\\secondolotto_1\\', custom_n_files='all', log=False)

# Loop on the files and print plots on multi-page pdf

custom_n_files = 100     # This is used to break the printing of plots: comment the line
                        # or assign to 'all' to plot all the files

log_choice = False
save_choice = False
save_path = 'aHundredPlots.pdf'

# Histograms of transition points and widths
tw_hist = True # Choose True or False for plotting, showing and saving
t_list = []
w_list = []

with PdfPages(save_path) as pdf:
    
    per_page = int(input("How many plots do you want per page? Allowed values are 1,2,3,4,6. "))
    if per_page==1: nrows, ncols = 1, 1
    elif per_page==2: nrows, ncols = 2, 1
    elif per_page==3: nrows, ncols = 3, 1
    elif per_page==4: nrows, ncols = 2, 2
    elif per_page==6: nrows, ncols = 3, 2
    else: raise NameError("Please run again and choose one of the allowed number of subplots.")
    
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

###### Histograms of transition points and widths
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,5))
hist_tw(t_list, w_list, ax)
# plt.savefig('Hist_tw.pdf')