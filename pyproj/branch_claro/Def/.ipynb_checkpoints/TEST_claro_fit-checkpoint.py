###############################################################################
#                      TEST code for claro_fit.py                             #
###############################################################################

from claro_fit import *
from matplotlib.backends.backend_pdf import PdfPages

a = fileinfo('C:\\Users\\MARTINA\\Desktop\\secondolotto_1\\', custom_n_files='all')

# Loop on the files and print plots on multi-page pdf

custom_n_files = 100    # This is used to break the printing of plots, comment the line
                        # or assign to 'all' to plot all the files

save_path = '\Plots\aHundredPlots.pdf'
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
        x,y,meta = read_data(file['path'])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            metafit = fit_erf(x,y,meta, interactive=False, log=True)
        
        # Plotting and saving on multipage pdf
        if n>=custom_n_files: continue
        index = n%per_page+1
        if index==1:
            fig=plt.figure(figsize=(10,15)) 
        fig.add_subplot(nrows,ncols,index)
        plot_fit(x, y, metafit, fileinfo=file, show=True, save=False, log=True)
        if index==per_page or n==len(a.values())-1:
            pdf.savefig(fig)
            plt.close(fig)
            
    plt.close()