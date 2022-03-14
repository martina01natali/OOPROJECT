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
int main()  // This may seem stupid, but it is COMPULSORY to call the main
            // function main(). Not doing it leads to the error "undefined reference to `WinMain'".
{
    // User control section
    std::cout   << "Enter path to file to process\n";
    std::string FILEPATH {};
    std::cin    >> FILEPATH;
    std::cout   << "You entered: " << "\"" + FILEPATH + "\"\n";

    // Reading file and preparing std::vector of lines of file
    Claro targetfile {FILEPATH};
    DataStruct data = targetfile.xyData();
    DataStruct fit_results = targetfile.linear_fit(0,950);

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

    // Support functions
    // float meanx = mean(data.x);
    // float varx = var(data.x);
    // float covarxy = covar(data.x,data.y);
    // float a {aCoeff(data.x,data.y)};
    // float b {bCoeff(data.x,data.y)};
    // float rquadro {rsq(data.x,data.y)};
    // float sigma {sigmasq(data.x,data.y)};

    // std::cout << a << std::endl;
    // std::cout << b << std::endl;
    // std::cout << sigma << std::endl;
    // std::cout << rquadro << std::endl;
    // std::cout << covarxy << std::endl;

    return 0;
}
