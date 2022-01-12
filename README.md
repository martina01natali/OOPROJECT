# README

## c++ projects

**GIT BRANCH OF CHOICE**: `local`

**WARNING**: it is better to start this project, or at least the chi-squared minimization, after having completed the python project

c++: 1 file in claro, read it (using std library), mettere parametri in container appropriati e provate a fare il fit lineare a mano con minimizzazione dei quadrati dei tre punti di mezzo con le y tra 0 e 1000. Use the most modern c++ syntax you can; passa argomenti by ref or by const ref

Goals and subgoals
- [x] create program to read 1 file
- [ ] update program to read all the files (all the absolute paths to the 
  files) from a file that contains paths to good files only, produced by 
  bash script or python
- [ ] select "middle" data (!= 0 && !=1000) and fit linearly with chi-squared minimization
