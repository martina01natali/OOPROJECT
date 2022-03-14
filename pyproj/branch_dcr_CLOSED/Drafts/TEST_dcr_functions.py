###############################################################################
#                    TEST code for dcr_functions.py                           #
###############################################################################

from dcr_functions import *

wf, meta = read_wf("..\\Data\\DCR\\HPKR00030_2cicli_OV5_wf.csv")
time_table = read_wf("..\\Data\\DCR\\HPKR00030_2cicli_OV5_time.csv")

wf_an, meta = analysis(wf_table=wf, meta=meta, timestamp_table=time_table,
                       custom_n_events=1000,
                       many_minima=500,
                       threshold=0.006, distance=50,
                       plot=False, save_plot=True,
                      )

wf_delta, meta = analysis_delta_t(wf_an, meta, crosstalk_thr=0.015)

plot_2d(wf_delta, meta, save=True)