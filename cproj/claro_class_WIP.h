#include <iostream>
#include <cstring>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <stdio.h>

class Data
{
private:
    std::vector<float> x {};
    std::vector<float> y {};
    std::vector<float> y1 {};
    std::vector<float> linear {}; // vector of data to fit linearly
    std::vector<float> meta {};

    // Methods on above objects
    // float self.Var ( return Var(x)) // implemented as a method that takes std::vector as parameters
    // float self.Cov ( return Cov(x,y))
    // float self.se (std::vector<float> data) { return se } // returns sum of squared errors
    // float self.ss (std::vector<float> data) { return se }// returns sum of squares

    // the following may be aggregated in a struct
    float a {}; // angular coefficient
    float b {}; // intercept
    float sigma2 {}; // variance of errors --> needed to compute variance on parameters
    float r2 {}; // estimator of correlation coefficient

    // Methods on above objects
    // float a.Var // specific method to return Var of a
    // float b.Var // specific method to return Var of b
    // float sigma


public:

protected:

};
