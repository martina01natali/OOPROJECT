#include <iostream>
#include <iomanip>
#include <cstring>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <stdio.h>
#include "Claro.h"

using namespace std;

//----------------------------------------------------------------------------//
int main()
{
    // User control section
    std::cout   << "Enter path to file to process\n";
    std::string FILEPATH {};
    std::cin    >> FILEPATH;
    std::cout   << "You entered: " << "\"" + FILEPATH + "\"\n";

    // Reading file and fitting linearly data in given range of values of y
    Claro targetfile {FILEPATH};
    DataStruct data = targetfile.xyData();
    DataStruct fit_results = targetfile.linear_fit(0,950);
    // auto [a,b,sigma,rsq] = fit_results; // structured binding is available only from c++17 on, but I don't have it :)

    std::ofstream outf("fit_results.txt", std::ios::out);
    if (outf.is_open()) {
        outf << "********* Fit results *********" << '\n';
        outf << std::scientific;
        outf << std::setprecision(2) << "angular coeff (a): " << fit_results.x1.at(0) << " +- " << fit_results.x1.at(1) << '\n';
        outf << std::setprecision(2) << "intercept (b): " << fit_results.x2.at(0) << " +- " << fit_results.x2.at(1) << '\n';
        outf << std::fixed;
        outf << "sigma2: " << fit_results.y1.at(0) << '\n';
        outf << std::setprecision(2) << "r2: " << fit_results.y2.at(0) << '\n';
        outf.close();
    }

    // Support functions calls
    // float meanx = mean(data.x);
    // float varx = var(data.x);
    // float covarxy = covar(data.x,data.y);
    // float a {aCoeff(data.x,data.y)};
    // float b {bCoeff(data.x,data.y)};
    // float rquadro {rsq(data.x,data.y)};
    // float sigma {sigmasq(data.x,data.y)};

    return 0;
}
