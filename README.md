# OOPROJECT
Exam project for Object Oriented Programming course.

The main goal of the exam was to produce two projects, in Python and C++, to analyze experimental data from tests on amplifiers and SiPMs.
Full explanation of everything that's going on is not assured. I tried my best but I am aware that I may have missed some important things. Most of the theoretical material that is needed to understand the functioning of SiPMs is contained in pyproj/Notes/ in the form of notes taken during class and a very instructive pdf from a lecture. Beware: everything is in italian. 


Organization:
- pyproj is the project in Python and Jupyter Notebooks: the project has been aggregated in the form of an installable module, named pyproj. Below you will find the installation instructions for the module if you're interested in actually using it. 
- cproj is the project in C++
- subprojects are named "/branch_\*"
- final codes are in folders named "/Def" 
- TEST_\* files are codes to test analysis routines on the classes that have been written, so you should always start from there


## Installing `pyproj`

Download this repo as a .zip file. Open the terminal and put yourself in the folder ./pyproj/projmodule/. If you check the list of files that are present, you should have `setup.py` as well as other files. Run the following on the command line: 

`python3 setup.py install`

If everything has gone well, we should now be able to import `pyproj` from anywhere on our system: this means that when building a code in python, the command `import pyroj` should import everything in the module as you do for any other library.
