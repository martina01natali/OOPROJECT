# README

## c++ projects

**GIT BRANCH OF CHOICE**: `cpp`

**WARNING**: it is better to start this project, or at least the chi-squared minimization, after having completed the python project

c++: 1 file in claro, read it (using std library), mettere parametri in container appropriati e provate a fare il fit lineare a mano con minimizzazione dei quadrati dei tre punti di mezzo con le y tra 0 e 1000. Use the most modern c++ syntax you can; passa argomenti by ref or by const ref

### Goals and subgoals
- [x] create program to read 1 file
- [ ] ~update program to read all the files (all the absolute paths to the
  files) from a file that contains paths to good files only, produced by
  bash script or python~
- [x] put data in a vector
- [x] divide data in vectors for x, y1, y2
- [ ] select "middle" data (!= 0 && !=1000) and fit linearly with chi-squared minimization
- [ ] construct header file and start building claro class for manipulation
  of files
- [ ] implement data in a struct/class
  - [ ] metadata could be put in a struct
  - [ ] data could be put in a class with private and public functions for
    fitting, constructors, getters, setters, etc...

### Fitting steps
- [ ] select the values that are >0 and <1000 and put them in a container
- [ ] implement linear minimization --> look on Guidi's lectures
- [ ] provide parameters a,b and errors
- [ ] build function to perform fit

## Workflow for an efficient class-building
1. list all the things you need to compute, try to organize them but don't be overly strict
2. list all the methods, with their approximate signatures, needed for computations
3. build the class one part at a time, compile, run and debug.
