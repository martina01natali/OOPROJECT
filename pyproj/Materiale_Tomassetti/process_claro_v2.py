
import os
import fnmatch
import re
import csv

TDIR = "/Users/luca/Documents/didattica/fisica/OOP for experimental data analysis/spunti/bash/secondolotto_1/"

fileinfos = dict()
# lista_di_file = []
for root, dirs, files in os.walk(TDIR):
    # print(root)
    if fnmatch.fnmatch(root, TDIR + "*Station_1__*/Station_1__??_Summary/Chip_*/S_curve"):
        for f in files:
            if fnmatch.fnmatch(f, "Ch_*_offset_*_Chip_*.txt"):
                thisfile = os.path.join(root,f)
                # print(thisfile)
                with open(thisfile, newline='') as csvfile:
                    firstline = csvfile.readline().split()
                    try:
                        if float(firstline[2]):
                            temp = re.findall("[0-9]+", thisfile)
                                # fileinfos[f] = temp
                            fileinfos[thisfile] = {'station': temp[0],
                                      'sub': temp[2],
                                      'chip': temp[5],
                                      'ch': temp[6],
                                      'offset': temp[7],
                                      'transition': firstline[1],
                                      'width': firstline[2]}
                    except (ValueError, IndexError):
                        pass

